---
title: On-chip learning for spiking neural network hardware
created: 2026-10-18
updated: 2026-10-18
type: summary
tags: [snn, neuromorphic, architecture, rtl]
sources: []
status: open
---

# On-chip learning for spiking neural network hardware

Text written in ASD-STE100 Simplified Technical English.

This page is a short literature scan (2026-10-18) on chips that change their own weights while
they run. It also tells which learning rule fits our core. The use case is the
[experience-memory musing](../tasks/musings/2026-10-18-snn-experience-memory-for-calibration.md).

## Background for beginners

Our core does **inference only**: the weights are fixed while it runs. **On-chip learning** means
that the chip changes its weights itself, from its own spikes, without a host computer.

- **STDP (spike-timing-dependent plasticity).** If a source neuron spikes just before a target
  neuron, the weight between them becomes larger. If it spikes just after, the weight becomes
  smaller. The hardware keeps a **trace** per neuron: a value that jumps at a spike and then decays.
  The trace tells "how recently did this neuron spike".
- **SDSP (spike-driven synaptic plasticity).** The weight changes only when the source neuron
  spikes. The direction depends on the state of the target neuron at that moment (its membrane
  potential and a slow activity value).
- **e-prop (eligibility propagation).** An approximation of gradient training for recurrent
  spiking networks. Each synapse or neuron keeps an **eligibility trace**, and a learning signal
  tells it how to change.

Each rule needs two things that our core does not have: weights that the core can write, and
extra state (traces) per neuron or per synapse.

## Chips with on-chip learning

| Chip | Rule | Key numbers | Label | Source |
|---|---|---|---|---|
| ODIN (Frenkel et al., 2018) | SDSP | 28 nm, 256 neurons, 64k 4-bit synapses, 0.086 mm². One-layer, 10-neuron net learns MNIST on chip: 84.5% after one pass of 6k images, 15 nJ per inference at 0.55 V | Silicon | [arXiv 1804.07858](https://arxiv.org/abs/1804.07858) |
| Loihi (Davies et al., 2018) | Programmable: a microcode learning engine per core, rules on traces and local variables, pair and triplet STDP | 14 nm, 60 mm² | Silicon | [IEEE Micro 2018 PDF](https://www.Gwern.net/doc/ai/scaling/hardware/2018-davies.pdf) |
| ReckOn (Frenkel and Indiveri, ISSCC 2022) | Modified e-prop, traces that scale with neurons, not synapses | 28 nm FDSOI, 0.45 mm² core, 5.3 pJ per synaptic operation at 0.5 V, memory overhead 0.8% over the same net without learning, below 50 µW for real-time learning | Silicon (vendor-style claims from the project page) | [github.com/ChFrenkel/ReckOn](https://github.com/ChFrenkel/ReckOn) |
| SpiNNaker 2 prototype (Rostami et al., 2022) | e-prop on ARM cores | The authors note O(N²) memory for e-prop with N recurrent neurons | Silicon, software rule | [Front. Neurosci. 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9742366/) |
| Loihi, multilayer supervised (2021) | Error-modulated STDP | Supervised multilayer learning on the chip | Silicon | [arXiv 2105.03649](https://arxiv.org/abs/2105.03649) |
| ITP-STDP (2026) | Power-of-two STDP with intrinsic timing | 8 neurons, 16 synapses: 387 LUTs and 251 registers on FPGA, 2,127.76 µm² in 28 nm | FPGA and ASIC layout | [arXiv 2606.06159](https://arxiv.org/abs/2606.06159) |
| Lammie et al. (IEEE TCAS-I 2019) | Pair and triplet STDP on FPGA, no floating-point multipliers | 1.78 to 2.38 times fewer resources than the best earlier pair-STDP design | FPGA | [JCU record](https://researchonline.jcu.edu.au/56547/) |

Surveys group ODIN, ROLLS and MorphIC as SDSP chips, and Loihi as a chip with an STDP learning
module ([arXiv 2412.17926](https://arxiv.org/abs/2412.17926)).

## Which rule fits our core

Our weight memory holds one word per **source**: word s has the weights from source s to all
targets ([tutorial 1](../tutorials/how-the-spiking-neuron-core-works.md)). This layout decides the
cost of each rule:

| Rule | When a weight changes | Memory access in our layout | Cost per event |
|---|---|---|---|
| SDSP | At a source spike, for all targets of that source | One read and one write of word s | 1 extra write per source spike |
| STDP, depression part | At a source spike | One read and one write of word s | 1 extra write |
| STDP, potentiation part | At a target spike, for all sources to that target | One 4-bit slice in each of the 128 words | 128 read-write pairs per target spike |
| e-prop | Each timestep, for each synapse with a trace | Many words | High. Needs a different memory layout |

Thus **SDSP fits our core best.** The RUN phase already reads word s when source s spiked. With a
write port, the core can write back the updated word one cycle later. The update for each of the
128 slices uses only the state of that target neuron (its v and one slow activity value). This is
an analysis of our layout, not a measured result.

What it needs:

1. A writable on-chip weight memory: `weight_store: loaded` (GitHub #11) with a second port, or one
   extra cycle per spiking source for the write.
2. One slow activity counter per neuron (128 small registers).
3. A golden-model rule in `targets/digital/model.py`, bit-exact with the RTL, and a parity test
   that checks the weights after learning, not only the spikes.
4. Weight saturation at the 4-bit range (-7 to +7).

## Gaps

- No source found for the area of a learning engine on sky130.
- The ReckOn numbers are from its project page. The ISSCC paper was not read.

## Ideas we can test

| Experiment | Proves it | Kills it |
|---|---|---|
| SDSP in the RUN phase with write-back, 128 neurons | Parity of weights and spikes after learning; area within +20% of the loaded-SRAM design; cycles per timestep at most 2 × PAD + 3 | Area or cycle cost above that, or no accuracy gain on a small task |
| Learning against reload (experience memory) | Fewer calibration rounds to the target error than with reload only | No gain, which means the agent and reload are enough |

## Notes

`tools/fetch_arxiv.py` downloaded the cited arXiv PDFs to `raw/papers/<id>.pdf` (2026-10-18)
and checked each id against the arXiv API:

| arXiv id | Title on arXiv | Published |
|---|---|---|
| 1804.07858 | A 0.086-mm² 12.7-pJ/SOP 64k-Synapse 256-Neuron Online-Learning Digital Spiking Neuromorphic Processor in 28nm CMOS | 2018-04-20 |
| 2105.03649 | In-Hardware Learning of Multilayer Spiking Neural Networks on a Neuromorphic Processor | 2021-05-08 |
| 2412.17926 | Contemporary implementations of spiking bio-inspired neural networks | 2024-12-23 |
| 2606.06159 | ITP-STDP: A Hardware-Efficient Intrinsic-Timing Power-of-Two Synaptic Learning Engine for On-Chip SNNs | 2026-06-04 |

The numbers on this page come from web search results and abstracts. The full papers were not
read.

Related: [CMOS compute-in-memory](cmos-compute-in-memory.md),
[weight storage hierarchy](../concepts/weight-storage-hierarchy.md), [index](../index.md).
