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

## Liger-Kernel First Policy (MANDATORY)

**Before writing ANY custom Triton kernel, check if Liger-Kernel already provides it.**

Liger-Kernel (`linkedin/Liger-Kernel`) is a production-tested library of fused Triton kernels for LLM training. It covers the most common operations — writing your own is wasted effort unless Liger doesn't cover your case.

### What Liger-Kernel Provides (DO NOT reinvent)

| Operation | Liger Module | What it fuses |
|-----------|-------------|---------------|
| RMSNorm | `liger_kernel.ops.rms_norm` | Forward + backward, in-place |
| LayerNorm | `liger_kernel.ops.layer_norm` | Forward + backward |
| SwiGLU | `liger_kernel.ops.swiglu` | Gate + up + SiLU fused |
| GeGLU | `liger_kernel.ops.geglu` | Gate + up + GELU fused |
| Cross-Entropy | `liger_kernel.ops.cross_entropy` | Online softmax + NLL + backward, in-place |
| Fused Linear+CE | `liger_kernel.ops.fused_linear_cross_entropy` | Avoids materializing BT×V logits |
| KL Divergence | `liger_kernel.ops.kl_div` | Fused KL with chunking |
| JSD | `liger_kernel.ops.jsd` | Fused Jensen-Shannon divergence |
| TVD | `liger_kernel.ops.tvd` | Fused Total Variation distance |
| GRPO Loss | `liger_kernel.ops.grpo_loss` | Selective log-softmax, PPO clipping, KL penalty |
| DPO Loss | `liger_kernel.ops.dpo_loss` | Chunked preference loss |
| SimPO/CPO/ORPO | `liger_kernel.ops.{simpo,cpo,orpo}_loss` | Chunked preference variants |
| RoPE | `liger_kernel.ops.rope` | Rotary position embedding |
| SparseMax | `liger_kernel.ops.sparsemax` | Sparsemax activation |
| CrossEntropy+Softcap | `liger_kernel.ops.cross_entropy` | Supports softcapping for Gemma2 |
| Hinge Loss | `liger_kernel.ops.hinge_loss` | Fused hinge |

### Decision Flow

```
Need an operation?
  │
  ├─ Is it in the table above?
  │   ├─ YES → Use liger_kernel.ops.<op>. Done.
  │   └─ NO  → Continue below
  │
  ├─ Is it a standard LLM op (norm, activation, loss)?
  │   ├─ Check liger_kernel/ops/ source — might be unlisted
  │   └─ If not there → Write custom Triton kernel
  │
  ├─ Is it a convolution op?
  │   └─ Use convolution-kernels.md reference (Triton Gluon / Inductor patterns)
  │
  ├─ Is it an MoE op?
  │   └─ Use moe-kernels.md reference
  │
  └─ Is it something novel / architecture-specific?
      └─ Write custom kernel using the optimization loop below
```

### How to Use Liger-Kernel

```python
# Installation
# pip install liger-kernel

# Drop-in replacement for PyTorch modules:
from liger_kernel.transformers import LigerRMSNorm, LigerSwiGLUMLP, LigerCrossEntropyLoss

# Or monkey-patch a HuggingFace model:
from liger_kernel.transformers import monkey_patch
monkey_patch(model)  # Replaces RMSNorm, SwiGLU, CE with fused Triton versions

# Or use the ops directly:
from liger_kernel.ops.rms_norm import liger_rms_norm
from liger_kernel.ops.cross_entropy import liger_cross_entropy
from liger_kernel.ops.fused_linear_cross_entropy import liger_fused_linear_cross_entropy
```

### When to Write Custom Kernels Instead

Only write custom Triton when:
1. **Liger doesn't cover it** — conv ops, attention variants, custom activations, MoE dispatch
2. **You need architecture-specific fusion** — e.g., fusing conv+SiLU+residual for BiBo
3. **You need different tiling/blocking** — Liger's defaults don't match your shapes
4. **You're doing kernel research** — ablations, new algorithms, benchmarking

**Never write a standalone RMSNorm, SwiGLU, cross-entropy, or RoPE kernel when Liger provides one.**

