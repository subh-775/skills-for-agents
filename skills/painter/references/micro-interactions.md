# Micro-Interactions Skill Reference

## 1. Button Micro-Interactions

### Hover: Scale + Glow
```css
.btn { transition: transform 0.15s ease-out, box-shadow 0.2s ease; }
.btn:hover { transform: scale(1.03); box-shadow: 0 4px 15px rgba(59,130,246,0.4); }
.btn:active { transform: scale(0.97); }
```

### Hover: Background Fill Wipe
```css
.btn-fill { position: relative; overflow: hidden; z-index: 1; transition: color 0.3s ease; }
.btn-fill::before {
  content: ''; position: absolute; inset: 0; background: currentColor;
  transform: scaleX(0); transform-origin: left; transition: transform 0.3s ease; z-index: -1;
}
.btn-fill:hover::before { transform: scaleX(1); }
.btn-fill:hover { color: white; }
```

### Hover: Underline Reveal
```css
.link { position: relative; }
.link::after {
  content: ''; position: absolute; bottom: -2px; left: 0; width: 100%; height: 2px;
  background: currentColor; transform: scaleX(0); transform-origin: right; transition: transform 0.3s ease;
}
.link:hover::after { transform: scaleX(1); transform-origin: left; }
```

### Click: Ripple (JS-based, origin from click point)
```javascript
function createRipple(e) {
  const btn = e.currentTarget, circle = document.createElement("span");
  const d = Math.max(btn.clientWidth, btn.clientHeight), r = d / 2, rect = btn.getBoundingClientRect();
  Object.assign(circle.style, { width: `${d}px`, height: `${d}px`,
    left: `${e.clientX - rect.left - r}px`, top: `${e.clientY - rect.top - r}px` });
  circle.classList.add("ripple-span");
  btn.querySelector(".ripple-span")?.remove();
  btn.appendChild(circle);
}
```
```css
.ripple-span {
  position: absolute; border-radius: 50%; background: rgba(255,255,255,0.3);
  transform: scale(0); animation: ripple 0.6s linear; pointer-events: none;
}
@keyframes ripple { to { transform: scale(4); opacity: 0; } }
```

### Loading / Success / Error State Machine
```javascript
async function handleSubmit(btn) {
  btn.classList.add('loading'); btn.disabled = true;
  try {
    await submitForm();
    btn.classList.remove('loading'); btn.classList.add('success');
    setTimeout(() => { btn.classList.remove('success'); btn.disabled = false; }, 2000);
  } catch {
    btn.classList.remove('loading'); btn.classList.add('error');
    setTimeout(() => { btn.classList.remove('error'); btn.disabled = false; }, 2000);
  }
}
```
```css
.spinner { width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.checkmark { stroke: #22c55e; stroke-width: 2; fill: none;
  stroke-dasharray: 48; stroke-dashoffset: 48; }
.success .checkmark { animation: draw-check 0.4s ease forwards 0.1s; }
@keyframes draw-check { to { stroke-dashoffset: 0; } }

.error { animation: shake 0.4s ease; }
@keyframes shake {
  0%,100% { transform: translateX(0); }
  20% { transform: translateX(-6px); } 40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); } 80% { transform: translateX(4px); }
}
```

---

## 2. Form Micro-Interactions

### Floating Label (CSS-only)
```css
.form-group { position: relative; margin-bottom: 1.5rem; }
.form-input {
  width: 100%; padding: 12px 0; border: none; border-bottom: 2px solid #e2e8f0;
  background: transparent; font-size: 16px; outline: none; transition: border-color 0.3s ease;
}
.form-input:focus { border-bottom-color: #3b82f6; }
.form-label {
  position: absolute; left: 0; top: 12px; font-size: 16px; color: #94a3b8;
  pointer-events: none; transition: all 0.2s ease;
}
.form-input:focus + .form-label,
.form-input:not(:placeholder-shown) + .form-label {
  top: -8px; font-size: 12px; color: #3b82f6;
}
```

### Focus Ring Animation
```css
.form-input { outline: none; box-shadow: 0 0 0 0 rgba(59,130,246,0); transition: box-shadow 0.2s ease; }
.form-input:focus { box-shadow: 0 0 0 3px rgba(59,130,246,0.2); }
```

### Inline Validation (debounced)
```javascript
let timeout;
input.addEventListener('input', () => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
    indicator.className = input.value === '' ? 'neutral' : valid ? 'valid' : 'invalid';
  }, 300);
});
```

### Error Slide-in
```css
.error-msg {
  max-height: 0; overflow: hidden; opacity: 0; transform: translateY(-4px);
  transition: all 0.3s ease; color: #ef4444; font-size: 0.875rem; margin-top: 4px;
}
.error-msg.visible { max-height: 40px; opacity: 1; transform: translateY(0); }
```
Accessibility: use `aria-live="polite"` on error container, `aria-describedby` on input.

---

## 3. Navigation Micro-Interactions

### Sliding Pill Indicator
```css
.tab-nav { position: relative; display: flex; border-bottom: 1px solid #e2e8f0; }
.tab { padding: 12px 24px; background: none; border: none; cursor: pointer;
  font-size: 14px; color: #64748b; transition: color 0.3s ease; }
.tab.active { color: #3b82f6; }
.tab-indicator {
  position: absolute; bottom: -1px; height: 2px; background: #3b82f6;
  transition: left 0.3s ease, width 0.3s ease; border-radius: 1px;
}
```
```javascript
function moveIndicator(tab) {
  indicator.style.left = `${tab.offsetLeft}px`;
  indicator.style.width = `${tab.offsetWidth}px`;
}
tabs.forEach(t => t.addEventListener('click', () => {
  tabs.forEach(x => { x.classList.remove('active'); x.setAttribute('aria-selected', 'false'); });
  t.classList.add('active'); t.setAttribute('aria-selected', 'true'); moveIndicator(t);
}));
```

