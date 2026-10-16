"""Target base class + registry. Target = device tech + sim + flow."""

from pathlib import Path


class Target:
    name = "abstract"
    required_keys: list[str] = []

    def evaluate(self, cfg: dict, out_dir: Path) -> dict:
        """One loop round for this target. Returns exactly
        {"sim": dict, "flow": dict, "config": cfg}."""
        raise NotImplementedError


def get_target(name: str) -> Target:
    if name == "digital":
        from targets.digital.evaluate import DigitalTarget
        return DigitalTarget()
    if name == "photonic":
        from targets.photonic.evaluate import PhotonicTarget
        return PhotonicTarget()
    if name == "memristive":
        from targets.memristive.evaluate import MemristiveTarget
        return MemristiveTarget()
    raise KeyError(f"unknown target: {name!r} (digital|photonic|memristive)")