# Triton Convolution Kernels — Complete Reference

> Sources: Triton Gluon (official), PyTorch Inductor, academic papers (implicit GEMM, Winograd).
> All code patterns extracted from production implementations.

## Overview

Convolution in Triton uses **implicit GEMM** — convolution is rewritten as matrix multiplication without materializing the im2col matrix. The key insight:

```
y[n, oh, ow, co] = Σ(r,s,cu) input[n, oh*stride+r-pad, ow*stride+s-pad, cu] * weight[co, r, s, cu]
```

This maps to GEMM as:
- **M** = N × out_h × out_w (output spatial positions)
- **N_gemm** = Co (output channels)
- **K** = R × S × Ci (reduction over filter × input channels)

---

## 1. Implicit GEMM with TMA im2col (Hopper/Blackwell)

The highest-performance approach. Uses NVIDIA TMA (Tensor Memory Access) hardware im2col mode for zero-overhead address generation.

### Core Algorithm

```python
# Pseudocode
for each M-tile (output positions):
    for each N-tile (output channels):
        acc = zeros(BLOCK_M, BLOCK_N)
        for r in range(R):
            for s in range(S):
                for ci_block in range(Ci // BLOCK_K):
                    # Input via TMA im2col — hardware does address gen + padding
                    tma.async_load_im2col(in_desc,
                        [batch, out_y*stride-pad, out_x*stride-pad, ci_block*BLOCK_K],
                        [r, s], barrier, a_smem)
                    # Weight via standard TMA
                    tma.async_load(weight_desc,
                        [co_start, r*S*Ci + s*Ci + ci_block*BLOCK_K],
                        barrier, b_smem)
                    acc += a_smem @ b_smem.T
        store output tile
```

### TMA im2col Descriptor Configuration

```python
from triton.experimental.gluon.nvidia.hopper import TensorDescriptorIm2Col

# Input: [N, H, W, Ci] in NHWC format
upper_h = (out_h - 1) * stride + 1 - H - padding
upper_w = (out_w - 1) * stride + 1 - W - padding

in_desc = TensorDescriptorIm2Col(
    base=input_nhwc,
    shape=[N, H, W, Ci],
    strides=input_nhwc.stride(),
    block_shape=[BLOCK_M, BLOCK_K],
    layout=NVMMASharedLayout.get_default_for([BLOCK_M, BLOCK_K], dtype),
    padding="zero",                    # TMA fills OOB with 0
    element_strides=[1, stride, stride, 1],  # Step by conv stride
    pixel_box_lower_corner=[-padding, -padding],
    pixel_box_upper_corner=[upper_h, upper_w],
)
```

**Key parameters:**
- `element_strides=[1, stride, stride, 1]` — TMA steps by convolution stride between output positions
- `pixel_box_lower_corner=[-padding, -padding]` — spatial window starts at -padding
- `pixel_box_upper_corner` — computed to cover exactly out_h × out_w pixels per batch
- `padding="zero"` — out-of-bounds reads return 0 automatically (conv zero-padding)

### Weight Reshape

```python
# Weight: [Co, R, S, Ci] -> [Co, R*S*Ci] for 2D TMA
weight_2d = weight.reshape(Co, R * S * Ci)
weight_desc = TensorDescriptor.from_tensor(weight_2d, [BLOCK_N, BLOCK_K], layout)
```

### M-Offset Decomposition

```python
# Map flat M index to (batch, out_y, out_x)
offs_m = pid_m * BLOCK_M
batch_id = offs_m // (out_h * out_w)
m_residual = offs_m % (out_h * out_w)
out_y = m_residual // out_w
out_x = m_residual % out_w
```

### TMA Load in K-Loop

