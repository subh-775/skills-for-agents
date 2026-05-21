<div class="domain-header">
  <span class="skill-badge content">Content</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process, Voice, Density</span>
</div>

# Researcher

Deep web research. Diverse sources, cross-referencing, synthesis, and structured output.

## When to Use

- User says "research X", "find info about Y", "what's the latest on Z"
- Need current information about tech, libraries, frameworks
- Gathering context before writing or planning

## Triggers

```
"research X", "find info about Y", "what's the latest on Z",
"look up", "investigate", "gather context on"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Research a technical topic</div>
<div class="example-desc">Deep dive into a specific technology.</div>

```
/researcher what's the state of Mixture of Experts in 2026?

The agent searches multiple sources:
- Latest papers (Switch Transformer, GShard, DeepSeek-MoE)
- Blog posts from labs (Google, Meta, Mistral)
- GitHub repos with implementations
- Benchmark comparisons

Output: structured summary with citations, key findings,
open problems, and recommended reading.
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Research then document</div>
<div class="example-desc">Research a library, then write docs for it.</div>

```
/researcher + /documenter

Researcher surveys how similar libraries handle their API
design, error messages, and documentation. Documenter
applies these patterns to write docs that follow industry
conventions.
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Research then plan</div>
<div class="example-desc">Gather context before making architecture decisions.</div>

```
/researcher + /plan

Researcher compares CRDT vs OT vs hybrid approaches for
real-time collaboration. Planner uses the findings to
write an informed architecture decision record with
proper trade-off analysis.
```
</div>

## Source Evaluation

Evaluates sources on:
- **Authority** — who wrote it, what's their expertise
- **Currency** — when was it published/updated
- **Accuracy** — can claims be verified
- **Purpose** — why was it written
