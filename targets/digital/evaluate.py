"""DigitalTarget.evaluate: cocotb parity sim (Task 4 runner) then ORFS flow.

Sim delegates to the Task 4 pytest harness logic: run the cocotb parity test
programmatically via cocotb_tools.runner on a small generated TB. If sim fails,
flow short-circuits with {"verdict": "skipped", "reason": "sim failed"}.
"""

import json
from pathlib import Path

from targets.base import Target
from targets.digital.flow import run_pnr
from targets.digital.rtl_gen import generate_rtl, module_name, pad_size
from common.config import estimate_weight_memory_bits


# OpenSpike-informed defaults (docs/openspike-memory-interface.md): the fabric
# is a 16-way mux over PAD*WW bus bits, short critical path — 40 ns (25 MHz)
# is a conservative floorplan target; low utilization leaves routing room.
DEFAULT_CFG = {"neurons": 256, "fanout": 8, "weight_width": 4, "timesteps": 64,
               "util_target": 20, "clock_ns": 40.0}


class DigitalTarget(Target):
    name = "digital"
    required_keys = ["neurons", "fanout", "weight_width", "timesteps",
                     "util_target", "clock_ns"]
    DEFAULT_CFG = DEFAULT_CFG

    def _run_sim(self, cfg: dict, out_dir: Path) -> dict:
        """cocotb parity sim, reusing Task 4 harness structure."""
        # lazy import keeps dockerless unit tests light
        from cocotb_tools.runner import get_runner

        iverilog = __import__("shutil").which("iverilog")
        if iverilog is None:
            return {"verdict": "fail", "reason": "iverilog not installed"}

        build_dir = Path(out_dir) / "sim_build"
        build_dir.mkdir(parents=True, exist_ok=True)
        rtl = build_dir / f"{module_name(cfg)}.v"
        rtl.write_text(generate_rtl(cfg))

        runner = get_runner("icarus")
        runner.build(
            verilog_sources=[str(rtl)],
            hdl_toplevel=module_name(cfg),
            build_dir=str(build_dir),
        )
        test_dir = Path(__file__).resolve().parents[2] / "tests" / "digital"
        import sys
        sys.path.insert(0, str(test_dir))
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
        results_xml = runner.test(
            test_module="tb_parity",
            hdl_toplevel=module_name(cfg),
            build_dir=str(build_dir),
            extra_env={"PARITY_CFG_JSON": json.dumps(cfg)},
        )
        # cocotb 2.x returns the results.xml path; parse pass/fail from it
        from cocotb_tools.check_results import get_results
        num_tests, num_failed = get_results(Path(results_xml))
        # external-interface cost metrics (peer measure list, item 6): the bus
        # replaces the dense ROM area, so report it next to the PPA numbers
        pad = pad_size(cfg)
        bus_bits = pad * int(cfg["weight_width"])
        return {"verdict": "pass" if num_failed == 0 else "fail",
                "bus_bits": bus_bits,
                "weight_mbit": estimate_weight_memory_bits(cfg) / 2**20,
                "reason": None if num_failed == 0 else f"{num_failed}/{num_tests} cocotb tests failed",
                "num_tests": int(num_tests), "num_failed": int(num_failed)}

    def _run_flow(self, cfg: dict, out_dir: Path) -> dict:
        return run_pnr(cfg, out_dir)

    def evaluate(self, cfg: dict, out_dir: Path) -> dict:
        sim = self._run_sim(cfg, out_dir)
        if sim.get("verdict") == "fail":
            flow = {"verdict": "skipped", "reason": "sim failed"}
        else:
            flow = self._run_flow(cfg, out_dir)
        return {"sim": sim, "flow": flow, "config": cfg}