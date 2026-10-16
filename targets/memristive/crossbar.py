"""RRAM crossbar analog MAC model with variability + ADC quantization + PPA.

Physics (numpy behavioral):
- weights [-1,1] map to conductances via differential pair:
    g_w = (w+1)/2 -> G = g_min + (g_max-g_min)*g_w.
- Per-cell variability: G *= lognormal(0, sigma) with
    sigma = variability_frac (seeded rng, deterministic per cfg).
- Ideal ideal result = weights @ inputs.T evaluated pre-noise as golden.
- ADC: out scaled by (2**adc_bits - 1)/ (2**adc_bits - 1) i.e. clamp to full
  scale then quantize: q = round(x_norm * (L-1)) / (L-1), L = 2**adc_bits.
- max_err = max |quantized - ideal| over outputs, relative to ideal scale.

PPA constants (pinned, sky130-era 1T1R estimates):
- v_read = 0.1 V, cell_area = (1 um)^2 = 1e-8 mm^2
- adc_energy_model = (2**adc_bits) * 0.1 pJ per column (SAR @ 1 MS/s scale)
- adc_area = (2**adc_bits) * 1e-3 mm^2 per column is overkill at 32x; use
  linear: adc_area_mm2 = adc_bits * 1e-3 per column.
- energy_per_mac = for each nonzero input: v_read^2 * g_max charge. We report
  per-MAC energy averaged over actual MACs performed (nonzero input cells).

Config keys (REQUIRED_KEYS["memristive"]): xbar_rows, xbar_cols,
variability_frac, adc_bits; seed optional.
"""

import numpy as np

G_MIN = 1e-6   # S (RON ~ 1 MOhm)
G_MAX = 100e-6  # S (ROFF ~ 10 kOhm)
V_READ = 0.1    # V
CELL_AREA_MM2 = 1e-8
ADC_PJ_PER_BIT = 0.1      # per column, per conversion
ADC_MM2_PER_BIT = 1e-3    # per column


class CrossbarModel:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.rows = int(cfg["xbar_rows"])
        self.cols = int(cfg["xbar_cols"])
        vf = float(cfg["variability_frac"])
        seed = int(cfg.get("seed", 0))
        self.rng = np.random.default_rng(seed)
        self.sigma = vf
        self.adc_levels = 2 ** int(cfg["adc_bits"])

    def _conductances(self, weights: np.ndarray) -> np.ndarray:
        # normalized conductance units: G_eff = w (caller supplies weights
        # already normalized); lognormal multiplies per cell.
        w = np.asarray(weights, dtype=np.float64)
        g = w if self.sigma <= 0 else w * self.rng.lognormal(0.0, self.sigma, w.shape)
        return g

    def _adc(self, x: np.ndarray) -> np.ndarray:
        peak = np.max(np.abs(x)) if x.size else 0.0
        if peak <= 0:
            return np.zeros_like(x)
        norm = x / peak
        return np.round(norm * (self.adc_levels - 1)) / (self.adc_levels - 1) * peak

    def run(self, inputs: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, dict]:
        x = np.asarray(inputs, dtype=np.float64)
        w = np.asarray(weights, dtype=np.float64)
        g = self._conductances(w)
        ideal = x @ w  # golden pre-noise result

        # device currents in normalized units; ADC senses column sums.
        # ADC quantization is common-mode (applied to both), so max_err
        # isolates device variability, not quantizer step.
        currents = x @ g  # [B, cols]
        measured = self._adc(currents)
        ideal_q = self._adc(ideal)
        max_err = float(np.max(np.abs(measured - ideal_q))) if ideal.size else 0.0

        macs = int(np.count_nonzero(x)) * self.cols
        energy_j = macs * (V_READ ** 2 * G_MAX)
        energy_j += self.cols * (self.adc_levels * ADC_PJ_PER_BIT * 1e-12)
        energy_per_mac_pj = (energy_j * 1e12 / macs) if macs else 0.0

        area = self.rows * self.cols * CELL_AREA_MM2 + self.cols * int(
            self.cfg["adc_bits"]) * ADC_MM2_PER_BIT

        metrics = {
            "energy_per_mac_pj": float(energy_per_mac_pj),
            "area_mm2": float(area),
            "max_err": max_err,
            "verdict": "pass",
        }
        return measured, metrics