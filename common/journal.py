"""JSONL design journal — the loop's spine (spec: one record per round)."""

import json
from pathlib import Path


class Journal:
    def __init__(self, path: Path):
        self.path = Path(path)

    def append(self, rec: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a") as f:
            f.write(json.dumps(rec) + "\n")

    def _valid(self) -> list[dict]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(rec, dict) and "round" in rec and "target" in rec:
                out.append(rec)
        return out

    def tail(self, n: int) -> list[dict]:
        return self._valid()[-n:]

    def entries(self, target: str | None = None) -> list[dict]:
        return [r for r in self._valid() if target is None or r["target"] == target]