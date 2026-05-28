---
name: tritonify
description: >
  Optimize CUDA and Triton GPU kernels using agent-driven workflows, profiling-guided
  iteration, and battle-tested optimization patterns. Use when user wants to: optimize
  a kernel, write a Triton kernel, profile CUDA code, fuse operators, speed up LLM
  operations, generate GPU kernels, or benchmark kernel performance. Covers both
  Triton and CUDA with agent-based optimization loops inspired by MIT Kernel Design
  Agents, CudaForge, KernelSkill, and 36+ academic papers on AI-driven kernel
  optimization.
domain: software-development
composable: true
yields_to: [process]
---

# Tritonify — Agent-Driven GPU Kernel Optimization

> **Research basis:** 36 academic papers (2024-2026), MIT Kernel Design Agents,
> CudaForge, KernelSkill, AutoKernel, CODA, FlashAttention family, ThunderKittens,
> CUTLASS, Liger Kernel, and production kernel libraries. Every technique is
> grounded in published research and documented benchmarks.

---

## When to Use

- Writing new Triton or CUDA kernels
- Optimizing existing kernels (Triton or CUDA)
- Fusing multiple operators into single kernels
- Speeding up LLM training/inference operations
- **Convolution operations** (conv1d, conv2d, depthwise, grouped, transposed)
- **Fused conv patterns** (conv+activation, conv+BN, conv+residual)
- Profiling and diagnosing kernel bottlenecks
- Generating kernels from PyTorch reference implementations
- Benchmarking kernel performance against baselines

### Triggers

```
"optimize kernel", "write triton", "profile CUDA", "fuse operators",
"speed up LLM ops", "MoE kernel", "fused loss", "attention kernel",
"beat torch.compile", "kernel benchmark", "write CUDA kernel",
"convolution kernel", "conv2d triton", "depthwise conv", "im2col",
"fused conv relu", "conv batchnorm", "conv silu"
```

---

## Core Architecture: The Optimization Loop

The tritonify workflow follows the **Profile → Diagnose → Plan → Implement → Validate** loop,
derived from MIT Kernel Design Agents (KDA), CudaForge, and KernelSkill.

```
┌─────────────────────────────────────────────────────────┐
│                    TRITONIFY LOOP                        │
│                                                          │
│  1. TASK CONTRACT    Define objective, constraints,      │
│                      validation, promotion criteria      │
│                          │                               │
│  2. PROFILE          Nsight Compute / triton.testing     │
│                      Identify bottlenecks                │
│                          │                               │
│  3. DIAGNOSE         Map profiling data to known         │
│                      patterns (see Diagnosis Playbook)   │
│                          │                               │
│  4. PLAN             Prioritize by Amdahl's law          │
│                      Select optimization strategy        │
│                          │                               │
│  5. IMPLEMENT        One candidate at a time             │
│                      Small, testable changes             │
│                          │                               │
│  6. VALIDATE         Correctness check → Performance     │
│                      measure → Record evidence           │
│                          │                               │
│  7. DECIDE           Keep / Revise / Reject candidate    │
│                      Update candidates.jsonl             │
│                          │                               │
│  Loop back to 2 until promotion criteria met            │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Task Contract Pattern

Every optimization task MUST define a task contract before any code is written.

```markdown
## Task Contract
- **Objective:** [What to optimize — e.g., "fused RMSNorm + residual add"]
- **Input:** [Tensor shapes, dtypes, device]
- **Output:** [Expected output tensor]
- **Correctness:** [Tolerance — e.g., "atol=1e-3, rtol=1e-3 for fp16"]
- **Baseline:** [Current implementation + timing — e.g., "PyTorch eager: 45μs"]
- **Target:** [Performance goal — e.g., "<20μs or 2.25x speedup"]
- **Constraints:** [Language, APIs, dependencies, memory limits]
- **Validation command:** [How to prove correctness]
- **Evaluation command:** [How to measure performance]
- **Promotion criteria:** [What must be true to accept — e.g., "correct + 2x faster"]
```

---

## Phase 2: Profiling

### For CUDA Kernels: Nsight Compute (NCU)

```bash
# Build minimal harness (one kernel call, warmup + measure)
ncu --set full -o profile ./harness

