"""One-off debug: golden v trajectory dump + RTL gen for the tiny sim."""
from pathlib import Path

import numpy as np

from targets.digital.model import LIFModel, sample_weight_ints
from targets.digital.rtl_gen import generate_rtl, module_name

CFG = {"neurons": 8, "fanout": 3, "weight_width": 4, "timesteps": 12,
       "util_target": 60, "clock_ns": 4.0, "seed": 11}

d = Path("/tmp/dbg"); d.mkdir(exist_ok=True)
(d / "c.v").write_text(generate_rtl(CFG))
(d / "weights.txt").write_text(str(sample_weight_ints(CFG).tolist()))
m = LIFModel(CFG)
train = np.zeros((12, 8), dtype=np.int8)
train[1::2, 3] = 1
out = m.run(train)
lines = [f"gold t={t} out={[int(x) for x in out[t]]} v={[x for x in (m.get_state_v() * 16).astype(int).tolist()]}"
         for t in range(12)]
(d / "gold.txt").write_text("\n".join(lines))
print(module_name(CFG), "written")