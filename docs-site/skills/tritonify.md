<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process</span>
</div>

# Tritonify

Agent-driven GPU kernel optimization for Triton and CUDA. Profiling-guided iteration backed by 52+ academic papers, the MIT Kernel Design Agents workflow, and production kernel libraries (Liger-Kernel, FlashAttention, vLLM, FlashInfer).

## When to Use

- Writing new Triton or CUDA kernels from scratch
- Optimizing existing GPU kernels that are too slow
- Fusing multiple operators into single kernels (RMSNorm+residual, SwiGLU, cross-entropy)
- Profiling and diagnosing kernel bottlenecks with Nsight Compute
- Speeding up LLM training or inference operations
- MoE dispatch/compute kernel optimization
- Benchmarking kernels against PyTorch eager or torch.compile

## Liger-Kernel First Policy (MANDATORY)

**Before writing ANY custom Triton kernel, check if Liger-Kernel already provides it.**

| Operation | Liger Module |
|-----------|-------------|
| RMSNorm | `liger_kernel.ops.rms_norm` |
| LayerNorm | `liger_kernel.ops.layer_norm` |
| SwiGLU | `liger_kernel.ops.swiglu` |
| GeGLU | `liger_kernel.ops.geglu` |
| Cross-Entropy | `liger_kernel.ops.cross_entropy` |
| Fused Linear+CE | `liger_kernel.ops.fused_linear_cross_entropy` |
| KL/JSD/TVD | `liger_kernel.ops.{kl_div,jsd,tvd}` |
| GRPO/DPO/SimPO | `liger_kernel.ops.{grpo_loss,dpo_loss,simpo_loss}` |
| RoPE | `liger_kernel.ops.rope` |

```python
# Drop-in replacement:
from liger_kernel.transformers import LigerRMSNorm, LigerSwiGLUMLP, LigerCrossEntropyLoss

# Monkey-patch HuggingFace model:
from liger_kernel.transformers import monkey_patch
monkey_patch(model)
```

Only write custom Triton when: Liger doesn't cover it (conv, MoE, attention variants), need architecture-specific fusion, need different tiling, or doing kernel research. **Never write standalone RMSNorm/SwiGLU/CE/RoPE when Liger provides one.**

### Backward Pass: Best Practice

Fused forward is still valuable even without a matching backward — it eliminates intermediate tensor allocation regardless. Forward-only Triton gave 1.51x full model speedup on BiBo's MoE with backward via PyTorch autograd.

**Write fused backward when:** training where backward is the bottleneck (>40% of step time), or when backward re-materializes large intermediates.

**Forward-only is fine when:** inference, backward dominated by other ops, or PyTorch autograd gives correct gradients through the Triton output.

**Verify:** Full model loss identical, backward completes without NaN/Inf, full fwd+bwd speedup holds.

## Triggers

```
"optimize kernel", "write triton", "profile CUDA", "fuse operators",
"speed up LLM ops", "MoE kernel", "fused loss", "attention kernel",
"beat torch.compile", "kernel benchmark", "write CUDA kernel"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Fused RMSNorm + Residual Add</div>
<div class="example-desc">Write a Triton kernel that fuses RMSNorm with residual add, eliminating 2 memory round-trips. Typical speedup: 1.5-2x over PyTorch eager.</div>

```
Write a fused RMSNorm + residual add Triton kernel for hidden_dim=4096

The agent:
1. Defines a task contract (atol=1e-3 for fp16, target 2x speedup)
2. Writes the Triton kernel with 2D tiling (BLOCK_M x BLOCK_N)
3. Autotunes BLOCK_N and num_warps across 6 configs
4. Benchmarks against PyTorch eager on your GPU
5. Verifies correctness with torch.allclose
6. Reports: "1.88x speedup at (256, 4096), all correctness checks pass"
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Profile and Diagnose a CUDA Kernel</div>
<div class="example-desc">Profile an existing kernel with Nsight Compute, identify bottlenecks using 14 known diagnosis patterns, and fix them.</div>

