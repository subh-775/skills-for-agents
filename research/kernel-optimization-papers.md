# AI/Agent-Based GPU Kernel Optimization: Academic Paper Survey

## Generated: 2026-05-28

---

## 1. CODA: Rewriting Transformer Blocks as GEMM-Epilogue Programs (arXiv: 2605.19269)

**Authors:** Han Guo, Jack Zhang, Arjun Menon, Driss Guessous, Vijay Thakkar, Yoon Kim, Tri Dao
**Published:** 2026-05-19
**Categories:** cs.LG

**Abstract:** Transformer training systems are built around dense linear algebra, yet a nontrivial fraction of end-to-end time is spent on surrounding memory-bound operators. Normalization, activations, residual updates, reductions, and related computations repeatedly move large intermediate tensors through global memory while performing little arithmetic. CODA is a GPU kernel abstraction that expresses these computations as GEMM-plus-epilogue programs, based on the observation that many Transformer operators can be algebraically reparameterized to execute while a GEMM output tile remains on chip. Both human- and LLM-authored CODA kernels achieve high performance.

**Key Insight for Tritonify:** CODA's GEMM-epilogue abstraction is a practical interface for LLMs to write high-performance kernels. The constrained interface preserves performance structure while being expressive enough for nearly all non-attention Transformer computation.

**Method Details:**
- Fixes GEMM mainloop, exposes composable epilogue primitives
- 5 epilogue primitive classes:
  1. Elementwise/pairwise maps (residual updates, activations, RoPE, SwiGLU)
  2. Vector (rank-1) loads/stores (row/col vectors, broadcast)
  3. Tile (rank-2) loads/stores (residual streams, saved activations)
  4. Tile reductions (partial row/col reductions)
  5. Stateful transforms (running max/sum-exp for online log-sum-exp, cross-entropy)
- LLM-authored kernels: Claude Code generates from written spec + curated examples + implementation tips
- Covers nearly all non-attention computation in Transformer forward+backward pass
- Compares against cuBLAS + torch.compile, Liger Kernel, FlashInfer

**GitHub:** https://github.com/HanGuo97/coda-kernels

---

## 2. KernelBench: Can LLMs Write Efficient GPU Kernels? (arXiv: 2502.10517)

**Authors:** Anne Ouyang, Simon Guo, Simran Arora, Alex L. Zhang, William Hu, Christopher Ré, Azalia Mirhoseini
**Published:** 2025-02-14
**Categories:** cs.LG, cs.AI, cs.PF, cs.SE

**Abstract:** Introduces KernelBench, an open-source framework for evaluating LMs' ability to write fast and correct kernels on 250 PyTorch ML workloads. Introduces the fast_p metric. Frontier reasoning models match PyTorch baseline in less than 20% of cases. Iterative refinement with execution/profiling feedback helps but KernelBench remains very challenging.

**Key Findings:**
- THE foundational benchmark for this field
- 250 carefully selected PyTorch workloads
- fast_p metric: % of kernels correct AND >p speedup over baseline
- Level 1 (simple), Level 2 (moderate), Level 3 (hard) difficulty tiers

**GitHub:** https://github.com/ScalingIntelligence/KernelBench (implied)

---

## 3. TritonForge: Profiling-Guided Framework for Automated Triton Kernel Optimization (arXiv: 2512.09196)

**Authors:** Haonan Li, Keyu Man, Partha Kanuparthy, et al.
**Published:** 2025-12-09
**Categories:** cs.SE

**Abstract:** TritonForge integrates kernel analysis, runtime profiling, and iterative code transformation. By incorporating profiling feedback, it identifies bottlenecks, proposes targeted modifications, and evaluates impact automatically. Achieves up to 5x performance improvement over baseline, average 1.76x success rate.

**Key Findings:**
- Profiling-guided iterative optimization
- Automated bottleneck identification
- Up to 5x speedup over baselines

---

## 4. Dr. Kernel: Reinforcement Learning Done Right for Triton Kernel Generations (arXiv: 2602.05885)

