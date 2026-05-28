"""
Benchmark: tanh GLU — torch.compile vs Triton
RTX 3050 Laptop, PyTorch 2.6, Triton 3.7
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triton_shim  # noqa: F401

import torch
import triton
import triton.language as tl

def tanh_glu_eager(gate, up):
    return torch.tanh(gate) * up

tanh_glu_compiled = torch.compile(tanh_glu_eager)

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
    # tanh(x) = 1 - 2/(e^{2x} + 1)
    e2x = tl.exp(2.0 * gate)
    t = (e2x - 1.0) / (e2x + 1.0)
    out = t * up
    tl.store(Out + off_m[:, None] * stride_m + off_n[None, :], out.to(tl.float16), mask=mask)

def tanh_glu_triton(gate, up):
    M, N = gate.shape
    out = torch.empty_like(gate)
    def grid(meta): return (triton.cdiv(M, meta['BLOCK_M']), triton.cdiv(N, meta['BLOCK_N']))
    tanh_glu_kernel[grid](gate, up, out, M, N, gate.stride(0))
    return out

def bench(fn, gate, up, warmup=30, rep=500):
    for _ in range(warmup): fn(gate, up)
    torch.cuda.synchronize()
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    times = []
    for _ in range(rep):
        start.record(); fn(gate, up); end.record()
        torch.cuda.synchronize()
        times.append(start.elapsed_time(end))
    times.sort()
    return times[len(times)//2] * 1000

if __name__ == "__main__":
    print("=" * 70)
    print("tanh GLU Benchmark: torch.compile vs Triton")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"PyTorch: {torch.__version__}, Triton: {triton.__version__}")
    print("=" * 70)

    g = torch.randn(32, 2048, device='cuda', dtype=torch.float16)
    u = torch.randn(32, 2048, device='cuda', dtype=torch.float16)
    print("\nWarming up torch.compile...")
    for _ in range(5): tanh_glu_compiled(g, u)
    torch.cuda.synchronize()
    print("Done.\n")

    shapes = [
        (1, 1024), (1, 2048), (1, 4096),
        (32, 1024), (32, 2048), (32, 4096),
        (128, 1024), (128, 2048),
        (256, 1024), (256, 2048),
        (512, 2048), (1024, 2048),
    ]

    print(f"{'Shape':<20} {'Eager':>10} {'Compiled':>10} {'Triton':>10} {'vs Eager':>10} {'vs Compile':>10}")
    print("-" * 75)

    for M, N in shapes:
        gate = torch.randn(M, N, device='cuda', dtype=torch.float16)
        up = torch.randn(M, N, device='cuda', dtype=torch.float16)
        ref = tanh_glu_eager(gate, up)
        tri = tanh_glu_triton(gate, up)
        ok = torch.allclose(ref.float(), tri.float(), atol=1e-2, rtol=1e-2)
        e = bench(tanh_glu_eager, gate, up)
        c = bench(tanh_glu_compiled, gate, up)
        t = bench(tanh_glu_triton, gate, up)
        vs_eager = e / t
        vs_compile = c / t
        marker = "WIN" if vs_compile > 1.0 else ""
        print(f"({M:>5}, {N:>5})       {e:7.1f}us  {c:7.1f}us  {t:7.1f}us    {vs_eager:5.2f}x     {vs_compile:5.2f}x {marker} [{'OK' if ok else 'FAIL'}]")