```
Profile this matmul kernel and tell me what's wrong

The agent:
1. Builds a minimal NCU harness (warmup + measured run)
2. Runs ncu --set full to collect all metrics
3. Extracts key metrics: SM occupancy, memory throughput,
   tensor core utilization, stall reasons
4. Maps to diagnosis patterns:
   - Pattern C: uncoalesced loads (sectors/request > 5)
   - Pattern J: low achieved occupancy (theoretical 75%, achieved 35%)
5. Proposes fixes ranked by impact:
   Priority 1: Restructure thread-to-data mapping (fix Pattern C)
   Priority 2: Reduce register pressure via launch_bounds (fix Pattern J)
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Fused MoE Dispatch Kernel</div>
<div class="example-desc">Write a fused MoE dispatch kernel with block-scheduled grouped GEMM for Mixtral-style models.</div>

```
Write a fused MoE dispatch kernel for Mixtral-8x7B (8 experts, top-2)

The agent uses the TritonMoE pattern:
1. Block-scheduled grouped GEMM: maps program blocks to
   (expert_id, token_offset) pairs
2. Fused gate+up SwiGLU: single kernel pass for both projections
   with in-register SiLU (35% memory savings)
3. Stable softmax router: subtract max before exp, mask top-k
   selections to -1.0 (not 0.0) to prevent re-selection
4. Sort-based permutation for coalesced memory access
5. Benchmarks against vLLM's fused MoE kernel
```
</div>

<div class="example-box">
<div class="example-label">Example 4</div>
<div class="example-title">Fused Cross-Entropy Loss</div>
<div class="example-desc">Write a numerically stable fused cross-entropy kernel that avoids materializing the full BT×V logit matrix.</div>

```
Write a fused cross-entropy loss kernel for vocab_size=32000

The agent uses the Liger-Kernel pattern:
1. Online softmax (2-pass): track running max + sum correction
2. All computation in float32 for numerical stability
3. In-place gradient storage: forward writes gradients into
   logits buffer, backward just scales by grad_output
4. Chunked linear+CE fusion for large vocab: avoids materializing
   the full BT×V logit matrix (saves ~2GB for BT=16384)
