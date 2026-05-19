# Template System

Templates define the visual identity applied to **every slide** automatically:
logos, watermarks, color palette, fonts, headers, footers, and slide numbering.

The generator reads the template JSON before rendering any slide, then injects
template elements into each slide. Editing visual identity = edit template JSON.

---

## Template JSON Schema

```json
{
  "name": "template-id",
  "extends": "default",

  "palette": {
    "primary":    "1E3A5F",
    "secondary":  "FFFFFF",
    "accent":     "C8A951",
    "text":       "1A1A1A",
    "muted":      "6B7280",
    "bg":         "FFFFFF",
    "dark_bg":    "1E3A5F"
  },

  "fonts": {
    "title":  "Calibri",
    "body":   "Calibri",
    "mono":   "Consolas"
  },

  "watermark": {
    "enabled":   true,
    "type":      "image",
    "path":      "assets/logo.png",
    "position":  "bottom-right",
    "opacity":   15,
    "w":         1.0,
    "h":         1.0,
    "margin":    0.2
  },

  "header": {
    "enabled":   false,
    "text":      "{title}",
    "fontSize":  9,
    "color":     "999999",
    "bold":      false
  },

  "footer": {
    "enabled":   true,
    "left":      "CSVTU Bhilai — B.Tech CSE (AI/ML)",
    "center":    "{title}",
    "right":     "{n} / {total}",
    "fontSize":  9,
    "color":     "9CA3AF",
    "y":         5.3
  },

  "title_slide": {
    "bg":          "dark_bg",
    "show_header": false,
    "show_footer": false,
    "watermark_opacity_override": 20
  },

  "section_slide": {
    "bg": "dark_bg"
  },

  "closing_slide": {
    "bg": "dark_bg",
    "show_footer": false
  }
}
```

`extends` — inherit all fields from another template, override only what differs.
Use `"extends": "default"` for custom templates to avoid repeating defaults.

---

## Watermark Modes

### Image Watermark (logo in corner)

```json
"watermark": {
  "enabled":  true,
  "type":     "image",
  "path":     "assets/csvtu-logo.png",
  "position": "bottom-right",
  "opacity":  15,
  "w":        0.9,
  "h":        0.9,
  "margin":   0.15
}
```

`position` options: `"bottom-right"`, `"bottom-left"`, `"top-right"`, `"top-left"`,
`"bottom-center"`, `"center"` (full background ghost watermark)

`opacity`: 0-100. Recommended:
- Corner logo: 15-25 (subtle but visible)
- Background ghost: 5-10 (barely visible, professional)
- Confidential stamp: 12-18

`path` — relative to skill root OR absolute. PNG with transparency preferred.

---

### Text Watermark

```json
"watermark": {
  "enabled":   true,
  "type":      "text",
  "text":      "CONFIDENTIAL",
  "position":  "center",
  "rotate":    315,
  "opacity":   8,
  "fontSize":  48,
  "color":     "FF0000",
  "bold":      true
}
```

---

### Dual Watermark (logo + text)

```json
"watermarks": [
  {
    "type": "image", "path": "assets/logo.png",
    "position": "bottom-right", "opacity": 20, "w": 0.9, "h": 0.9
  },
  {
    "type": "text", "text": "DRAFT",
    "position": "center", "rotate": 315, "opacity": 6, "fontSize": 60
  }
]
```

Use `"watermarks"` (plural array) instead of `"watermark"` for multiple.

---

## Footer Variables

| Variable | Expands to |
|----------|-----------|
| `{title}` | Presentation title from `meta.title` |
| `{author}` | `meta.author` |
| `{date}` | `meta.date` or today's date |
| `{n}` | Current slide number |
| `{total}` | Total slide count |
| `{template}` | Template name |

Title slide and closing slide suppress the footer by default (override in template).

---

## Built-in Templates

Templates in `assets/templates/`:

| ID | Use case |
|----|----------|
| `default` | Clean white, no watermark, no footer |
| `csvtu-research` | CSVTU logo watermark, navy palette, slide numbers |
| `research-dark` | Dark navy throughout, white text, accent gold |
| `minimal` | Off-white bg, charcoal text, no logo |
| `corporate` | Teal/navy, header bar, logo top-left |
| `conference` | Two-tone sidebar, slide numbers, date footer |

---

## Creating a Custom Template

### Quickest path — copy + modify

```bash
cp assets/templates/csvtu-research.json assets/templates/my-college.json
# Edit: palette, watermark.path, footer.left
```

### Full college/university template checklist

```json
{
  "name": "my-college",
  "extends": "default",

  "palette": {
    "primary":  "003087",
    "accent":   "FFB81C",
    "bg":       "FFFFFF",
    "dark_bg":  "003087"
  },

  "watermark": {
    "enabled":  true,
    "type":     "image",
    "path":     "assets/my-college-logo.png",
    "position": "bottom-right",
    "opacity":  18,
    "w":        0.85,
    "h":        0.85,
    "margin":   0.2
  },

  "footer": {
    "enabled": true,
    "left":    "My College Name",
    "center":  "{title}",
    "right":   "Slide {n} of {total}",
    "fontSize": 8,
    "color":   "9CA3AF"
  }
}
```

**Logo prep tips:**
- PNG with transparent background preferred
- Minimum 300px width for crisp rendering at 0.9" on slide
- If only JPG available, add `"bg_fill": "FFFFFF"` in watermark config
- Position: `"bottom-right"` is standard for academic slides

---

## Template Inheritance

```json
{ "name": "my-dark-variant", "extends": "csvtu-research",
  "palette": { "bg": "1A1A2E", "dark_bg": "0F0F23", "text": "E2E8F0" },
  "title_slide": { "bg": "dark_bg" }
}
```

Only override what changes. Inheritance is shallow-merged per section.

---

## Per-Slide Template Overrides

Any slide can override template values:

```json
{
  "type": "content",
  "title": "Acknowledgements",
  "layout": "bullets",
  "items": ["..."],
  "_template_override": {
    "watermark": { "opacity": 30 },
    "footer": { "enabled": false }
  }
}
```

Use `_template_override` sparingly — for exceptions, not the rule.
