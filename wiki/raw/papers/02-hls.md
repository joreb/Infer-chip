---
title: HLS (High-Level Synthesis)
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, hls]
sources: []
---

# HLS (High-Level Synthesis)

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 12 papers.

## What this covers

High-level synthesis (HLS) translates algorithmic descriptions in C/C++/SystemC into optimized hardware designs. This section covers AI-driven approaches to automate and improve HLS flows. It particularly emphasizes recent work that uses large language models for generation, verification, and optimization. These papers address how to bridge software abstractions and hardware constraints. They improve design quality and iteration speed through learning methods.

## Themes

- **Graph neural networks for code representation** (HARP, ProgSG): Early approaches that apply GNNs learn semantic representations of HLS designs for downstream tasks such as QoR prediction.
- **LLM-based design generation** (Synthai, Hlspilot, C2hlsc, LLM-assisted-HLS, ChatHLS): These papers use large language models to directly generate HLS code from specifications or perform interactive design synthesis.
- **LLM-driven testing and correctness** (LLMs4HLS, HLSTester, HLSDebugger): These papers evaluate LLM-generated code, detect behavioral bugs, and automatically correct HLS implementations.
- **Agentic and multi-agent systems** (Pragmas2Partners): These papers treat design optimization and code iteration as collaborative agent processes rather than monolithic generators.
- **Hybrid learning for QoR prediction** (DiffHLS): These papers combine graph representations with LLM code embeddings for performance and quality prediction in HLS.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2023-10-28 | [HARP](https://par.nsf.gov/servlets/purl/10539416) | Robust GNN-based Representation Learning for HLS | n/a | n/a |
| 2024-5-25 | [Synthai](https://arxiv.org/pdf/2405.16072?) | Synthai: A multi agent generative ai framework for automated modular hls design generation. | n/a | n/a |
| 2024-6-13 | [ProgSG](https://dl.acm.org/doi/pdf/10.1145/3670474.3685952) | Cross-modality program representation learning for electronic design automation with high-level synthesis. | n/a | n/a |
| 2024-08-13 | [Hlspilot](https://dl.acm.org/doi/pdf/10.1145/3676536.3676781) | Hlspilot: Llm-based high-level synthesis | n/a | n/a |
| 2024-8-19 | [LLMs4HLS](https://dl.acm.org/doi/pdf/10.1145/3676536.3699507) | Are llms any good for high-level synthesis? | n/a | n/a |
| 2024-11-29 | [C2hlsc](https://dl.acm.org/doi/pdf/10.1145/3734524) | C2hlsc: Leveraging large language models to bridge the software-tohardware design gap | n/a | n/a |
| 2025-2-19 | [LLM-assisted-HLS](https://dl.acm.org/doi/pdf/10.1145/3658617.3697616) | Exploring code language models for automated hls-based hardware generation: Benchmark, infrastructure and analysis | n/a | n/a |
| 2025-04-20 | [HLSTester](https://arxiv.org/abs/2504.14641) | HLSTester: Efficient Testing of Behavioral Discrepancies with LLMs for High-Level Synthesis | n/a | n/a |
| 2025-7-1 | [ChatHLS](https://arxiv.org/pdf/2507.00642) | ChatHLS: Towards Systematic Design Automation and Optimization for High-Level Synthesis | n/a | n/a |
| 2025-07-29 | [HLSDebugger](https://arxiv.org/abs/2507.21485) | HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions | [HLSDebugger](https://github.com/hkust-zhiyao/HLSDebugger) | n/a |
| 2026-02-01 | [Pragmas2Partners](https://arxiv.org/abs/2602.01401) | From Pragmas to Partners: A Symbiotic Evolution of Agentic High-Level Synthesis | n/a | n/a |
| 2026-04-10 | [DiffHLS](https://arxiv.org/abs/2604.09240) | DiffHLS: Differential Learning for High-Level Synthesis QoR Prediction with GNNs and LLM Code Embeddings | n/a | n/a |

## Notable entries

- **Pragmas2Partners** (2026-02-01): This paper frames HLS optimization as a symbiotic multi-agent process rather than a single-pass generation or offline tool.
- **HLSDebugger** (2025-07-29): This paper is the only one to address the correctness gap. It detects and fixes logic bugs in LLM-generated HLS with concrete code solutions. Among the papers in this set, only this paper has released code.
- **LLMs4HLS** (2024-08-19): This empirical benchmark study from ICCAD establishes baselines and failure modes for LLM application to HLS. It was published at the same conference as Hlspilot and provides comparative grounding for the rapidly expanding LLM-HLS field.
- **DiffHLS** (2026-04-10): This paper combines graph neural networks with LLM embeddings for QoR prediction. It represents the most recent synthesis of symbolic and learned representations for hardware optimization.
- **ProgSG** (2024-06-13): This paper introduces cross-modality representation learning. It combines techniques from both code analysis and hardware modeling. Later multi-modal approaches to HLS automation use this technique.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **Synthai** ([arXiv:2405.16072](https://arxiv.org/abs/2405.16072)). The paper presents a method that automates the creation of high-level synthesis designs for complex hardware tasks. It uses ReAct agents, chain-of-thought prompting, web search, and retrieval-augmented generation in a decision graph to make synthesizable multi-module designs.
- **HLSTester** ([arXiv:2504.14641](https://arxiv.org/abs/2504.14641)). In high-level synthesis, behavioral discrepancies appear between C/C++ programs and FPGA circuits, and existing tests need much human effort. HLSTester uses LLMs to generate HLS-compatible testbenches, applies backward slicing to analyze discrepancies, and filters redundant test inputs.
- **ChatHLS** ([arXiv:2507.00642](https://arxiv.org/abs/2507.00642)). Strict coding constraints and design-specific optimizations limit the adoption of High-Level Synthesis. ChatHLS uses specialized LLMs for automated debugging and directive tuning and improves debugging by 32.6% relative to Gemini-3-pro.
- **HLSDebugger** ([arXiv:2507.21485](https://arxiv.org/abs/2507.21485)). Debugging HLS code is difficult for designers with little hardware knowledge, and good circuit data and test cases are rare. HLSDebugger makes a labeled dataset of 300K samples and uses an encoder-decoder model to find, classify, and correct logic bugs.
- **Pragmas2Partners** ([arXiv:2602.01401](https://arxiv.org/abs/2602.01401)). This paper asks if high-level synthesis still matters when AI agents design hardware. It explains why HLS helps agents, lists three tool limits, and gives a taxonomy for agent and human roles.
- **DiffHLS** ([arXiv:2604.09240](https://arxiv.org/abs/2604.09240)). Exploring pragma choices in high-level synthesis takes much time because each design point needs slow synthesis. The framework encodes kernel and design graphs with GNN branches, uses LLM code embeddings, and predicts baseline and delta.

## See also

- [Wiki index](../../index.md)
- [Previous: Survey & Benchmark](01-survey-and-benchmark.md)
- [Next: RTL (Register Transfer Level)](03-rtl.md)
