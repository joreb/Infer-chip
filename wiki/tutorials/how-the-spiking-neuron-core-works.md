---
title: How the spiking neuron core works
created: 2026-10-18
updated: 2026-10-18
type: tutorial
tags: [snn, neuromorphic, rtl]
sources: []
---

# Tutorial 1: How the spiking neuron core works

Text written in ASD-STE100 Simplified Technical English.

**Goal.** After this tutorial, you can explain what the digital core of this project computes, one
timestep at a time. You can also find each part in the code.

**What you need.** No chip-design knowledge. Basic programming. Words in **bold** are in the
[glossary](../concepts/glossary.md).

## 1. A neuron that counts and fires

A **spiking neuron** keeps one number, the **membrane potential** (v). Each timestep it does three
things:

1. It **leaks**: v becomes a little smaller.
2. It **integrates**: it adds the weights of all inputs that spiked in this timestep.
3. It **fires** if v is at or above a **threshold**. Then it sends a **spike** (a 1), and v goes
   back to the **rest** value.

This model is called **leaky integrate-and-fire (LIF)**.

In our core, all numbers are integers (**fixed-point**). With 4-bit weights, the scale is 2^4 = 16:

| Item | Value in the code | Meaning |
|---|---|---|
| Decay | `v * 14 >> 4` | v × 0.875, rounded down |
| Threshold | 16 | 1.0 × 16 |
| Rest | 0 | 0.0 × 16 |
| Leak | 0 | 0.0 × 16 |
| Weight | integer from -7 to +7 | weight / 16 |

The update is: v' = (v × 14 >> 4) + (sum of weights from spiking inputs) - leak. If v' ≥ 16, the
neuron fires and v' becomes 0.

**Example.** v = 0. Three inputs spike with weights 7, 6 and 5. The sum is 18. v' = 0 + 18 = 18.
18 ≥ 16, so the neuron fires and v goes back to 0. With only the inputs 7 and 6, v' = 13. The
neuron does not fire. In the next timestep, v decays to 13 × 14 >> 4 = 11.

## 2. Many neurons, few connections

The core has N neurons (128 in the main runs). Each neuron gets input from **fanout** other neurons
(8 in the main runs). The connections and the weights come from a random generator with a fixed
**seed**, so each run gets the same network.

The weights form an N × N table. Most entries are zero, because each row has only 8 non-zero
entries out of 128. See `sample_weight_ints()` in `targets/digital/model.py`.

## 3. The golden model and the hardware

There are two copies of the same neuron logic:

- The **golden model**, `LIFModel` in `targets/digital/model.py`. It is Python. It is the truth.
- The **RTL**, made by `generate_rtl()` in `targets/digital/rtl_gen.py`. It is Verilog text that
  describes the hardware.

The **parity test** runs both on the same input spikes and checks that each spike of each neuron
in each timestep is the same. If one bit is different, the test fails. See
[tutorial 2](from-verilog-to-gds.md).

## 4. One timestep in the hardware

The RTL is a **finite state machine (FSM)** with four **phases**:

| Phase | What happens | Cycles |
|---|---|---|
| IDLE | Wait for `timestep_start`. Then copy the input spike frame `in_spk`. | 1 |
| RUN | Read one weight word per **clock cycle**. Word s holds the weights from source s to all neurons. If source s spiked, add the word into the 128 accumulators. | PAD + 2 |
| UPDATE | For each neuron: decay, add, compare with the threshold, fire or keep. | 1 |
| EMIT | Send each fired neuron address on `spike_out_addr`, one per cycle. | one per spike |

PAD is N rounded up to a power of two (128 stays 128). Thus a timestep takes about 131 cycles plus
one cycle per spike. At a 40 ns clock, that is about 5.2 µs.

The cycle count does not depend on the number of input spikes. The core reads all words in every
timestep.

## 5. Where the weights come from

Each weight word is PAD × 4 bits = 512 bits at 128 neurons. The core gives an address, and the
word comes back exactly one cycle later. There are two options today:

- `weight_store: external` (default). The words come from an SRAM outside the core, through the
  ports `w_read_sram_addr` and `w_read_sram`.
- `weight_store: rom`. The words are fixed in the logic of the core.

[ROM against external SRAM](../comparisons/rom-vs-external-sram-weights.md) compares the two, and
[weight storage hierarchy](../concepts/weight-storage-hierarchy.md) tells why the weights cannot
come from an SSD directly.

## Check your understanding

1. v = 16, no input spikes, leak 0. What is v after one timestep? Answer: 16 × 14 >> 4 = 14. No
   fire.
2. Why must the golden model and the RTL use integers? Answer: floating-point rounding would make
   the parity test fail on single bits.
3. Why is the weight table mostly zeros? Answer: fanout 8 out of 128 sources.

## Next

[Tutorial 2: From Verilog to a chip layout](from-verilog-to-gds.md).

Related: [index](../index.md).