### Autograd Safety — CRITICAL (from SEV1 incident 2026-05-29)

> **HARD RULES — violation of ANY of these is a P0 bug:**
>
> 1. **NEVER write into `torch.empty()` via raw Triton kernel without wrapping in `torch.autograd.Function`.** `torch.empty()` creates a leaf tensor — autograd sees no connection between input and output. Gradients stop dead.
>
> 2. **NEVER use `register_buffer()` for tensors that participate in computation that needs gradients.** Buffers are excluded from `parameters()` and `requires_grad=False` by default. Using a buffer in `F.linear` means the weight never updates.
>
> 3. **NEVER promote a kernel based on "backward doesn't crash" alone.** Backward can "succeed" while producing zero gradients for entire subgraphs. The loss still gets a gradient from working components, so `.backward()` completes silently.
>
> 4. **ALWAYS verify gradient equivalence before promoting any training kernel.** Compare weight gradients between patched and unpatched models. Fail if any param has zero grad, `grad=None`, or max diff > 1e-3 (fp32) / 5e-2 (fp16).

#### The Two Gradient Killers (BiBo SEV1 — May 2026)

**Killer #1: `register_buffer` — Dead Weight Copy**
```python
# BROKEN: buffer = no gradients, layers frozen forever
fused_w = torch.cat([module.gate_proj.weight.data, module.up_proj.weight.data], dim=0)
module.register_buffer('_fused_gate_up_weight', fused_w)  # ← DEAD COPY
gate_up = F.linear(x_2d, self._fused_gate_up_weight)      # ← gate_proj.grad = None

# FIXED: concatenate LIVE parameters on every forward
fused_weight = torch.cat([self.gate_proj.weight, self.up_proj.weight], dim=0)
gate_up = F.linear(x_2d, fused_weight)  # ← autograd traces through both weights
```

**Killer #2: `torch.empty()` — Severs Autograd Graph**
```python
# BROKEN: Triton writes into fresh tensor — no autograd history
def triton_fused_glu_activation(gate_up, act_type):
    out = torch.empty(M, I, device=gate_up.device, dtype=gate_up.dtype)  # ← LEAF
    _fused_glu_act_kernel[grid](gate_up, out, ...)  # ← kernel fills it
    return out  # ← autograd: "this has no grad_fn"

# FIXED: wrap in torch.autograd.Function
class _TritonFusedGLUFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, gate_up, act_type):
        ctx.save_for_backward(gate_up)
        ctx.act_type = act_type
        M, I2 = gate_up.shape
        out = torch.empty(M, I2 // 2, device=gate_up.device, dtype=gate_up.dtype)
        _fused_glu_act_kernel[grid](gate_up, out, ...)  # Triton for speed
        return out

    @staticmethod
    def backward(ctx, grad_output):
        gate_up, = ctx.saved_tensors
        gate, up = gate_up[:, :I], gate_up[:, I:]
        # Recompute activation grads via PyTorch ops (correct by construction)
        if ctx.act_type == 'silu':
            sig = torch.sigmoid(gate)
            grad_gate = grad_output * (sig + gate * sig * (1 - sig)) * up
            grad_up = grad_output * (gate * sig)
        # ... other activation types
        return torch.cat([grad_gate, grad_up], dim=-1), None
```

#### Decision Tree: Do I Need `torch.autograd.Function`?

```
Does the kernel output participate in training (backward pass needed)?
├─ NO (inference-only) → No wrapper needed. Raw kernel is fine.
└─ YES →
    ├─ Is the output tensor created by autograd-traced ops?
    │   (e.g., output of F.linear, torch.mm, +, *, etc.)
    │   ├─ YES → Autograd CAN trace through. Forward-only is fine.
    │   └─ NO → Is the output from torch.empty(), torch.zeros(),
    │           torch.ones(), or any non-traced allocation?
    │           ├─ YES → MUST wrap in torch.autograd.Function
    │           └─ UNSURE → MUST wrap in torch.autograd.Function
    │
    └─ Does any input come from register_buffer()?
        ├─ YES → MUST convert to live parameter recomputation
        └─ NO → Check above decision tree
```

