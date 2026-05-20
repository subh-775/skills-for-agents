# Design Styles Reference

> Comprehensive guide to UI/web design aesthetics, movements, and implementation patterns.

---

## 1. Glassmorphism

### History and Evolution

Glassmorphism emerged around 2020 when Apple introduced it in macOS Big Sur and iOS 14. The frosted-glass aesthetic replaced the flat design that dominated since iOS 7 (2013). Microsoft had explored similar territory with Fluent Design's "Acrylic" material in Windows 10 (2017), but Apple popularized it for the web. By 2021, every SaaS landing page had glassmorphic cards. By 2022, backlash began — overuse made it feel generic. In 2025-2026, it's used selectively, not as a default.

### What Defines It

- Semi-transparent backgrounds with blur (frosted glass effect)
- Subtle white/light borders on edges (simulating glass refraction)
- Multi-layered depth with background content visible through the surface
- Soft shadows that suggest floating above the background
- Vibrant, colorful backgrounds (gradients, images) that show through

### When It Works vs When It Fails

**Works when:**
- Overlaying content on rich backgrounds (hero images, video, gradients)
- Creating visual hierarchy without solid color blocks
- The background is intentionally designed to show through
- Used on 1-2 layers max, not stacked glass-on-glass
- Paired with strong typography and clear content

**Fails when:**
- Background is plain/solid — the blur does nothing, just looks like a gray overlay
- Too many glass layers stacked — becomes muddy and unreadable
- Text contrast is insufficient (WCAG AA requires 4.5:1)
- Used on every element — becomes visual noise
- Over animated/complex backgrounds — causes motion sickness

### CSS Implementation

```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px); /* Safari */
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  padding: 24px;
}

/* Dark mode variant */
.glass-card-dark {
  background: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Always provide solid fallback for browsers without backdrop-filter */
@supports not (backdrop-filter: blur(1px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
}
```

### Accessibility Concerns

- **Contrast is the #1 problem.** Glass over bright gradients can drop text contrast below 2:1. Always test with a contrast checker.
- **Solution:** Add a solid dark/light scrim behind text: `background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(...);`
- **Reduced motion:** Disable any animated backgrounds behind glass elements for `prefers-reduced-motion`.
- **Screen readers:** Glass is purely visual — ensure semantic HTML underneath.

### Best Use Cases

- Cards over hero images or gradient backgrounds
- Modal dialogs and overlays
- Sidebars/navigation drawers
- Dashboard widgets over a subtle gradient canvas
- Pricing cards on colorful backgrounds

### Anti-Patterns

- Glass cards on white/solid backgrounds (blur does nothing)
- 3+ stacked glass layers (muddy, unreadable)
- Glass on every element (buttons, inputs, cards, nav — pick one)
- Small text over complex glass (headings only)
- Animated backgrounds directly behind glass (performance + nausea)

### Color Palette

- Background: vibrant gradient (e.g., `linear-gradient(135deg, #667eea, #764ba2, #f093fb)`)
- Glass surface: `rgba(255,255,255, 0.1-0.25)` on light, `rgba(0,0,0, 0.15-0.35)` on dark
- Border: `rgba(255,255,255, 0.15-0.3)`
- Text: High-contrast white or near-white on dark glass, dark on light glass

### Typography Pairing

- Headings: Inter, Poppins, or Sora (geometric sans, clean on glass)
- Body: Inter, DM Sans (high x-height for readability at lower contrast)
- Avoid: serif fonts (clash with the modern glass aesthetic), thin weights (vanish on glass)

### Famous Examples

- Apple macOS Big Sur / iOS control center
- Spotify Wrapped (glassmorphic cards over gradient)
- Many Figma community templates
- Stripe's early dashboard explorations

---

## 2. Brutalism (Web Brutalism)

### Philosophy

Web brutalism borrows from the architectural movement of the 1950s-70s (Le Corbusier, Alison and Peter Smithson) — raw concrete, exposed structure, function over ornament. In web design, it rejects polish, corporate smoothness, and the homogeneity of modern SaaS design. It's intentionally raw, sometimes ugly, always honest. The message: "We don't need your rounded corners and gradient buttons."

### Key Characteristics

- **Monospace fonts** (or system defaults) — no web font pretension
- **Raw HTML aesthetics** — default browser styling, unstyled form elements
- **No rounded corners** — sharp edges, raw borders (2-3px solid black)
- **Stark contrast** — black/white, with one accent color max
- **Visible grid** — borders, rules, structural lines are features not bugs
- **Oversized typography** — massive headings, often all-caps
- **No shadows, no gradients, no blur** — flat in the truest sense
- **System cursors** — default pointer, text cursor
- **Breaks conventions intentionally** — horizontal scroll, unusual navigation

### When to Use

- Art portfolios, creative agencies, design studios
- Anti-corporate brands, punk/DIY aesthetics
- Music labels, indie publications
- When the brand identity IS the rebellion against polish
- Experimental/personal sites

### When NOT to Use

- E-commerce (users need trust, not confrontation)
- SaaS products (usability suffers)
- Healthcare, finance, government (credibility matters)
- Accessibility-first projects (brutalism often sacrifices a11y)

### CSS Implementation

```css
/* Brutalist foundation */
:root {
  --raw-black: #000000;
  --raw-white: #ffffff;
  --accent: #ff0000;
  --border: 2px solid var(--raw-black);
}

body {
  font-family: 'Courier New', Courier, monospace;
  background: var(--raw-white);
  color: var(--raw-black);
  margin: 0;
  cursor: default;
}

h1 {
  font-size: clamp(3rem, 10vw, 8rem);
  text-transform: uppercase;
  letter-spacing: -0.03em;
  line-height: 0.9;
  margin: 0;
  border-bottom: var(--border);
  padding: 16px;
}

.card {
  border: var(--border);
  border-radius: 0;
  padding: 24px;
  background: none;
  box-shadow: none;
}

.card:hover {
  background: var(--raw-black);
  color: var(--raw-white);
}

a {
  color: var(--raw-black);
  text-decoration: underline;
  text-underline-offset: 4px;
}

a:hover {
  background: var(--accent);
  color: var(--raw-white);
}

/* Visible grid lines */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 0;
}

.grid > * {
  border: var(--border);
  padding: 24px;
}
```

### Color Palette

- Primary: `#000000` (black), `#ffffff` (white)
- Accent: `#ff0000` (red), `#0000ff` (blue), or `#ffcc00` (yellow)
- Max 2-3 colors total. No tints, no shades.

