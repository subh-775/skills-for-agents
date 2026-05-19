# Slide Spec Reference

The **slide spec** is the AI-editable JSON that drives all PPTX generation.
Write this, not raw pptxgenjs code. The generator handles layout math, template
injection, and pptxgenjs quirks automatically.

---

## Top-Level Schema

```json
{
  "meta": {
    "title": "Presentation Title",
    "author": "Your Name",
    "template": "csvtu-research",
    "output": "output.pptx",
    "layout": "16x9"
  },
  "slides": [ ...slide objects... ]
}
```

`layout` options: `"16x9"` (default, 10x5.625"), `"16x10"`, `"4x3"`, `"wide"`

---

## Slide Types

### `title` — Opening / section title slide

```json
{
  "type": "title",
  "title": "TokenAdapt: Efficient Hindi Tokenization",
  "subtitle": "arXiv:2505.09738 · May 2025",
  "presenter": "Shaurya Sharthak",
  "affiliation": "CSVTU Bhilai · TinyCompany AI",
  "date": "May 2026"
}
```

All fields except `title` are optional.

---

### `content` — General content slide

```json
{
  "type": "content",
  "title": "Key Results",
  "layout": "bullets",
  "items": [
    "4x better Hindi token efficiency vs Phi-4",
    "~2x perplexity improvement (TokenAdapt)",
    "QTK-81K: best Hindi tokenizer at 7B scale"
  ],
  "notes": "OPEN: Here are the headline results.\n- 4x efficiency: this is our core claim, backed by benchmark data.\n- ~2x perplexity: TokenAdapt halves the gap to English-quality models.\n- QTK-81K: our vocabulary, trained specifically for Hindi.\nEMPHASIS: Pause on the 4x stat.\nTRANSITION: Now let's look at the architecture..."
}
```

**Every slide must have a `notes` field.** See the "Speaker Notes" section below for guidelines.

`layout` options for content slides:

| layout | Description |
|--------|-------------|
| `"bullets"` | Single-column bullet list |
| `"two-column"` | `left` + `right` sub-blocks |
| `"image-right"` | Text left, image right (40% width) |
| `"image-left"` | Image left, text right |
| `"cards"` | 2-4 card grid, each card has `title` + `body` |
| `"stats"` | Big number callouts, use `stats` array |
| `"timeline"` | Horizontal steps, use `steps` array |
| `"blank"` | No auto-layout; use `shapes` array for manual |

---

### Two-column layout

```json
{
  "type": "content",
  "title": "Architecture",
  "layout": "two-column",
  "left": {
    "type": "bullets",
    "items": ["SuperTokenizer core", "XLA-optimized attention", "GSPMD sharding"]
  },
  "right": {
    "type": "image",
    "path": "assets/architecture.png",
    "alt": "Architecture diagram"
  }
}
```

`left`/`right` block types: `bullets`, `image`, `stats`, `text`, `chart`

---

### Stats callout slide

```json
{
  "type": "content",
  "title": "Impact",
  "layout": "stats",
  "stats": [
    { "value": "4x",   "label": "Hindi token efficiency" },
    { "value": "155+", "label": "HuggingFace models" },
    { "value": "25M+", "label": "Dataset rows" },
    { "value": "234",  "label": "GitHub stars" }
  ]
}
```

Up to 4 stats in a row. Values render at 60pt, labels at 14pt.

---

### Chart slide

```json
{
  "type": "content",
  "title": "Perplexity Comparison",
  "layout": "chart",
  "chart": {
    "kind": "bar",
    "labels": ["Phi-4 Tokenizer", "LLaMA Tokenizer", "TokenAdapt (ours)"],
    "series": [
      { "name": "Hindi Perplexity", "values": [48.2, 52.1, 24.6] }
    ],
    "colors": ["CADCFC", "CADCFC", "2563EB"],
    "yAxisTitle": "Perplexity (lower = better)"
  }
}
```

`kind` options: `bar`, `column`, `line`, `pie`, `doughnut`, `scatter`, `area`

---

### Timeline slide

```json
{
  "type": "content",
  "title": "Research Timeline",
  "layout": "timeline",
  "steps": [
    { "label": "Aug 2022", "text": "Joined CSVTU CSE AI/ML" },
    { "label": "2023",     "text": "Built TokenAdapt on free TPU v2-8" },
    { "label": "May 2025", "text": "Published arXiv:2505.09738" },
    { "label": "May 2026", "text": "Graduating" }
  ]
}
```

---

### Cards layout

```json
{
  "type": "content",
  "title": "Contributions",
  "layout": "cards",
  "cards": [
    { "title": "Tokenization", "body": "QTK-81K — 4x Hindi efficiency" },
    { "title": "Training",     "body": "7B-14B on free TPU v2-8" },
    { "title": "Datasets",     "body": "54 datasets, 140GB, 25M rows" },
    { "title": "RLHF",         "body": "Qwen2.5-GRPO, 3.5M math rows" }
  ]
}
```

---

### `section` — Divider between sections

```json
{
  "type": "section",
  "title": "Part 2: Results",
  "subtitle": "Empirical evaluation across 5 benchmarks"
}
```

Renders as a dark full-bleed slide (template accent color background).

---

### `image-full` — Full-bleed image slide

```json
{
  "type": "image-full",
  "title": "System Architecture",
  "path": "assets/arch.png",
  "caption": "TPU SPMD sharding with GSPMD + Pallas kernels"
}
```

---

### `closing` — Last slide

```json
{
  "type": "closing",
  "title": "Thank You",
  "contact": "email@example.com",
  "links": [
    { "label": "arXiv",      "url": "https://arxiv.org/abs/2505.09738" },
    { "label": "GitHub",     "url": "https://github.com/example" }
  ]
}
```

---

## Spec Editing Rules

1. **Edit `slides.json` only** — never touch generated `.js`
2. **Reorder slides** by moving objects in the array
3. **Duplicate a slide** by copying the JSON object
4. **Change template** in `meta.template` — all slides update
5. **Add speaker notes** via `"notes": "..."` on any slide — **MANDATORY on every slide**
6. **Image paths** — relative to the working directory, or absolute
7. **Consistency** — all slides with same `type` auto-inherit template styles

### Speaker Notes

Every slide object **must** include a `"notes"` field. The notes appear in the PPTX notes panel and serve as the presenter's speaking script.

```json
{
  "type": "content",
  "title": "Key Results",
  "layout": "stats",
  "stats": [
    { "value": "4x", "label": "Token efficiency" }
  ],
  "notes": "OPEN: Here are the headline numbers.\n- 4x token efficiency vs Phi-4 on Hindi.\nEMPHASIS: Pause on this — it's the core contribution.\nTRANSITION: Now let me explain how we achieved this..."
}
```

Notes should include: opening line, talking points for each visual/bullet, emphasis cues, transitions, and Q&A prep hints.

---

## Full Example: Research Paper Presentation

```json
{
  "meta": {
    "title": "Efficient Hindi Tokenization",
    "author": "Shaurya Sharthak",
    "template": "csvtu-research",
    "output": "tokenadapt-slides.pptx"
  },
  "slides": [
    {
      "type": "title",
      "title": "Efficient Hindi Tokenization\nwith TokenAdapt",
      "subtitle": "arXiv:2505.09738",
      "presenter": "Shaurya Sharthak",
      "affiliation": "CSVTU Bhilai",
      "date": "May 2026",
      "notes": "Welcome everyone. Today I'll present our work on TokenAdapt — a new approach to Hindi tokenization that achieves 4x better efficiency than existing models. This is joint work from CSVTU Bhilai."
    },
    {
      "type": "content",
      "title": "Problem",
      "layout": "bullets",
      "items": [
        "Existing LLM tokenizers are 4x less efficient on Hindi than English",
        "Byte-fallback causes perplexity spikes in Indic scripts",
        "No open tokenizer trained specifically for Hindi at 7B+ scale"
      ],
      "notes": "OPEN: Let's start with the core problem.\n- First: Hindi gets 4x fewer tokens per word than English — that's a massive gap in representation quality.\n- Second: byte-fallback, the standard workaround, actually HURTS perplexity in Indic scripts because it loses morphological information.\n- Third: nobody has released an open tokenizer specifically for Hindi at 7B+ scale.\nTRANSITION: So what did we do about it?"
    },
    {
      "type": "content",
      "title": "Our Approach",
      "layout": "two-column",
      "left": {
        "type": "bullets",
        "items": ["SuperToken architecture", "QTK-81K vocab", "TPU v2-8 training"]
      },
      "right": {
        "type": "image",
        "path": "assets/arch.png"
      },
      "notes": "OPEN: Here's our approach in a nutshell.\n- SuperToken architecture: we group subword tokens into semantic super-tokens for Hindi.\n- QTK-81K: our vocabulary of 81K tokens, hand-curated for Hindi morphology.\n- We trained on a free TPU v2-8 — yes, you can do 7B-scale work on free hardware.\n- On the right, the architecture diagram shows how the tokenizer plugs into the LLM pipeline.\nTRANSITION: Let's see if it actually works..."
    },
    {
      "type": "content",
      "title": "Results",
      "layout": "stats",
      "stats": [
        { "value": "4x",   "label": "Token efficiency vs Phi-4" },
        { "value": "~2x",  "label": "Perplexity improvement" },
        { "value": "81K",  "label": "Vocabulary size" },
        { "value": "4",    "label": "Citations (May 2025)" }
      ],
      "notes": "OPEN: Here are the headline numbers.\n- 4x token efficiency compared to Phi-4's tokenizer on Hindi — this is our core contribution.\n- ~2x perplexity improvement — TokenAdapt halves the gap to English-quality models.\n- 81K vocabulary — compact enough for efficient inference.\n- 4 citations within the first month — the community is paying attention.\nEMPHASIS: Pause on the 4x stat — it's the number to remember.\nTRANSITION: Let me wrap up..."
    },
    {
      "type": "closing",
      "title": "Thank You",
      "contact": "shauryajnvkkr@gmail.com",
      "notes": "Thank you for your attention. I'm happy to take questions. You can reach me at the email shown. The paper is on arXiv and the code is on GitHub — links are on this slide."
    }
  ]
}
```
