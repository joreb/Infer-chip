# Musing: BindSNET is a trainer, not a golden model

Date: 2026-10-17. Question asked by JSR during the digital e2e PnR run:
would https://github.com/BindsNET/bindsnet help us? Short answer: wrong
layer. It is a PyTorch SNN simulator and trainer, not a hardware path.

## What BindSNET does

Torch-based SNN networks (LIF, AdEx, Izhikevich neurons; STDP and
supervised learning rules; Poisson encoders; datasets such as MNIST) for
learning experiments. Software simulation, floats, GPU.

## Why it does not replace our core

1. The golden model is deliberately integer-quantized numpy: the same
   fixed-point widths, shift decay, threshold and reset semantics as the
   RTL, verified bit-exact at 16, 128, 256 and 300 neurons. BindSNET is
   float32 torch dynamics. Pinning RTL parity against it means
   reimplementing the quantization anyway, inheriting the torch dependency
   to reproduce what model.py already does exactly.

2. Wrong layer. The pipeline is agent, config, numpy golden model,
   cocotb RTL, ORFS GDS, plus physics models for photonic and memristive
   targets. BindSNET would sit where the golden model sits: the one piece
   already proven and the cheap auditable artifact the agent layer reasons
   over.

3. Dependency weight: the torch stack plus a project in maintenance mode
   (snnTorch is the livelier option in that family) for what a roughly
   200-line LIF model covers.

## Where it earns a slot

- Demo stimulus, stage 2: real-data spike trains (Poisson-encoded MNIST or
  CIFAR) into the cocotb bench as in_spk frames, about a hundred lines of
  glue.
- Train-then-map story: train weights in snnTorch or BindSNET, quantize,
  weight_words(), external SRAM image, fabric and ORFS unchanged. Jury
  gets "a trained SNN running on silicon we placed and routed". Works only
  because weights are external data, not baked into the netlist.

Recorded in docs/backlog.md entry 1 and tasks/musings/ for the full shape.

## Related

- docs/backlog.md entry 1: train-and-map path.
- tasks/musings/2026-10-17-bindsnet-plus-hls4ml-seam.md: the same library
  in the proposed RTL-generation role.
- tasks/musings/2026-10-17-llms-on-snn-hardware.md: train-then-map is also
  how every deployable spiking language model lands on hardware.