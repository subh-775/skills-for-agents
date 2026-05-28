# MoE (Mixture of Experts) Kernel Optimization: Comprehensive Reference

## 1. KEY PAPERS AND CODE REPOS

### 1.1 TritonMoE — Cross-Platform Fused MoE Dispatch in Triton
- **Paper**: arXiv:2605.23911 (Apr 2026)
- **Author**: Subhadip Mitra
- **Repo**: https://github.com/bassrehab/triton-kernels
- **Key Innovation**: Complete fused MoE dispatch kernel in pure OpenAI Triton (no CUDA)
- **What it does**: Router scoring → token permutation → expert GEMMs → weighted output combination
- **Key optimizations**:
  - Block-scheduled grouped GEMM mapping Triton program blocks to (expert_id, token_offset) pairs
  - Fused gate+up GEMM: computes both SwiGLU projections from shared L2-cached input tiles with in-register SiLU activation
  - Eliminates 35% of global memory traffic vs unfused
  - 5 kernel launches regardless of expert count (vs 3E+4 naive)
- **Performance**: 89-131% of CUDA-optimized Megablocks at ≤512 tokens on A100
- **Cross-platform**: All 162 tests pass on both NVIDIA A100 and AMD MI300X with zero code changes
- **Code patterns**:
  - Manual stable softmax (subtract max before exp) — Triton's tl.softmax doesn't do this
  - Top-k via iterative argmax with masking to -1.0 (not 0.0) to prevent re-selection
  - Supports both softmax gating (Mixtral) and sigmoid gating (DeepSeek)
  - Permute via stable sort on expert assignments + Triton gather kernel with BLOCK_D tiling
  - BLOCK_M fixed (not autotuned) to match precomputed schedule; only BLOCK_N/BLOCK_K autotuned
  - Weight tensor stored as E·N × K (flattened)

### 1.2 FlashMoE — Fast Distributed MoE in a Single Kernel
- **Paper**: arXiv:2506.04667 (Jun 2025)
- **Repo**: https://github.com/osayamenja/FlashMoE
- **Key Innovation**: Fully GPU-resident MoE operator fusing computation + inter-GPU communication into ONE persistent kernel
- **What it does**: Dispatch → compute → combine phases in single kernel with fine-grained pipelining
- **Key optimizations**:
  - Eliminates CPU-managed scheduling and host-initiated communication
  - Uses device-initiated one-sided RDMA transfers (not bulk-synchronous collectives)
  - Payload efficiency: eliminates bloated/redundant network payloads in sparse layers
  - Persistent kernel eliminates kernel launch overhead
- **Performance**: Up to 9× higher GPU utilization, 6× lower latency, 5.7× higher throughput vs baselines on 8×H100
- **Scale**: Up to 128 experts, 16K token sequences

