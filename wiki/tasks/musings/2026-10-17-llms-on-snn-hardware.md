---
title: Can one run LLMs on spiking neural network hardware?
created: 2026-10-17
updated: 2026-10-17
type: musing
tags: [snn, neuromorphic, benchmark]
sources: []
---

# Can one run LLMs on spiking neural network hardware?

Date: 2026-10-17. Backdrop: the digital SNN fabric PnR run in flight.
Question asked by JSR during the session. Answer written for the proposal
backlog conversation, not for the pitch.

## Short answer

Not today at GPT scale, but the research direction exists and the fit is
partial, not natural. Small-scale spiking language models are published and
running; large-scale ones are blocked by compute shape and memory bandwidth,
not by neuron science.

## What has been shown

- SpikeGPT (2023): a spiking recurrent language model, ~26M weights, trained
  with surrogate gradients, generated coherent text. Energy estimate claims
  versus equal-size LSTMs/transformers on hardware.
- Spikformer / SpikingBERT (2022 onward): spiking transformers and BERT
  variants, attention with binary spiking representations, small to medium
  scale, all trained on GPUs first and only *interpreted* as spiking.
- Intel Loihi 2 and IBM NorthPole class hardware: Loihi research groups have
  run transformer-style attention blocks mapped to core grids; NorthPole
  deliberately sidesteps "spiking" rhetoric but is inference-only,
  memory-near compute. Neither runs a usable ChatGPT-class model.

## Why the fit is partial

1. LLM compute is dense matmul over long-range attention; the useful
   neuromorphic property is sparse, event-driven, stateful local compute.
   An SNN fabric pays for what it does not spike: our own PAD+O(1) budget
   is exactly this trade, and attention defeats it because every token
   attends to everything.
2. State fits well. KV-cache, membrane state, recurrent state are the same
   idea: carry state in memory rather than recompute. SNN cores are
   naturally stateful; that is genuinely a good match and worth keeping in
   stage-2 language.
3. Precision. LLM inference tolerates 4- and 2-bit weights; SNNs push
   toward binary spikes and small integer weights. Our 4-bit weight_words
   image is in that regime already, but activation quantization to one bit
   per timestep is the aggressive part that costs attention quality.
4. Training happens away from the chip either way (surrogate gradients,
   spike replacement, BPTT). Every deployable spiking LM today is trained
   on GPUs, then mapped. Same shape as our backlog entry 1: train-then-map.
5. Memory bandwidth is the wall. The fabric story removes weight memory
   from the block precisely because dense weight traffic is the cost
   driver. An LLM layer on a crossbar (memristive/photonic target) is the
   more credible silicon story than the digital fanout fabric.

## What this means for us

- The pitch claim stays honest if scoped: the PoC is a spiking *fabric* with
  bit-exact verification and real PnR, an LLM-class workload on it today
  would not be credible.
- Stage 2 credible claim: spiking inference for token/sequence models at
  small scale via train-and-map, with the crossbar/photonic targets as the
  dense-matmul path. Our three-target structure covers exactly the split
  above: digital fabric for event-driven sparse compute, memristive/photonic
  crossbars for dense weights.
- If we ever want a demo: SpikeGPT-sized model, quantized weights, SRAM
  image, one layer live on the 256-neuron fabric. Ambitious, stage 2+.

## Related

- [BindSNET is a trainer, not a golden model](2026-10-17-bindsnet-not-a-golden-model.md)
- [Why not hls4ml for the fabric](2026-10-17-why-not-hls4ml-for-the-fabric.md)
- [SpikeLLM is not a target for the fabric](2026-10-17-spikellm-is-not-a-target-for-the-fabric.md)
- [Wiki index](../../index.md)