5. Supports: label smoothing, z-loss, softcapping, class weights
```
</div>

## Optimization Workflow

The workflow comes from MIT Kernel Design Agents (mit-han-lab/kernel-design-agents):

### The Loop

```
1. TASK CONTRACT    Define objective, constraints, validation, promotion criteria
2. PROFILE          Nsight Compute (CUDA) or triton.testing (Triton)
3. DIAGNOSE         Map profiling data to 14 known bottleneck patterns
4. PLAN             Prioritize by Amdahl's law, select optimization strategy
5. IMPLEMENT        One candidate at a time, small testable changes
6. VALIDATE         Correctness check → performance measurement → record evidence
7. DECIDE           Keep / Revise / Reject candidate, update candidates.jsonl
8. REPEAT           Until promotion criteria met
```

### Task Contract Template

Every optimization task must define:

```
- Objective:      What to optimize (e.g., "fused RMSNorm + residual add")
- Input:          Tensor shapes, dtypes, device
- Output:         Expected output tensor
- Correctness:    Tolerance (e.g., "atol=1e-3, rtol=1e-3 for fp16")
- Baseline:       Current implementation + timing (e.g., "PyTorch eager: 45μs")
- Target:         Performance goal (e.g., "<20μs or 2.25x speedup")
- Constraints:    Language, APIs, dependencies, memory limits
- Validation:     Command that proves correctness
- Evaluation:     Command that measures performance
- Promotion:      What must be true to accept a candidate
```

### Candidate Lineage Tracking

```
{"name": "v1_baseline", "parent": null, "status": "baseline", "perf_us": 45.2}
{"name": "v2_triton_naive", "parent": "v1_baseline", "status": "rejected", "perf_us": 52.1}
{"name": "v3_autotuned", "parent": "v2_triton_naive", "status": "promoted", "perf_us": 18.4}
{"name": "v4_fused", "parent": "v3_autotuned", "status": "promoted", "perf_us": 12.1}
```

## Diagnosis Playbook (14 Patterns)

From MIT KDA's ncu-report-skill. Map profiling data to these patterns to identify bottlenecks:

| Pattern | Signal | Cause | Fix |
|---------|--------|-------|-----|
| **A: Small grid** | SM idle, waves < 0.5 | Too few blocks | Increase parallelism, fuse ops, persistent kernels |
| **B: Tail effect** | max_seq/avg_seq > 3 | Variable-length inputs | Sort by length, split long sequences, chunkwise kernel |
| **C: Uncoalesced loads** | sectors/request > 5 | Strided memory access | AoS→SoA, vectorize with float4, shared mem transpose |
| **D: Sparse writes** | bytes_per_sector_st < 16 | Subset of lanes write | Pack writes via shuffle/shared mem, coalesced store |
| **E: Latency-bound** | long_scoreboard > 40% | Memory latency stalls | Unroll, more warps, cp.async/TMA, software pipelining |
| **F: Not on tensor cores** | FMA pipe > 50%, TC = 0% | Using scalar FMA | Use WMMA/wgmma/tcgen05.mma, restructure for MMA tiles |
| **G: Atomics contention** | Stalls on ATOM/RED | Serialized atomics | Hierarchical reduction: warp shuffle → shared mem → atomic |
| **H: Bank conflicts** | High shared-mem wavefronts | Same-bank access | Padding (tile[32][33]), XOR swizzle |
| **I: Sync overhead** | barrier stall > 20% | Too many syncthreads | Warp-level primitives, mbarrier, reduce sync count |
| **J: Low occupancy** | Achieved << theoretical | Stalls, imbalance | Find stall reason (E, H, I, B), launch_bounds |
| **K: Register spill** | local_ld/st > 0, regs > 128 | Spilled to DRAM | launch_bounds, reduce live values, split kernel |
| **L: Unintentional FP64** | fp64_cycles > 0 | Literals default to double | Add `f` suffix, use __expf/__logf |
| **M: Pipeline bubbles** | Sawtooth timeline | No compute/mem overlap | Double-buffer, 3-4 stage pipeline, cp.async/TMA |
| **N: Warp divergence** | threads/inst < 32 | Branches serialize | Rearrange data, branchless masking |

## Kernel Types Covered

### Attention
- **FlashAttention** — IO-aware tiling, online softmax, never materializes N×N matrix
- **FlashAttention-3** — Hopper: warp specialization + FP8, 740 TFLOPS on H100
- **PagedAttention** — Non-contiguous KV cache pages (vLLM)
- **GQA/MQA** — Fewer KV heads, repeat in kernel not memory

### Normalization
- **RMSNorm + residual** — Fused: single read, compute, single write (saves 2 round-trips)
- **LayerNorm + dropout + residual** — Fused pass

### Activations (GLU variants)
- **SwiGLU** — SiLU(gate) * up. `gate * tl.sigmoid(gate)` — native Triton, fast
- **tanhGLU** — tanh(gate) * up. Use `2*sigmoid(2x)-1` (NOT libdevice.tanh, it's slow)
- **ReLU²GLU** — ReLU(gate)² * up. `tl.maximum(gate, 0.0) ** 2` — native, fast
- **GeGLU** — GELU(gate) * up. Fast approx: `gate * sigmoid(1.702 * gate)`

### Loss Functions
- **Fused Cross-Entropy** — Online softmax, in-place gradient storage, chunked for large vocab
- **Fused Linear+CE** — Avoids materializing BT×V logits (saves ~2GB for BT=16384, V=32000)
- **KL/JSD/TVD** — All fused in single Triton kernels (Liger-Kernel)
- **GRPO Loss** — 1004-line kernel: selective log-softmax, PPO clipping, KL penalty
- **DPO/SimPO/CPO/ORPO** — Chunked preference losses via torch.func.grad_and_value

### MoE (Mixture of Experts)
- **Block-scheduled grouped GEMM** — Map program blocks to (expert, token-offset) pairs
- **Fused gate+up SwiGLU** — Single kernel, shared A-tile loads, in-register activation (35% savings)
- **Stable softmax router** — Subtract max, mask top-k to -1.0 (not 0.0)
- **Routing-aware dispatch** — Adapt tile size to runtime expert histogram (RaMP: 1.30x over vLLM)

### Convolution (from Triton Gluon + PyTorch Inductor)
- **Conv2d forward** — Implicit GEMM + TMA im2col (Hopper/Blackwell) or tl.dot (all GPUs). M=N×out_h×out_w, N=Co, K=R×S×Ci
- **Conv2d dgrad** — Input gradient via subproblem decomposition (stride_h × stride_w subproblems) + split-K reduction
- **Conv2d wgrad** — Weight gradient: grad_out^T @ im2col(input), tiled over Co × Ci × spatial
- **Depthwise conv1d** — Direct 3D tiling (NLC layout), element-wise multiply-accumulate per channel
- **Fused conv + SiLU** — SiLU in epilogue: `result * sigmoid(result)` (for BiBo conv layers)
- **Fused conv + residual** — Load residual + conv output in epilogue, single write
- **Fused conv + BN** — Pre-compute fused weights on host (eval mode): W_fused = W * gamma/sqrt(var+eps)
- **Conv + bias + activation** — All in epilogue, no extra kernel launch

**Key APIs:**
- `TensorDescriptorIm2Col` — TMA im2col descriptor for NHWC input
- `tma.async_load_im2col(desc, coord, offsets, barrier, smem)` — Hardware im2col load
- `TensorDescriptor.from_tensor(weight_2d, block_shape, layout)` — TMA for weight
- `tcgen05_mma(a, b, acc, use_acc)` — Blackwell MMA

**Critical patterns:**
- NHWC layout required (permute from NCHW: `x.permute(0,2,3,1).contiguous()`)
- Weight reshape: `[Co, R, S, Ci] → [Co, R*S*Ci]` for 2D TMA
- Channel padding for TMA 16-byte alignment (Ci=3 → pad to 8 for bf16)
- M-offset decomposition: flat M → `(batch, out_y, out_x)`
- Autotune key: `(out_h, out_w, stride_h, stride_w)` not full input shape
- Dgrad subproblem decomposition required for stride > 1

### Other
- **Fused Adam/AdamW** — Momentum + variance + weight update in single kernel
- **RoPE** — Rotary position embedding fused with attention
- **Fused QKV projection** — Single matmul for Q, K, V
- **KV cache** — Paged attention, INT8/FP8 quantization

## Triton vs CUDA Decision

| Use Case | Language | Why |
|----------|----------|-----|
| Rapid prototyping | **Triton** | 10x less code |
| Cross-platform (NVIDIA+AMD) | **Triton** | Zero code changes |
| Standard patterns (matmul, attention, elementwise) | **Triton** | Block-level programming is natural fit |
| Architecture-specific (TMA, WGMMA, DPX) | **CUDA** | Triton can't express these |
| Warp specialization (producer-consumer) | **CUDA** | Triton doesn't support it |
| Production inference (every TFLOP counts) | **CUDA** | 5-15% typical gap |
| LLM-generated kernels | **Triton** | Easier for models to generate correctly |

## Triton API Quick Reference

### Native intrinsics (fast)
- `tl.sigmoid(x)` — hardware sigmoid
- `tl.exp(x)` — exponential
- `tl.log(x)` — logarithm
- `tl.maximum(a, b)` — element-wise max
- `tl.dot(a, b)` — matrix multiply (uses tensor cores)

### Libdevice calls (slow, ~2x overhead)
- `tl.extra.cuda.libdevice.tanh(x)` — tanh via CUDA math library
- Prefer sigmoid identity: `2 * tl.sigmoid(2*x) - 1`

### Autotuning
```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256}, num_warps=8),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 512}, num_warps=4),
    ],
    key=['M', 'N'],  # retune per input shape
)
```

## State of the Art (May 2026)

| System | Approach | Result |
|--------|----------|--------|
| **KernelSkill** | Multi-agent + skill memory | 100% success, 5.44x/2.82x/1.92x on KBL1/L2/L3 |
| **CUDA Agent** | Agentic RL | 100%/100%/92% faster than torch.compile |
| **DRTriton-7B** | RL + synthetic data | 92% speedup rate on KBL2 (vs 23% GPT-5.2) |
| **CODA** | GEMM-epilogue abstraction | High perf for non-attention Transformer ops |
| **CudaForge** | Multi-agent + NCU feedback | 97.6% correct, 1.68x, $0.30/kernel |

## Reference Files

| File | What's Inside |
|------|---------------|
| `references/paper-survey.md` | 36 academic papers: abstracts, key findings, GitHub repos, thematic analysis across RL-training, multi-agent, evolutionary, DSL, and benchmark approaches |
| `references/kda-extraction.md` | MIT KDA deep dive: 9-step workflow, task contract template, 14 NCU diagnosis patterns with signals/causes/fixes, 6 analysis dimensions, KernelWiki (2265 pages, 15 techniques, 12 kernel case studies), B200/Blackwell specs (tcgen05, TMEM, CLC, 2CTA, NVFP4) |
| `references/moe-kernels.md` | MoE kernel reference: 16 papers (TritonMoE, FlashMoE, MegaBlocks, ScatterMoE, RaMP, UniEP), production implementations (vLLM, DeepGEMM, Alpha-MoE), code patterns for block-scheduled grouped GEMM, fused gate+up SwiGLU, stable softmax router, routing-aware dispatch |
| `references/loss-kernels.md` | Fused loss functions: online softmax algorithm, in-place gradient storage, chunked linear+CE fusion, LogSumExp decomposition for 256K vocab, all Liger-Kernel loss kernels (CE, KL, JSD, TVD, GRPO, DPO, sparsemax) |
| `references/llm-optimizations.md` | Every LLM kernel op: RMSNorm, LayerNorm, SwiGLU, tanhGLU, ReLU²GLU, GeGLU, FlashAttention, PagedAttention, RoPE, fused QKV, fused Adam, KV cache, sampling, speculative decoding |
| `references/profiling-guide.md` | NCU profiling: essential commands, key metrics for A100/Hopper/B200, diagnosis decision tree, harness template, Triton profiling with torch.profiler |
| `references/optimization-playbook.md` | Six-tier optimization framework from AutoKernel: baseline → autotuning → memory optimization → operator fusion → algorithmic optimization → architecture-specific (with code examples for each tier) |
| `references/convolution-kernels.md` | Conv2d implicit GEMM, TMA im2col, depthwise, dgrad/wgrad, fused conv patterns from Triton Gluon + PyTorch Inductor |
| `templates/llm-kernels.py` | 6 ready-to-use Triton kernels: fused RMSNorm+residual, fused SwiGLU, fused cross-entropy, fused softmax, fused RMSNorm, fused linear+GELU (with autotuning configs and correctness test patterns) |
| `templates/glu-kernels.md` | GLU activation reference: all variants (SwiGLU, tanhGLU, ReLU²GLU, GeGLU), correct Triton API for each (tl.sigmoid for SiLU, sigmoid identity for tanh, tl.maximum for ReLU²), fused linear+GLU pattern |
| `benchmarks/glu_benchmark.py` | GLU benchmark script: PyTorch eager vs Triton for SiLU/tanh/ReLU² across 12 shapes, correctness verification, timing with CUDA events |

## Key GitHub Repos

**Kernel Generation Agents:**
- [mit-han-lab/kernel-design-agents](https://github.com/mit-han-lab/kernel-design-agents) — KDA workflow (Claude Code-centric)
- [OptimAI-Lab/CudaForge](https://github.com/OptimAI-Lab/CudaForge) — Multi-agent CUDA generation
- [0satan0/KernelMem](https://github.com/0satan0/KernelMem) — KernelSkill (100% success rate)
- [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel) — AutoKernel, 18 starter kernels

**Production Kernels:**
- [linkedin/Liger-Kernel](https://github.com/linkedin/Liger-Kernel) — Triton training kernels (CE, RMSNorm, SwiGLU, RoPE, Adam)
- [Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention) — FlashAttention family
- [flashinfer-ai/flashinfer](https://github.com/flashinfer-ai/flashinfer) — Serving-optimized attention
- [vllm-project/vllm](https://github.com/vllm-project/vllm) — PagedAttention, fused MoE

**MoE:**
- [bassrehab/triton-kernels](https://github.com/bassrehab/triton-kernels) — TritonMoE cross-platform
- [stanford-futuredata/megablocks](https://github.com/stanford-futuredata/megablocks) — Block-sparse MoE
- [deepseek-ai/DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) — FP8 grouped GEMM

**Convolution:**
- [triton-lang/triton/python/examples/gluon/02-conv-*.py](https://github.com/triton-lang/triton/tree/main/python/examples/gluon) — Production conv2d (fprop/dgrad/wgrad)
- [triton-lang/triton/python/tutorials/gluon/13-conv-im2col.py](https://github.com/triton-lang/triton/blob/main/python/tutorials/gluon/13-conv-im2col.py) — TMA im2col tutorial
- [pytorch/pytorch/torch/_inductor/kernel/conv.py](https://github.com/pytorch/pytorch/blob/main/torch/_inductor/kernel/conv.py) — Inductor conv templates
