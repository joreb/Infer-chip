---
title: RTL (Register Transfer Level)
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, rtl]
sources: []
---

# RTL (Register Transfer Level)

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 97 papers. It is the largest section of the index.

## What this covers

RTL (Register Transfer Level) is the main abstraction for hardware design. Engineers use HDLs such as Verilog and VHDL. This section tracks LLM-based approaches to RTL generation. These approaches range from English-to-Verilog translation to multi-agent workflows and reinforcement learning. These methods address problems in four areas: code correctness, pattern matching, hallucination prevention, and EDA integration. The section covers benchmarks, domain adaptation strategies, evaluation frameworks, and agentic systems.

## Themes

- **Foundational LLM-based Verilog generation:** Dave, VGen, VeriGen, ChipChat, Chipgpt, GPT4AIGChip, Rtlcoder, chipgptft. These are systems that translate natural language and specifications to RTL code.

- **Domain adaptation and fine-tuning:** ChipNeMo, RTLCoder, chipgptft, OpenLLM-RTL, MG-Verilog. These are models trained on hardware datasets to improve code quality and EDA understanding.

- **Evaluation and benchmarking frameworks:** Verilogeval, CreativEval, RTL-Repo, VHDLEval, ReVerilogeval, MetRex. These are methods to test RTL code for correctness, creativity, and coverage.

- **Multi-agent and agentic RTL flows:** Mage, Rtlsquad, VeriDispatcher, ChipCraftBrain, SiliconMind-V1, VeriGraphi, CorrectHDL, Dr. RTL. These are systems that coordinate multiple specialized models and reasoning agents for synthesis, verification, and optimization.

- **Reasoning and advanced prompting strategies:** MCTS, AttenSink, VFlow, VToT, ChipSeek-R1, VeriOpt, VeriRL, StepPRM-RTL. These are techniques that use tree search, process rewards, reinforcement learning, and hierarchical prompting to improve code quality.

- **Hallucination mitigation and correctness:** HDLCORE, Invertible-HDL, HaVen, Origen, Craftrtl, RTLSeeker, CorrectHDL. These are methods to detect, prevent, or repair logical errors and mismatches with specifications in code.

- **Multimodal and cross-format approaches:** chipgptv, CircuitFusion, MOSS, En2asic, LEGO, QiMeng-CRUX. These are systems that use circuit diagrams, schematics, architectural specifications, and hybrid representations alongside text.