**Authors:** Wei Liu, Jiawei Xu, Yingru Li, et al.
**Published:** 2026-02-05
**Categories:** cs.LG, cs.AI, cs.CL

**Abstract:** Systematically studies RL for kernel generation. Designs KernelGYM, a robust distributed GPU environment. Proposes Turn-level Reinforce-Leave-One-Out (TRLOO) for unbiased advantage estimation. Dr Kernel-14B reaches performance competitive with Claude-4.5-Sonnet. On KernelBench Level-2, 31.6% of kernels achieve >=1.2x speedup (surpassing Claude-4.5-Sonnet at 26.7% and GPT-5 at 28.6%).

**Key Findings:**
- Identifies biased policy gradient issue in GRPO from self-inclusion
- Profiling-based Rewards (PR) and Profiling-based Rejection Sampling (PRS)
- TRLOO for multi-turn RL
- Best-of-N across turns: 47.8% achieve 1.2x speedup

**GitHub:** https://github.com/hkust-nlp/KernelGYM

---

## 5. DRTriton: Large-Scale Synthetic Data Driven RL for Triton Kernel Generation (arXiv: 2603.21465)

**Authors:** Siqi Guo, Ming Lin, Tianbao Yang
**Published:** 2026-03-23
**Categories:** cs.CL, cs.LG

**Abstract:** Proposes DRTriton with CSP-DAG for synthetic data generation, curriculum RL with decoupled rewards, and test-time search. DRTriton-7B achieves speedup on 92% of KernelBench Level 2 tasks (vs 23% for GPT-5.2, 19% for Claude-Sonnet-4.5).

**Key Findings:**
- CSP-DAG: guarantees full coverage and unbiased uniform sampling over operator space
- Curriculum RL with decoupled rewards (success rate + execution speed)
- Test-time search for further speedup improvement
- 7B model outperforms frontier models by huge margin

---

## 6. TritonRL: Training LLMs to Think and Code Triton Without Cheating (arXiv: 2510.17891)

**Authors:** Jiin Woo, Shaowei Zhu, Allen Nie, et al.
**Published:** 2025-10-18
**Categories:** cs.SE, cs.LG

**Abstract:** 8B-scale LLM for Triton programming via novel RL framework. Multi-layered verification for high-fidelity rewards. Hierarchical Reward Decomposition (HRD) decouples reinforcement for reasoning vs implementation. State-of-the-art on KernelBench, matching >100B parameter models.

**Key Findings:**
- Hierarchical Reward Decomposition (HRD) for credit assignment
- Multi-layered verification (syntax + function + performance)
- Addresses reward hacking in RL for kernel generation

---

## 7. AutoTriton: Automatic Triton Programming with RL in LLMs (arXiv: 2507.05687)

**Authors:** Shangzhan Li, Zefan Wang, et al.
**Published:** 2025-07-08
**Categories:** cs.LG, cs.CL

**Abstract:** First dedicated model for Triton programming powered by RL. Uses SFT + GRPO with rule-based and execution-based rewards. 8B model comparable to Claude-4-Sonnet and DeepSeek-R1-0528.

**Key Findings:**
- SFT stage + RL stage pipeline
- Rule-based + execution-based reward combination
- Evaluates on TritonBench and KernelBench

**GitHub:** https://github.com/AI9Stars/AutoTriton

---

## 8. CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation (arXiv: 2602.24286)

**Authors:** Weinan Dai, Hanlin Wu, et al.
**Published:** 2026-02-27
**Categories:** cs.LG, cs.AI

**Abstract:** Large-scale agentic RL system with scalable data synthesis, skill-augmented CUDA dev environment, and RL algorithmic techniques. Achieves 100%, 100%, 92% faster rate over torch.compile on KernelBench Level-1/2/3. Outperforms Claude Opus 4.5 and Gemini 3 Pro by ~40% on Level-3.

