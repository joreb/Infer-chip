---
title: Glossary of key concepts
created: 2026-10-18
updated: 2026-10-18
type: concept
tags: [snn, neuromorphic, flow, eda]
sources: []
---

# Glossary of key concepts

Text written in ASD-STE100 Simplified Technical English.

Short definitions of the terms in this wiki, in alphabetical order. Each entry tells what the term
means in this project. The tutorials use these terms:
[1](../tutorials/how-the-spiking-neuron-core-works.md),
[2](../tutorials/from-verilog-to-gds.md), [3](../tutorials/reading-ppa-metrics.md),
[4](../tutorials/running-the-agent-loop.md).

## A to C

**Accumulator.** A register that adds values over time. Each neuron has one. In the RUN phase it
adds the weights of the inputs that spiked.

**ADC (analog-to-digital converter).** A circuit that changes an analog voltage or current into a
number. Analog compute-in-memory needs many ADCs, and they cost much area and power.

**Agent loop.** The loop in which an AI agent proposes a design config, the tools measure it, and
the agent reads the result. `orchestrator.py`.

**Area.** The size of the cells of a design, in µm² or mm². In this wiki it means the standard-cell
area (`finish__design__instance__area__stdcell`) unless the text says die area.

**Backend.** The part of the agent loop that proposes configs: `stub`, `cc` (Claude Code) or `api`.

**Bandwidth.** How many bytes per second a memory or a link can move.

**Bind mount.** A docker option (`-v host:container`) that connects a host directory to a
directory in a container. Files written there stay on the host after the container stops.

**Cell (standard cell).** A small, ready-made logic gate or flip-flop from the cell library. The
flow builds the design only from these cells.

**Cell library.** The set of standard cells for one process. We use **sky130hs** (high speed).
**sky130hd** (high density) has smaller cells.

**CIM (compute-in-memory).** Arithmetic done inside the memory array or directly beside it, so the
data does not move. See [CMOS compute-in-memory](../summaries/cmos-compute-in-memory.md).

**Clock, clock period.** The signal that makes all flip-flops change at the same time. The period
is the time between two clock edges: 40 ns (25 MHz) in the main runs.

**cocotb.** A Python library that drives a Verilog simulation. The parity test uses it with
iverilog.

**Config.** The JSON dict that defines one design: `neurons`, `fanout`, `weight_width`,
`timesteps`, `util_target`, `clock_ns`, and optionally `weight_store` and `seed`.

**Container.** An isolated run environment from a docker image. Our flow runs ORFS in the
container `openroad/orfs`. With `--rm`, docker deletes it when it stops.

**Core area, die area.** The die is the full chip. The core is the inner area where cells can go.

**CTS (clock tree synthesis).** The flow stage that adds buffers so that the clock gets to each
flip-flop at the same time.

## D to G

**Decay.** The part of v that a neuron keeps from one timestep to the next. Here 14/16 = 0.875.

**Detailed route.** The flow stage that draws each real wire. It gives the real wirelength and the
DRC count.

**DRAM, DDR5, HBM.** Large, slow memories outside the chip. DDR5 is the normal computer memory. HBM
is DRAM stacked beside a processor for high bandwidth.

**DRC (design rule check).** A check that the layout obeys the rules of the factory, for example
minimum wire spacing. The count must be 0.

**Evidence page.** A short record in `runs_digital_e2e/digital/evidence/` of one run: config,
commit, image, `inv`, keys and log lines.

**Fanout.** In this project: the number of source neurons that connect to each neuron (8 in the
main runs). In general chip design, fanout also means the number of inputs that one output drives.

**Fixed-point.** Integer arithmetic with an implied scale. With 4-bit weights the scale is 16, so
the integer 8 means 0.5.

**Flip-flop.** A cell that stores one bit and changes only at a clock edge.

**Floorplan.** The flow stage that sets the die and core size and the power rails.

**Flow.** The chain of tools that turns RTL into a layout. Here ORFS.

**FSM (finite state machine).** Logic that moves between a fixed set of states. The core has four
phases: IDLE, RUN, UPDATE, EMIT.

**GDS (GDSII).** The layout file format. A factory makes the masks from it. Our file is
`6_final.gds`, copied as `final.gds`.

**Global route.** The flow stage that plans the wires on a coarse grid before detailed routing.

**Golden model.** The reference software model that the hardware must match exactly. Here
`LIFModel` in `targets/digital/model.py`.

## H to N

**Hold slack.** The margin that a signal does not arrive too early after a clock edge. It must be
≥ 0.

