---
title: CMOS compute-in-memory
created: 2026-10-18
updated: 2026-10-18
type: summary
tags: [neuromorphic, snn, architecture, eda]
sources: []
status: open
---

# CMOS compute-in-memory

Text written in ASD-STE100 Simplified Technical English.

This page is a digest of a literature scan made on 2026-10-18 by a research agent. It tells what is
known about compute-in-memory (CIM) in standard CMOS, and which ideas fit our sky130 flow.
Memristive CIM (RRAM, PCM, MRAM, FeFET) is out of scope. The memristive target covers it.

## Background for beginners

**The problem that CIM solves.** In a normal design, the weights are in a memory and the arithmetic
is in a different place. Each operation moves a weight from the memory to the arithmetic. Moving
data often costs more energy than the arithmetic itself. Our core streams one 512-bit weight word
per source, 128 words per timestep, from an external SRAM to 128 accumulators.

**What CIM does.** CIM does the arithmetic inside the memory array, or directly beside it. The
weights do not move.

**Two types of CIM:**

- **Digital CIM.** Each memory cell has a small gate (AND or NOR) that multiplies one weight bit
  by one input bit. An adder tree adds the results. The result is exact.
- **Analog CIM.** Many rows are switched on at the same time. Each cell adds a current or a charge
  to a shared wire (the bitline). The total is the sum. An analog-to-digital converter (ADC) then
  reads the sum. This is fast and dense, but the ADC is expensive, and noise and variation make the
  result less precise.

**Why spikes help.** A spike is one bit: 1 or 0. The synaptic operation is "if spike, add the
weight". Thus there is no multiply, and no converter is necessary on the input side.

**TOPS/W.** Tera-operations per second per watt. Higher is better. Be careful: papers count
operations at different bit widths. A 1-bit × 1-bit number looks about 16 times better than a
4-bit × 4-bit number on the same macro. Compare only at the same precision, node and sparsity.

**Evidence labels on this page.** [Si] means measured on silicon. [Sim] means simulation or a
model. [Vendor] means a company claim without a published method. [Title] means the number comes
from the paper title or record, and the research agent did not read the measurement conditions.

## Main findings