**Key Findings:**
- Scalable data synthesis pipeline
- Skill-augmented environment with automated verification and profiling
- SOTA on KernelBench across all levels
- Surpasses strongest proprietary models

---

## 9. DICE: Diffusion LLMs Excel at Generating CUDA Kernels (arXiv: 2602.11715)

**Authors:** Haolei Bai, Lingcheng Kong, et al.
**Published:** 2026-02-12
**Categories:** cs.LG, cs.CL

**Abstract:** Applies diffusion LLMs (dLLMs) to CUDA kernel generation. Constructs CuKe dataset. Proposes bi-phase curated RL (BiC-RL) with infilling + end-to-end generation stages. DICE 1.7B/4B/8B significantly outperform comparable autoregressive and diffusion LLMs on KernelBench.

**Key Findings:**
- Novel diffusion LLM approach (non-autoregressive)
- BiC-RL: two-phase training (infilling then full generation)
- CuKe dataset for high-performance CUDA kernels
- SOTA for comparable-scale models

---

## 10. Kevin: Multi-Turn RL for Generating CUDA Kernels (arXiv: 2507.11948)

**Authors:** Carlo Baronio, Pietro Marsella, Ben Pan, et al.
**Published:** 2025-07-16
**Categories:** cs.LG, cs.AI, cs.PF, cs.SE

**Abstract:** First model trained with multi-turn RL for CUDA kernel generation. Flexible multi-turn RL recipe addressing learning from long trajectories and reward attribution. Improves correctness from 56% to 82% and mean speedup from 0.53x to 1.10x over PyTorch Eager.

**Key Findings:**
- Multi-turn RL formulation (iterative refinement)
- Serial refinement scaling > parallel sampling
- QwQ-32B base model, surpasses o4-mini

---

## 11. EvoEngineer: Mastering Automated CUDA Kernel Code Evolution with LLMs (arXiv: 2510.03760)

**Authors:** Ping Guo, Chenyu Zhu, et al.
**Published:** 2025-10-04
**Categories:** cs.LG, cs.AI

**Abstract:** Formalizes CUDA kernel optimization as code optimization task. Systematic LLM-based code evolution framework. On 91 real-world CUDA kernels: 2.72x median speedup, 69.8% validity rate. Max speedup of 36.75x.

**Key Findings:**
- Formal problem formulation (objective, constraints, metrics)
- Balance between performance and correctness
- 91 real-world CUDA kernel benchmark

---

## 12. CudaForge: Agent Framework with Hardware Feedback for CUDA Kernel Optimization (arXiv: 2511.01884)

**Authors:** Zijian Zhang, Rong Wang, et al.
**Published:** 2025-10-23
**Categories:** cs.LG, cs.AI, cs.CL, cs.DC

**Abstract:** Training-free multi-agent workflow with Coder and Judge agents. Integrates Nsight Compute (NCU) metrics. 97.6% correctness, 1.68x average speedup over PyTorch. ~26.5 min per kernel, ~$0.30 API cost.

**Key Findings:**
- Multi-agent: Coder + Judge pattern
- Nsight Compute hardware feedback integration
- Training-free (uses base models like OpenAI-o3)
- Very cost-effective ($0.30 per kernel)
- Generalizes across GPUs (A100, RTX 6000, 4090, 3090)

**GitHub:** https://github.com/OptimAI-Lab/CudaForge

---

## 13. CUDA-LLM: LLMs Can Write Efficient CUDA Kernels (arXiv: 2506.09092)

**Authors:** Wentao Chen, Jiace Zhu, et al.
**Published:** 2025-06-10
**Categories:** cs.LG, cs.AI

**Abstract:** Proposes Feature Search and Reinforcement (FSR) framework. Jointly optimizes compilation/functional correctness and runtime performance. Generated kernels outperform human-written code by up to 179x.

**Key Findings:**
- FSR: Feature Search and Reinforcement
- Joint correctness + performance optimization
- Up to 179x speedup over human code

---

## 14. OptiML: End-to-End Framework for Program Synthesis and CUDA Kernel Optimization (arXiv: 2602.12305)

