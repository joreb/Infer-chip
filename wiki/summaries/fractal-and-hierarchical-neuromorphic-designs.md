---
title: Fractal and hierarchical designs for neuromorphic chips
created: 2026-10-18
updated: 2026-10-18
type: summary
tags: [neuromorphic, snn, architecture, layout]
sources: []
status: open
---

# Fractal and hierarchical designs for neuromorphic chips

Text written in ASD-STE100 Simplified Technical English.

This page is a digest of a literature scan made on 2026-10-18 by a research agent. It tells what
is known about fractal, self-similar and hierarchical structure in neuromorphic hardware. It also
tells which ideas we can test in our flow.

## Background for beginners

**Why wires matter.** A chip has two big costs: the cells (logic and memory) and the wires between
them. Long wires use area, add delay and use power each time a signal changes. Our 128-neuron core
has about 1.45 m of routed wire on 0.705 mm². Thus wires are a large part of the design.

**What "fractal" means here.** A fractal structure looks the same at each scale. An **H-tree** is
the standard example. It is a letter H, with a smaller H at each of its four ends, and so on. Each
end point has the same wire distance to the center. Chip designers use H-trees to send the clock to
all flip-flops at the same time.

**What "hierarchical" means.** A hierarchical network has levels. Neurons in one group connect
directly. Groups connect through a router. Groups of groups connect through a higher router. This
is not a fractal, because each level is usually different. Many papers call it "fractal" loosely.

**Rent's rule.** Cut a circuit into blocks. Count the cells in a block (C) and the wires that leave
the block (T). Rent's rule says T = t × C^p. The exponent p tells how local the wiring is. A low p
means that most wires stay inside their block. Random all-to-all wiring gives p near 1, which is
the worst case.

**Evidence labels on this page.** [SILICON] means measured on a fabricated chip. [P&R] means from
place and route, not fabricated. [FPGA] means measured on an FPGA. [SIM] means simulation, theory
or estimate. [SECONDARY] means that the number comes from a review, not from the primary paper.

## Main findings

1. **Real fractal routing in neuromorphic silicon is rare.** The one clear case is the H-tree
   router of Stanford's Braindrop. It is fabricated in 28 nm. The thesis says that it "requires
   less wiring per signal than a grid". It serves a 16 × 16 array of neuron clusters, and it uses
   43% of each cluster tile [SILICON]. Source: S. Fok, PhD thesis, Stanford 2018,
   <https://purl.stanford.edu/qk018rf9117>.