**H-tree.** A fractal tree in the shape of the letter H, repeated at smaller scales. Every end
point has the same distance to the center. See
[fractal and hierarchical designs](../summaries/fractal-and-hierarchical-neuromorphic-designs.md).

**inv (invocation id).** A random 8-character id for each start of the orchestrator. It names the
run directory `inv_<id>` and is in each journal line.

**iverilog (Icarus Verilog).** An open-source Verilog simulator.

**Journal.** `journal.jsonl`: one JSON line per round, with config, results and agent note.

**Latency.** The time from a request to its answer. The core needs a weight word exactly one cycle
after the address.

**Leak.** A constant that a neuron subtracts from v each timestep. 0 in the main runs.

**LIF (leaky integrate-and-fire).** The neuron model of the core: decay, add the inputs, fire at
the threshold, reset.

**Membrane potential (v).** The number that each neuron keeps. It goes up with input and fires at
the threshold.

**metadata.json.** The file that ORFS writes with `make metadata-generate`. It holds every metric
of every stage.

**Mixture-of-experts (MoE).** A model in which only a small part of the parameters is active for
each token.

**Netlist.** A list of cells and the wires between them. Synthesis makes it from the RTL.

**Neuromorphic.** Hardware that computes in a way similar to neurons, usually with spikes.

## O to R

**OpenRAM, ORRAM.** Open tools that make memories. OpenRAM makes SRAM macros with custom cells.
ORRAM makes RAM from standard cells inside OpenROAD.

**ORFS (OpenROAD-flow-scripts).** The open-source flow that we use for synthesis, place and route.

**PAD.** The neuron count rounded up to a power of two. The core always has PAD accumulators and
reads PAD weight words.

**Parity test.** The test that runs the RTL and the golden model on the same spikes and checks
that every spike is the same. `tests/digital/tb_parity.py`.

**PDK (process design kit).** The files that describe one factory process. sky130 is the open 130
nm PDK from SkyWater.

**Placement.** The flow stage that gives each cell a position on the die.

**PnR (place and route).** Placement plus routing. Often used for the full flow.

**Power.** Energy per second, in W. Here `finish__power__total`, estimated with default switching
activity.

**PPA.** Power, performance (here slack) and area. The three main metrics of a design.

**Rent's rule.** T = t × C^p: the wires (T) that leave a block grow with the cells (C) in it. A
low exponent p means local wiring.

**Rest.** The value that v gets after a spike. 0 in the main runs.

**ROM (read-only memory).** Memory with fixed contents. With `weight_store: rom` the weights are
fixed in the logic of the core.

**Round.** One pass of the agent loop: propose, evaluate, record.

**RTL (register-transfer level).** A description of hardware as registers and the logic between
them. Here Verilog from `rtl_gen.py`.

## S to Z

**Seed.** The start value of the random generator. The same seed gives the same weights.

**Setup slack, WNS.** The time that is left on the slowest path before the next clock edge. Must
be ≥ 0. WNS is the worst value. Here `finish__timing__setup__ws`.

**sky130.** The open 130 nm process from SkyWater and Google.

**Slack.** See setup slack and hold slack.

**SNN (spiking neural network).** A neural network in which neurons send spikes (single bits)
instead of numbers.

**Spike.** A single 1 that a neuron sends when it fires.

**SPI, QSPI.** Simple serial links with few pins. QSPI uses 4 data lines.

**SRAM (static RAM).** Fast memory that keeps data while it has power. An SRAM macro is a ready
block of it.

**SSD.** Flash storage. It keeps data with the power off, but each read takes about 50 to 100 µs.

**Stage.** One step of the flow: synthesis, floorplan, placement, CTS, global route, detailed
route, finish.

**Synthesis.** The flow stage that turns RTL into a netlist of standard cells. Yosys does it.

**Target.** What the agent designs: `digital`, `photonic` or `memristive`.

**Threshold.** The value of v at which a neuron fires. 16 (1.0 × 16) in the main runs.

**Timestep.** One update of all neurons. About 131 clock cycles at 128 neurons, plus one per spike.

**Utilization.** Cell area divided by core area. The flow sets the core size from the target (25%).

**Verilog.** A language that describes hardware.

**weight_store.** The config key that selects where the weights are: `external` (default) or
`rom`. `loaded` is planned (GitHub #11).

**Wirelength.** The total length of all routed wires. Here `detailedroute__route__wirelength`.

**Yosys.** The open-source synthesis tool in ORFS.

Related: [weight storage hierarchy](weight-storage-hierarchy.md), [index](../index.md).
