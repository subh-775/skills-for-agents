# Painter

Max pro UI/UX design with WebGPU/shader support for GPU-accelerated effects. Handles animation, color, typography, layout, interaction, accessibility, and advanced visual effects.

## Domain

**Craft** — controls visual design, UI/UX, motion, color, typography, layout, interaction design, accessibility, and performance of frontend output.

## When to Use

- `/painter [command]` or "make it look pro", "fix the ui"
- "gpu effects", "shader animation", "particle system", "fluid animation", "webgpu ui"
- Frontend code generation, design system creation, visual critique and scoring

## Commands

| Command | Purpose |
|---------|---------|
| `paint` | Godmode — full analyze, diagnose, plan, implement, test loop |
| `analyze` | Run full critique — heuristics scoring, slop detection, persona walkthrough |
| `polish` | Refine existing design |
| `shape` | Design brief via discovery |
| `craft` | Build from design brief |
| `audit` | Score accessibility, performance, theming, responsive, anti-patterns |
| `animate` | Motion design |
| `colorize` | Color system work |
| `typeset` | Typography rules |
| `layout` | Spatial design and grid |
| `bolder` | Amplification — stronger hierarchy, sharper accents |
| `quieter` | Refinement — reduce saturation, neutral dominance |
| `distill` | Simplification — one primary action, progressive disclosure |
| `harden` | Resilience — test with extreme inputs |
| `onboard` | First-run experience design |
| `overdrive` | Extraordinary effects — View Transitions, spring physics, WebGL/WebGPU |
| `optimize` | Core Web Vitals — LCP, INP, CLS |
| `extract` | Generate DESIGN.md from existing UI |
| `gpu` | WebGPU effects — particles, fluid sims, procedural gradients |

## Key Concepts

**Register Split**: Brand mode (design IS the product) vs Product mode (design SERVES the product). Brand allows typographic risk and motion-heavy entrances. Product favors familiar patterns and 150-250ms transitions.

**Absolute Bans**: Side-stripe borders, gradient text, glassmorphism as default, hero-metric template, identical card grids, modal as first thought, cyan/purple neon on dark.

**Motion Quick Ref**: 100-150ms feedback, 200-300ms state changes, 500-800ms entrances. Easing: `cubic-bezier(0.16, 1, 0.3, 1)`. Only animate `transform` + `opacity`. Mandatory `prefers-reduced-motion` fallback.

**Color**: Use OKLCH (not HSL). Tinted neutrals (0.005-0.01 chroma). Never pure `#000` or `#fff`. Dark mode: depth from surface lightness, reduce text weight.

**Spatial Design**: 4pt grid. Semantic tokens (`--space-sm`). Use `gap` not margins. Cards are the lazy answer — never nest them. Touch targets: 44px minimum.

**Heuristics Scoring**: Nielsen's 10 heuristics, 0-4 each. 36-40 Excellent, 28-35 Good, 20-27 Acceptable, 12-19 Poor, 0-11 Critical.

**Five Audit Dimensions**: Accessibility, Performance, Theming, Responsive, Anti-patterns. Each 0-4, total /20.

## Composability

```yaml
domain: craft
composable: true
yields_to: [voice, process]
```

Painter owns **craft** — everything visual about frontend output. CSS values, design tokens, and technical specs are never compressed or overridden.

### When Painter Leads

- Any request to design, build, fix, or audit UI
- Frontend code generation or modification
- Design system creation or enforcement
- Visual critique and scoring

### When Painter Defers

| Other Skill's Domain | What Painter Does |
|---------------------|-------------------|
| **Voice** | Painter handles code and visuals. Voice handles prose and explanations. UX copy is shared territory. |
| **Density** | Design knowledge stays dense. Compress teaching, keep implementation. `cubic-bezier(0.16, 1, 0.3, 1)` stays verbatim. |
| **Process** | Painter fills craft sections within a process framework. Doesn't restructure the overall document. |
| **Content** | Painter doesn't invent content. It shapes how content is presented visually. |

## Related Skills

- [Slidify](./slidify) — visual design guidance for slide templates
- [Blogger](./blogger) — voice skill that composes on UX copy
- [Postmortem](./postmortem) — advisory mode for UI-related incidents
- [Documenter](./documenter) — content skill that defers to painter on visual presentation

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/painter/SKILL.md) — complete craft guide with all commands
- [SIP Framework](/guide/sip-framework) — how painter composes