**"Forward-only is fine" — WHEN IT ACTUALLY IS:**
- Inference workloads (no backward at all)
- The output tensor is produced by autograd-traced ops (e.g., you call `F.linear` then Triton post-processes the result of that traced op)
- The kernel is a pure elementwise transform on a tensor that already has `grad_fn`

**"Forward-only is fine" — WHEN IT IS NOT:**
- The kernel writes into `torch.empty()` or any pre-allocated leaf tensor
- Any input comes from `register_buffer()`
- The kernel replaces a PyTorch op that has its own backward (e.g., replacing `F.silu` with a Triton silu)
- You are unsure → default to wrapping in `torch.autograd.Function`

#### Backward Pass Decision

**When you SHOULD write a fused backward:**
- Training workloads where backward pass is the bottleneck (>40% of step time)
- When the backward re-materializes large intermediates that forward fused away
- When Liger-Kernel covers your op (it already includes fused backward via `torch.autograd.Function`)

**When forward-only is fine (with autograd.Function wrapper for the forward):**
- When backward is dominated by other ops (attention, allreduce)
- When the forward fusion eliminates the memory bottleneck
- The wrapper ensures gradients flow even if backward is done by PyTorch autograd (recomputes via standard ops)

### Gradient Verification Protocol — MANDATORY

**Before promoting ANY kernel that touches training, run ALL of these:**

#### Test 1: Gradient Equivalence (P0 — most important)
```python
def test_gradient_equivalence(model_patched, model_unpatched, batch):
    """Compare weight gradients between patched and unpatched models."""
    # Forward + backward on both models (same input, same seed)
    loss_p = model_patched(**batch).loss
    loss_p.backward()
    loss_u = model_unpatched(**batch).loss
    loss_u.backward()

    # Check: loss must be identical
    assert abs(loss_p.item() - loss_u.item()) < 1e-6, \
        f"Loss mismatch: {loss_p.item()} vs {loss_u.item()}"

    # Check: every parameter must have non-zero gradient
    for name, param in model_patched.named_parameters():
        if param.requires_grad:
            assert param.grad is not None, f"{name}.grad is None (patched)"
            assert param.grad.norm() > 0, f"{name}.grad is zero (patched)"

    # Check: gradients must match unpatched
    for (n1, p1), (n2, p2) in zip(
        model_patched.named_parameters(),
        model_unpatched.named_parameters()
    ):
        if p1.requires_grad and p2.requires_grad:
            diff = (p1.grad - p2.grad).abs().max().item()
            tol = 5e-2 if p1.dtype == torch.float16 else 1e-3
            assert diff < tol, f"{n1}: grad diff {diff} > {tol}"
```

#### Test 2: No Zero Gradients (P0)
```python
def test_no_zero_gradients(model, batch):
    """Every trainable parameter must receive non-zero gradient."""
    model(**batch).loss.backward()
    for name, param in model.named_parameters():
        if param.requires_grad:
            assert param.grad is not None, f"{name}.grad is None"
            assert param.grad.abs().sum() > 0, f"{name}.grad is all zeros"
            assert not torch.isnan(param.grad).any(), f"{name}.grad has NaN"
            assert not torch.isinf(param.grad).any(), f"{name}.grad has Inf"
```

#### Test 3: No Stale Buffers (P0)
```python
def test_no_stale_buffers(model):
    """No register_buffer used for tensors that need gradients."""
    for name, buf in model.named_buffers():
        # Buffers should only be for non-learnable state (running stats, masks, etc.)
        assert not name.endswith(('_weight', '_bias', '_proj')), \
            f"Suspicious buffer '{name}' — should this be a parameter?"
```

