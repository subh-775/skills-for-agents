# Comprehensive LLM Kernel Optimization Reference

Every fused kernel optimization for transformer operations, organized by operation type.

---

## 1. NORMALIZATION

### RMSNorm (Llama, Qwen, Mistral, etc.)
**Fused operations**: RMSNorm + residual add, RMSNorm + dropout + residual

```python
@triton.jit
def fused_rmsnorm_residual(X, Residual, W, Out, N, eps, BLOCK_N: tl.constexpr):
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N
    # Single read: fuse residual add
    x = tl.load(X + row * N + cols, mask=mask).to(tl.float32) + \
        tl.load(Residual + row * N + cols, mask=mask).to(tl.float32)
    # RMSNorm in registers
    rrms = tl.rsqrt(tl.sum(x * x, axis=0) / N + eps)
    w = tl.load(W + cols, mask=mask).to(tl.float32)
    tl.store(Out + row * N + cols, (x * rrms * w).to(tl.float16), mask=mask)
```

**Savings**: 2 memory round-trips (residual read + write eliminated)
**Source**: Liger-Kernel `rms_norm.py`, Unsloth

### LayerNorm (GPT-2, BERT, etc.)
**Fused**: LayerNorm + residual + dropout
**Source**: Liger-Kernel `layer_norm.py`

---

## 2. ACTIVATIONS

### SwiGLU (Llama, Qwen, Mistral, Mixtral)
**Fused**: gate_proj + up_proj + SiLU activation in single kernel

```python
@triton.jit
def swiglu_kernel(Gate, Up, Out, M, N, BLOCK_N: tl.constexpr):
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N
    gate = tl.load(Gate + row * N + cols, mask=mask).to(tl.float32)
    up = tl.load(Up + row * N + cols, mask=mask).to(tl.float32)
    # SwiGLU: silu(gate) * up
    out = (gate * tl.sigmoid(gate)) * up
    tl.store(Out + row * N + cols, out.to(tl.float16), mask=mask)
```

**Savings**: Eliminates intermediate gate_out buffer
**Source**: Liger-Kernel `swiglu.py`

### GELU (GPT-2, BERT)
**Fused**: linear + GELU
**Approximation**: `0.5 * x * (1 + tanh(0.7978845608 * (x + 0.044715 * x^3)))`

### GeGLU
**Fused**: gate + up + GELU activation
**Source**: Liger-Kernel `geglu.py`

---

## 3. ATTENTION

### FlashAttention Family
| Version | arXiv | Key Innovation | Perf |
|---------|-------|---------------|------|
| FlashAttention-1 | 2205.14135 | IO-aware tiling, online softmax | 15% BERT, 3x GPT-2 |
| FlashAttention-2 | 2307.08691 | Better parallelism, 2x over FA1 | 72% A100 util |
| FlashAttention-3 | 2407.08608 | Hopper: warp spec + FP8 | 740 TFLOPS, 75% H100 |

**Core pattern**: Tile Q, iterate over K/V tiles, maintain online softmax statistics in SRAM.
Never materializes full N×N attention matrix.

### PagedAttention (vLLM)
**Key**: KV cache stored in non-contiguous pages, paged kernel handles gather
**Source**: vLLM `attention/`

### FlashInfer
**Key**: Serving-optimized attention, ragged batch, paged KV
**Source**: flashinfer-ai/flashinfer

### Multi-Query / Grouped-Query Attention
**Key**: Repeat KV heads in kernel, not in memory. Use `head_idx // n_kv_heads` for KV indexing.

---

## 4. POSITIONAL ENCODING

### RoPE (Rotary Position Embedding)
**Fused**: Apply RoPE in attention kernel or as fused pre-attention op

```python
@triton.jit
def fused_rope(Q, Cos, Sin, seq_len, head_dim, BLOCK_D: tl.constexpr):
    row = tl.program_id(0)
    d = tl.arange(0, BLOCK_D)
    half = BLOCK_D // 2
    # Split into pairs
    q_even = tl.load(Q + row * head_dim + d, mask=d < half)
    q_odd = tl.load(Q + row * head_dim + d + half, mask=d < half)
    cos = tl.load(Cos + row * head_dim + d, mask=d < half)
    sin = tl.load(Sin + row * head_dim + d, mask=d < half)
    # Rotate
    out_even = q_even * cos - q_odd * sin
    out_odd = q_even * sin + q_odd * cos
    tl.store(Q + row * head_dim + d, out_even, mask=d < half)
    tl.store(Q + row * head_dim + d + half, out_odd, mask=d < half)
```

**Source**: Unsloth, Liger-Kernel `rope.py`

---

## 5. LINEAR PROJECTIONS