**Authors:** Arijit Bhattacharjee, Heng Ping, et al.
**Published:** 2026-02-12
**Categories:** cs.LG, cs.AI, cs.DC, cs.MA, cs.SE

**Abstract:** Maps natural language or CUDA code to optimized kernels. Mixture-of-Thoughts generator (OptiML-G) + MCTS-based optimizer (OptiML-X). Nsight Compute profiling, composite objective combining runtime with hardware bottleneck proxies.

**Key Findings:**
- NL-to-CUDA or CUDA-to-optimized-CUDA pipeline
- MCTS over LLM-driven edits
- Hardware-aware reward from profiler feedback
- Composite objective (runtime + bottleneck proxies + regression guards)

**GitHub:** https://github.com/rlx-lab/POLCA (related)

---

## 15. Towards Robust Agentic CUDA Kernel Benchmarking, Verification, and Optimization (arXiv: 2509.14279)

**Authors:** Robert Tjarko Lange, Qi Sun, et al.
**Published:** 2025-09-16
**Categories:** cs.SE, cs.AI, cs.LG

**Abstract:** Introduces robust-kbench and agentic framework for CUDA kernel discovery, verification, optimization. Evolutionary meta-generation procedure with LLM-based verifiers.

**Key Findings:**
- robust-kbench: more rigorous benchmark than KernelBench
- Evolutionary meta-generation
- LLM-based verifiers for correctness filtering
- Operation fusion and runtime optimization strategies

---

## 16. cuPilot: Strategy-Coordinated Multi-agent Framework for CUDA Kernel Evolution (arXiv: 2512.16465)

**Authors:** Jinwu Chen, Qidie Wu, et al.
**Published:** 2025-12-18
**Categories:** cs.AI

**Abstract:** Strategy-coordinated multi-agent framework with strategy as intermediate semantic representation. Roofline-guided prompting. 3.09x average speedup over PyTorch on 100 kernels.

**Key Findings:**
- Strategy-level abstraction for kernel evolution
- Roofline-guided prompting (hardware-aware)
- Strategy-level population initialization
- High hardware utilization on GEMM tasks

**GitHub:** https://github.com/champloo2878/cuPilot-Kernels

---

## 17. KernelSkill: Multi-Agent Framework for GPU Kernel Optimization (arXiv: 2603.10085)

**Authors:** Qitong Sun, Jun Han, et al.
**Published:** 2026-03-10
**Categories:** cs.LG, cs.AI, cs.MA

**Abstract:** Dual-level memory architecture: long-term memory of reusable expert skills + short-term memory to prevent backtracking. 100% success rate on KernelBench L1-3. Speedups: 5.44x (L1), 2.82x (L2), 1.92x (L3).

**Key Findings:**
- Expert skill memory (knowledge-driven, not implicit heuristics)
- Dual-level memory: long-term (skills) + short-term (anti-backtracking)
- 100% success rate on all KernelBench levels
- Best reported results

**GitHub:** https://github.com/0satan0/KernelMem/

---

## 18. Astra: Multi-Agent System for GPU Kernel Performance Optimization (arXiv: 2509.07506)

**Authors:** Anjiang Wei, Tianran Sun, et al.
**Published:** 2025-09-09
**Categories:** cs.DC, cs.AI, cs.CL, cs.LG, cs.SE

**Abstract:** First LLM-based multi-agent system for GPU kernel optimization starting from existing CUDA implementations (SGLang). Specialized agents collaborate through iterative code generation, testing, profiling, planning. 1.32x average speedup with zero-shot OpenAI o4-mini.

**Key Findings:**
- Starts from existing CUDA code (not PyTorch)
- Targets real SGLang production kernels
- LLMs can autonomously apply loop transforms, memory optimizations, CUDA intrinsics
- Multi-agent collaboration pattern

**GitHub:** https://github.com/Anjiang-Wei/Astra

---

## 19. AutoKernel: Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search (arXiv: 2603.21331)

