# Nsight Compute (NCU) Profiling Quick Reference

## Essential Commands

```bash
# Full profiling (all metrics, one kernel)
ncu --set full -o profile ./harness

# Specific metrics only (faster)
ncu --metrics \
    sm__warps_active.avg.pct_of_peak_sustained_active,\
    gpu__time_duration.sum,\
    dram__throughput.avg.pct_of_peak_sustained_elapsed,\
    sm__throughput.avg.pct_of_peak_sustained_elapsed,\
    lts__throughput.avg.pct_of_peak_sustained_elapsed,\
    sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active \
    -o profile ./harness

# Export to CSV for analysis
ncu --csv --set full ./harness > profile.csv

# Filter by kernel name
ncu --kernel-name "matmul_kernel" --set full ./harness
```

## Key B200/Blackwell Metrics (sm_100)

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| `sm__warps_active.avg.pct_of_peak_sustained_active` | Warp occupancy | >70% |
| `dram__throughput.avg.pct_of_peak_sustained_elapsed` | Memory bandwidth util | >70% for mem-bound |
| `sm__throughput.avg.pct_of_peak_sustained_elapsed` | Compute throughput | >70% for compute-bound |
| `sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active` | Tensor core util | >50% |
| `lts__throughput.avg.pct_of_peak_sustained_elapsed` | L2 cache throughput | Context-dependent |
| `smsp__warps_issue_stalled_long_scoreboard.avg.pct` | Memory latency stalls | <20% |
| `smsp__warps_issue_stalled_wait.avg.pct` | Barrier/sync stalls | <10% |
| `smsp__warps_issue_stalled_not_selected.avg.pct` | Scheduler stalls | <15% |
| `sm__inst_executed_pipe_tensor.avg.pct` | Tensor core instruction % | >30% for TC kernels |

## A100/Hopper Metrics (sm_80/sm_90)

| Metric | A100 Name | Hopper Name |
|--------|-----------|-------------|
| Warp occupancy | `sm__warps_active.avg.per_cycle_active` | same |
| Memory util | `dram__bytes.sum.per_second` | same + TMA metrics |
| Tensor cores | `sm__pipe_tensor_op_hmma_cycles_active` | `sm__pipe_tensor_op_wmma_cycles_active` |
| L2 hit rate | `lts__t_sectors_hit_rate.pct` | same |
| Shared mem bank conflicts | `l1tex__data_bank_conflicts_pipe_lsu_mem_shared` | same |

## Diagnosis Decision Tree

```
Is kernel memory-bound or compute-bound?
├── Memory-bound (dram throughput > sm throughput)
│   ├── Low L2 hit rate?
│   │   ├── YES → Adjust tile size to fit L2 cache
│   │   └── NO → Check coalescing (dram__sectors_read vs dram__bytes_read)
│   │       ├── High ratio → Uncoalesced access (Pattern C)
│   │       └── Low ratio → True bandwidth limit, reduce data movement
│   ├── High long_scoreboard stalls?
│   │   └── YES → More warps for latency hiding (Pattern E)
│   └── Shared memory bank conflicts?
│       └── YES → Pad or swizzle shared memory (Pattern D)
│
└── Compute-bound (sm throughput > dram throughput)
    ├── Using tensor cores?
    │   ├── NO → Enable TC: aligned dims, use mma.sync/wmma (Pattern F)
    │   └── YES → Check TC utilization percentage
    │       ├── Low (<40%) → Pipeline bubbles (Pattern M) or register spilling (Pattern G)
    │       └── High → Already near optimal, look for algorithmic changes
    ├── Warp divergence?
    │   └── YES → Restructure branches (Pattern I)
    └── Occupancy limited?
        └── YES → Reduce registers/SMEM per CTA (Pattern J)
```

## Harness Template

```cuda
// Minimal harness for NCU profiling
#include <cuda_runtime.h>
#include <cstdio>

// Your kernel here
__global__ void kernel_to_profile(float* in, float* out, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        // kernel body
        out[idx] = in[idx] * 2.0f;
    }
}

int main() {
    int N = 1 << 20;
    float *d_in, *d_out;
    cudaMalloc(&d_in, N * sizeof(float));
    cudaMalloc(&d_out, N * sizeof(float));

    // Warmup
    for (int i = 0; i < 10; i++) {
        kernel_to_profile<<<(N+255)/256, 256>>>(d_in, d_out, N);
    }
    cudaDeviceSynchronize();

    // Profiled run
    kernel_to_profile<<<(N+255)/256, 256>>>(d_in, d_out, N);
    cudaDeviceSynchronize();

    cudaFree(d_in);
    cudaFree(d_out);
    return 0;
}
```

## Triton Profiling

```python
import torch
import triton
import triton.testing as tt
import triton.language as tl

# Basic benchmark
@triton.jit
def my_kernel(X, Y, N, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < N
    x = tl.load(X + offs, mask=mask)
    tl.store(Y + offs, x * 2.0, mask=mask)

N = 1 << 20
X = torch.randn(N, device='cuda')
Y = torch.empty_like(X)

# do_bench handles warmup + timing
ms = tt.do_bench(lambda: my_kernel[(N // 256,)](X, Y, N, BLOCK=256))
print(f"Time: {ms:.3f} ms")

# Torch profiler for detailed breakdown
with torch.profiler.profile(
    activities=[torch.profiler.ProfilerActivity.CUDA],
    record_shapes=True,
    profile_memory=True,
) as prof:
    my_kernel[(N // 256,)](X, Y, N, BLOCK=256)

print(prof.key_averages().table(sort_by="cuda_time_total"))
```