# Key metrics to extract:
# - SM occupancy (% of theoretical max)
# - Warp occupancy
# - Tensor core utilization (%)
# - Memory throughput (% of peak)
# - Compute throughput (% of peak)
# - L2 cache hit rate
# - Stall reasons (long_scoreboard, wait, barrier, etc.)
# - Grid/block dimensions
# - Shared memory usage per CTA
# - Register usage per thread
```

### For Triton Kernels: Built-in Profiling

```python
import triton
import triton.testing as tt

# Basic benchmarking
ms = tt.do_bench(lambda: kernel[grid](...), rep=100)

# With torch profiler for detailed view
with torch.profiler.profile(activities=[
    torch.profiler.ProfilerActivity.CUDA,
    torch.profiler.ProfilerActivity.CPU,
]) as prof:
    kernel[grid](...)

print(prof.key_averages().table(sort_by="cuda_time_total"))
```

### Profiling Metrics Priority (by impact)

| Metric | What It Tells You | Fix Direction |
|--------|-------------------|---------------|
| Memory throughput < 60% peak | Memory-bound, poor access pattern | Coalescing, tiling, vectorized loads |
| Compute throughput < 60% peak | Compute-bound or idle SMs | Warp specialization, tensor cores |
| SM occupancy < 50% | Too many registers or shared mem | Reduce register pressure, smaller tiles |
| L2 hit rate < 70% | Cache thrashing | Adjust tile size, data layout |
| Tensor core util < 40% | Not using tensor cores or low utilization | Ensure aligned dims, use wmma/mma.sync |
| Long scoreboard stalls > 30% | Memory latency not hidden | More warps, prefetch, async copies |
| Tail effect > 20% | Uneven grid, partial waves | Adjust grid dims, handle edge cases |

---

## Phase 3: Diagnosis Playbook

### 14 Known Bottleneck Patterns (from ncu-report-skill)

| Pattern | Signal | Cause | Fix |
|---------|--------|-------|-----|
| **A: Small grid** | SM idle, low occupancy | Too few blocks | Increase parallelism, fuse operations |
| **B: Tail effect** | Partial waves, uneven blocks | Variable-length inputs | Pad, use persistent kernels |
| **C: Uncoalesced loads** | Low memory throughput | Strided access | Restructure data layout, use .contiguous() |
| **D: Bank conflicts** | Shared memory stalls | Bad swizzle patterns | Pad shared memory, swizzle access |
| **E: Latency-bound** | long_scoreboard > 30% | Insufficient warps | Increase warps, prefetch, async pipeline |
| **F: Compute-notensor** | High compute, low TC util | Using FP32 ALUs not TCs | Use wmma/mma.sync, ensure aligned dims |
| **G: Register spilling** | High local memory traffic | Too many live variables | Simplify code, reduce tile size |
| **H: Shared mem conflict** | Shared memory bottleneck | Bank conflicts in SMEM | Pad, swizzle, transpose |
| **I: Divergent branches** | Warp divergence | Conditionals per thread | Use predication, restructure logic |
| **J: Occupancy limiter** | Low SM occupancy | Registers/SMEM per CTA | Reduce register pressure, smaller tiles |
| **K: Grid imbalance** | Some SMs finish early | Non-uniform work | Persistent kernels, work-stealing |
| **L: Atomic contention** | Atomic operation bottleneck | Too many atomics | Reduce atomics, use shared mem reduction |
| **M: Pipeline bubbles** | No compute/memory overlap | Synchronous operations | Async copies, double buffering |
| **N: Cache thrashing** | Low L2 hit rate | Working set > cache | Tile size tuning, data reuse |

---

## Phase 4: Optimization Strategies

### Strategy Priority (by typical impact)

#### 1. Autotuning (Low-hanging fruit — up to 95x speedup on naive kernels)

```python
import triton
import triton.language as tl