**Authors:** Jaber Jaber, Osama Jaber
**Published:** 2026-03-22
**Categories:** cs.LG, cs.PF

**Abstract:** Profiles model to identify bottlenecks, ranks by Amdahl's law impact, iteratively refines Triton or CUDA C++ kernels. Five-stage correctness harness. 9000+ lines Python, 18 starter kernels, six-tier optimization playbook.

**Key Findings:**
- Amdahl's law-based bottleneck prioritization
- Five-stage correctness harness (smoke, shape sweeps, numerical, determinism, edge cases)
- Triton + CUDA C++ dual backend
- RMSNorm: 5.29x over eager, 2.83x over torch.compile
- First place on vectorsum_v2 B200 leaderboard

**GitHub:** https://github.com/RightNow-AI/autokernel

---

## 20. AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents (arXiv: 2605.16819)

**Authors:** Sharareh Younesian, Wenwen Ouyang, et al.
**Published:** 2026-05-16
**Categories:** cs.CL, cs.AI, cs.LG

**Abstract:** 196 tasks: HIP-to-HIP, Triton-to-Triton, PyTorch-to-HIP. Evaluates full agent workflows (not single LLM calls). Unseen-configuration generalization protocol. Up to 6.89x on PyTorch-to-HIP, 6.69x on HIP-to-HIP, 2.13x on Triton-to-Triton.

**Key Findings:**
- Tests generalization to unseen input configurations
- HIP and Triton optimizations transfer; PyTorch-to-HIP does not (hardcoded shapes)
- Tests Cursor Agent, Claude Code, Codex Agent
- Modular, extensible framework

---

## 21. GPU Kernel Scientist: LLM-Driven Framework for Iterative Kernel Optimization (arXiv: 2506.20807)

**Authors:** Martin Andrews, Sam Witteveen
**Published:** 2025-06-25
**Categories:** cs.LG, cs.AI, cs.PF, cs.SE

**Abstract:** LLM-powered automated methodology for iterative kernel refinement on AMD MI300. Evolutionary process: selecting prior versions, generating hypotheses, implementing experiments. Uses only timing data as feedback.

**Key Findings:**
- Targets AMD MI300 (less-documented architecture)
- Evolutionary optimization approach
- Compensates for limited domain expertise
- No source code mentioned

---

## 22. SwizzlePerf: Hardware-Aware LLMs for GPU Kernel Performance Optimization (arXiv: 2508.20258)

**Authors:** Arya Tschand, Muhammad Awad, et al.
**Published:** 2025-08-27
**Categories:** cs.DC, cs.AI

**Abstract:** Gives LLMs explicit hardware-awareness for spatial optimizations. Takes <5 minutes to generate optimal swizzling patterns that took experts 2 weeks. Up to 2.06x speedup, 70% L2 hit rate improvement.

**Key Findings:**
- Hardware-awareness via memory access patterns + architecture specs + profiling logs
- Swizzling pattern optimization
- Sub-5-minute generation vs 2 weeks expert time
- First systematic hardware-aware LLM performance engineering

---

## 23. QiMeng-Kernel: Macro-Thinking Micro-Coding for LLM-Based GPU Kernel Generation (arXiv: 2511.20100)

**Authors:** Xinguo Zhu, Shaohui Peng, et al.
**Published:** 2025-11-25
**Categories:** cs.DC, cs.CL

**Abstract:** MTMC framework: decouples optimization strategy from implementation. Macro Thinking uses RL for lightweight LLMs to explore strategies. Micro Coding uses general-purpose LLMs for incremental implementation. Near 100% accuracy at L1-2, 70% at L3 on KernelBench. Up to 7.3x speedup over LLMs, 2.2x over expert PyTorch.

**Key Findings:**
- Hierarchical: strategy (RL-trained lightweight LLM) + implementation (general LLM)
- Decouples what to optimize from how to implement
- Up to 59.64% accuracy on TritonBench, 34x speedup

---

