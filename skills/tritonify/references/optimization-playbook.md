# Six-Tier Optimization Playbook (from AutoKernel/RightNow-AI)

## Tier 1: Baseline (Naive Implementation)
**Goal:** Get correctness first, performance later.
```python
@triton.jit
def naive_kernel(X, Y, M, N, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    mask = (off_m[:, None] < M) & (off_n[None, :] < N)
    x = tl.load(X + off_m[:, None] * N + off_n[None, :], mask=mask)
    tl.store(Y + off_m[:, None] * N + off_n[None, :], x, mask=mask)
```
**Verify:** Correctness against PyTorch reference.

---

## Tier 2: Autotuning
**Goal:** Find optimal block sizes and launch parameters.
```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256}, num_warps=8, num_stages=3),
        triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128}, num_warps=8, num_stages=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 64}, num_warps=4, num_stages=2),
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128}, num_warps=4, num_stages=3),
    ],
    key=['M', 'N'],
)
@triton.jit
def autotuned_kernel(X, Y, M, N, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    # ... same body as naive
```
**Expected improvement:** 2-10x over naive, up to 95x in extreme cases.

---

## Tier 3: Memory Optimization
**Goal:** Eliminate memory bottlenecks.
- Coalesced access (contiguous along innermost dim)
- Vectorized loads (`tl.load` with 4-element vectors)
- Minimize intermediate memory writes
- Use `.contiguous()` at host level if needed

```python
# Vectorized load (4 elements per load instruction)
@triton.jit
def vectorized_kernel(X, Y, N, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    # Load 4 elements at once
    x0 = tl.load(X + offs, mask=offs < N)
    x1 = tl.load(X + offs + BLOCK, mask=(offs + BLOCK) < N)
    # ... process and store
```
**Expected improvement:** 1.5-3x over autotuned baseline.

---

## Tier 4: Operator Fusion
**Goal:** Eliminate memory round-trips between operations.
```python
# Fuse elementwise ops: read once, compute multiple ops, write once
@triton.jit
def fused_gelu_residual(X, Residual, Y, M, N, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    mask = (off_m[:, None] < M) & (off_n[None, :] < N)

    # Single read
    x = tl.load(X + off_m[:, None] * N + off_n[None, :], mask=mask).to(tl.float32)
    r = tl.load(Residual + off_m[:, None] * N + off_n[None, :], mask=mask).to(tl.float32)

    # GELU + residual in registers
    x = x + r
    # GELU approximation: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
    inner = 0.7978845608 * (x + 0.044715 * x * x * x)
    gelu = 0.5 * x * (1.0 + tl.where(inner > 0, 1.0, -1.0) * tl.minimum(tl.exp(2.0 * inner) - 1.0, 1.0))

    # Single write
    tl.store(Y + off_m[:, None] * N + off_n[None, :], gelu.to(tl.float16), mask=mask)
```
**Expected improvement:** 1.5-4x for fused ops (eliminates 2+ memory round-trips).

---

## Tier 5: Algorithmic Optimization
**Goal:** Change the algorithm to reduce compute or memory.
- Online softmax (FlashAttention pattern)
- Tiling with accumulator reuse
- Numerical tricks (log-space computation, fused operations)

```python
# Online softmax (avoids materializing full attention matrix)
@triton.jit
def online_softmax_kernel(Q, K, V, Out, N, D, BLOCK_N: tl.constexpr, BLOCK_D: tl.constexpr):
    # For each query, iterate over K/V tiles
    # Maintain running max and sum-exp for numerical stability
    m_prev = tl.full((BLOCK_D,), value=-float('inf'), dtype=tl.float32)
    l_prev = tl.zeros((BLOCK_D,), dtype=tl.float32)
    acc = tl.zeros((BLOCK_D,), dtype=tl.float32)

    for k_start in range(0, N, BLOCK_N):
        k_offs = k_start + tl.arange(0, BLOCK_N)
        k_mask = k_offs < N
        # Compute attention scores for this tile
        scores = tl.dot(q, tl.trans(k_tile))  # [1, BLOCK_N]
        # Update running statistics
        m_new = tl.maximum(m_prev, tl.max(scores, axis=1))
        alpha = tl.exp(m_prev - m_new)
        beta = tl.exp(scores - m_new)
        l_new = alpha * l_prev + tl.sum(beta, axis=1)
        acc = alpha * acc + tl.dot(beta, v_tile)
        m_prev = m_new
        l_prev = l_new

    out = acc / l_prev
```
**Expected improvement:** 2-5x for attention operations.

---

## Tier 6: Architecture-Specific Optimization
**Goal:** Exploit hardware-specific features.
- Warp specialization (Hopper+)
- TMA (Tensor Memory Accelerator for async copies)
- WGMMA (Warp Group Matrix Multiply Accumulate)
- FP8 tensor cores
- Distributed shared memory (Blackwell)

**Note:** These require CUDA, not Triton. Triton abstracts them away at ~5-15% perf cost.

```cpp
// Warp specialization pattern (Hopper CUDA)
__global__ void warp_specialized_kernel() {
    // Producer warps (threads 0-31): TMA loads
    if (threadIdx.x < 32) {
        // Issue async TMA copies
        uint64_t mbar;
        asm volatile("mbarrier.init.shared.b64 %0, 1;" : "=l"(mbar));
        // ... TMA load with barrier
    }
    // Consumer warps (threads 32+): WGMMA compute
    else {
        // Wait on barrier, then WGMMA
        // ... tensor core compute
    }
}
```
**Expected improvement:** 1.2-1.5x over well-optimized non-specialized code.

---

## Optimization Checklist

After each tier, verify:
- [ ] Correctness: atol < 1e-3 (fp16) or atol < 1e-5 (fp32)
- [ ] Performance: measured with proper warmup (10+ iterations)
- [ ] Determinism: same input → same output across runs
- [ ] Edge cases: handles non-aligned dimensions gracefully

Stop optimizing when:
- You've hit >80% of theoretical peak bandwidth (for memory-bound)
- You've hit >70% of theoretical peak FLOPS (for compute-bound)
- Further changes yield <5% improvement
- You've tried 3-4 rounds without improvement (diminishing returns pattern)