#### Test 4: 50-Step Smoke Test (P0)
```python
def test_50_step_smoke(model_patched, model_unpatched, dataloader, seed=42):
    """Run 50 steps on both models, assert loss curves within 5%."""
    torch.manual_seed(seed)
    losses_p, losses_u = [], []
    for i, batch in enumerate(dataloader):
        if i >= 50: break
        # Patched
        loss_p = model_patched(**batch).loss
        loss_p.backward()
        optimizer_p.step(); optimizer_p.zero_grad()
        losses_p.append(loss_p.item())
        # Unpatched (same data)
        loss_u = model_unpatched(**batch).loss
        loss_u.backward()
        optimizer_u.step(); optimizer_u.zero_grad()
        losses_u.append(loss_u.item())

    # At step 50, losses must be within 5%
    ratio = losses_p[-1] / losses_u[-1]
    assert 0.95 < ratio < 1.05, \
        f"Loss divergence at step 50: patched={losses_p[-1]:.4f} unpatched={losses_u[-1]:.4f} ratio={ratio:.3f}"
```

#### Test 5: Grad Norm Sanity (P1 — runtime hook)
```python
def grad_norm_hook(model, step=0):
    """Log WARNING if any param has suspiciously low grad norm on first backward."""
    for name, param in model.named_parameters():
        if param.requires_grad and param.grad is not None:
            gnorm = param.grad.norm().item()
            if gnorm == 0:
                print(f"WARNING [step {step}] {name}: grad norm = 0 (possible gradient death)")
            elif gnorm < 1e-10:
                print(f"WARNING [step {step}] {name}: grad norm = {gnorm:.2e} (suspiciously low)")
```

#### Promotion Gate — NEVER skip this

A kernel is ONLY promoted when ALL of these pass:
1. ✅ Forward numerical correctness (atol=1e-3 fp16, 1e-5 fp32)
2. ✅ Gradient equivalence test (max diff < tolerance)
3. ✅ No zero/None/NaN/Inf gradients on any trainable parameter
4. ✅ No stale buffers used for learnable tensors
5. ✅ 50-step smoke test (loss curves within 5%)
6. ✅ Full model fwd+bwd speedup measured (not just kernel-level)

**"Backward doesn't crash" is NOT a valid promotion criterion. It was the exact failure mode in the BiBo SEV1 incident.**

---

## Core Architecture: The Optimization Loop

The tritonify workflow follows the **Profile → Diagnose → Plan → Implement → Validate** loop,
derived from MIT Kernel Design Agents (KDA), CudaForge, and KernelSkill.

