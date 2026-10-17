---
title: Analog
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, analog]
sources: []
---

# Analog

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 10 papers.

## What this covers

Automatic design of analog and mixed-signal circuits uses LLMs and generative models. This section covers topology synthesis, circuit sizing, schematic generation, and layout design. The designs are for operational amplifiers, baseband hardware, and general analog integrated circuits. Engineers traditionally made the design decisions in the early stage. Now automated methods can do this work.

## Themes

- **Topology synthesis and generation**: LaMAGIC, AnalogXpert, AnalogGenie, and LADAC use language models to generate circuit topologies from specifications.
- **Optimization and design space exploration**: ADO-LLM, LEDRO, and Artisan use Bayesian optimization, in-context learning, and domain-specific models. They refine designs. They explore the design space.
- **Code-centric layout and synthesis**: AnalogCoder, FLAG, and LayoutCopilot use code generation and multiagent collaboration. They do not require model training. The design process is interactive.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2023-12 | [LADAC](https://www.techrxiv.org/doi/full/10.36227/techrxiv.170473941.10097233) | Ladac: Large language model-driven auto-designer for analog circuits | n/a | n/a |
| 2024-04-09 | [ADO-LLM](https://dl.acm.org/doi/pdf/10.1145/3676536.3676816) | Ado-llm: Analog design bayesian optimization with in-context learning of large language models | n/a | n/a |
| 2024-05 | [AnalogCoder](https://ojs.aaai.org/index.php/AAAI/article/view/32016) | Analogcoder: Analog circuit design via training-free code generation | [AnalogCoder](https://github.com/anonyanalog/AnalogCoder) | n/a |
| 2024-05 | FLAG | Flag: Formula-llm-based auto-generator for baseband hardware | n/a | n/a |
| 2024-07 | [LaMAGIC](https://arxiv.org/pdf/2407.18269?) | Lamagic: Language-model-based topology generation for analog integrated circuits | n/a | n/a |
| 2024-11 | Artisan | Artisan: Automated operational amplifier design via domain-specific large language model | n/a | n/a |
| 2024-11-19 | [LEDRO](https://arxiv.org/pdf/2411.12930) | Ledro: Llm-enhanced design space reduction and optimization for analog circuits | n/a | n/a |
| 2024-12-17 | [AnalogXpert](https://arxiv.org/abs/2412.19824) | Analogxpert: Automating analog topology synthesis by incorporating circuit design expertise into large language models | n/a | n/a |
| 2025-01-14 | [LayoutCopilot](https://ieeexplore.ieee.org/document/10841395) | LayoutCopilot: An LLM-Powered Multiagent Collaborative Framework for Interactive Analog Layout Design. | n/a | n/a |
| 2025-02-28 | [AnalogGenie](https://arxiv.org/pdf/2503.00205) | Analoggenie: A generative engine for automatic discovery of analog circuit topologies | [AnalogGenie](https://github.com/xz-group/AnalogGenie) | n/a |

## Notable entries

- **AnalogGenie** (ICLR 2025): This paper presents a generative engine that discovers circuit topologies automatically. The authors released the code.
- **AnalogCoder** (AAAI 2025): This work generates circuits as code. The method does not require model training. It can be deployed without retraining.
- **LayoutCopilot** (TCAD 2025): This is a multiagent framework for layout design. Multiple agents collaborate. The framework extends automation from schematic generation to physical layout.
- **LaMAGIC** (July 2024): This work uses language models to generate circuit topologies.
- **Artisan** (DAC 2024): This work uses a domain-specific LLM to design operational amplifiers.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **LaMAGIC** ([arXiv:2407.18269](https://arxiv.org/abs/2407.18269)). Existing search-based methods need many simulation iterations to design custom analog circuit topologies. A language model with supervised finetuning generates an optimized circuit design from a custom specification in one pass.
- **LEDRO** ([arXiv:2411.12930](https://arxiv.org/abs/2411.12930)). Analog circuit design takes much time and needs expert knowledge, and current automation methods are sub-optimal and costly to generalize. LEDRO uses large language models with optimization to refine the design space and outperforms baselines by 13% to 48% FoM.
- **AnalogXpert** ([arXiv:2412.19824](https://arxiv.org/abs/2412.19824)). Existing LLM methods for analog topology synthesis do not meet practical needs because they use vague requirements and ideal models. AnalogXpert writes SPICE code, selects and connects subcircuit blocks, and iteratively corrects errors to reach 40% and 23% success rates.
- **AnalogGenie** ([arXiv:2503.00205](https://arxiv.org/abs/2503.00205)). The design of analog circuit topologies is difficult because no complete dataset and no good representation method exist. The paper presents an engine that generates these topologies with a complete dataset and a sequence-based graph representation.

## See also

- [Wiki index](../index.md)
- [Previous: Flow & Layout](08-flow-and-layout.md)
- [Next: Survey & Benchmark](01-survey-and-benchmark.md)