@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 64}, num_warps=8, num_stages=3),
        triton.Config({'BLOCK_M': 256, 'BLOCK_N': 128, 'BLOCK_K': 32}, num_warps=8, num_stages=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 64, 'BLOCK_K': 64}, num_warps=4, num_stages=2),
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 64}, num_warps=4, num_stages=3),
        triton.Config({'BLOCK_M': 256, 'BLOCK_N': 64, 'BLOCK_K': 32}, num_warps=4, num_stages=4),
    ],
    key=['M', 'N', 'K'],  # Retune per input shape
)
@triton.jit
def matmul_kernel(A, B, C, M, N, K, stride_am, stride_ak, stride_bk, stride_bn, stride_cm, stride_cn):
    # ... kernel body
    pass
```

#### 2. Memory Coalescing (2-5x typical)

```python
# BAD: Strided access along reduction dim
@triton.jit
def bad_kernel(A, B, N, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    # A is row-major but we're loading along columns
    vals = tl.load(A + offs * N + col)  # Strided!

# GOOD: Contiguous access along innermost dim
@triton.jit
def good_kernel(A, B, N, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    vals = tl.load(A + row * N + offs)  # Contiguous!
```

#### 3. Tiling & Data Reuse (3-10x for GEMM-like ops)

```python
# 2D tiling with accumulator reuse
@triton.jit
def tiled_kernel(A, B, C, M, N, K, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    # Accumulator in registers
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)

    for k in range(0, K, BLOCK_K):
        # Load tiles — reused across iterations
        a = tl.load(A + (pid_m * BLOCK_M + tl.arange(0, BLOCK_M)[:, None]) * K +
                     k + tl.arange(0, BLOCK_K)[None, :])
        b = tl.load(B + (k + tl.arange(0, BLOCK_K)[:, None]) * N +
                     pid_n * BLOCK_N + tl.arange(0, BLOCK_N)[None, :])
        # Accumulate — keeps partial sums in registers
        acc += tl.dot(a, b)

    # Write once
    c_offs = (pid_m * BLOCK_M + tl.arange(0, BLOCK_M)[:, None]) * N + \
             pid_n * BLOCK_N + tl.arange(0, BLOCK_N)[None, :]
    tl.store(C + c_offs, acc)
```

#### 4. Operator Fusion (2-5x by eliminating memory round-trips)

```python
# Fused RMSNorm + Residual Add (saves 2 global memory round-trips)
@triton.jit
def fused_rmsnorm_residual(
    X, Residual, W, Out,
    stride_xm, stride_rm, stride_om,
    N, eps,
    BLOCK_N: tl.constexpr,
):
    row = tl.program_id(0)
    X += row * stride_xm
    Residual += row * stride_rm
    Out += row * stride_om

    # Load + residual add in one pass
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N
    x = tl.load(X + cols, mask=mask, other=0.0).to(tl.float32)
    r = tl.load(Residual + cols, mask=mask, other=0.0).to(tl.float32)
    x = x + r  # Fused residual

    # RMSNorm computation — all in registers
    mean_sq = tl.sum(x * x, axis=0) / N
    rrms = 1.0 / tl.sqrt(mean_sq + eps)

    # Load weight and apply
    w = tl.load(W + cols, mask=mask, other=1.0).to(tl.float32)
    out = (x * rrms * w).to(tl.load(Out + cols, mask=mask).dtype)  # Preserve input dtype

    tl.store(Out + cols, out, mask=mask)
```

#### 5. Warp Specialization (Hopper/Blackwell — 1.5x+ for latency-bound)

```python
# Producer-consumer warp specialization pattern
# Producer warps: TMA loads from global memory
# Consumer warps: Tensor core compute
# Requires: Hopper+ (sm_90+), async barrier coordination

# In CUDA (Triton doesn't support warp specialization natively):
__global__ void specialized_kernel() {
    if (threadIdx.x < 32) {
        // Producer warp: load data via TMA
        // ... async copy operations
    } else {
        // Consumer warps: compute via tensor cores
        // ... WGMMA operations
    }
}
```

#### 6. Mixed Precision (1.5-2x on Hopper with FP8)

```python
# FP8 matmul on Hopper (Triton supports fp8)
@triton.jit
def fp8_matmul(A, B, C, M, N, K, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr):
    # A and B in fp8e4m3 or fp8e5m2
    a = tl.load(A + ...)  # fp8
    b = tl.load(B + ...)  # fp8
    acc = tl.dot(a, b, out_dtype=tl.float32)  # Accumulate in fp32
    tl.store(C + ..., acc.to(tl.float16))  # Output in fp16
```

---

## Triton-Specific Best Practices

### Kernel Structure Template

```python
import triton
import triton.language as tl

@triton.autotune(configs=[...], key=['M', 'N'])
@triton.jit
def kernel(
    # Input/output pointers
    X, Y,
    # Strides (for non-contiguous tensors)
    stride_xm, stride_xn,
    stride_ym, stride_yn,
    # Dimensions
    M, N,
    # Compile-time constants (enables optimization)
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
):
    # 1. Program ID → tile coordinates
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    # 2. Compute offsets
    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)

    # 3. Masks for boundary handling
    mask_m = off_m < M
    mask_n = off_n < N
    mask = mask_m[:, None] & mask_n[None, :]

    # 4. Load, compute, store
    x = tl.load(X + off_m[:, None] * stride_xm + off_n[None, :] * stride_xn, mask=mask)
    y = compute(x)
    tl.store(Y + off_m[:, None] * stride_ym + off_n[None, :] * stride_yn, y, mask=mask)
```

### Common Triton Pitfalls

1. **Don't assume contiguous layout** — always pass strides explicitly
2. **Use `tl.constexpr` for tile sizes** — enables compile-time optimization
3. **Mask every load/store** — undefined behavior on OOB access
4. **Avoid in-kernel transposes** — prefer host-side `.contiguous()` if needed
5. **Keep power-of-2 tile sizes** — 64, 128, 256 for BLOCK_M/N; 32, 64 for BLOCK_K
6. **Don't over-tile** — register pressure kills occupancy; profile both
7. **`num_warps=4` is default** — try 4, 8, 16; more isn't always better
8. **`num_stages=2-4`** — pipeline depth for software prefetching

### Triton vs CUDA Decision Matrix

| Use Case | Language | Why |
|----------|----------|-----|
| Rapid prototyping | **Triton** | 10x less code |
| Cross-platform (NVIDIA+AMD) | **Triton** | Zero code changes |
| Standard patterns (matmul, attention, elementwise) | **Triton** | Block-level programming is natural fit |
| Architecture-specific features (TMA, WGMMA, DPX) | **CUDA** | Triton can't express these |
| Warp specialization (producer-consumer) | **CUDA** | Triton doesn't support it |
| Complex shared memory swizzling | **CUDA** | Need PTX-level control |
| Production inference (every TFLOP counts) | **CUDA** | 5-15% typical gap |
| LLM-generated kernels | **Triton** | Easier for models to generate correctly |
| MoE dispatch, FFT, sparse ops | **CUDA** | Complex memory patterns |

---

## CUDA-Specific Best Practices

### Key CUDA Optimization Patterns (from FlashAttention, ThunderKittens, CUTLASS)

#### 1. IO-Awareness (FlashAttention principle)
```cpp
// Minimize HBM↔SRAM transfers
// FlashAttention: tile attention so softmax normalization
// happens entirely in SRAM, never materializing full N×N matrix

// Key: each tile of Q loads once, iterates over all K/V tiles
// Total HBM reads: O(N²d²/M) vs O(N²d) for naive
// where M = SRAM size, d = head dim, N = seq len
```

#### 2. Async Pipeline (Hopper+)
```cpp
// Double-buffering with TMA + WGMMA
// Producer warps issue TMA loads for next tile
// Consumer warps compute on current tile
// Overlaps memory and compute

// Pipeline stages:
// Stage 0: TMA load tile[0]
// Stage 1: TMA load tile[1] + WGMMA compute tile[0]
// Stage 2: TMA load tile[2] + WGMMA compute tile[1]
// ...
```

#### 3. Shared Memory Swizzling
```cpp
// Eliminate bank conflicts for 100% shared memory utilization
// Pattern: XOR-based swizzle
// Layout: smem[row][col ^ (row % 8)]  // for 8-bank conflict resolution

// CUTLASS swizzle functors:
// Swizzle<3, 3, 3> for 128-bit access patterns
// Auto-handle bank conflict elimination
```

#### 4. Tensor Core Utilization
```cpp
// Ensure aligned dimensions for tensor core ops
// M, N, K must be multiples of 16 (FP16) or 32 (FP8)
// Use mma.sync.aligned.m16n8k16 for Hopper
// Use WGMMA for warp-group level operations

// Register layout must match tensor core requirements:
// A: [m/16][k/16][16][16] in registers
// B: [k/16][n/8][8][16] in registers
```

---

## Agent-Based Optimization Workflow

### Multi-Agent Pattern (from CudaForge, KernelSkill)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   CODER      │────▶│   JUDGE      │────▶│  PROFILER    │
│   Agent      │     │   Agent      │     │   (NCU)      │
│              │◀────│              │◀────│              │
│  Generate    │     │  Validate    │     │  Measure     │
│  kernels     │     │  correctness │     │  bottlenecks │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Candidate Lineage Tracking

```jsonl
{"name": "v1_baseline", "parent": null, "status": "baseline", "perf_us": 45.2, "notes": "PyTorch eager"}
{"name": "v2_triton_naive", "parent": "v1_baseline", "status": "rejected", "perf_us": 52.1, "notes": "No autotuning, worse than baseline"}
{"name": "v3_triton_autotuned", "parent": "v2_triton_naive", "status": "promoted", "perf_us": 18.4, "notes": "2.46x over baseline, BLOCK_M=128,BLOCK_N=256"}
{"name": "v4_fused_residual", "parent": "v3_triton_autotuned", "status": "promoted", "perf_us": 12.1, "notes": "Fused residual add, 3.74x over baseline"}
```

### Evidence-Based Promotion Rules

1. **Never promote without measurement** — every candidate must have timing data
2. **Correctness is binary** — pass/fail, no "close enough"
3. **Record exact numbers** — "faster" is not evidence, "18.4μs vs 45.2μs (2.46x)" is
4. **Compare against baseline** — always measure relative to the starting point
5. **Reject with reason** — never silently discard; record why

---

## Reference Implementations (Production Kernels)

### Key GitHub Repos to Study

| Repo | What to Learn |
|------|--------------|
| `Dao-AILab/flash-attention` | IO-aware attention, tiling patterns |
| `flashinfer-ai/flashinfer` | Serving-optimized attention kernels |
| `linkedin/Liger-Kernel` | Triton training kernels, fusion patterns |
| `unsloth` | Optimized Triton for fine-tuning |
| `pytorch/torchinductor` | Triton as default backend, code generation |
| `triton-lang/triton` | Official tutorials and examples |
| `thunderkittens` | CUDA-level perf with simpler abstractions |

### Liger Kernel Fusion Patterns (High-Value for LLMs)

- RMSNorm + residual → 1 kernel (saves 2 memory round-trips)
- Cross-entropy + softmax → 1 kernel (numerically stable, fused)
- SwiGLU activation → 1 kernel (gate + up + activation fused)
- LayerNorm + dropout + residual → 1 kernel
- Adam optimizer → 1 kernel (momentum + variance + update)

### Convolution Kernel Patterns (from Triton Gluon, PyTorch Inductor)

- **Conv2d forward** — Implicit GEMM + TMA im2col (Hopper/Blackwell) or tl.dot (all GPUs)
- **Conv2d dgrad** — Subproblem decomposition for stride > 1, split-K reduction
- **Conv2d wgrad** — grad_out^T @ im2col(input), tiled over Co × Ci × spatial
- **Depthwise conv1d** — Direct 3D tiling (NLC), element-wise multiply-accumulate
- **Fused conv + SiLU** — SiLU in epilogue: `result * tl.sigmoid(result)`
- **Fused conv + residual** — Load residual + conv output in epilogue
- **Fused conv + BN** — Pre-compute fused weights on host (eval mode)
- **Conv + bias + activation** — All in epilogue, no extra kernel launch

**Key APIs:**
- `TensorDescriptorIm2Col` — TMA im2col descriptor for NHWC input
- `tma.async_load_im2col(desc, coord, offsets, barrier, smem)` — Hardware im2col load
- `TensorDescriptor.from_tensor(weight_2d, block_shape, layout)` — TMA for weight
- `tcgen05_mma(a, b, acc, use_acc)` — Blackwell MMA
- `gl.warp_specialize(partitions, num_warps, ...)` — Warp specialization

**Critical patterns:**
- NHWC layout required (permute from NCHW before kernel)
- Weight reshape: [Co, R, S, Ci] → [Co, R*S*Ci] for 2D TMA
- Channel padding for TMA 16-byte alignment (Ci=3 → pad to 8)
- M-offset decomposition: flat M → (batch, out_y, out_x)
- Autotune key: (out_h, out_w, stride_h, stride_w) not full input shape

See `references/convolution-kernels.md` for complete code patterns.

---

## Benchmarking Protocol

### Correctness Verification (5-stage, from AutoKernel)

1. **Smoke test** — basic shapes work
2. **Shape sweeps** — test across batch sizes, seq lens, hidden dims
3. **Numerical tolerance** — atol=1e-3/rtol=1e-3 for fp16, atol=1e-5 for fp32
4. **Determinism** — same input → same output across runs
5. **Edge cases** — empty tensors, single element, max dimensions

### Performance Measurement

```python
import triton.testing as tt

# Warmup + measure
def benchmark(fn, rep=100, warmup=50):
    # Warmup
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()

    # Measure
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    times = []
    for _ in range(rep):
        start.record()
        fn()
        end.record()
        torch.cuda.synchronize()
        times.append(start.elapsed_time(end))

    return {
        'median_us': sorted(times)[len(times)//2] * 1000,
        'mean_us': sum(times) / len(times) * 1000,
        'min_us': min(times) * 1000,
        'p95_us': sorted(times)[int(0.95*len(times))] * 1000,
    }
```

### Speedup Calculation

```python
def speedup(baseline_us, optimized_us):
    return baseline_us / optimized_us

# Fast-p metric (from KernelBench)
def fast_p(correct, baseline_us, optimized_us, p=1.2):
    if not correct:
        return False
    return speedup(baseline_us, optimized_us) >= p
```

---

## Quick Reference: Common Operations

### Fused RMSNorm (Triton)

```python
@triton.jit
def rmsnorm_kernel(X, W, Out, stride_xm, stride_om, N, eps, BLOCK_N: tl.constexpr):
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N
    x = tl.load(X + row * stride_xm + cols, mask=mask, other=0.0).to(tl.float32)
    w = tl.load(W + cols, mask=mask, other=1.0).to(tl.float32)
    rms = tl.rsqrt(tl.sum(x * x, axis=0) / N + eps)
    tl.store(Out + row * stride_om + cols, (x * rms * w).to(tl.float16), mask=mask)
```

### Fused Softmax-CrossEntropy (Triton)

```python
@triton.jit
def cross_entropy_kernel(Logits, Targets, Loss, N, V, BLOCK_V: tl.constexpr):
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_V)
    mask = cols < V
    logits = tl.load(Logits + row * V + cols, mask=mask, other=-float('inf')).to(tl.float32)
    target = tl.load(Targets + row)

    # Online log-sum-exp
    max_val = tl.max(logits, axis=0)
    logits -= max_val
    sum_exp = tl.sum(tl.exp(logits), axis=0)
    log_sum_exp = tl.log(sum_exp) + max_val

    # Cross-entropy loss
    target_logit = tl.load(Logits + row * V + target)
    loss = log_sum_exp - target_logit
    tl.store(Loss + row, loss)
```

### Fused SwiGLU (Triton)

```python
@triton.jit
def swiglu_kernel(Gate, Up, Out, M, N, stride_gm, stride_um, stride_om, BLOCK_N: tl.constexpr):
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N
    gate = tl.load(Gate + row * stride_gm + cols, mask=mask, other=0.0).to(tl.float32)
    up = tl.load(Up + row * stride_um + cols, mask=mask, other=0.0).to(tl.float32)
    # SwiGLU: silu(gate) * up
    silu_gate = gate * tl.sigmoid(gate)
    out = silu_gate * up
    tl.store(Out + row * stride_om + cols, out.to(tl.float16), mask=mask)
```

---

## State of the Art (May 2026)

| System | Approach | Result |
|--------|----------|--------|
| **KernelSkill** | Multi-agent + skill memory | 100% success, 5.44x/2.82x/1.92x on KBL1/L2/L3 |
| **CUDA Agent** | Agentic RL | 100%/100%/92% faster than torch.compile |
| **DRTriton-7B** | RL + synthetic data | 92% speedup rate on KBL2 (vs 23% GPT-5.2) |
| **Makora/GPT-5-RL** | RL post-training | 97.4% solve rate, 2.12x over TorchInductor |
| **CODA** | GEMM-epilogue abstraction | High perf for non-attention Transformer ops |
| **CudaForge** | Multi-agent + NCU feedback | 97.6% correct, 1.68x, $0.30/kernel |

**Critical gap:** Even best agents only achieve 0.94x over production baselines (FastKernels finding).
Human expertise + agent assistance > pure agent optimization.

---

## Reference Files (load these for deep detail)

> **IMPORTANT**: This skill has reference files in the `references/` directory.
> Load them with `skill_view(name='tritonify', file_path='references/<file>')` for
> detailed code patterns, kernel implementations, and optimization techniques.

### Available References

| File | Contents |
|------|----------|
| `references/paper-survey.md` | 36 academic papers with abstracts, findings, GitHub repos |
| `references/moe-kernels.md` | MoE dispatch/compute kernels, 16 papers, code patterns |
| `references/loss-kernels.md` | Fused CE, KL, JSD, GRPO, DPO kernels from Liger-Kernel |
| `references/llm-optimizations.md` | Every LLM op: attention, norm, activation, RoPE, optimizer, KV cache |
| `references/profiling-guide.md` | NCU commands, metrics, Triton profiling, decision tree |
| `references/optimization-playbook.md` | Six-tier optimization framework from AutoKernel |
| `references/convolution-kernels.md` | Conv2d implicit GEMM, TMA im2col, depthwise, dgrad/wgrad, fused conv patterns |
| `templates/llm-kernels.py` | 6 ready-to-use Triton kernel templates |

### When to Load References

- **Optimizing MoE models** → Load `moe-kernels.md`
- **Writing loss functions** → Load `loss-kernels.md`
- **Convolution operations** → Load `convolution-kernels.md`
- **Any LLM operation** → Load `llm-optimizations.md`
- **Profiling/debugging** → Load `profiling-guide.md`
- **Starting optimization** → Load `optimization-playbook.md`
- **Need starter code** → Load `templates/llm-kernels.py`
- **Researching approaches** → Load `paper-survey.md`

---

## MIT Kernel Design Agents (KDA) Workflow

The KDA repo (`mit-han-lab/kernel-design-agents`) provides the core agent workflow pattern:

### Task Contract Pattern
Every optimization MUST define:
- Objective, inputs, outputs
- Correctness requirements (tolerance)
- Baseline timing + target timing
- Validation command + evaluation command
- Promotion criteria

### Candidate Lineage Tracking
```jsonl
{"name": "v1_baseline", "parent": null, "status": "baseline", "perf_us": 45.2}
{"name": "v2_triton_naive", "parent": "v1_baseline", "status": "rejected", "perf_us": 52.1}
{"name": "v3_autotuned", "parent": "v2_triton_naive", "status": "promoted", "perf_us": 18.4}
```

### Evidence-Based Promotion Rules
1. Never promote without measurement
2. Correctness is binary (pass/fail)
3. Record exact numbers, not "faster"
4. Compare against baseline
5. Reject with reason

### ncu-report-skill Analysis Dimensions
1. SM occupancy & wave structure
2. Thread-block balance (tail effect)
3. Instruction-level stall analysis
4. Tensor core utilization
5. SM utilization timeline
6. Memory access pattern & cache efficiency

---

## References

### Academic Papers (52+ total, key ones listed)

**Kernel Generation Agents:**
- CODA (2605.19269) — GEMM-epilogue abstraction for Transformer ops
- KernelBench (2502.10517) — Foundational benchmark, 250 tasks
- TritonForge (2512.09196) — Profiling-guided Triton optimization
- Dr. Kernel (2602.05885) — RL for Triton generation, TRLOO
- DRTriton (2603.21465) — Synthetic data + curriculum RL, 92% on KBL2
- KernelSkill (2603.10085) — Dual-level memory, 100% success rate
- CudaForge (2511.01884) — Multi-agent + NCU, $0.30/kernel
- CUDA Agent (2602.24286) — Agentic RL, SOTA on all KBL levels
- AgentKernelArena (2605.16819) — Generalization testing, 196 tasks
- FastKernels (2605.23215) — Production benchmark, 46 architectures

**MoE Kernels:**
- TritonMoE (2605.23911) — Pure Triton fused MoE dispatch
- FlashMoE (2506.04667) — Single persistent kernel, 9x GPU util
- MegaBlocks (2211.15841) — Block-sparse MoE, CUDA gold standard
- ScatterMoE (2403.08245) — ParallelLinear, no padding
- RaMP (2604.26039) — Routing-aware dispatch, 1.30x over vLLM
- UniEP (2604.19241) — ByteDance mega-kernel, EP comm+compute
- Hexcute (2504.16214) — Automated layout synthesis, 6.46x over Triton

**Attention & Core Ops:**
- FlashAttention (2205.14135) — IO-aware attention
- FlashAttention-3 (2407.08608) — Hopper: warp spec + FP8, 740 TFLOPs/s
- ThunderKittens (2410.20399) — Warp-level CUDA abstractions
- Liger Kernel (2410.10989) — Production Triton training kernels
- Cut Cross-Entropy (2411.09009) — CE without materializing logits

**CUDA Optimization:**
- CUDA-L2 (2512.02551) — LLM+RL for HGEMM, surpasses cuBLAS by 19.2%
- CUDA-LLM/FSR (2506.09092) — Generated kernels outperform human code 179x
- OptiML (2602.12305) — MCTS over LLM edits with NCU profiling
- EvoEngineer (2510.03760) — 91 real-world CUDA kernels, 2.72x median

### Key GitHub Repos

**Kernel Generation:**
- `mit-han-lab/kernel-design-agents` — KDA workflow
- `OptimAI-Lab/CudaForge` — Multi-agent CUDA generation
- `0satan0/KernelMem` — KernelSkill
- `RightNow-AI/autokernel` — AutoKernel, 18 starter kernels
- `hkust-nlp/KernelGYM` — Dr. Kernel environment
- `AI9Stars/AutoTriton` — RL-trained Triton model
- `HanGuo97/coda-kernels` — CODA kernels

**Production Kernels:**
- `linkedin/Liger-Kernel` — Triton training kernels (CE, RMSNorm, SwiGLU, RoPE, Adam)
- `unslothai/unsloth` — Optimized Triton for fine-tuning
- `Dao-AILab/flash-attention` — FlashAttention family
- `flashinfer-ai/flashinfer` — Serving-optimized attention
- `vllm-project/vllm` — PagedAttention, fused MoE, sampling
- `sgl-project/sglang` — Radix attention, speculative decoding
- `HazyResearch/thunderkittens` — CUDA-level perf with simpler abstractions

**MoE:**
- `bassrehab/triton-kernels` — TritonMoE cross-platform
- `osayamenja/FlashMoE` — Persistent kernel MoE
- `stanford-futuredata/megablocks` — Block-sparse MoE
- `shawntan/scattermoe` — ParallelLinear MoE
- `rbgo/alpha-moe` — JIT-tuned MoE
- `Aleph-Alpha/Alpha-MoE` — JIT-tuned MoE

**Convolution:**
- `triton-lang/triton/python/examples/gluon/02-conv-*.py` — Production conv2d (fprop/dgrad/wgrad)
- `triton-lang/triton/python/tutorials/gluon/13-conv-im2col.py` — TMA im2col tutorial
- `pytorch/pytorch/torch/_inductor/kernel/conv.py` — Inductor conv templates
- `pytorch/pytorch/torch/_inductor/kernel/templates/triton_depthwise_conv.py.jinja` — Depthwise

**Benchmarks:**
- `thunlp/TritonBench` — 184 Triton operators
- `ScalingIntelligence/KernelBench` — 250 PyTorch workloads
- `Snowflake-AI-Research/fastkernels` — Production benchmark
