# Dense-ROM baseline, 128 neurons, against the external-SRAM design (#2)

Text written in ASD-STE100 Simplified Technical English.

Date: 2026-10-18. Commits: 175c76c (`weight_store: rom`), 1968f2e
(`SYNTH_MEMORY_MAX_BITS`). Image: `openroad/orfs:latest` d4590b320d36.
Config: neurons=128, fanout=8, weight_width=4, timesteps=64, util_target=25,
clock_ns=40.0, weight_store=rom. This is the same config as the external run of
2026-10-18 (`inv = f6599c24`), plus `weight_store`.

Command: `orchestrator.py --target digital --rounds 1 --out runs_rom128
--seed-config '{... "weight_store": "rom"}'`. Files:
`2026-10-18-rom-docker_cmd.txt`, `2026-10-18-rom-journal-line.json`
(`inv = 15914a90`), `2026-10-18-rom-metadata.json`. Parity sim: pass.
Wall time: 103 min (21:20 to 23:03 CEST). GDS: 75,833,468 bytes, sha256
b931030b22da1975…, at `runs_rom128/digital/round_0/inv_15914a90/final.gds`
(not in git).

The first attempt (`inv = 8eba745c`) stopped in synthesis: "Synthesized memory
size 4096 exceeds SYNTH_MEMORY_MAX_BITS". 1968f2e fixed it.

## Same keys, two runs

| Metric | Key | External SRAM | Dense ROM | ROM / external |
|---|---|---|---|---|
| Design area (um²) | `finish__design__instance__area__stdcell` | 704,933 | 743,245 | 1.054 |
| Total power (W) | `finish__power__total` | 0.0141645 | 0.0137524 | 0.971 |
| Wirelength (um) | `detailedroute__route__wirelength` | 1,449,559 | 1,826,253 | 1.260 |
| Setup slack at 40 ns (ns) | `finish__timing__setup__ws` | +33.1432 | +32.3965 | 0.977 |
| DRC | `detailedroute__route__drc_errors` | 0 | 0 | |
| Hold slack (ns) | `finish__timing__hold__ws` | +0.2743 | +0.2712 | |
| Die area (um²) | `finish__design__die__area` | 2,540,310 | 2,677,480 | 1.054 |
| Std cells | `finish__design__instance__count__stdcell` | 81,156 | 86,275 | 1.063 |
| Synth area (um²) | `synth__design__instance__area__stdcell` | 633,486 | 667,733 | 1.054 |
| Utilization | `finish__design__instance__utilization` | 0.2789 | 0.2789 | |

Log lines (ROM run): `Design area 743245 um^2 28% utilization.`,
`[INFO DRT-0199]   Number of violations = 0.`

Both runs use util 25. Thus the die size follows the cell area, and the
floorplans are not identical: the ROM die is 5.4% larger.

## How to read this

1. **The ROM is mostly removed by synthesis.** 65,536 ROM bits add only
   34,247 um² of synthesized cells (+5.4%). With fanout 8, each neuron has 8
   non-zero weights out of 128. Thus about 94% of the ROM bits are constant
   zero, and yosys removes their logic. This baseline is "sparse weights folded
   into logic", not a dense memory.
2. **The external design area does not include its weight memory.** That memory
   is 65,536 bits in an external SRAM, plus a 512-bit input port. We do not
   invent an SRAM macro area. A rough figure from the literature is about
   0.44 mm² for an OpenRAM 6T macro on sky130hd (see the wiki summary on CMOS
   compute-in-memory). Thus the ROM design (0.743 mm², weights included) is
   probably smaller than the external design plus its SRAM.
3. **The ROM costs wire: +26% routed wirelength.** The ROM logic for each word
   must reach all 128 accumulators.
4. **Power is 2.9% lower for the ROM.** A possible cause is the switching
   activity that the power tool assumes on the 512 external input pins. Not
   verified.
5. **Timing is the same within 0.75 ns.** Both have more than 32 ns of slack
   at 40 ns.

The result does not show that the fabric beats a dense ROM. A real dense test
needs non-zero weights everywhere (for example fanout = neurons).
