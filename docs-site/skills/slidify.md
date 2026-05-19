# Slidify

End-to-end PowerPoint presentation generator. Structured JSON specs, template system, automatic speaker notes.

## Domain

**Process** — slide spec format, generation pipeline, export workflow, template system.

## When to Use

- `/slidify`
- "make a presentation", "create slides", "generate pptx", "make a deck"
- "export to pdf", "add watermark", "college logo on slides"
- "apply template", "slide deck for report"
- Any request involving `.pptx` files

## What It Creates

1. `slides.json` — AI-editable slide spec (single source of truth)
2. `output.pptx` — generated PowerPoint file
3. Optional: PDF, images via export script

## Architecture

Two-layer design:

- **Slide Spec (JSON)** — you write and edit this; humans can read and tweak it
- **Code Layer (JS)** — generated from the spec; you run it

Editing means editing JSON, not wrestling with pptxgenjs internals.

## Slide Types

| Type | Use For | Key Fields |
|------|---------|------------|
| `title` | Opening slide | `title`, `subtitle`, `presenter`, `affiliation`, `date` |
| `content` | General slides | `title`, `layout`, `items`/`stats`/`cards`/`steps`/`chart` |
| `section` | Section dividers | `title`, `subtitle` |
| `image-full` | Full-bleed image | `path`, `caption` |
| `closing` | Final slide | `title`, `contact`, `links` |

Content layouts: `bullets`, `two-column`, `image-right`, `image-left`, `cards`, `stats`, `timeline`, `chart`, `blank`

## Speaker Notes (Automatic)

**Every slide must have a `notes` field.** The AI generates speaker notes automatically based on slide content:

- Opening lines and talking points
- Emphasis cues ("pause on this stat")
- Transitions between slides
- Context for visuals and charts
- Q&A preparation hints

Notes appear in the PPTX notes panel during presentation mode.

## Template System

Templates live as JSON in `assets/templates/`. Built-in: `default`, `csvtu`, `conference`, `research-dark`, `minimal`, `corporate`.

Templates control: palette, fonts, watermarks, footers, slide-specific overrides.

## Workflow

1. Resolve template (user brand/university/default)
2. Write `slides.json` with speaker notes on every slide
3. `node scripts/gen_pptx.js slides.json` → output.pptx
4. Optional: `bash scripts/export.sh output.pptx pdf`
5. QA: text extraction + visual check

## Composability

```yaml
domain: process
composable: true
yields_to: [craft]
```

Process owns slide structure. Craft handles visual design decisions. Content skills provide the substance.

## Related Skills

- [Documenter](./documenter) — generate report content to convert into slides
- [Researcher](./researcher) — gather context for presentation content
- [Painter](./painter) — visual design guidance for templates
- [Blogger](./blogger) — write speaker notes in authentic voice
- [Learn](./learn) — study plans that can become slide decks

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/slidify/SKILL.md)
