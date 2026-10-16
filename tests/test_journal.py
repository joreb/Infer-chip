"""Journal JSONL spine tests (malformed-line tolerant)."""

import json
from pathlib import Path

from common.journal import Journal


def _rec(round_: int, target: str = "digital") -> dict:
    return {"round": round_, "target": target, "config": {}, "sim": {}, "flow": {}, "agent_note": ""}


def test_append_tail_entries(tmp_path):
    j = Journal(tmp_path / "journal.jsonl")
    for i in range(3):
        j.append(_rec(i))
    j.append(_rec(10, "photonic"))
    assert [e["round"] for e in j.tail(2)] == [2, 10]
    assert len(j.entries("digital")) == 3
    assert len(j.entries("photonic")) == 1
    assert j.entries() [0]["round"] == 0


def test_malformed_lines_skipped(tmp_path):
    p = tmp_path / "journal.jsonl"
    p.write_text(
        json.dumps(_rec(0, "digital")) + "\n"
        + "not json at all\n"
        + json.dumps({"round": 2}) + "\n"  # missing target
        + json.dumps(_rec(3, "digital")) + "\n"
    )
    j = Journal(p)
    assert [e["round"] for e in j.entries("digital")] == [0, 3]
    assert j.tail(1)[0]["round"] == 3