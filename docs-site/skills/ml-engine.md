<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Density, Craft</span>
</div>

# ML Engine

TPU-first ML research engine for reproducible distributed training and ablation studies.

## When to Use

- User mentions TPU, distributed training, MoE, Pallas kernels
- User invokes `/ml`
- Working with PyTorch-XLA, JAX, SPMD, GSPMD

## Triggers

```
/ml [command]
TPU mentions, distributed training, MoE, Pallas, SPMD,
FSDPv2, multi-pod training, ablation studies
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Set up distributed training</div>
<div class="example-desc">Configure a TPU v5e pod for distributed training with proper sharding.</div>

```
/ml setup training on v5e-8 with FSDPv2

The agent generates:
- TPU topology configuration
- FSDPv2 sharding strategy (full-shard vs hybrid-shard)
- Data pipeline with proper sharding
- Checkpoint saving strategy
- Logging and metrics setup
- Reshard-on-resume logic
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Run ablation study</div>
<div class="example-desc">Systematic ablation on learning rate and batch size.</div>

```
/ml ablation learning_rate=[1e-4, 3e-4, 1e-3] batch_size=[128, 256, 512]

The agent generates:
- Config grid with all 9 combinations
- Launch script for parallel runs
- Results aggregation and comparison table
- Best config recommendation with confidence intervals
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Research-backed implementation</div>
<div class="example-desc">Research finds a technique, ML Engine implements it.</div>

```
/researcher + /ml-engine

Researcher finds the latest MoE routing paper with load
balancing improvements. ML Engine implements the router
as a Pallas kernel with proper gradient scaling and
auxiliary loss for balance.
```
</div>

## Capabilities

| Area | Coverage |
|------|----------|
| **TPU Training** | PyTorch-XLA, JAX, v5e, v2-8, v3-8 |
| **Distributed** | SPMD, GSPMD, FSDPv2, multi-pod |
| **MoE** | Mixture of Experts, router design, load balancing |
| **Kernels** | Pallas custom kernels, fused operations |
| **Experiments** | Ablation studies, hyperparameter sweeps |
