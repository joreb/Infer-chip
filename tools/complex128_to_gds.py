import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from targets.digital.flow import container_script, parse_metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate GDSII for complex128 RTL")
    parser.add_argument("--src", type=Path,
                        default=REPO / "spikes/complex128-unit/complex128_unit.v")
    parser.add_argument("--out", type=Path, default=REPO / "runs_complex128_gds")
    parser.add_argument("--name", default="complex128_unit")
    args = parser.parse_args()

    src = args.src.resolve()
    out = args.out.resolve()
    final_gds = out / "run" / "final.gds"
    if final_gds.exists():
        final_gds.unlink()
    stage = out / "run" / "orfs"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    combined = src.read_text()
    if src.name != "complex128_unit.v":
        combined = src.with_name("complex128_unit.v").read_text() + "\n" + combined
    (stage / "snn_core.v").write_text(combined)
    (stage / "snn_core.sdc").write_text(
        "create_clock -name clk -period 10.0 [get_ports clk]\n")

    name = args.name
    cfg_text = (
        f"export DESIGN_NAME = {name}\n"
        f"export DESIGN_NICKNAME = {name}\n"
        "export PLATFORM = sky130hs\n"
        "export VERILOG_FILES = ./designs/src/snn_core/snn_core.v\n"
        "export SDC_FILE = ./designs/src/snn_core/snn_core.sdc\n"
        "export CORE_UTILIZATION = 40\n"
        "export CLOCK_PERIOD = 10.0\n"
        "export CLOCK_PORT = clk\n"
    )
    if name == "complex128_gpu_128":
        cfg_text += (
            "export SYNTH_HIERARCHICAL = 1\n"
            "export SYNTH_KEEP_MODULES = complex128_unit\n"
        )
    (stage / "config.mk").write_text(cfg_text)

    uid = __import__("os").getuid()
    gid = __import__("os").getgid()
    results_host = out / "run" / "results"
    if results_host.exists():
        shutil.rmtree(results_host)
    results_host.mkdir(parents=True, exist_ok=True)

    cmd = container_script(name, uid, gid)
    container = f"orfs-{name}-{__import__('secrets').token_hex(4)}"
    docker_cmd = [
        "docker", "run", "--rm", "--name", container,
        "-u", "0:0",
        "-v", f"{stage.resolve()}:/mnt/design",
        "-v", f"{results_host.resolve()}:/results",
        "openroad/orfs:latest", "bash", "-c", cmd,
    ]
    print(f"Running PnR for {name}...")
    try:
        proc = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=7200)
    except subprocess.TimeoutExpired as exc:
        subprocess.run(["docker", "kill", container], capture_output=True, text=True)
        print(f"ORFS timeout after {exc.timeout}s; killed {container}")
        print(exc.output or "")
        print(exc.stderr or "")
        return 124
    print("docker rc:", proc.returncode)
    if proc.returncode != 0:
        print(proc.stdout[-4000:])
        print(proc.stderr[-4000:])
        return proc.returncode

    metrics = parse_metrics((results_host / name) / "base")
    print("metrics:", metrics)
    gds = (results_host / name) / "base" / "6_final.gds"
    if not gds.exists():
        print("No fresh GDSII produced")
        return 1
    if metrics.get("verdict") != "pass":
        print("GDSII withheld because metrics did not pass")
        return 1
    shutil.copy(gds, final_gds)
    print("GDS:", final_gds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
