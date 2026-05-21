<div class="domain-header">
  <span class="skill-badge content">Content</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process, Voice, Density</span>
</div>

# Learn

Structured study plans, topic guides, exam prediction, and active recall techniques.

## When to Use

- User says "teach me X", "how do I learn Y", "study plan for Z"
- User invokes `/learn`
- Preparing for an exam or interview

## Triggers

```
/learn [topic]
"teach me X", "how do I learn Y", "study plan for Z",
"prepare for exam", "learning path"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Generate a study plan</div>
<div class="example-desc">Create a structured learning path for a complex topic.</div>

```
/learn distributed systems for ML training

The agent generates:
- Week 1-2: Fundamentals (CAP theorem, consistency models,
  consensus protocols)
- Week 3-4: ML-specific (data parallelism, model parallelism,
  pipeline parallelism)
- Week 5-6: TPU/GPU specifics (SPMD, FSDPv2, Megatron-LM)
- Week 7-8: Hands-on (set up distributed training, debug
  common issues)
- Daily active recall questions
- Practice exercises with increasing difficulty
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Research-backed learning</div>
<div class="example-desc">Research the best resources before creating the plan.</div>

```
/researcher + /learn

Researcher finds the best current resources for learning
distributed ML: papers, courses, blog posts, GitHub repos.
Learn structures them into a progressive curriculum with
spaced repetition and active recall built in.
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Exam preparation</div>
<div class="example-desc">Prepare for a specific exam with targeted study.</div>

```
/learn prepare for ML systems design interview

The agent creates:
- Common question patterns (design a recommendation system,
  design a real-time fraud detector)
- Framework for answering (requirements → architecture →
  training → serving → monitoring)
- Practice problems with sample answers
- Key concepts to have ready (embedding tables, feature
  stores, model serving, A/B testing)
```
</div>
