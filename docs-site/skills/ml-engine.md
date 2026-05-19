# ML Engine

TPU-first ML research engine for reproducible distributed training and ablation studies.

## Domain

**Process** — training workflow, distributed setup, evaluation loops.

## When to Use

- TPU mentions (v5e-8, v3-8, v3-64)
- `torch_xla`, JAX, distributed training
- MoE, router, Pallas, SPMD, GSPMD, FSDPv2
- `/ml`, `/ml-train`, `/ml-mesh`, `/ml-debug`

## Commands

| Command | Purpose |
|---------|---------|
| `/ml [idea]` | **Godmode** — full research scaffold |
| `/ml-train` | Generate training script |
| `/ml-mesh` | Generate mesh setup |
| `/ml-debug` | Debug XLA issues |
| `/ml-benchmark` | Benchmark attention kernel |
| `/ml-migrate` | Migrate old API → modern |
| `/ml-port` | Port PyTorch → torch_xla |
| `/ml-optimize` | Optimize XLA bottleneck |
| `/ml-plan` | Plan & template research |
| `/ml-ablate` | Run ablation matrix |
| `/ml-checkpoint` | Save/resume checkpoint |
| `/ml-profile` | Profile training bottleneck |

## What It Provides

- Modern `torch_xla` APIs (`torch_xla.step()`, `torch_xla.sync()`)
- SPMD / FSDPv2 setup
- Attention kernel selection (Splash, Flash, SDPA)
- Sharded data pipelines
- wandb logging on multi-host
- Reproducible ablation studies
- Pallas custom kernels

## Composability

```yaml
domain: process
composable: true
yields_to: [craft, voice]
```

## Related Skills

- [Researcher](./researcher) — finds prior work for ML research
- [Documenter](./documenter) — documents ML experiments

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/ml-engine/SKILL.md)
- [References](https://github.com/IsNoobgrammer/skills-for-agents/tree/main/ml-engine/references)
