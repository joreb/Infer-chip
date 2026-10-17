---
title: Flow & Layout
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, layout]
sources: []
---

# Flow & Layout

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 14 papers.

## What this covers

This section covers automation and optimization of back-end EDA flows. These flows include tool orchestration, standard cell design, hotspot detection, placement, routing, and design rule checking. Work targets the physical design phase of chip implementation. It covers agent systems that use language models to interact with EDA tools. It also covers models for layout prediction and defect analysis.

## Themes

- **Autonomous agents for tool interaction**: ChatEDA, EDAid, EDA-Copilot, and DRC-Coder use language models as agents. These agents query, configure, and execute EDA tools.
- **Retrieval-augmented knowledge systems**: RAG-EDA, MM-GRADE, and FabGPT use retrieval augmented generation. They retrieve information from EDA tool documentation and wafer defect databases.
- **Layout and physical design optimization**: LLM4Scldof, LLM-HD, two-stage, CROP, OptAware-PRTP, and EIM address standard cell design, routing, placement, and timing prediction. They use language models and multimodal learning.
- **Design knowledge and instruction alignment**: ChipAlign aligns language model instructions with chip design practices. It uses geodesic interpolation to do this.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2023-08 | [ChatEDA](https://arxiv.org/pdf/2308.10204) | Chateda: A large language model powered autonomous agent for eda | [ChatEDAv1](https://github.com/wuhy68/ChatEDAv1) | n/a |
| 2024-05-24 | [LLM4Scldof](https://arxiv.org/pdf/2406.06549?) | Large language model (llm) for standard cell layout design optimization | n/a | n/a |
| 2024-06-23 | LLM-HD | LLM-HD: Layout Language Model for Hotspot Detection with GDS Semantic Encoding | n/a | n/a |
| 2024-07 | RAG-[EDA](https://arxiv.org/pdf/2407.15353) | Customized retrieval augmented generation and benchmarking for eda tool documentation qa | [RAG-EDA](https://github.com/lesliepy99/RAG-EDA) | n/a |
| 2024-07-15 | [FabGPT](https://arxiv.org/pdf/2407.10810?) | Fabgpt: An efficient large multimodal model for complex wafer defect knowledge queries | n/a | n/a |
| 2024-08-24 | two-[stage](https://ojs.aaai.org/index.php/AAAI/article/view/34479) | Intelligent opc engineer assistant for semiconductor manufacturing | n/a | n/a |
| 2024-11-28 | DRC-[Coder](https://dl.acm.org/doi/pdf/10.1145/3698364.3705347) | Drc-coder: Automated drc checker code generation using llm autonomous agent | n/a | n/a |
| 2024-12 | [ChipAlign](https://arxiv.org/pdf/2412.19819?) | Chipalign: Instruction alignment in large language models for chip design via geodesic interpolation | n/a | n/a |
| 2025-02-15 | [EDAid](https://arxiv.org/abs/2502.10857) | Divergent Thoughts toward One Goal: LLM-based Multi-Agent Collaboration System for Electronic Design Automation | n/a | n/a |
| 2025-07-02 | [CROP](https://arxiv.org/abs/2507.02128) | CROP: Circuit Retrieval and Optimization with Parameter Guidance using LLMs | n/a | n/a |
| 2025-10-01 | OptAware-PRTP | An Optimization-Aware Prerouting Timing Prediction Framework Based on Multimodal Learning | n/a | n/a |
| 2025-10-18 | EDA-Copilot | EDA-Copilot: A RAG-Powered Intelligent Assistant for EDA Tools | n/a | n/a |
| 2025-10-27 | MM-GRADE | MM-GRADE: A Multi-Modal EDA Tool Documentation QA Framework Leveraging Retrieval Augmented Generation | [MM-GRADE](https://github.com/lesliepy99/MM-GRADE-Benchmarks-ICCAD) | n/a |
| 2026-04-28 | [EIM](https://arxiv.org/abs/2604.25191) | How Can Reinforcement Learning Achieve Expert-level Placement? | n/a | n/a |

## Notable entries

- **EDAid** (2025): EDAid is a multi-agent system that uses language models for EDA.
- **RAG-EDA** (2024): RAG-EDA uses retrieval augmented generation for EDA tool documentation. Code is available.
- **MM-GRADE** (2025): MM-GRADE is a multimodal framework for EDA tool documentation that uses retrieval augmented generation.
- **ChatEDA** (2023): ChatEDA is an autonomous agent that uses language models for EDA. Code is available.
- **EIM** (2026): EIM uses reinforcement learning for placement.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **ChatEDA** ([arXiv:2308.10204](https://arxiv.org/abs/2308.10204)). Circuit designers must integrate a complex set of EDA tools to improve interoperability. The paper presents an autonomous agent that uses a large language model to manage task decomposition, script generation, and execution.
- **LLM4Scldof** ([arXiv:2406.06549](https://arxiv.org/abs/2406.06549)). Current design automation tools struggle to make competitive and routable layouts for complex sequential standard cells in 2nm technology. A large language model with ReAct prompting makes cluster constraints that fix routability and decrease average cell area by 4.65%.
- **RAG-EDA** ([arXiv:2407.15353](https://arxiv.org/abs/2407.15353)). Off-the-shelf retrieval augmented generation flows have problems with question answering for electronic design automation tool documentation. The authors present a custom RAG framework with three domain-specific techniques and release the ORD-QA benchmark for OpenROAD.
- **FabGPT** ([arXiv:2407.10810](https://arxiv.org/abs/2407.10810)). Manual threshold settings are subjective, and minute defects under complex wafer backgrounds are hard to detect. The authors present a large multimodal model with a modulation module and interactive corpus training for defect detection and queries.
- **ChipAlign** ([arXiv:2412.19819](https://arxiv.org/abs/2412.19819)). Chip design language models do not follow human instructions well, and this limits their use as assistants for engineers. ChipAlign merges an instruction model with a chip model by geodesic interpolation and improves IFEval scores by up to 26.6%.
- **EDAid** ([arXiv:2502.10857](https://arxiv.org/abs/2502.10857)). Large language models do not fully understand EDA tools, and errors in long chains of tool calls make automation fail. EDAid coordinates multiple agents with different thoughts that work toward one goal, and each agent uses a fine-tuned ChipLlama model.
- **CROP** ([arXiv:2507.02128](https://arxiv.org/abs/2507.02128)). The large parameter space of EDA tools makes chip design optimization hard, and manual parameter selection is slow. CROP uses a large language model to search design parameters and retrieves similar circuits to reduce power by 9.9%.
- **EIM** ([arXiv:2604.25191](https://arxiv.org/abs/2604.25191)). Reinforcement learning methods for chip placement train for wirelength and often do not make expert-quality layouts. The authors identify reward design as the main cause and train a reward model with expert trajectories.

## See also

- [Wiki index](../../index.md)
- [Previous: Netlist](07-netlist.md)
- [Next: Analog](09-analog.md)
