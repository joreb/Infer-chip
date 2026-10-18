---
title: Weight storage hierarchy, from SSD to the core
created: 2026-10-18
updated: 2026-10-18
type: concept
tags: [snn, architecture, neuromorphic]
sources: []
status: open
---

# Weight storage hierarchy, from SSD to the core

Text written in ASD-STE100 Simplified Technical English.

This page tells where the weights of a neural network can be kept, and how they get to the
arithmetic. It answers two questions: "Can the core read its weights from an SSD or from DDR5?"
and "Can a 1-trillion-parameter model go on the chip?". GitHub issue #11 is the feature that
follows from it.

## Background for beginners

A memory has three properties that matter here:

- **Capacity.** How many bits it holds.
- **Latency.** The time from "give me this address" to "here is the data".
- **Bandwidth.** How many bytes per second it can give, when it streams.

Large memories are slow and small memories are fast. Thus a computer uses a hierarchy. It keeps
the data in a large, slow memory and copies the part that it needs now into a small, fast memory.

| Level | Typical capacity | Typical latency | Keeps data with power off |
|---|---|---|---|
| On-chip SRAM or ROM | kB to MB (a full wafer: tens of GB) | 1 clock cycle | SRAM no, ROM yes |
| DDR5 DRAM | GB to TB | about 15 to 50 ns, not constant | No |
| HBM (DRAM stacked beside the chip) | tens of GB per stack | similar to DDR, much more bandwidth | No |
| SSD (NVMe flash) | TB | about 50 to 100 µs, reads 4 KB blocks | Yes |

These are typical industry values, given for scale. They are not measured in this project.

## What our core needs

The core reads one 512-bit word in each clock cycle. At a 40 ns clock, that is 1.6 GB/s. The data
must come exactly one cycle after the address. There is no handshake. The generator docstring
says that a memory with a different latency breaks the design silently.

Thus:

- **An SSD cannot feed the core directly.** Its latency is about 1,000 times too long, and it
  needs PCIe and an NVMe controller.
- **DDR5 cannot feed the core directly.** Its latency is not constant. It needs a DDR5 controller
  and PHY, which the open sky130 flow does not have. The sky130 I/O pins are also too slow for
  DDR5.
- **On-chip memory can.** This is what the current design expects.

## The path that works: load, then run

```text
SSD (stores the weights) -> host CPU -> DDR5 (host RAM) -> SPI/QSPI -> on-chip SRAM -> core
```

The SSD keeps the weights when the power is off. The host reads the file into its DDR5, then
sends it to the chip over a slow serial link. The chip writes the words into its on-chip SRAM.
After the load, the core runs at full speed from on-chip memory.

For the current model, 128 neurons × 128 × 4 bits = 65,536 bits (8 KB). Over QSPI at 50 MHz
(25 MB/s), the load takes about 0.3 ms.

The cost is the on-chip memory. For 65,536 bits on sky130hd, the literature gives about 2.0 to
4.2 mm² in standard cells, and about 0.44 mm² as an OpenRAM macro
([CMOS compute-in-memory](../summaries/cmos-compute-in-memory.md)). The core logic itself is
0.705 mm² ([ROM against external SRAM](../comparisons/rom-vs-external-sram-weights.md)).

## When the model is too large for the chip: stream

If the weights do not fit on the chip, the chip must stream them from DRAM while it runs. Use two
on-chip buffers. The core reads one buffer while the next block loads into the other. The core
then needs a valid/ready handshake, so that it can wait when a word is late. This needs a real
DRAM controller, thus an FPGA with a hard DDR controller or a more advanced process.

## Scale check: a 1-trillion-parameter model on the chip

"1 T" can mean two things. Both are given here.

| Model size | Bits |
|---|---|
| 1 terabit (Tb) | 1 × 10^12 bits = 125 GB |
| 1 T parameters at 4 bits | 4 × 10^12 bits = 500 GB |
| 1 T parameters at 8 bits | 8 × 10^12 bits = 1 TB |

**On-chip SRAM area for 1 Tb.** This is arithmetic with the densities named, not a measurement.

| Process and memory | Density | Area for 1 Tb | 300 mm wafers (about 70,700 mm² each) |
|---|---|---|---|
| sky130, OpenRAM 6T macro | about 148,000 bits/mm² (ORRAM paper, Sim) | about 6.8 million mm² (6.8 m²) | about 95 |
| sky130, standard-cell latches | about 32,500 bits/mm² (ORRAM paper, Sim) | about 31 million mm² | about 435 |
| Leading-edge 3 nm SRAM | about 30 million bits/mm² (approximate industry value, not checked) | about 33,000 mm² | about 0.5 |

Thus a 1 T-parameter model at 4 bits needs about 2 wafers of SRAM even in a leading-edge node. In
sky130 it needs hundreds of wafers.

**What large systems do.** These are vendor figures given from memory for scale. They are not
checked in this project.

- A wafer-scale engine holds tens of GB of SRAM on one wafer. For larger models it streams the
  weights from an external memory unit.
- SRAM-only inference chips hold a few hundred MB each. A large model is split across hundreds or
  thousands of chips.
- GPUs keep the weights in HBM beside the chip and stream them. They do not keep the weights on
  the die.

**Mixture-of-experts helps.** Many 1 T-parameter reasoning models are mixture-of-experts models.
Only a small part of the parameters is active for each token (tens of billions, not one trillion).
The full model stays in DRAM or on SSD, and only the active experts move to the compute. At 4 bits,
32 billion active parameters are 16 GB per token. At 10 tokens per second, that is 160 GB/s, which
is HBM bandwidth.

**Verdict for this project.** A 1 T-parameter model cannot be stored on one chip, and not on a
sky130 chip at any size. The realistic design is a compute tile that streams weights from DRAM or
HBM, with flash for storage. Our core can be that tile if it gets the streaming interface above.
Spiking models at this scale do not exist yet
([LLMs on SNN hardware](../tasks/musings/2026-10-17-llms-on-snn-hardware.md)).

## Next steps

1. GitHub #11: `weight_store: loaded`, an on-chip SRAM with a SPI write port, loaded from a file.
2. Later: the valid/ready handshake and double buffering for streaming from DRAM.
3. Later: banked weight memory beside neuron clusters
   ([fractal and hierarchical designs](../summaries/fractal-and-hierarchical-neuromorphic-designs.md)).

Related: [index](../index.md).