### Typography Pairing

- Primary: Courier New, Space Mono, JetBrains Mono (monospace)
- Display: Arial Black, Impact, or a single bold grotesque
- No decorative fonts. No Google Fonts prettiness.

### Famous Examples

- Bloomberg.com (redesign circa 2016 — the poster child)
- Balenciaga.com (high-fashion brutalism)
- Yale School of Art (art-school brutalism)
- Hacker News (accidental brutalism)
- Ling's Cars (maximalist brutalism)

---

## 3. Neumorphism (Soft UI)

### What It Is

Neumorphism (also "neomorphism" or "Soft UI") emerged around 2019-2020, credited to designer Alexander Plyuto. It creates the illusion that UI elements are extruded from or pressed into the background surface — like soft clay or embossed paper. Everything looks like it's part of one continuous surface.

### Why It Fell Out of Favor

- **Accessibility nightmare:** Low contrast between elements and background. The "pressed" and "raised" states look nearly identical to colorblind users.
- **Disabled states are impossible:** How do you make a "disabled" button look different when the entire design is soft and subtle?
- **Real-world testing failure:** Users couldn't distinguish interactive elements from decorative ones.
- **Limited to specific backgrounds:** Only works on mid-tone, neutral backgrounds. White or black backgrounds break the illusion.
- **Performance:** Multiple layered box-shadows on every element slow rendering.

### When It Can Still Work

- **Dark mode:** Higher contrast achievable, shadows more visible
- **Music players / media controls:** The tactile, button-like feel suits play/pause/volume
- **Calculators, toggles, sliders:** Physical-feeling controls
- **Single-screen apps:** Not for multi-page navigation
- **When the entire UI is neumorphic:** Partial neumorphism looks broken

### CSS Implementation

```css
/* Neumorphic foundation — light mode */
:root {
  --bg: #e0e5ec;
  --shadow-light: #ffffff;
  --shadow-dark: #a3b1c6;
}

.neu-raised {
  background: var(--bg);
  border-radius: 16px;
  box-shadow:
    8px 8px 16px var(--shadow-dark),
    -8px -8px 16px var(--shadow-light);
  padding: 24px;
  border: none;
}

/* Pressed/inset state */
.neu-inset {
  background: var(--bg);
  border-radius: 16px;
  box-shadow:
    inset 8px 8px 16px var(--shadow-dark),
    inset -8px -8px 16px var(--shadow-light);
  padding: 24px;
}

/* Button with interactive states */
.neu-button {
  background: var(--bg);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  box-shadow:
    5px 5px 10px var(--shadow-dark),
    -5px -5px 10px var(--shadow-light);
  cursor: pointer;
  transition: box-shadow 0.15s ease;
}

.neu-button:active {
  box-shadow:
    inset 5px 5px 10px var(--shadow-dark),
    inset -5px -5px 10px var(--shadow-light);
}

/* Dark neumorphism — works better */
.neu-dark {
  --bg: #2d2d35;
  --shadow-light: rgba(255, 255, 255, 0.05);
  --shadow-dark: rgba(0, 0, 0, 0.5);
}
```

### Color Palette

- Background: `#e0e5ec` (light gray-blue) or `#2d2d35` (dark)
- Shadows: lighter and darker variants of the background (not black/white)
- Accent: ONE saturated color for interactive elements
- No gradients on surfaces

### Typography Pairing

- Headings: Nunito, Poppins (rounded, soft — matches the aesthetic)
- Body: Inter, DM Sans (readable at the low contrast)
- Avoid: sharp/geometric fonts (clash with softness)

### Famous Examples

- Alexander Plyuto's original Dribbble shots
- Music player UIs on Dribbble
- Some smart home control panels
- Calculator apps

---

## 4. Claymorphism

### What It Is

Claymorphism emerged around 2022 as a playful evolution — 3D clay-like elements that look soft, rounded, and colorful, like characters from a Pixar movie or objects made of modeling clay. It adds inner shadows and highlights to create a puffy, inflated 3D look.

### CSS Implementation

```css
.clay-card {
  background: #f5f0ff;
  border-radius: 24px;
  padding: 32px;
  box-shadow:
    /* outer shadow for depth */
    12px 12px 24px rgba(166, 150, 180, 0.4),
    /* inner highlight for 3D effect */
    inset 0 4px 8px rgba(255, 255, 255, 0.8),
    /* inner shadow for roundness */
    inset 0 -4px 8px rgba(0, 0, 0, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.6);
}

/* Colored clay element */
.clay-blob {
  background: #ff6b9d;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  box-shadow:
    8px 8px 16px rgba(200, 80, 120, 0.4),
    inset 0 4px 8px rgba(255, 255, 255, 0.3),
    inset 0 -4px 8px rgba(0, 0, 0, 0.1);
  border: 3px solid rgba(255, 255, 255, 0.3);
}
```

### When to Use

- Children's apps and games
- Playful brands (food, toys, entertainment)
- Onboarding flows (friendly, approachable)
- Illustration-heavy sites
- 404 pages, empty states, fun moments

### When NOT to Use

- Enterprise/B2B software
- Data-heavy dashboards
- Serious/medical/financial contexts
- Accessibility-first designs (the 3D effect reduces contrast)

### Color Palette

- Soft pastels: `#f5f0ff` (lavender), `#fff0f5` (pink), `#f0fff5` (mint)
- Accent clays: `#ff6b9d` (coral), `#6c5ce7` (purple), `#00cec9` (teal)
- Background: light neutral `#faf8ff`

### Typography Pairing

- Headings: Nunito, Baloo 2, Quicksand (rounded, bubbly)
- Body: Nunito, Open Sans (friendly, readable)
- Avoid: sharp serifs, condensed fonts

### Famous Examples

- Dribbble clay-style illustrations
- Some fintech apps targeting Gen Z
- Gaming landing pages
- Kids' educational platforms

---

## 5. Aurora UI

### What It Is

Aurora UI uses soft, blurred gradient blobs that float and animate like the northern lights. It emerged around 2021-2022 as a reaction to flat design fatigue. Companies like Vercel, Linear, and Stripe popularized it for SaaS landing pages. The effect is organic, modern, and premium-feeling.

### CSS Implementation

