"""Pareto front + markdown report generator over the design journal."""

import json
import math
from pathlib import Path

# per-target PPA axes (x, y), both minimized, matching plan/spec tables
AXES: dict[str, tuple[str, str]] = {
    "digital": ("area_mm2", "pwr_w"),
    "photonic": ("footprint_mm2", "energy_per_mac_pj"),
    "memristive": ("max_err", "energy_per_mac_pj"),
}


def _num(v) -> float | None:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    f = float(v)
    return None if math.isnan(f) else f


def _metric(rec: dict, key: str) -> float | None:
    for section in ("flow", "sim"):
        v = _num((rec.get(section) or {}).get(key))
        if v is not None:
            return v
    return None


def pareto_front(entries: list[dict], x: str, y: str) -> list[dict]:
    pts = [(e, _metric(e, x), _metric(e, y)) for e in entries if isinstance(e, dict)]
    pts = [(e, px, py) for e, px, py in pts if px is not None and py is not None]
    front = []
    for e, px, py in pts:
        dominated = any(
            (ox <= px and oy <= py) and (ox < px or oy < py)
            for o, ox, oy in pts if o is not e)
        if not dominated:
            front.append(e)
    return front


def _plot(recs: list[dict], x: str, y: str, png_path: Path) -> bool:
    pts = [(e, _metric(e, x), _metric(e, y)) for e in recs if isinstance(e, dict)]
    pts = [(e, px, py) for e, px, py in pts if px is not None and py is not None]
    if len(pts) < 2:
        return False
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    front = set(id(e) for e in pareto_front([e for e, _, _ in pts], x, y))
    fig, ax = plt.subplots(figsize=(4, 3))
    for e, px, py in pts:
        on_front = id(e) in front
        ax.scatter(px, py, marker="o", color="crimson" if on_front else "tab:blue")
        ax.annotate(str(e["round"]), (px, py), fontsize=7)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"Pareto front: {x} vs {y}")
    fig.tight_layout()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=110)
    plt.close(fig)
    return True


def write_report(journal_path: Path, out_md: Path) -> Path:
    entries = []
    for line in Path(journal_path).read_text().splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and "round" in rec and "target" in rec:
            entries.append(rec)

    lines = ["# Agentic design-loop report", ""]
    for target in sorted({e["target"] for e in entries}):
        recs = [e for e in entries if e["target"] == target]
        lines.append(f"## {target}")
        lines.append("")
        lines.append("| round | config | sim | flow | metrics | agent_note |")
        lines.append("|---|---|---|---|---|---|")
        for e in recs:
            cfg = json.dumps(e.get("config", {}), default=str)
            sim = (e.get("sim") or {}).get("verdict", "?")
            flow = (e.get("flow") or {}).get("verdict", "?")
            flowm = {k: v for k, v in (e.get("flow") or {}).items()
                     if k != "verdict" and v is not None}
            simm = {k: v for k, v in (e.get("sim") or {}).items()
                    if k != "verdict" and v is not None}
            metrics = json.dumps({**simm, **flowm}, default=str)
            note = (e.get("agent_note") or "").replace("|", "\\|")
            lines.append(f"| {e['round']} | `{cfg}` | {sim} | {flow} | `{metrics}` | {note} |")

        if target in AXES:
            x, y = AXES[target]
            front = pareto_front(recs, x, y)
            if front:
                pts = ", ".join(
                    f"({e['round']}: {_metric(e, x):.4g}, {_metric(e, y):.4g})"
                    for e in sorted(front, key=lambda e: e["round"]))
                lines += ["", f"Pareto front ({x} vs {y}, minimized): {pts}"]
            png = out_md.with_suffix("") / f"pareto_{target}.png"
            if _plot(recs, x, y, png):
                lines += ["", f"![Pareto {target}]({png.name})"]
        lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n")
    return out_md