# Images Reference

**1 image > 2 slides of text.** Visuals are processed 60,000x faster than text.
Every slide with more than 4 bullets is a candidate for an image replacement.

---

## The Image-First Philosophy

When building a slide deck, ask: **"Can this be a chart/diagram/image instead of text?"**

| If the content is... | Replace with... |
|---------------------|----------------|
| 5+ bullet points with data | Bar chart or comparison visual |
| A process with 3+ steps | Flowchart diagram |
| A timeline of events | Timeline visual |
| Statistics/numbers | Stat callout cards with big numbers |
| Before/after comparison | Side-by-side visual |
| Overlapping concepts | Venn diagram |
| Feature list | Icon grid |
| Correlation data | Heatmap |
| Trend over time | Line chart |
| Part-of-whole data | Pie/donut chart |
| Hero/intro slide | Searched stock image |
| Architecture/system | Generated diagram |

---

## Image Pipeline

```
slides.json (with image specs)
    ├── gen_images.py  →  charts, diagrams, infographics  →  assets/generated/
    ├── fetch_images.py  →  stock photos from web  →  assets/fetched/
    └── gen_pptx.js  →  embeds all images into PPTX
```

### Step 1: Generate Data Visualizations

Use `scripts/gen_images.py` with a config JSON:

```bash
python scripts/gen_images.py images-config.json assets/generated/
```

### Step 2: Fetch Stock Images (if needed)

Use `scripts/fetch_images.py` to find and download images from the web:

```bash
python scripts/fetch_images.py fetch-config.json assets/fetched/
```

### Step 3: Reference in Slide Spec

Point the slide spec to the generated/fetched images:

```json
{
  "type": "content",
  "title": "Performance",
  "layout": "image-right",
  "image": { "path": "assets/generated/perf_chart.png" },
  "notes": "The chart shows a 4x improvement..."
}
```

---

## Available Chart Types (gen_images.py)

| Type | ID | Best For | Key Data Fields |
|------|----|----------|-----------------|
| **Bar chart** | `bar` | Comparing values | `labels`, `values`, `colors` |
| **Grouped bar** | `grouped_bar` | Multi-series comparison | `labels`, `series[].name`, `series[].values` |
| **Line chart** | `line` | Trends over time | `labels`, `series[].values` |
| **Pie chart** | `pie` | Part-of-whole | `labels`, `values` |
| **Donut chart** | `pie` (donut: true) | Part-of-whole with center label | Same as pie |
| **Scatter plot** | `scatter` | Correlations | `series[].x`, `series[].y` |
| **Heatmap** | `heatmap` | Correlation matrices | `matrix`, `row_labels`, `col_labels` |
| **Comparison** | `comparison` | Side-by-side stats | `items[].label`, `items[].value` |
| **Flowchart** | `flowchart` | Process flow | `steps[].id`, `steps[].label` |
| **Timeline** | `timeline` | Chronological events | `events[].date`, `events[].label` |
| **Stat callout** | `stat_callout` | Big number highlights | `stats[].value`, `stats[].label` |
| **Venn diagram** | `venn` | Overlapping concepts | `sets[].label`, `sets[].size` |
| **Icon grid** | `icon_grid` | Feature lists | `items[].icon`, `items[].title` |

---

## Style Presets

| Preset | Best For | Colors |
|--------|----------|--------|
| `minimal` | Clean, professional | White bg, blue accent |
| `dark` | Tech, modern | Dark slate bg, blue accent |
| `research` | Academic papers | White bg, gold accent |
| `corporate` | Business decks | White bg, navy accent |
| `vibrant` | Creative, startup | White bg, pink accent |

Override any color in the `options` object:

```json
{
  "type": "bar",
  "options": {
    "style": "dark",
    "accent": "#10B981"
  }
}
```

---

## gen_images.py Config Format

