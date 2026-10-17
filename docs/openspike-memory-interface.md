# OpenSpike memory interface specification

Text written in ASD-STE100 Simplified Technical English.

This document describes the external memory interface of the OpenSpike accelerator. OpenSpike is an
open-source spiking neural network accelerator. The authors hardened it on sky130 with OpenLane. The
source is in `raw/git/sfmth__OpenSpike`.

The purpose of this document is to let our 256-neuron LIF fabric use the same interface. The accelerator
holds no weight memory and no state memory inside the hardened block. All memory is external. A golden
model, an RTL design and a testbench can all target the ports below.

Source files:

- `openlane/src/accelerator.v`, lines 13 to 42 for the port list
- `openlane/src/control_unit.v`, the complete finite state machine
- `openlane/config.tcl` for the physical settings

## Port list

The accelerator drives every address and every write enable. The accelerator never reads a ready signal
and never waits. The memory must answer in a fixed number of cycles.

| Port | Direction | Width | Address width | Words | Contents |
|---|---|---|---|---|---|
| `w_read_sram` | in | 2048 | 11 | 2048 | 1024 synapse weights, 2 bits each |
| `w_read_sram_addr` | out | 11 | n/a | n/a | weight word address |
| `u_read_sram` | in | 128 | 9 | 512 | 16 membrane potentials, 8 bits each |
| `u_read_sram_addr` | out | 9 | n/a | n/a | potential read address |
| `u_write_sram` | out | 128 | 9 | 512 | 16 updated potentials |
| `u_write_sram_addr` | out | 9 | n/a | n/a | potential write address |
| `u_write_sram_we` | out | 1 | n/a | n/a | potential write enable |
| `b_read_sram` | in | 64 | 9 | 512 | 16 leak factors, 4 bits each |
| `b_read_sram_addr` | out | 9 | n/a | n/a | leak factor address |
| `spk_read_sram` | in | 16 | 9 | 512 | 16 output spikes, 1 bit each |
| `spk_read_sram_addr` | out | 9 | n/a | n/a | spike read address |
| `spk_write_sram` | out | 16 | 9 | 512 | 16 new spikes |
| `spk_write_sram_addr` | out | 9 | n/a | n/a | spike write address |
| `spk_write_sram_we` | out | 1 | n/a | n/a | spike write enable |
| `spkblty_read_sram` | in | 16 | 9 | 512 | 16 spike-ability flags |
| `spkblty_read_sram_addr` | out | 9 | n/a | n/a | spike-ability read address |
| `spkblty_write_sram` | out | 16 | 9 | 512 | 16 new spike-ability flags |
| `spkblty_write_sram_addr` | out | 9 | n/a | n/a | spike-ability write address |
| `spkblty_write_sram_we` | out | 1 | n/a | n/a | spike-ability write enable |
| `in_spk_read_sram` | in | 128 | 9 | 512 | 128 input spikes, 1 bit each |
| `in_spk_read_sram_addr` | out | 9 | n/a | n/a | input spike address |
| `clk` | in | 1 | n/a | n/a | single clock |
| `reset` | in | 1 | n/a | n/a | synchronous reset, active high |

The design has six independent read ports and three write ports. Each port needs its own memory
instance. The ports work at the same time, so one shared memory cannot serve them.

## Word format

The parallel width of a word follows from the group size. The accelerator processes 16 neurons per
cycle. One potential word therefore holds 16 potentials of 8 bits. One leak word holds 16 factors of
4 bits. One spike word holds 16 bits.

The weight word is different. It holds 1024 weights of 2 bits, which is one weight for each of the 1024
accumulators. `accelerator.v` line 80 gives the slice: accumulator `i` reads
`w_read_sram[(i*2)+1 : i*2]`.

Note the weight precision. OpenSpike uses 2 bits for each weight, not 8 bits. This decision sets the
bus width and the memory size. Our dense ROM plan assumed 8 bits, so our weight memory and our weight
bus are four times larger than the OpenSpike equivalent.

## Timing protocol

The protocol is simple and has no handshake.

1. Every address is a registered output. The control unit assigns each address in a clocked block.
2. A read address presented in cycle N expects its data in cycle N plus 1. The control unit increments
   the weight address when `cnt_512 > 0` and the comment on `control_unit.v` line 174 states "512 cycles
   with 1 cycle delay". This confirms a read latency of exactly one cycle.
3. A write is a single cycle. The accelerator drives the data, the address and the write enable in the
   same cycle.
4. There is no wait state, no stall input and no error response. A memory with a different latency
   breaks the design silently, because nothing detects the mismatch.

A standard synchronous SRAM with a registered address and a one-cycle read latency satisfies this
protocol. An OpenRAM macro on sky130 satisfies it. An asynchronous memory does not, and a memory with
two or more cycles of latency does not.

## Address map

The accelerator holds three layers. Each layer holds 1024 neurons in 64 words of 16 neurons. The
control unit uses fixed offsets for each layer.

| Memory | Input layer | Hidden layer | Output layer |
|---|---|---|---|
| weight read, start address | 0 | 1 | 513 |
| potential read, start address | 0 | 64 | 128 |
| leak read, start address | 0 | 64 | 128 |
| potential write, start address | 128 | 0 | 64 |
| spike-ability read and write, start address | 128 | 0 | 64 |
| spike read, start address | n/a | 0 | 64 |
| spike write, start address | current time step | 0 | 64 |

The weight memory is the large one. The hidden layer consumes 512 words from address 1, and the output
layer consumes 512 words from address 513. Each word is 2048 bits, so the hidden layer alone needs
1 Mbit of weight storage.

## Cycle budget

The state machine in `control_unit.v` gives an exact cycle count.