```python
for k_iter in range(R * S * cdiv(Ci, BLOCK_K)):
    ci_block = k_iter % ci_num_blocks
    rs_idx = k_iter // ci_num_blocks
    r, s = rs_idx // S, rs_idx % S

    # Input tile via TMA im2col
    tma.async_load_im2col(in_desc,
        [batch_id, out_y * stride_h - pad_h, out_x * stride_w - pad_w, ci_block * BLOCK_K],
        [r.to(tl.int16), s.to(tl.int16)],
        barrier, a_smem)

    # Weight tile via standard TMA
    k_offset = r * S * Ci + s * Ci + ci_block * BLOCK_K
    tma.async_load(weight_desc, [pid_n * BLOCK_N, k_offset], barrier, b_smem)

    mbarrier.wait(barrier, phase)
    acc += tl.dot(a_smem, b_smem.T)
    phase ^= 1
```

---

## 2. Warp-Specialized Convolution (Production)

From Triton Gluon `02-conv-fprop.py`. Three warp-specialized partitions:

### Load Partition
```python
@gluon.jit
def load_partition(p):
    state = Counter.create(1, num_buffers)
    for idx in range(num_tiles):
        prog = config.get_program(tile_id)
        batch_id, out_y, out_x = prog.get_m_offsets()
        for k_iter in range(num_k_iter):
            # Compute (r, s, ci_block) from k_iter
            mbarrier.wait(empty_bars[state.index], state.phase)
            mbarrier.expect(ready_bar, in_block_nbytes + weight_block_nbytes)
            tma.async_load_im2col(...)
            tma.async_load(...)
            state = state.next()
```

### MMA Partition
```python
@gluon.jit
def mma_partition(p):
    load_state = Counter.create(0, num_buffers)
    acc_state = Counter.create(1, num_acc_buffers)
    for idx in range(num_tiles):
        mbarrier.wait(acc_empty_bars[acc_state.index], acc_state.phase)
        use_acc = False
        for k_iter in range(num_k_iter):
            mbarrier.wait(load_ready_bars[load_state.index], load_state.phase)
            tcgen05_mma(a_bufs[load_state.index], b_bufs[load_state.index].permute((1,0)),
                       acc_buf, use_acc=use_acc)
            tcgen05_commit(load_empty_bars[load_state.index])
            load_state = load_state.next()
            use_acc = True
        tcgen05_commit(acc_ready_bars[acc_state.index])
```

### Epilogue Partition
```python
@gluon.jit
def epilogue_partition(p):
    for idx in range(num_tiles):
        mbarrier.wait(acc_ready_bars[acc_state.index], acc_state.phase)
        acc = acc_bufs[acc_state.index].load()
        result = gl.convert_layout(acc.to(bf16), gl.CoalescedLayout())
        mbarrier.arrive(acc_empty_bars[acc_state.index], count=1)
        # Scatter store to NHWC output
        c_offsets = batch[:,None]*stride_n + out_y[:,None]*stride_h + out_x[:,None]*stride_w + co[None,:]
        gl.store(output_ptr + c_offsets, result, mask=mask)
```

### Autotuning Configs

```python
configs = [
    triton.Config({'BLOCK_M': bm, 'BLOCK_N': bn, 'BLOCK_K': 64,
                   'GROUP_SIZE_M': 4, 'num_buffers': nb, 'num_acc_buffers': 2},
                  num_warps=4)
    for bm in (64, 128)
    for bn in (8, 32, 128, 256)
    for nb in (3, 4, 5)
]
# Key: out_h, out_w, stride_h, stride_w (not full input shape)
```

---

## 3. PyTorch Inductor Conv2d Template

Simpler approach (no TMA, works on all GPUs). Uses `tl.dot` for the inner product.

### Forward Pass (Implicit GEMM)

