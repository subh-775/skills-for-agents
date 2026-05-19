# TPU v5e — Setup, Best Practices, and Kaggle Integration

## Overview

TPU v5e (v5 lite) = cost-efficient training + inference accelerator. 2.3x price-perf vs v4 training, 2.7x inference. Primary target for <200B param models.

**Key specs per chip:**
- 197 TFLOPS BF16/FP16
- 393 TOPS INT8
- 16GB HBM (2x v3-8)
- 800 GiBps HBM bandwidth
- 400 GBps ICI bandwidth (bidirectional)

**Configurations:**
- Single-host: 1, 4, 8 chips (v5litepod-1, v5litepod-4, v5litepod-8)
- Multi-host training: 16, 32, 64, 128, 256 chips (v5litepod-16 to v5litepod-256)
- Pod size: 256 chips max, 2D torus interconnect

**Framework support:**
- JAX 0.4.6+
- TensorFlow 2.15+ (deprecated on v6e+)
- PyTorch 2.1+ (2.6.0 recommended)
- PJRT runtime ONLY (no XRT)

---

## GCP Setup

### 1. Request Quota

v5e requires quota. Contact Cloud Sales or use quota request form.

Quota types:
- On-demand: `TPUv5 lite pod cores for training per project per zone`
- Spot: `Preemptible TPU v5 lite pod cores for training per project per zone`
- Reserved: separate quota

### 2. Create TPU (Queued Resources — Best Practice)

```bash
export PROJECT_ID=your-project-id
export TPU_NAME=your-tpu-name
export ZONE=us-west4-a  # or us-east5-a, us-central2-b
export ACCELERATOR_TYPE=v5litepod-8
export RUNTIME_VERSION=v2-alpha-tpuv5-lite
export SERVICE_ACCOUNT=your-service-account@PROJECT_ID.iam.gserviceaccount.com
export QUEUED_RESOURCE_ID=your-queued-resource-id

# Create queued resource (recommended)
gcloud compute tpus queued-resources create ${QUEUED_RESOURCE_ID} \
   --node-id=${TPU_NAME} \
   --project=${PROJECT_ID} \
   --zone=${ZONE} \
   --accelerator-type=${ACCELERATOR_TYPE} \
   --runtime-version=${RUNTIME_VERSION} \
   --service-account=${SERVICE_ACCOUNT}

# Check status
gcloud compute tpus queued-resources describe ${QUEUED_RESOURCE_ID} \
   --project=${PROJECT_ID} \
   --zone=${ZONE}

# Wait for state: ACTIVE
```

### 3. Install PyTorch/XLA

```bash
gcloud compute tpus tpu-vm ssh ${TPU_NAME} \
   --project=${PROJECT_ID} \
   --zone=${ZONE} \
   --worker=all \
   --command='
      sudo apt-get update -y
      sudo apt-get install libomp5 libopenblas-dev -y
      pip install mkl mkl-include numpy
      pip install torch==2.6.0 torchvision torch_xla[tpu]==2.6.0 \
         -f https://storage.googleapis.com/libtpu-releases/index.html \
         -f https://storage.googleapis.com/libtpu-wheels/index.html'
```

### 4. Verify Setup

```bash
gcloud compute tpus tpu-vm ssh ${TPU_NAME} \
   --project=${PROJECT_ID} \
   --zone=${ZONE} \
   --worker=all \
   --command='
      export PJRT_DEVICE=TPU
      export TPU_LIBRARY_PATH=$HOME/.local/lib/python3.10/site-packages/libtpu/libtpu.so
      python3 -c "import torch_xla.core.xla_model as xm; print(xm.xla_device()); print(xm.get_xla_supported_devices())"'
```

Expected output:
```
xla:0
['xla:0', 'xla:1', 'xla:2', 'xla:3', 'xla:4', 'xla:5', 'xla:6', 'xla:7']
```

### 5. Delete Resources

```bash
# Delete TPU
gcloud compute tpus tpu-vm delete ${TPU_NAME} \
   --project=${PROJECT_ID} \
   --zone=${ZONE} \
   --quiet

# Delete queued resource
gcloud compute tpus queued-resources delete ${QUEUED_RESOURCE_ID} \
   --project=${PROJECT_ID} \
   --zone=${ZONE} \
   --quiet
```

---

## Kaggle TPU v5e Setup

Kaggle offers **free TPU v5e-8** (8 chips, single-host). UI shows "TPU VM v3-8" but backend is v5e.

### Enable TPU

1. Create new notebook
2. Settings → Accelerator → **TPU VM v3-8**
3. Verify v5e:

