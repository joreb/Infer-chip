---
title: SNN with a CPU-built experience memory on disk, streamed by an LLM agent for calibration
created: 2026-10-18
updated: 2026-10-18
type: musing
tags: [snn, neuromorphic, architecture]
sources: []
---

# SNN with a CPU-built experience memory on disk, streamed by an LLM agent for calibration

Text written in ASD-STE100 Simplified Technical English.

Date: 2026-10-18. Question from the user: "Spiking neural network that builds a memory bank with
CPU support and stores experiences to HDD, which then with LLM agent support stream to help a
calibrated task."

## Verdict

Possible as a system now, if the memory bank is on the host and not in the chip. The spiking core
detects events. The CPU stores experiences on disk. The LLM agent finds similar past experiences
and loads the matching weights into the core. A memory bank that learns inside the chip needs
on-chip learning, which the core does not have. That is research work.

## Argument

Each part works at its own speed, so the slow disk never sits in the fast path:

| Layer | Role | Time scale |
|---|---|---|
| Spiking core | Event detection on sensor data, at low power | µs per timestep |
| CPU | Puts spike output and conditions into experience records, indexes them, controls the chip | ms |
| HDD or SSD | Keeps the experiences: summaries, conditions, calibration results | ms per read |
| LLM agent | Finds similar experiences, selects or changes weights and parameters | s |

The loop:

1. The core runs and sends spikes (`spike_out_valid`, `spike_out_addr`).
2. The CPU stores one record per episode: conditions (for example temperature, drift, sensor id),
   a spike summary (firing rates, events) and the result.
3. For a new calibration task, the agent retrieves the closest past records.
4. The agent selects a weight set or calibration parameters.
5. The CPU loads them into the core over the load path of GitHub #11.
6. The new result becomes a new record.

An HDD is about 10^5 times too slow for one weight word per cycle
([weight storage hierarchy](../../concepts/weight-storage-hierarchy.md)). It is fast enough for
retrieval at agent speed (seconds). A reload of kB to MB of weights takes milliseconds.

## What the current core does not have

- **Loadable weights.** `weight_store: loaded` (GitHub #11). Without it, no new weights reach the
  core.
- **On-chip learning.** The core is inference only. A local rule such as STDP needs new RTL, a new
  golden model and more state per synapse.
- **A record format.** Store summaries, not raw spikes, so that retrieval stays small and fast.
- **A calibration metric.** Calibration error before and after, against a reference. Each record
  needs this score, so that the agent can rank records.

## Rejection rationale

- **Store the memory bank in the chip.** Rejected for now: no on-chip learning, and on-chip memory
  is small on sky130 (see the weight storage page).
- **Read experiences from the HDD in the core loop.** Rejected: the latency is too long by orders
  of magnitude.
- **Let the LLM compute the calibration itself.** Rejected: the agent works in seconds. It should
  select and configure, not be in the signal path.

## Proof for a pitch

Compare calibration with the experience memory against calibration without it, on the same task:
the number of calibration rounds to reach a target error, and the final error.

## Related

- [Weight storage hierarchy](../../concepts/weight-storage-hierarchy.md)
- [LLMs on SNN hardware](2026-10-17-llms-on-snn-hardware.md)
- [Tutorial 4: How to run the agent loop](../../tutorials/running-the-agent-loop.md)
- [index](../../index.md)