```python
# Grid: (cdiv(N*H*W, BLOCK_M), cdiv(Co, BLOCK_N), GROUPS)
nhw = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
idx_y_w = nhw % OUT_W
nh = nhw // OUT_W
idx_y_h = nh % OUT_H
idx_n = nh // OUT_H
idx_y_c = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)

acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)

for ijk in range(KERNEL_H * KERNEL_W * BLOCK_K_COUNT):
    k = (ijk % BLOCK_K_COUNT) * BLOCK_K
    ij = ijk // BLOCK_K_COUNT
    i = ij // KERNEL_W
    j = ij % KERNEL_W

    # Load input patch with bounds checking
    idx_x_h = i - PADDING_H + idx_y_h * STRIDE_H
    idx_x_w = j - PADDING_W + idx_y_w * STRIDE_W
    idx_x_c = tl.arange(0, BLOCK_K) + k
    mask_x = (idx_n < BATCH) & (idx_x_h >= 0) & (idx_x_h < IN_H) & ...
    matrix_x = tl.load(x_ptrs, mask=mask_x, other=0.0)

    # Load weight
    mask_w = (idx_x_c[:,None] < GROUP_IN_C) & (idx_y_c[None,:] < GROUP_OUT_C)
    matrix_w = tl.load(w_ptrs, mask=mask_w, other=0.0)

    acc += tl.dot(matrix_x, matrix_w, allow_tf32=True)
```

### Depthwise Conv1d (NLC Layout)

For groups == in_channels == out_channels (each channel independent):

```python
# Grid: (cdiv(BATCH, BLOCK_N), cdiv(OUT_L, BLOCK_L), cdiv(CHANNELS, BLOCK_C))
# 3D tiling: BLOCK_N × BLOCK_L × BLOCK_C

acc = tl.zeros((BLOCK_N, BLOCK_L, BLOCK_C), dtype=tl.float32)

for k in range(KERNEL_SIZE):
    # Load weight for this kernel position (broadcast across N, L)
    wk = tl.load(W + c_offs * stride_wc + k * stride_wk, mask=c_mask, other=0.0)

    # Compute input positions with stride/padding
    l_in = l_offs * CONV_STRIDE - PADDING + k
    mask_in = (l_in >= 0) & (l_in < IN_L)

    # Load input with bounds checking
    x_vals = tl.load(X + in_base + l_in[None,:,None] * stride_xl,
                      mask=n_mask[None,:,None] & mask_in[None,:,None] & c_mask, other=0.0)

    acc += x_vals * wk[None, None, :]  # element-wise multiply (depthwise)
```

### Backward Pass (dgrad — Input Gradient)

```python
# grad_X[M, Ci] = im2col(grad_Y)[M, R*S*Co] @ W_rot[R*S*Co, Ci]^T
# Where W_rot = weight flipped and permuted

# For each input position, find which output positions contribute
yhn = h_i[:,None] + PADDING_H - i_k[None,:] * DILATION_H
ywn = w_i[:,None] + PADDING_W - j_k[None,:] * DILATION_W

# Check if valid (divisible by stride)
div_ok_h = (yhn >= 0) & (yhn <= (OUT_H-1)*STRIDE_H) & ((yhn % STRIDE_H) == 0)
yh = tl.where(div_ok_h, yhn // STRIDE_H, 0)

# Load grad_output and weight, accumulate via tl.dot
mat_dy = tl.load(dy_ptrs, mask=mask_dy, other=0.0)
mat_w = tl.load(w_ptrs, mask=mask_w, other=0.0)
acc += tl.dot(mat_dy, mat_w, allow_tf32=True)
```

### Backward Pass (wgrad — Weight Gradient)

```python
# grad_W[Co, R*S*Ci] = grad_out[M, Co]^T @ im2col(input)[M, R*S*Ci]
# M = N * out_h * out_w (spatial positions — reduction dimension)

# MMA tiling:
#   BLOCK_M = tile over Co (rows of grad_weight)
#   BLOCK_N = tile over Ci per (r,s) (cols of grad_weight)
#   BLOCK_K = tile over spatial (reduction)
```

---

## 4. Dgrad Subproblem Decomposition (Stride > 1)

From Triton Gluon `02-conv-dgrad.py`. For stride > 1, dgrad decomposes into stride_h × stride_w subproblems:

