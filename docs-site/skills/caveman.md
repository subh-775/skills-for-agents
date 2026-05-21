<div class="domain-header">
  <span class="skill-badge density">Density</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process</span>
</div>

# Caveman

Ultra-compressed communication mode. Cuts token usage 30-95% while keeping full technical accuracy. Smart caveman — every extra word is a waste of heat.

## When to Use

- User says "caveman mode", "talk like caveman", "less tokens"
- User invokes `/caveman`
- Token efficiency is requested

## Triggers

```
/caveman [lite|full|ultra|extreme|symbolic]
"talk like caveman", "use caveman", "less tokens", "be brief"
```

## Intensity Levels

| Level | Compression | Use Case |
|-------|------------|----------|
| `lite` | ~30% | Slightly terse, still readable |
| `full` | ~50% | Default. Smart caveman. |
| `ultra` | ~75% | Maximum useful compression |
| `extreme` | ~90% | Barely readable, use with caution |
| `symbolic` | ~95% | Near-gibberish, for storage only |

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Compress a long explanation</div>
<div class="example-desc">User asks about distributed training. Caveman strips the fluff.</div>

**Before (normal):**
> So basically, when you're doing distributed training across multiple TPU pods, you need to think about how the data gets sharded across the devices. The way it works is that each pod processes a different batch of data, and then the gradients get synchronized across all the pods using all-reduce operations. This is actually quite different from how GPU training works because...

**After (`/caveman full`):**
> Distributed TPU training: data sharded across pods. Each pod processes different batch. Gradients sync via all-reduce. Different from GPU training — TPUs use SPMD, GPUs use data-parallel. Key: shard data, sync gradients, manage pod topology.
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Terse postmortem summary</div>
<div class="example-desc">Compress a postmortem report for quick distribution.</div>

```
/postmortem → /caveman ultra

Postmortem generates full report with timeline, root cause,
action items. Caveman ultra strips it to essentials:

"14:00 deploy pushed. 14:03 auth service crashed.
Root cause: null check missing in middleware.
Fix: added null guard. Deploy in 2min.
Action: add integration test for auth middleware.
Lesson: deploy canary first."
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Code comments compression</div>
<div class="example-desc">Apply caveman to code comments while keeping code syntax valid.</div>

**Before:**
```javascript
// This function calculates the optimal batch size based on
// available memory and the model's parameter count. It uses
// a heuristic approach to find the largest batch size that
// fits in memory without causing OOM errors.
function calculateBatchSize(memory, params) { ... }
```

**After (`/caveman`):**
```javascript
// Calc max batch size that fits memory. Heuristic, avoids OOM.
function calculateBatchSize(memory, params) { ... }
```
</div>

## Why It Works

Research shows brevity constraints improve large model accuracy by up to 26 percentage points while reducing tokens 45-75%. Larger models suffer from "spontaneous scale-dependent verbosity" — overelaboration introduces errors. Forcing concise responses removes this failure mode.

## Rules

- Apply compression to ALL text generation
- Exception: code syntax must be valid
- Don't change tone or personality (that's voice domain)
- Don't change factual content
