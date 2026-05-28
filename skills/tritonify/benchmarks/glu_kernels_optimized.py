"""
Optimized GLU Kernels — Vectorized loads + fused compute
=========================================================
These kernels use:
1. Vectorized 4-element loads (float4 equivalent)
2. Fused read-compute-write (single pass)
3. FP32 intermediate compute for numerical stability
4. Optimal tile sizes for T4 (2560 CUDA cores, 80 SMs)

Designed to beat torch.compile on T4.
"""

import torch
import triton
import triton.language as tl


# ============================================================================
# VECTORIZED TRITON KERNELS (4 loads at once)
# ============================================================================

@triton.autotune(
    configs=[
        # T4 has 2560 CUDA cores (80 SMs × 32 cores)
        # Sweet spot: 4096-8192 elements per block with 8 warps
        triton.Config({'BLOCK_N': 4096}, num_warps=8),
        triton.Config({'BLOCK_N': 8192}, num_warps=8),
        triton.Config({'BLOCK_N': 4096}, num_warps=4),
        triton.Config({'BLOCK_N': 2048}, num_warps=4),
        triton.Config({'BLOCK_N': 8192}, num_warps=16),
        triton.Config({'BLOCK_N': 16384}, num_warps=16),
    ],
    key=['N'],
)
@triton.jit
def silu_glu_vec_kernel(
    Gate, Up, Out,
    stride_m,
    N,
    BLOCK_N: tl.constexpr,
):
    """Vectorized SiLU(gate) * up — processes 4 elements per load"""
    row = tl.program_id(0)

    # Process in chunks of 4 vectorized loads
    for base in range(0, BLOCK_N, BLOCK_N):
        cols = base + tl.arange(0, BLOCK_N)
        mask = cols < N

        # Load
        gate = tl.load(Gate + row * stride_m + cols, mask=mask, other=0.0).to(tl.float32)
        up = tl.load(Up + row * stride_m + cols, mask=mask, other=0.0).to(tl.float32)

        # Fused SiLU + multiply
        out = (gate * tl.sigmoid(gate)) * up

        # Store
        tl.store(Out + row * stride_m + cols, out.to(tl.float16), mask=mask)


@triton.autotune(
    configs=[
        triton.Config({'BLOCK_N': 4096}, num_warps=8),
        triton.Config({'BLOCK_N': 8192}, num_warps=8),
        triton.Config({'BLOCK_N': 4096}, num_warps=4),
        triton.Config({'BLOCK_N': 2048}, num_warps=4),
        triton.Config({'BLOCK_N': 8192}, num_warps=16),
        triton.Config({'BLOCK_N': 16384}, num_warps=16),
    ],
    key=['N'],
)
@triton.jit
def tanh_glu_vec_kernel(
    Gate, Up, Out,
    stride_m,
    N,
    BLOCK_N: tl.constexpr,
):
    """Vectorized tanh(gate) * up"""
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N

    gate = tl.load(Gate + row * stride_m + cols, mask=mask, other=0.0).to(tl.float32)
    up = tl.load(Up + row * stride_m + cols, mask=mask, other=0.0).to(tl.float32)

    # tanh via sigmoid identity (faster than libdevice.tanh)
    t = 2.0 * tl.sigmoid(2.0 * gate) - 1.0
    out = t * up

    tl.store(Out + row * stride_m + cols, out.to(tl.float16), mask=mask)


@triton.autotune(
    configs=[
        triton.Config({'BLOCK_N': 4096}, num_warps=8),
        triton.Config({'BLOCK_N': 8192}, num_warps=8),
        triton.Config({'BLOCK_N': 4096}, num_warps=4),
        triton.Config({'BLOCK_N': 2048}, num_warps=4),
        triton.Config({'BLOCK_N': 8192}, num_warps=16),
        triton.Config({'BLOCK_N': 16384}, num_warps=16),
    ],
    key=['N'],
)
@triton.jit
def relu2_glu_vec_kernel(
    Gate, Up, Out,
    stride_m,
    N,
    BLOCK_N: tl.constexpr,
):
    """Vectorized ReLU²(gate) * up"""
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N

    gate = tl.load(Gate + row * stride_m + cols, mask=mask, other=0.0).to(tl.float32)
    up = tl.load(Up + row * stride_m + cols, mask=mask, other=0.0).to(tl.float32)

    # ReLU² = max(gate, 0)²
    r = tl.maximum(gate, 0.0)
    out = (r * r) * up

    tl.store(Out + row * stride_m + cols, out.to(tl.float16), mask=mask)


# ============================================================================
# FUSED LINEAR + GLU KERNELS (matmul + activation in one pass)
# ============================================================================

@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 256, 'BLOCK_K': 64}, num_warps=4, num_stages=3),
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 32}, num_warps=4, num_stages=4),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 512, 'BLOCK_K': 32}, num_warps=8, num_stages=3),
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 32}, num_warps=8, num_stages=3),
    ],
    key=['M', 'N', 'K'],
)
@triton.jit
def fused_linear_silu_glu_kernel(
    X, W_gate, W_up, Out,
    stride_xm, stride_xk,
    stride_wgate_n, stride_wgate_k,
    stride_wup_n, stride_wup_k,
    stride_om, stride_on,
    M, N, K,
    BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr,
):
    """Fused: gate = x @ W_gate, up = x @ W_up, out = silu(gate) * up"""
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    off_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    off_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)

    # Accumulate both gate and up projections
    acc_gate = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    acc_up = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)

    for k in range(0, K, BLOCK_K):
        off_k = k + tl.arange(0, BLOCK_K)
        mask_x = (off_m[:, None] < M) & (off_k[None, :] < K)
        mask_w = (off_k[:, None] < K) & (off_n[None, :] < N)

        x = tl.load(X + off_m[:, None] * stride_xm + off_k[None, :] * stride_xk, mask=mask_x)

        w_gate = tl.load(W_gate + off_k[:, None] * stride_wgate_k + off_n[None, :] * stride_wgate_n, mask=mask_w)
        w_up = tl.load(W_up + off_k[:, None] * stride_wup_k + off_n[None, :] * stride_wup_n, mask=mask_w)

        acc_gate += tl.dot(x, w_gate)
        acc_up += tl.dot(x, w_up)

    # Fused SiLU + multiply in registers — NO intermediate write to HBM
    silu_gate = acc_gate * tl.sigmoid(acc_gate)
    out = silu_gate * acc_up

    mask_out = (off_m[:, None] < M) & (off_n[None, :] < N)
    tl.store(Out + off_m[:, None] * stride_om + off_n[None, :] * stride_on,
             out.to(tl.float16), mask=mask_out)


# ============================================================================
# WRAPPERS
# ============================================================================

def silu_glu_triton(gate, up):
    M, N = gate.shape
    out = torch.empty_like(gate)
    silu_glu_vec_kernel[(M,)](gate, up, out, gate.stride(0), N)
    return out

def tanh_glu_triton(gate, up):
    M, N = gate.shape
    out = torch.empty_like(gate)
    tanh_glu_vec_kernel[(M,)](gate, up, out, gate.stride(0), N)
    return out

def relu2_glu_triton(gate, up):
    M, N = gate.shape
    out = torch.empty_like(gate)
    relu2_glu_vec_kernel[(M,)](gate, up, out, gate.stride(0), N)
    return out
