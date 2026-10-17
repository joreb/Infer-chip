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

The paper addresses online learning at the edge with a digital spiking neuromorphic processor. Its 256-neuron 64k-synapse core has synapses that learn with spike-dependent plasticity and neurons that reproduce 20 Izhikevich behaviors.

[project page](https://open-neuromorphic.org/neuromorphic-computing/hardware/odin-frenkel/).

## ReckOn: A Spiking RNN Processor Enabling On-Chip Learning over Second-Long Timescales

The paper addresses on-chip learning over second-long timescales in spiking recurrent neural network hardware. The processor uses a modified e-prop algorithm in 28-nm FDSOI CMOS and keeps millisecond temporal resolution.

[project page](https://open-neuromorphic.org/neuromorphic-computing/hardware/reckon-frenkel/).

## RANC - Reconfigurable Architecture for Neuromorphic Computing

A prefabricated ASIC does not give architects access to the parameters of a neuromorphic architecture. RANC provides a flexible environment for rapid experiments with neuromorphic architectures in C++ simulation and FPGA emulation.

[project page](https://ua-rcl.github.io/projects/ranc/).

## SNE: an Energy-Proportional Digital Accelerator for Sparse Event-Based Convolutions

The paper addresses efficient acceleration of spiking neural network inference at the extreme edge. The accelerator encodes event temporal and spatial locations and reuses input data and weights to reduce memory traffic.

[project page](https://github.com/pulp-platform/sne).

## A Lightweight Spiking Neural Network Accelerator [Google Shuttle]

The paper describes a SkyWater 130nm accelerator with different time constants to model many temporal dynamics in spiking neural networks. It processes up to 50 MEvents/s in a dense network with 128 hidden neurons at up to about 214 MHz.

[project page](https://github.com/jeshraghian/snn-accelerator).

## SNN ASIC accelerator [Google Shuttle]

This paper presents a hardware design for spiking neural networks. The authors design an application-specific integrated circuit with adaptive threshold neurons and recurrent connective synapses.

[project page](https://github.com/pengzhouzp/wrapped_snn_network).

## OpenSpike: An OpenRAM SNN AcceleratorOpenSpike

The paper addresses the design of a spiking neural network accelerator with fully open-source tools and memory macros. The chip integrates over 1 million synaptic weights, and its neurons use hysteresis to reduce state instability.

[project page](https://github.com/sfmth/OpenSpike).

## See also

- [Wiki index](../../index.md)
- [Previous: Event-based data utilities](onm-event-based-data-utilities.md)
- [Next: SNN training frameworks for ML](onm-snn-training-frameworks-for-ml.md)
