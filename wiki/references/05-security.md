---
title: Security
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, security]
sources: []
---

# Security

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 12 papers.

## What this covers

This section covers the use of AI and large language models (LLMs) in hardware security. Engineers use LLMs to detect and repair flaws in RTL and HDL code. This work includes automated security analysis for SoCs, side-channel analysis, and detection of trojans and backdoors. It also includes IP protection for LLM-generated designs. When engineers use LLMs to generate code, new attack surfaces and bugs appear. These bugs may not be caught by traditional verification.

## Themes

- **LLM-based vulnerability repair and detection**: EZSVR, SAbyLLM, Self-HWDebug, llmrag, and RTL-Breaker use LLMs to find and patch security flaws in hardware code. These papers also address threats such as backdoors that LLMs generate during code generation.
- **Hardware security analysis and SoC protection**: DIVAS and NSPG provide frameworks to analyze security and assure SoC designs.
- **Side-channel and power analysis**: SCAR and Netlist Whisperer analyze side-channel leakage in RTL designs. This includes power leakage and electromagnetic leakage.
- **Security databases and knowledge bases**: SecRT-LLM provides a database of vulnerable hardware examples. Engineers use this database to train and evaluate LLMs.
- **IP protection for generated designs**: RTLMarker introduces hardware watermarks to protect copyrights of LLM-generated RTL code.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2021-12-03 | [EZSVR](https://arxiv.org/pdf/2112.02125)🔥 | Examining zero-shot vulnerability repair with large language models | n/a | n/a |
| 2023-02 | n/a | On hardware security bug code fixes by prompting large language models | n/a | n/a |
| 2023-06-24 | [SAbyLLM](https://arxiv.org/pdf/2306.14027) | (security) assertions by large language models | n/a | n/a |
| 2023-08-14 | [DIVAS](https://arxiv.org/pdf/2308.06932) | Divas: An llm-based end-to-end framework for soc security analysis and policy-based protection | n/a | n/a |
| 2023-08-21 | [NSPG](https://arxiv.org/pdf/2308.11042) | Unlocking hardware security assurance: The potential of llms | n/a | n/a |
| 2023-10-10 | [SCAR](https://arxiv.org/pdf/2310.06257) | Scar: Power side-channel analysis at rtl level | n/a | n/a |
| 2023-11-26 | Netlist Whisperer | Netlist whisperer: Ai and nlp fight circuit leakage! | n/a | n/a |
| 2024-05 | [SecRT-LLM](https://www.researchgate.net/profile/Dipayan-Saha/publication/381234667_Empowering_Hardware_Security_with_LLM_The_Development_of_a_Vulnerable_Hardware_Database/links/675936c2138b414414d56fcb/Empowering-Hardware-Security-with-LLM-The-Development-of-a-Vulnerable-Hardware-Database.pdf) | Empowering hardware security with llm: The development of a vulnerable hardware database | n/a | n/a |
| 2024-05 | [Self-HWDebug](https://arxiv.org/pdf/2405.12347) | Self-hwdebug: Automation of llm self-instructing for hardware security verification | n/a | n/a |
| 2024-10-01 | [llmrag](https://agra.informatik.uni-bremen.de/doc/konf/LAD2024_KQ.pdf) | From bugs to fixes: Hdl bug identification and patching using llms and rag | n/a | n/a |
| 2024-11-26 | [RTL-Breaker](https://ieeexplore.ieee.org/document/10993260) | RTL-Breaker: Assessing the Security of LLMs Against Backdoor Attacks on HDL Code Generation | n/a | n/a |
| 2025-01-05 | [RTLMarker](https://arxiv.org/abs/2501.02446) | RTLMarker: Protecting LLM-Generated RTL Copyright via a Hardware Watermarking Framework | n/a | n/a |

## Notable entries

- **EZSVR** (2021): This paper presents zero-shot vulnerability repair with LLMs. It shows that LLMs can fix bugs in hardware code without task-specific training.
- **DIVAS** (2023): This paper presents an end-to-end framework for SoC security analysis with policy-based protection mechanisms. It integrates LLMs into security verification.
- **RTL-Breaker** (2024): This paper investigates how LLMs introduce backdoors during RTL generation. It presents a threat model for this scenario.
- **RTLMarker** (2025): This paper introduces hardware watermarking to protect copyrights of LLM-generated designs. It addresses IP protection concerns for agentic chip design.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **EZSVR🔥** ([arXiv:2112.02125](https://arxiv.org/abs/2112.02125)). The paper studies how to write prompts that help large language models repair insecure code. The authors test five commercial models, one open-source model, and one locally-trained model on synthetic and real-world bug scenarios.
- **SAbyLLM** ([arXiv:2306.14027](https://arxiv.org/abs/2306.14027)). Writing security assertions for hardware verification is difficult. The authors make a benchmark suite and use a large language model to write SystemVerilog assertions from natural language prompts.
- **DIVAS** ([arXiv:2308.06932](https://arxiv.org/abs/2308.06932)). Designers find it difficult to secure a SoC because the design is complex and the assets are in many IPs. DIVAS uses LLMs to find vulnerabilities in user-defined SoC specifications, map them to CWEs, generate assertions, and enforce security policies.
- **NSPG** ([arXiv:2308.11042](https://arxiv.org/abs/2308.11042)). Traditional methods to generate SoC security properties need experts, cover few IP cores, and are slow. NSPG uses the NLP model HS-BERT to extract 326 security properties from OpenTitan documents and helps to find eight bugs.
- **SCAR** ([arXiv:2310.06257](https://arxiv.org/abs/2310.06257)). Current power side-channel analysis runs after chip manufacture, so late design changes cost a lot of time and money. SCAR converts RTL designs of encryption hardware into control-data flow graphs and uses graph neural networks to find leakage-prone modules.
- **Self-HWDebug** ([arXiv:2405.12347](https://arxiv.org/abs/2405.12347)). Writing precise instructions to find and fix security vulnerabilities in hardware designs needs much time and expert knowledge. The framework gives known bugs and fixes to LLMs, which then make instructions to fix similar vulnerabilities in other designs.
- **RTLMarker** ([arXiv:2501.02446](https://arxiv.org/abs/2501.02446)). Existing watermarking methods do not protect RTL code copyright because RTL code differs from software code. The paper proposes a framework that embeds watermarks into RTL code and the synthesized netlist with rule-based Verilog transformations.

## See also

- [Wiki index](../index.md)
- [Previous: Verification & Debug](04-verification-and-debug.md)
- [Next: Architecture](06-architecture.md)
