# GLU Activation Kernels — Complete Reference

## All GLU Variants Used in LLMs

| Variant | Formula | Used By |
|---------|---------|---------|
| SwiGLU | SiLU(gate) * up, SiLU(x) = x·σ(x) | Llama, Qwen, Mistral, Mixtral |
| tanhGLU | tanh(gate) * up | Some custom architectures |
| ReLU²GLU | ReLU(gate)² * up | Some custom architectures |
| GeGLU | GELU(gate) * up | GPT-NeoX, some BERT variants |
| GLU | σ(gate) * up | Original GLU paper |

## Triton Kernel Template

```python
import triton
import triton.language as tl

@triton.autotune(
    configs=[
        triton.Config({'BLOCK_N': 4096}, num_warps=8),
        triton.Config({'BLOCK_N': 8192}, num_warps=8),
        triton.Config({'BLOCK_N': 4096}, num_warps=4),
        triton.Config({'BLOCK_N': 2048}, num_warps=4),
    ],
    key=['N'],
)
@triton.jit
def glukernel(Gate, Up, Out, stride_m, N, BLOCK_N: tl.constexpr):
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_N)
    mask = cols < N
    gate = tl.load(Gate + row * stride_m + cols, mask=mask).to(tl.float32)
    up = tl.load(Up + row * stride_m + cols, mask=mask).to(tl.float32)
    # Replace with your activation:
    # SiLU: gate * tl.sigmoid(gate)
    # tanh: tl.math.tanh(gate)
    # ReLU²: tl.maximum(gate, 0.0) ** 2
    # GELU: 0.5 * gate * (1 + tl.math.tanh(0.7978845608 * (gate + 0.044715 * gate * gate * gate)))
    activated = gate * tl.sigmoid(gate)  # SiLU
    out = activated * up
    tl.store(Out + row * stride_m + cols, out.to(tl.float16), mask=mask)
```

## Fused Linear + GLU (Matmul + Activation)

Saves writing intermediate gate/up projections to HBM:
```python
# Instead of:
gate = x @ W_gate  # write to HBM
up = x @ W_up      # write to HBM
out = activation(gate) * up  # read from HBM

# Fuse into single kernel:
for k in range(0, K, BLOCK_K):
    x_tile = load(x)
    acc_gate += x_tile @ W_gate_tile
    acc_up += x_tile @ W_up_tile
# Activation in registers — no HBM write
out = activation(acc_gate) * acc_up
# Single write to HBM
```

## Performance Notes
- FP32 intermediate compute is mandatory for numerical stability
- tl.sigmoid, tl.math.tanh are native Triton intrinsics
- Vectorized loads (processing BLOCK_N elements at once) beat strided access
- For T4: 8 warps with BLOCK_N=4096-8192 is typically optimal
- Fused linear+GLU saves 2 memory round-trips (gate_out + up_out eliminated)