```python
def make_dgrad_subproblem_specs(R, S, stride_h, stride_w, pad_h, pad_w):
    p_h_prime = R - 1 - pad_h
    p_w_prime = S - 1 - pad_w
    subproblems = []
    for a in range(stride_h):
        for b in range(stride_w):
            r0 = ((p_h_prime - a) % stride_h + stride_h) % stride_h
            s0 = ((p_w_prime - b) % stride_w + stride_w) % stride_w
            R_eff = (R - r0 + stride_h - 1) // stride_h
            S_eff = (S - s0 + stride_w - 1) // stride_w
            if R_eff > 0 and S_eff > 0:
                offset_a = (a + r0 - p_h_prime) // stride_h
                offset_b = (b + s0 - p_w_prime) // stride_w
                subproblems.append((a, b, r0, s0, R_eff, S_eff, offset_a, offset_b))
    return subproblems
```

Each subproblem:
- Fixes (sub_a, sub_b, r0, s0, R_eff, S_eff)
- Builds a grad_Y im2col descriptor with shifted offsets
- Launches the persistent kernel once
- Epilogue scatters results to `h = sub_a + out_y * stride_h`

### Split-K for Dgrad

When K dimension is large, split across multiple CTAs and reduce:

```python
# Split-K reduction kernel
@triton.jit
def reduce_split_k_partials_kernel(partial_ptr, output_ptr, ...):
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    for split_k_idx in range(ACTIVE_SPLIT_K):
        partial_offsets = (split_k_idx * N + batch_idx)[:,None] * stride + ...
        acc += tl.load(partial_ptr + partial_offsets, mask=mask, other=0.0)
    tl.store(output_ptr + output_offsets, acc, mask=mask)
```

---

## 5. Autotuning Strategy for Convolution

### Key Dimensions to Tune

| Parameter | Typical Range | Impact |
|-----------|--------------|--------|
| BLOCK_M | 64, 128 | Output spatial tile |
| BLOCK_N | 8, 32, 64, 128, 256 | Output channel tile |
| BLOCK_K | 64 | Reduction tile (Ci per iter) |
| GROUP_SIZE_M | 4 | L2 cache locality |
| num_buffers | 3, 4, 5 | Pipeline depth |
| num_acc_buffers | 2 | Accumulator buffering |
| num_warps | 4 | Warp count |
| SPLIT_K | 1, 2, 4, 8 | K-dimension parallelism (dgrad/wgrad only) |

### Autotune Key Selection

```python
# For fprop: key on effective geometry, not raw input shape
key=["out_h", "out_w", "stride_h", "stride_w"]

# For dgrad/wgrad: key on full problem shape
key=[device_capability, num_sms, N, Co, Ci, S, out_h, out_w, H_in, W_in, ...]
```

### TMA Block Size Hook

```python
def tma_set_block_size_hook(nargs):
    """Update TMA descriptors when autotune changes block sizes."""
    in_block_shape = [nargs["BLOCK_M"], nargs["BLOCK_K"]]
    weight_block_shape = [nargs["BLOCK_N"], nargs["BLOCK_K"]]
    nargs["in_desc"].block_shape = in_block_shape
    nargs["in_desc"].layout = NVMMASharedLayout.get_default_for(in_block_shape, dtype)
    nargs["weight_desc"].block_shape = weight_block_shape
    nargs["weight_desc"].layout = NVMMASharedLayout.get_default_for(weight_block_shape, dtype)
```

---

## 6. Channel Padding for TMA Alignment

TMA requires 16-byte aligned strides. For narrow channels (e.g., RGB Ci=3):

```python
def maybe_pad_channel_dims_for_tma(*tensors, alignment_bytes=16):
    elem_bytes = tensors[0].element_size()
    channel_alignment = alignment_bytes // elem_bytes
    orig_channels = tensors[0].shape[-1]
    padded_channels = cdiv(orig_channels, channel_alignment) * channel_alignment
    if padded_channels == orig_channels:
        return tensors
    padded = tensor.new_zeros((*tensor.shape[:-1], padded_channels))
    padded[..., :orig_channels] = tensor
    return padded.contiguous()
```

