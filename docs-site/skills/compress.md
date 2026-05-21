<div class="domain-header">
  <span class="skill-badge density">Density</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process</span>
</div>

# Compress

File-level compression at 4 intensity levels. Preserves all meaning and technical accuracy. Unlike Caveman (which changes how you speak), Compress changes how long documents are.

## When to Use

- User wants to reduce file size or token count
- User says "compress this", "reduce tokens", "shrink this file"
- User invokes `/compress`

## Triggers

```
/compress [lite|standard|aggressive|extreme]
"compress this", "reduce tokens", "shrink this", "make it smaller"
```

## Intensity Levels

| Level | Reduction | Description |
|-------|-----------|-------------|
| `lite` | ~30% | Light compression, maintains readability |
| `standard` | ~50% | Default. Good balance of size and clarity |
| `aggressive` | ~70% | Significant reduction, still meaningful |
| `extreme` | ~90% | Maximum compression, minimal readability |

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Compress a research summary</div>
<div class="example-desc">Reduce a long research document for quick distribution.</div>

```
/researcher → /compress standard

Researcher gathers 2000-word summary of latest MoE papers.
Compress standard reduces to ~1000 words. Key findings,
methodologies, and results preserved. Background sections
and redundant explanations removed.
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Archive-ready postmortem</div>
<div class="example-desc">Compress a postmortem for long-term storage.</div>

```
/postmortem → /compress aggressive

Full postmortem (1500 words) compressed to ~450 words.
Timeline preserved verbatim. Root cause and action items
intact. Narrative sections condensed to key points.
```
</div>

## Caveman vs Compress

| Aspect | Caveman | Compress |
|--------|---------|----------|
| Scope | Live responses | Files and documents |
| Style | Speaks like caveman | Normal prose, just shorter |
| Application | Real-time output | File processing |
| Personality | Has a character | Neutral |
