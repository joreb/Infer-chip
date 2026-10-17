---
title: Survey & Benchmark
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, benchmark]
sources: []
---

# Survey & Benchmark

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 26 papers.

## What this covers

This section collects surveys, benchmarks, and reviews of AI applied to electronic design automation and VLSI. Large language models (LLMs) are the primary focus. These papers describe what AI does in chip design. Tasks range from high-level EDA automation to low-level hardware coding. Tasks also include design verification and security assessment. Benchmarks define measurement standards for LLM performance on these tasks.

## Themes

- **LLM and GNN surveys for EDA**: Surveys of LLM and GNN methods in EDA (GNN-IC-Reliability-Security, EDA-GNN-Survey, Llm4eda, LLM4EDA, HdvLlm).

- **RTL generation and code benchmarks**: Benchmarks that evaluate LLM performance on Verilog and RTL code (CVDP, RealBench, ChipBench, RTL-BenchMT, RTL-BenchLS, AssertLLM2).

- **Circuit foundation models and multimodal evaluation**: Foundation models for circuits (LCM, FoundationAI) and multimodal benchmarks for circuits (MMCircuitEval).

- **LLM-guided EDA workflows**: Workflows that use LLMs to guide EDA tasks in SoC security, hardware design, and automation (LLM4SS, llm-guided, Llm-aided).

