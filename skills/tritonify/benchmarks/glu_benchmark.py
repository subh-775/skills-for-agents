"""
GLU Benchmark: PyTorch Eager vs Triton
========================================
SiLU GLU, tanhGLU, ReLU² GLU — RTX 3050 Laptop
"""

import torch
import triton
import triton.language as tl

# ============================================================================
# BASELINE
# ============================================================================

def silu_glu_eager(gate, up):
    return (gate * torch.sigmoid(gate)) * up

def tanh_glu_eager(gate, up):
    return torch.tanh(gate) * up

def relu2_glu_eager(gate, up):
    return (torch.relu(gate) ** 2) * up


# ============================================================================
# TRITON KERNELS — 2D grid, proper masking
# ============================================================================

@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 1024}, num_warps=4),
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 2048}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 1024}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 2048}, num_warps=8),
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 4096}, num_warps=8),
    ],
    key=['M', 'N'],
)
@triton.jit
def silu_glu_kernel(Gate, Up, Out, M, N, stride_m, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    mask = (off_m[:, None] < M) & (off_n[None, :] < N)

    gate = tl.load(Gate + off_m[:, None] * stride_m + off_n[None, :], mask=mask, other=0.0).to(tl.float32)
    up = tl.load(Up + off_m[:, None] * stride_m + off_n[None, :], mask=mask, other=0.0).to(tl.float32)
    out = (gate * tl.sigmoid(gate)) * up
    tl.store(Out + off_m[:, None] * stride_m + off_n[None, :], out.to(tl.float16), mask=mask)


@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 1024}, num_warps=4),
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 2048}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 1024}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 2048}, num_warps=8),
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 4096}, num_warps=8),
    ],
    key=['M', 'N'],
)
@triton.jit
def tanh_glu_kernel(Gate, Up, Out, M, N, stride_m, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    mask = (off_m[:, None] < M) & (off_n[None, :] < N)

    gate = tl.load(Gate + off_m[:, None] * stride_m + off_n[None, :], mask=mask, other=0.0).to(tl.float32)
    up = tl.load(Up + off_m[:, None] * stride_m + off_n[None, :], mask=mask, other=0.0).to(tl.float32)
    # Fast tanh: tanh(x) = (e^2x - 1) / (e^2x + 1) = 1 - 2/(e^2x + 1)
    # Single exp, no libdevice overhead
    e2x = tl.exp(2.0 * gate)
    t = (e2x - 1.0) / (e2x + 1.0)
    out = t * up
    tl.store(Out + off_m[:, None] * stride_m + off_n[None, :], out.to(tl.float16), mask=mask)


@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 1024}, num_warps=4),
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 2048}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 1024}, num_warps=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 2048}, num_warps=8),
        triton.Config({'BLOCK_M': 32, 'BLOCK_N': 4096}, num_warps=8),
    ],
    key=['M', 'N'],
)
@triton.jit
def relu2_glu_kernel(Gate, Up, Out, M, N, stride_m, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    mask = (off_m[:, None] < M) & (off_n[None, :] < N)

    gate = tl.load(Gate + off_m[:, None] * stride_m + off_n[None, :], mask=mask, other=0.0).to(tl.float32)
    up = tl.load(Up + off_m[:, None] * stride_m + off_n[None, :], mask=mask, other=0.0).to(tl.float32)
    r = tl.maximum(gate, 0.0)
    out = (r * r) * up
    tl.store(Out + off_m[:, None] * stride_m + off_n[None, :], out.to(tl.float16), mask=mask)


# ============================================================================
# WRAPPERS
# ============================================================================

def _run(kernel, gate, up):
    M, N = gate.shape
    out = torch.empty_like(gate)
    def grid(meta):
        return (triton.cdiv(M, meta['BLOCK_M']), triton.cdiv(N, meta['BLOCK_N']))
    kernel[grid](gate, up, out, M, N, gate.stride(0))
    return out

def silu_glu_triton(gate, up): return _run(silu_glu_kernel, gate, up)
def tanh_glu_triton(gate, up): return _run(tanh_glu_kernel, gate, up)
def relu2_glu_triton(gate, up): return _run(relu2_glu_kernel, gate, up)


# ============================================================================
# BENCHMARK
# ============================================================================

def verify(name, ref_fn, tri_fn, gate, up):
    ref = ref_fn(gate, up)
    tri = tri_fn(gate, up)
    max_diff = (ref.float() - tri.float()).abs().max().item()
    ok = torch.allclose(ref.float(), tri.float(), atol=1e-2, rtol=1e-2)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: max_diff={max_diff:.6f}")
    return ok

def bench(fn, gate, up, warmup=30, rep=500):
    for _ in range(warmup):
        fn(gate, up)
    torch.cuda.synchronize()
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    times = []
    for _ in range(rep):
        start.record()
        fn(gate, up)
        end.record()
        torch.cuda.synchronize()
        times.append(start.elapsed_time(end))
    times.sort()
    return times[len(times)//2] * 1000

def run_benchmark(M, N):
    print(f"\n{'='*70}")
    print(f"Shape: M={M}, N={N}")
    print(f"{'='*70}")

    gate = torch.randn(M, N, device='cuda', dtype=torch.float16)
    up = torch.randn(M, N, device='cuda', dtype=torch.float16)

    print("\nCorrectness:")
    all_ok = True
    all_ok &= verify("SiLU GLU", silu_glu_eager, silu_glu_triton, gate, up)
    all_ok &= verify("tanh GLU", tanh_glu_eager, tanh_glu_triton, gate, up)
    all_ok &= verify("ReLU2 GLU", relu2_glu_eager, relu2_glu_triton, gate, up)

    results = {}
    for name, eager_fn, triton_fn in [
        ("SiLU GLU", silu_glu_eager, silu_glu_triton),
        ("tanh GLU", tanh_glu_eager, tanh_glu_triton),
        ("ReLU2 GLU", relu2_glu_eager, relu2_glu_triton),
    ]:
        e_med = bench(eager_fn, gate, up)
        t_med = bench(triton_fn, gate, up)
        sp = e_med / t_med
        results[name] = {'eager': e_med, 'triton': t_med, 'speedup': sp}
        print(f"\n  {name}: eager={e_med:.1f}us  triton={t_med:.1f}us  speedup={sp:.2f}x {'WIN' if sp > 1.0 else ''}")

    return results

if __name__ == "__main__":
    print("=" * 70)
    print("GLU Benchmark: PyTorch Eager vs Triton")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"SMs: {torch.cuda.get_device_properties(0).multi_processor_count}")
    print(f"Triton: {triton.__version__}, PyTorch: {torch.__version__}")
    print("=" * 70)

    shapes = [
        (1, 1024), (1, 2048), (1, 4096),
        (32, 1024), (32, 2048), (32, 4096),
        (128, 1024), (128, 2048),
        (256, 1024), (256, 2048),
        (512, 2048), (1024, 2048),
    ]

    all_results = {}
    for M, N in shapes:
        try:
            results = run_benchmark(M, N)
            all_results[(M, N)] = results
        except torch.cuda.OutOfMemoryError:
            print(f"\n  OOM at ({M}, {N}), skipping")
            torch.cuda.empty_cache()

    print("\n" + "=" * 90)
    print("SUMMARY: Triton Speedup over PyTorch Eager")
    print("=" * 90)
    print(f"{'Shape':<20} {'SiLU GLU':>12} {'tanh GLU':>12} {'ReLU2 GLU':>12}")
    print("-" * 90)
    for (M, N), results in all_results.items():
        row = f"({M:>5}, {N:>5})     "
        for name in ["SiLU GLU", "tanh GLU", "ReLU2 GLU"]:
            sp = results[name]['speedup']
            marker = "WIN" if sp > 1.0 else "   "
            row += f"  {sp:5.2f}x {marker}"
        print(row)
    print("-" * 90)
    print("\nAverage speedups:")
    for name in ["SiLU GLU", "tanh GLU", "ReLU2 GLU"]:
        avg = sum(r[name]['speedup'] for r in all_results.values()) / len(all_results)
        print(f"  {name}: {avg:.2f}x")
