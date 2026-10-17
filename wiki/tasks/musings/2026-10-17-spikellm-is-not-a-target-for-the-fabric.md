---
title: SpikeLLM is not a target for the fabric
created: 2026-10-17
updated: 2026-10-17
type: musing
tags: [snn, neuromorphic, architecture]
sources: []
---

# SpikeLLM is not a target for the fabric

Text written in ASD-STE100 Simplified Technical English.

## Verdict

SpikeLLM is not a workload for our 256-neuron fabric. The scale and the spike mechanism both
mismatch. The paper still names one real constraint in our control unit, so it is worth a record.

## Argument

SpikeLLM redesigns language models of 7 to 70 billion parameters with spiking mechanisms
([arXiv:2407.04752](https://arxiv.org/abs/2407.04752)). Our fabric holds 256 neurons and 65536
synapses. The gap is about five orders of magnitude, so the paper's workload cannot run here.

The paper measures language quality. It reports 11.01 percent lower WikiText2 perplexity and 2.55
percent better accuracy on a LLAMA-7B model at 4-bit weights and 4-bit activations. Our loop measures
area, routability and power. Neither set of numbers converts into the other.

The paper is not in the upstream AI4CHIPS index, and every page under `references/` is generated from
that index. A row added by hand there would disappear at the next rebuild. A musing is therefore the
correct home for this paper, and that is a property of our wiki rather than a judgment about the work.

## Rejection rationale

We do not reject the method. We reject the paper as a target workload, on three grounds.

The Generalized Integrate-and-Fire neuron allocates a different spike length T to each channel. Our
control unit assumes one uniform T for every neuron. The state machine walks a fixed address sequence
of 1092 cycles per time step, and its timing does not depend on the data. A per-channel T breaks both
properties at once.

The Optimal Brain Spiking framework separates outlier channels and treats them differently. Our weight
memory streams one word per cycle, and that word serves every neuron in the group. Separate treatment
of outlier channels needs a second address stream and a second memory port.

The comparison baseline differs. The paper argues against quantized models at 4-bit weights and 4-bit
activations. Our weights are 2-bit or 8-bit integers, so the paper's advantage over its baseline says
nothing about our design point.

The useful residue is a condition, not a rejection. If we ever want a variable spike length per
neuron, then the control unit and the external memory interface both change. Record that cost before
anybody proposes variable T as a small feature.

## Related

- [LLMs on SNN hardware](2026-10-17-llms-on-snn-hardware.md)
- [BindsNET is not a golden model](2026-10-17-bindsnet-not-a-golden-model.md)
- [Wiki index](../../index.md)
