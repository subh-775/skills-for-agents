# TPU Setup — v5e / v3-8 / v2-8 Detection and Mesh Initialization

## Device Detection

```python
import torch_xla
import torch_xla.core.xla_model as xm
from torch_xla import runtime as xr
import os

def detect_tpu():
    """Returns TPU version string and device count."""
    try:
        dev = torch_xla.device()  # Modern API
        tpu_type = xm.get_tpu_env("TYPE", os.environ.get("TPU_TYPE", "unknown"))
        num_devices = xr.global_runtime_device_count()  # SPMD-aware
        
        # Detect chip generation
        if "v5" in tpu_type:
            chip_gen = "v5"
            cores_per_chip = 1  # v5e: 1 TensorCore per chip
        elif "v4" in tpu_type:
            chip_gen = "v4"
            cores_per_chip = 2
        elif "v3" in tpu_type:
            chip_gen = "v3"
            cores_per_chip = 2
        elif "v2" in tpu_type:
            chip_gen = "v2"
            cores_per_chip = 2
        else:
            chip_gen = "unknown"
            cores_per_chip = 2
        
        return {
            "type": tpu_type,       # e.g. "v5litepod-8", "v3-8", "v2-8"
            "chip": chip_gen,       # e.g. "v5", "v3", "v2"
            "num_devices": num_devices,
            "cores_per_chip": cores_per_chip,
        }
    except Exception as e:
        return {"type": "none", "error": str(e)}
```

## Mesh Initialization

### 1D Mesh (Data Parallelism)

Default for single-host training (v5e-8, v3-8, v2-8).

```python
import numpy as np
from torch_xla.distributed.spmd import Mesh
from torch_xla import runtime as xr

num_devices = xr.global_runtime_device_count()
mesh = Mesh(np.arange(num_devices), (num_devices,), axis_names=("data",))

# Use for: batch dimension sharding, FSDP
```

### 2D Mesh (Data + Model Parallelism)

For larger models where single-core HBM is insufficient.

```python
import math
import numpy as np
from torch_xla.distributed.spmd import Mesh
from torch_xla import runtime as xr

num_devices = xr.global_runtime_device_count()
data_parallel = 4      # 4-way data parallel
model_parallel = 2     # 2-way tensor parallel

assert data_parallel * model_parallel == num_devices

mesh = Mesh(
    np.arange(num_devices),
    (data_parallel, model_parallel),
    axis_names=("data", "model"),
)
```

### Single-Host (v5e-8 / v3-8 / v2-8)

Single pod has 8 TPU cores visible to ONE process. No `spawn` needed.

```python
import torch_xla
from torch_xla import runtime as xr

num_devices = xr.global_runtime_device_count()
print(f"Visible TPU devices: {num_devices}")  # 8

# Model and data automatically use all devices via SPMD
# Just run: python train.py
```

### Multi-Host SPMD (Multi-Pod)

For TPU pod slices (v5litepod-16+, v3-32+, v2-32+) with MULTIPLE hosts.
Use `torch_xla.launch()` (modern) or `xmp.spawn()` (legacy).

```python
import torch_xla

def _mp_fn(index):
    device = torch_xla.device()
    # index: local process rank (0..7 per host)
    # Each host runs its own 8 processes
    # All processes coordinate via XLA collective ops
    # Training loop here

# Modern: torch_xla.launch (auto world_size)
if __name__ == '__main__':
    torch_xla.launch(_mp_fn, args=())

# Legacy: xmp.spawn (manual nprocs)
# xmp.spawn(_mp_fn, args=(), nprocs=8, start_method="fork")
```

**Key distinction:**
- **v5e-8 / v3-8 / v2-8**: Single host, 8 cores, 1 process. No `spawn`.
- **v5litepod-16+ / v3-32+ / v2-32+**: Multiple hosts, `torch_xla.launch()` per host. Each host launches 8 processes.

## TPU Version Comparison

| Feature | v2-8 | v3-8 | v5e-8 |
|--------|------|------|-------|
| Cores | 8 | 8 | 8 |
| HBM per core | 8 GB | 16 GB | 16 GB |
| Peak compute (BF16) | 45 TFLOPS | 123 TFLOPS | 197 TFLOPS |
| Peak compute (INT8) | 90 TOPS | 246 TOPS | 393 TOPS |
| HBM bandwidth | 600 GiBps | 900 GiBps | 800 GiBps |
| ICI bandwidth | 496 GBps | 656 GBps | 400 GBps |
| Splash Attention | No | Limited | Yes (via Pallas) |
| Flash Attention | Custom kernel | Custom kernel | Custom kernel |
| SDPA | Yes | Yes | Yes |
| PJRT | Yes | Yes | Yes (only) |
| XRT | Yes (legacy) | Yes (legacy) | No |

**Recommendation:**
- **v5e-8**: Primary target. Best price-perf, Kaggle free tier, 2x HBM vs v2-8.
- **v3-8**: Legacy quota. Use if v5e unavailable.
- **v2-8**: Deprecated. Migrate to v5e.

## Device Placement Patterns

```python
import torch_xla

# Explicit device placement
x = torch.randn(2, 16).to('xla')

# Check if tensor is on TPU
assert x.device.type == "xla"

# Synchronize (modern API)
torch_xla.sync()

# Or use context manager
with torch_xla.step():
    # ... operations ...
    pass
```

## Anti-Patterns

- Don't create mesh before confirming TPU is available — check `torch_xla.device()` first
- Don't assume 8 devices; check dynamically with `xr.global_runtime_device_count()`
- Don't mix `torch.cuda` calls with `torch_xla` — they are mutually exclusive backends
- Don't use `xm.xla_device()` — prefer `torch_xla.device()` (modern top-level API)
- Don't use `xm.mark_step()` — prefer `torch_xla.sync()` or `torch_xla.step()` context manager
- Don't use XRT APIs on v5e — PJRT only