```css
.aurora-bg {
  position: relative;
  min-height: 100vh;
  background: #0a0a0f;
  overflow: hidden;
}

.aurora-bg::before,
.aurora-bg::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.5;
  animation: aurora-float 8s ease-in-out infinite;
}

.aurora-bg::before {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #7c3aed, transparent 70%);
  top: -200px;
  left: -100px;
}

.aurora-bg::after {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #06b6d4, transparent 70%);
  bottom: -200px;
  right: -100px;
  animation-delay: -4s;
}

/* Multiple aurora blobs via extra elements */
.aurora-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  mix-blend-mode: screen;
}

.aurora-blob--1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #8b5cf6, transparent 70%);
  top: 20%;
  left: 30%;
  animation: aurora-drift 12s ease-in-out infinite;
}

.aurora-blob--2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #ec4899, transparent 70%);
  top: 40%;
  right: 20%;
  animation: aurora-drift 10s ease-in-out infinite reverse;
}

@keyframes aurora-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.05); }
  66% { transform: translate(-20px, 30px) scale(0.95); }
}

@keyframes aurora-drift {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(40px, -40px); }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .aurora-bg::before,
  .aurora-bg::after,
  .aurora-blob {
    animation: none;
  }
}
```

### When to Use

- Modern SaaS landing pages
- Tech brands (AI, dev tools, infrastructure)
- Hero sections that need visual impact
- Dark-mode-first designs
- Premium/prestige positioning

### When NOT to Use

- Content-heavy pages (aurora distracts from reading)
- Light-mode designs (aurora is best on dark)
- Performance-constrained contexts (blur is GPU-heavy)
- When every competitor is already doing it (2024-2025 SaaS fatigue)

### Color Palette

- Background: `#0a0a0f` (near-black with blue tint)
- Blob 1: Purple/violet (`#7c3aed`, `#8b5cf6`)
- Blob 2: Cyan/teal (`#06b6d4`, `#22d3ee`)
- Blob 3: Pink/magenta (`#ec4899`, `#f472b6`)
- Text: `#f4f4f5` (near-white)

### Typography Pairing

- Headings: Inter, General Sans, Satoshi (modern geometric)
- Body: Inter, system-ui (clean, technical)
- Monospace accent: JetBrains Mono for code/dev content

### Famous Examples

- Vercel.com (gradient mesh hero)
- Linear.app (subtle aurora backgrounds)
- Stripe.com (color-shifting gradients)
- Resend.com, Cal.com

---

## 6. Memphis Design

### What It Is

Memphis design originated in 1981 with the Memphis Group (founded by Ettore Sottsass in Milan). It rejected modernism's "good taste" with clashing colors, geometric shapes, squiggly lines, and playful patterns. In web design, it experienced a revival around 2018-2022 as a reaction to minimalism's sterility.

### Key Characteristics

- Geometric shapes (circles, triangles, zigzags, dots)
- Bold, clashing colors (pink, yellow, teal, purple)
- Playful patterns (polka dots, stripes, checkerboards)
- Asymmetric layouts
- Mixed illustration styles
- Confident, loud, unapologetic

### When to Use

- Creative agencies, design studios
- Children's products, education
- Fun campaigns, event pages
- Brands targeting younger demographics
- When differentiation from corporate blandness is the goal

### When NOT to Use

- Enterprise/B2B (too playful, not trustworthy)
- Data-heavy interfaces (shapes compete with data)
- Accessibility-first (high visual complexity)
- Long-form reading (shapes distract)

### CSS Implementation

```css
/* Memphis shapes via CSS */
.memphis-bg {
  position: relative;
  background: #fef5e7;
  overflow: hidden;
}

/* Floating geometric shapes */
.memphis-shape {
  position: absolute;
  z-index: 0;
}

.memphis-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #ff6b6b;
  top: 10%;
  left: 5%;
}

.memphis-triangle {
  width: 0;
  height: 0;
  border-left: 60px solid transparent;
  border-right: 60px solid transparent;
  border-bottom: 104px solid #4ecdc4;
  top: 30%;
  right: 10%;
  transform: rotate(15deg);
}

.memphis-zigzag {
  width: 200px;
  height: 40px;
  background: repeating-linear-gradient(
    -45deg,
    transparent,
    transparent 8px,
    #ffe66d 8px,
    #ffe66d 16px
  );
  bottom: 20%;
  left: 15%;
}

.memphis-dots {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, #2d3436 3px, transparent 3px);
  background-size: 20px 20px;
  top: 50%;
  right: 5%;
  opacity: 0.3;
}

/* Squiggly line via SVG background */
.memphis-squiggle {
  width: 300px;
  height: 60px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 40'%3E%3Cpath d='M0 20 Q25 0 50 20 T100 20 T150 20 T200 20 T250 20 T300 20' fill='none' stroke='%23ff6b6b' stroke-width='3'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  position: absolute;
  bottom: 10%;
  right: 20%;
}
```

### Color Palette

- Pink: `#ff6b6b`
- Teal: `#4ecdc4`
- Yellow: `#ffe66d`
- Purple: `#a55eea`
- Dark: `#2d3436`
- Background: `#fef5e7` (warm cream) or `#ffffff`

### Typography Pairing

- Headings: Rubik, Poppins, Space Grotesk (geometric, bold)
- Body: DM Sans, Work Sans (clean, friendly)
- Accent: Any bold display font for impact words

### Famous Examples

- Moma Design Store (80s revival)
- Many startup landing pages (2019-2021)
- Slack's early illustrations
- Mailchimp's playful campaigns

---

## 7. Skeuomorphism (Modern Revival)

### What It Was

Skeuomorphism dominated UI design from 2007-2013 (iPhone OS 1 through iOS 6). Interfaces mimicked real-world objects — leather textures, wooden shelves, paper notebooks, felt poker tables, glossy buttons with bevels. Steve Jobs insisted on it. It helped users transition from physical to digital by using familiar metaphors.

### How It's Coming Back

The 2024-2026 revival is subtler — not full skeuomorphic interfaces, but:
- Subtle textures (linen, paper grain, noise) on backgrounds
- Tactile button effects (press states that look physically pushed)
- Depth through soft shadows and highlights (not flat)
- Icon design with realistic materials (glass, metal, wood)
- Note-taking apps that look like actual notebooks
- Music apps with vinyl/turntable metaphors

### When to Use

- Music/audio apps (turntables, mixers, knobs)
- Note-taking/journaling (paper, leather textures)
- Gaming interfaces (immersive, themed)
- Smart home controls (switches, dials)
- When the app's purpose maps to a physical object