```python
import torch_xla.core.xla_model as xm
print(xm.get_tpu_env("TYPE", "unknown"))  # Should show v5e or v5litepod-8
```

### PyTorch/XLA on Kaggle

Kaggle pre-installs PyTorch/XLA. Verify:

```python
import torch
import torch_xla
import torch_xla.core.xla_model as xm

device = torch_xla.device()
print(f"Device: {device}")
print(f"Devices: {xm.get_xla_supported_devices()}")

# Test computation
t1 = torch.randn(3, 3, device=device)
t2 = torch.randn(3, 3, device=device)
print(t1 + t2)
```

### Kaggle Gotchas

**Issue: "TPU not found, using default strategy"**

TensorFlow detection fails on Kaggle v5e. Use PyTorch/XLA directly:

```python
# Don't use tf.distribute.TPUStrategy on Kaggle v5e
# Use torch_xla instead

import torch_xla
device = torch_xla.device()  # Works
```

**Issue: Slower than v3-8**

v5e has different memory hierarchy. Optimize batch size:

```python
# v3-8: batch_size = 32 per device
# v5e: batch_size = 64 per device (2x HBM)
```

**Issue: "Utilization is not currently available for TPU VMs"**

Kaggle doesn't expose TPU utilization metrics for v5e. Use XLA profiler:

```python
import torch_xla.debug.profiler as xp

server = xp.start_server(9012)
# Training loop
# Navigate to http://localhost:9012 in Kaggle notebook
```

---

## Training Loop (v5e-specific)

### Single-Host (v5e-8)

```python
import torch
import torch_xla
import torch_xla.core.xla_model as xm
from torch_xla import runtime as xr

device = torch_xla.device()
num_devices = xr.global_runtime_device_count()  # 8

model = MyModel().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

for epoch in range(num_epochs):
    for batch in train_loader:
        with torch_xla.step():
            inputs, labels = batch
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
    
    torch_xla.sync()  # End of epoch sync
```

### Multi-Host (v5litepod-16+)

```python
import torch_xla

def _mp_fn(index):
    device = torch_xla.device()
    model = MyModel().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    for epoch in range(num_epochs):
        for batch in train_loader:
            with torch_xla.step():
                inputs, labels = batch
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = loss_fn(outputs, labels)
                loss.backward()
                xm.optimizer_step(optimizer)  # all_reduce + step

if __name__ == '__main__':
    torch_xla.launch(_mp_fn, args=())
```

---

## SPMD on v5e

v5e supports SPMD (single-process multi-device). Better throughput than DDP.

```python
import torch_xla.distributed.spmd as xs
from torch_xla import runtime as xr
import numpy as np

xr.use_spmd()

num_devices = xr.global_runtime_device_count()  # 8
mesh = xs.Mesh(np.arange(num_devices), (num_devices,), ('data',))
xs.set_global_mesh(mesh)

# Scale batch size
batch_size = 32 * num_devices  # 256 total

# Shard input
from torch_xla.distributed import parallel_loader as pl

train_loader = pl.MpDeviceLoader(
    train_loader,
    device,
    input_sharding=xs.ShardingSpec(mesh, ('data', None, None, None))
)
```

---

## FSDPv2 on v5e

Large model training. Requires SPMD + mesh with `fsdp` axis.

```python
import torch_xla.distributed.spmd as xs
from torch_xla.experimental.spmd_fully_sharded_data_parallel import SpmdFullyShardedDataParallel as FSDPv2
from torch_xla import runtime as xr
from torch_xla.distributed.fsdp.wrap import transformer_auto_wrap_policy
import functools
import numpy as np

xr.use_spmd()
num_devices = xr.global_runtime_device_count()
mesh = xs.Mesh(np.arange(num_devices), (num_devices, 1), ('fsdp', 'model'))
xs.set_global_mesh(mesh)

auto_wrap_policy = functools.partial(
    transformer_auto_wrap_policy,
    transformer_layer_cls={DecoderLayer},
)
model = FSDPv2(model, auto_wrap_policy=auto_wrap_policy)
```

---

## Attention Kernels on v5e

v5e supports Splash Attention (via Pallas). Priority: Splash → Flash → SDPA.

```python
def get_attention_fn(tpu_type):
    if "v5" in tpu_type or "v4" in tpu_type or "v3" in tpu_type:
        try:
            from torch_xla.experimental.splash_attention import splash_attention
            return splash_attention
        except ImportError:
            pass
    try:
        from torch_xla.experimental.custom_kernel import flash_attention
        return flash_attention
    except ImportError:
        pass
    return torch.nn.functional.scaled_dot_product_attention

attention_fn = get_attention_fn("v5e")
```