1. **No measured standard-cell CIM on sky130 exists yet, but the open tools exist.** ORRAM is a
   standard-cell RAM generator in OpenROAD ([arXiv 2607.12244](https://arxiv.org/abs/2607.12244),
   placed and routed, no tapeout) [Sim]. Its sky130hd densities for 8 KB are in the table below.
   For our 65,536 bits, standard cells need about 2.0 to 4.2 mm². An OpenRAM 6T macro needs about
   0.44 mm². Thus standard-cell storage costs 5 to 10 times the area of an SRAM macro. Our library
   is sky130hs, which has larger cells than sky130hd.
2. **Digital CIM has no ADC and suits binary spikes.** The TSMC 22 nm macro (ISSCC 2021,
   DOI 10.1109/ISSCC42613.2021.9365766) uses a NOR gate per bit and an adder tree. It gives 89
   TOPS/W and 16.3 TOPS/mm² with 4-bit weights [Si, numbers Title]. With spikes as inputs, the
   bit-serial input loop disappears.
3. **Analog CIM loses much of its gain outside the array.** The Princeton 16 nm chip (ISSCC 2021)
   gives 121 TOPS/W at 4 bits, with an 8-bit ADC on each column [Si]. Per output, the array and ADC
   use 19.08 pJ. Buffers and digital post-processing add about 13 pJ more [Si]. EnCharge test chips
   give more than 150 TOPS/W at 8 bits, but the EN100 product gives up to 40 TOPS/W at 8 bits
   [Vendor].
4. **Measured SNN CIM chips are modest.** IMPULSE: 0.99 TOPS/W, 11-bit, 65 nm
   ([arXiv 2105.08217](https://arxiv.org/abs/2105.08217)) [Si]. SpiDR: up to 5 TOPS/W at 95% input
   sparsity, 65 nm ([arXiv 2411.02854](https://arxiv.org/abs/2411.02854)) [Si]. In these designs,
   the cost moves from the multiply to the membrane-potential update.
5. **A compute-in-ROM exists on sky130.** Ankhdjet
   ([arXiv 2608.26206](https://arxiv.org/abs/2608.26206)) compiles ternary weights into a via-mask
   ROM, with one transistor per weight at 2.21 µm². It is on Tiny Tapeout ttsky26c. Silicon is
   expected in 2027. Its energy numbers are simulated [Sim].

## Storage density on sky130hd (ORRAM paper, 8 KB, 64-bit words) [Sim]

| Storage | bits/mm² | Area for our 65,536 bits |
|---|---|---|
| ORRAM latch | 32,508 | about 2.0 mm² |
| ORRAM flip-flop | 28,677 | about 2.3 mm² |
| DFFRAM | 14,879 | about 4.4 mm² |
| Plain RTL through ORFS | 15,649 | about 4.2 mm² |
| OpenRAM 6T macro | 148,413 | about 0.44 mm² |

## SRAM CIM macros

| Work | Node | Precision | TOPS/W | Label |
|---|---|---|---|---|
| TSMC digital, ISSCC 2021 | 22 nm | 4-bit weights | 89 | Si, Title |
| TSMC, ISSCC 2024 | 3 nm | INT12 | 32.5 | Title |
| Princeton charge-domain, ISSCC 2021 | 16 nm | 4-bit | 121 | Si |
| C3SRAM (Seo and Seok, JSSC 2020) | 65 nm | 1-bit | 672 (divide by about 16 for a 4-bit estimate) | Si |
| CAP-RAM ([arXiv 2107.02388](https://arxiv.org/abs/2107.02388)) | 65 nm | programmable | 49.4 | Si |
| NeuDW-CIM ([arXiv 2606.08947](https://arxiv.org/abs/2606.08947)) | 65 nm | ternary, digital LIF | 0.8 pJ per synaptic operation | Si |

## Open tools for a digital flow

| Tool | What it does | Status |
|---|---|---|
| ORRAM ([arXiv 2607.12244](https://arxiv.org/abs/2607.12244)) | Standard-cell RAM in OpenROAD, sky130hd | Sim |
| OpenRAM | SRAM compiler with custom 6T cells, sky130 | Si, on shuttles |
| OpenACM ([arXiv 2601.11292](https://arxiv.org/abs/2601.11292)) | Digital CIM compiler with an OpenROAD flow, FreePDK45 | Sim |
| SynDCIM ([arXiv 2411.16806](https://arxiv.org/abs/2411.16806)) | Digital CIM compiler | Si, 40 nm |
| Ankhdjet ([arXiv 2608.26206](https://arxiv.org/abs/2608.26206)) | Ternary compute-in-ROM compiler, sky130 | Submitted, silicon in 2027 |

## Limits

- **The ADC cost.** In the ISAAC study, ADCs use about half of the chip area and power [Sim]. The
  research agent found no source for the "58% ADC power" figure that some texts give. Do not use it.
- **Noise.** Analog CIM accuracy has a limit that comes from the signal-to-noise ratio of the
  computation ([arXiv 2012.13645](https://arxiv.org/abs/2012.13645)) [Sim]. Digital CIM is exact.
- **Test chips are not products.** Almost all numbers come from test macros at the best voltage,
  sparsity and toggle rate.
- **Near-memory DRAM compute** (Samsung HBM-PIM, SK hynix AiM, UPMEM) does not fit a sky130 core.
  Its lesson is the same: keep the arithmetic beside the memory bank.

## Ideas we can test

| Experiment | Proves it | Kills it |
|---|---|---|
| Standard-cell CIM columns: each neuron keeps its 128 × 4-bit weights beside its accumulator, gated by the spike vector, summed by an adder tree | Cycles per timestep fall from up to 128 to 1 to 4, energy per timestep falls, slack stays positive | Area much larger than the baseline (storage alone is about 2 to 4 mm²), or negative slack from 128-input adder trees |
| Near-memory banks: same schedule, storage split into banks beside neuron groups | Routed wirelength and switching power fall at the same cycle count | Power does not fall, or area is above about 2 times the SRAM-macro baseline with no wirelength gain |
| Weights as logic (compute-in-ROM): each neuron input becomes a fixed sum of "spike AND constant", so synthesis removes the zero weights | Area at or below the ROM baseline, 1 cycle per timestep, lower power | Area grows faster than the count of non-zero weight bits, or routing fails |

The third idea already has a first data point. In the
[ROM against external SRAM comparison](../comparisons/rom-vs-external-sram-weights.md), synthesis
removed most of the 65,536 ROM bits, because the weights are sparse (fanout 8). The ROM design was
only 5.4% larger.

## Notes

The 18 cited arXiv papers are in `raw/papers/<arxiv id>.pdf` (downloaded 2026-10-18, git-ignored).
The title on page 1 of each 2026 PDF matches the title in this page. The numbers themselves come
from the research agent and were not checked again.

Related: [Fractal and hierarchical neuromorphic designs](fractal-and-hierarchical-neuromorphic-designs.md),
[index](../index.md).