### When NOT to Use

- Data-heavy dashboards (textures compete with data)
- When realism adds cognitive load without value
- Performance-constrained (textures are heavier than flat colors)
- When users are digital-native and don't need physical metaphors

### CSS Implementation

```css
/* Subtle paper texture */
.note-app {
  background-color: #f5f0e8;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4'%3E%3Crect width='4' height='4' fill='%23f5f0e8'/%3E%3Crect width='1' height='1' fill='%23ece7db'/%3E%3C/svg%3E");
}

/* Tactile button */
.tactile-btn {
  background: linear-gradient(180deg, #f0f0f0, #d4d4d4);
  border: 1px solid #b0b0b0;
  border-radius: 8px;
  box-shadow:
    0 2px 4px rgba(0,0,0,0.2),
    inset 0 1px 0 rgba(255,255,255,0.8),
    inset 0 -1px 0 rgba(0,0,0,0.05);
  padding: 10px 20px;
  font-family: -apple-system, system-ui;
  cursor: pointer;
}

.tactile-btn:active {
  box-shadow:
    inset 0 2px 4px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(0,0,0,0.05);
  transform: translateY(1px);
}

/* Leather texture card */
.leather-card {
  background-color: #8b6914;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23n)' opacity='0.1'/%3E%3C/svg%3E");
  border-radius: 4px;
  border: 1px solid #6b5010;
  box-shadow:
    0 4px 8px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.1);
  padding: 20px;
  color: #f0e6d0;
}

/* Noise texture overlay */
.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
  mix-blend-mode: multiply;
}
```

### Color Palette

- Warm neutrals: `#f5f0e8` (paper), `#e8e0d0` (aged white)
- Rich materials: `#8b6914` (leather), `#5c3a1e` (wood), `#2a2a2a` (metal)
- Accents: muted, natural tones (forest green, burgundy, navy)

### Typography Pairing

- Headings: Georgia, Merriweather (warm, editorial)
- Body: Charter, Lora (readable, textured feel)
- Avoid: ultra-modern geometric sans (clashes with organic feel)

### Famous Examples

- Apple's iOS Notes app (subtle paper texture)
- Bear note-taking app
- Many weather apps (realistic weather icons)
- Music production apps (DAWs with realistic knobs)

---

## 8. Dark Mode Design

### Not Just Inverting Colors

Proper dark mode is NOT `filter: invert(1)` or swapping black/white. It requires a complete rethinking of the color system:

### Surface Elevation Through Lightness

In light mode, depth is communicated through shadows. In dark mode, **lighter surfaces appear closer**:

```css
:root {
  /* Light mode: shadow-based depth */
  --surface-1: #ffffff;  /* base */
  --surface-2: #ffffff;  /* elevated (gets shadow) */
  --surface-3: #ffffff;  /* more elevated (bigger shadow) */
}

:root[data-theme="dark"] {
  /* Dark mode: lightness-based depth */
  --surface-1: #0f0f0f;  /* base — darkest */
  --surface-2: #1a1a1a;  /* elevated — slightly lighter */
  --surface-3: #242424;  /* more elevated — lighter still */
}
```

### Accent Color Desaturation

Saturated colors vibrate on dark backgrounds, causing eye strain. Desaturate and lighten:

```css
:root {
  --accent: #3b82f6;        /* blue-500 */
  --accent-hover: #2563eb;  /* blue-600 */
}

:root[data-theme="dark"] {
  --accent: #60a5fa;        /* blue-400 — lighter */
  --accent-hover: #93bbfd;  /* blue-300 — even lighter */
}
```

### Text Weight Reduction

Heavy text on dark backgrounds looks bloated. Reduce weight:

```css
:root {
  --text-body-weight: 400;
  --text-heading-weight: 700;
}

:root[data-theme="dark"] {
  --text-body-weight: 350;    /* slightly lighter */
  --text-heading-weight: 600;  /* reduce heading weight */
}
```

### Image Handling

```css
/* Reduce image brightness slightly to prevent "flash" */
:root[data-theme="dark"] img {
  filter: brightness(0.9);
}

/* Or use a subtle overlay */
:root[data-theme="dark"] .img-container {
  position: relative;
}

:root[data-theme="dark"] .img-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.1);
  pointer-events: none;
}
```

### Full Dark Mode Implementation

```css
:root[data-theme="dark"] {
  /* Surfaces */
  --bg: #0f0f0f;
  --surface-1: #141414;
  --surface-2: #1c1c1c;
  --surface-3: #242424;

  /* Text */
  --text-primary: #e8e8e8;    /* NOT #fff — too harsh */
  --text-secondary: #a0a0a0;
  --text-tertiary: #6b6b6b;

  /* Borders */
  --border: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.15);

  /* Accents (desaturated) */
  --accent: #60a5fa;
  --accent-muted: rgba(96, 165, 250, 0.15);

  /* Shadows (subtle, colored) */
  --shadow: 0 4px 16px rgba(0, 0, 0, 0.4);

  /* Typography adjustments */
  --text-body-weight: 350;
  --text-heading-weight: 600;
  --line-height-boost: 0.05;  /* add to base line-height */
}
```

### When to Use

- Always offer as an option (user preference)
- Default for media/video apps, code editors, gaming
- Essential for battery savings on OLED screens
- Reduces eye strain in low-light environments

### When NOT to Use

- Don't force dark mode — respect `prefers-color-scheme` AND manual toggle
- Avoid for print-heavy content (dark bg uses more ink)
- Avoid for data visualization without careful color work

### Color Palette

- Background: `#0f0f0f` (not pure black)
- Surfaces: `#141414`, `#1c1c1c`, `#242424`
- Text: `#e8e8e8` (primary), `#a0a0a0` (secondary)
- Borders: `rgba(255,255,255, 0.08-0.15)`

### Typography Pairing

- Same as light mode, but reduce weights
- Increase line-height by 0.05
- Increase letter-spacing by 0.01-0.02em

---

## 9. Bento Box / Bento Grid

### What It Is

Popularized by Apple (especially their keynote presentations and product pages), the Bento Grid is an asymmetric grid layout where items span different column/row sizes, creating an organic, magazine-like composition. Named after Japanese bento lunch boxes with their compartmentalized sections.

### How to Build It

