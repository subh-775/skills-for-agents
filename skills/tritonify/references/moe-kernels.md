# MoE Kernel Optimization Reference

## Key Papers

| Paper | arXiv | Innovation | Repo |
|-------|-------|-----------|------|
| TritonMoE | 2605.23911 | Pure Triton fused MoE dispatch, 89-131% of Megablocks | bassrehab/triton-kernels |
| FlashMoE | 2506.04667 | Single persistent kernel, 9x GPU util, 6x latency | osayamenja/FlashMoE |
| MegaBlocks | 2211.15841 | Block-sparse MoE, CUDA gold standard | stanford-futuredata/megablocks |
| ScatterMoE | 2403.08245 | ParallelLinear, no padding, 53.6% memory of Megablocks | shawntan/scattermoe |
| RaMP | 2604.26039 | Routing-aware dispatch, 1.30x over vLLM Triton | - |
| UniEP | 2604.19241 | ByteDance mega-kernel, EP comm+compute fusion | - |
| Hexcute | 2504.16214 | Automated layout synthesis, 6.46x over Triton on MoE | - |
| ARGUS | 2604.18616 | LLM agent for MoE kernels, 99-104% of hand-optimized | - |

## Production Implementations

| System | Backend | Notes |
|--------|---------|-------|
| vLLM Fused MoE | Triton FP8 | ~2K configs, static dispatch |
| DeepGEMM | CUDA FP8 JIT | DeepSeek, fixed bm=128 |
| Alpha-MoE | CUDA C++ JIT | Aleph Alpha, 160 configs |
| FlashInfer | CUTLASS | Internal autotuning |

## Model Configurations

| Model | Experts | Top-k | d_model | d_ffn | Gating |
|-------|---------|-------|---------|-------|--------|
| Mixtral-8x7B | 8 | 2 | 4096 | 14336 | Softmax |
| Mixtral-8x22B | 8 | 2 | 6144 | 16384 | Softmax |
| DeepSeek-V2 | 160 | 6 | 5120 | 1536 | Sigmoid |
| DeepSeek-V3 | 256 | 8 | 7168 | 2048 | Sigmoid |
| Qwen2-MoE-57B | 64 | 4 | 3584 | 2560 | Softmax |
| Qwen3 | 128 | 8 | - | - | - |
| OLMoE | 64 | 8 | 2048 | 2048 | Softmax |

## Critical Insight: Routing Skew
Real MoE routing is deeply skewed (β≈0.5, only 8-14% experts active). Static dispatch tuned at β=1.0 leaves 10-70% throughput unrealized. Use routing-aware dispatch when possible.

## Kernel Design Patterns

### Pattern 1: Block-Scheduled Grouped GEMM (TritonMoE)
```python
# Build schedule: map program blocks to (expert_id, token_offset) pairs
expert_offsets = compute_expert_offsets(token_assignments)  # E+1 entries
blocks = []
for e in range(E):
    n_e = expert_offsets[e+1] - expert_offsets[e]
    for b in range(ceil(n_e / BLOCK_M)):
        blocks.append((e, b * BLOCK_M))

# Each Triton program block:
# - Loads expert e's weight from flattened E*N x K tensor
# - Processes BLOCK_M token rows from expert-contiguous input
# CRITICAL: BLOCK_M must be fixed (not autotuned) to match schedule
```

### Pattern 2: Fused Gate+Up Projection (SwiGLU)
```python
# Single kernel pass for both gate and up projections
for k in range(0, K, BLOCK_K):
    A = load_input_tile(m:m+M, k:k+K)  # from L2 cache
    B_gate = load_weight_tile(W_gate, e, n:n+N, k:k+K)
    B_up = load_weight_tile(W_up, e, n:n+N, k:k+K)
    acc_gate += A @ B_gate
    acc_up += A @ B_up

# SiLU in FP32 registers - NO write to HBM between phases
intermediate = SiLU(acc_gate) * acc_up  # single write
# Saves: 35% memory traffic reduction
```

### Pattern 3: Router Kernel (Stable Softmax + Top-k)
```python
# Manual stable softmax - tl.softmax doesn't subtract max!
scores = W_r @ x
scores_max = tl.max(scores, axis=0)
scores = tl.exp(scores - scores_max)
scores = scores / tl.sum(scores, axis=0)

# Top-k via iterative argmax with -1.0 masking (NOT 0.0!)
selected_mask = tl.full([E], -1.0, dtype=float32)  # -1.0 prevents re-selection
for i in range(k):
    idx = tl.argmax(scores + selected_mask, axis=0)
    selected_mask[idx] = -1.0
```

### Pattern 4: 3-Phase Fused MoE (CUDA)
```
Phase 1 (up-proj): TMA load weights → WGMMA matmul
Phase 2 (activation): SwiGLU in registers, NO HBM write
Phase 3 (down-proj): WGMMA matmul → scatter via atomic add
```

### Pattern 5: Routing-Aware Dispatch (RaMP)
```python
# Performance-region variables
rho = N * K / (ttn * tile_k)  # compute density per CTA
lam = ceil(N / ttn)            # L2 pressure
omega = grid(c, routing) / SM_COUNT  # wave utilization
kappa = K / tile_k             # K-reduction depth

# Decision thresholds
GROUP_M needed when: lam * kappa > 1440
Split-K needed when: kappa >= 48 and omega < 0.2
```

## GitHub Repos
- `bassrehab/triton-kernels` — TritonMoE cross-platform
- `osayamenja/FlashMoE` — Persistent kernel MoE
- `stanford-futuredata/megablocks` — Block-sparse MoE
- `shawntan/scattermoe` — ParallelLinear MoE
- `deepseek-ai/DeepGEMM` — FP8 grouped GEMM
- `Aleph-Alpha/Alpha-MoE` — JIT-tuned MoE
- `vllm-project/vllm` — Production fused MoE serving
- `perplexityai/pplx-garden` — RDMA MoE dispatch
- `IST-DASLab/qmoe` — Compressed MoE inference
