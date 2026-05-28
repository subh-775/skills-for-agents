# AI/Agent-Based GPU Kernel Optimization: Academic Paper Survey (36 Papers)

## Category 1: RL-Training Approaches

### Dr. Kernel (arXiv: 2602.05885)
- Systematic study of RL for kernel generation
- KernelGYM: robust distributed GPU environment
- TRLOO: Turn-level Reinforce-Leave-One-Out for unbiased advantage
- 14B model competitive with Claude-4.5-Sonnet
- GitHub: https://github.com/hkust-nlp/KernelGYM

### DRTriton (arXiv: 2603.21465)
- CSP-DAG for synthetic data generation
- Curriculum RL with decoupled rewards (success rate + execution speed)
- Test-time search for further improvement
- 7B model: 92% speedup rate on KBL2 (vs 23% GPT-5.2, 19% Claude-Sonnet-4.5)

### TritonRL (arXiv: 2510.17891)
- 8B-scale LLM for Triton programming via RL
- Hierarchical Reward Decomposition (HRD): decouples reasoning vs implementation
- Multi-layered verification (syntax + function + performance)
- SOTA on KernelBench, matching >100B parameter models

### AutoTriton (arXiv: 2507.05687)
- First dedicated model for Triton programming via RL
- SFT + GRPO with rule-based and execution-based rewards
- 8B model comparable to Claude-4-Sonnet and DeepSeek-R1-0528
- GitHub: https://github.com/AI9Stars/AutoTriton

### CUDA Agent (arXiv: 2602.24286)
- Large-scale agentic RL with scalable data synthesis
- Skill-augmented CUDA dev environment
- 100%/100%/92% faster than torch.compile on KBL1/L2/L3
- Outperforms Claude Opus 4.5 and Gemini 3 Pro by ~40% on L3

### Kevin (arXiv: 2507.11948)
- First multi-turn RL for CUDA kernel generation
- Serial refinement scaling > parallel sampling
- QwQ-32B base, surpasses o4-mini
- Correctness: 56% → 82%, mean speedup: 0.53x → 1.10x

### Makora/GPT-5-RL (arXiv: 2602.11000)
- RL finetuning of GPT-5 for Triton code generation
- Correctness: 43.7% → 77.0% (+33.3pp)
- 97.4% solve rate, 2.12x geomean over TorchInductor

### DICE (arXiv: 2602.11715)
- Diffusion LLMs for CUDA kernel generation
- BiC-RL: two-phase training (infilling then full generation)
- CuKe dataset for high-performance CUDA kernels

---

## Category 2: Multi-Agent Systems

### KernelSkill (arXiv: 2603.10085)
- Dual-level memory: long-term (reusable skills) + short-term (anti-backtracking)
- 100% success rate on KernelBench L1-3
- Speedups: 5.44x (L1), 2.82x (L2), 1.92x (L3) — BEST REPORTED
- GitHub: https://github.com/0satan0/KernelMem

### CudaForge (arXiv: 2511.01884)
- Multi-agent: Coder + Judge with Nsight Compute feedback
- Training-free (uses OpenAI-o3)
- 97.6% correctness, 1.68x average speedup
- ~26.5 min per kernel, ~$0.30 API cost
- Works across GPUs (A100, RTX6000, 4090, 3090)
- GitHub: https://github.com/OptimAI-Lab/CudaForge

### Astra (arXiv: 2509.07506)
- First LLM multi-agent for GPU kernel optimization starting from existing CUDA
- Targets real SGLang production kernels
- 1.32x average speedup with zero-shot OpenAI o4-mini
- LLMs apply loop transforms, memory optimizations, CUDA intrinsics
- GitHub: https://github.com/Anjiang-Wei/Astra

### cuPilot (arXiv: 2512.16465)
- Strategy-coordinated multi-agent framework
- Roofline-guided prompting (hardware-aware)
- 3.09x average speedup over PyTorch on 100 kernels
- GitHub: https://github.com/champloo2878/cuPilot-Kernels

### CUDAnalyst (arXiv: 2605.26720)
- Analysis layer for feedback-to-plan decisions
- Trajectory freezing + selective feedback injection
- Strong-to-weak plan transfer

---

## Category 3: Evolutionary/Search-Based

### EvoEngineer (arXiv: 2510.03760)
- 91 real-world CUDA kernels: 2.72x median speedup, 69.8% validity
- Max speedup: 36.75x
- Formal problem formulation (objective, constraints, metrics)

### OptiML (arXiv: 2602.12305)
- MCTS over LLM-driven edits with Nsight Compute profiling
- Composite objective: runtime + bottleneck proxies + regression guards
- NL-to-CUDA or CUDA-to-optimized-CUDA pipeline
- GitHub: https://github.com/rlx-lab/POLCA