```css
/* Bento Grid Foundation */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 200px);
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px;
}

/* Varied spans create the bento effect */
.bento-item--hero {
  grid-column: span 2;
  grid-row: span 2;
}

.bento-item--wide {
  grid-column: span 2;
}

.bento-item--tall {
  grid-row: span 2;
}

.bento-item--standard {
  grid-column: span 1;
  grid-row: span 1;
}

/* Bento cards */
.bento-item {
  background: var(--surface-2);
  border-radius: 20px;
  padding: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

/* Responsive: collapse to single column on mobile */
@media (max-width: 768px) {
  .bento-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }

  .bento-item--hero,
  .bento-item--wide,
  .bento-item--tall {
    grid-column: span 1;
    grid-row: span 1;
  }
}

/* Alternative: auto-fit bento */
.bento-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-auto-rows: 200px;
  gap: 16px;
}

/* Subgrid for internal alignment (modern browsers) */
.bento-item {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 2;
}
```

### Content Types That Work

- Feature highlights (icon + title + description)
- Stats/metrics (big number + label)
- Images/illustrations (full-bleed in card)
- Testimonials (quote + author)
- Code snippets
- Interactive widgets (mini charts, toggles)
- Video thumbnails

### Responsive Behavior

- Desktop: full grid with varied spans (4-6 columns)
- Tablet: 2-3 columns, some items collapse
- Mobile: single column, all items full-width
- Use `container queries` for component-level responsiveness

### Color Palette

- Surface: `#f5f5f7` (Apple-style light gray)
- Cards: `#ffffff` or subtle gradient
- Dark mode: `#1c1c1e` surface, `#2c2c2e` cards
- Accent: single brand color for highlights

### Typography Pairing

- Headings: SF Pro, Inter, system-ui (clean, technical)
- Body: Same family, lighter weight
- Numbers/metrics: Tabular figures (`font-variant-numeric: tabular-nums`)

### Famous Examples

- Apple.com product pages (iPhone, MacBook features)
- Apple keynote presentations
- Vercel dashboard
- Linear feature pages
- Many modern SaaS landing pages (2023-2026)

---

## 10. Minimalism vs Maximalism

### Minimalism

**When it works:** SaaS products, productivity tools, enterprise software, developer tools, documentation sites.

**How to do it right (not just "less stuff"):**

```css
/* Minimalism done right: intentional whitespace, strong hierarchy */
.minimal-layout {
  --space-unit: 8px;
  max-width: 72ch;  /* optimal reading width */
  margin: 0 auto;
  padding: calc(var(--space-unit) * 8);  /* 64px */
}

.minimal-heading {
  font-size: 2.5rem;
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: calc(var(--space-unit) * 3);  /* 24px */
  color: #111;
}

.minimal-text {
  font-size: 1.125rem;
  line-height: 1.7;
  color: #555;
  max-width: 60ch;
}

/* Minimalism is hierarchy through space, not decoration */
.minimal-section {
  margin-bottom: calc(var(--space-unit) * 10);  /* 80px */
}

.minimal-divider {
  /* Not a line — space IS the divider */
  margin-top: calc(var(--space-unit) * 12);
}
```

**Minimalism principles:**
- Every element must earn its place
- Hierarchy through size, weight, and space — not decoration
- 1-2 colors + neutrals
- One font family, 3-4 sizes
- Generous whitespace (it's not empty, it's breathing room)
- Functional, not boring

### Maximalism

**When it works:** Fashion brands, entertainment, art, music, luxury, creative campaigns, Gen Z targeting.

**How to do it right (not just "more stuff"):**

```css
/* Maximalism done right: controlled chaos */
.maximal-layout {
  background: #0a0a0a;
  position: relative;
  overflow: hidden;
}

/* Layered, but intentional */
.maximal-hero {
  position: relative;
  padding: 80px 40px;
  background:
    linear-gradient(135deg, rgba(255,0,100,0.3), rgba(0,100,255,0.3)),
    repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
}

/* Mixed typography is OK in maximalism */
.maximal-heading {
  font-size: clamp(4rem, 12vw, 10rem);
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.05em;
  line-height: 0.85;
  background: linear-gradient(135deg, #ff0066, #ffcc00, #00ffcc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Bold accent elements */
.maximal-accent {
  border: 3px solid #ff0066;
  padding: 20px 40px;
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  background: transparent;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
}

.maximal-accent:hover {
  background: #ff0066;
  color: #0a0a0a;
  box-shadow: 0 0 40px rgba(255, 0, 102, 0.5);
}
```

**Maximalism principles:**
- Controlled chaos — there's still a system
- Visual rhythm through repetition
- Bold typography as design element
- Color is fearless but coordinated
- Every "extra" serves the brand personality
- Layer textures, patterns, and type intentionally

### When Minimalism Fails

- When it becomes generic (every SaaS looks the same)
- When whitespace wastes screen real estate in tools
- When it sacrifices discoverability for cleanliness
- When "clean" means "no personality"

### When Maximalism Fails

- When it's just clutter without hierarchy
- When readability suffers
- When load times balloon from assets
- When the design overpowers the content

---

## 11. Retro/Vintage Web

### What It Is

Retro web design recreates the aesthetics of early computing (1980s-2000s): pixel art, CRT monitor effects, old-school UI elements (Windows 95/98 borders, Mac OS 9 buttons), lo-fi color palettes, bitmap fonts, and intentionally degraded imagery.

### CSS Patterns