2. **Hierarchy saves routing memory at a large neuron count, not at a small count.** DYNAPs uses
   two-stage tag routing. The calculation shows less than 1.2k bits of routing memory per neuron,
   against about 160k bits for a conventional scheme. But this is true only at about one million
   neurons [SIM]. On the real chip (0.18 µm, 1k neurons), memory uses 31.7% of the die and routers
   use 9.7% [SILICON]. Source: [arXiv 1708.04198](https://arxiv.org/abs/1708.04198).
3. **Small-world tiling saves nothing at 128 neurons.** Mosaic puts small memristor crossbars in a
   mesh, with dense local wiring and sparse long wiring. It needs about 10 times fewer memory devices
   at 1024 neurons, and no fewer at 128 neurons [SIM]. The locality costs about 2.5 to 3% accuracy.
   Source: Nature Communications 15:142 (2024),
   <https://pmc.ncbi.nlm.nih.gov/articles/PMC10761708/>.
4. **Brains and chip netlists follow the same Rent scaling.** Bassett et al. (2010) measured Rent
   exponents of 0.75 to 0.78 for brain networks and 0.73 for a VLSI netlist. Both are modular over
   several levels. Source: DOI 10.1371/journal.pcbi.1000748. Partzsch and Schüffny (2015) show
   that local connectivity needs about 10 times less address space than random connectivity [SIM].
   Source: DOI 10.3389/fnins.2015.00386.
5. **Most large chips use a plain mesh.** Loihi, TrueNorth, Tianjic and SpiNNaker are 2D meshes.
   The scan found no fractal network-on-chip, no neuromorphic fat-tree network, and no source for
   Hilbert or Morton ordering of neurons at gate level.

## Chips and their topologies

| System | Topology | Key numbers | Label |
|---|---|---|---|
| DYNAPs ([arXiv 1708.04198](https://arxiv.org/abs/1708.04198)) | 3 router levels: in core, between cores, mesh between chips | 0.18 µm, 1k neurons, memory 31.7% of area, routers 9.7%, 17 pJ per hop | SILICON |
| Braindrop ([thesis](https://purl.stanford.edu/qk018rf9117)) | H-tree router | 28 nm, 16 × 16 clusters, router 43% of tile | SILICON |
| Neurogrid (DOI 10.1109/TCSI.2013.2284184) | Multicast tree between 16 chips | about 1 M neurons, 31.2 pJ per event | SILICON, energy SECONDARY |
| H-NoC (Carrillo et al., IEEE TPDS 2013) | Routers in a cluster, routers between clusters | 400 neurons: 0.587 mm², 13.16 mW, 65 nm | P&R |
| MorphIC ([arXiv 1904.08513](https://arxiv.org/abs/1904.08513)) | Hierarchical routing between 4 cores | 65 nm, 2k neurons, 738k synapses/mm² | SILICON |
| Loihi (DOI 10.1109/MM.2018.112130359) | 2D mesh, 128 cores | 14 nm, about 128k neurons, 23.6 pJ per event | SILICON, energy SECONDARY |
| TrueNorth (DOI 10.1126/science.1254642) | 2D mesh, 4096 cores, 256 × 256 crossbar per core | 28 nm, 1 M neurons, 26 pJ per event (sources disagree) | SILICON |
| SpiNNaker (DOI 10.1109/JPROC.2014.2304638) | Triangular toroidal mesh | 130 nm, 18 ARM cores per chip | SILICON |
| Tianjic (DOI 10.1038/s41586-019-1424-8) | 2D mesh, 156 cores | 28 nm, 650 GSOPS/W | SILICON |

For scale: ODIN ([arXiv 1804.07858](https://arxiv.org/abs/1804.07858)) holds 256 neurons and
256 kbit of 4-bit synapses in 0.086 mm² (28 nm) [SILICON]. Our weight store is 64 kbit.

## Placement

- **H-trees for the clock** are standard. The OpenROAD clock tree tool already builds them, so this
  is not new for us.
- **Space-filling curves.** One 2026 paper compares Hilbert-curve placement of SNN layers onto a
  64 × 64 mesh of cores against spectral placement. Spectral placement is slightly better on
  energy-latency (0.96 × Hilbert) [SIM]. This maps networks onto cores, not cells onto silicon.
  Source: [arXiv 2601.16118](https://arxiv.org/abs/2601.16118).

## Where "fractal" is loose usage

Real self-similar structures in hardware are the H-tree, the recursive layouts that Rent's rule
implies, and the Cambricon-F machine (DOI 10.1145/3307650.3322226, a DNN accelerator, not
neuromorphic). In most neuromorphic papers, "fractal" means 2 or 3 router levels. The brain
"fractal" claim is a statistical scaling property, not a geometric fractal.

Fractal electrodes and self-organized nanoparticle networks exist. They are not CMOS logic and do
not fit our flow.

## Gaps

The scan found no source for these items:

- Wirelength with and without a hierarchical interconnect inside one digital SNN core, measured
  after place and route.
- Hilbert or Morton placement of cells for neuron arrays.
- A Rent exponent taken from the netlist of a neuromorphic chip.

## Ideas we can test

| Experiment | Proves it | Kills it |
|---|---|---|
| Banked weight memory: split the 128 × 128 × 4 store into 4 or 16 banks, one bank beside each neuron cluster | Routed wirelength falls by 20% or more at 128 neurons, area within +5%, slack not worse | Wirelength saving below 10%, or bank overhead cancels the area gain |
| Modular connectivity: 4 dense blocks of 32 neurons plus 8 long-range inputs per neuron (about 27.6k stored bits instead of 65.5k) | Weight area and routed wirelength fall by 40% or more, task accuracy drops by 3 points or less | Accuracy drops by more than 3 points, or tag logic uses more than half the memory saving |
| Rent-guided placement: get the Rent exponent of our netlist, then place neuron clusters in regions on a Hilbert order | Routed wirelength falls by 10% or more at the same utilization | Change below 5%. The research agent expects this result, because the default placer already finds locality |

The [ROM against external SRAM comparison](../comparisons/rom-vs-external-sram-weights.md) gives
the first measured data point for these ideas: the on-die weights added 26% wirelength at 128
neurons.

## Notes

The 12 cited arXiv papers are in `raw/papers/<arxiv id>.pdf` (downloaded 2026-10-18, git-ignored).
Some numbers come from secondary sources, as the labels show.

Related: [CMOS compute-in-memory](cmos-compute-in-memory.md),
[Open Neuromorphic digital hardware projects](../raw/papers/onm-digital-hardware-projects.md),
[index](../index.md).
