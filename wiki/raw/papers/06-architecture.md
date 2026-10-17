---
title: Architecture
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, architecture]
sources: []
---

# Architecture

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 15 papers.

## What this covers

This section covers using AI and large language models to automate and optimize architecture design. The architectures are for processors, accelerators, and system-on-chip platforms. Papers address design space exploration, performance and power trade-offs, hierarchical design synthesis, and end-to-end automation of design flows. AI now enables system-level architecture generation and verification.

## Themes

- **LLM-guided CPU and processor design**. BSD/Enlightenment, ChatCPU, QiMeng-CPU, Design Conductor, and LPCM synthesize and optimize processor architectures automatically. They use machine learning models and reasoning based on language models.
- **AI accelerator and chiplet design**. GPT4AIGChip, MAHL, ThermoDSE, FSGen, and Redwood design DNN accelerators. They include thermal-aware design. They handle sparse and fused operators with multi-agent coordination.
- **Design space exploration with learning models**. QGAS, SpecLLM, and MultiModel-DSE use language models and multi-modal fusion. They navigate architecture trade-offs. They generate specifications automatically.
- **Multi-agent and hierarchical design**. MAHL and MultiModel-DSE introduce coordinated multi-agent flows and modal fusion approaches. These approaches enable complex design decisions across abstraction levels.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2023-06-12 | [LCDA](https://arxiv.org/pdf/2306.06923) | On the viability of using LLMs for SW/HW co-design: An example in designing CiM DNN accelerators. | n/a | n/a |
| 2023-06-21 | [BSD (AlphaChip / Enlightenment)](https://arxiv.org/abs/2306.12456) | Pushing the Limits of Machine Design: Automated CPU Design with AI | n/a | n/a |
| 2023-07-17 | [QGAS](https://arxiv.org/pdf/2307.08191) | Unleashing the potential of LLMs for quantum computing: A study in quantum architecture design | n/a | n/a |
| 2023-9-19 | [GPT4AIGChip](https://arxiv.org/pdf/2309.10730)🔥 | GPT4AIGChip: Towards next-generation AI accelerator design automation via large language models. | n/a | n/a |
| 2024-1-24 | [SpecLLM](https://arxiv.org/pdf/2401.13266) | SpecLLM: Exploring generation and review of vlsi design specification with large language model. | n/a | n/a |
| 2024-06-23 | ChatCPU | ChatCPU: An Agile CPU Design & Verification Platform with LLM | n/a | n/a |
| 2024-08-03 | BSD (Enlightenment-1 / QiMeng-CPU-v1) | Automated CPU Design by Learning from Input-Output Examples | n/a | n/a |
| 2025-05-06 | [State-BSD](https://arxiv.org/abs/2505.03195) | QiMeng-CPU-v2: Automated Superscalar Processor Design by Learning Data Dependencies | n/a | n/a |
| 2025-06-03 | [LPCM](https://arxiv.org/abs/2506.02929) | Large Processor Chip Model | n/a | n/a |
| 2025-08-08 | [MAHL](https://arxiv.org/abs/2508.14053) | MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging | n/a | n/a |
| 2025-10-26 | MultiModel-DSE | LLM-Augmented Multi-Modal Fusion for SoC Design Space Exploration | n/a | n/a |
| 2026-02-06 | [Design Conductor (DC)](https://arxiv.org/abs/2603.08716) | Design Conductor: An agent autonomously builds a 1.5 GHz Linux-capable RISC-V CPU | n/a | n/a |
| 2026-07-08 | [ThermoDSE](https://arxiv.org/abs/2607.07096) | ThermoDSE: A Thermal-Aware and Comprehensive Design Space Exploration for Chiplet-Based DNN Accelerators | n/a | n/a |
| 2026-08-10 | [FSGen](https://arxiv.org/abs/2608.09252) | FSGen: Agile Fused and Sparse Accelerator Generator with Accurate Power Model for LLM Applications | [FSGen](https://github.com/hkust-zhiyao/FSGen) | n/a |
| 2026-08-26 | [Redwood](https://arxiv.org/abs/2608.26418) | Redwood: A Frontier AI Accelerator Designed, Verified, and Deployed from Scratch in 2 Weeks by AI | n/a | n/a |

## Notable entries

- **Design Conductor (2026)**. The most recent example of end-to-end autonomous design. It builds a functional 1.5 GHz Linux-capable RISC-V CPU from scratch.
- **Redwood (2026)**. A result showing that AI designs, verifies, and deploys an AI accelerator in two weeks.
- **GPT4AIGChip (2023)**. Early work applying GPT-4 to AI accelerator design. It establishes that LLMs can make detailed architecture decisions.
- **MAHL (2025)**. This work introduces multi-agent LLM coordination with adaptive debugging for hierarchical chiplet design. It advances beyond single-model approaches.
- **LPCM (2025)**. This work presents dedicated large foundational models for processor design. They specialize beyond general LLMs.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **LCDA** ([arXiv:2306.06923](https://arxiv.org/abs/2306.06923)). Software and hardware co-design optimizers work slowly because they do not use heuristic knowledge. The paper uses pre-trained large language models in the optimization process and gets a 25x speedup.
- **BSD (AlphaChip / Enlightenment)** ([arXiv:2306.12456](https://arxiv.org/abs/2306.12456)). The paper addresses whether machines can design complex hardware like humans. The method generates a RISC-V CPU design in 5 hours from input-output observations with a Binary Speculation Diagram.
- **QGAS** ([arXiv:2307.08191](https://arxiv.org/abs/2307.08191)). The paper examines how GPT models can help research in NISQ technologies and fault-tolerant quantum computing. The authors develop a QGAS model that rapidly suggests ansatz architectures and tests them with quantum chemistry and finance tasks.
- **GPT4AIGChip🔥** ([arXiv:2309.10730](https://arxiv.org/abs/2309.10730)). Designing AI accelerators needs a lot of labor, time, and hardware knowledge, and this blocks non-experts. The authors use large language models with an automatic prompt-generation pipeline and in-context learning to make accelerator designs.
- **SpecLLM** ([arXiv:2401.13266](https://arxiv.org/abs/2401.13266)). Writing architecture specifications for chip design takes time, and errors in the specifications can affect later design stages. This paper uses large language models to write specifications, to convert RTL code into specifications, and to review specifications.
- **State-BSD** ([arXiv:2505.03195](https://arxiv.org/abs/2505.03195)). Previous automated methods design only single-cycle processors because they cannot address data dependencies between instructions. State-BSD uses a state-selector and a state-speculator to predict dependent data and improves performance by about 380 times.
- **LPCM** ([arXiv:2506.02929](https://arxiv.org/abs/2506.02929)). Manual computer architecture design depends on expert knowledge and has high costs. The paper presents an LLM framework for end-to-end automated design and tests it with 3D Gaussian Splatting.
- **MAHL** ([arXiv:2508.14053](https://arxiv.org/abs/2508.14053)). Large language models for chiplet design produce flat designs, high validation cost, and parameter optimization that is not accurate. MAHL is a hierarchical framework with six agents for description generation, retrieval-augmented code generation, validation, and design space exploration.
- **Design Conductor (DC)** ([arXiv:2603.08716](https://arxiv.org/abs/2603.08716)). The paper addresses the problem of building a complete CPU from specification to verified GDSII layout with no human help. An autonomous agent uses frontier models to build a RISC-V CPU from a 219-word requirements document in 12 hours.
- **ThermoDSE** ([arXiv:2607.07096](https://arxiv.org/abs/2607.07096)). Chiplet-based DNN accelerators face area and thermal constraints in design space optimization. ThermoDSE integrates fine-grained modeling into one framework that considers architecture, task orchestration, and inter-chiplet communication under thermal and area constraints.
- **FSGen** ([arXiv:2608.09252](https://arxiv.org/abs/2608.09252)). Designers lack end-to-end methods for efficient design space exploration of AI chip accelerators for large language models. FSGen generates attention-based LLM accelerators with fused dataflows and sparsity and uses an early-stage PPA estimator for faster exploration.
- **Redwood** ([arXiv:2608.26418](https://arxiv.org/abs/2608.26418)). AI workloads change in months, but hardware design takes years, so design decisions face deep uncertainty. An AI system co-designs and verifies hardware and software and generates an accelerator from a specification in under two weeks.

## See also

- [Wiki index](../../index.md)
- [Previous: Security](05-security.md)
- [Next: Netlist](07-netlist.md)
