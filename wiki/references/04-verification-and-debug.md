---
title: Verification & Debug
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, verification]
sources: []
---

# Verification & Debug

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 36 papers.

## What this covers

Large language models automate RTL verification and debugging. Work in this area covers assertion generation, test stimulus generation, HDL bug detection, repair, and formal verification workflows. This area contains the most AI4CHIPS papers.

## Themes

- **Assertion Generation**: LLMs translate natural language and design specifications into formal assertions. Examples are NL2SVA, ChIRAAG, AssertLLM, AssertionBench, CodeV-SVA, AgileAssert, and AssertSolver.
- **Test & Stimulus Generation**: LLMs generate automated testbenches and test stimuli. They improve coverage closure and functional verification. Examples are LLM4DV, VerilogReader, Latg, CorrectBench, STG, CHORUS, and GoGoTB.
- **Bug Detection & Repair**: LLMs locate and fix RTL bugs, including syntax errors and logic bugs. Examples are RTLFixer, MEIC, HDLDebugger, LiK, llmrag, VeriPilot, and ARSP.
- **Formal Verification & Specification**: LLMs apply formal methods and specification synthesis to formal verification tasks and autoformalization. Examples are FVEval, SpecLoop, CktFormalizer, and UVM^2.
- **Agentic Verification Frameworks**: Multi-agent systems coordinate verification loops with feedback. Examples are PRO-V, UVMarvel, VeriTrace, UVLLM, and GoGoTB.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2023-06-03 | [NL2SVA](https://openreview.net/pdf?id=FKH8qCuM44) | Towards improving verification productivity with circuitaware translation of natural language to systemverilog assertions | n/a | n/a |
| 2023-09-18 | [AutoSVA2](https://arxiv.org/pdf/2309.09437) | Using LLMs to facilitate formal verification of RTL | n/a | n/a |
| 2023-10-06 | [LLM4DV](https://arxiv.org/pdf/2310.04535) | Llm4dv: Using large language models for hardware test stimuli generation. | [ml4dv](https://github.com/ZixiBenZhang/ml4dv) | n/a |
| 2023-11-28 | [RTLFixer](https://arxiv.org/pdf/2311.16543)🔥 | Rtlfixer: Automatically fixing rtl syntax errors with large language models | [RTLFixer](https://github.com/NVlabs/RTLFixer) | n/a |
| 2024-01-31 | [ChIRAAG](https://arxiv.org/pdf/2402.00093) | Chiraag: Chatgpt informed rapid and automated assertion generation. | [ChIRAAG](https://github.com/karthikmaddala/ChIRAAG) | n/a |
| 2024-02-01 | [AssertLLM](https://arxiv.org/pdf/2402.00386) | AssertLLM: Generating and evaluating hardware verification assertions from design specifications via multi-LLMs. | [AssertLLM](https://github.com/hkust-zhiyao/AssertLLM) | n/a |
| 2024-03-18 | [HDLDebugger](https://dl.acm.org/doi/pdf/10.1145/3735638) | Hdldebugger: Streamlining hdl debugging with large language models | n/a | n/a |
| 2024-05-10 | [MEIC](https://arxiv.org/pdf/2405.06840) | Meic: Re-thinking rtl debug automation using llms | n/a | n/a |
| 2024-05-29 | n/a | Domain-adapted llms for vlsi design and verification: A case study on formal verification | n/a | n/a |
| 2024-05-31 | [VeriAssist](https://arxiv.org/pdf/2406.00115) | Towards llm-powered verilog rtl assistant: Self-verification and self-correction | n/a | n/a |
| 2024-06-03 | [VerilogReader](https://arxiv.org/pdf/2406.04373?) | Verilogreader: Llm-aided hardware test generation | n/a | n/a |
| 2024-06-10 | n/a | Llm-based processor verification: A case study for neuronnorphic processor. | n/a | n/a |
| 2024-06-24 | [Latg](https://arxiv.org/pdf/2406.17132) | Llm-aided testbench generation and bug detection for finite-state machines. | n/a | n/a |
| 2024-06-26 | [AssertionBench](https://arxiv.org/pdf/2406.18627) | Assertionbench: A benchmark to evaluate large-language models for assertion generation | n/a | n/a |
| 2024-8-15 | [Verilogcoder](https://arxiv.org/pdf/2408.08927) | Verilogcoder: Autonomous verilog coding agents with graph-based planning and abstract syntax tree (ast)-based waveform tracing tool | [VerilogCoder](https://github.com/NVlabs/VerilogCoder) | n/a |
| 2024-09-23 | [LiK](https://arxiv.org/abs/2409.15186) | Location is Key: Leveraging Large Language Model for Functional Bug Localization in Verilog | n/a | n/a |
| 2024-10-01 | [llmrag](https://agra.informatik.uni-bremen.de/doc/konf/LAD2024_KQ.pdf) | From bugs to fixes: Hdl bug identification and patching using llms and rag | n/a | n/a |
| 2024-10-15 | [FVEval](https://arxiv.org/pdf/2410.23299) | Fveval: Understanding language model capabilities in formal verification of digital hardware | [FVEval](https://github.com/NVlabs/FVEval) | n/a |
| 2024-11-13 | [CorrectBench](https://ieeexplore.ieee.org/document/10992873) | CorrectBench: Automatic Testbench Generation with Functional Self-Correction using LLMs for HDL Design | [CorrectBench](https://github.com/AutoBench/CorrectBench) | n/a |
| 2024-11-25 | [UVLLM](https://arxiv.org/pdf/2411.16238) | Uvllm: An automated universal rtl verification framework using llms. | n/a | n/a |
| 2025-03-06 | [AssertSolver](https://arxiv.org/abs/2503.04057) | Insights from Rights and Wrongs: A Large Language Model for Solving Assertion Failures in RTL Design | [AssertSolver](https://github.com/SEU-ACAL/reproduce-AssertSolver-DAC-25) | n/a |
| 2025-03-31 | SSF | Early Functional Safety and PPA Evaluation of Digital Designs | n/a | n/a |
| 2025-04-28 | [UVM^2](https://arxiv.org/abs/2504.19959) | From Concept to Practice: an Automated LLM-aided UVM Machine for RTL Verification | n/a | n/a |
| 2025-06-13 | [PRO-V](https://arxiv.org/pdf/2506.12200) | PRO-V: An Efficient Program Generation Multi-Agent System for Automatic RTL Verification | n/a | n/a |
| 2025-08-22 | [ARSP](https://arxiv.org/abs/2508.16517) | ARSP: Automated Repair of Verilog Designs via Semantic Partitioning | n/a | n/a |
| 2025-11-19 | [CD-DPO (TB or not TB)](https://arxiv.org/abs/2511.15767) | TB or Not TB: Coverage-Driven Direct Preference Optimization for Verilog Stimulus Generation | n/a | n/a |
| 2026-03-03 | [SpecLoop](https://arxiv.org/abs/2603.02895) | SpecLoop: An Agentic RTL-to-Specification Framework with Formal Verification Feedback Loop | n/a | n/a |
| 2026-03-15 | [CodeV-SVA](https://arxiv.org/abs/2603.14239) | QiMeng-CodeV-SVA: Training Specialized LLMs for Hardware Assertion Generation via RTL-Grounded Bidirectional Data Synthesis | [CodeV-SVA](https://github.com/wyt2000/CodeV-SVA) | n/a |
| 2026-04-10 | [AgileAssert](https://arxiv.org/abs/2604.08932) | From Indiscriminate to Targeted: Functionally Critical Signal-Driven Assertion Generation using LLMs for Efficient RTL Verification | n/a | n/a |
| 2026-05-06 | [UVMarvel](https://arxiv.org/abs/2605.04704) | UVMarvel: an Automated LLM-aided UVM Machine for Subsystem-level RTL Verification | n/a | n/a |
| 2026-05-08 | [CktFormalizer](https://arxiv.org/abs/2605.07782) | CktFormalizer: Autoformalization of Natural Language into Circuit Representations | n/a | n/a |
| 2026-06-11 | [STG](https://arxiv.org/abs/2606.12983) | Structured Testbench Generation for LLM-Driven HDL Design and Verification-Oriented Data Curation | n/a | n/a |
| 2026-06-22 | [VeriPilot](https://arxiv.org/abs/2606.23759) | VeriPilot: An LLM-Powered Verilog Debugging Framework | [VeriPilot](https://github.com/YihanWn/VeriPilot) | n/a |
| 2026-07-28 | [GoGoTB](https://arxiv.org/abs/2607.26181) | GoGoTB: Agentic RTL Verification with Specification-Grounded Coverage Closure | n/a | n/a |
| 2026-08-03 | [VeriTrace](https://arxiv.org/abs/2608.02878) | VeriTrace: Human-Like Temporal Exploration Completes Agentic Action Space | n/a | n/a |
| 2026-08-10 | [CHORUS](https://arxiv.org/abs/2608.10090) | CHORUS: Complementary Experts for High-Coverage Testbench Stimulus Generation | n/a | n/a |

## Notable entries

- **RTLFixer** (2023-11-28, DAC 2024): This work automated syntax error fixing with LLMs. It became the foundation for RTL repair methods.
- **CorrectBench** (2024-11-13, DATE 2025): This benchmark establishes evaluation standards for testbench generation. It includes functional self-correction feedback.
- **CodeV-SVA** (2026-03-15, DAC 2026): This work trains specialized LLMs through RTL-grounded bidirectional data synthesis. It represents assertion-generation methods.
- **GoGoTB** (2026-07-28, ICCAD 2026): This method provides agentic verification with specification-grounded coverage closure. It exemplifies closed-loop multi-agent verification systems.
- **VeriTrace** (2026-08-03, ICLAD 2026): This method explores temporal sequences in a human-like way. It extends agentic action spaces for verification-loop automation.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **AutoSVA2** ([arXiv:2309.09437](https://arxiv.org/abs/2309.09437)). Writing formal properties for hardware verification is slow and error-prone. The authors design an evaluation framework and use GPT4 prompts to generate SystemVerilog Assertions for open-source RTL.
- **LLM4DV** ([arXiv:2310.04535](https://arxiv.org/abs/2310.04535)). Test stimuli generation for hardware design verification needs much human engineering effort. The paper proposes an open-source framework that uses large language models to automate test stimuli generation.
- **RTLFixer🔥** ([arXiv:2311.16543](https://arxiv.org/abs/2311.16543)). About 55% of errors in Verilog code that large language models generate are syntax errors and cause compilation failures. RTLFixer uses retrieval-augmented generation and ReAct prompting to let large language models interactively debug the code with feedback.
- **ChIRAAG** ([arXiv:2402.00093](https://arxiv.org/abs/2402.00093)). Manual writing of SystemVerilog Assertions is slow and causes errors. The ChIRAAG framework uses GPT4 to generate assertions from natural language specifications and corrects errors with simulation log feedback.
- **AssertLLM** ([arXiv:2402.00386](https://arxiv.org/abs/2402.00386)). Verification engineers manually convert natural language specifications into assertions, and existing methods process only sentences that engineers extract. AssertLLM uses three customized LLMs to generate assertions from complete specifications, and 89% of them are syntactically and functionally accurate.
- **MEIC** ([arXiv:2405.06840](https://arxiv.org/abs/2405.06840)). Large language models do not debug RTL code well because training sets contain little RTL data. MEIC uses LLMs in a repeated process and fixes 93% of syntax errors and 78% of function errors.
- **VeriAssist** ([arXiv:2406.00115](https://arxiv.org/abs/2406.00115)). Manual writing of RTL code takes much time and causes errors. VeriAssist uses automatic prompts and an RTL simulator to help an LLM self-verify and self-correct generated Verilog code.
- **VerilogReader** ([arXiv:2406.04373](https://arxiv.org/abs/2406.04373)). Test generation in hardware design verification is critical and labor-intensive. The authors use a large language model in coverage directed test generation to produce stimuli that reach unexplored code branches.
- **Latg** ([arXiv:2406.17132](https://arxiv.org/abs/2406.17132)). The paper addresses the problem of testbench generation for functional tests of RTL designs. The method uses large language models and feedback from commercial EDA tools to improve test coverage and detect RTL bugs.
- **AssertionBench** ([arXiv:2406.18627](https://arxiv.org/abs/2406.18627)). Little quantitative evaluation exists for large language models that generate hardware assertions. The authors present a benchmark of 100 Verilog designs with verified assertions to compare LLMs.
- **Verilogcoder** ([arXiv:2408.08927](https://arxiv.org/abs/2408.08927)). Automating hardware design can prevent human errors as integrated circuits become more complex. VerilogCoder uses multiple AI agents with graph-based planning and AST-based waveform tracing to write and fix Verilog code.
- **LiK** ([arXiv:2409.15186](https://arxiv.org/abs/2409.15186)). Engineers need much time to find functional errors in Verilog code when they verify hardware designs. LiK uses a large language model to locate these errors and needs only the design specification and the bad code.
- **FVEval** ([arXiv:2410.23299](https://arxiv.org/abs/2410.23299)). Researchers lack a full evaluation of how well large language models do formal verification of hardware. The paper presents a benchmark with three sub-tasks that measure generation of SystemVerilog assertions and reasoning about design RTL.
- **UVLLM** ([arXiv:2411.16238](https://arxiv.org/abs/2411.16238)). Verification of hardware designs takes much time and work, and existing methods often make unrealistic assumptions. UVLLM combines LLMs with UVM to automate testing and repair of RTL code, with fix rates of 86.99% and 71.92%.
- **AssertSolver** ([arXiv:2503.04057](https://arxiv.org/abs/2503.04057)). Solving assertion failures in RTL designs depends on human expertise because no automatic tool exists. The open-source LLM AssertSolver uses synthetic data and error responses to fix failures and gets 88.54% pass@1.
- **UVM^2** ([arXiv:2504.19959](https://arxiv.org/abs/2504.19959)). Verification consumes nearly 70% of the total effort in integrated circuit development. UVM^2 is an automated framework that uses large language models to generate UVM testbenches and refine them with coverage feedback.
- **PRO-V** ([arXiv:2506.12200](https://arxiv.org/abs/2506.12200)). RTL verification consumes 60-70% of development time, and current methods use proprietary models with high cost and privacy risks. PRO-V-R1 is an open-source agentic framework that combines LLM reasoning with programmatic tools and trains with reinforcement learning.
- **ARSP** ([arXiv:2508.16517](https://arxiv.org/abs/2508.16517)). LLM debugging methods do not work well on large Verilog modules because many unrelated lines hide the few bug tokens. The system uses LLMs to split the module into semantic fragments, repair each fragment, and merge the edits.
- **CD-DPO (TB or not TB)** ([arXiv:2511.15767](https://arxiv.org/abs/2511.15767)). Generating effective test stimuli for hardware verification takes much time and effort. The method fine-tunes large language models with coverage-driven direct preference optimization to improve code coverage by up to 77.27 percent.
- **SpecLoop** ([arXiv:2603.02895](https://arxiv.org/abs/2603.02895)). RTL designs often lack current specifications, and large language models alone do not always capture design intent. SpecLoop generates candidate specifications, reconstructs RTL from them, and improves the specifications with counterexamples from formal equivalence checking.
- **CodeV-SVA** ([arXiv:2603.14239](https://arxiv.org/abs/2603.14239)). General-purpose LLMs do not perform well when they translate natural language properties to SystemVerilog Assertions because the data is limited. The paper uses large-scale open-source RTL code to guide LLMs to generate real-world SVAs and bidirectional translation to select data.
- **AgileAssert** ([arXiv:2604.08932](https://arxiv.org/abs/2604.08932)). Existing LLM-based assertion generation methods do not consider how critical each signal is, so verification cost is high. AgileAssert builds RTL semantic graphs, selects top-K critical signals, and slices the RTL to help LLMs make targeted assertions.
- **UVMarvel** ([arXiv:2605.04704](https://arxiv.org/abs/2605.04704)). Verification needs nearly 70% of total effort in integrated circuit development, and engineers write subsystem-level UVM testbenches by hand. UVMarvel uses large language models, an intermediate representation, and a bus protocol library to build UVM testbenches and refine stimuli.
- **CktFormalizer** ([arXiv:2605.07782](https://arxiv.org/abs/2605.07782)). Hardware infrastructure limits what LLM agents can express, compile, and refine in circuit design. The authors build a typed hardware language in Lean and an agent framework for generation, repair, optimization, and equivalence proofs.
- **STG** ([arXiv:2606.12983](https://arxiv.org/abs/2606.12983)). Existing prompt-based methods write testbenches as free code and give random outputs with high cost and low reproducibility. STG uses the structure of hardware designs to make deterministic testbenches and runs 720x faster than an LLM-based flow.
- **VeriPilot** ([arXiv:2606.23759](https://arxiv.org/abs/2606.23759)). Verilog debugging is slow, and LLM methods that use test outputs and compiler feedback have limited success with complex bugs. VeriPilot uses golden reference models, LLM analysis of variable semantics, and signal tracing with CDFGs to find and repair bugs.
- **GoGoTB** ([arXiv:2607.26181](https://arxiv.org/abs/2607.26181)). Existing LLM verification methods make each component with separate single-turn calls, so interface mismatches stay undetected. GoGoTB is an agentic framework that controls execution, shares knowledge, and links every coverage bin to a specification behavior.
- **VeriTrace** ([arXiv:2608.02878](https://arxiv.org/abs/2608.02878)). Existing multi-agent systems for Verilog RTL generation reach only about 95% accuracy because their debugging action space is incomplete. VeriTrace gives the Inspector agent independent control of signals, time windows, and iteration depth, and gets 100% Pass@1 on VerilogEval-V2.
- **CHORUS** ([arXiv:2608.10090](https://arxiv.org/abs/2608.10090)). Hardware verification needs testbench stimulus with high coverage, but a standard SFT-to-RL pipeline limits performance. CHORUS trains experts with staged SFT and dense-reward RL and combines them into one model with 88.0% Pass@1 on CVDP-ECov.

## See also

- [Wiki index](../index.md)
- [Previous: RTL (Register Transfer Level)](03-rtl.md)
- [Next: Security](05-security.md)