```json
{
  "output_dir": "assets/generated",
  "images": [
    {
      "id": "perf_chart",
      "type": "bar",
      "title": "Token Efficiency Comparison",
      "data": {
        "labels": ["Phi-4", "LLaMA", "TokenAdapt"],
        "values": [48.2, 52.1, 24.6],
        "colors": ["#CADCFC", "#CADCFC", "#2563EB"]
      },
      "options": {
        "ylabel": "Perplexity (lower = better)",
        "highlight_best": true,
        "lower_is_better": true,
        "style": "minimal"
      }
    },
    {
      "id": "timeline",
      "type": "timeline",
      "title": "Research Journey",
      "data": {
        "events": [
          { "date": "Aug 2022", "label": "Joined CSVTU" },
          { "date": "2023", "label": "Built TokenAdapt" },
          { "date": "May 2025", "label": "arXiv publication" }
        ]
      },
      "options": { "style": "research" }
    }
  ]
}
```

---

## fetch_images.py Config Format

```json
{
  "output_dir": "assets/fetched",
  "images": [
    {
      "id": "hero_ai",
      "query": "artificial intelligence neural network abstract",
      "count": 3,
      "orientation": "landscape",
      "min_width": 800
    },
    {
      "id": "tpu_hardware",
      "query": "google TPU chip server rack",
      "count": 2,
      "orientation": "landscape"
    }
  ]
}
```

### Image Sources (in order of preference)

1. **Unsplash** — Free, high-quality, no API key needed for basic use
2. **Pixabay** — Free, API available with demo key
3. **Pexels** — Free, web scraping fallback
4. **Lorem Picsum** — Ultimate fallback, random high-quality photos

The script tries multiple sources and downloads up to `count` images per query.
If no images are found, it creates a placeholder.

---

## When to Use Each Image Type

### Data → Chart

| Data Pattern | Chart Type | Example |
|-------------|------------|---------|
| Compare 2-5 items | `bar` | Model accuracy comparison |
| Track metric over time | `line` | Training loss curve |
| Show proportions | `pie` / `donut` | Dataset composition |
| Correlation between vars | `scatter` | Parameters vs performance |
| Matrix of relationships | `heatmap` | Feature correlation |
| Before vs after | `comparison` | Old vs new approach |
| Multiple series comparison | `grouped_bar` | Accuracy across models and tasks |

### Process → Diagram

| Content | Visual Type | Example |
|---------|-------------|---------|
| 3-7 step workflow | `flowchart` | Data → Train → Evaluate → Deploy |
| Chronological events | `timeline` | Research milestones |
| Overlapping categories | `venn` | Skills intersection |
| Feature highlights | `icon_grid` | Product features |

### Context → Image

| Situation | Source | Example |
|-----------|--------|---------|
| Hero/intro slide | `fetch_images.py` | Abstract AI background |
| Architecture diagram | Generate or draw | System architecture |
| Concept illustration | `fetch_images.py` | Neural network visual |
| Team/organization | User provides | Team photo |

---

## Slide Layouts That Use Images

| Layout | Image Placement | Best For |
|--------|----------------|----------|
| `image-right` | 40% width, right side | Text + supporting chart |
| `image-left` | 40% width, left side | Chart + explanation |
| `two-column` | One column is image | Side-by-side comparison |
| `image-full` | Full bleed | Hero images, architecture diagrams |
| `chart` | Auto-sized in center | Data visualizations |

---

## Image Quality Rules

1. **Minimum width: 800px** — anything less looks blurry on projectors
2. **Use JPG for photos, PNG for charts** — JPG is smaller for photographs, PNG preserves chart crispness
3. **16:9 aspect ratio preferred** — matches slide dimensions
4. **No watermarks** — use fetch_images.py to find clean images
5. **Consistent style** — all charts in a deck should use the same style preset
6. **Label everything** — axes, legends, titles. If the audience has to guess, the chart failed
7. **Highlight the insight** — use `highlight_best`, accent colors, or annotations to draw attention to what matters