## 24. CUDAnalyst: Feedback-to-Plan Decisions for Self-Evolving LLM Agents (arXiv: 2605.26720)

**Authors:** Yee Hin Chong, Jiaming Wu, et al.
**Published:** 2026-05-26
**Categories:** cs.AI

**Abstract:** Analysis layer for controlled attribution of planning decisions to feedback components. Shows explicit planning beneficial only when feedback is aligned. High-level plans from stronger reasoning models can transfer to weaker ones.

**Key Findings:**
- Trajectory freezing + selective feedback injection
- Coalitional-style attribution of feedback effects
- Planning emerges from structured multi-feedback interactions
- Strong-to-weak plan transfer

---

## 25. Fine-Tuning GPT-5 for GPU Kernel Generation / Makora (arXiv: 2602.11000)

**Authors:** Ali Tehrani, Yahya Emara, et al.
**Published:** 2026-02-11
**Categories:** cs.DC, cs.AI, cs.LG

**Abstract:** RL finetuning of GPT-5 for Triton code generation. Improves correctness from 43.7% to 77.0% (+33.3pp). Full coding agent solves up to 97.4% of expanded KernelBench, beating TorchInductor on 72.9% with 2.12x geomean speedup.

**Key Findings:**
- RL post-training of frontier models (GPT-5)
- 33.3pp correctness improvement
- 2.12x geomean speedup over TorchInductor
- Shows RL can unlock capabilities in specialized domains

---

## 26. FastKernels: Benchmarking GPU Kernel Generation in Production (arXiv: 2605.23215)

**Authors:** Gabriele Oliaro, Yichao Fu, et al.
**Published:** 2026-05-22
**Categories:** cs.LG, cs.AI, cs.CL

**Abstract:** 46 architectures spanning 8 categories, subsuming 96.2% of HuggingFace Transformers architectures. Doubles as production-grade inference framework (parity with vLLM/SGLang). Strongest agent achieves only 0.94x aggregate speedup over production baselines.

**Key Findings:**
- Production-aligned benchmark (not sandbox)
- Reveals benchmark-production misalignment as critical bottleneck
- Even best agents don't beat production baselines in aggregate

**GitHub:** https://github.com/Snowflake-AI-Research/fastkernels

---

## 27. Xe-Forge: Multi-Stage LLM-Powered Kernel Optimization for Intel GPU (arXiv: 2605.26118)

**Authors:** Marcin Spoczynski, et al.
**Published:** 2026-04-16
**Categories:** cs.DC, cs.AI

**Abstract:** Multi-stage pipeline for Intel GPU. Up to 9 optimization stages from algorithmic restructuring through operator fusion, block pointer modernization, GPU-specific tuning. Chain-of-Verification-and-Refinement (CoVeR) agent. 1.17x geomean speedup, up to 82x on individual kernels.

**Key Findings:**
- Targets Intel GPUs (cross-platform relevance)
- 9-stage optimization pipeline
- Chain-of-Verification-and-Refinement pattern
- Curated knowledge base for Intel GPU constraints

---

## 28. muCUTLASS: DSL + Speed-of-Light Guidance for GPU Kernel Optimization (arXiv: 2603.29010)

**Authors:** Siva Kumar Sastry Hari, et al.
**Published:** 2026-03-30
**Categories:** cs.LG, cs.AI

**Abstract:** Compact DSL (muCUTLASS) + Speed-of-Light (SOL) guidance. DSL lets model reason at higher level while preserving optimization levers. SOL uses first-principles performance bounds to steer search.

**Key Findings:**
- DSL approach: higher abstraction for LLM reasoning
- SOL guidance: estimate headroom, steer search, detect diminishing returns
- 0.40x regression -> 1.27x speedup with DSL; 1.56x with SOL guidance
- 19-43% token savings with SOL budgeting
- Detects benchmark-gaming cases

---

## 29. KernelFoundry: Hardware-aware Evolutionary GPU Kernel Optimization (arXiv: 2603.12440)

