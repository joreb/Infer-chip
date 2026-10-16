"""Orchestrator: the one agentic loop over all three device targets.

Round cycle: propose -> validate -> evaluate -> journal append. Stops on
rounds exhausted or backend returning None. Never raises out of the loop —
failures become verdict dicts (spec ruling), journal is written even when
every round fails.
"""

import argparse
import json
import sys
from pathlib import Path

from agents.base import Backend
from agents.stub import StubBackend
from common.config import validate_config
from common.journal import Journal
from targets.base import get_target

RETRIES = 2  # bounded retries per round (spec)


def _valid(target: str, cfg: dict | None) -> bool:
    return isinstance(cfg, dict) and not [w for w in validate_config(target, cfg)
                                          if w.startswith("missing-key")]


def run_loop(target: str, backend: Backend, rounds: int, out_root: Path,
             config_override: dict | None = None, retries: int = RETRIES) -> Path:
    tgt = get_target(target)
    journal = Journal(Path(out_root) / f"{target}" / "journal.jsonl")
    cfg: dict | None = None
    note = ""

    for round_i in range(rounds):
        proposed = backend.propose_config(journal.tail(5), target)
        if proposed is None and not config_override and cfg is not None:
            break  # backend says stop; config_override backfills per Task 14 ruling
        candidate = proposed if isinstance(proposed, dict) else cfg

        if _valid(target, candidate):
            cfg = dict(candidate)
            note = ""
        else:
            # first round without config -> DEFAULT_CFG; later -> keep previous
            if cfg is None:
                cfg = dict(getattr(tgt, "DEFAULT_CFG", {}))
                note = "proposed config invalid; fell back to DEFAULT_CFG"
            else:
                note = "proposed config invalid; kept previous config"
        if config_override:
            cfg.update(config_override)

        for w in validate_config(target, cfg):
            if w.startswith("weight-memory"):
                print(f"WARNING: {w} for {target} config; proceeding anyway",
                      file=sys.stderr)

        run_dir = Path(out_root) / target / f"round_{round_i}"
        run_dir.mkdir(parents=True, exist_ok=True)
        try:
            result = tgt.evaluate(cfg, run_dir)
        except Exception as exc:  # OOM, missing tool, whatever: a verdict, never out of the loop
            result = {"sim": {"verdict": "fail", "reason": f"{type(exc).__name__}: {exc}"},
                      "flow": {"verdict": "skipped", "reason": "sim failed"}}

        failed_stage = next((s for s in ("sim", "flow")
                             if result.get(s, {}).get("verdict") == "fail"), None)
        if failed_stage:
            logs = json.dumps(result.get(failed_stage, {}), default=str)
            note = backend.analyze_failure(failed_stage, logs, cfg)

        journal.append({"round": round_i, "target": target, "config": cfg,
                        "sim": result["sim"], "flow": result["flow"],
                        "agent_note": note})
    return journal.path


def main() -> None:
    ap = argparse.ArgumentParser(description="agentic SNN chip design loop")
    ap.add_argument("--target", required=True,
                    choices=["digital", "photonic", "memristive"])
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--backend", default="stub",
                    choices=["stub", "cc", "api"])
    ap.add_argument("--seed-config", default="",
                    help="JSON dict overriding configs each round")
    ap.add_argument("--out", default="runs")
    args = ap.parse_args()
    override = json.loads(args.seed_config) if args.seed_config else None
    backend = StubBackend() if args.backend == "stub" else None
    if backend is None:
        from agents.base import get_backend
        try:
            backend = get_backend(args.backend,
                                  journal_path=Path(args.out) / args.target / "journal.jsonl")
        except KeyError as exc:  # e.g. "api" deferred to stage-1
            print(f"error: {exc.args[0]}", file=sys.stderr)
            raise SystemExit(2)
    jp = run_loop(args.target, backend, args.rounds, Path(args.out), override)
    print(f"journal: {jp}")


if __name__ == "__main__":
    main()