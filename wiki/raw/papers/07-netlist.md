---
title: Netlist
created: 2026-10-17
updated: 2026-10-17
type: reference
tags: [reference, generated, netlist]
sources: []
---

# Netlist

> Section of the [AI4CHIPS paper index](https://github.com/Archerll/AI4CHIPSpaper). 21 papers.

## What this covers

Netlist representation learning encodes circuits as dense embeddings. Engineers work at the gate level and the netlist level. Netlists connect synthesis to physical layout. Good embeddings enable logic synthesis optimization. They enable timing prediction. They enable circuit reasoning without manual features.

## Themes

- **Graph Neural Network encoders**. [DeepGate](https://arxiv.org/pdf/2111.14616), [Fgnn](https://www.cse.cuhk.edu.hk/~byu/papers/C142-DAC2022-GCL.pdf), [DeepGate2](https://arxiv.org/pdf/2305.16373), [Deepgate4](https://arxiv.org/pdf/2502.01681?), [Less is more](https://arxiv.org/pdf/2403.01317). Graph Neural Networks aggregate gate information across circuits.
- **Sequential circuit learning**. [Deepseq](https://arxiv.org/pdf/2302.13608), [Deepseq2](https://dl.acm.org/doi/pdf/10.1145/3658617.3697594), [DeepSeq3](https://arxiv.org/abs/2608.28188). Sequence models encode circuits with temporal dependencies. Hierarchical representations encode circuits with state dependencies.
- **Pre-trained foundation models**. [Fgnn2](https://www.cse.cuhk.edu.hk/~byu/papers/J119-TCAD2025-FGNN2.pdf), [CircuitEncoder](https://zhiyaoxie.com/files/ASPDAC25_CircuitEncoder.pdf), [NetTAG](https://arxiv.org/pdf/2504.09260), [GenEDA](https://arxiv.org/pdf/2504.09485?). Experts pre-train these models on many circuits. Engineers apply them to many downstream tasks.
- **AIG and Boolean reasoning**. [Gamora](https://arxiv.org/pdf/2303.08256), [TAG](https://arxiv.org/abs/2209.03465), [Polargate](https://www.cse.cuhk.edu.hk/~byu/papers/C233-ICCAD2024-PolarGate.pdf), [MGVGA](https://arxiv.org/pdf/2502.12732). These models learn on and-inverter graphs. They learn functional logic properties.
- **Multimodal and cross-stage alignment**. [Deepcell](https://arxiv.org/pdf/2502.06816), [CircuitEncoder](https://zhiyaoxie.com/files/ASPDAC25_CircuitEncoder.pdf), [NetTAG](https://arxiv.org/pdf/2504.09260), [GenEDA](https://arxiv.org/pdf/2504.09485?). These models align RTL, netlists, and layouts.
- **Generative and autoregressive models**. [CircuitAR](https://arxiv.org/abs/2502.12751), [GenEDA](https://arxiv.org/pdf/2504.09485?). These autoregressive models generate circuits from abstract specifications.

## Papers

| Date | Name | Venue | Title | Code |
|---|---|---|---|---|
| 2021-11-26 | [DeepGate](https://arxiv.org/pdf/2111.14616) | DeepGate: Learning neural representations of logic gates | n/a | n/a |
| 2022-8-23 | [Fgnn](https://www.cse.cuhk.edu.hk/~byu/papers/C142-DAC2022-GCL.pdf) | Functionality matters in netlist representation learning | n/a | n/a |
| 2022-09-07 | [TAG](https://arxiv.org/abs/2209.03465) | TAG: Learning Circuit Spatial Embedding From Layouts | n/a | n/a |
| 2022-11-07 | [WhyGNN](https://dl.acm.org/doi/10.1145/3508352.3561093) | Why are Graph Neural Networks Effective for EDA Problems?: (Invited Paper) | n/a | n/a |
| 2023-02-27 | [Deepseq](https://arxiv.org/pdf/2302.13608) | Deepseq: Deep sequential circuit learning. In Design, Automation and Test in Europe Conference and Exhibition | n/a | n/a |
| 2023-03-14 | [Gamora](https://arxiv.org/pdf/2303.08256) | Gamora: Graph learning based symbolic reasoning for large-scale boolean networks | n/a | n/a |
| 2023-05-25 | [DeepGate2](https://arxiv.org/pdf/2305.16373) | DeepGate2: Functionality-aware circuit representation learning | n/a | n/a |
| 2024-03-02 | [Less is more](https://arxiv.org/pdf/2403.01317) | Less is more: Hop-wise graph attention for scalable and generalizable learning on circuits | n/a | n/a |
| 2024-11-01 | [Deepseq2](https://dl.acm.org/doi/pdf/10.1145/3658617.3697594) | Deepseq2: Enhanced sequential circuit learning with disentangled representations | n/a | n/a |
| 2025-01-01 | [Fgnn2](https://www.cse.cuhk.edu.hk/~byu/papers/J119-TCAD2025-FGNN2.pdf) | Fgnn2: A powerful pre-training framework for learning the logic functionality of circuits | n/a | n/a |
| 2025-01-23 | [Deepgate4](https://arxiv.org/pdf/2502.01681?) | Deepgate4: Efficient and effective representation learning for circuit design at scale | n/a | n/a |
| 2025-2-5 | [Deepcell](https://arxiv.org/pdf/2502.06816) | Deepcell: Multiview representation learning for post-mapping netlists | n/a | n/a |
| 2025-2-18 | [MGVGA](https://arxiv.org/pdf/2502.12732) | Circuit representation learning with masked gatemodeling and verilog-aigalignment | n/a | n/a |
| 2025-02-18 | [CircuitAR](https://arxiv.org/abs/2502.12751) | Architect of the Bits World: Masked Autoregressive Modeling for Circuit Generation Guided by Truth Table | n/a | n/a |
| 2025-3-4 | [CircuitEncoder](https://zhiyaoxie.com/files/ASPDAC25_CircuitEncoder.pdf) | A self-supervised, pre-trained, and cross-stage-aligned circuit encoder provides a foundation for various design tasks | n/a | n/a |
| 2025-04-09 | [Polargate](https://www.cse.cuhk.edu.hk/~byu/papers/C233-ICCAD2024-PolarGate.pdf) | Polargate: Breaking the functionality representation bottleneck of and-inverter graph neural network | n/a | n/a |
| 2025-04-12 | [NetTAG](https://arxiv.org/pdf/2504.09260) | Nettag: A multimodal rtl-and-layoutaligned netlist foundation model via text-attributed graph | n/a | n/a |
| 2025-04-13 | [GenEDA](https://arxiv.org/pdf/2504.09485?) | GenEDA: Unleashing Generative Reasoning on Netlist via Multimodal Encoder-Decoder Aligned Foundation Model | n/a | n/a |
| 2025-11-12 | [DR-GNN](https://arxiv.org/abs/2511.09593) | DynamicRTL: RTL Representation Learning for Dynamic Circuit Behavior | [DR-GNN](https://github.com/magicyang1573/DynamicRTL) | n/a |
| 2026-03-10 | [WrongCode](https://arxiv.org/abs/2603.09161) | Wrong Code, Right Structure: Learning Netlist Representations from Imperfect LLM-Generated RTL | n/a | n/a |
| 2026-08-28 | [DeepSeq3](https://arxiv.org/abs/2608.28188) | Beyond Flat Netlist: Hierarchical Graph Representation Learning for Scalable Analysis of Sequential Circuits | [DeepSeq3](https://github.com/cure-lab/DeepSeq3) | n/a |

## Notable entries

- **[DeepGate](https://arxiv.org/pdf/2111.14616) and [DeepGate2](https://arxiv.org/pdf/2305.16373)**. DeepGate and DeepGate2 work on gate-level representations using Graph Neural Networks. DeepGate2 added functionality awareness. Later works extend DeepGate2.
- **[Fgnn2](https://www.cse.cuhk.edu.hk/~byu/papers/J119-TCAD2025-FGNN2.pdf)**. Fgnn2 is a large-scale pre-trained foundation model for netlists. Engineers apply it to many EDA tasks.
- **[NetTAG](https://arxiv.org/pdf/2504.09260) and [CircuitEncoder](https://zhiyaoxie.com/files/ASPDAC25_CircuitEncoder.pdf)**. NetTAG and CircuitEncoder are foundation models for multiple design stages. They align RTL, netlists, and layouts. Engineers reason across these stages.
- **[DeepSeq3](https://arxiv.org/abs/2608.28188)**. DeepSeq3 is a hierarchical approach for sequential circuits. It handles circuits at scale. It works on actual post-mapping scenarios.
- **[GenEDA](https://arxiv.org/pdf/2504.09485?)**. GenEDA generates circuits from abstract specifications. Foundation model reasoning guides this synthesis.

## Paper summaries

Each summary below comes from the abstract of the paper on arXiv. Papers that are not on arXiv have no summary here.

- **DeepGate** ([arXiv:2111.14616](https://arxiv.org/abs/2111.14616)). The paper studies how to obtain a general and effective neural representation of circuits. DeepGate embeds logic function and structure of a circuit as vectors on each gate and uses signal probabilities for supervision.
- **TAG** ([arXiv:2209.03465](https://arxiv.org/abs/2209.03465)). Analog and mixed-signal circuit designs still rely on human design expertise. TAG learns circuit representation from layouts with text, self-attention and graph, and learns spatial information without manual labels.
- **Deepseq** ([arXiv:2302.13608](https://arxiv.org/abs/2302.13608)). Existing representation learning methods only target combinational circuits. The paper proposes a graph neural network with a customized propagation scheme and a multi-task training objective for sequential netlists.
- **Gamora** ([arXiv:2303.08256](https://arxiv.org/abs/2303.08256)). Conventional symbolic reasoning methods for gate-level netlists do not scale well and use modern computing power inefficiently. Gamora uses graph neural networks and GPU acceleration to identify high-level functional blocks in netlists with over 33 million nodes.
- **DeepGate2** ([arXiv:2305.16373](https://arxiv.org/abs/2305.16373)). Existing methods that learn circuit representations show poor performance in downstream tasks because of weak supervision or design errors. DeepGate2 uses pairwise truth table differences as supervision, a loss that considers circuit functionality, and a one-round graph neural network.
- **Less is more** ([arXiv:2403.01317](https://arxiv.org/abs/2403.01317)). Graph neural networks for circuit learning show limited scalability on large graphs and limited generalizability to new designs. HOGA computes hop-wise features per node and uses gated self-attention to learn node representations without graph topology.
- **Deepgate4** ([arXiv:2502.01681](https://arxiv.org/abs/2502.01681)). Graph neural networks over-squash information and transformer models have quadratic complexity, so existing models can not process large circuits. DeepGate4 uses a sub-linear memory update strategy, a GAT-based sparse transformer with structural encodings, and a CUDA kernel.
- **Deepcell** ([arXiv:2502.06816](https://arxiv.org/abs/2502.06816)). This paper addresses representation learning for Post-Mapping netlists. DeepCell uses self-supervised Mask Circuit Modeling to fuse multiview information from And-Inverter Graphs and Post-Mapping netlists into unified embeddings.
- **MGVGA** ([arXiv:2502.12732](https://arxiv.org/abs/2502.12732)). Masking parts of circuits destroys logical equivalence, and existing methods often give priority to structure over circuit function. MGVGA masks gates in the latent space and aligns graphs with Verilog code to learn circuit function.
- **CircuitAR** ([arXiv:2502.12751](https://arxiv.org/abs/2502.12751)). Traditional logic synthesis tools use human-designed heuristics and often give results that are not optimum. A masked autoregressive model with a circuit tokenizer generates initial circuits from truth tables to guide differentiable architecture search.
- **NetTAG** ([arXiv:2504.09260](https://arxiv.org/abs/2504.09260)). Existing pre-trained models learn only simple and-inverter graphs and cannot fully encode complex gate functions. NetTAG formulates netlists as text-attributed graphs and combines an LLM text encoder with a graph transformer.
- **GenEDA** ([arXiv:2504.09485](https://arxiv.org/abs/2504.09485)). Existing circuit foundation models use standalone encoders or decoders that operate separately and cannot complement each other. GenEDA aligns graph-based netlist encoders with large language models in a shared latent space to generate specifications and RTL code.
- **DR-GNN** ([arXiv:2511.09593](https://arxiv.org/abs/2511.09593)). Existing GNN models learn static circuit properties but do not capture circuit runtime behavior. DR-GNN uses an operator-level CDFG to learn RTL representations that include static structures and multi-cycle execution behaviors.
- **WrongCode** ([arXiv:2603.09161](https://arxiv.org/abs/2603.09161)). Labeled netlist data is scarce because companies protect real circuit designs as intellectual property. The paper uses imperfect LLM-generated RTL as training data because the synthesized netlists keep structural patterns of the intended functionality.
- **DeepSeq3** ([arXiv:2608.28188](https://arxiv.org/abs/2608.28188)). Industrial netlists are large, and current methods do not model register-level temporal behavior. DeepSeq3 uses graph neural networks on flip-flop subgraphs and a Super-Node Graph, and reduces bounded model checking time by 18%.

## See also

- [Wiki index](../../index.md)
- [Previous: Architecture](06-architecture.md)
- [Next: Flow & Layout](08-flow-and-layout.md)