**Authors:** Nina Wiedemann, et al.
**Published:** 2026-03-12
**Categories:** cs.DC, cs.LG

**Abstract:** Evolutionary framework with MAP-Elites quality-diversity search, meta-prompt evolution, template-based parameter optimization. Generates SYCL (cross-platform) and CUDA kernels. 2.3x average speedup on KernelBench for SYCL.

**Key Findings:**
- MAP-Elites for diverse exploration
- Meta-prompt evolution (co-evolve prompts with kernels)
- Template-based parameter tuning
- Cross-platform SYCL support

---

## 30. CuTeGen: LLM-Based Agentic Framework for GPU Kernel Generation using CuTe (arXiv: 2604.01489)

**Authors:** Tara Saba, et al.
**Published:** 2026-04-01
**Categories:** cs.LG, cs.AI, cs.DC, cs.PF, cs.SE

**Abstract:** Uses CuTe abstraction layer for more stable iterative modification. Generate-test-refine workflow with execution-based validation, structured debugging, staged optimization. Workload-aware optimization prompts and delayed profiling feedback.

**Key Findings:**
- CuTe abstraction as LLM-friendly kernel representation
- Progressive refinement (not one-shot or large-scale search)
- Delayed integration of profiling feedback
- Focuses on stability of iterative modification

---

## 31. KEET: Explaining Performance of GPU Kernels Using LLM Agents (arXiv: 2605.04467)

**Authors:** Joshua H. Davis, et al.
**Published:** 2026-05-06
**Categories:** cs.PF, cs.DC

**Abstract:** LLM-based agentic framework for interpreting Nsight Compute profiles. Generates natural language explanations of performance issues and optimization suggestions.

**Key Findings:**
- Nsight Compute profile interpretation
- Natural language explanations improve downstream code optimization
- Can process large sets of profiles

---

## 32. Record-Remix-Replay: Hierarchical GPU Kernel Optimization (arXiv: 2604.11109)

**Authors:** Daniel Nichols, et al.
**Published:** 2026-04-13
**Categories:** cs.DC, cs.AI, cs.LG, cs.PF

**Abstract:** Combines LLM-driven evolutionary search, Bayesian optimization, and record-replay compilation. Optimizes from source-level to compiler pass ordering to runtime configuration.

**Key Findings:**
- Hierarchical: source -> compiler -> runtime
- Nearly order of magnitude faster than modern evolutionary search
- Full scientific application optimization

---

## 33. GPU Kernel Optimization Beyond Full Builds (arXiv: 2512.22147)

**Authors:** Ruifan Chu, et al.
**Published:** 2025-12-15
**Categories:** cs.DC, cs.AI, cs.LG, cs.PF

**Abstract:** Optimizes kernels without building full application. Minimal Executable Program (MEP) approach. Auto Error Repair + Performance Pattern Inheritance.

**Key Findings:**
- MEP: extract hotspot, create standalone program, optimize outside full app
- Cross-platform (NVIDIA + AMD DCU)
- 5.05x avg on PolyBench NVIDIA, 7.77x on DCU

---

## 34. POLCA: Stochastic Generative Optimization with LLM (arXiv: 2603.14769)

**Authors:** Xuanfei Ren, Allen Nie, et al.
**Published:** 2026-03-16
**Categories:** cs.LG, cs.AI

**Abstract:** General framework for stochastic generative optimization. Priority queue + epsilon-Net + LLM Summarizer. Evaluated on KernelBench among other benchmarks.

**Key Findings:**
- General optimization framework applicable to kernel generation
- Handles stochasticity in feedback
- Meta-learning across historical trials

**GitHub:** https://github.com/rlx-lab/POLCA

---

## 35. Liger Kernel: Efficient Triton Kernels for LLM Training (arXiv: 2410.10989)

**Authors:** Pin-Lun Hsu, et al.
**Published:** 2024-10-14
**Categories:** cs.LG, cs.AI, cs.CL, cs.DC