### 1.3 MegaBlocks — Efficient Sparse Training with MoE
- **Paper**: arXiv:2211.15841 (Nov 2022) — MLSys 2023
- **Authors**: Trevor Gale, Deepak Narayanan, Cliff Young, Matei Zaharia
- **Repo**: https://github.com/stanford-futuredata/megablocks
- **Key Innovation**: Reformulates MoE as block-sparse operations with custom GPU kernels
- **Key optimizations**:
  - Block-sparse matrix operations (uses stk framework: https://github.com/stanford-futuredata/stk)
  - Never drops tokens (no capacity factor needed)
  - No padding waste
  - dMoE variant with SwiGLU support
- **Performance**: Up to 40% faster than Tutel, 2.4× over Megatron-LM
- **Limitation**: CUDA-only, fragile at 256 experts, doesn't support DeepSeek-V3 top-8 routing
- **Used by**: Megatron-LM

### 1.4 ScatterMoE — Scattered Mixture-of-Experts Implementation
- **Paper**: arXiv:2403.08245 (Mar 2024)
- **Repo**: https://github.com/shawntan/scattermoe
- **Key Innovation**: ParallelLinear primitive that fuses grouped GEMMs with scatter/gather
- **Key optimizations**:
  - Avoids padding AND avoids excessive copies of input
  - ParallelLinear supports 4 modes: grouped→grouped, scattered→grouped, scattered→scattered, grouped→scattered
  - Sorts tokens by expert, pads indices instead of data → load padded tiles into SRAM
  - Memory: 66.2% of Megablocks during training, 53.6% for inference
  - Extends to Mixture-of-Attention (MoA) via scattered→scattered mode
- **Performance**: 38.1% faster than Megablocks sparse in training, scales better with granularity
- **Written in**: Triton

### 1.5 RaMP — Runtime-Aware Megakernel Polymorphism for MoE
- **Paper**: arXiv:2604.26039 (Apr 2026)
- **Authors**: Vyom Sharma, Debajyoti Datta
- **Key Innovation**: Routing-aware dispatch — selects kernel config from runtime expert histogram, not just batch size
- **Key optimizations**:
  - 4-parameter wave cost model: startup + wave scheduling + per-CTA traffic + sub-wave nonlinearity
  - Performance-region analysis from hardware constants (ρ, λ, ω, κ)
  - GROUP_M swizzle when λ·κ > 1440 (L2 pressure threshold)
  - Split-K when κ ≥ 48 ∧ ω < 0.2
  - CuTe DSL kernel with 134-268 polymorphic configurations
  - Runtime dispatch via fused Triton kernel: bincount + cost eval + argmin in ~38μs
- **Performance**: 1.22× kernel speedup over static dispatch, 1.30× E2E in vLLM over Triton, 1.41× over DeepGEMM, 1.13× over FlashInfer CUTLASS
- **Kernel-agnostic**: Applied to Alpha-MoE with no source modification → 1.14× speedup
- **Key insight**: Real MoE routing is deeply skewed (β≈0.5, only 8-14% experts active), yet all production systems dispatch as if uniform

### 1.6 UniEP — Unified Expert-Parallel MoE MegaKernel for LLM Training
- **Paper**: arXiv:2604.19241 (Apr 2026)
- **Authors**: Size Zheng, Xuegui Zheng, Li-wen Chang, Jidong Zhai (ByteDance/Tsinghua)
- **Key Innovation**: Fuses MoE communication + computation into MegaKernels with unified parameter search
- **Key optimizations**:
  - Deterministic token ordering for numerical consistency
  - Transforms complex EP tuning into unified parameter search space
  - Co-designed with Megatron-LM
- **Performance**: 1.03×-1.38× over state-of-the-art on Hopper GPUs

### 1.7 MoEBlaze — Breaking Memory Wall for Efficient MoE Training
- **Paper**: arXiv:2601.05296 (Jan 2026)
- **Key Innovation**: End-to-end token dispatch + MoE training with optimized data structures
- **Key optimizations**:
  - Eliminates intermediate buffers and activation materializing
  - Co-designed kernels with smart activation checkpoint
  - 4× speedups, 50%+ memory savings vs existing MoE frameworks

### 1.8 NCCL EP — Unified Expert Parallel Communication API
- **Paper**: arXiv:2603.13606 (Mar 2026)
- **Key Innovation**: MoE communication library built on NCCL Device API
- **Key optimizations**:
  - ncclEpDispatch and ncclEpCombine primitives (C and Python)
  - LL mode: inference decoding (1-128 tokens) with direct all-to-all RDMA+NVLink
  - HT mode: training/prefill (4096+ tokens) with hierarchical NVLink→RDMA
  - Double-buffered communication for overlap

### 1.9 DySHARP — Dynamic In-Switch Computing for MoE
- **Paper**: arXiv:2605.05607 (May 2026)
- **Key Innovation**: In-switch computing for MoE dispatch-compute-combine pipeline
- **Key optimizations**:
  - Dynamic multimem addressing as extension to NVLink SHARP
  - Token-centric kernel fusion deeply fusing dispatch-computation-combine
  - 1.79× speedup over state-of-the-art

### 1.10 Hexcute — Automated Layout Synthesis for GPU Programs
- **Paper**: arXiv:2504.16214 (Apr 2025)
- **Key Innovation**: Compiler framework automating layout synthesis for GPU programs
- **MoE relevance**: 6.46× average speedup over Triton on mixed-type MoE operators
- **E2E**: Up to 2.60× speedup on DeepSeek-R1-AWQ in vLLM

### 1.11 ParallelKittens — Multi-GPU AI Kernel Simplification
- **Paper**: arXiv:2511.13940 (Nov 2025)
- **Key Innovation**: Minimal CUDA framework for overlapped multi-GPU kernels
- **MoE relevance**: 1.22× speedup for expert-parallel workloads with <50 lines device code

### 1.12 fabric-lib — RDMA Point-to-Point Communication
- **Paper**: arXiv:2510.27656 (Oct 2025)
- **Repo**: https://github.com/perplexityai/pplx-garden/
- **MoE relevance**: MoE dispatch/combine implementation exceeding DeepEP decode latency
- **Portability**: Works on both ConnectX-7 and AWS EFA

### 1.13 MoEShard — Expert Sharding for MoE Inference
- **Paper**: arXiv:2503.08467 (Mar 2025)
- **Key Innovation**: Perfect load balancing through tensor sharding of MoE experts
- **Key optimizations**:
  - Row- and column-wise decomposition of expert matrices
  - Fuses decomposed expert computations
  - 6.4× speedup in TTFT over DeepSpeed

### 1.14 MoE-Inference-Bench — Performance Evaluation
- **Paper**: arXiv:2508.17467 (Aug 2025)
- **Key**: Comprehensive benchmark of MoE optimizations on H100
- **Evaluates**: Pruning, Fused MoE, speculative decoding, quantization, parallelization
- **Models**: Mixtral, DeepSeek, OLMoE, Qwen families

### 1.15 QMoE — Sub-1-Bit Compression of Trillion-Parameter MoEs
- **Paper**: arXiv:2310.16795 (Oct 2023)
- **Repo**: https://github.com/IST-DASLab/qmoe
- **Key Innovation**: Custom GPU decoding kernels for compressed MoE inference
- **Achievement**: 1.6T param SwitchTransformer in <160GB (20× compression, 0.8 bits/param)

### 1.16 ARGUS — Agentic GPU Optimization for MoE Kernels
- **Paper**: arXiv:2604.18616 (Apr 2026)
- **Key Innovation**: LLM agent for generating optimized MoE kernels with data-flow invariants
- **Achievement**: Generated MoE kernels at 99-104% of hand-optimized assembly throughput on MI300X

---

## 2. PRODUCTION MoE KERNEL IMPLEMENTATIONS

### 2.1 vLLM Fused MoE (Triton)
- **Code**: vLLM repo, `vllm/model_executor/layers/fused_moe/`
- **Backend**: Triton FP8 kernel
- **Dispatch**: Nearest-M batch-size dispatch (static, not routing-aware)
- **Config space**: ~2K configurations
- **Used for**: OLMoE, DeepSeek-V3, Mixtral, Qwen serving

### 2.2 DeepGEMM (DeepSeek)
- **Repo**: https://github.com/deepseek-ai/DeepGEMM
- **Backend**: JIT-compiled FP8 grouped GEMM
- **Dispatch**: Fixed bm=128 (no routing awareness)
- **Limitation**: Poorly matched to small expert sizes (OLMoE)

### 2.3 Alpha-MoE (Aleph Alpha)
- **Repo**: https://github.com/Aleph-Alpha/Alpha-MoE
- **Backend**: JIT-tuned C++ kernel (~2 hours per model)
- **Dispatch**: Per-M dispatch (has RA modules but default serving uses per-M only)
- **Config space**: 160 configurations

### 2.4 FlashInfer
- **Repo**: FlashInfer project
- **Backend**: Integrated CUTLASS/TRT-LLM kernels
- **Dispatch**: Internal autotuning, per-M

### 2.5 SonicMoE
- **Paper**: arXiv:2512.14080
- **Focus**: Training (IO-overlapping kernels for near-roofline throughput)

### 2.6 Tutel (Microsoft)
- **Paper**: Hwang et al., MLSys 2023
- **Key**: Adaptive parallelism for MoE at scale
- **CUDA-only**

### 2.7 FasterMoE
- **Paper**: He et al., PPoPP 2022
- **Key**: Dynamic expert scheduling
- **CUDA-only**

---

## 3. CODE PATTERNS AND KERNEL DESIGN PATTERNS

### 3.1 Fused MoE Kernel Anatomy (3-phase)
```
Phase 1 (up-projection):
  - Load expert weight tiles via TMA (Tensor Memory Accelerator)
  - Compute H_e = X_e · W_{1,e} through WGMMA matrix-multiply-accumulate
  - Producer threads issue TMA loads + cp.async into multi-stage SMEM pipeline
  - Consumer threads drain pipeline via WGMMA from SMEM descriptors

Phase 2 (activation):
  - Apply SwiGLU nonlinearity with in-register FP8 re-quantization
  - NO write to HBM (keep in registers between phases)

Phase 3 (down-projection):
  - Compute final output
  - Scatter back to token positions via atomic add / cp.reduce.async.bulk
```

### 3.2 Block-Scheduled Grouped GEMM (TritonMoE pattern)
```python
# Algorithm: Block Schedule Construction
expert_offsets = compute_expert_offsets(token_assignments)  # E+1 entries
blocks = []
for e in range(E):
    n_e = expert_offsets[e+1] - expert_offsets[e]
    for b in range(ceil(n_e / BLOCK_M)):
        blocks.append((e, b * BLOCK_M))

# Each Triton program block:
#   - loads expert e's weight from flattened E*N x K tensor
#   - processes BLOCK_M token rows from expert-contiguous input
#   - partial tiles handled via masking
# CRITICAL: BLOCK_M must be fixed (not autotuned) to match schedule
```

### 3.3 Fused Gate+Up Projection (SwiGLU)
```python
# Single kernel pass for both gate and up projections:
for k in range(0, K, BLOCK_K):
    A = load_input_tile(m:m+M, k:k+K)  # from L2 cache
    B_gate = load_weight_tile(W_gate, e, n:n+N, k:k+K)
    B_up = load_weight_tile(W_up, e, n:n+N, k:k+K)
    acc_gate += A @ B_gate
    acc_up += A @ B_up

# After K-loop: SiLU in FP32 registers
intermediate = SiLU(acc_gate) * acc_up  # single write to global memory
# Saves: gate_out and up_out buffers eliminated (35% memory traffic reduction)
```

### 3.4 Router Kernel (TritonMoE)
```python
# Manual stable softmax (tl.softmax doesn't subtract max)
scores = W_r @ x  # router projection
scores_max = tl.max(scores, axis=0)
scores = tl.exp(scores - scores_max)
scores = scores / tl.sum(scores, axis=0)

# Top-k via iterative argmax with masking
selected_mask = tl.full([E], -1.0, dtype=float32)  # NOT 0.0!
for i in range(k):
    idx = tl.argmax(scores + selected_mask, axis=0)
    selected_mask[idx] = -1.0  # mask with -1.0 prevents re-selection
    # Why -1.0 not 0.0: softmax scores near 0 for large E (256+)
    # masking to 0.0 fails to differentiate selected vs unselected
```

### 3.5 ScatterMoE ParallelLinear Pattern
```python
# Core: scatter2scatter Triton kernel
# Supports 4 modes:
#   grouped_in=True, grouped_out=True   → standard grouped GEMM
#   grouped_in=False, grouped_out=True  → scatter input, group output
#   grouped_in=True, grouped_out=False  → group input, scatter output
#   grouped_in=False, grouped_out=False → scatter→scatter (for MoA)

# SMoE MLP optimization:
H = ParallelLinear(X, W1, order, grouped_in=False, grouped_out=True)  # up
H = activation(H)
Y = ParallelLinear(H, W2, order, weights, grouped_in=True, grouped_out=False)  # down
# Each ParallelLinear needs only ONE group operation in backward pass
```

### 3.6 CuTe DSL Fused MoE Kernel (RaMP pattern)
```
Configuration space: c = (bm, bn, wn, stg)
  bm: token block size (2-104)
  bn: weight sub-tile width
  wn: consumer warp count
  stg: pipeline depth (1-5 stages)

CTA grid = Σ_e ⌈c_e/bm⌉ × ⌈N/(bn·wn)⌉
  M-tiles: routing-dependent (changes every step)
  N-tiles: config-dependent

Producer-consumer warp specialization:
  128 producer threads: TMA weight loads + cp.async activation gathers
  wn×32 consumer threads: WGMMA from SMEM descriptors

Dynamic register allocation: supports bm up to 104 (vs 72 in prior work)
Grid overlaunch: upper-bound grid with early-exit, no GPU-to-CPU sync
```

### 3.7 Routing-Aware Dispatch (RaMP)
```python
# Performance-region variables (from hardware constants):
rho = N * K / (ttn * tile_k)  # compute density per CTA
lam = ceil(N / ttn)            # L2 pressure (N-tiles)
omega = grid(c, routing) / SM_COUNT  # wave utilization
kappa = K / tile_k             # K-reduction depth

# Cost model (4 parameters per config):
T(c) = a(c) + b(c) * g/SM + c(c) * g + d(c) * log(g+1)
#  startup   waves      per-CTA     sub-wave
# g = Σ_e ⌈c_e/bm⌉ (routing-dependent)

# Decision thresholds:
GROUP_M needed: λ·κ > 1440
Split-K needed: κ ≥ 48 ∧ ω < 0.2
ttn=512 beneficial: ω > 1

# Runtime dispatch (~38μs):
# 1. Expert histogram via atomic bincount
# 2. Vectorized cost evaluation for all configs
# 3. Argmin → select pre-compiled kernel binary
```

### 3.8 FlashMoE Persistent Kernel Design
```
Single persistent kernel fusing:
  - Dispatch phase: device-initiated one-sided RDMA
  - Compute phase: expert GEMMs
  - Combine phase: weighted output aggregation

Key: eliminates bulk-synchronous collectives (all-to-all)
Instead: one-sided RDMA transfers with fine-grained pipelining
  - Dispatch, compute, and combine phases overlap
  - Payload efficiency: no bloated/redundant network payloads
  - 9× higher GPU utilization vs baselines
```

---

## 4. MoE ARCHITECTURE REFERENCE

### 4.1 Standard MoE Forward Pass
```python
# Router
s = softmax(W_r @ x) ∈ R^E           # or sigmoid for DeepSeek-style
T = top-k(s) = {(e1,w1), ..., (ek,wk)}  # routing decisions

# Expert computation (SwiGLU)
FFN_e(x) = (SiLU(x @ W_gate_e) ⊙ x @ W_up_e) @ W_down_e

# Output
y = Σ wi · FFN_ei(x)  # weighted sum of expert outputs
```

### 4.2 Model Configurations
| Model | Experts (E) | Top-k | d_model | d_ffn | Notes |
|-------|------------|-------|---------|-------|-------|
| Mixtral-8x7B | 8 | 2 | 4096 | 14336 | Softmax gating |
| Mixtral-8x22B | 8 | 2 | 6144 | 16384 | |
| DeepSeek-V2 | 160 | 6 | 5120 | 1536 | Sigmoid, MLA |
| DeepSeek-V3 | 256 | 8 | 7168 | 2048 | Sigmoid, MLA, 671B total/37B active |
| Qwen2-MoE-57B | 64 | 4 | 3584 | 2560 | |
| Qwen3 | 128 | 8 | — | — | |
| OLMoE | 64 | 8 | 2048 | 2048 | 7B total/1B active |
| DBRX | 16 | 4 | 6144 | 10752 | |
| Phi-3.5-MoE | 16 | 2 | 4096 | — | |

### 4.3 Expert Routing Skew in Production
- Real routing is deeply skewed: β ≈ 0.5 (far from uniform β=1.0)
- Only 8-14% of experts active per layer
- 96% of observations have β < 0.7
- Static dispatch tuned at β=1.0 is systematically mismatched
- This mismatch leaves 10-70% of kernel throughput unrealized

---

## 5. GITHUB REPOS SUMMARY

| Repo | URL | Language | Focus |
|------|-----|----------|-------|
| TritonMoE (triton-kernels) | github.com/bassrehab/triton-kernels | Triton | Cross-platform fused MoE dispatch |
| FlashMoE | github.com/osayamenja/FlashMoE | CUDA | Persistent kernel, GPU-resident MoE+comm |
| MegaBlocks | github.com/stanford-futuredata/megablocks | CUDA/Triton | Block-sparse MoE training |
| ScatterMoE | github.com/shawntan/scattermoe | Triton | ParallelLinear, no-padding MoE |
| Alpha-MoE | github.com/Aleph-Alpha/Alpha-MoE | CUDA/C++ | JIT-tuned fused MoE kernel |
| DeepGEMM | github.com/deepseek-ai/DeepGEMM | CUDA | FP8 grouped GEMM for MoE |
| vLLM | github.com/vllm-project/vllm | Python/Triton | Production MoE serving |
| fabric-lib | github.com/perplexityai/pplx-garden/ | C/CUDA | RDMA p2p for MoE dispatch |
| QMoE | github.com/IST-DASLab/qmoe | CUDA | Compressed MoE inference kernels |
| stk | github.com/stanford-futuredata/stk | Triton/CUDA | Sparse toolkit (used by MegaBlocks) |
| SeerAttention | github.com/microsoft/SeerAttention | CUDA | MoE-inspired block-sparse attention |
| DeepSeek-V3 | github.com/deepseek-ai/DeepSeek-V3 | Python | Full model with MoE architecture |
| PipeWeave | github.com/zksainx/pipeweave | Python | GPU perf prediction, MoE kernel optimization |

---

## 6. KEY INSIGHTS FOR TRITONIFY SKILL

### What makes MoE kernels hard:
1. Variable batch sizes per expert (prevents standard batched GEMM)
2. Irregular memory access patterns (token routing is dynamic)
3. Small per-expert batches at high expert counts → weight loading dominates
4. Routing distribution changes every forward step
5. 35% of frontier models use MoE; fused kernel is 60%+ of per-token latency

### Critical optimizations to implement:
1. **Grouped GEMM**: Map program blocks to (expert, token-offset) pairs
2. **Fused gate+up**: Shared A-tile loads, in-register SiLU (35% memory savings)
3. **Block-sparse layout**: For handling variable expert sizes without padding
4. **Routing-aware dispatch**: Adapt tile size to runtime expert histogram
5. **Cross-platform Triton**: Use only tl.* primitives, no libdevice

### Triton-specific patterns:
- Use manual stable softmax (subtract max)
- Mask top-k selections to -1.0 not 0.0
- Fix BLOCK_M for grouped GEMM scheduling; autotune only BLOCK_N/BLOCK_K
- Use sort-based permutation for coalesced memory access
- Scatter/gather kernels with BLOCK_D tiling over hidden dimension