| State | Cycles | Work |
|---|---|---|
| `STATE_INIT` | 1 | reset the processor and the neurons |
| `STATE_INPUT_O` | 8 | load 1024 input spikes as 8 words of 128 bits |
| `STATE_PRE_INPUT` | 1 | set the addresses for the input layer |
| `STATE_INPUT` | 65 | accumulate the input layer over 64 neuron groups |
| `STATE_P_H` | 1 | set the addresses for the hidden layer |
| `STATE_HIDDEN` | 512 | accumulate the hidden layer, one weight word per cycle |
| `STATE_PRE_OUTPUT` | 1 | set the addresses for the output layer |
| `STATE_OUTPUT` | 512 | accumulate the output layer and load the next input frame |

One time step costs 1092 cycles. The machine runs the loop while `time_step < 128`, so a complete
inference costs about 141 thousand cycles. At 25 MHz one time step takes 43.7 microseconds and one
inference takes 5.6 milliseconds.

The cycle count does not depend on the spike rate. Every accumulator does work in every cycle, and the
address sequence is fixed. A high spike rate raises the dynamic power but does not change the
throughput. This property makes the timing easy to verify and makes the power the interesting variable.

## How to scale the interface to 256 neurons

Our fabric holds 256 neurons in one layer. Keep the group size of 16 neurons, because the group size
sets every word width.

| Quantity | OpenSpike | Our 256-neuron fabric |
|---|---|---|
| neurons | 1024 in 3 layers | 256 in 1 layer |
| neuron groups | 64 per layer | 16 |
| potential word | 128 bits | 128 bits, unchanged |
| potential words | 512 | 16 |
| potential address | 9 bits | 4 bits |
| weight word, at 2 bits | 2048 bits | 512 bits |
| weight word, at 8 bits | n/a | 2048 bits |
| weight words for 256 by 256 | n/a | 256 |
| cycles for one time step | 1092 | about 272 |

The weight bus is the decision that matters. At 2 bits per weight the bus is 512 bits. At 8 bits per
weight the bus is 2048 bits. A 2048-bit bus at 25 MHz carries 51.2 gigabits per second and needs 2048
pins or a wide macro abutment. Check this against the pin budget before the first physical run.

## Hazards found in the source

Do not copy the source without these corrections.

1. The input spike address looks wrong. `control_unit.v` line 231 sets
   `cntrl_in_spk_read_addr <= time_step + 1`, and `STATE_OUTPUT` then increments the address for 8
   cycles. Time step `t` therefore reads the addresses `t+1` to `t+8`. One input frame occupies 8 words,
   so consecutive time steps should start 8 words apart, not 1 word apart. The windows overlap. Verify
   the intent against the OpenSpike testbench before you copy this addressing.

2. The spike write address for the input layer is the time step itself (line 102), but the hidden and
   output layers write to fixed banks. The spike memory therefore holds a time trace for one layer and a
   current state for the others. Keep this difference deliberate in our design, or make all three
   uniform.

3. `STATE_INPUT` runs 65 cycles, not 64. The counter increments to 64 before the state changes. The
   extra cycle is harmless here, but a tight cycle model must account for it.

4. The design has no memory initialization of any kind. Every memory starts undefined. The testbench or
   the harness must write the weights and the leak factors before the first time step.

## Physical settings from the hardened run

These values come from `openlane/config.tcl`. The authors used them for a 1024-neuron design on sky130.

| Variable | Value | Note |
|---|---|---|
| `CLOCK_PERIOD` | 40 | 25 MHz |
| `FP_SIZING` | absolute | fixed die, not driven by utilization |
| `DIE_AREA` | 0 0 3000 3000 | 9 square millimetres |
| `FP_CORE_UTIL` | 15 | low, because of routing congestion |
| `PL_TARGET_DENSITY` | 0.20 | low, for the same reason |
| `RT_MAX_LAYER` | met4 | the caravel user area reserves met5 |
| `DESIGN_IS_CORE` | 0 | the block is a macro, not the core |
| `PL_RESIZER_BUFFER_OUTPUT_PORTS` | 0 | tristate cells must stay at the outputs |
| `RUN_KLAYOUT_DRC` | 0 | sign-off checks are disabled in the committed flow |

A utilization of 15 percent is low for a design of this type. The cause is visible in the RTL. The
`neuron_selector` module multiplexes 8192 bits of potential down to 128 bits with a 6-bit select, and
it demultiplexes the write path by the same factor. This wide multiplexer and its wiring, not the
arithmetic, set both the area and the critical path.

Our 256-neuron fabric needs a 16-way multiplexer over 2048 bits instead of a 64-way multiplexer over
8192 bits. The path is therefore much shorter, and 40 nanoseconds is a conservative target for our
design.

## What to measure

Record these numbers for the version with external memory and for the dense ROM baseline.

1. Cell area and die area after place and route. Also record the utilization at which the router first
   succeeds, because this number moved the OpenSpike design to 15 percent.
2. Instance count for each module. Separate the neurons, the accumulators, the selector multiplexer and
   the control unit. The selector is the suspect.
3. Global route overflow and the number of detailed route iterations. Record a failure as a result, not
   as a retry.
4. Worst negative slack after routing, with the start point and the end point of the critical path.
5. Dynamic power at several spike rates. Use an activity file from the simulation, because the cycle
   count is independent of the spike rate but the power is not. Measure at a low rate, a middle rate and
   full rate.
6. The external bus width and the resulting bandwidth. This cost replaces the ROM area, so the
   comparison is only honest when it appears next to the area saving.

Note on the standard cell library. The OpenSpike numbers come from the sky130 high-density library. Our
plan names sky130hs, the high-speed library. The high-speed cells switch faster, but they occupy more
area and they leak more. The 40 nanosecond period and the 15 percent utilization do not transfer to
sky130hs without measurement.