```css
/* CRT Scanline Effect */
.crt {
  position: relative;
  background: #0a0a0a;
}

.crt::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 1px,
    rgba(0, 0, 0, 0.15) 1px,
    rgba(0, 0, 0, 0.15) 2px
  );
  pointer-events: none;
  z-index: 1;
}

/* CRT Flicker */
@keyframes flicker {
  0% { opacity: 0.97; }
  5% { opacity: 0.95; }
  10% { opacity: 0.98; }
  15% { opacity: 0.96; }
  100% { opacity: 0.98; }
}

.crt {
  animation: flicker 0.15s infinite;
}

/* Pixel Font */
.pixel-text {
  font-family: 'Press Start 2P', 'Courier New', monospace;
  font-size: 16px;
  line-height: 2;
  image-rendering: pixelated;
  -webkit-font-smoothing: none;
}

/* Windows 95 Style */
.win95-box {
  background: #c0c0c0;
  border-top: 2px solid #ffffff;
  border-left: 2px solid #ffffff;
  border-bottom: 2px solid #404040;
  border-right: 2px solid #404040;
  padding: 4px;
  font-family: 'MS Sans Serif', 'Segoe UI', sans-serif;
  font-size: 11px;
}

.win95-button {
  background: #c0c0c0;
  border-top: 2px solid #ffffff;
  border-left: 2px solid #ffffff;
  border-bottom: 2px solid #404040;
  border-right: 2px solid #404040;
  padding: 4px 16px;
  font-family: 'MS Sans Serif', 'Segoe UI', sans-serif;
  font-size: 11px;
  cursor: pointer;
}

.win95-button:active {
  border-top: 2px solid #404040;
  border-left: 2px solid #404040;
  border-bottom: 2px solid #ffffff;
  border-right: 2px solid #ffffff;
  padding: 5px 15px 3px 17px;
}

/* Mac OS 9 Style */
.mac-os9-window {
  background: #dddddd;
  border: 1px solid #333333;
  border-radius: 4px;
  box-shadow:
    inset 0 0 0 1px #ffffff,
    2px 2px 8px rgba(0, 0, 0, 0.3);
}

.mac-os9-titlebar {
  background: linear-gradient(180deg, #eeeeee, #cccccc);
  padding: 4px 8px;
  border-bottom: 1px solid #999999;
  display: flex;
  align-items: center;
  gap: 6px;
}

.mac-os9-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.2);
}

.mac-os9-dot--close { background: #ff5f57; }
.mac-os9-dot--minimize { background: #ffbd2e; }
.mac-os9-dot--maximize { background: #28c940; }

/* VHS Distortion */
@keyframes vhs {
  0% { transform: translateX(0); }
  20% { transform: translateX(-2px); }
  40% { transform: translateX(2px); }
  60% { transform: translateX(-1px); }
  80% { transform: translateX(1px); }
  100% { transform: translateX(0); }
}

.vhs-text {
  animation: vhs 0.3s infinite;
  text-shadow: 2px 0 #ff0000, -2px 0 #0000ff;
}

/* Pixel art rendering */
.pixel-art {
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
```

### Color Palette

- DOS/VGA: `#000000`, `#0000aa`, `#00aa00`, `#aa0000`, `#00aaaa`, `#aa00aa`, `#aa5500`, `#aaaaaa`
- Gameboy: `#0f380f`, `#306230`, `#8bac0f`, `#9bbc0f`
- Win95: `#008080` (teal desktop), `#c0c0c0` (silver), `#808080` (gray)
- CRT warm: `#0a1a0a` (dark green tint), `#33ff33` (phosphor green)

### Typography Pairing

- Pixel: Press Start 2P, VT323, Silkscreen
- System: MS Sans Serif, Chicago, Geneva
- Mono: Courier New, IBM Plex Mono

### Famous Examples

- Windows93.net (browser-based Win95 parody)
- Neal.fun (retro-inspired interactive sites)
- Many indie game landing pages
- Geocities.archive sites

---

## 12. Cyberpunk / Neon

### What It Is

Inspired by cyberpunk fiction (Blade Runner, Ghost in the Shell, Neuromancer, Cyberpunk 2077) — dark backgrounds, neon glows, grid lines, scanlines, glitch effects, futuristic typography. It's the aesthetic of high-tech dystopia.

### CSS Patterns

```css
/* Neon Text Glow */
.neon-text {
  color: #fff;
  text-shadow:
    0 0 7px #fff,
    0 0 10px #fff,
    0 0 21px #fff,
    0 0 42px #0fa,
    0 0 82px #0fa,
    0 0 92px #0fa;
  font-family: 'Orbitron', sans-serif;
  font-size: 3rem;
  text-transform: uppercase;
}

/* Neon Box */
.neon-box {
  border: 2px solid #0fa;
  border-radius: 0;
  padding: 24px;
  box-shadow:
    0 0 5px #0fa,
    0 0 10px #0fa,
    inset 0 0 5px #0fa,
    0 0 20px #0fa;
  background: rgba(0, 255, 170, 0.05);
}

/* Grid Background */
.cyber-grid {
  background:
    linear-gradient(rgba(0, 255, 170, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 170, 0.05) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* Perspective Grid */
.perspective-grid {
  background:
    linear-gradient(rgba(0, 255, 170, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 170, 0.1) 1px, transparent 1px);
  background-size: 60px 60px;
  transform: perspective(500px) rotateX(60deg);
  transform-origin: center top;
}

/* Scanlines */
.scanlines::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 1px,
    rgba(0, 0, 0, 0.1) 1px,
    rgba(0, 0, 0, 0.1) 2px
  );
  pointer-events: none;
}

/* Glitch Effect */
@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-3px, 3px); }
  40% { transform: translate(-3px, -3px); }
  60% { transform: translate(3px, 3px); }
  80% { transform: translate(3px, -3px); }
  100% { transform: translate(0); }
}

.glitch-text {
  position: relative;
}

.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
}

.glitch-text::before {
  color: #ff0000;
  animation: glitch 0.3s infinite;
  clip-path: polygon(0 0, 100% 0, 100% 35%, 0 35%);
}

.glitch-text::after {
  color: #00ffff;
  animation: glitch 0.3s infinite reverse;
  clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);
}

/* Neon Button */
.neon-btn {
  background: transparent;
  color: #0fa;
  border: 2px solid #0fa;
  padding: 12px 32px;
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.neon-btn:hover {
  background: rgba(0, 255, 170, 0.1);
  box-shadow:
    0 0 10px #0fa,
    0 0 40px rgba(0, 255, 170, 0.2);
}
```

### When to Use

- Gaming sites, esports teams
- Tech/entertainment brands
- Event pages (hackathons, gaming tournaments)
- Music (electronic, synthwave)
- When the brand IS futuristic/edgy

### When NOT to Use

- Healthcare, finance, government
- Accessibility-first projects (glow effects reduce readability)
- Content-heavy sites (neon distracts)
- When the audience is older/conservative

### Color Palette

- Background: `#0a0a0f` (near-black), `#0d0221` (deep purple)
- Neon green: `#00ffaa` / `#0fa`
- Neon cyan: `#00ffff`
- Neon pink: `#ff00ff` / `#ff2a6d`
- Neon yellow: `#f0f000`
- Grid lines: `rgba(0, 255, 170, 0.05-0.1)`

### Typography Pairing

- Headings: Orbitron, Rajdhani, Exo 2 (futuristic, geometric)
- Body: Share Tech Mono, Source Code Pro
- Accent: Any condensed, uppercase display font

### Famous Examples

