<div class="domain-header">
  <span class="skill-badge craft">Craft</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Process</span>
</div>

# Painter

Impeccable UI/UX design. Every pixel intentional. Every animation purposeful. Every color choice psychologically reasoned. You do not do "good enough" — you do impeccable.

## When to Use

- User asks to design, build, fix, or audit UI/UX
- User says "make it look good", "design this", "fix the ui"
- User wants hero sections, dashboards, landing pages
- User wants animation, scroll effects, micro-interactions

## Triggers

```
/painter [command]
"make it look pro", "fix the ui", "design this", "hero section",
"dashboard", "animation", "scroll effects", "color palette"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Design a landing page hero</div>
<div class="example-desc">Create a hero section with scroll-linked animations and proper typography.</div>

```
/painter hero section for a TPU benchmarking dashboard

The agent designs a hero with:
- Montserrat 800 for headline, 300 for subtitle
- OKLCH color system with tinted neutrals
- Scroll-linked parallax on background elements
- Staggered text reveal animation (expo-out easing)
- CTA buttons with hover lift + shadow micro-interaction
- Responsive: stacked on mobile, side-by-side on desktop
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Audit existing UI for anti-patterns</div>
<div class="example-desc">Score the current UI against Nielsen's heuristics and fix issues.</div>

```
/painter audit

The agent runs a full critique:
- Heuristics scoring (0-40 scale)
- Slop detection (gradient text? identical card grids?)
- Persona walkthrough (Alex, Jordan, Sam)
- Audit dimensions: accessibility, performance, theming,
  responsive, anti-patterns
- Priority-tagged fix list (P0-P3)
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Design system with micro-interactions</div>
<div class="example-desc">Create a component library with proper hover states, focus rings, and transitions.</div>

```
/painter design system

The agent creates:
- Button states: default, hover (translateY -2px), active
  (scale 0.97), loading (spinner), disabled
- Card hover: lift + multi-layer shadow
- Link: underline wipe effect (scaleX 0→1)
- Focus rings: 2px offset, brand color, :focus-visible
- Form inputs: floating labels, inline validation
- All transitions use expo-out easing, <300ms
```
</div>

<div class="example-box">
<div class="example-label">Example 4</div>
<div class="example-title">Production-ready UI pipeline</div>
<div class="example-desc">Design then harden — the full pipeline.</div>

```
/painter → /harden

Painter creates the visual design with proper colors,
typography, spacing, and animations. Harden wraps it
with production patterns: error boundaries, loading
states, accessibility attributes, performance budgets.
```
</div>

## Capabilities

| Area | Coverage |
|------|----------|
| **Visual Design** | Color psychology, typography, layout, spacing |
| **Animation** | CSS animations, scroll effects, micro-interactions |
| **3D/WebGL** | Three.js, shaders, particle systems |
| **Design Systems** | Component libraries, tokens, patterns |
| **Accessibility** | WCAG compliance, screen readers, keyboard nav |
| **Responsive** | Mobile-first, breakpoints, fluid layouts |
