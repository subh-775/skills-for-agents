<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process</span>
</div>

# Tritonify

Agent-driven GPU kernel optimization. Triton + CUDA. Profiling-guided iteration backed by 52+ academic papers and the MIT Kernel Design Agents workflow.

## When to Use

- Writing new Triton or CUDA kernels
- Optimizing existing GPU kernels
- Fusing operators (RMSNorm+residual, SwiGLU, cross-entropy, MoE dispatch)
- Profiling and diagnosing kernel bottlenecks with Nsight Compute
- Speeding up LLM training/inference operations
- Benchmarking kernel performance against baselines

## Triggers

```
"optimize kernel", "write triton", "profile CUDA", "fuse operators",
"speed up LLM ops", "MoE kernel", "fused loss", "attention kernel",
"beat torch.compile", "kernel benchmark"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Fused RMSNorm + Residual</div>
<div class="example-desc">Write a Triton kernel that fuses RMSNorm with residual add, eliminating 2 memory round-trips.</div>

```
Write a fused RMSNorm + residual add Triton kernel for hidden_dim=4096

The agent:
- Defines a task contract (correctness tolerance, perf target)
- Writes the Triton kernel with 2D tiling
- Autotunes BLOCK_N and num_warps
- Benchmarks against PyTorch eager
- Reports speedup (typically 1.5-2x)
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Profile and optimize a CUDA kernel</div>
<div class="example-desc">Profile an existing kernel with Nsight Compute, diagnose bottlenecks, and fix them.</div>

```
Profile this matmul kernel and tell me what's wrong

The agent:
- Builds a minimal NCU harness
- Runs ncu --set full
- Maps metrics to 14 known diagnosis patterns
- Identifies: uncoalesced loads (Pattern C), low occupancy (Pattern J)
- Proposes fixes ranked by impact
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Fused MoE dispatch kernel</div>
<div class="example-desc">Write a fused MoE dispatch kernel with block-scheduled grouped GEMM.</div>

```
Write a fused MoE dispatch kernel for Mixtral-8x7B (8 experts, top-2)

The agent:
- Uses TritonMoE pattern: block-scheduled grouped GEMM
- Fuses gate+up SwiGLU projection (35% memory savings)
- Implements stable softmax router with -1.0 masking
- Benchmarks against vLLM's fused MoE
```
</div>

## What It Covers

### Kernel Types
- **Attention**: FlashAttention, PagedAttention, GQA, MQA
- **Normalization**: RMSNorm, LayerNorm (fused with residual/dropout)
- **Activations**: SiLU GLU, tanhGLU, ReLU²GLU, GeGLU, SwiGLU
- **Loss functions**: Cross-entropy, KL, JSD, GRPO, DPO, focal loss
- **MoE**: Dispatch, compute, combine, routing, grouped GEMM
- **Optimizer**: Fused Adam/AdamW
- **Positional**: RoPE (fused with attention)
- **KV cache**: Paged attention, quantization, speculative decoding

### Optimization Workflow (from MIT KDA)
1. **Task contract** — define objective, constraints, validation, promotion criteria
2. **Profile** — Nsight Compute or Triton profiling
3. **Diagnose** — map to 14 known bottleneck patterns (A-N)
4. **Plan** — prioritize by Amdahl's law
5. **Implement** — one candidate at a time
6. **Validate** — correctness + performance measurement
7. **Record** — candidate lineage tracking with evidence

### Research Basis
- 52+ academic papers (2024-2026)
- MIT Kernel Design Agents workflow
- CudaForge, KernelSkill, AutoKernel, DRTriton, CUDA Agent
- FlashAttention family, ThunderKittens, CUTLASS, Liger Kernel
- Production kernels: vLLM, FlashInfer, SGLang, Unsloth

## References

| File | Contents |
|------|----------|
| `references/paper-survey.md` | 36 academic papers with abstracts and GitHub repos |
| `references/kda-extraction.md` | MIT KDA: 14 diagnosis patterns, B200 specs, workflow |
| `references/moe-kernels.md` | MoE dispatch/compute: 16 papers, code patterns |
| `references/loss-kernels.md` | Fused CE, KL, JSD, GRPO, DPO from Liger-Kernel |
| `references/llm-optimizations.md` | Every LLM op: attention, norm, activation, RoPE, optimizer |
| `references/profiling-guide.md` | NCU commands, metrics, Triton profiling, decision tree |
| `references/optimization-playbook.md` | Six-tier optimization framework |
| `templates/llm-kernels.py` | 6 ready-to-use Triton kernel templates |
| `templates/glu-kernels.md` | GLU activation reference (all variants) |
| `benchmarks/glu_benchmark.py` | GLU benchmark: PyTorch eager vs Triton |
