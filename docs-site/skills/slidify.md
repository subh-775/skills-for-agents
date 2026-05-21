<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Craft</span>
</div>

# Slidify

End-to-end PowerPoint presentation generator. JSON specs, templates, auto speaker notes, charts, diagrams, and animations.

## When to Use

- User says "make a presentation", "create slides", "generate pptx"
- User invokes `/slidify`
- Building slide decks from any content

## Triggers

```
/slidify
"make a presentation", "create slides", "generate pptx",
"make a deck", "export to pdf", "add watermark"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Generate a presentation from research</div>
<div class="example-desc">Research a topic, then create a slide deck about it.</div>

```
/researcher → /slidify

Researcher gathers findings on MoE architecture trends.
Slidify generates:
- Title slide with custom branding
- Executive summary (1 slide)
- Key findings (3-4 slides with charts)
- Architecture diagram (auto-generated)
- Comparison table (MoE vs dense models)
- Conclusion with next steps
- Speaker notes for every slide
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Create deck from project plan</div>
<div class="example-desc">Convert a PRD into a stakeholder presentation.</div>

```
/plan → /slidify

Planner creates a PRD for a new feature. Slidify converts it:
- Problem slide (user pain points)
- Solution overview (feature description)
- Architecture diagram (system design)
- Timeline slide (milestones and dates)
- Success metrics (KPIs and targets)
- Risks and mitigations
- Q&A slide
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Apply brand template</div>
<div class="example-desc">Use an existing brand template for consistent styling.</div>

```
/slidify apply brand template to this presentation

The agent applies:
- Company colors and fonts
- Logo placement (header/footer)
- Watermark if required
- Consistent slide transitions
- Branded chart colors
```
</div>

## Architecture

Slidify uses a two-layer architecture:

1. **Slide Spec (JSON)** — you write and edit this; humans can read and tweak it
2. **Code Layer (JS)** — generated from the spec; you run it

**Core philosophy:** 1 image > 2 slides of text. Visuals are processed 60,000x faster than text.
