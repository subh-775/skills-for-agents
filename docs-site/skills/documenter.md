<div class="domain-header">
  <span class="skill-badge content">Content</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process, Craft</span>
</div>

# Documenter

Comprehensive documentation engine. Writes docs that developers actually read — structured, searchable, example-rich.

## When to Use

- User says "document this", "write docs", "create documentation"
- User wants README, API reference, or user guide
- User wants a documentation website

## Triggers

```
"document this", "write docs", "create documentation",
"API docs", "README", "user guide", "doc site"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Document a codebase</div>
<div class="example-desc">Generate full documentation for a project.</div>

```
/documenter document this CLI tool

The agent generates:
- README.md with badges, quickstart, one working example
- Getting Started guide (install → first command in <5 min)
- CLI reference (every command, every flag)
- Configuration guide
- Troubleshooting (symptom-first, copy-paste fixes)
- Contributing guide
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Research-backed documentation</div>
<div class="example-desc">Research the domain before writing docs.</div>

```
/researcher + /documenter

Researcher gathers context on how similar tools document
their APIs (Docusaurus, MkDocs, VitePress patterns).
Documenter uses findings to structure docs that follow
industry conventions while being specific to this project.
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Terse documentation</div>
<div class="example-desc">Document then compress for minimal docs.</div>

```
/documenter + /caveman lite

Documenter writes comprehensive API docs. Caveman lite
removes verbose explanations while keeping all technical
details, examples, and structure intact.
```
</div>

## Documentation Hierarchy

```
Getting Started (zero to first success)
  ↓
Guides (common use cases, patterns)
  ↓
API Reference (complete technical spec)
  ↓
Advanced (optimization, edge cases, internals)
```
