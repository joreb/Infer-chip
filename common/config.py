"""Config validation shared by orchestrator and targets."""

REQUIRED_KEYS: dict[str, list[str]] = {
    "digital": ["neurons", "fanout", "weight_width", "timesteps", "util_target", "clock_ns"],
    "photonic": ["mesh_depth", "precision_bits", "laser_mw", "wavelength_nm"],
    "memristive": ["xbar_rows", "xbar_cols", "variability_frac", "adc_bits"],
}

_WEIGHT_MEM_WARN_BITS = 4 * 1024 * 1024  # 4 Mbit external-SRAM ballpark


def estimate_weight_memory_bits(cfg: dict) -> int:
    """External weight SRAM (docs/openspike-memory-interface.md): pad words of
    pad*weight_width bits. Dense by construction — the port addresses every
    source — so fanout does not shrink it."""
    n = int(cfg["neurons"])
    p = 2
    while p < n:
        p *= 2
    return p * p * int(cfg["weight_width"])


def validate_config(target: str, cfg: dict) -> list[str]:
    """Return warnings about cfg. Never raises except unknown target."""
    if target not in REQUIRED_KEYS:
        raise KeyError(target)
    warnings: list[str] = []
    for key in REQUIRED_KEYS[target]:
        if key not in cfg:
            warnings.append(f"missing-key:{key}")
    if target == "digital" and all(k in cfg for k in REQUIRED_KEYS["digital"]):
        if int(cfg["weight_width"]) > 8:
            warnings.append(
                f"weight_width:{int(cfg['weight_width'])} exceeds 8 bits — "
                "RTL compare-stage 32-bit intermediates may overflow; parity "
                "with the golden model is not guaranteed"
            )
        if estimate_weight_memory_bits(cfg) > _WEIGHT_MEM_WARN_BITS:
            bits = estimate_weight_memory_bits(cfg)
            warnings.append(
                f"weight-memory: SRAM image {bits / 2**20:.1f} Mbit exceeds "
                f"{_WEIGHT_MEM_WARN_BITS // 2**20} Mbit (256 neurons at ww=4 is 0.25 Mbit for scale)"
            )
    return warnings