---

## Best Practices

### 1. Batch Size

v5e has 16GB HBM per chip (2x v3-8). Scale batch size accordingly:

```python
# v3-8: batch_size = 32 per device → 256 global
# v5e-8: batch_size = 64 per device → 512 global
```

### 2. Compilation Cache

Persist HLO across restarts:

```python
import torch_xla.runtime as xr

xr.initialize_cache('/tmp/xla_cache', readonly=False)
```

### 3. Environment Variables

```bash
export PJRT_DEVICE=TPU
export PT_XLA_DEBUG=0
export USE_TORCH=ON
export XLA_USE_BF16=1  # Enable bfloat16
export LIBTPU_INIT_ARGS=--xla_jf_auto_cross_replica_sharding
export TPU_LIBRARY_PATH=$HOME/.local/lib/python3.10/site-packages/libtpu/libtpu.so
```

### 4. Queued Resources

Always use queued resources for production:

```bash
gcloud compute tpus queued-resources create ...
```

Benefits:
- Automatic retry on preemption
- Queue position visibility
- Guaranteed allocation when available

### 5. PyTorch Version

Use PyTorch 2.6.0 (latest stable with v5e support):

```bash
pip install torch==2.6.0 torch_xla[tpu]==2.6.0 \
   -f https://storage.googleapis.com/libtpu-releases/index.html
```

---

## Migration from v3-8 to v5e

### Code Changes

**None required.** v5e uses same PyTorch/XLA APIs as v3-8.

### Config Changes

```python
# Before (v3-8)
ACCELERATOR_TYPE = "v3-8"
RUNTIME_VERSION = "v2-alpha-tpuv3"
batch_size_per_device = 32

# After (v5e-8)
ACCELERATOR_TYPE = "v5litepod-8"
RUNTIME_VERSION = "v2-alpha-tpuv5-lite"
batch_size_per_device = 64  # 2x HBM
```

### Performance Expectations

- Training: 2.3x price-perf vs v4 (similar to v3-8 absolute speed, but cheaper)
- Inference: 2.7x price-perf vs v4
- LLM training: ~10-15% faster than v3-8 at same batch size
- Larger batch sizes possible (16GB vs 8GB HBM)

---

## Benchmarks

### ResNet-50 (ImageNet)

| Accelerator | Global Batch | Throughput (ex/s) |
|-------------|--------------|-------------------|
| v5litepod-4 | 32 | 4,240 |
| v5litepod-16 | 128 | 10,810 |
| v5litepod-64 | 512 | 46,154 |

### ViT (Imagenette)

| Accelerator | Global Batch | Throughput (ex/s) |
|-------------|--------------|-------------------|
| v5litepod-4 | 32 | 263 |
| v5litepod-16 | 128 | 429 |
| v5litepod-64 | 512 | 471 |

### Stable Diffusion (Pokémon)

| Accelerator | Global Batch | Throughput (ex/s) |
|-------------|--------------|-------------------|
| v5litepod-4 | 32 | 36.53 |
| v5litepod-16 | 64 | 43.71 |
| v5litepod-64 | 128 | 49.36 |

---

## Troubleshooting

### "No TPU devices found"

```bash
# Check TPU_LIBRARY_PATH
export TPU_LIBRARY_PATH=$HOME/.local/lib/python3.10/site-packages/libtpu/libtpu.so

# Verify libtpu
python3 -c "import torch_xla; print(torch_xla.__version__)"
```

### "PJRT not available"

v5e requires PJRT. XRT not supported.

```python
# Don't use XRT APIs
# xm.xla_device()  # Legacy

# Use PJRT APIs
torch_xla.device()  # Modern
```

### Slow compilation

Enable compilation cache:

```python
import torch_xla.runtime as xr
xr.initialize_cache('/tmp/xla_cache', readonly=False)
```

### OOM on v5e-8

v5e has 16GB HBM per chip. If OOM:

1. Reduce batch size
2. Enable gradient checkpointing
3. Use FSDPv2 for large models

```python
from torch_xla.distributed.fsdp import checkpoint_module
model = checkpoint_module(model)
```

---

## References

- [Official v5e docs](https://cloud.google.com/tpu/docs/v5e)
- [v5e training guide](https://cloud.google.com/tpu/docs/v5e-training)
- [PyTorch/XLA on v5e](https://cloud.google.com/tpu/docs/run-calculation-pytorch)
- [MLPerf v5e results](https://cloud.google.com/blog/products/compute/announcing-cloud-tpu-v5e-in-ga)
- [Kaggle TPU setup](https://www.geeksforgeeks.org/how-to-use-tpu-in-kaggle/)
