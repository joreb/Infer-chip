---
title: Digital hardware projects
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, neuromorphic]
sources: []
---

# Digital hardware projects

> Section of the [Open Neuromorphic resource list](https://github.com/open-neuromorphic/open-neuromorphic). 7 entries.

## ODIN Spiking Neural Network (SNN) Processor

[ODIN](https://open-neuromorphic.org/neuromorphic-computing/hardware/odin-frenkel/) is an online-learning digital spiking neuromorphic processor designed and prototyped in 28-nm FDSOI CMOS at Université catholique de Louvain (UCLouvain), published in 2019 in the IEEE Transactions on Biomedical Circuits and Systems journal. ODIN is based on a single 256-neuron 64k-synapse crossbar neurosynaptic core with the following key features: - synapses embed spike-dependent synaptic plasticity (SDSP)-based online learning, - neurons can phenomenologically reproduce the 20 Izhikevich behaviors.

[project page](https://open-neuromorphic.org/neuromorphic-computing/hardware/odin-frenkel/).

## ReckOn: A Spiking RNN Processor Enabling On-Chip Learning over Second-Long Timescales

[ReckOn](https://open-neuromorphic.org/neuromorphic-computing/hardware/reckon-frenkel/) is a spiking recurrent neural network (RNN) processor enabling on-chip learning over second-long timescales based on a modified version of the e-prop algorithm (we released a PyTorch implementation of the vanilla e-prop algorithm for leaky integrate-and-fire neurons here). It was prototyped and measured in 28-nm FDSOI CMOS at the Institute of Neuroinformatics, University of Zurich and ETH Zurich, and published at the 2022 IEEE International Solid-State Circuits Conference (ISSCC) with the following three main claims: - ReckOn demonstrates end-to-end on-chip learning over second-long timescales while keeping a milli-second temporal resolution, - it provides a low-cost solution with a 0.45-mm² core area, 5.3pJ/SOP at 0.5V, and a memory overhead of only 0.8% compared to the equivalent inference-only network, - it exploits a spike-based representation for task-agnostic learning toward user customization and chip repurposing at the edge.

[project page](https://open-neuromorphic.org/neuromorphic-computing/hardware/reckon-frenkel/).

## RANC - Reconfigurable Architecture for Neuromorphic Computing

[RANC](https://ua-rcl.github.io/projects/ranc/) is a highly flexible environment that enables rapid experimentation with neuromorphic architectures in both software via C++ simulation and hardware via FPGA emulation. RANC enables hardware architects and application engineers to investigate and tune parameters of their neuromorphic architecture that would otherwise be unavailable on a purely prefabricated ASIC.

[project page](https://ua-rcl.github.io/projects/ranc/).

## SNE: an Energy-Proportional Digital Accelerator for Sparse Event-Based Convolutions

[SNE](https://github.com/pulp-platform/sne) is a novel digital sparse neural engine (SNE) to efficiently accelerate SNN inference tasks at the extreme edge. The accelerator exploits an explicit input event temporal and spatial location encoding; the SNE architecture is designed to improve input data and weight reuse, reducing the traffic towards the memory.

[project page](https://github.com/pulp-platform/sne).

## A Lightweight Spiking Neural Network Accelerator [Google Shuttle]

[A spiking neural network accelerator](https://github.com/jeshraghian/snn-accelerator) in the SkyWater 130nm process using heterogenous time constants to model a variety of temporal dynamics. Input events can be streamed at a rate of up to 50 MEvents per second, and the accelerator can process them in a dense network with 128 hidden neurons at up to approximately 214 MHz.

[project page](https://github.com/jeshraghian/snn-accelerator).

## SNN ASIC accelerator [Google Shuttle]

An [SNN ASIC](https://github.com/pengzhouzp/wrapped_snn_network) with adaptive threshold neurons and recurrent connective synapses.

[project page](https://github.com/pengzhouzp/wrapped_snn_network).

## OpenSpike: An OpenRAM SNN AcceleratorOpenSpike

This paper presents a spiking neural network (SNN) accelerator made using fully open-source EDA tools, process design kit (PDK), and memory macros synthesized using OpenRAM. The chip is taped out in the 130 nm SkyWater process and integrates over 1 million synaptic weights, and offers a reprogrammable architecture.

[project page](https://github.com/sfmth/OpenSpike).

## See also

- [Wiki index](../../index.md)
- [Previous: Event-based data utilities](onm-event-based-data-utilities.md)
- [Next: SNN training frameworks for ML](onm-snn-training-frameworks-for-ml.md)
