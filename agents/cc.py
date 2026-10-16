"""Claude-Code agent backend: shells out to `claude -p` for configs + notes.

Contract with the loop: propose_config is total — any failure (nonzero exit,
timeout, non-JSON output, missing keys) falls back to the journal's latest
config for the target, else None. analyze_failure returns raw text.
"""

import json
import re
import subprocess
from pathlib import Path

from agents.base import Backend
from common.config import REQUIRED_KEYS

_JSON_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


class CcBackend(Backend):
    def __init__(self, journal_path: Path, binary: str = "claude",
                 timeout_s: int = 600):
        self.journal_path = Path(journal_path)
        self.binary = binary
        self.timeout_s = timeout_s

    def _shell(self, prompt: str) -> str | None:
        try:
            proc = subprocess.run(
                [self.binary, "-p", prompt], capture_output=True, text=True,
                timeout=self.timeout_s)
        except (subprocess.TimeoutExpired, OSError):
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout

    def _fallback(self, journal_tail: list[dict], target: str) -> dict | None:
        for rec in reversed(journal_tail):
            if rec.get("target") == target and rec.get("config"):
                return rec["config"]
        return None

    @staticmethod
    def _last_json(text: str) -> dict | None:
        if not text:
            return None
        last = None
        for m in _JSON_RE.finditer(text):
            try:
                obj = json.loads(m.group(0))
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                last = obj
        return last

    def _coerce(self, cfg: dict, target: str) -> dict:
        out = {}
        for k, v in cfg.items():
            if k in ("neurons", "fanout", "weight_width", "timesteps",
                     "util_target", "mesh_depth", "precision_bits",
                     "xbar_rows", "xbar_cols", "adc_bits"):
                out[k] = int(float(v))
            elif k == "variability_frac":
                out[k] = float(v)
            else:
                out[k] = v
        return out

    def propose_config(self, journal_tail: list[dict], target: str) -> dict | None:
        keys = ", ".join(REQUIRED_KEYS[target])
        hist = json.dumps(journal_tail[-5:], default=str)
        prompt = (
            f"You are the agent in an autonomous chip-design loop, target={target}.\n"
            f"Journal (last rounds): {hist}\n"
            f"Propose the NEXT config as a single flat JSON object with exactly these keys: {keys}. "
            "Vary one or two knobs from the last config; respond with ONLY the JSON object."
        )
        out = self._shell(prompt)
        cfg = None
        if out:
            last = self._last_json(out)
            if last is not None and all(k in last for k in REQUIRED_KEYS[target]):
                cfg = self._coerce(last, target)
        return cfg if cfg is not None else self._fallback(journal_tail, target)

    def analyze_failure(self, stage: str, logs: str, cfg: dict) -> str:
        prompt = (
            f"Stage '{stage}' failed in a chip design loop with config {cfg}.\n"
            f"Last log lines:\n{logs[-2000:]}\n"
            "Diagnose in under 120 words what to change next."
        )
        out = self._shell(prompt)
        return out.strip() if out and out.strip() else "no analysis"