- **Reliability and failure analysis**: Studies of LLM limitations, generalization, and failure modes in hardware design (SimEval, RevolutionOrHype, LLMsFailRTL, HWE-Bench).

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2023-01-16 | [GNN-IC-Reliability-Security](https://arxiv.org/abs/2211.16495) | ASP-DAC 2023 (pp. 83-90) | Graph Neural Networks: A Powerful and Versatile Tool for Advancing Design, Reliability, and Security of ICs | n/a |
| 2023-09-14 | EDA-GNN-Survey | ACM TODAES (Trans. on Design Automation of Electronic Systems), Vol. 26, No. 6, 2022/2023 | A Comprehensive Survey on Electronic Design Automation and Graph Neural Networks: Theory and Applications | n/a |
| 2023-10 | [LLM4SS](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10596266) | Access | LLM for SoC Security: A Paradigm Shift | n/a |
| 2023-12-28 | [Llm4eda](https://arxiv.org/pdf/2401.12224) | arXiv | Llm4eda: Emerging progress in large language models for electronic design automation | [paper list](https://github.com/Thinklab-SJTU/Awesome-LLM4EDA) |
| 2024-03 | [LCM](https://link.springer.com/content/pdf/10.1007/s11432-024-4155-7.pdf) | SCIS 2024 | Large circuit models: opportunities and challenges. | n/a |
| 2024-03-12 | FutureOrMirage | ISPD 2024 (pp. 65-66); extended journal version ACM TODAES 30(6), 2025 | Large Language Models for EDA: Future or Mirage? | n/a |
| 2024-05 | [LFCD]() | ISVLSI 2024 | Llms and the future of chip design: Unveiling security risks and building trust | n/a |
| 2024-06 | [llm-guided](https://dl.acm.org/doi/abs/10.1145/3649476.3660393) | GLSVLSI 2024 | Navigating soc security landscape on llm-guided paths | n/a |
| 2024-10-24 | [Llm-aided](https://arxiv.org/pdf/2410.18582) | arXiv | Llm-aided efficient hardware design automation | n/a |
| 2024-12 | [HdvLlm](https://www.proquest.com/openview/2b7fbab1fe9882dce439c2d611ad0285/1?pq-origsite=gscholar&cbl=2032404) | Electronics 2025 | Hardware design and verification with large language models: A scoping review, challenges, and open issues | n/a |
| 2025-01 | [LLM4EDA](https://dl.acm.org/doi/pdf/10.1145/3715324) | TODAES 2025 | A survey of research in large language models for electronic design automation | n/a |
| 2025-01-20 | SimEval | ASP-DAC 2025 (pp. 1002-1007) | SimEval: Investigating the Similarity Obstacle in LLM-based Hardware Code Generation | n/a |
| 2025-03 | [🌟FoundationAI](https://arxiv.org/pdf/2504.03711) | arXiv | A Survey of Circuit Foundation Model: Foundation AI Models for VLSI Circuit Design and EDA | n/a |
| 2025-06-17 | [CVDP](https://arxiv.org/abs/2506.14074) | arXiv | Comprehensive Verilog Design Problems: A Next-Generation Benchmark Dataset for Evaluating Large Language Models and Agents on RTL Design and Verification | [CVDP](https://github.com/NVlabs/cvdp_benchmark) |
| 2025-06-22 | LLMsDrivingForce | DAC 2025 (62nd ACM/IEEE DAC) | LLMs: A Driving Force in Next Generation Digital Design Automation | n/a |
| 2025-07-20 | [MMCircuitEval](https://arxiv.org/abs/2507.19525) | ICCAD 2025 | MMCircuitEval: A Comprehensive Multimodal Circuit-Focused Benchmark for Evaluating LLMs | [MMCircuitEval](https://github.com/cure-lab/MMCircuitEval) |
| 2025-07-22 | [RealBench](https://arxiv.org/abs/2507.16200) | arXiv | RealBench: Benchmarking Verilog Generation Models with Real-World IP Designs | [RealBench](https://github.com/IPRC-DIP/RealBench) |
| 2025-08 | [LLMsEDA](https://arxiv.org/abs/2508.20030) | arXiv | Large Language Models (LLMs) for Electronic Design Automation (EDA) | n/a |
| 2025-09-05 | [RevolutionOrHype](https://arxiv.org/abs/2509.04905) | ICCAD 2025 (invited panel paper) | Revolution or Hype? Seeking the Limits of Large Models in Hardware Design | n/a |
| 2026-01-05 | [RTL-OPT](https://arxiv.org/abs/2601.01765) | arXiv | A New Benchmark for the Appropriate Evaluation of RTL Code Optimization | n/a |
| 2026-01-29 | [ChipBench](https://arxiv.org/abs/2601.21448) | arXiv | ChipBench: A Next-Step Benchmark for Evaluating LLM Performance in AI-Aided Chip Design | [ChipBench](https://github.com/zhongkaiyu/ChipBench) |
| 2026-04-16 | [HWE-Bench](https://arxiv.org/abs/2604.14709) | arXiv | HWE-Bench: Benchmarking LLM Agents on Real-World Hardware Bug Repair Tasks | n/a |
| 2026-04-26 | [LLMsFailRTL](https://arxiv.org/abs/2606.19347) | arXiv (under submission for EMNLP 2026) | How LLMs Fail and Generalize in RTL Coding for Hardware Design? | n/a |
| 2026-05-15 | [RTL-BenchMT](https://arxiv.org/abs/2605.15537) | DAC 2026 | RTL-BenchMT: Dynamic Maintenance of RTL Generation Benchmark Through Agent-Assisted Analysis and Revision | n/a |
| 2026-05-26 | [AssertLLM2](https://arxiv.org/abs/2605.27472) | arXiv | AssertLLM2: A Comprehensive LLM Benchmark for Assertion Generation from Design Specifications | n/a |
| 2026-06-08 | [RTL-BenchLS](https://arxiv.org/abs/2606.08976) | arXiv | RTL-BenchLS: A Large-Scale Benchmark for RTL Reasoning and Generation with Large Language Models | n/a |

## Notable entries

- **CVDP** (2025-06-17): A benchmark for RTL design. It evaluates LLMs and agents on Verilog problems from real designs, not synthetic tasks.

- **FoundationAI** (2025-03): A survey of foundation models for circuits. Models train directly on VLSI design patterns and EDA workflows.

- **ChipBench** (2026-01-29): A benchmark for LLM-aided chip design. It defines standardized criteria for production-readiness.

- **RevolutionOrHype** (2025-09-05): An ICCAD invited panel that examines limits of large models in hardware design.

- **RTL-BenchLS** (2026-06-08): A large-scale RTL reasoning benchmark. It tracks LLM performance as models and tasks evolve.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **GNN-IC-Reliability-Security** ([arXiv:2211.16495](https://arxiv.org/abs/2211.16495)). The paper answers the need to review graph neural network methods for integrated circuit design. The authors present a generic pipeline that adjusts graph neural network models for design, reliability, and security problems.
- **Llm4eda** ([arXiv:2401.12224](https://arxiv.org/abs/2401.12224)). Modern chip design needs much time, many resources, and much prior expert knowledge. This paper sorts large language model use in electronic design automation into chatbot, HDL generation, and HDL verification and analysis.
- **Llm-aided** ([arXiv:2410.18582](https://arxiv.org/abs/2410.18582)). Because modern chips are complex, hardware engineers spend much effort on design, verification, and physical implementation. The paper explores large language models in EDA for HDL generation, debugging, verification, and implementation, with two case studies.
- **🌟FoundationAI** ([arXiv:2504.03711](https://arxiv.org/abs/2504.03711)). Circuit foundation models are a new technology trend in AI-driven electronic design automation for VLSI circuits. This paper reviews more than 130 works and sorts them into encoder-based and decoder-based types.
- **CVDP** ([arXiv:2506.14074](https://arxiv.org/abs/2506.14074)). Current models show large gaps in hardware design and verification capabilities. The authors present a benchmark of 783 problems in 13 categories and evaluate models with open-source tools.
- **MMCircuitEval** ([arXiv:2507.19525](https://arxiv.org/abs/2507.19525)). The narrow scope of existing benchmarks makes evaluation of multimodal large language models in circuit design difficult. The authors present a benchmark with 3614 question-answer pairs from textbooks and datasheets for digital and analog circuits.
- **RealBench** ([arXiv:2507.16200](https://arxiv.org/abs/2507.16200)). Existing benchmarks do not match real design workflows because their designs are simple and their verification is not strict. The authors present a benchmark of open-source IP designs with multi-modal specifications, 100% line coverage testbenches, and a formal checker.
- **LLMsEDA** ([arXiv:2508.20030](https://arxiv.org/abs/2508.20030)). The growing complexity of integrated circuits makes the design-to-manufacturing workflow labor-intensive and error-prone. This paper reviews large language models in EDA and gives three case studies in design, testing, and optimization.
- **RevolutionOrHype** ([arXiv:2509.04905](https://arxiv.org/abs/2509.04905)). The paper asks if large AI models can improve hardware design or if expectations are too high. It combines views from experts in industry and academia and examines reliability, scalability, and interpretability.
- **RTL-OPT** ([arXiv:2601.01765](https://arxiv.org/abs/2601.01765)). Existing benchmarks evaluate only syntactic correctness of LLM-generated RTL code, not optimization quality in power, performance, and area. The paper introduces RTL-OPT, a benchmark of 36 handcrafted designs and an automated framework that measures PPA improvements.
- **ChipBench** ([arXiv:2601.21448](https://arxiv.org/abs/2601.21448)). Current benchmarks for large language models in chip design are saturated and have limited task diversity. The paper presents a benchmark for these models with 44 Verilog modules, 89 debugging cases, and 132 reference model samples.
- **HWE-Bench** ([arXiv:2604.14709](https://arxiv.org/abs/2604.14709)). Existing benchmarks test large language model agents only on isolated component-level hardware tasks and do not cover full repositories. The authors build a benchmark with 417 bug repair tasks from six open-source projects and verify solutions with simulation flows.
- **LLMsFailRTL** ([arXiv:2606.19347](https://arxiv.org/abs/2606.19347)). Large language models fail to translate sequential programming knowledge into parallel hardware logic. The authors introduce an error taxonomy with four failure types and show a 90.8% initial pass rate ceiling on VerilogEval.
- **RTL-BenchMT** ([arXiv:2605.15537](https://arxiv.org/abs/2605.15537)). Current RTL generation benchmarks contain flawed cases and models overfit to these cases. The paper proposes an agentic framework that automatically revises flawed cases and updates overfitting cases.
- **AssertLLM2** ([arXiv:2605.27472](https://arxiv.org/abs/2605.27472)). Engineers write SystemVerilog Assertions by hand, and this work takes much time and can cause errors. The paper gives a benchmark with 83 real-world designs in 13 categories that tests how LLMs generate assertions.
- **RTL-BenchLS** ([arXiv:2606.08976](https://arxiv.org/abs/2606.08976)). Frontier models already saturate on current RTL benchmarks, which have small designs and cover mainly specification-to-RTL generation. RTL-BenchLS contains over 10,000 formally verified Verilog designs and three new reasoning and generation tasks verified through formal equivalence checking.

## See also

- [Wiki index](../index.md)
- [Previous: Analog](09-analog.md)
- [Next: HLS (High-Level Synthesis)](02-hls.md)