**Abstract:** Open-sourced Triton kernels for LLM training. Kernel operation fusing and input chunking. 20% increase in training throughput, 60% reduction in GPU memory.

**Key Findings:**
- Human-written optimized Triton kernels (not AI-generated)
- Kernel fusion and input chunking techniques
- Practical reference for what high-quality Triton looks like

**GitHub:** https://github.com/linkedin/Liger-Kernel

---

## 36. ClusterFusion: Expanding Operator Fusion Scope for LLM Inference (arXiv: 2508.18850)

**Authors:** Xinhao Luo, et al.
**Published:** 2025-08-26
**Categories:** cs.DC, cs.AI

**Abstract:** Cluster-level communication primitives (ClusterReduce, ClusterGather) for expanding operator fusion. Fuses QKV Projection + Attention + Output Projection into single kernel. 1.61x avg end-to-end latency improvement.

**Key Findings:**
- Cluster-level fusion on H100
- Fuses multiple attention stages into single kernel
- Structured collective communication primitives

**GitHub:** https://github.com/xinhao-luo/ClusterFusion

---

## SUMMARY OF KEY THEMES AND PATTERNS

### Approaches to AI-Powered Kernel Optimization:

1. **RL Training** (Dr. Kernel, DRTriton, TritonRL, AutoTriton, CUDA Agent, Kevin, Makora/GPT-5)
   - SFT warmup + RL fine-tuning
   - Key challenges: reward hacking, lazy optimization, data scarcity
   - Solutions: profiling-based rewards, hierarchical reward decomposition, multi-turn RL

2. **Multi-Agent Systems** (Astra, CudaForge, KernelSkill, cuPilot, CUDAnalyst)
   - Coder + Judge / Coder + Verifier patterns
   - Strategy-level coordination
   - Hardware feedback integration (Nsight Compute)

3. **Evolutionary/Search-Based** (EvoEngineer, OptiML, KernelFoundry, R3, GPU Kernel Scientist)
   - Code evolution with LLM-generated mutations
   - MCTS, MAP-Elites, Bayesian optimization
   - Population-based search

4. **Abstraction/DSL Approaches** (CODA, muCUTLASS, CuTeGen)
   - Higher-level abstractions for LLM reasoning
   - Constrained interfaces that preserve performance structure
   - DSL + compiler backends

5. **Benchmarks** (KernelBench, AgentKernelArena, FastKernels, robust-kbench)
   - KernelBench: 250 tasks, 3 levels, fast_p metric
   - AgentKernelArena: generalization testing, 196 tasks
   - FastKernels: production-aligned, 46 architectures
   - robust-kbench: rigorous correctness testing

### Key GitHub Repos:

| Repo | Paper |
|------|-------|
| github.com/hkust-nlp/KernelGYM | Dr. Kernel |
| github.com/AI9Stars/AutoTriton | AutoTriton |
| github.com/OptimAI-Lab/CudaForge | CudaForge |
| github.com/Anjiang-Wei/Astra | Astra |
| github.com/0satan0/KernelMem/ | KernelSkill |
| github.com/RightNow-AI/autokernel | AutoKernel |
| github.com/champloo2878/cuPilot-Kernels | cuPilot |
| github.com/Snowflake-AI-Research/fastkernels | FastKernels |
| github.com/linkedin/Liger-Kernel | Liger Kernel |
| github.com/xinhao-luo/ClusterFusion | ClusterFusion |
| github.com/rlx-lab/POLCA | POLCA/OptiML |

### State of the Art (as of May 2026):
- **KernelSkill**: 100% success rate, 5.44x/2.82x/1.92x on KernelBench L1/L2/L3
- **CUDA Agent**: 100%/100%/92% faster than torch.compile on L1/L2/L3
- **DRTriton-7B**: 92% speedup rate on L2 (vs 23% GPT-5.2)
- **Makora/GPT-5-RL**: 97.4% solve rate, 2.12x over TorchInductor
- **FastKernels finding**: even best agents only 0.94x over production baselines (gap remains!)