### KernelFoundry (arXiv: 2603.12440)
- MAP-Elites quality-diversity search
- Meta-prompt evolution (co-evolve prompts with kernels)
- Template-based parameter tuning
- 2.3x average speedup on KernelBench for SYCL

### GPU Kernel Scientist (arXiv: 2506.20807)
- Evolutionary optimization on AMD MI300
- Uses only timing data as feedback
- Compensates for limited domain expertise

### R3 / Record-Remix-Replay (arXiv: 2604.11109)
- Hierarchical: source → compiler → runtime
- Nearly order of magnitude faster than modern evolutionary search

### Kernel-Smith (arXiv: 2603.28342)
- SOTA on KernelBench with Triton/NVIDIA backend
- Evolutionary kernel optimization

---

## Category 4: Abstraction/DSL Approaches

### CODA (arXiv: 2605.19269)
- GEMM-plus-epilogue abstraction for Transformer ops
- 5 composable epilogue primitives
- LLM-authored kernels achieve high performance
- GitHub: https://github.com/HanGuo97/coda-kernels

### muCUTLASS (arXiv: 2603.29010)
- Compact DSL + Speed-of-Light guidance
- DSL lets model reason at higher level while preserving optimization levers
- 0.40x regression → 1.27x speedup with DSL; 1.56x with SOL guidance

### CuTeGen (arXiv: 2604.01489)
- CuTe abstraction for LLM-friendly kernel representation
- Progressive refinement with delayed profiling feedback

---

## Category 5: Benchmarks

### KernelBench (arXiv: 2502.10517)
- 250 PyTorch workloads, 3 difficulty levels
- fast_p metric: % of kernels correct AND >p speedup
- Frontier models match PyTorch baseline <20% of cases
- THE foundational benchmark

### AgentKernelArena (arXiv: 2605.16819)
- 196 tasks: HIP-to-HIP, Triton-to-Triton, PyTorch-to-HIP
- Tests generalization to unseen input configurations
- Evaluates full agent workflows (Cursor, Claude Code, Codex)

### FastKernels (arXiv: 2605.23215)
- 46 architectures covering 96.2% of HuggingFace Transformers
- Production-grade (parity with vLLM/SGLang)
- Critical finding: best agents only 0.94x over production baselines
- GitHub: https://github.com/Snowflake-AI-Research/fastkernels

### TritonBench (arXiv: 2502.14752)
- 184 real-world Triton operators from GitHub repos (>100 stars)
- First comprehensive Triton operator benchmark
- GitHub: https://github.com/thunlp/TritonBench

### robust-kbench (arXiv: 2509.14279)
- Rigorous correctness testing beyond KernelBench
- Evolutionary meta-generation with LLM-based verifiers

---

## Category 6: CUDA Frameworks & Libraries

### FlashAttention Family
- FlashAttention (2205.14135) — IO-aware tiling, 15% on BERT, 3x on GPT-2
- FlashAttention-3 (2407.08608) — Hopper: warp spec + FP8, 740 TFLOPs/s
- CUTLASS FA-2 (2312.11918) — TMA + WGMMA, 20-50% over Ampere

### ThunderKittens (arXiv: 2410.20399)
- Three abstraction levels: warp-level, thread-block-level, grid-level
- Matches cuBLAS and FlashAttention-3
- 10-40% faster on attention backward, 8x on SSMs, 14x on linear attention

### Liger Kernel (arXiv: 2410.10989)
- Production Triton kernels for LLM training
- 20% throughput increase, 60% GPU memory reduction
- GitHub: https://github.com/linkedin/Liger-Kernel

### CUDA-L2 (arXiv: 2512.02551)
- LLM+RL for HGEMM optimization
- Surpasses cuBLAS by 19.2%, cuBLASLt by 11.4%
- GitHub: https://github.com/deepreinforce-ai/CUDA-L2

---

## Key Findings Across All Papers

1. **RL training > few-shot prompting** for specialized kernel generation
2. **Profiling feedback is critical** — 42.7% success with profiling vs 11.4% without
3. **Multi-agent > single agent** — Coder+Judge pattern consistently wins
4. **3-4 iteration rounds optimal** — diminishing returns beyond that
5. **Autotuning is #1 low-hanging fruit** — up to 95x on naive kernels
6. **Triton is highly portable** — 62-101% of cuBLAS across architectures
7. **Production gap remains** — even best agents don't beat hand-tuned production kernels
8. **Memory coalescing + occupancy** are the two dominant bottlenecks
9. **Smaller RL-trained models beat frontier models** — DRTriton-7B >> GPT-5.2
10. **CODA's epilogue abstraction** is practical for LLM-generated kernels