### Fused QKV Projection
**Key**: Single matmul for Q, K, V projections (stacked weight matrix)
```python
# Instead of 3 separate matmuls:
qkv = x @ W_qkv  # [B, T, 3*hidden_dim]
q, k, v = qkv.split([hidden_dim, hidden_dim, hidden_dim], dim=-1)
```

### Fused Output Projection + Residual
**Key**: Combine output projection with residual add in single kernel

### Fused Linear + Activation
**Key**: GEMM + GELU/SwiGLU in single pass (avoids writing intermediate to HBM)
**Source**: Liger-Kernel `fused_linear_cross_entropy.py` pattern

---

## 6. EMBEDDING

### Fused Embedding + Gather
**Key**: Embedding lookup with fused operations (e.g., position add)
```python
@triton.jit
def fused_embedding(Emb, PosEmb, TokenIds, Out, BLOCK_D: tl.constexpr):
    row = tl.program_id(0)
    d = tl.arange(0, BLOCK_D)
    token_id = tl.load(TokenIds + row)
    emb = tl.load(Emb + token_id * BLOCK_D + d)
    pos = tl.load(PosEmb + row * BLOCK_D + d)
    tl.store(Out + row * BLOCK_D + d, emb + pos)
```

---

## 7. OPTIMIZER

### Fused Adam/AdamW
**Key**: Single kernel for momentum + variance + weight update
```python
@triton.jit
def fused_adam(Params, Grads, M, V, lr, beta1, beta2, eps, step, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    p = tl.load(Params + offs)
    g = tl.load(Grads + offs)
    m = tl.load(M + offs)
    v = tl.load(V + offs)
    # Update moments
    m_new = beta1 * m + (1 - beta1) * g
    v_new = beta2 * v + (1 - beta2) * g * g
    # Bias correction
    m_hat = m_new / (1 - beta1 ** step)
    v_hat = v_new / (1 - beta2 ** step)
    # Weight update
    p_new = p - lr * m_hat / (tl.sqrt(v_hat) + eps)
    tl.store(Params + offs, p_new)
    tl.store(M + offs, m_new)
    tl.store(V + offs, v_new)
```

**Source**: Liger-Kernel, Unsloth

---

## 8. KV CACHE

### Paged KV Cache
**Key**: Non-contiguous page table, gather in kernel
**Source**: vLLM, SGLang, FlashInfer

### KV Cache Quantization
**Key**: INT8/FP8 quantization of KV cache for memory savings
**Source**: vLLM, SqueezeLLM

---

## 9. SAMPLING

### Fused Top-k/Top-p Sampling
**Key**: Sort + threshold + sample in single kernel
**Source**: vLLM, SGLang

### Speculative Decoding
**Key**: Draft model generates candidates, verify in parallel
**Source**: SGLang, Medusa

---

## 10. COMMUNICATION

### Fused AllReduce + Residual
**Key**: Overlap NCCL allreduce with residual add
**Source**: Megatron-LM, DeepSpeed

### Expert Parallel Dispatch/Combine
**Key**: Fused dispatch + compute + combine
**Source**: FlashMoE, UniEP, NCCL-EP

---

## Production Kernel Libraries (Reference)

| Library | What It Fuses | Language | Repo |
|---------|--------------|---------|------|
| Liger-Kernel | RMSNorm, SwiGLU, CE, RoPE, KL, JSD, GRPO, Adam | Triton | linkedin/Liger-Kernel |
| Unsloth | CE, RMSNorm, RoPE, optimizer | Triton | unslothai/unsloth |
| FlashInfer | Attention, paged KV, ragged batch | CUDA/Triton | flashinfer-ai/flashinfer |
| vLLM | PagedAttention, fused MoE, sampling | CUDA/Triton | vllm-project/vllm |
| SGLang | Attention, radix attention, sampling | CUDA/Triton | sgl-project/sglang |
| xformers | Attention, memory-efficient ops | CUDA | facebookresearch/xformers |
| torchtune | Training kernels | Triton | pytorch/torchtune |
| ThunderKittens | GEMM, attention, SSM | CUDA | HazyResearch/thunderkittens |

---

## Optimization Priority (by typical impact)

1. **Attention** (FlashAttention) — 3-10x for long sequences
2. **Loss function** (fused CE) — 2-5x, massive memory savings
3. **MoE dispatch** (fused MoE) — 2-4x for MoE models
4. **Normalization** (fused RMSNorm+residual) — 1.5-2x
5. **Activation** (fused SwiGLU) — 1.3-1.8x
6. **Optimizer** (fused Adam) — 1.2-1.5x
7. **RoPE** (fused) — 1.1-1.3x
8. **Embedding** (fused) — 1.1-1.2x