- Cyberpunk 2077 official site
- Many esports team sites
- Synthwave music pages
- Hackathon/event sites

---

## 13. Organic / Biomorphic

### What It Is

Organic/biomorphic design uses soft, flowing shapes inspired by nature — blob forms, fluid curves, natural color palettes, and asymmetric compositions. It contrasts with the rigid geometry of traditional UI design. Think amoeba shapes, river stones, leaf veins, cellular structures.

### CSS Patterns

```css
/* Blob Shape — 8-value border-radius */
.blob {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #a8edea, #fed6e3);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

/* Animated blob */
@keyframes morph {
  0%   { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
  25%  { border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%; }
  50%  { border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%; }
  75%  { border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%; }
  100% { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
}

.blob-animated {
  animation: morph 8s ease-in-out infinite;
}

/* Organic Card */
.organic-card {
  background: #faf8f5;
  border-radius: 24px 48px 24px 48px;
  padding: 32px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
}

/* Wavy Section Divider */
.wave-divider {
  position: relative;
  height: 80px;
  overflow: hidden;
}

.wave-divider::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: -5%;
  width: 110%;
  height: 100%;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 80'%3E%3Cpath fill='%23ffffff' d='M0 40 C360 80 720 0 1080 40 C1260 60 1360 50 1440 40 L1440 80 L0 80 Z'/%3E%3C/svg%3E");
  background-size: cover;
}

/* Organic background pattern */
.organic-bg {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(168, 237, 234, 0.3), transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(254, 214, 227, 0.3), transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(221, 214, 254, 0.3), transparent 50%),
    #faf8f5;
}

/* Leaf/nature-inspired texture */
.leaf-pattern {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M30 5 Q40 15 35 30 Q30 45 20 35 Q10 25 20 15 Z' fill='none' stroke='rgba(0,100,50,0.05)' stroke-width='1'/%3E%3C/svg%3E");
}

/* Smooth curved section */
.organic-section {
  background: #f0faf8;
  border-radius: 0 0 50% 50% / 0 0 100px 100px;
  padding: 80px 20px 160px;
}
```

### When to Use

- Health, wellness, mental health apps
- Nature/environmental brands
- Organic food, sustainable products
- Meditation/yoga apps
- Children's education (friendly shapes)
- Biotech, pharmaceutical (approachable)

### When NOT to Use

- Fintech, banking (needs sharpness and trust)
- Developer tools (users expect precision)
- Data-heavy dashboards
- When the audience expects corporate formality

### Color Palette

- Soft greens: `#a8edea`, `#e8f8f5`
- Soft pinks: `#fed6e3`, `#fce4ec`
- Lavenders: `#ddd6fe`, `#f3f0ff`
- Warm neutrals: `#faf8f5`, `#f5f0eb`
- Accent: `#2d6a4f` (deep green), `#7c3aed` (purple)

### Typography Pairing

- Headings: Nunito, Quicksand, Comfortaa (rounded, organic)
- Body: Nunito Sans, DM Sans (clean but friendly)
- Avoid: sharp geometric fonts (clash with organic shapes)

### Famous Examples

- Headspace (organic illustrations + shapes)
- Calm (nature-inspired UI)
- Many wellness/health apps
- Sustainable brand sites

---

## 14. Swiss / International Typographic Style

### History

Born in Switzerland in the 1950s-60s (also called "Swiss Style" or "International Typographic Style"). Pioneered by Josef Muller-Brockmann, Armin Hofmann, Max Bill, and others at the Basel and Zurich schools of design. It's the foundation of modern corporate and editorial design.

### Key Principles

1. **Grid systems** — mathematical, systematic layout
2. **Objective photography** — not illustration
3. **Sans-serif typography** — Helvetica, Univers, Akzidenz-Grotesk
4. **Flush-left, ragged-right** text alignment (not justified)
5. **Asymmetric layouts** — dynamic, not centered symmetry
6. **Mathematical proportions** — golden ratio, rule of thirds
7. **Content-driven hierarchy** — size, weight, position
8. **Minimal decoration** — function over form
9. **White space as design element** — deliberate, not leftover

### When to Use

- Corporate identity, brand guidelines
- Editorial design, magazines, newspapers
- Data-heavy presentations
- Government/institutional communications
- Architecture, design, art portfolios
- When credibility and objectivity matter

### CSS Implementation

```css
/* Swiss Grid System */
.swiss-layout {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 48px;
}

/* Mathematical spacing */
:root {
  --swiss-unit: 8px;
  --swiss-gutter: 24px;
  --swiss-margin: 48px;
}

/* Typography scale (1:1.333 — perfect fourth) */
:root {
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 1rem;       /* 16px */
  --text-md: 1.333rem;   /* 21px */
  --text-lg: 1.777rem;   /* 28px */
  --text-xl: 2.369rem;   /* 38px */
  --text-2xl: 3.157rem;  /* 50px */
}

.swiss-heading {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin-bottom: calc(var(--swiss-unit) * 3);
}

.swiss-body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-weight: 400;
  font-size: var(--text-sm);
  line-height: 1.6;
  max-width: 65ch;
  text-align: left;
}

/* Flush-left alignment */
.swiss-text {
  text-align: left;
  /* NEVER justify in Swiss style */
}

/* Minimal horizontal rules */
.swiss-rule {
  border: none;
  border-top: 1px solid #000;
  margin: calc(var(--swiss-unit) * 4) 0;
}

/* Grid-based poster layout */
.swiss-poster {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(8, 1fr);
  aspect-ratio: 2/3;
  gap: 0;
  background: #fff;
  color: #000;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.swiss-poster__title {
  grid-column: 1 / 5;
  grid-row: 1 / 3;
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 900;
  letter-spacing: -0.03em;
  line-height: 0.95;
  align-self: end;
  padding: 24px;
}

.swiss-poster__image {
  grid-column: 1 / 7;
  grid-row: 3 / 7;
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.swiss-poster__info {
  grid-column: 5 / 7;
  grid-row: 1 / 3;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 24px;
  align-self: end;
}
```

### Color Palette

- Primary: Black `#000000`, White `#ffffff`
- Accent: ONE bold color (red `#ff0000`, blue `#0055ff`)
- No gradients, no tints
- Maximum 3 colors total

### Typography Pairing

- Display: Helvetica Neue, Univers, Akzidenz-Grotesk
- Body: Same family, lighter weight
- Modern alternatives: Inter, IBM Plex Sans, Libre Franklin
- Never use decorative or script fonts

