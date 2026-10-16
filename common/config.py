"""Config validation shared by orchestrator and targets."""

REQUIRED_KEYS: dict[str, list[str]] = {
    "digital": ["neurons", "fanout", "weight_width", "timesteps", "util_target", "clock_ns"],
    "photonic": ["mesh_depth", "precision_bits", "laser_mw", "wavelength_nm"],
    "memristive": ["xbar_rows", "xbar_cols", "variability_frac", "adc_bits"],
}

_RAM_WARN_BYTES = 5 * 1024 * 1024 * 1024  # 5 GB of a 8 GB WSL box


def estimate_digital_rams(cfg: dict) -> int:
    """Bytes of synapse state a digital config needs: neurons*fanout*weight_width*timesteps."""
    return int(cfg["neurons"]) * int(cfg["fanout"]) * int(cfg["weight_width"]) * int(cfg["timesteps"])


def validate_config(target: str, cfg: dict) -> list[str]:
    """Return warnings about cfg. Never raises except unknown target."""
    if target not in REQUIRED_KEYS:
        raise KeyError(target)
    warnings: list[str] = []
    for key in REQUIRED_KEYS[target]:
        if key not in cfg:
            warnings.append(f"missing-key:{key}")
    if target == "digital" and all(k in cfg for k in REQUIRED_KEYS["digital"]):
        if estimate_digital_rams(cfg) > _RAM_WARN_BYTES:
            warnings.append(
                f"ram-ceiling: estimate {estimate_digital_rams(cfg) / 2**30:.1f} GiB exceeds 5 GiB "
                "on this 8 GB host"
            )
    return warnings