```
┌─────────────────────────────────────────────────────────┐
│                    TRITONIFY LOOP                        │
│                                                          │
│  1. TASK CONTRACT    Define objective, constraints,      │
│                      validation, GRADIENT PLAN,          │
│                      BUFFER AUDIT, promotion criteria    │
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
│  6. VALIDATE         Correctness check → GRADIENT CHECK  │
│                      → Performance measure → Record      │
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
- **🔴 Gradient verification:** [How you'll prove gradients flow — e.g., "gradient equivalence test vs unpatched"]
- **🔴 Buffer audit:** [Confirm no register_buffer used for learnable tensors]
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
9. **🔴 NEVER write into `torch.empty()` without `autograd.Function` wrapper** — severs gradient graph (SEV1: 2026-05-29)
10. **🔴 NEVER use `register_buffer` for tensors that need gradients** — buffers are invisible to autograd (SEV1: 2026-05-29)
11. **🔴 NEVER promote kernel on "backward doesn't crash" alone** — silent gradient death is worse than a crash (SEV1: 2026-05-29)

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

### Evidence-Based Promotion Rules (SEV1 upgraded, 2026-05-29)

1. **Never promote without measurement** — every candidate must have timing data
2. **Correctness is binary** — pass/fail, no "close enough"
3. **Record exact numbers** — "faster" is not evidence, "18.4μs vs 45.2μs (2.46x)" is
4. **Compare against baseline** — always measure relative to the starting point
5. **Reject with reason** — never silently discard; record why
6. **🔴 Gradient equivalence is MANDATORY** — "backward doesn't crash" is NOT a valid promotion criterion (SEV1: backward "succeeded" while gradients were zero for 3 layers)
7. **🔴 No zero/None/NaN gradients** — every trainable param must receive a gradient
8. **🔴 50-step loss comparison** — patched vs unpatched must converge within 5%
9. **🔴 No register_buffer for learnable tensors** — buffers are invisible to autograd

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

### Correctness Verification (8-stage — SEV1 upgraded, 2026-05-29)

1. **Smoke test** — basic shapes work
2. **Shape sweeps** — test across batch sizes, seq lens, hidden dims
3. **Numerical tolerance** — atol=1e-3/rtol=1e-3 for fp16, atol=1e-5 for fp32
4. **Determinism** — same input → same output across runs
5. **Edge cases** — empty tensors, single element, max dimensions
6. **🔴 Gradient equivalence** — compare weight grads patched vs unpatched (max diff < tolerance)
7. **🔴 No zero gradients** — every trainable param has non-None, non-zero, non-NaN grad
8. **🔴 50-step smoke test** — loss curves within 5% of unpatched baseline

**Stages 6-8 are MANDATORY for any kernel used in training.** Skipping them is how the BiBo SEV1 incident happened — forward was verified to 1e-7 precision but gradients were completely dead.

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
| `templates/gradient_verification.py` | 🔴 MANDATORY: 5-test gradient verification suite (SEV1 incident response) |

### When to Load References

- **Optimizing MoE models** → Load `moe-kernels.md`
- **Writing loss functions** → Load `loss-kernels.md`
- **Convolution operations** → Load `convolution-kernels.md`
- **Any LLM operation** → Load `llm-optimizations.md`
- **Profiling/debugging** → Load `profiling-guide.md`
- **Starting optimization** → Load `optimization-playbook.md`
- **Need starter code** → Load `templates/llm-kernels.py`
- **🔴 Before promoting ANY training kernel** → Load `templates/gradient_verification.py` and run all 5 tests
- **Researching approaches** → Load `paper-survey.md`

---

## MIT Kernel Design Agents (KDA) Workflow

The KDA repo (`mit-han-lab/kernel-design-agents`) provides the core agent workflow pattern:

### Task Contract Pattern (SEV1 upgraded)
Every optimization MUST define:
- Objective, inputs, outputs
- Correctness requirements (tolerance)
- Baseline timing + target timing
- Validation command + evaluation command
- Promotion criteria
- **🔴 Gradient verification plan** — how will you prove gradients flow correctly?
- **🔴 register_buffer audit** — confirm no buffers used for learnable tensors

### Candidate Lineage Tracking
```jsonl
{"name": "v1_baseline", "parent": null, "status": "baseline", "perf_us": 45.2}
{"name": "v2_triton_naive", "parent": "v1_baseline", "status": "rejected", "perf_us": 52.1}
{"name": "v3_autotuned", "parent": "v2_triton_naive", "status": "promoted", "perf_us": 18.4}
```

### Evidence-Based Promotion Rules (SEV1 upgraded)
1. Never promote without measurement
2. Correctness is binary (pass/fail)
3. Record exact numbers, not "faster"
4. Compare against baseline
5. Reject with reason
6. 🔴 Gradient equivalence MANDATORY — "backward doesn't crash" is NOT evidence
7. 🔴 No zero/None/NaN gradients on any trainable parameter
8. 🔴 50-step loss comparison patched vs unpatched (within 5%)
9. 🔴 No register_buffer for learnable tensors

### ncu-report-skill Analysis Dimensions
1. SM occupancy & wave structure
2. Thread-block balance (tail effect)
3. Instruction-level stall analysis
4. Tensor core utilization
5. SM utilization timeline
6. Memory access pattern & cache efficiency

---

## References

### Incident Postmortems (READ THESE)

| Incident | Date | What Happened | Lesson |
|----------|------|---------------|--------|
| **BiBo SEV1: Gradient Death** | 2026-05-29 | Custom Triton kernels for MoE GLU + Dense MLP broke autograd. `register_buffer()` froze 3 layers, `torch.empty()` severed graph. 1 full training run wasted. | NEVER use `register_buffer` for learnable tensors. NEVER write into `torch.empty()` without `autograd.Function`. ALWAYS verify gradient equivalence before promoting. See `BiBo/postmortem/2026-05-29-triton-kernel-gradient-death/` |

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
