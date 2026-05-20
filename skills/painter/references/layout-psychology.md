# Layout Psychology, Visual Hierarchy & Placement Principles in Web/UI Design

> Deep research report — Bauna Intern | 2026-05-20

---

## Table of Contents

1. [Visual Hierarchy Principles](#1-visual-hierarchy-principles)
2. [Reading Patterns](#2-reading-patterns)
3. [Fitts' Law](#3-fitts-law)
4. [Hick's Law](#4-hicks-law)
5. [Miller's Law](#5-millers-law)
6. [Gestalt Principles](#6-gestalt-principles)
7. [Whitespace (Negative Space)](#7-whitespace-negative-space)
8. [Above the Fold](#8-above-the-fold)
9. [CTA Placement](#9-cta-placement)
10. [Content Grouping](#10-content-grouping)
11. [Responsive Placement](#11-responsive-placement)
12. [Attention Direction](#12-attention-direction)
13. [Combined Reference Patterns](#13-combined-reference-patterns)

---

## 1. Visual Hierarchy Principles

Visual hierarchy is the arrangement of elements to show their order of importance. Users don't read -- they scan. Hierarchy guides their eyes to what matters.

### The Six Levers of Hierarchy

| Lever | Mechanism | Psychological Basis |
|-------|-----------|-------------------|
| **Size** | Larger elements = more important | Pre-attentive processing; eyes go to biggest thing first |
| **Color/Contrast** | High contrast = focal point | Pop-out effect in visual cortex |
| **Position** | Top-left (LTR) = first attention | Gutenberg Diagram; reading gravity |
| **Whitespace** | More space around = elevated importance | Isolation effect (Von Restorff) |
| **Typography** | Weight, size, style create tiers | Pattern recognition; readers scan headings first |
| **Repetition** | Consistent patterns = predictability | Schema formation reduces cognitive load |

### Concrete CSS Patterns for Visual Hierarchy

#### Size-Based Hierarchy (Type Scale)

```css
/* Modular type scale (1.25 ratio — "major third") */
:root {
  --text-xs:    0.64rem;   /* 10.24px — captions, legal */
  --text-sm:    0.8rem;    /* 12.8px  — secondary text */
  --text-base:  1rem;      /* 16px    — body copy */
  --text-lg:    1.25rem;   /* 20px    — lead paragraphs */
  --text-xl:    1.563rem;  /* 25px    — section headings */
  --text-2xl:   1.953rem;  /* 31.25px — page headings */
  --text-3xl:   2.441rem;  /* 39px    — hero headings */
  --text-4xl:   3.052rem;  /* 48.8px  — display text */
}

/* Each level has a clear visual purpose */
h1 { font-size: var(--text-3xl); font-weight: 800; line-height: 1.1; }
h2 { font-size: var(--text-2xl); font-weight: 700; line-height: 1.2; }
h3 { font-size: var(--text-xl);  font-weight: 600; line-height: 1.3; }
h4 { font-size: var(--text-lg);  font-weight: 600; line-height: 1.4; }
p  { font-size: var(--text-base); font-weight: 400; line-height: 1.6; }
```

**Why this works:** The eye jumps to the largest, boldest text first. A 2.4:1 size ratio between heading and body creates a clear "this is more important" signal without conscious effort.

#### Color/Contrast Hierarchy

```css
/* Contrast creates instant focal points */
:root {
  --color-primary:    #2563EB;  /* Blue — action, trust */
  --color-primary-fg: #FFFFFF;  /* White text on primary */
  --color-text:       #1F2937;  /* Near-black — body */
  --color-muted:      #6B7280;  /* Gray — secondary info */
  --color-surface:    #F9FAFB;  /* Light gray — backgrounds */
}

/* High contrast = "look here first" */
.btn-primary {
  background: var(--color-primary);
  color: var(--color-primary-fg);
  /* Contrast ratio: 8.6:1 — exceeds AAA */
}

/* Low contrast = "look here last" */
.caption {
  color: var(--color-muted);
  font-size: var(--text-sm);
  /* Contrast ratio: 4.6:1 — passes AA only */
}
```

**Research note:** The pre-attentive processing system in the visual cortex detects contrast differences in under 200ms (before conscious awareness). High-contrast elements are literally seen first.

#### Position-Based Hierarchy (Gutenberg Diagram)

```css
/*
  Gutenberg Diagram for LTR layouts:

  ┌─────────────────────┬──────────────┐
  │  PRIMARY OPTICAL     │  STRONG      │
  │  AREA (top-left)     │  FALL        │
  │  ← User starts here  │              │
  ├──────────────────────┤              │
  │  WEAK                │  TERMINAL    │
  │  FALL                │  AREA        │
  │                      │  (CTA here)  │
  └──────────────────────┴──────────────┘

  Place: Logo top-left, primary CTA bottom-right
*/

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 2rem;
  padding: 4rem 6rem;
}

/* Top-left: Primary optical area — logo, headline */
.hero-headline {
  grid-column: 1;
  grid-row: 1;
  align-self: start;
}

/* Top-right: Strong fall — supporting visual */
.hero-visual {
  grid-column: 2;
  grid-row: 1 / 3;
  align-self: center;
}

/* Bottom-left: Weak fall — secondary text */
.hero-description {
  grid-column: 1;
  grid-row: 2;
  color: var(--color-muted);
}

/* Bottom-right: Terminal area — primary CTA */
.hero-cta {
  grid-column: 2;
  grid-row: 2;
  align-self: end;
  justify-self: end;
}
```

---

## 2. Reading Patterns

### F-Pattern (Text-Heavy Pages)

Users scan in an F-shape: horizontal across top, horizontal across a secondary point, then vertically down the left side.

```
 ─────────────────────────────────  ← First horizontal scan
 ──────────────────────             ← Second horizontal scan (shorter)
 │
 │                                  ← Vertical scan down left
 │
 │
 │
```

**Design for F-pattern:**

```css
/* F-pattern: Put key info at start of lines, use bullet points */
.f-pattern-content {
  max-width: 72ch;          /* Optimal line length for reading */
  margin-left: 0;           /* Strong left edge for vertical scan */
}

/* Lead with the important word in each line/item */
.f-pattern-content li {
  padding-left: 0;
  margin-bottom: 0.75rem;
}

/* Break up long text with subheadings every 2-3 paragraphs */
.f-pattern-content h3 {
  margin-top: 2rem;
  font-size: var(--text-lg);
  font-weight: 600;
  border-left: 3px solid var(--color-primary); /* Draws vertical scan */
  padding-left: 0.75rem;
}
```

**HTML pattern for F-pattern compliance:**

```html
<article class="f-pattern-content">
  <h2>Page Title — Keywords Here</h2>          <!-- First horizontal -->
  <p><strong>Key finding</strong> explained in detail...</p>  <!-- Second horizontal -->
  <h3>Section with Keyword</h3>                 <!-- Vertical anchors -->
  <ul>
    <li><strong>Action verb</strong> — detail follows</li>
    <li><strong>Action verb</strong> — detail follows</li>
  </ul>
</article>
```

### Z-Pattern (Landing Pages, Minimal Content)

Users scan: top-left → top-right → bottom-left → bottom-right.

```
  START ──────────────────→  [Logo/Nav]
    ↘
      ╲
        ╲
  [CTA] ←─────────────────  [Hero Image]
```

**Design for Z-pattern:**

```css
.z-pattern-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

/* Position 1 (top-left): Logo */
.z-logo    { grid-area: 1 / 1; }

/* Position 2 (top-right): Navigation / secondary CTA */
.z-nav     { grid-area: 1 / 2; justify-self: end; }

/* Position 3 (bottom-left): Headline + description */
.z-content { grid-area: 2 / 1; align-self: center; }

/* Position 4 (bottom-right): Primary CTA or hero visual */
.z-cta     { grid-area: 2 / 2; align-self: center; justify-self: end; }
```

### Gutenberg Diagram

Already covered in Section 1. Key principle: the eye travels from Primary Optical Area (top-left) to Terminal Area (bottom-right) in LTR layouts. Place your "payoff" (CTA, conclusion) in the terminal area.

### Layer-Cake Pattern (Scanning Behavior)

Users read headings, skip body, read next heading, skip body. This is how most people consume long-form content.

```css
/* Design headings to be scannable "layer separators" */
.layer-heading {
  font-size: var(--text-xl);
  font-weight: 700;
  margin-top: 3rem;          /* Clear separation from previous section */
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--color-surface); /* Visual anchor */
  color: var(--color-text);
}

/* Make headings self-contained — meaningful without body text */
/* Bad:  "Introduction" */
/* Good: "Why F-Pattern Layouts Increase Conversion by 47%" */

/* Add a subtle visual cue that there's content below */
.layer-heading::after {
  content: '';
  display: block;
  width: 3rem;
  height: 2px;
  background: var(--color-primary);
  margin-top: 0.5rem;
}
```

---

## 3. Fitts' Law

**Formula:** `T = a + b * log2(1 + D/W)`

Where:
- `T` = time to reach target
- `a`, `b` = empirically determined constants
- `D` = distance from starting point to target center
- `W` = width of target (in direction of movement)

### Practical Implications

| Principle | Rule | CSS Implementation |
|-----------|------|-------------------|
| Larger targets are faster | Min touch target: 44x44px (Apple), 48x48dp (Google) | `min-width: 44px; min-height: 44px` |
| Closer targets are faster | Related actions within 200px of each other | `gap: 0.5rem` in flex/grid |
| Edge targets have infinite effective size | Place frequent actions at screen edges | `position: fixed; bottom: 0; left: 0; right: 0` |
| Corners are fastest | OS-level actions at corners (Start menu, hot corners) | `position: fixed; bottom: 0; right: 0` |

### Concrete Patterns

```css
/* Fitts' Law-compliant button sizing */
.btn {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 24px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  /* Larger hit area than visual boundary */
  position: relative;
}

/* Extend hit area beyond visual boundary (common in mobile) */
.btn::before {
  content: '';
  position: absolute;
  top: -8px;
  right: -8px;
  bottom: -8px;
  left: -8px;
}

/* Edge targeting: sticky CTA at screen bottom */
.sticky-cta-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: white;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  z-index: 100;
  /* Effective width = screen width (infinite in horizontal axis) */
}

/* Proximity: related actions grouped close together */
.action-group {
  display: flex;
  gap: 8px;        /* 8px gap = actions are clearly related */
  align-items: center;
}

/* vs. unrelated actions with more space */
.action-group + .action-group {
  margin-top: 24px;  /* 24px = clearly separate group */
}
```

### Edge Targeting on Mobile

```css
/* Mobile bottom navigation — exploits edge targeting */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  padding-bottom: env(safe-area-inset-bottom); /* iPhone notch */
  background: white;
  border-top: 1px solid #e5e7eb;
}

.bottom-nav a {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 16px;
  min-width: 48px;
  min-height: 48px;
  text-decoration: none;
  color: var(--color-muted);
}

/* The bottom edge gives infinite effective height */
/* The left/right edges give infinite effective width to first/last items */
```

---

## 4. Hick's Law

**Formula:** `RT = a + b * log2(n + 1)`

Where:
- `RT` = reaction time
- `n` = number of choices
- `a`, `b` = constants

### Key Implications

- **Every additional option adds decision time** (logarithmically, not linearly)
- **5 choices** = ~2.58 bits of information
- **10 choices** = ~3.46 bits (only 34% more time for 2x the options)
- But **perceived complexity** scales linearly — 10 options *feels* twice as complex as 5

### Reducing Decision Burden

```css
/* Strategy 1: Progressive Disclosure — show 3-5 options, "More" for rest */
.option-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.option-group .option:nth-child(n+6) {
  display: none;  /* Hide options 6+ initially */
}

.option-group .show-more {
  display: block;
  color: var(--color-primary);
  cursor: pointer;
  font-size: var(--text-sm);
  margin-top: 4px;
}

/* Strategy 2: Default Selection — reduce decision to "accept or change" */
.radio-group input[type="radio"]:checked + label {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

/* Visually emphasize the recommended/default option */
.option-recommended {
  border: 2px solid var(--color-primary);
  position: relative;
}

.option-recommended::before {
  content: 'Recommended';
  position: absolute;
  top: -10px;
  left: 12px;
  background: var(--color-primary);
  color: white;
  font-size: var(--text-xs);
  padding: 2px 8px;
  border-radius: 4px;
}

/* Strategy 3: Grouping — chunk 10 items into 2 groups of 5 */
.option-groups {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.option-groups h3 {
  font-size: var(--text-lg);
  margin-bottom: 0.75rem;
  color: var(--color-text);
}
```

**HTML for progressive disclosure:**

```html
<div class="option-group" id="colorOptions">
  <button class="option">Red</button>
  <button class="option">Blue</button>
  <button class="option">Green</button>
  <button class="option">Black</button>
  <button class="option">White</button>
  <!-- These are hidden by CSS, shown on "More" click -->
  <button class="option hidden">Navy</button>
  <button class="option hidden">Burgundy</button>
  <button class="option hidden">Forest</button>
  <button class="show-more" onclick="toggleMore(this)">+ 3 more colors</button>
</div>
```

### Hick's Law Applied to Navigation

```css
/* Limit primary nav to 5-7 items max */
.main-nav {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.main-nav > a {
  /* Each item = 1 decision point. 7 items ≈ 3 bits = fast scanning */
  padding: 8px 0;
  font-weight: 500;
  color: var(--color-text);
}

/* Use mega-menus for secondary options (progressive disclosure) */
.main-nav .has-dropdown:hover .mega-menu {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 2rem;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
```

---

## 5. Miller's Law

**Original finding (George Miller, 1956):** Working memory holds 7 +/- 2 items.

**Modern refinement (Cowan, 2001):** The actual limit is closer to 4 +/- 1 chunks for most people under cognitive load.

### Practical Application

| Context | Recommended Limit | Rationale |
|---------|-------------------|-----------|
| Primary navigation | 5-7 items | Miller's upper bound |
| Dashboard KPI cards | 4-5 | Cowan's refined limit |
| Form fields per step | 4-6 | Beyond 6, completion drops |
| Bullet points per list | 5-7 | Chunking sweet spot |
| Choices per decision | 5 | Hick's Law + Miller overlap |
| Steps in a process | 3-5 | Working memory for sequences |

### Chunking in CSS

```css
/* Phone number: 5558675309 → 555-867-5309 (3 chunks of 3-4) */
.phone-display {
  font-family: 'SF Mono', 'Fira Code', monospace;
  letter-spacing: 0.05em;
}
.phone-display::before { content: '('; }
.phone-display::after  { content: ')'; }

/* Credit card: 4111111111111111 → 4111 1111 1111 1111 (4 chunks of 4) */
.cc-input {
  font-family: monospace;
  letter-spacing: 0.1em;
  max-width: 20ch;
}

/* Dashboard: max 5 KPI cards in a row */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

/* Beyond 5, use scrolling or pagination */
.kpi-grid > .kpi-card:nth-child(n+6) {
  display: none; /* Or move to a "more metrics" section */
}

/* Form fields: chunk related fields with visual grouping */
.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--color-surface);
}

.form-section legend,
.form-section h3 {
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: 1rem;
}
```

### Navigation Chunking Example

```html
<nav class="main-nav">
  <!-- Primary chunk: 5 items -->
  <a href="/products">Products</a>
  <a href="/solutions">Solutions</a>
  <a href="/pricing">Pricing</a>
  <a href="/docs">Docs</a>
  <a href="/company">Company</a>
  <!-- Overflow goes into dropdown or footer -->
</nav>
```

---

## 6. Gestalt Principles

### 6.1 Proximity

**Principle:** Items close together are perceived as a group.

```css
/* WRONG: Equal spacing between all items — no grouping */
.list-bad li { margin-bottom: 8px; }

/* RIGHT: Tight spacing within groups, wide spacing between groups */
.list-good li { margin-bottom: 4px; }
.list-good li.group-break { margin-top: 16px; }

/* Card groups: cards close together, groups separated */
.card-group {
  display: flex;
  gap: 12px;           /* Within group: tight */
  margin-bottom: 2rem; /* Between groups: wide */
}

/* Form field proximity: label near its input, far from next label */
.form-field {
  margin-bottom: 1.5rem;
}

.form-field label {
  display: block;
  margin-bottom: 0.25rem;  /* Label close to input */
  font-weight: 500;
}

.form-field input {
  width: 100%;
  padding: 0.5rem;
}

/* Related controls: close together */
.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-row .form-field {
  flex: 1;
  margin-bottom: 0; /* Don't double the spacing */
}
```

### 6.2 Similarity

**Principle:** Items that look alike are perceived as related.

```css
/* Similar styling = perceived as same category */
.product-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  /* All product cards look the same → perceived as same type */
}

/* Different styling = perceived as different category */
.product-card.featured {
  border: 2px solid var(--color-primary);
  background: linear-gradient(135deg, #eff6ff, #ffffff);
  /* Featured card stands out as "different from the rest" */
}

/* Consistent icon treatment = perceived as related features */
.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  margin-bottom: 1rem;
}

/* Button hierarchy through similarity + difference */
.btn-primary   { background: #2563EB; color: white; }
.btn-secondary { background: white; color: #2563EB; border: 1px solid #2563EB; }
.btn-tertiary  { background: transparent; color: #2563EB; text-decoration: underline; }
/* All three are "buttons" (similarity) but different emphasis (difference) */
```

### 6.3 Continuity

**Principle:** The eye follows smooth lines and curves; elements on a line are perceived as related.

```css
/* Timeline: continuity through vertical line */
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e5e7eb;
  /* This continuous line connects all timeline items */
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -2rem;
  top: 4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 2px solid white;
  box-shadow: 0 0 0 2px #e5e7eb;
}

/* Horizontal continuity: breadcrumb trail */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: var(--text-sm);
}

.breadcrumb li:not(:last-child)::after {
  content: '/';
  margin-left: 0.5rem;
  color: var(--color-muted);
  /* The slash creates continuity — eye flows left to right */
}

/* Stepper: continuity through horizontal line */
.stepper {
  display: flex;
  align-items: center;
}

.stepper-step {
  display: flex;
  align-items: center;
}

.stepper-step:not(:last-child)::after {
  content: '';
  flex: 1;
  height: 2px;
  background: #e5e7eb;
  min-width: 40px;
}

.stepper-step.completed:not(:last-child)::after {
  background: var(--color-primary);
}
```

### 6.4 Closure

**Principle:** The brain fills in missing parts of a pattern.

```css
/* Incomplete borders — brain completes the rectangle */
.card-closure {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  /* Full border works, but partial borders feel lighter */
}

/* Even lighter: only top border + shadow = brain "closes" the card */
.card-closure-light {
  border-top: 3px solid var(--color-primary);
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border-radius: 8px;
  padding: 1.5rem;
  /* Brain sees a complete card despite missing 3 sides */
}

/* Logo with closure: partial letter forms */
/* The brain recognizes letters even when parts are missing */
/* Used in: IBM (horizontal stripes), NBC (peacock), FedEx (arrow) */

/* Loading skeleton: closure makes incomplete content feel "coming" */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 4px;
}

@keyframes skeleton-loading {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### 6.5 Figure/Ground

**Principle:** The brain separates foreground from background.

```css
/* Modal overlay: ground (dark bg) recedes, figure (modal) pops */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  box-shadow: 0 25px 50px rgba(0,0,0,0.25);
  /* Figure: elevated, bright, sharp edges */
}

/* Card elevation: more shadow = more "figure" */
.card-level-0 { box-shadow: none; }
.card-level-1 { box-shadow: 0 1px 3px rgba(0,0,0,0.12); }
.card-level-2 { box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.card-level-3 { box-shadow: 0 12px 40px rgba(0,0,0,0.2); }

/* Frosted glass: ground bleeds through, figure is semi-transparent */
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  /* Ground (background) visible through figure = depth illusion */
}
```

### 6.6 Common Region

**Principle:** Items within a border or shared background are perceived as grouped.

```css
/* Border-based grouping */
.card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  /* Everything inside this border = one group */
}

/* Background-based grouping */
.section-alt {
  background: #f9fafb;
  padding: 4rem 2rem;
  /* Alternating sections = different groups */
}

/* Fieldset grouping */
fieldset {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
}

fieldset legend {
  font-weight: 600;
  padding: 0 0.5rem;
}

/* Toolbar grouping */
.toolbar {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: #f3f4f6;
  border-radius: 8px;
}

.toolbar button {
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  background: transparent;
}
```

### 6.7 Parallelism

**Principle:** Parallel elements are perceived as related.

```css
/* Consistent card layout = parallelism */
.feature-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.feature-card .icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem; /* Same position on every card */
}

.feature-card h3 {
  margin-bottom: 0.5rem; /* Same position */
}

.feature-card p {
  color: var(--color-muted);
  flex: 1; /* Push CTA to bottom — consistent across cards */
}

.feature-card .cta {
  margin-top: 1rem; /* Same position */
}

/* All cards have the same structure = parallelism = "these are peers" */
```

---

## 7. Whitespace (Negative Space)

### Types of Whitespace

| Type | Definition | Example | Impact |
|------|-----------|---------|--------|
| **Macro** | Between major sections | Hero → Features gap | Creates visual separation |
| **Micro** | Between lines, letters | `line-height`, `letter-spacing` | Affects readability |
| **Active** | Intentionally placed | Padding around CTA | Draws attention |
| **Passive** | Natural result of layout | Space between words | Enables reading |

### Research Backing

- **Wichita State University (2012):** Whitespace between paragraphs and in margins increases comprehension by ~20%.
- **Human Factors International:** Proper whitespace can increase user performance on tasks by up to 20%.
- **Google:** Increased whitespace in search results (2010 redesign) improved user satisfaction.
- **Luxury brands** use 50-70% whitespace; budget brands use 20-30%.

### CSS Whitespace Patterns

```css
/* Micro whitespace */
body {
  font-size: 16px;
  line-height: 1.6;        /* 25.6px — optimal for body text */
  letter-spacing: -0.01em;  /* Slight tightening for large blocks */
  word-spacing: 0;
}

h1, h2, h3 {
  line-height: 1.2;         /* Tighter for headings (less whitespace) */
  letter-spacing: -0.02em;  /* Headings can be tighter */
}

p {
  margin-bottom: 1.25rem;   /* Paragraph spacing = ~20px */
}

/* Macro whitespace — section rhythm */
section {
  padding: 6rem 2rem;       /* Generous vertical padding */
}

section + section {
  margin-top: 0;            /* Padding handles spacing */
}

/* Container max-width prevents overly long lines */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;          /* Side breathing room */
}

/* Content max-width for readability */
.prose {
  max-width: 72ch;          /* ~72 characters per line — optimal */
  margin: 0 auto;
}

/* Active whitespace: padding around important elements */
.cta-section {
  padding: 4rem;
  text-align: center;
  /* Generous space = "this matters" */
}

/* Don't fill every pixel — resist the urge */
.hero {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Empty space IS the design */
}
```

### Whitespace Anti-Patterns

```css
/* WRONG: Cramming everything "above the fold" */
.hero-bad {
  padding: 1rem;
  font-size: 12px;
  line-height: 1.3;
  /* Sacrificing whitespace for density = worse comprehension */
}

/* RIGHT: Let the hero breathe */
.hero-good {
  padding: 6rem 2rem;
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.hero-good h1 {
  font-size: clamp(2rem, 5vw, 4rem);
  margin-bottom: 1.5rem;
}

.hero-good p {
  font-size: 1.25rem;
  max-width: 60ch;
  margin-bottom: 2rem;
  color: var(--color-muted);
}
```

---

## 8. Above the Fold

### What Research Says

- **Nielsen Norman Group (2010, updated 2018):** Users spend 80% of their time above the fold. Content above the fold gets 84% more attention than content below.
- **However:** The "fold" varies by device, resolution, and browser chrome. On mobile, it's roughly 600-900px. On desktop, roughly 600-700px.
- **The fold is not a wall.** Users DO scroll — but only if what's above the fold gives them a reason to.

### What Belongs Above the Fold

| Element | Priority | Rationale |
|---------|----------|-----------|
| Value proposition | Critical | Users decide in 3 seconds whether to stay |
| Primary CTA | Critical | Capture intent immediately |
| Hero visual | High | Emotional engagement |
| Navigation | High | Orientation and control |
| Social proof snippet | Medium | Trust signal |
| Scroll cue | Medium | Indicate more below |

### CSS Patterns

```css
/* Hero section: everything needed for first impression */
.hero {
  min-height: 100vh;          /* Full viewport = everything above fold */
  min-height: 100svh;          /* Small viewport height (mobile) */
  display: grid;
  grid-template-rows: auto 1fr auto;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-nav    { grid-row: 1; }  /* Navigation: always visible */
.hero-main   { grid-row: 2; display: flex; flex-direction: column; justify-content: center; }
.hero-scroll { grid-row: 3; }  /* Scroll cue at bottom */

/* Scroll cue: animated arrow */
.scroll-cue {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-muted);
  font-size: var(--text-sm);
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-8px); }
  60% { transform: translateY(-4px); }
}

/* Partially visible content = scroll affordance */
.preview-content {
  margin-top: -4rem;           /* Overlap into hero = "there's more" */
  padding-top: 4rem;
  background: white;
  border-radius: 24px 24px 0 0;
  position: relative;
  z-index: 1;
}
```

### Scroll Progress Indicator

```css
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-primary);
  z-index: 1000;
  transition: width 0.1s;
  /* Width set via JS: (scrollTop / (scrollHeight - clientHeight)) * 100 + '%' */
}
```

---

## 9. CTA Placement

### CTA Hierarchy

```css
/* Primary CTA: high contrast, large, prominent */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  font-size: 1rem;
  font-weight: 600;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  min-height: 48px;
  min-width: 120px;
  transition: all 0.15s ease;
}

.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

/* Secondary CTA: outline, medium emphasis */
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 500;
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 8px;
  cursor: pointer;
  min-height: 48px;
}

/* Tertiary CTA: text link, low emphasis */
.btn-tertiary {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 8px 0;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-primary);
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}
```

### CTA Placement Patterns

```css
/* Pattern 1: CTA near relevant content (don't separate action from context) */
.feature {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  padding: 4rem 2rem;
}

.feature-text .btn-primary {
  margin-top: 1.5rem;  /* CTA immediately follows description */
}

/* Pattern 2: Sticky CTA on mobile */
@media (max-width: 768px) {
  .sticky-cta {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 12px 16px;
    padding-bottom: calc(12px + env(safe-area-inset-bottom));
    background: white;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    z-index: 100;
  }

  .sticky-cta .btn-primary {
    width: 100%;
  }
}

/* Pattern 3: CTA at terminal area (Gutenberg) */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 80vh;
}

.hero-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-cta-area {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;  /* Bottom of the grid = terminal area */
  align-items: flex-end;      /* Right side = terminal area */
  padding-bottom: 4rem;
}

/* Pattern 4: Multiple CTAs — visual hierarchy */
.cta-group {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.cta-group .btn-primary   { /* Filled — highest priority */ }
.cta-group .btn-secondary { /* Outlined — medium priority */ }
.cta-group .btn-tertiary  { /* Text — lowest priority */ }
```

### CTA Spacing from Context

```css
/* CTA should be visually connected to its context */
.pricing-card {
  display: flex;
  flex-direction: column;
  padding: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.pricing-card .price {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 1rem 0;
}

.pricing-card .features {
  flex: 1;          /* Push CTA to bottom — but still IN the card */
  margin-bottom: 1.5rem;
}

.pricing-card .btn-primary {
  width: 100%;      /* Full-width CTA inside card = clearly attached */
}
```

---

## 10. Content Grouping

### Card-Based Grouping

```css
/* Cards = distinct, actionable content units */
.card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Card with image */
.card-image {
  margin: -1.5rem -1.5rem 1.5rem;  /* Bleed to card edges */
  border-radius: 12px 12px 0 0;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
```

### Section-Based Grouping

```css
/* Sections = related content blocks */
.section {
  padding: 6rem 2rem;
}

/* Alternating backgrounds = visual separation */
.section:nth-child(even) {
  background: #f9fafb;
}

/* Section with contained width */
.section-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 600px;
  margin: 0 auto 3rem;
}

.section-header h2 {
  font-size: var(--text-2xl);
  margin-bottom: 1rem;
}

.section-header p {
  color: var(--color-muted);
  font-size: var(--text-lg);
}
```

### Dividers (Use Sparingly)

```css
/* Prefer whitespace over dividers */
/* But when needed, use subtle ones */
.divider {
  border: none;
  height: 1px;
  background: #e5e7eb;
  margin: 2rem 0;
}

/* Or use a more decorative divider */
.divider-ornament {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
  color: var(--color-muted);
}

.divider-ornament::before,
.divider-ornament::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e5e7eb;
}
```

### Sticky Headers for Context

```css
/* Sticky section header — maintains context while scrolling */
.sticky-header {
  position: sticky;
  top: 0;
  background: white;
  padding: 1rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  z-index: 10;
  /* Provides constant context: "which section am I in?" */
}
```

---

## 11. Responsive Placement

### Mobile-First Approach

```css
/* Base: single column (mobile) */
.layout {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
}

/* Most important content first in source order */
.main-content { order: 1; }
.sidebar      { order: 2; }  /* Below main on mobile */

/* Tablet: two-column */
@media (min-width: 768px) {
  .layout {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    padding: 2rem;
  }
}

/* Desktop: multi-column with persistent sidebar */
@media (min-width: 1024px) {
  .layout {
    grid-template-columns: 240px 1fr 300px;
    gap: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  .sidebar {
    position: sticky;
    top: 80px;
    align-self: start;
  }
}
```

### Thumb Zone Optimization (Mobile)

```css
/*
  Mobile thumb zones (one-handed, right-handed):

  ┌─────────────────────┐
  │  HARD    OK   HARD   │  ← Top: hard to reach
  │                      │
  │  OK     EASY   OK    │  ← Middle: comfortable
  │                      │
  │  EASY  EASY  EASY    │  ← Bottom: easiest (thumb natural rest)
  └─────────────────────┘
     ↑                    ↑
   Left edge          Right edge (for right-handed)
*/

/* Bottom navigation = easiest to reach */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  padding-bottom: env(safe-area-inset-bottom);
  background: white;
  border-top: 1px solid #e5e7eb;
}

/* Primary actions at bottom of screen */
.mobile-action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  background: white;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
}

/* FAB (Floating Action Button) — bottom-right = easy thumb reach */
.fab {
  position: fixed;
  bottom: 80px;  /* Above bottom nav */
  right: 16px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 50;
}
```

### Content Reflow (Most Important First)

```css
/* Mobile: reflow so most important content is first */
@media (max-width: 767px) {
  /* Use order to reorder content for mobile */
  .product-page .product-image { order: 1; }   /* Image first on mobile */
  .product-page .product-title { order: 2; }   /* Title */
  .product-page .product-price { order: 3; }   /* Price */
  .product-page .product-cta   { order: 4; }   /* Buy button */
  .product-page .product-desc  { order: 5; }   /* Description (long) */
  .product-page .product-specs { order: 6; }   /* Specs (longest) */
}

/* Desktop: side-by-side layout */
@media (min-width: 1024px) {
  .product-page {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }

  .product-page .product-image { grid-column: 1; grid-row: 1 / 6; }
  .product-page .product-title { grid-column: 2; }
  .product-page .product-price { grid-column: 2; }
  .product-page .product-cta   { grid-column: 2; }
  .product-page .product-desc  { grid-column: 2; }
  .product-page .product-specs { grid-column: 2; }
}
```

---

## 12. Attention Direction

### Visual Cues That Direct Attention

```css
/* 1. Arrows */
.arrow-down {
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-top: 12px solid var(--color-text);
  /* Points eye downward */
}

/* CSS arrow using borders */
.pointer-right::after {
  content: '';
  display: inline-block;
  width: 0;
  height: 0;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 6px solid currentColor;
  margin-left: 4px;
}

/* 2. Visual weight — darker = heavier = draws eye */
.heavy-element {
  background: #1f2937;  /* Dark background */
  color: white;
  font-weight: 700;
  /* Dark, bold elements have more visual weight */
}

.light-element {
  background: #f9fafb;
  color: #6b7280;
  font-weight: 400;
  /* Light, gray elements have less visual weight */
}

/* 3. Motion — animated elements draw attention */
.attention-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Notification badge — subtle animation draws eye */
.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 10px;
  height: 10px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid white;
  animation: badge-pulse 2s infinite;
}

@keyframes badge-pulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* 4. Contrast — high contrast = focal point */
.focal-point {
  background: var(--color-primary);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  /* Everything else is gray/white — this is the ONLY blue element = focal point */
}

/* 5. Novelty — unique elements stand out */
.unique-shape {
  clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
  /* Pentagon shape among rectangles = instant attention */
}

/* Diagonal element among horizontal/vertical elements */
.diagonal-banner {
  transform: rotate(-3deg);
  background: var(--color-primary);
  color: white;
  padding: 1rem 2rem;
  margin: 2rem -1rem;
  /* Tilt among straight elements = attention grab */
}
```

### Line of Sight

```css
/* Use visual flow to guide eye toward CTA */
.hero {
  position: relative;
}

/* Image looking toward the CTA */
.hero-image {
  /* Person in image should face right (toward CTA in LTR layout) */
  /* Or look down toward the form/button */
}

/* Lines/curves pointing to important element */
.hero::before {
  content: '';
  position: absolute;
  /* Curved line from headline to CTA */
  /* Implementation depends on design */
}

/* Grid lines converging on focal point */
.converging-grid {
  background-image:
    linear-gradient(to right, #f0f0f0 1px, transparent 1px),
    linear-gradient(to bottom, #f0f0f0 1px, transparent 1px);
  background-size: 50px 50px;
  /* Grid lines create implied convergence points */
}
```

---

## 13. Combined Reference Patterns

### Landing Page (All Principles Combined)

```css
/*
  STRUCTURE:
  1. Navigation (Hick's Law: 5 items max)
  2. Hero (Z-pattern, above fold, whitespace, CTA)
  3. Social proof (Proximity, Similarity)
  4. Features (F-pattern, Cards, Gestalt)
  5. Pricing (Hick's Law: 3-4 plans, Miller's: chunk features)
  6. CTA section (Gutenberg terminal, Whitespace)
  7. Footer (Layer-cake scanning)
*/

/* Hero: Z-pattern layout */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  padding: 2rem 4rem;
  gap: 3rem;
  align-items: center;
}

.hero-headline {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--color-muted);
  max-width: 50ch;
  margin-bottom: 2rem;
}

.hero-ctas {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* Social proof: Proximity + Similarity */
.social-proof {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  background: #f9fafb;
  border-radius: 12px;
  margin-top: 3rem;
}

.social-proof .logo {
  height: 24px;
  opacity: 0.6;
  filter: grayscale(100%);
  /* Similarity: all logos same style = "trusted by many" */
}

/* Features: Cards with Gestalt grouping */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.feature-card {
  padding: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.feature-card:hover {
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  margin-bottom: 1rem;
}

/* Pricing: Hick's Law (3 choices) + Miller's (chunk features) */
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.pricing-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

/* Featured plan: visual weight (Figure/Ground) */
.pricing-card.featured {
  border: 2px solid var(--color-primary);
  transform: scale(1.05);
  box-shadow: 0 12px 40px rgba(37, 99, 235, 0.15);
  position: relative;
}

.pricing-card.featured::before {
  content: 'Most Popular';
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: white;
  padding: 4px 16px;
  border-radius: 20px;
  font-size: var(--text-sm);
  font-weight: 600;
}

/* Final CTA: Whitespace + Gutenberg terminal */
.final-cta {
  text-align: center;
  padding: 8rem 2rem;
  /* Maximum whitespace = maximum importance */
}

.final-cta h2 {
  font-size: var(--text-3xl);
  margin-bottom: 1rem;
}

.final-cta p {
  font-size: var(--text-lg);
  color: var(--color-muted);
  max-width: 50ch;
  margin: 0 auto 2rem;
}

.final-cta .btn-primary {
  padding: 16px 40px;
  font-size: 1.125rem;
}
```

### Form Layout (All Principles Combined)

```css
/*
  PRINCIPLES APPLIED:
  - Miller's Law: 4-6 fields per step
  - Hick's Law: Progressive disclosure (multi-step)
  - Proximity: Label near input
  - Fitts' Law: Large touch targets
  - Figure/Ground: Clear form boundary
  - Whitespace: Breathing room between fields
*/

.form-card {
  max-width: 480px;
  margin: 4rem auto;
  padding: 2.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.form-card h2 {
  font-size: var(--text-xl);
  margin-bottom: 0.5rem;
}

.form-card .form-subtitle {
  color: var(--color-muted);
  margin-bottom: 2rem;
}

/* Progress indicator: continuity + closure */
.form-progress {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.form-progress-step {
  display: flex;
  align-items: center;
}

.form-progress-step .step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: var(--text-sm);
  border: 2px solid #e5e7eb;
  color: var(--color-muted);
}

.form-progress-step.active .step-number {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.form-progress-step.completed .step-number {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.form-progress-step:not(:last-child)::after {
  content: '';
  flex: 1;
  height: 2px;
  background: #e5e7eb;
  min-width: 40px;
  margin: 0 8px;
}

.form-progress-step.completed:not(:last-child)::after {
  background: #10b981;
}

/* Field grouping: proximity */
.form-section {
  margin-bottom: 2rem;
}

.form-field {
  margin-bottom: 1.25rem;
}

.form-field label {
  display: block;
  margin-bottom: 0.375rem;
  font-weight: 500;
  font-size: var(--text-sm);
}

.form-field input,
.form-field select {
  width: 100%;
  padding: 10px 14px;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  min-height: 44px;  /* Fitts' Law */
}

.form-field input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Submit button: Fitts' Law (full width on mobile) */
.form-submit {
  width: 100%;
  padding: 14px;
  font-size: 1rem;
  font-weight: 600;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  min-height: 48px;
  margin-top: 0.5rem;
}

/* Inline validation: proximity to field */
.form-field .error-message {
  color: #ef4444;
  font-size: var(--text-sm);
  margin-top: 0.25rem;  /* Close to the field it relates to */
}

.form-field input.error {
  border-color: #ef4444;
}
```

---

## Quick Reference Cheat Sheet

| Principle | Rule | One-Line CSS |
|-----------|------|-------------|
| **Size** | Bigger = more important | `font-size: clamp(2rem, 5vw, 4rem)` |
| **Contrast** | High contrast = focal point | `background: #2563EB; color: white` |
| **Position** | Top-left first (LTR) | `grid-area: 1 / 1` for hero headline |
| **Whitespace** | More space = more important | `padding: 6rem 2rem` |
| **Fitts' Law** | Big targets, close together | `min-width: 44px; min-height: 44px` |
| **Hick's Law** | Fewer choices = faster decisions | Show 5 options, "More" for rest |
| **Miller's Law** | 4-5 items per group | `grid-template-columns: repeat(5, 1fr)` |
| **Proximity** | Close = grouped | `gap: 8px` within group, `margin: 2rem` between |
| **Similarity** | Same style = same type | Consistent `.card` styling |
| **Continuity** | Lines connect elements | `border-left: 2px solid` for timeline |
| **Closure** | Brain fills gaps | `border-top` + `box-shadow` = perceived card |
| **Figure/Ground** | Pop elements forward | `box-shadow: 0 12px 40px` |
| **Common Region** | Border = group | `border: 1px solid; border-radius: 12px` |
| **Parallelism** | Same structure = peers | Consistent card layouts |

---

## Sources & Further Reading

- Nielsen Norman Group — "F-Shaped Pattern of Reading on the Web" (2006, updated 2019)
- Nielsen Norman Group — "Visual Hierarchy in Web Design" (2021)
- Steve Krug — "Don't Make Me Think" (3rd edition, 2014)
- Don Norman — "The Design of Everyday Things" (2013 revised edition)
- Miller, G.A. — "The Magical Number Seven, Plus or Minus Two" (1956)
- Cowan, N. — "The Magical Number 4 in Short-Term Memory" (2001)
- Fitts, P.M. — "The Information Capacity of the Human Motor System" (1954)
- Hick, W.E. — "On the Rate of Gain of Information" (1952)
- Wertheimer, M. — "Laws of Organization in Perceptual Forms" (1923) — Gestalt principles
- Google Material Design — Touch target guidelines (48dp minimum)
- Apple Human Interface Guidelines — Minimum touch target (44x44pt)

---

> Report compiled by Bauna Intern | Layout Psychology Research | 2026-05-20
