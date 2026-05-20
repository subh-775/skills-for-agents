# Niche & Advanced CSS/JS Patterns

Cutting-edge patterns that create distinctive, premium experiences. Most designers don't know these.

---

## CSS Scroll-Driven Animations

Native browser feature — zero JavaScript.

```css
/* Scroll-linked progress bar */
.progress {
  animation: grow linear;
  animation-timeline: scroll();
}
@keyframes grow {
  from { scaleX: 0; }
  to { scaleX: 1; }
}

/* Reveal on scroll */
.reveal {
  animation: fade-in linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
@keyframes fade-in {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}
```

Feature detect: `@supports (animation-timeline: scroll()) { ... }`

---

## View Transitions API

Browser-native page transitions.

```js
// SPA transitions
document.startViewTransition(() => {
  updateContent()
})
```

```css
::view-transition-old(root) {
  animation: fade-out 0.3s ease-out;
}
::view-transition-new(root) {
  animation: fade-in 0.3s ease-in;
}

/* Named transitions for specific elements */
.hero-image {
  view-transition-name: hero;
}
```

MPA support: `@view-transition { navigation: auto; }`

---

## CSS `@starting-style`

Entry animations without JavaScript.

```css
dialog {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.3s, transform 0.3s;
}

@starting-style {
  dialog {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

Works with `dialog`, `popover`, and dynamically inserted elements.

---

## CSS Anchor Positioning

Position elements relative to other elements — no JS.

```css
.anchor {
  anchor-name: --my-anchor;
}

.tooltip {
  position: fixed;
  position-anchor: --my-anchor;
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 8px;
}

/* Fallback positions */
@position-try --flip-top {
  bottom: anchor(top);
  top: auto;
}
```

Tooltip, dropdown, popover positioning without JavaScript.

---

## CSS Container Queries

Component-level responsive design.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { display: flex; gap: 1rem; }
}

@container card (max-width: 399px) {
  .card { display: block; }
}
```

Container query units: `cqi` (inline), `cqb` (block), `cqmin`, `cqmax`.

---

## CSS `has()` Selector

Parent selection based on children.

```css
/* Card with image gets different layout */
.card:has(img) { display: grid; grid-template-columns: 200px 1fr; }
.card:not(:has(img)) { display: block; }

/* Form group with error */
.form-group:has(.error) { border-color: red; }

/* Nav with active item */
nav:has(.active) { background: var(--primary); }

/* Hide placeholder when input has value */
input:has(+ label:not(:empty)) { padding-top: 1.5rem; }
```

---

## CSS `color-mix()` and Relative Colors

Create shades/tints from a single base color.

```css
/* Mix with white for lighter variant */
.btn-hover {
  background: color-mix(in oklch, var(--primary) 85%, white);
}

/* Opacity variant */
.btn-transparent {
  background: color-mix(in oklch, var(--primary) 20%, transparent);
}

/* Relative color syntax */
.btn-dark {
  background: oklch(from var(--primary) calc(l - 0.1) c h);
}
```

---

## CSS Layers (`@layer`)

Manage cascade order.

```css
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; box-sizing: border-box; }
}

@layer components {
  .btn { padding: 0.5rem 1rem; }
}

@layer utilities {
  .hidden { display: none; }
}
```

Non-layered always beats layered. Later layers beat earlier. `!important` reverses order.

---

## Fluid Typography

```css
/* Fluid type scale using clamp */
h1 { font-size: clamp(2rem, 1.5rem + 2.5vw, 4rem); }
h2 { font-size: clamp(1.5rem, 1.25rem + 1.5vw, 2.5rem); }
body { font-size: clamp(1rem, 0.9rem + 0.5vw, 1.125rem); }
```

Generate at utopia.fyi.

---

## CSS Grid Subgrid

Align nested grid items to parent grid.

```css
.parent {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
}

.child {
  display: grid;
  grid-template-columns: subgrid; /* inherits parent's columns */
  grid-column: span 3;
}
```

---

## `text-wrap: balance` and `text-wrap: pretty`

```css
h1, h2, h3 { text-wrap: balance; } /* balanced line lengths */
p { text-wrap: pretty; } /* avoid orphans */
```

