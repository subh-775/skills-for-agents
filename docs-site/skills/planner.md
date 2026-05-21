<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Density, Craft</span>
</div>

# Planner

Project plans with PRDs, design docs, architecture flows, and task breakdowns.

## When to Use

- User says "create a PRD", "design the architecture", "plan this project"
- User invokes `/plan`
- Breaking down complex tasks

## Triggers

```
/plan [optional: prd|design|architecture|tasks]
"create a PRD", "design the architecture", "plan this project"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Generate a PRD</div>
<div class="example-desc">Create a product requirements document for a new feature.</div>

```
/plan prd Add real-time collaboration to our code editor

The agent generates:
- Problem statement and user stories
- Functional requirements (CRDT-based sync, presence
  indicators, conflict resolution)
- Non-functional requirements (latency < 100ms, 100
  concurrent editors)
- Success metrics, risks, open questions
- Timeline with milestones
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Architecture design doc</div>
<div class="example-desc">Design the system architecture for a new service.</div>

```
/plan architecture Design a distributed cache layer

The agent produces:
- Component diagram (cache nodes, client SDK, invalidation)
- Data flow (write-through, read-through patterns)
- API contracts (get, set, delete, invalidate)
- Trade-offs: consistency vs availability
- Alternatives considered (Redis, Memcached, custom)
- Decision rationale with ADR format
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Research then plan</div>
<div class="example-desc">Research best practices before creating the plan.</div>

```
/researcher + /plan

Researcher surveys current best practices for real-time
collaboration (CRDTs, OT, hybrid approaches). Planner
uses findings to create an informed architecture doc
with proper trade-off analysis.
```
</div>