---

## 7. Convolution Types and When to Use Each

| Type | Use Case | Triton Approach |
|------|----------|-----------------|
| **Conv2d forward** | Training/inference | Implicit GEMM + TMA im2col |
| **Conv2d dgrad** | Training backward (input) | Subproblem decomposition + split-K |
| **Conv2d wgrad** | Training backward (weight) | grad_out^T @ im2col(input) |
| **Depthwise conv1d** | Efficient attention, SSMs | Direct 3D tiling (NLC) |
| **Depthwise conv2d** | MobileNet, EfficientNet | Direct per-channel multiply |
| **Grouped conv** | ResNeXt, shufflenet | Loop over groups in kernel |
| **Conv1d** | Audio, 1D sequence models | Same as conv2d but 1D |
| **Conv3d** | Video, 3D medical imaging | 5D implicit GEMM |
| **Transposed conv** | GANs, segmentation | Modified dgrad with output padding |

---

## 8. Fused Convolution Patterns

### Conv + Bias + ReLU

```python
# In epilogue, after MMA accumulation:
acc = acc_bufs[acc_state.index].load()
result = gl.convert_layout(acc.to(bf16), gl.CoalescedLayout())
# Add bias (broadcast across spatial dim)
result = result + bias[None, :]  # bias shape: [Co]
# ReLU
result = gl.maximum(result, gl.zeros_like(result))
gl.store(output_ptr + offsets, result, mask=mask)
```

### Conv + BatchNorm (Eval Mode)

```python
# Fuse BN into conv weights (pre-computed on host):
# W_fused = W * (gamma / sqrt(var + eps))
# b_fused = (b - running_mean) * gamma / sqrt(var + eps) + beta
# Then conv kernel uses W_fused, b_fused — no separate BN kernel needed
```

### Conv + SiLU (for BiBo's conv layers)

```python
# SiLU(x) = x * sigmoid(x)
# In epilogue:
result = gl.convert_layout(acc.to(bf16), gl.CoalescedLayout())
result = result * gl.sigmoid(result)
gl.store(output_ptr + offsets, result, mask=mask)
```

### Conv + Residual Add

```python
# Load existing residual, add conv output
residual = gl.load(residual_ptr + offsets, mask=mask, other=0.0)
result = gl.convert_layout(acc.to(bf16), gl.CoalescedLayout()) + residual
gl.store(output_ptr + offsets, result, mask=mask)
```

---

## 9. Optimization Patterns

### Multi-Buffering

```python
# Triple-buffer loads to overlap compute and memory
num_buffers = 3  # or 4, 5
a_bufs = gl.allocate_shared_memory(dtype, [num_buffers, BLOCK_M, BLOCK_K], layout)
b_bufs = gl.allocate_shared_memory(dtype, [num_buffers, BLOCK_N, BLOCK_K], layout)
load_empty_bars = gl.allocate_shared_memory(gl.int64, [num_buffers, 1], MBarrierLayout())
load_ready_bars = gl.allocate_shared_memory(gl.int64, [num_buffers, 1], MBarrierLayout())
```

### Persistent Tile Scheduling

```python
# Distribute tiles across CTAs, each CTA processes multiple tiles
@gluon.jit
def PersistentTileScheduler.initialize(num_tiles):
    kernel_id = gl.program_id(axis=0)
    num_kernels = gl.num_programs(axis=0)
    pid_per_kernel = gl.cdiv(num_tiles, num_kernels)
    pid_start = kernel_id * pid_per_kernel
    pid_end = gl.minimum(pid_start + pid_per_kernel, num_tiles)
```

### Grouped Tile Ordering (L2 Cache)

```python
# Reorder tile IDs so nearby CTAs process spatially adjacent tiles
num_pid_in_group = GROUP_SIZE_M * num_pid_n
group_id = pid // num_pid_in_group
first_pid_m = group_id * GROUP_SIZE_M
group_size_m = gl.minimum(num_pid_m - first_pid_m, GROUP_SIZE_M)
pid_m = first_pid_m + (pid % group_size_m)
pid_n = (pid % num_pid_in_group) // group_size_m
```