### Hamburger to X Morph
```css
.hamburger { width: 24px; height: 18px; position: relative; cursor: pointer; background: none; border: none; }
.hamburger span { display: block; position: absolute; width: 100%; height: 2px;
  background: currentColor; left: 0; transition: all 0.3s ease; }
.hamburger span:nth-child(1) { top: 0; }
.hamburger span:nth-child(2) { top: 8px; }
.hamburger span:nth-child(3) { top: 16px; }
.hamburger.open span:nth-child(1) { top: 8px; transform: rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; transform: translateX(-10px); }
.hamburger.open span:nth-child(3) { top: 8px; transform: rotate(-45deg); }
```

### Dropdown: Slide + Fade
```css
.dropdown {
  opacity: 0; transform: translateY(-8px) scale(0.95); transform-origin: top left;
  pointer-events: none; transition: opacity 0.2s ease, transform 0.2s ease;
}
.dropdown.open { opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; }
```

---

## 4. Scroll Micro-Interactions

### Scroll Progress Bar
```javascript
const bar = document.querySelector('.scroll-progress');
window.addEventListener('scroll', () => {
  const pct = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
  bar.style.width = `${pct}%`;
}, { passive: true });
```
```css
.scroll-progress { position: fixed; top: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6); width: 0%; z-index: 9999; }
```

### Sticky Header Shrink (IntersectionObserver)
```javascript
const observer = new IntersectionObserver(([e]) => {
  header.classList.toggle('scrolled', !e.isIntersecting);
}, { threshold: 0, rootMargin: '-1px 0px 0px 0px' });
observer.observe(document.getElementById('sentinel'));
```
```css
.header { position: sticky; top: 0; padding: 20px 0; transition: padding 0.3s ease, box-shadow 0.3s ease; }
.header.scrolled { padding: 10px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
```

### Scroll-Triggered Reveal
```css
.reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.6s ease, transform 0.6s ease; }
.reveal.revealed { opacity: 1; transform: translateY(0); }
```
```javascript
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('revealed'); revealObs.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));
```

### Back-to-Top Button
```css
.back-to-top { position: fixed; bottom: 24px; right: 24px; opacity: 0;
  transform: translateY(10px); pointer-events: none; transition: opacity 0.3s ease, transform 0.3s ease; }
.back-to-top.visible { opacity: 1; transform: translateY(0); pointer-events: auto; }
```

---

## 5. Data Micro-Interactions

### Number Counter (animate 0 to target)
```javascript
function animateCounter(el, target, duration = 2000) {
  const start = performance.now();
  function update(now) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3); // ease-out cubic
    el.textContent = Math.floor(target * eased).toLocaleString();
    if (p < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
// Trigger on scroll into view via IntersectionObserver
```

### Card Hover: Lift + Shadow
```css
.card { transition: transform 0.3s ease, box-shadow 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.card:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.15); }
```

### Card Hover: 3D Tilt
```javascript
card.addEventListener('mousemove', (e) => {
  const r = card.getBoundingClientRect();
  const rx = ((e.clientY - r.top) / r.height - 0.5) * -8;
  const ry = ((e.clientX - r.left) / r.width - 0.5) * 8;
  card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg)`;
});
card.addEventListener('mouseleave', () => { card.style.transform = ''; });
```

### Skeleton Loading
```css
.skeleton {
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 37%, #e2e8f0 63%);
  background-size: 200% 100%; animation: shimmer 1.5s ease-in-out infinite; border-radius: 4px;
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
.content-loaded { animation: fade-in 0.3s ease; }
@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
```

---

## 6. Timing Standards

| Category | Duration | Use Cases |
|----------|----------|-----------|
| Instant | <100ms | Hover, focus rings, pressed states |
| Quick | 100-200ms | Color changes, opacity shifts |
| Standard | 200-300ms | Dropdowns, panels, toggles, tabs |
| Complex | 300-500ms | Modals, page sections, reveals |
| Dramatic | 500-1000ms | Hero animations, scroll-linked, first-load |

### Easing Functions
```css
:root {
  --ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);      /* Entering -- fast start, slow end */
  --ease-in: cubic-bezier(0.4, 0.0, 1, 1);          /* Exiting -- slow start, fast end */
  --ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);    /* Moving -- smooth both ends */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* Playful -- overshoots, settles */
}
```

### Duration Tokens
```css
:root {
  --dur-instant: 0.1s; --dur-quick: 0.15s; --dur-standard: 0.25s;
  --dur-complex: 0.4s; --dur-dramatic: 0.7s;
}
```

---

## 7. Performance & Accessibility

### Golden Rules
- Only animate `transform` and `opacity` when possible (compositor-only, zero layout/paint cost)
- `will-change` sparingly -- creates compositor layers, costs memory
- `box-shadow` triggers paint but not layout -- acceptable for hover, avoid on scroll
- `width/height/top/left` trigger layout -- avoid animating these

### prefers-reduced-motion (mandatory)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Performance Cheat Sheet
| Property | Layout | Paint | Composite | Cost |
|----------|--------|-------|-----------|------|
| transform | No | No | Yes | Lowest |
| opacity | No | No | Yes | Lowest |
| color | No | Yes | No | Low |
| box-shadow | No | Yes | No | Low |
| width/height | Yes | Yes | Yes | High |
| top/left | Yes | Yes | Yes | High |
| filter | No | Yes | Yes | Medium |