- **Synthesis optimization and PPA prediction:** MasterRTL, RocketPPA, PPA-RTL, VeriOpt, PipeRTL, RTL-Sequencer. These are systems that predict and optimize power, performance, and area during RTL generation without full EDA synthesis.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2020-8-27 | [Dave](https://dl.acm.org/doi/pdf/10.1145/3380446.3430634) | MLCAD 2020 | Dave: Deriving automatically verilog from english | n/a |
| 2021-10-10 | [Design2Vec](https://proceedings.neurips.cc/paper/2021/file/c5aa65949d20f6b20e1a922c13d974e7-Paper.pdf) | NeurIPS 2021 | Learning semantic representations to verify hardware designs | n/a |
| 2022-12-13 | [VGen](https://arxiv.org/pdf/2212.11140)🔥 | DATE 2023 | Benchmarking large language models for automated verilog rtl code generation | [VGen](https://github.com/shailja-thakur/VGen) |
| 2023-2-17 | [paper](https://eprint.iacr.org/2023/212.pdf) | n/a | Generating secure hardware using chatgpt resistant to cwes | n/a |
| 2023-5-22 | [Chip-chat](https://arxiv.org/pdf/2305.13243)🔥 | MLCAD 2023 | Chip-chat: Challenges and opportunities in conversational hardware design | [ChipChatData](https://github.com/MJoergen/ChipChatData) |
| 2023-5-23 | [Chipgpt](https://arxiv.org/pdf/2305.14019)🔥 | arXiv | Chipgpt: How far are we from natural language hardware design | n/a |
| 2023-7-28 | [VeriGen](https://dl.acm.org/doi/pdf/10.1145/3643681)🔥 | TODAES 2024 | Verigen: A large language model for verilog code generation | [VeriGen](https://github.com/SohamD34/VeriGen?tab=readme-ov-file) |
| 2023-9-14 | [Verilogeval](https://arxiv.org/pdf/2309.07544)🔥 | ICCAD 2023 | Verilogeval: Evaluating large language models for verilog code generation | [verilog-eval](https://github.com/NVlabs/verilog-eval) |
| 2023-9-19 | [GPT4AIGChip](https://arxiv.org/pdf/2309.10730)🔥 | ICCAD 2023 | GPT4AIGChip: Towards next-generation AI accelerator design automation via large language models. | n/a |
| 2023-10-31 | [ChipNeMo](https://arxiv.org/pdf/2311.00176)🔥 | arXiv | ChipNeMo: Domain-Adapted LLMs for Chip Design | n/a |
| 2023-11-8 | [Autochip](https://arxiv.org/pdf/2311.04887)🔥 | arXiv | Autochip: Automating hdl generation using llm feedback | [AutoChip](https://github.com/shailja-thakur/AutoChip) |
| 2023-12-8 | SNS v2 | MICRO 2023 | Fast, robust and transferable prediction for hardware logic synthesis | n/a |
| 2023-12-14 | [Rtlcoder](https://arxiv.org/pdf/2312.08617) | TCAD 2024 | Rtlcoder: Fully open-source and efficient llm-assisted rtl code generation technique | [RTL-Coder](https://github.com/hkustzhiyao/RTL-Coder) |
| 2024-01-01 | [MasterRTL](https://arxiv.org/abs/2311.08441) | IEEE TCAD (DOI 10.1109/TCAD.2024.3420904) | Transferable Presynthesis PPA Estimation for RTL Designs With Data Augmentation Techniques | n/a |
| 2024-1-12 | [AttenSink](https://arxiv.org/pdf/2401.08683) | arxiv | Zero-shot rtl code generation with attention sink augmented large language models | n/a |
| 2024-2-5 | [MCTS](https://arxiv.org/pdf/2402.03289) | arxiv | Make every move count: Llm-based high-quality rtl code generation using mcts | n/a |
| 2024-2-23 | [Betterv](https://arxiv.org/pdf/2402.03375) | ICML 2024 | Betterv: Controlled verilog generation with discriminative guidance | n/a |
| 2024-3-11 | [En2asic](https://arxiv.org/pdf/2403.07039?) | arxiv | From english to asic: Hardware implementation with large language model | n/a |
| 2024-3-17 | [chipgptft](https://dl.acm.org/doi/pdf/10.1145/3649329.3657356) | DAC 2024 | Data is all you need: Finetuning llms for chip design via an automated design-data augmentation framework | [chipgptft](https://github.com/aichipdesign/chipgptft) |
| 2024-4-12 | [Creativeval](https://arxiv.org/pdf/2404.08806) | LAD 2024 | Creativeval: Evaluating creativity of llm-based hardware code generation | [CreativEval](https://github.com/matthewdelorenzo/CreativEval/) |
| 2024-5-27 | [Rtl-repo](https://arxiv.org/pdf/2405.17378?) | LAD 2024 | Rtl-repo: A benchmark for evaluating llms on large-scale rtl design projects | [code](https://github.com/AUCOHL/RTL-Repo) |
| 2024-6-6 | [Vhdl-eval](https://arxiv.org/pdf/2406.04379?) | LAD 2024 | Vhdl-eval: A framework for evaluating large language models in vhdl code generation | n/a |
| 2024-7-2 | [Mg-verilog](https://arxiv.org/pdf/2407.01910?) | LAD 2024 | Mg-verilog: Multi-grained dataset towards enhanced llm-assisted verilog generation | [code](https://github.com/GATECH-EIC/mg-verilog) |
| 2024-7-4 | [CBA](https://arxiv.org/pdf/2407.18326) | arxiv | Classification-based automatic hdl code generation using llms | n/a |
| 2024-7-11 | [chipgptv](https://dl.acm.org/doi/pdf/10.1145/3676536.3676679) | ICCAD 2024 | Natural language is not enough: Benchmarking multi-modal generative ai for verilog generation | [code](https://github.com/aichipdesign/chipgptv) |
| 2024-7-15 | [Codev](https://arxiv.org/pdf/2407.10424) | arxiv | Codev: Empowering llms for verilog generation through multi-level summarization | [CodeV](https://github.com/IPRC-DIP/CodeV) |
| 2024-7-21 | [VeriSeek](https://arxiv.org/pdf/2407.18271) | arxiv | Large Language Model for Verilog Generation with Code-Structure-Guided Reinforcement Learning | n/a |
| 2024-7-23 | [Origen](https://arxiv.org/pdf/2407.16237?) | ICCAD 2024 | Origen: Enhancing rtl code generation with code-to-code augmentation and self-reflection | [OriGen](https://github.com/pku-liang/OriGen) |
| 2024-7-23 | [Hp4lcd](https://arxiv.org/pdf/2407.18276?) | MLCAD 2024 | Rome was not built in a single step: Hierarchical prompting for llm-based chip design | n/a |
| 2024-7-24 | [Autovcoder](https://arxiv.org/pdf/2407.18333?) | ICCD 2024 | Autovcoder: A systematic framework for automated verilog code generation using llms | [AutoVCoder](https://github.com/sjtu-zhao-lab/AutoVCoder) |
| 2024-8-15 | [Verilogcoder](https://arxiv.org/pdf/2408.08927) | AAAI 2025 | Verilogcoder: Autonomous verilog coding agents with graph-based planning and abstract syntax tree (ast)-based waveform tracing tool | [VerilogCoder](https://github.com/NVlabs/VerilogCoder) |
| 2024-8-20 | [ReVerilogeval](https://arxiv.org/pdf/2408.11053v1) | arxiv | Revisiting verilogeval: Newer llms, in-context learning, and specification-to-rtl tasks | n/a |
| 2024-09-04 | [RTLRewriter](https://arxiv.org/abs/2409.11414) | ICCAD 2024 | RTLRewriter: Methodologies for Large Models aided RTL Code Optimization | n/a |
| 2024-9-9 | [CoDes](https://dl.acm.org/doi/pdf/10.1145/3670474.3685966) | MLCAD 2024 | Chain-of-descriptions: Improving code llms for vhdl code generation and summarization | n/a |
| 2024-9-19 | [Craftrtl](https://arxiv.org/pdf/2409.12993?) | ICLR 2025 | Craftrtl: High-quality synthetic data generation for verilog code models with correct-by-construction non-textual representations and targeted code repair | [craftrtl](https://github.com/nvlabs/craftrtl) |
| 2024-11-5 | [MetRex](https://dl.acm.org/doi/pdf/10.1145/3658617.3697625) | ASP- DAC 2025 | MetRex: A Benchmark for Verilog Code Metric Reasoning Using LLMs | [MetRex](https://github.com/scale-lab/MetRex) |
| 2024-11-21 | [AIVRIL2](https://arxiv.org/pdf/2412.04485) | DATE 2025 | Eda-aware rtl generation with large language models | n/a |
| 2024-11-25 | [Opl4gpt](https://eprint.iacr.org/2024/1905.pdf) | ASP-DAC 2025 | Opl4gpt: An application space exploration of optimal programming language for hardware design by llm | n/a |
| 2024-12-09 | [PyraNet](https://arxiv.org/abs/2412.06947) | DAC 2025 | PyraNet: A Multi-Layered Hierarchical Dataset for Verilog | [PyraNet](https://huggingface.co/datasets/bnadimi/PyraNet-Verilog) |
| 2024-12-10 | [Mage](https://arxiv.org/pdf/2412.07822) | DAC 2025 | Mage: A multi-agent engine for automated rtl code generation | [MAGE](https://github.com/stable-lab/MAGE) |
| 2025-1-6 | [Rtlsquad](https://arxiv.org/pdf/2501.05470?) | arxiv | Rtlsquad: Multi-agent based interpretable rtl design | n/a |
| 2025-01-09 | [HaVen](https://arxiv.org/pdf/2501.04908) | DATE 2025 | HaVen: Hallucination-Mitigated LLM for Verilog Code Generation Aligned with HDL Engineers | n/a |
| 2025-01-20 | LLSM | ASP-DAC 2025 (30th Asia and South Pacific Design Automation Conference; DOI 10.1145/3658617.3697618) | LLSM: LLM-enhanced Logic Synthesis Model with EDA-guided CoT Prompting, Hybrid Embedding and AIG-tailored Acceleration | n/a |
| 2025-2-15 | [Lintllm](https://arxiv.org/pdf/2502.10815) | arxiv | Lintllm: An open-source verilog linting framework based on large language models | n/a |
| 2025-2-20 | [Deeprtl](https://arxiv.org/pdf/2502.15832?) | ICLR 2025 | Deeprtl: Bridging verilog understanding and generation with a unified representation model | n/a |
| 2025-3-4 | [CircuitEncoder](https://zhiyaoxie.com/files/ASPDAC25_CircuitEncoder.pdf) | ASP-DAC 2025 | A self-supervised, pre-trained, and cross-stage-aligned circuit encoder provides a foundation for various design tasks | n/a |
| 2025-03-18 | [VFlow](https://arxiv.org/pdf/2504.03723) | arxiv | VFlow: Discovering Optimal Agentic Workflows for Verilog Generation | n/a |
| 2025-3-19 | [Openllm-rtl](https://arxiv.org/pdf/2503.15112) | ICCAD 2024 | Openllm-rtl: Open dataset and benchmark for llm-aided design rtl generation | n/a |
| 2025-03-27 | [RocketPPA](https://arxiv.org/pdf/2503.21971) | arxiv | RocketPPA: Code-Level Power, Performance, and Area Prediction via LLM and Mixture of Experts | n/a |
| 2025-03-30 | [HDLCORE](https://arxiv.org/pdf/2503.16528) | arxiv | HDLCORE: A TRAINING-FREE FRAMEWORK FOR MIT-IGATING HALLUCINATIONS IN LLM-GENERATED HDL | n/a |
| 2025-04-20 | [ReasoningV](https://arxiv.org/abs/2504.14560) | arXiv | ReasoningV: Efficient Verilog Code Generation with Adaptive Hybrid Reasoning Model | [ReasoningV](https://github.com/BUAA-CLab/ReasoningV) |
| 2025-5-4 | [Circuitfusion](https://arxiv.org/pdf/2505.02168) | ICLR 2025 | Circuitfusion: multimodal circuit representation learning for agile chip design | [CircuitFusion](https://github.com/hkust-zhiyao/CircuitFusion) |
| 2025-5-9 | [Spec2Doc2RTL](https://ieeexplore.ieee.org/abstract/document/11101140) | ISEDA | Spec2Doc2RTL: RTL Generation from Specification with Natural Language Representation | n/a |
| 2025-05-09 | [FreeV](https://arxiv.org/pdf/2505.06096?) | DAC 2025 | Free and Fair Hardware: A Pathway to Copyright Infringement-Free Verilog Generation using LLMs | n/a |
| 2025-5-21 | [LLM4GV](https://ieeexplore.ieee.org/document/10992751) | DATE 2025 | LLM4GV: An LLM-Based Flexible Performance-Aware Framework for GEMM Verilog Generation | n/a |
| 2025-5-21 | [Data Augmentation and RL](https://ieeexplore.ieee.org/abstract/document/10992897) | DATE 2025 | Improving LLM-Based Verilog Code Generation with Data Augmentation and RL | n/a |
| 2025-5-21 | [VToT](https://ieeexplore.ieee.org/document/10993029) | DATE 2025 | VToT: Automatic Verilog Generation via LLMs with Tree of Thoughts Prompting | n/a |
| 2025-05-30 | [CodeV-R1](https://arxiv.org/abs/2505.24183) | NeurIPS 2025 | QiMeng-CodeV-R1: Reasoning-Enhanced Verilog Generation | [CodeV-R1](https://github.com/IPRC-DIP/CodeV-R1) |
| 2025-06-01 | MOSS | DAC 2025 (62nd ACM/IEEE Design Automation Conference) | MOSS: Multi-Modal Representation Learning on Sequential Circuits | n/a |
| 2025-06-24 | [PPA-RTL](https://dl.acm.org/doi/abs/10.1109/DAC63849.2025.11132897) | DAC 2025 | Hardware Generation with High Flexibility using Reinforcement Learning Enhanced LLMs | n/a |
| 2025-6-26 | [OpenRTLSet](https://ieeexplore.ieee.org/abstract/document/11106163/) | ICLAD 2025 | OpenRTLSet: A Fully Open-Source Dataset for Large Language Model-based Verilog Module Design | n/a |
| 2025-6-26 | [EvoVerilog](https://arxiv.org/abs/2508.13156) | arxiv | EvoVerilog: Large Langugage Model Assisted Evolution of Verilog Code | n/a |
| 2025-07-07 | [ChipSeek-R1](https://arxiv.org/abs/2507.04736) | ACL 2026 | ChipSeek: Optimizing Verilog Generation via EDA-Integrated Reinforcement Learning | n/a |
| 2025-07-20 | [VeriOpt](https://arxiv.org/abs/2507.14776) | ICCAD 2025 | VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs | n/a |
| 2025-08-25 | [VeriRL](https://arxiv.org/abs/2508.18462) | arXiv | VeriRL: Boosting the LLM-based Verilog Code Generation via Reinforcement Learning | [VeriRL](https://github.com/omniAI-Lab/VeriRL) |
| 2025-08-26 | [SynCircuit](https://arxiv.org/abs/2509.00071) | DAC 2025 | SynCircuit: Automated Generation of New Synthetic RTL Circuits Can Enable Big Data in Circuits | n/a |
| 2025-09-01 | SynC-LLM | EMNLP 2025 | SynC-LLM: Generation of Large-Scale Synthetic Circuit Code with Hierarchical Language Models | [SynC-LLM](https://github.com/hkust-zhiyao/SynCircuitData) |
| 2025-10-26 | [FADR](https://ece.k-state.edu/research/hardware-security/papers/iccad.pdf) | ICCAD 2025 | Building Reasoning LLMs for Hardware Design Generation via Function-Aligned Differentiated Revision | n/a |
| 2025-10-26 | LLM4Verilog | ICCAD 2025 | LLM4Verilog: Building Large-Scale, High-Quality Data Infrastructure for Verilog Code Generation via Community Efforts | n/a |
| 2025-11-08 | [ArchCraft](https://arxiv.org/abs/2511.06067) | arXiv | Automating Hardware Design and Verification from Architectural Papers via a Neural-Symbolic Graph Framework | n/a |
| 2025-11-15 | [EARL](https://arxiv.org/abs/2511.12033) | CTS 2026 (Chips to Systems Conference) | EARL: Entropy-Aware RL Alignment of LLMs for Reliable RTL Code Generation | n/a |
| 2025-11-20 | [CorrectHDL](https://arxiv.org/abs/2511.16395) | arXiv | CorrectHDL: Agentic HDL Design with LLMs Leveraging High-Level Synthesis as Reference | n/a |
| 2025-11-25 | [QiMeng-CRUX](https://arxiv.org/abs/2511.20099) | AAAI 2026 | QiMeng-CRUX: Narrowing the Gap Between Natural Language and Verilog via Core Refined Understanding eXpression for Circuit Design | [QiMeng-CRUX](https://github.com/Taskii-Lei/QiMeng-CRUX-V) |
| 2025-11-25 | [Invertible-HDL](https://arxiv.org/abs/2512.03053) | arXiv | Mitigating hallucinations and omissions in LLMs for invertible problems: An application to hardware logic design automation | n/a |
| 2025-11-27 | [VeriDispatcher](https://arxiv.org/abs/2511.22749) | arXiv | VeriDispatcher: Multi-Model Dispatching through Pre-Inference Difficulty Prediction for RTL Generation Optimization | n/a |
| 2025-12-04 | [David vs. Goliath](https://arxiv.org/abs/2512.05073) | arXiv | David vs. Goliath: Can Small Models Win Big with Agentic AI in Hardware Design? | n/a |
| 2025-12-05 | [ChipMind](https://arxiv.org/abs/2512.05371) | AAAI 2026 | ChipMind: Retrieval-Augmented Reasoning for Long-Context Circuit Design Specifications | n/a |
| 2026-01-26 | [EvolVE](https://arxiv.org/abs/2601.18067) | arXiv | EvolVE: Evolutionary Search for LLM-based Verilog Generation and Optimization | [EvolVE](https://github.com/weiber2002/ICRTL) |
| 2026-01-31 | [LocalV](https://arxiv.org/abs/2602.00704) | arXiv | LocalV: Exploiting Information Locality for IP-level Verilog Generation | n/a |
| 2026-02-03 | [LLM-FSM](https://arxiv.org/abs/2602.07032) | arXiv | LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation | n/a |
| 2026-02-10 | [ACE-RTL](https://arxiv.org/abs/2602.10218) | arXiv | ACE-RTL: When Agentic Context Evolution Meets RTL-Specialized LLMs | n/a |
| 2026-02-10 | [SiliconMind-V1](https://arxiv.org/abs/2603.08719) | arXiv | SiliconMind-V1: Multi-Agent Distillation and Debug-Reasoning Workflows for Verilog Code Generation | n/a |
| 2026-03-29 | [RTLSeek](https://arxiv.org/abs/2603.27630) | DAC 2026 | RTLSeek: Boosting the LLM-Based RTL Generation with Multi-Stage Diversity-Oriented Reinforcement Learning | [RTLSeek](https://anonymous.4open.science/r/DAC2026ID71-ACB4/) |
| 2026-04-16 | [VeriGraphi](https://arxiv.org/abs/2604.14550) | arXiv | VeriGraphi: A Multi-Agent Framework of Hierarchical RTL Generation for Large Hardware Designs | n/a |
| 2026-04-16 | [Dr. RTL](https://arxiv.org/abs/2604.14989) | ICCAD 2026 | Dr. RTL: Autonomous Agentic RTL Optimization through Tool-Grounded Self-Improvement | n/a |
| 2026-04-16 | [Self-Evolved ABC](https://arxiv.org/abs/2604.15082) | DAC 2026 | Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC | n/a |
| 2026-04-20 | [VerilogCL](https://arxiv.org/abs/2604.18162) | arXiv | VerilogCL: A Contrastive Learning Framework for Robust LLM-Based Verilog Generation | n/a |
| 2026-04-21 | [ChipCraftBrain](https://arxiv.org/abs/2604.19856) | arXiv | ChipCraftBrain: Validation-First RTL Generation via Multi-Agent Orchestration | n/a |
| 2026-04-25 | [LEGO](https://arxiv.org/abs/2604.23355) | ISEDA 2026 | LEGO: An LLM Skill-Based Front-End Design Generation Platform | n/a |
| 2026-05-03 | [PipeRTL](https://arxiv.org/abs/2605.01836) | arXiv | PipeRTL: Timing-Aware Pipeline Optimization at IR-Level for RTL Generation | n/a |
| 2026-05-13 | [ChipMATE](https://arxiv.org/abs/2605.12857) | arXiv | ChipMATE: Multi-Agent Training via Reinforcement Learning for Enhanced RTL Generation | [ChipMATE](https://github.com/zhongkaiyu/ChipMATE) |
| 2026-05-20 | [Trace2Skill](https://arxiv.org/abs/2605.21810) | arXiv | Trace2Skill: Verifier-Guided Skill Evolution for Long-Context EDA Agents | n/a |
| 2026-05-26 | [Verilog-Evolve](https://arxiv.org/abs/2605.26498) | arXiv | Verilog-Evolve: Feedback-Driven and Skill-Evolving Verilog Generation | n/a |
| 2026-06-02 | [StepPRM-RTL](https://arxiv.org/abs/2606.04246) | DAC 2026 | StepPRM-RTL: Stepwise Process-Reward Guided LLM Fine-Tuning for Enhanced RTL Synthesis | n/a |
| 2026-06-03 | [Alpha-RTL (TTT-RTL)](https://arxiv.org/abs/2606.05253) | arXiv | Alpha-RTL: Test-Time Training for RTL Hardware Optimization | n/a |
| 2026-06-06 | [ROSUM-MCTS](https://arxiv.org/abs/2606.07925) | arXiv | ROSUM-MCTS: Monte Carlo Tree Search-Inspired HDL Code Summarization with Structural Rewards | n/a |
| 2026-07-17 | [RTL-Sequencer](https://arxiv.org/abs/2607.15830) | DAC 2026 | RTL-Sequencer: Towards Scalable RTL Timing Prediction with the Sequence-based Paradigm | n/a |

## Notable entries

- **VeriGen and Verilogeval (2023):** These works established the task of LLM-based Verilog generation and introduced the first systematic evaluation framework. These papers set baselines against which subsequent methods are measured.

- **ChipNeMo (2023):** This paper shows that instruction-tuning LLMs on chip-design-specific datasets improves code quality and reasoning about hardware constraints.

- **Mage, VeriDispatcher, and SiliconMind-V1 (2024 to 2025):** These papers show that agentic coordination of multiple specialized models and tools outperforms single monolithic models for complex RTL tasks.

- **Craftrtl and Origen (2024):** These papers present methods to generate correct-by-construction code. They use synthetic data augmentation, code-to-code augmentation, and self-reflection. These methods address the hallucination problem.

- **ChipSeek-R1, VeriOpt, and VeriRL (2025):** These papers integrate reinforcement learning and process-reward models into RTL generation. EDA-aware optimization and verification feedback guide the generation process. Evaluation now includes end-to-end design metrics, not just code quality.

- **VFlow and ACE-RTL (2025):** These systems discover and optimize workflows dynamically. Instead of fixed pipelines, they learn workflows that adapt to the context of each design task.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **VGen🔥** ([arXiv:2212.11140](https://arxiv.org/abs/2212.11140)). This paper examines if large language models can generate useful Verilog code. The authors train the models with Verilog data from GitHub and textbooks and test the code with test benches.
- **Chip-chat🔥** ([arXiv:2305.13243](https://arxiv.org/abs/2305.13243)). Studies of large language models for hardware design are lacking, so this paper examines their challenges and opportunities. A hardware engineer and a language model design an 8-bit microprocessor and tape out the design in a 130nm process.
- **Chipgpt🔥** ([arXiv:2305.14019](https://arxiv.org/abs/2305.14019)). The paper examines if large language models can generate hardware logic designs from natural language specifications. It presents a four-stage zero-code framework that produces Verilog, corrects and optimizes the programs, and selects the optimal design.
- **Verilogeval🔥** ([arXiv:2309.07544](https://arxiv.org/abs/2309.07544)). The paper presents a framework that evaluates large language models for Verilog code generation. The framework uses 156 problems and tests the generated code with automatic simulation.
- **GPT4AIGChip🔥** ([arXiv:2309.10730](https://arxiv.org/abs/2309.10730)). Designing AI accelerators needs a lot of labor, time, and hardware knowledge, and this blocks non-experts. The authors use large language models with an automatic prompt-generation pipeline and in-context learning to make accelerator designs.
- **ChipNeMo🔥** ([arXiv:2311.00176](https://arxiv.org/abs/2311.00176)). The paper addresses the application of large language models to industrial chip design. The method combines domain-adaptive tokenization, continued pretraining, domain-specific instruction alignment, and adapted retrieval models.
- **Autochip🔥** ([arXiv:2311.04887](https://arxiv.org/abs/2311.04887)). Manual writing and debugging of Verilog code take much time and cause errors in complex designs. AutoChip gives compiler errors and simulation output to large language models to generate 24.20% more accurate Verilog.
- **Rtlcoder** ([arXiv:2312.08617](https://arxiv.org/abs/2312.08617)). Existing RTL generation methods use commercial models, and the lack of high-quality open-source solutions restricts flexibility and data privacy. The authors use a new open-source dataset and a customized algorithm to build a 7B parameter model that outperforms GPT-3.5.
- **MasterRTL** ([arXiv:2311.08441](https://arxiv.org/abs/2311.08441)). Standard RTL evaluation needs time-consuming synthesis steps, and recent machine learning methods do not stay accurate for all designs. The framework converts HDL code to a simple operator graph and estimates timing, power, and area with machine learning.
- **AttenSink** ([arXiv:2401.08683](https://arxiv.org/abs/2401.08683)). Hardware design and optimization need many resources and special skills. This paper uses large language models with a new attention mechanism to generate RTL code from high-level design specifications.
- **MCTS** ([arXiv:2402.03289](https://arxiv.org/abs/2402.03289)). Large language models for register transfer level code generation have compilation failures and low power, performance, and area efficiency. The method adds Monte Carlo tree search lookahead to transformer decoding to produce compilable, correct, and optimized code.
- **Betterv** ([arXiv:2402.03375](https://arxiv.org/abs/2402.03375)). The growing complexity of integrated circuits creates a need for automated circuit design methods. BetterV fine-tunes large language models on processed Verilog datasets and uses generative discriminators to guide generation.
- **En2asic** ([arXiv:2403.07039](https://arxiv.org/abs/2403.07039)). Large language models do not generate HDL code well, and high-quality HDL code datasets are scarce. The authors fine-tune a large language model and reshuffle the HDL dataset, and pass@1 accuracy increases by 10% to 20%.
- **Creativeval** ([arXiv:2404.08806](https://arxiv.org/abs/2404.08806)). Existing evaluations of language models for hardware code generation measure only functional correctness and not creativity. The paper presents a framework that measures four creative qualities of generated hardware designs.
- **Rtl-repo** ([arXiv:2405.17378](https://arxiv.org/abs/2405.17378)). Existing benchmarks do not show the complexity of real-world RTL design projects. The authors present a benchmark of more than 4000 Verilog code samples with full repository context and evaluate several LLMs.
- **Vhdl-eval** ([arXiv:2406.04379](https://arxiv.org/abs/2406.04379)). Existing evaluation frameworks do not cover VHDL code generation by large language models. The authors build a dataset of 202 problems and use self-verifying testbenches to evaluate LLMs.
- **Mg-verilog** ([arXiv:2407.01910](https://arxiv.org/abs/2407.01910)). Existing public hardware datasets are limited in size, complexity, or detail, and this hinders LLMs in hardware design tasks. The paper proposes criteria for high-quality hardware datasets and presents a multi-grained Verilog dataset with a balanced fine-tuning scheme.
- **CBA** ([arXiv:2407.18326](https://arxiv.org/abs/2407.18326)). Large language models generate incorrect HDL code because of hallucination. The method classifies the circuit type, splits the task into sub-procedures, and uses a search method to reduce code variation.
- **Codev** ([arXiv:2407.10424](https://arxiv.org/abs/2407.10424)). High-quality HDL data is scarce, so the application of large language models to HDL generation remains limited. The paper presents a fine-tuning pipeline that combines multi-level summarization data synthesis with a Chat-FIM-Tag supervised fine-tuning method.
- **VeriSeek** ([arXiv:2407.18271](https://arxiv.org/abs/2407.18271)). Public Verilog code is scarce, so pre-training and instruction tuning methods do not learn parallel Verilog code structures well. VeriSeek uses reinforcement learning with code structure information as feedback to refine a pre-trained model for Verilog generation.
- **Origen** ([arXiv:2407.16237](https://arxiv.org/abs/2407.16237)). Open-source language models do not generate RTL code as well as commercial models because few high-quality RTL datasets exist. OriGen uses code-to-code augmentation to improve open-source RTL datasets and self-reflection with compiler feedback to correct syntactic errors.
- **Hp4lcd** ([arXiv:2407.18276](https://arxiv.org/abs/2407.18276)). LLM-assisted HDL generation struggles with complex hardware design tasks. The paper introduces hierarchical prompting techniques and an automation pipeline for stepwise design.
- **Autovcoder** ([arXiv:2407.18333](https://arxiv.org/abs/2407.18333)). Large language models produce many syntax and function errors when they generate Verilog code. AutoVCoder combines a hardware dataset generation method, two-round LLM fine-tuning, and domain-specific retrieval-augmented generation to increase correctness.
- **Verilogcoder** ([arXiv:2408.08927](https://arxiv.org/abs/2408.08927)). Automating hardware design can prevent human errors as integrated circuits become more complex. VerilogCoder uses multiple AI agents with graph-based planning and AST-based waveform tracing to write and fix Verilog code.
- **ReVerilogeval** ([arXiv:2408.11053](https://arxiv.org/abs/2408.11053)). Large language models learn mainly from natural language and software code, and few benchmarks test hardware code generation. The authors test new models against an improved VerilogEval benchmark that adds automatic failure classification, in-context learning, and specification-to-RTL tasks.
- **RTLRewriter** ([arXiv:2409.11414](https://arxiv.org/abs/2409.11414)). Manual RTL code optimization needs skilled engineers and many synthesis iterations, and compiler methods are not sufficient for complex designs. RTLRewriter uses large models, circuit partitioning, multi-modal analysis, cost-aware Monte Carlo tree search, and fast verification to optimize RTL code.
- **Craftrtl** ([arXiv:2409.12993](https://arxiv.org/abs/2409.12993)). Fine-tuned language models for Verilog code have difficulty with non-textual representations and make small mistakes at random. The authors create correct-by-construction data for these representations and inject model errors into open-source code to make repair data.
- **AIVRIL2** ([arXiv:2412.04485](https://arxiv.org/abs/2412.04485)). Large language models often produce RTL code with syntax and functional errors, and manual correction increases the verification workload. The AIvril2 multi-agent system corrects them with EDA tool error logs and gets best-case pass rates of 77% and 66%.
- **PyraNet** ([arXiv:2412.06947](https://arxiv.org/abs/2412.06947)). Large language models generate low quality Verilog code because high quality datasets and fine-tuning methods are not available. The authors present an open-source dataset and a fine-tuning method that uses a multi-layered structure.
- **Mage** ([arXiv:2412.07822](https://arxiv.org/abs/2412.07822)). Single LLM agents find it difficult to produce syntactically and functionally correct Verilog RTL code from natural language instructions. MAGE uses multiple agents, candidate sampling with debugging, and Verilog-state checkpoint checks to generate 95.7% correct code on VerilogEval-Human 2.
- **Rtlsquad** ([arXiv:2501.05470](https://arxiv.org/abs/2501.05470)). Current LLM methods for RTL code generation give no clear reasons for decisions, so engineers cannot easily trust the results. RTLSquad is an LLM-based multi-agent system with squads for design stages that generate improved RTL code and give clear reasons.
- **HaVen** ([arXiv:2501.04908](https://arxiv.org/abs/2501.04908)). Large language models for Verilog code generation do not meet the practical demands of HDL engineering. HaVen uses a taxonomy and a chain-of-thought mechanism to reduce hallucinations and makes new instruction-code pairs that match HDL practices.
- **Lintllm** ([arXiv:2502.10815](https://arxiv.org/abs/2502.10815)). Traditional Verilog linting tools give many false positives and repeated defect reports. LintLLM uses large language models with Prompt of Logic-Tree and Defect Tracker to detect Verilog defects.
- **Deeprtl** ([arXiv:2502.15832](https://arxiv.org/abs/2502.15832)). Prior efforts focus on Verilog generation, neglect Verilog understanding, and show weak alignment between natural language and code. The authors present DeepRTL and fine-tune CodeT5+ with curriculum learning on a dataset that aligns Verilog code with multi-level descriptions.
- **VFlow** ([arXiv:2504.03723](https://arxiv.org/abs/2504.03723)). Hardware design automation faces challenges in generating high-quality Verilog code efficiently. VFlow searches graph-structured LLM invocation sequences and balances functional correctness, area, power, timing, and token cost with cooperative evolution.
- **Openllm-rtl** ([arXiv:2503.15112](https://arxiv.org/abs/2503.15112)). A lack of public datasets and benchmarks prevents development and fair evaluation of LLM solutions for RTL generation. The paper presents RTLLM 2.0 with 50 designs, AssertEval with 18 designs, RTLCoder-Data with 80K samples, and a verification method.
- **RocketPPA** ([arXiv:2503.21971](https://arxiv.org/abs/2503.21971)). Current PPA estimation methods need slow synthesis flows and manual feature engineering. RocketPPA uses an LLM with a mixture-of-experts architecture to predict power, delay, and area directly from HDL code.
- **HDLCORE** ([arXiv:2503.16528](https://arxiv.org/abs/2503.16528)). Large language models produce hallucinations and incorrect hardware description language code because training data is scarce. The training-free framework uses chain-of-thought prompting with self-verification and a two-stage retrieval-augmented generation system.
- **ReasoningV** ([arXiv:2504.14560](https://arxiv.org/abs/2504.14560)). Large language models that generate Verilog code have problems with data quality, reasoning, and computational efficiency. ReasoningV uses hybrid reasoning, a 5,000-example dataset, two-stage training, and adaptive depth that cuts token use by up to 75%.
- **Circuitfusion** ([arXiv:2505.02168](https://arxiv.org/abs/2505.02168)). Growing IC complexity makes design costly and time-consuming, and most AI methods are task-specific or use only circuit structure. CircuitFusion fuses hardware code, structural graph, and functionality summary to learn general representations for different design tasks.
- **FreeV** ([arXiv:2505.06096](https://arxiv.org/abs/2505.06096)). Small Verilog training datasets have few license checks, so fine-tuned LLMs can generate copyright-protected code. The authors present a copyright risk benchmark, FreeSet with over 220k files, and FreeV, a fine-tuned Llama model.
- **CodeV-R1** ([arXiv:2505.24183](https://arxiv.org/abs/2505.24183)). Reinforcement learning for Verilog generation from natural language specifications lacks accurate automatic verification, quality data, and low training cost. The framework uses a rule-based testbench generator, round-trip data synthesis, and a two-stage distill-then-RL training pipeline with adaptive DAPO.
- **EvoVerilog** ([arXiv:2508.13156](https://arxiv.org/abs/2508.13156)). Current Verilog code generation methods need human help and curated datasets, so they do not scale in automatic design workflows. The framework combines large language models with evolutionary algorithms to generate and refine Verilog code without human help.
- **ChipSeek-R1** ([arXiv:2507.04736](https://arxiv.org/abs/2507.04736)). Existing LLM-based methods for RTL code generation do not optimize functional correctness and power, performance, and area together. ChipSeek uses Curriculum-Guided Dynamic Policy Optimization with a hierarchical reward based on feedback from EDA simulators and synthesis tools.
- **VeriOpt** ([arXiv:2507.14776](https://arxiv.org/abs/2507.14776)). Large language models for hardware design generate functionally correct Verilog code but do not consider power, performance, and area metrics. VeriOpt gives specialized roles to LLMs and adds PPA constraints and synthesis reports to produce high-quality synthesizable Verilog.
- **VeriRL** ([arXiv:2508.18462](https://arxiv.org/abs/2508.18462)). Code generation research rarely addresses Verilog because Verilog has concurrent behavior, rigid syntax, and complex simulation. The authors use reinforcement learning with a 53K problem dataset, a trace-back rescore for rewards, and balanced sample weights.
- **SynCircuit** ([arXiv:2509.00071](https://arxiv.org/abs/2509.00071)). The lack of public circuit design data limits the development of AI-assisted IC design methods. The framework uses a diffusion model, circuit constraints, and Monte Carlo tree search to generate valid synthetic RTL circuits.
- **ArchCraft** ([arXiv:2511.06067](https://arxiv.org/abs/2511.06067)). It is difficult to reproduce hardware architectures from papers because source code is not available and HDLs are complex. ArchCraft uses graphs and symbols to convert architectural descriptions from papers into synthesizable Verilog with RTL verification.
- **EARL** ([arXiv:2511.12033](https://arxiv.org/abs/2511.12033)). LLMs that generate RTL code show syntax errors, wrong functions, and weak alignment to designer intent. EARL uses verifiable rewards, gates policy gradients to high-entropy tokens, and improves pass rates by up to 14.7%.
- **CorrectHDL** ([arXiv:2511.16395](https://arxiv.org/abs/2511.16395)). Large language models often cause functional errors in the hardware description language designs that they generate. CorrectHDL repairs syntax errors with retrieval-augmented generation and iteratively corrects functional errors against a high-level synthesis reference.
- **QiMeng-CRUX** ([arXiv:2511.20099](https://arxiv.org/abs/2511.20099)). Existing methods use ambiguous, redundant, and unstructured natural language descriptions for Verilog code generation. The authors introduce CRUX, a structured intermediate space, and a two-stage training framework to improve Verilog code generation.
- **Invertible-HDL** ([arXiv:2512.03053](https://arxiv.org/abs/2512.03053)). Large language models make hallucinations and omissions when they generate hardware description language code from logic condition tables. The method uses the models as a lossless encoder and decoder to reconstruct the tables and detect design errors.
- **VeriDispatcher** ([arXiv:2511.22749](https://arxiv.org/abs/2511.22749)). Different LLMs perform well on different RTL generation tasks, but prior work uses one model only. VeriDispatcher trains compact classifiers to predict task difficulty before inference and routes each task to suitable LLMs.
- **David vs. Goliath** ([arXiv:2512.05073](https://arxiv.org/abs/2512.05073)). Large language model inference needs large amounts of compute and energy, so domain-specific hardware design tasks are expensive and unsustainable. This study evaluates small language models with a curated agentic AI framework on the NVIDIA CVDP benchmark.
- **ChipMind** ([arXiv:2512.05371](https://arxiv.org/abs/2512.05371)). Large language models have restricted context windows and cannot reason well over long circuit design specifications. ChipMind changes the specifications into a knowledge graph and uses adaptive retrieval and semantic filtering to improve results by 34.59%.
- **EvolVE** ([arXiv:2601.18067](https://arxiv.org/abs/2601.18067)). Verilog design needs much manual work and expert knowledge, and LLMs do not fully capture hardware logic and concurrency. EvolVE examines evolution strategies such as Monte Carlo Tree Search for chip design and reaches 98.1% on VerilogEval v2.
- **LocalV** ([arXiv:2602.00704](https://arxiv.org/abs/2602.00704)). Existing language models and agents do not scale to industrial IP-level RTL code generation. The paper proposes a multi-agent framework that divides long RTL generation into short tasks and achieves a 45.0% pass rate.
- **LLM-FSM** ([arXiv:2602.07032](https://arxiv.org/abs/2602.07032)). The paper evaluates how well large language models recover finite-state machine behavior from natural-language specifications and produce RTL code. A fully automated pipeline builds finite-state machines and makes 1,000 verified problems with natural-language specifications, reference RTL, and testbenches.
- **ACE-RTL** ([arXiv:2602.10218](https://arxiv.org/abs/2602.10218)). Prior RTL code generation methods use either domain-adapted models or agentic systems with generic LLMs. ACE-RTL uses Agentic Context Evolution to combine an RTL-specialized LLM with a reasoning LLM for iterative code refinement.
- **SiliconMind-V1** ([arXiv:2603.08719](https://arxiv.org/abs/2603.08719)). Existing Verilog code generation methods use commercial models or external verification tools and do not fully guarantee functional correctness. This paper proposes a multi-agent framework with testbench-driven verification that trains a local model to generate, test, and debug RTL.
- **RTLSeek** ([arXiv:2603.27630](https://arxiv.org/abs/2603.27630)). Functionally verifiable high-quality data for LLM-based RTL generation is scarce, and existing post-training produces one implementation per specification. In three stages, RTLSeek uses rule-based diversity-oriented reinforcement learning with a reward schedule that combines expert knowledge and EDA feedback.
- **VeriGraphi** ([arXiv:2604.14550](https://arxiv.org/abs/2604.14550)). Large language models cannot reliably generate synthesizable Verilog for large hierarchical hardware designs. Agents iteratively analyze the specification to build a knowledge graph of module hierarchy, interfaces, and wiring, then generate RTL incrementally.
- **Dr. RTL** ([arXiv:2604.14989](https://arxiv.org/abs/2604.14989)). Existing LLM methods for RTL optimization use unrealistic test designs, weak tools, and simple pre-defined rewriting rules. The paper presents an agentic framework that optimizes RTL timing in an industrial EDA workflow and learns reusable skills.
- **Self-Evolved ABC** ([arXiv:2604.15082](https://arxiv.org/abs/2604.15082)). The paper addresses the problem of improving a logic synthesis tool without manual design of new heuristics. A team of large language model agents rewrites ABC code in a correctness and quality of results evaluation loop.
- **VerilogCL** ([arXiv:2604.18162](https://arxiv.org/abs/2604.18162)). Large language models make Verilog code with errors because good training data are not sufficient. VerilogCL uses contrastive learning on pairs of correct and wrong RTL and filters low-confidence candidates during generation.
- **ChipCraftBrain** ([arXiv:2604.19856](https://arxiv.org/abs/2604.19856)). Single-shot LLM generation reaches only 60 to 65 percent functional correctness, and earlier multi-agent methods stay untested on industrial benchmarks. The method combines symbolic-neural reasoning with adaptive orchestration of six agents to generate RTL code from natural language specifications.
- **LEGO** ([arXiv:2604.23355](https://arxiv.org/abs/2604.23355)). Current LLM-based EDA agents are isolated task-specific systems that cause repeated engineering effort and limited reuse of design strategies. LEGO separates the digital front-end flow into six steps and makes each agent capability a standardized composable circuit skill.
- **PipeRTL** ([arXiv:2605.01836](https://arxiv.org/abs/2605.01836)). Common flows insert registers early and adjust them late, so the compiler loses operator structure for global optimization. PipeRTL makes register relocation legality explicit in the IR, uses a learned timing predictor, and solves a min-cost flow problem.
- **ChipMATE** ([arXiv:2605.12857](https://arxiv.org/abs/2605.12857)). Current agentic systems for RTL code generation need a golden testbench and cannot train on internal RTL codebases. ChipMATE trains a Verilog agent and a Python reference-model agent in two stages to verify each other's outputs.
- **Trace2Skill** ([arXiv:2605.21810](https://arxiv.org/abs/2605.21810)). Complex Verilog design problems are difficult because hardware LLM agents must find relevant code and recover from hidden verifier failures. Trace2Skill mines rollout traces and evolves the agent's skill through an oracle, mutator, and selector loop with dense verifier feedback.
- **Verilog-Evolve** ([arXiv:2605.26498](https://arxiv.org/abs/2605.26498)). Most pipelines use isolated sampling and functional checking only, a method that is not sufficient for practical RTL design. Verilog-Evolve generates candidates, evaluates them with simulation, synthesis, and timing feedback, promotes the best, and evolves skills across tasks.
- **StepPRM-RTL** ([arXiv:2606.04246](https://arxiv.org/abs/2606.04246)). Automatic generation of RTL code is difficult because it needs many reasoning steps and strict correctness. The framework combines stepwise trajectory modeling, process-reward modeling, and retrieval-augmented fine-tuning and is more than 10% better than prior methods.
- **Alpha-RTL (TTT-RTL)** ([arXiv:2606.05253](https://arxiv.org/abs/2606.05253)). Existing LLM methods train a general RTL generator before deployment or search with a frozen policy. TTT-RTL adapts the policy to EDA feedback at test time and reduces the geometric mean PPA product by 65.1%.
- **ROSUM-MCTS** ([arXiv:2606.07925](https://arxiv.org/abs/2606.07925)). Large language models show promise in code summarization, but few studies examine how well they work for hardware description languages. The method uses Monte Carlo Tree Search-inspired exploration, hierarchical candidate expansion, and a composite reward function to refine HDL summaries.
- **RTL-Sequencer** ([arXiv:2607.15830](https://arxiv.org/abs/2607.15830)). Accurate timing prediction at the register-transfer level is a difficult problem in design automation. The proposed sequence-based method linearizes logic cones by breadth-first traversal, applies linear sequence models, and uses four customization techniques.

## See also

- [Wiki index](../index.md)
- [Previous: HLS (High-Level Synthesis)](02-hls.md)
- [Next: Verification & Debug](04-verification-and-debug.md)
