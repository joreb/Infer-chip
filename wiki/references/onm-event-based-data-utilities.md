---
title: Event-based data utilities
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, neuromorphic]
sources: []
---

# Event-based data utilities

> Section of the [Open Neuromorphic resource list](https://github.com/open-neuromorphic/open-neuromorphic). 6 entries.

## Tonic

Users need a tool to download, process, and load event-based and spike-based data. The paper presents a data tool that works like PyTorch Vision for neuromorphic data.

[project page](https://open-neuromorphic.org/neuromorphic-computing/software/data-tools/tonic/) and [repository](https://github.com/neuromorphs/tonic).

## expelliarmus

Prophesee cameras produce binary files that need decoding. This package decodes these files with code in Python and C.

[project page](https://open-neuromorphic.org/neuromorphic-computing/software/data-tools/expelliarmus/) and [repository](https://github.com/open-neuromorphic/expelliarmus).

## AEStream

The tool parses event-based dynamic-vision system data from an input source. It streams the data to a sink such as a GPU, a CPU, or network ports.

[project page](https://open-neuromorphic.org/neuromorphic-computing/software/data-tools/aestream/) and [repository](https://github.com/aestream/aestream).

## AEDAT

The tool reads AEDAT 4 data fast in Python. The implementation uses Rust.

[project page](https://open-neuromorphic.org/neuromorphic-computing/software/data-tools/aedat/) and [repository](https://github.com/neuromorphicsystems/aedat).

## BIMVEE

Event data exists in many formats, and users need tools to import, process, and export it. The method is an open-source Python library that imports, manipulates, visualizes, and exports event data with timestamp synchronization.

[project page](https://github.com/event-driven-robotics/bimvee) and [repository](https://github.com/event-driven-robotics/bimvee).

## MUSTARD

The paper addresses playback and visualization of multistream data, including event-camera data. The open-source Python application opens a visualiser sub-window for each data stream and controls playback speed, direction and time-window globally.

[project page](https://github.com/event-driven-robotics/mustard) and [repository](https://github.com/event-driven-robotics/mustard).

## See also

- [Wiki index](../index.md)
- [Previous: SNN training frameworks for ML and neuroscience](onm-snn-training-frameworks-for-ml-and-neuroscience.md)
- [Next: Digital hardware projects](onm-digital-hardware-projects.md)