### Famous Examples

- Josef Muller-Brockmann's concert posters
- IBM design system
- New York Times (editorial grid)
- Swiss International Air Lines
- Many government/institutional sites

---

## 15. Japanese / Zen Aesthetic

### Core Concepts

- **Ma** (間) — negative space as a design element, not emptiness
- **Wabi-sabi** — beauty in imperfection and transience
- **Kanso** (簡素) — simplicity and elimination of clutter
- **Shibui** — subtle, unobtrusive beauty
- **Asymmetry** — balanced but not symmetrical (inspired by nature)
- **Nature elements** — subtle references to natural materials and seasons

### When to Use

- Luxury brands (especially Japanese or East Asian)
- Wellness, meditation, spa
- High-end hospitality
- Art galleries, museums
- Tea, sake, fine dining
- When the brand values subtlety and restraint

### CSS Implementation

```css
/* Ma — Generous negative space */
.zen-layout {
  max-width: 960px;
  margin: 0 auto;
  padding: 120px 48px;  /* generous breathing room */
}

.zen-section {
  margin-bottom: 160px;  /* sections breathe */
}

/* Asymmetric grid */
.zen-grid {
  display: grid;
  grid-template-columns: 1fr 1.618fr;  /* golden ratio */
  gap: 64px;
  align-items: center;
}

/* Vertical text (Japanese calligraphy feel) */
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  letter-spacing: 0.1em;
  line-height: 2;
}

/* Minimal typography */
.zen-heading {
  font-family: 'Noto Serif JP', 'Georgia', serif;
  font-weight: 400;  /* light, not bold */
  font-size: 2.5rem;
  letter-spacing: 0.1em;
  line-height: 1.4;
  color: #1a1a1a;
}

.zen-text {
  font-family: 'Noto Sans JP', 'Helvetica Neue', sans-serif;
  font-weight: 300;
  font-size: 1rem;
  line-height: 2;
  color: #666;
  max-width: 40ch;
}

/* Subtle ink wash / watercolor effect */
.ink-wash {
  background:
    radial-gradient(ellipse at 30% 50%, rgba(0, 0, 0, 0.03), transparent 60%),
    radial-gradient(ellipse at 70% 30%, rgba(0, 0, 0, 0.02), transparent 50%);
  background-color: #faf9f6;
}

/* Enso circle (zen calligraphy) */
.enso {
  width: 200px;
  height: 200px;
  border: 3px solid #1a1a1a;
  border-radius: 50%;
  /* Intentionally imperfect — gap in the circle */
  border-right-color: transparent;
  transform: rotate(-15deg);
}

/* Nature-inspired separator */
.zen-separator {
  width: 60px;
  height: 1px;
  background: #1a1a1a;
  margin: 48px 0;
}

/* Stone texture background */
.stone-bg {
  background-color: #f5f3f0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
}

/* Subtle hover — gentle, not jarring */
.zen-link {
  color: #1a1a1a;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.4s ease;
}

.zen-link:hover {
  border-bottom-color: #1a1a1a;
}

/* Scroll-based reveal (subtle) */
.zen-reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.zen-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Color Palette

- Background: `#faf9f6` (warm white), `#f5f3f0` (stone)
- Text: `#1a1a1a` (warm black, not pure black)
- Secondary text: `#666666`, `#999999`
- Accent: `#8b7355` (earth brown), `#5a6e5a` (moss green), `#c45c4a` (terracotta)
- Nature: `#d4c5b0` (sand), `#7a8b7a` (sage)

### Typography Pairing

- Headings: Noto Serif JP, Cormorant Garamond, Playfair Display (serif, refined)
- Body: Noto Sans JP, Inter, DM Sans (light weight, airy)
- Japanese text: Noto Serif JP for headings, Noto Sans JP for body
- Line-height: 1.8-2.0 (more airy than Western conventions)

### Famous Examples

- Muji (brand and website)
- Japanese Garden websites
- Many onsen/ryokan sites
- Issey Miyake
- Some Samsung Japan designs

---

## Style Selection Guide

| Context | Recommended Style(s) |
|---------|----------------------|
| SaaS Product | Minimalism, Aurora UI, Bento Grid |
| SaaS Landing | Aurora UI, Glassmorphism (selective), Bento Grid |
| Creative Agency | Brutalism, Memphis, Maximalism |
| Children's App | Claymorphism, Memphis |
| Gaming | Cyberpunk, Retro, Brutalism |
| Health/Wellness | Organic, Japanese/Zen |
| Music/Audio | Skeuomorphism, Cyberpunk |
| Fashion/Luxury | Maximalism, Japanese/Zen, Brutalism |
| Corporate/Enterprise | Swiss, Minimalism |
| Dark Mode App | Dark Mode Design + any style adapted |
| Portfolio | Brutalism, Swiss, Minimalism |
| Data Dashboard | Swiss, Minimalism, Dark Mode |
| Retro Brand | Retro/Vintage, Memphis |
| Nature/Sustainability | Organic, Japanese/Zen |
| Tech/Dev Tools | Aurora UI, Swiss, Minimalism |

---

## Combining Styles

Styles can be mixed intentionally:

- **Dark Mode + Aurora UI** = most modern SaaS landing pages (2024-2026)
- **Minimalism + Bento Grid** = Apple-style product pages
- **Swiss + Organic** = editorial design with warmth
- **Dark Mode + Cyberpunk** = gaming/entertainment
- **Japanese/Zen + Minimalism** = luxury brands
- **Skeuomorphism + Dark Mode** = music production apps

**Rules for combining:**
1. Pick ONE dominant style, ONE accent style
2. The dominant style sets layout and structure
3. The accent style adds personality (color, texture, shape)
4. Never combine two strong visual styles (e.g., Cyberpunk + Memphis = chaos)
5. When in doubt, go simpler

---

## Anti-Patterns Across All Styles

1. **Style without purpose** — choosing a style because it looks cool, not because it serves the user
2. **Trend-chasing** — every SaaS doing Aurora UI in 2025 because Vercel did it
3. **Accessibility sacrifice** — glassmorphism that fails contrast, neumorphism that's invisible
4. **Inconsistency** — mixing styles without intent
5. **Over-decoration** — style elements that compete with content
6. **Performance ignore** — blur, shadows, gradients that tank FPS
7. **Mobile ignore** — styles that only work on desktop
8. **Content mismatch** — brutalism for a medical app, claymorphism for a bank
