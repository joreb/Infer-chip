import json
import subprocess
import sys


def test_macro_driver_copies_fresh_gds(monkeypatch, tmp_path):
    from tools import complex128_macro_to_gds

    name = "complex128_unit"
    seen = {}

    def fake_orfs(cmd, **kwargs):
        seen["timeout"] = kwargs.get("timeout")
        seen["mount"] = cmd[cmd.index("-v") + 1]
        base = tmp_path / "results" / name / "base"
        base.mkdir(parents=True)
        (base / "metadata.json").write_text(json.dumps({
            "finish__timing__setup__ws": 1.0,
            "detailedroute__route__drc_errors": 0,
        }))
        (base / "6_final.gds").write_bytes(b"macro array gds")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(complex128_macro_to_gds.subprocess, "run", fake_orfs)
    monkeypatch.setattr(sys, "argv", [
        "complex128_macro_to_gds.py", "--out", str(tmp_path),
        "--name", name, "--timeout", "123",
    ])
    assert complex128_macro_to_gds.main() == 0
    assert (tmp_path / "final.gds").read_bytes() == b"macro array gds"
    assert seen["timeout"] == 123
    assert seen["mount"] == f"{tmp_path / 'orfs'}:/mnt/design"
