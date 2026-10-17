---
title: BindSNET for model gen and hls4ml for RTL?
created: 2026-10-17
updated: 2026-10-17
type: musing
tags: [hls, snn, flow]
sources: []
---

# BindSNET for model gen and hls4ml for RTL?

Date: 2026-10-17. Proposal raised by JSR during the digital e2e PnR run.
Verdict: the combo breaks at the seam. Full argument kept here; the short
version lives in docs/backlog.md entry 2.

## The proposed chain

BindSNET (train SNN in torch) to ??? to hls4ml (emit RTL). Walk it and it
fails twice at the question mark.

## Where the seam breaks

1. hls4ml has no SNN entry point. It ingests Keras/ONNX inference graphs,
   dense, conv, activations. A trained BindSNET network is stateful torch
   modules: membrane state, spike events, STDP updates. There is no
   torch-SNN to ONNX exporter; the stateful temporal loop mostly cannot
   survive ONNX export cleanly. Even with one, hls4ml has no LIF layer to
   compile to. The community has poked at hls4ml-SNN; nothing mainline. The
   HLS C++ kernel would be hand-written anyway, so the tool contributes
   nothing for the part that matters.

2. Even if it compiled, wrong architecture. hls4ml emits frame-based
   dataflow pipelines with weights baked in as ROMs. Peer-accepted design:
   weights external over an OpenSpike SRAM port, spike-event streaming,
   PAD+O(1) cycle budget. Trading the protocol-conformant FSM for an opaque
   HLS datapath contradicts the memory-interface doc and the pitch story.

3. Verification story collapses. Current proof: numpy golden model against
   RTL, bit-exact, one source of truth the agent audits. The new chain is
   torch floats, quantize, HLS fixed point, RTL: three semantics layers, no
   bit-exact story, new bug classes (ENG-005-class silent-success failures
   all over again), zero time to build that proof before the Nov 30
   deadline.

4. Toolchain cost: Vitis HLS in docker is a multi-GB install on top of the
   ORFS image, another flow to debug, another surface for jury-demo
   failure.

## The stage-2 shape that actually works

Our architecture already anticipates it, because weights are external data
by design:

```text
snnTorch/BindSNET train (floats)
  -> quantize to WW bits, extract weight matrix
  -> weight_words() -> external SRAM image
  -> our fabric + ORFS (unchanged)
```

Train-then-map: no exporter into HLS, reuse the verified back end. If dense
ANN layers join the same die later (ANN front-end plus SNN core), that is
where hls4ml slots in, generating only the ANN block.

Decision: rtl_gen.py stays. Recorded in docs/backlog.md entries 1 and 2.

## Related

- [Why not hls4ml for the fabric](2026-10-17-why-not-hls4ml-for-the-fabric.md)
- [BindSNET is a trainer, not a golden model](2026-10-17-bindsnet-not-a-golden-model.md)
- [Wiki index](../../index.md)