### Warp Specialization (Hopper/Blackwell)

```python
# 3 partitions: epilogue(1 warp), MMA(1 warp), loads(24 warps)
gl.warp_specialize([
    (epilogue_partition, (p,)),
    (mma_partition, (p,)),
    (load_partition, (p,)),
], [1, 1], [24, 24])
```

---

## 10. Common Pitfalls

### Pitfall 1: NCHW vs NHWC Layout
```
PyTorch default: NCHW
Triton/TMA: NHWC (required for efficient channel-last access)
Solution: permute(0, 2, 3, 1).contiguous() before kernel
```

### Pitfall 2: Weight Layout
```
PyTorch: [Co, Ci, R, S] (OIHW)
Triton: [Co, R, S, Ci] (ORSC) -> reshape to [Co, R*S*Ci]
Solution: weight.permute(0, 2, 3, 1).contiguous()
```

### Pitfall 3: Channel Alignment for TMA
```
Ci=3 (RGB) is not 16-byte aligned for bf16 (needs 8 elements)
Solution: pad channels to 8, then slice output
```

### Pitfall 4: Asymmetric Strides
```
stride=(1,2) requires separate handling
Solution: normalize_2d() to handle int/tuple/list
```

### Pitfall 5: Dgrad with stride > 1
```
Single kernel launch gives wrong results for stride > 1
Solution: decompose into stride_h × stride_w subproblems
```

### Pitfall 6: Split-K Workspace Indexing
```
Very large workspaces exceed 32-bit indexing
Solution: check workspace_elems < 2^31 - 1 before launch
```

---

## 11. Benchmarking Convolution

```python
def benchmark_conv(fn, N, H, W, Ci, Co, R, S, stride, padding):
    ms = triton.testing.do_bench(fn)
    out_h = (H + 2*padding - R) // stride + 1
    out_w = (W + 2*padding - S) // stride + 1
    flops = 2.0 * N * out_h * out_w * Co * Ci * R * S
    tflops = flops * 1e-12 / (ms * 1e-3)
    return tflops
```

### Reference Performance (Triton Gluon on H100)

| Shape | Config | TFLOPS |
|-------|--------|--------|
| N=128, Ci=384, Co=384, 64×64, 3×3, s=1, p=1 | autotuned | ~700+ |
| N=128, Ci=384, Co=384, 64×64, 3×3, s=2, p=1 | autotuned | ~600+ |
| N=1, Ci=384, Co=384, 64×64, 3×3, s=1, p=1 | autotuned | ~200+ |

---

## 12. Key Sources

| Source | URL | What |
|--------|-----|------|
| Triton Gluon fprop | `triton-lang/triton/python/examples/gluon/02-conv-fprop.py` | Production conv2d forward |
| Triton Gluon dgrad | `triton-lang/triton/python/examples/gluon/02-conv-dgrad.py` | Input gradient |
| Triton Gluon wgrad | `triton-lang/triton/python/examples/gluon/02-conv-wgrad.py` | Weight gradient |
| Triton im2col tutorial | `triton-lang/triton/python/tutorials/gluon/13-conv-im2col.py` | TMA im2col fundamentals |
| PyTorch Inductor conv | `pytorch/pytorch/torch/_inductor/kernel/conv.py` | Template-based conv |
| PyTorch depthwise conv | `pytorch/pytorch/torch/_inductor/kernel/templates/triton_depthwise_conv.py.jinja` | Depthwise conv1d |
| PyTorch dgrad template | `pytorch/pytorch/torch/_inductor/kernel/templates/triton_conv2d_bwd_input.py.jinja` | Backward input |
| PyTorch wgrad template | `pytorch/pytorch/torch/_inductor/kernel/templates/triton_conv2d_bwd_weight.py.jinja` | Backward weight |
