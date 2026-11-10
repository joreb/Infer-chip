import argparse
import os
import secrets
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from targets.digital.flow import container_script, parse_metrics

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run ORFS on a pre-staged <out>/orfs design directory")
    parser.add_argument("--out", type=Path,
                        default=REPO / "runs_complex128_macro_gds" / "run")
    parser.add_argument("--name", default="complex128_gpu_128")
    parser.add_argument("--timeout", type=int, default=14400)
    args = parser.parse_args()
    OUT = args.out.resolve()
    NAME = args.name

    final_gds = OUT / "final.gds"
    if final_gds.exists():
        final_gds.unlink()
    results_host = OUT / "results"
    if results_host.exists():
        shutil.rmtree(results_host)
    results_host.mkdir(parents=True, exist_ok=True)

    container = f"orfs-macro-{NAME}-{secrets.token_hex(4)}"
    cmd = container_script(NAME, os.getuid(), os.getgid())
    docker_cmd = [
        "docker", "run", "--rm", "--name", container, "-u", "0:0",
        "-v", f"{OUT / 'orfs'}:/mnt/design",
        "-v", f"{results_host}:/results",
        "openroad/orfs:latest", "bash", "-c", cmd,
    ]
    (OUT / "docker_cmd.txt").write_text(
        " ".join(map(shlex.quote, docker_cmd)) + "\n")
    print(f"Running macro PnR for {NAME}...")
    try:
        proc = subprocess.run(docker_cmd, capture_output=True, text=True,
                              timeout=args.timeout)
    except subprocess.TimeoutExpired as exc:
        subprocess.run(["docker", "kill", container], capture_output=True, text=True)
        print(f"ORFS timeout after {exc.timeout}s; killed {container}")
        print(exc.output or "")
        print(exc.stderr or "")
        return 124

    print("docker rc:", proc.returncode)
    print(proc.stdout[-4000:])
    print(proc.stderr[-4000:])
    if proc.returncode:
        return proc.returncode

    metrics = parse_metrics(results_host / NAME / "base")
    print("metrics:", metrics)
    gds = results_host / NAME / "base" / "6_final.gds"
    if metrics.get("verdict") != "pass" or not gds.exists():
        print("No fresh GDSII with passing metrics")
        return 1
    shutil.copy(gds, final_gds)
    print("GDS:", final_gds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