---

## GSAP ScrollTrigger (Advanced)

```js
// Pin section while scrolling
gsap.to(".panel", {
  scrollTrigger: {
    trigger: ".panel",
    pin: true,
    end: "+=500%",
    scrub: 1,
  },
})

// Horizontal scroll
gsap.to(".horizontal", {
  x: () => -(document.querySelector(".horizontal").scrollWidth - window.innerWidth),
  scrollTrigger: {
    trigger: ".horizontal",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".horizontal").scrollWidth,
  },
})

// Snap to sections
ScrollTrigger.create({
  trigger: ".section",
  snap: 1 / 3,
})
```

---

## Magnetic Elements

```js
// Magnetic button
button.addEventListener('mousemove', (e) => {
  const rect = button.getBoundingClientRect()
  const x = e.clientX - rect.left - rect.width / 2
  const y = e.clientY - rect.top - rect.height / 2
  button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`
})
button.addEventListener('mouseleave', () => {
  button.style.transform = 'translate(0, 0)'
})
```

---

## 3D Tilt on Hover

```js
card.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect()
  const x = (e.clientX - rect.left) / rect.width - 0.5
  const y = (e.clientY - rect.top) / rect.height - 0.5
  card.style.transform = `perspective(1000px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`
})
card.addEventListener('mouseleave', () => {
  card.style.transform = 'perspective(1000px) rotateY(0) rotateX(0)'
})
```

---

## Text Scramble Effect

```js
function scramble(el, finalText, duration = 1000) {
  const chars = '!@#$%^&*()_+{}|:<>?'
  let frame = 0
  const interval = setInterval(() => {
    el.textContent = finalText.split('').map((char, i) => {
      if (i < frame) return finalText[i]
      return chars[Math.floor(Math.random() * chars.length)]
    }).join('')
    frame++
    if (frame > finalText.length) clearInterval(interval)
  }, duration / finalText.length)
}
```

---

## Glitch Text Effect

```css
.glitch {
  position: relative;
}
.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  left: 0;
  top: 0;
}
.glitch::before {
  animation: glitch-1 2s infinite;
  color: #ff0000;
  clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
}
.glitch::after {
  animation: glitch-2 2s infinite;
  color: #0000ff;
  clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
}
@keyframes glitch-1 {
  0%, 90% { transform: translate(0); }
  92% { transform: translate(-2px, 1px); }
  94% { transform: translate(2px, -1px); }
  96% { transform: translate(-1px, 2px); }
}
```

---

## Infinite Marquee

```css
.marquee { overflow: hidden; white-space: nowrap; }
.marquee-content {
  display: inline-block;
  animation: marquee 20s linear infinite;
}
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

Duplicate content for seamless loop.

---

## Noise/Grain Overlay

```css
.grain::after {
  content: "";
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.65'/></filter><rect width='100%' height='100%' filter='url(#n)' opacity='0.05'/></svg>");
  pointer-events: none;
  z-index: 9999;
}
```

---

## CSS `overscroll-behavior`

Prevent scroll chaining (e.g., modal body scroll shouldn't scroll page behind).

```css
.modal-body {
  overscroll-behavior: contain;
}
```

---

## WebGPU Post-Processing (Three.js)

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js'

const composer = new EffectComposer(renderer)
composer.addPass(new RenderPass(scene, camera))
composer.addPass(new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
))
// In render loop: composer.render() instead of renderer.render()
```

---

## Tools & Resources

| Need | Tool |
|------|------|
| CSS patterns | Pattern.css, heropatterns.com |
| SVG backgrounds | haikei.app, svgbackgrounds.com |
| Mesh gradients | meshgradient.in, csshero.org/mesher |
| Noise textures | noisetexturegenerator.com |
| Fluid type | utopia.fyi |
| Color palettes | coolors.co, realtimecolors.com |
| Contrast check | webaim.org/resources/contrastchecker |
| Scroll animations | GSAP ScrollTrigger, Motion One |
| Smooth scroll | Lenis (lenis.darkroom.engineering) |
| 3D web | Three.js, react-three-fiber |
| Pre-built WebGL | Vanta.js |
