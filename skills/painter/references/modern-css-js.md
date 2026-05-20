# Modern UI/UX Technical Reference
## Scrollable Animations, Three.js, GSAP, and Cutting-Edge CSS

> Compiled 2026-05-20 from official documentation (MDN, Three.js, GSAP) and authoritative web sources.

---

## 1. Scrollable Animated Hero Sections

### 1.1 Scroll-Linked vs Scroll-Triggered Animations

These are fundamentally different concepts:

**Scroll-triggered animations** fire once when an element enters the viewport (using Intersection Observer). The animation runs on its own timeline after being triggered. Scrolling back does not reverse the animation.

**Scroll-linked animations** are directly coupled to scroll position. The animation progress (0% to 100%) maps 1:1 to scroll progress. Scrolling backward reverses the animation. This is what creates parallax and scrub effects.

```javascript
// Scroll-TRIGGERED (fires once, plays independently)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, { threshold: 0.1 });

// Scroll-LINKED (progress tied to scroll position)
// CSS approach:
.element {
  animation: slideIn linear;
  animation-timeline: scroll();  // progress = scroll progress
}
```

### 1.2 Technologies Used

| Technology | Type | Best For |
|-----------|------|----------|
| **GSAP ScrollTrigger** | JS library | Complex pinned scenes, scrub animations, cross-browser parallax |
| **CSS scroll-driven animations** | Native CSS | Simple parallax, progress bars, fade-in on scroll (Chromium 115+, Firefox 110+) |
| **Framer Motion** | React library | React component animations, layout animations, gesture-driven |
| **Intersection Observer** | Browser API | Trigger-class toggling, lazy loading, simple reveal animations |
| **Lenis + GSAP** | Smooth scroll | Butter-smooth scroll + GSAP-powered animations |

### 1.3 Typical Hero Section Architecture

The standard pattern for award-winning hero sections:

```
[Sticky Container]           <- position: sticky; top: 0;
  [Scroll Progress Driver]   <- height: 300vh (creates scroll distance)
    [Fixed Viewport]         <- height: 100vh, overflow: hidden
      [Animated Layer 1]     <- background parallax (slow)
      [Animated Layer 2]     <- midground elements
      [Animated Layer 3]     <- foreground text (fast)
```

**Key insight:** You create a tall container (300vh+) to generate scroll distance, then pin the visible viewport so elements inside can animate based on scroll progress.

### 1.4 GSAP ScrollTrigger Hero Implementation

```html
<div class="hero-wrapper">   <!-- This gets pinned -->
  <div class="hero-content">
    <h1 class="hero-title">Title</h1>
    <p class="hero-subtitle">Subtitle</p>
    <img class="hero-image" src="product.png" />
  </div>
</div>
<!-- Enough content below to allow scrolling -->
<div class="spacer" style="height: 200vh;"></div>
```

```javascript
gsap.registerPlugin(ScrollTrigger);

// Pin the hero and scrub animations
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".hero-wrapper",
    start: "top top",        // when top of trigger hits top of viewport
    end: "+=150%",           // pin for 150% of viewport height
    pin: true,               // pin the trigger element
    scrub: 1,                // smooth scrubbing (1s catch-up)
    snap: {
      snapTo: "labels",      // snap to timeline labels
      duration: { min: 0.2, max: 0.5 },
      ease: "power1.inOut"
    }
  }
});

// Staggered text reveal
tl.from(".hero-title", {
  y: 100,
  opacity: 0,
  duration: 1
})
.from(".hero-subtitle", {
  y: 50,
  opacity: 0,
  duration: 0.8
}, "-=0.5")  // overlap by 0.5s
.to(".hero-image", {
  scale: 1.1,
  y: -50,
  duration: 2
}, 0);  // start at beginning of timeline
```

### 1.5 CSS Scroll-Driven Animations Hero

```css
.hero-wrapper {
  height: 300vh;  /* scroll distance */
  position: relative;
}

.hero-content {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}

.hero-title {
  animation: titleReveal linear both;
  animation-timeline: scroll();
  animation-range: 0% 50%;
}

.hero-image {
  animation: imageParallax linear both;
  animation-timeline: scroll();
  animation-range: 0% 100%;
}

@keyframes titleReveal {
  from {
    opacity: 0;
    transform: translateY(100px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes imageParallax {
  from {
    transform: translateY(0) scale(1);
  }
  to {
    transform: translateY(-100px) scale(1.1);
  }
}

/* Feature detection */
@supports not (animation-timeline: scroll()) {
  .hero-title {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

### 1.6 How Apple, Stripe, Vercel Build Their Heroes

**Apple.com** uses a combination of:
- GSAP ScrollTrigger for pinned scroll-jacking scenes
- Canvas/WebGL for 3D product reveals (iPhone, Mac)
- Intersection Observer for section entry animations
- Custom scroll-snapping between sections
- Large scroll distances (300-500vh) with pinned viewports

**Stripe.com** uses:
- GSAP for gradient mesh animations and element staggering
- Canvas-based animated gradient backgrounds (WebGL shaders)
- CSS transitions for hover states
- Intersection Observer for section reveals
- Smooth scroll (Lenis or custom)

**Vercel.com** uses:
- Framer Motion (React-based)
- Three.js for 3D globe and particle effects
- CSS animations for simpler transitions
- Intersection Observer for scroll-triggered reveals

### 1.7 Parallax Technical Implementation

Parallax creates depth illusion by moving layers at different speeds:

```javascript
// GSAP parallax layers
gsap.to(".bg-layer", {
  yPercent: -30,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero",
    start: "top bottom",
    end: "bottom top",
    scrub: true  // true = instant scrub, no catch-up
  }
});

gsap.to(".mid-layer", {
  yPercent: -15,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});

gsap.to(".fg-layer", {
  yPercent: -5,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

```css
/* Pure CSS parallax */
.parallax-container {
  perspective: 1px;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
}

.parallax-layer {
  position: absolute;
  inset: 0;
}

.parallax-layer--back {
  transform: translateZ(-2px) scale(3);
}

.parallax-layer--mid {
  transform: translateZ(-1px) scale(2);
}

.parallax-layer--front {
  transform: translateZ(0);
}
```

---

## 2. Three.js in Modern Websites

### 2.1 Core Architecture

Three.js requires three fundamental objects:

```javascript
// 1. Renderer - draws to canvas
const renderer = new THREE.WebGLRenderer({ antialias: true, canvas });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// 2. Camera - defines what's visible
const camera = new THREE.PerspectiveCamera(
  75,                                      // FOV (degrees)
  window.innerWidth / window.innerHeight,  // aspect
  0.1,                                     // near
  1000                                     // far
);
camera.position.z = 5;

// 3. Scene - container for everything
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000011);

// 4. Geometry + Material = Mesh
const geometry = new THREE.SphereGeometry(1, 64, 64);
const material = new THREE.MeshStandardMaterial({
  color: 0x4488ff,
  roughness: 0.3,
  metalness: 0.7
});
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// 5. Lights
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// 6. Animation loop
function animate(time) {
  requestAnimationFrame(animate);
  mesh.rotation.y = time * 0.001;
  renderer.render(scene, camera);
}
animate();
```

### 2.2 Common Patterns for Websites

**Particle Background:**
```javascript
const count = 5000;
const positions = new Float32Array(count * 3);

for (let i = 0; i < count * 3; i++) {
  positions[i] = (Math.random() - 0.5) * 10;
}

const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

const material = new THREE.PointsMaterial({
  size: 0.02,
  color: 0xffffff,
  transparent: true,
  blending: THREE.AdditiveBlending
});

const particles = new THREE.Points(geometry, material);
scene.add(particles);

// Animate
function animate() {
  particles.rotation.y += 0.0005;
  particles.rotation.x += 0.0002;
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

**Interactive Globe:**
```javascript
// Sphere with custom shader for globe effect
const globeGeometry = new THREE.SphereGeometry(2, 64, 64);
const globeMaterial = new THREE.ShaderMaterial({
  vertexShader: `
    varying vec3 vNormal;
    varying vec2 vUv;
    void main() {
      vNormal = normalize(normalMatrix * normal);
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec3 vNormal;
    varying vec2 vUv;
    uniform float uTime;

    // Simple noise for land masses
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }

    void main() {
      float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0, 0, 1))), 3.0);
      vec3 color = mix(vec3(0.05, 0.1, 0.3), vec3(0.1, 0.4, 0.8), fresnel);
      gl_FragColor = vec4(color, 0.8 + fresnel * 0.2);
    }
  `,
  uniforms: {
    uTime: { value: 0 }
  },
  transparent: true,
  side: THREE.DoubleSide
});
```

**3D Product Viewer:**
```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  const model = gltf.scene;
  scene.add(model);

  // Auto-rotate
  function animate() {
    model.rotation.y += 0.005;
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();
});

// Orbit controls for user interaction
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enableZoom = true;
controls.autoRotate = true;
controls.autoRotateSpeed = 1.0;
```

### 2.3 React Three Fiber Integration

```jsx
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Float, Environment } from '@react-three/drei';
import { useRef } from 'react';

// A rotating mesh component
function RotatingBox() {
  const meshRef = useRef();

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta * 0.5;
    meshRef.current.rotation.y += delta * 0.3;
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}

// Particle system
function Particles({ count = 2000 }) {
  const points = useRef();
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
    }
    return pos;
  }, [count]);

  useFrame((state, delta) => {
    points.current.rotation.y += delta * 0.05;
  });

  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.02}
        color="#ffffff"
        transparent
        sizeAttenuation
      />
    </points>
  );
}

// Main scene
function Scene() {
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <Float speed={2} rotationIntensity={0.5}>
        <RotatingBox />
      </Float>
      <Particles />
      <OrbitControls enableDamping />
      <Environment preset="city" />
    </>
  );
}

// App wrapper
export default function Hero3D() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 75 }}
      dpr={[1, 2]}  // pixel ratio clamped to 2
      gl={{ antialias: true, alpha: true }}
      style={{ position: 'fixed', top: 0, left: 0, zIndex: -1 }}
    >
      <Scene />
    </Canvas>
  );
}
```

### 2.4 Performance Budget

| Metric | Desktop Target | Mobile Target |
|--------|---------------|---------------|
| **Polygons** | < 500K | < 100K |
| **Draw calls** | < 100 | < 50 |
| **Texture size** | 2048x2048 max | 1024x1024 max |
| **FPS** | 60fps | 30fps minimum |
| **Memory** | < 200MB | < 100MB |
| **GPU memory** | < 512MB | < 256MB |

**Optimization techniques:**
- Use `InstancedMesh` for repeated objects (reduces draw calls)
- Use LOD (Level of Detail) for complex models
- Compress textures (KTX2/Basis Universal)
- Use `BufferGeometry` (not legacy `Geometry`)
- Set `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`
- Use `renderer.powerPreference = 'high-performance'`
- Dispose unused geometries, materials, textures

### 2.5 Responsive Three.js

```javascript
// Handle resize
function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}
window.addEventListener('resize', onResize);

// Mobile detection for quality
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
const quality = isMobile ? 0.5 : 1.0;
renderer.setSize(
  window.innerWidth * quality,
  window.innerHeight * quality
);
```

### 2.6 Key Shaders for Web Design

**Noise Shader (Perlin/Simplex):**
```glsl
// Common noise function used in fluid, clouds, terrain
float noise(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

// Smooth noise with interpolation
float smoothNoise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f); // smoothstep

  float a = noise(i);
  float b = noise(i + vec2(1.0, 0.0));
  float c = noise(i + vec2(0.0, 1.0));
  float d = noise(i + vec2(1.0, 1.0));

  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}
```

**Fresnel Effect (edge glow):**
```glsl
varying vec3 vNormal;
varying vec3 vViewDir;

void main() {
  float fresnel = pow(1.0 - abs(dot(vNormal, vViewDir)), 3.0);
  vec3 color = mix(baseColor, glowColor, fresnel);
  gl_FragColor = vec4(color, 1.0);
}
```

**Matcap (Material Capture):**
```glsl
// Uses a texture that encodes lighting - no lights needed
varying vec3 vNormal;
uniform sampler2D matcapTexture;

void main() {
  vec3 viewNormal = normalize(vNormal);
  vec2 matcapUV = viewNormal.xy * 0.5 + 0.5;
  vec4 matcapColor = texture2D(matcapTexture, matcapUV);
  gl_FragColor = matcapColor;
}
```

**Toon/Cel Shading:**
```glsl
varying vec3 vNormal;
varying vec3 vLightDir;

void main() {
  float intensity = dot(normalize(vNormal), normalize(vLightDir));

  // Quantize to discrete steps
  if (intensity > 0.8) intensity = 1.0;
  else if (intensity > 0.5) intensity = 0.7;
  else if (intensity > 0.2) intensity = 0.4;
  else intensity = 0.2;

  vec3 color = baseColor * intensity;
  gl_FragColor = vec4(color, 1.0);
}
```

### 2.7 Scroll-Linked 3D Scenes

```javascript
// GSAP + Three.js scroll-linked camera movement
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Camera moves on scroll
gsap.to(camera.position, {
  z: 10,
  y: 5,
  scrollTrigger: {
    trigger: ".scroll-container",
    start: "top top",
    end: "bottom bottom",
    scrub: 1,
    onUpdate: (self) => {
      // Rotate model based on scroll progress
      model.rotation.y = self.progress * Math.PI * 2;
    }
  }
});

// React Three Fiber + scroll
function ScrollScene() {
  const { camera } = useThree();
  const modelRef = useRef();

  useFrame(() => {
    const scrollProgress = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    camera.position.z = 5 + scrollProgress * 10;
    if (modelRef.current) {
      modelRef.current.rotation.y = scrollProgress * Math.PI * 2;
    }
  });

  return (
    <mesh ref={modelRef}>
      <torusKnotGeometry args={[1, 0.3, 128, 32]} />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  );
}
```

---

## 3. GSAP (GreenSock Animation Platform)

### 3.1 Core APIs

**`gsap.to()` — Animate TO target values:**
```javascript
gsap.to(".box", {
  x: 200,            // translateX: 200px
  opacity: 0.5,
  duration: 1,       // seconds
  ease: "power2.out",
  delay: 0.5,
  onComplete: () => console.log("done")
});
```

**`gsap.from()` — Animate FROM starting values:**
```javascript
gsap.from(".box", {
  x: -200,           // starts at -200, animates to current position
  opacity: 0,
  duration: 1,
  ease: "power2.out"
});
```

**`gsap.fromTo()` — Explicit start and end:**
```javascript
gsap.fromTo(".box",
  { x: -200, opacity: 0 },      // from
  { x: 200, opacity: 1, duration: 1, ease: "power2.out" }  // to
);
```

**`gsap.timeline()` — Sequence animations:**
```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });

tl.to(".box1", { x: 100 })
  .to(".box2", { x: 100 }, "-=0.3")  // overlap by 0.3s
  .to(".box3", { x: 100 }, "+=0.2")  // 0.2s gap after previous
  .to(".box4", { x: 100 }, "<");     // start at same time as previous
```

### 3.2 GSAP Easing

```
Power:    "power1", "power2", "power3", "power4"
          "power1.in", "power1.out", "power1.inOut"
Back:     "back.in(1.7)", "back.out(1.7)", "back.inOut(1.7)"
Elastic:  "elastic.in(1, 0.3)", "elastic.out(1, 0.3)"
Bounce:   "bounce.in", "bounce.out", "bounce.inOut"
Steps:    "steps(10)"
Custom:   CustomEase.create("custom", "M0,0 C0.126,0.382 0.282,0.598 0.454,0.736...")
```

### 3.3 Staggered Animations

```javascript
// Simple stagger
gsap.from(".item", {
  y: 100,
  opacity: 0,
  duration: 0.8,
  stagger: 0.15,  // 0.15s between each element
  ease: "power2.out"
});

// Advanced stagger with grid
gsap.from(".grid-item", {
  scale: 0,
  opacity: 0,
  duration: 0.5,
  stagger: {
    amount: 1.5,        // total stagger time
    from: "center",     // start from center
    grid: "auto",       // auto-detect grid
    axis: "y",          // stagger along Y axis
    ease: "power2.inOut"
  }
});

// Stagger with function
gsap.from(".item", {
  y: 50,
  opacity: 0,
  stagger: {
    each: 0.1,
    from: "random"
  }
});
```

### 3.4 ScrollTrigger Deep Dive

```javascript
// Basic trigger
ScrollTrigger.create({
  trigger: ".section",
  start: "top 80%",       // when top of trigger hits 80% from top
  end: "bottom 20%",      // when bottom of trigger hits 20% from top
  onEnter: () => {},       // scrolling down past start
  onLeave: () => {},       // scrolling down past end
  onEnterBack: () => {},   // scrolling up past end
  onLeaveBack: () => {},   // scrolling up past start
  onToggle: (self) => {},  // any toggle
  markers: true            // debug markers
});

// Scrub animation (scroll-linked)
gsap.to(".box", {
  x: 500,
  scrollTrigger: {
    trigger: ".box",
    start: "top center",
    end: "top 10%",
    scrub: 1,        // 1s smooth catch-up (true = instant)
    pin: true,        // pin element during animation
    anticipatePin: 1  // prevent jump when pinning
  }
});

// Pinning a section
ScrollTrigger.create({
  trigger: ".pinned-section",
  start: "top top",
  end: "+=500%",       // pin for 5x viewport height of scrolling
  pin: true,
  pinSpacing: true      // add spacing so content below is pushed down
});

// Snap to sections
ScrollTrigger.create({
  trigger: ".container",
  start: "top top",
  end: "bottom bottom",
  snap: {
    snapTo: 1 / 4,     // snap to quarters
    duration: 0.5,
    ease: "power2.inOut"
  }
});

// Parallax
gsap.to(".parallax-bg", {
  yPercent: -30,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

### 3.5 Page Transitions

```javascript
// GSAP + Barba.js for page transitions
import barba from '@barba/core';

barba.init({
  transitions: [{
    name: 'fade',
    leave(data) {
      return gsap.to(data.current.container, {
        opacity: 0,
        y: -50,
        duration: 0.5,
        ease: "power2.in"
      });
    },
    enter(data) {
      return gsap.from(data.next.container, {
        opacity: 0,
        y: 50,
        duration: 0.5,
        ease: "power2.out"
      });
    }
  }]
});
```

### 3.6 GSAP vs Framer Motion vs CSS Animations

| Feature | GSAP | Framer Motion | CSS Animations |
|---------|------|--------------|----------------|
| **Scroll-linked** | ScrollTrigger (best) | useScroll hook | animation-timeline: scroll() |
| **Stagger** | Advanced (grid, random, center) | Basic (with variants) | Not possible |
| **Timeline** | Full timeline control | orchestrate prop | Not possible |
| **Performance** | Excellent (requestAnimationFrame) | Good (React overhead) | Best (GPU compositor) |
| **Bundle size** | ~28KB core + ScrollTrigger ~8KB | ~32KB | 0KB |
| **React** | Manual refs | Native hooks | N/A |
| **Easing** | 30+ built-in + custom | spring + cubic bezier | cubic-bezier + steps |
| **SVG** | MorphSVG, DrawSVG | pathLength | stroke-dasharray |
| **3D** | CSS transforms only | CSS transforms only | CSS transforms only |
| **Mobile** | Excellent | Good | Excellent |

**When to use each:**
- **GSAP**: Complex scroll-linked animations, pinned sections, SVG morphing, production award sites
- **Framer Motion**: React apps, layout animations, gesture-driven UI, component-level animation
- **CSS**: Simple transitions, hover effects, performance-critical animations, no JS dependency

---

## 4. Modern CSS Techniques

### 4.1 CSS Scroll-Driven Animations

**animation-timeline property:**
```css
/* Scroll-based timeline */
.element {
  animation: fade-in linear;
  animation-timeline: scroll();           /* nearest scroller, block axis */
  animation-timeline: scroll(root);       /* root scroller */
  animation-timeline: scroll(nearest inline); /* inline axis */
  animation-timeline: scroll(self);       /* element's own scroll */
}

/* View-based timeline (element visibility) */
.element {
  animation: reveal linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;   /* animate during entry */
}
```

**Named timelines:**
```css
.scroller {
  scroll-timeline: --my-scroller block;
}

.animated-child {
  animation: slide-in linear;
  animation-timeline: --my-scroller;
}
```

**Complete example:**
```html
<div class="scroll-container">
  <div class="progress-bar"></div>
  <div class="content">
    <section class="section">Section 1</section>
    <section class="section">Section 2</section>
    <section class="section">Section 3</section>
  </div>
</div>
```

```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(to right, #00f, #f0f);
  transform-origin: left;
  animation: grow-progress linear;
  animation-timeline: scroll(root);
}

@keyframes grow-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

.section {
  animation: reveal-section linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes reveal-section {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Feature detection */
@supports not (animation-timeline: scroll()) {
  .section {
    animation: none;
    opacity: 1;
  }
}
```

**Critical note:** The `animation` shorthand resets `animation-timeline` to `auto`. Always declare `animation-timeline` after the `animation` shorthand.

### 4.2 CSS Container Queries

```css
/* Declare containment context */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Default card styles */
.card {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

/* Responsive to container, not viewport */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
    padding: 2rem;
  }
  .card-title {
    font-size: 1.5rem;
  }
}

@container card (min-width: 700px) {
  .card {
    gap: 2rem;
  }
  .card-title {
    font-size: 2rem;
  }
}

/* Container query units */
.card-title {
  font-size: max(1rem, 3cqi);  /* 3% of container inline size */
}
```

**Container query length units:**
| Unit | Meaning |
|------|---------|
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `cqmin` | Smaller of cqi/cqb |
| `cqmax` | Larger of cqi/cqb |

### 4.3 CSS `:has()` Selector

The parent selector CSS has needed for 20+ years:

```css
/* Style parent based on children */
form:has(:invalid) {
  border-color: red;
}

.card:has(img) {
  grid-template-columns: 1fr 2fr;
}

/* Sibling logic */
h1:has(+ h2) {
  margin-bottom: 0.25rem;
}

/* Logical operations */
/* OR */
body:has(video, audio) {
  --has-media: true;
}
/* AND */
body:has(video):has(audio) {
  --has-both: true;
}

/* Negative logic */
.card:not(:has(.badge)) {
  opacity: 0.7;
}

/* Style based on state */
input:has(+ label:hover) {
  border-color: blue;
}

/* Complex patterns */
.gallery:has(> img[data-loaded="false"])::after {
  content: "Loading...";
}
```

**Performance rules:**
- Avoid broad anchors: `body:has(.item)` is slow
- Prefer direct child: `.container:has(> .item)` is fast
- Limit subtree depth in `:has()` arguments

### 4.4 View Transitions API

**SPA transitions:**
```javascript
// Basic SPA view transition
document.startViewTransition(() => {
  updateDOM(); // your DOM update function
});
```

```css
/* Named transitions - elements animate between states */
.old-page-header {
  view-transition-name: page-header;
}
.new-page-header {
  view-transition-name: page-header;
}

/* Customize transitions with pseudo-elements */
::view-transition-old(root) {
  animation: fade-out 0.3s ease-out;
}
::view-transition-new(root) {
  animation: fade-in 0.3s ease-in;
}
::view-transition-group(page-header) {
  animation-duration: 0.5s;
}
```

**MPA (cross-document) transitions:**
```css
/* Both documents must opt in */
@view-transition {
  navigation: auto;
}
```

```javascript
// Handle in departing document
window.addEventListener('pageswap', (e) => {
  if (e.viewTransition) {
    // customize departing transition
  }
});

// Handle in arriving document
window.addEventListener('pagereveal', (e) => {
  if (e.viewTransition) {
    // customize arriving transition
  }
});
```

**Transition pseudo-element hierarchy:**
```
::view-transition
  ::view-transition-group(name)
    ::view-transition-image-pair(name)
      ::view-transition-old(name)  <- snapshot of old state
      ::view-transition-new(name)  <- live new state
```

### 4.5 CSS `color-mix()`

Mix colors in any color space:

```css
/* Basic mixing */
.mixed {
  background: color-mix(in oklch, blue 50%, white 50%);
  /* 50/50 mix of blue and white in OKLCH space */
}

/* Generate opacity variants */
:root {
  --primary: #3b82f6;
}
.overlay {
  background: color-mix(in srgb, var(--primary) 50%, transparent);
  /* 50% opacity of primary */
}

/* Lighter/darker variants */
.button:hover {
  background: color-mix(in oklch, var(--primary) 80%, white);
}
.button:active {
  background: color-mix(in oklch, var(--primary) 80%, black);
}

/* Hue interpolation */
.gradient-stop {
  color: color-mix(in oklch longer hue, red 50%, blue);
}
```

**Color space choices:**
| Use Case | Color Space |
|----------|------------|
| Perceptually uniform mixing | `oklab` or `oklch` |
| Avoid muddy midtones | `oklch` (polar) |
| Match design tool behavior | `srgb` |
| Physically accurate light mixing | `srgb-linear` |

### 4.6 OKLCH Color Space

Perceptually uniform color space - the future of CSS colors:

```css
/* Syntax: oklch(lightness chroma hue) */
.brand-primary {
  color: oklch(0.65 0.25 265);     /* vivid blue */
  /* L: 0-1, C: 0-0.4, H: 0-360 */
}

/* Generate palette from single hue */
:root {
  --hue: 265;
}
.color-50  { background: oklch(0.97 0.01 var(--hue)); }
.color-100 { background: oklch(0.93 0.03 var(--hue)); }
.color-200 { background: oklch(0.87 0.06 var(--hue)); }
.color-300 { background: oklch(0.78 0.12 var(--hue)); }
.color-400 { background: oklch(0.68 0.19 var(--hue)); }
.color-500 { background: oklch(0.58 0.25 var(--hue)); }
.color-600 { background: oklch(0.48 0.22 var(--hue)); }
.color-700 { background: oklch(0.38 0.18 var(--hue)); }
.color-800 { background: oklch(0.28 0.13 var(--hue)); }
.color-900 { background: oklch(0.18 0.08 var(--hue)); }

/* Relative color syntax - modify any color */
.button:hover {
  /* Lighten the primary color by 15% */
  background: oklch(from var(--primary) calc(l + 0.15) c h);
}
.button:active {
  /* Darken and desaturate */
  background: oklch(from var(--primary) calc(l - 0.1) calc(c - 0.05) h);
}
```

**Key advantages over HSL:**
- Equal lightness values look equally bright across all hues
- Changing hue doesn't shift perceived saturation
- Covers entire visible gamut (beyond sRGB)
- Gradients don't produce muddy midtones

### 4.7 CSS Nesting

Native browser nesting (no Sass needed):

```css
/* Basic nesting */
.card {
  padding: 1rem;
  background: white;

  & .title {
    font-size: 1.5rem;
    font-weight: bold;
  }

  & .description {
    color: gray;
    line-height: 1.6;
  }

  &:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  /* Nested media queries */
  @media (min-width: 768px) {
    padding: 2rem;
    & .title {
      font-size: 2rem;
    }
  }
}

/* Compound selectors require & */
.button {
  background: blue;

  &.small {     /* .button.small */
    padding: 0.25rem 0.5rem;
  }

  & .icon {     /* .button .icon */
    margin-right: 0.5rem;
  }
}

/* Appended nesting - reverse context */
.sidebar {
  width: 300px;

  .layout:has(.sidebar-open) & {
    transform: translateX(0);
  }
}
```

**Key differences from Sass:**
- No string concatenation: `&__child` does NOT work
- `&` is optional for descendant selectors (whitespace implied)
- `&` is required for compound selectors (`.parent.child`)
- Specificity follows `:is()` rules (highest specificity in list)
- Parsed by browser, no build step

### 4.8 CSS `@layer` Cascade Management

Control cascade order explicitly:

```css
/* Declare layer order (last wins) */
@layer reset, base, components, utilities;

/* Or separate declaration from assignment */
@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
}

@layer base {
  body {
    font-family: system-ui;
    line-height: 1.6;
  }
}

@layer components {
  .button {
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
  }
}

@layer utilities {
  .hidden { display: none; }
  .flex { display: flex; }
}

/* Import into layers */
@import "reset.css" layer(reset);
@import "base.css" layer(base);
```

**Critical behaviors:**
- Non-layered styles always beat layered styles
- Later layers beat earlier layers (regardless of specificity)
- `!important` reverses the order (first layer wins)
- Simple selectors in later layers beat complex selectors in earlier layers

```css
@layer first, second;

@layer first {
  #deeply .nested .selector {
    color: red;    /* loses - earlier layer */
  }
}

@layer second {
  p {
    color: blue;   /* wins - later layer, despite lower specificity */
  }
}
```

**Use case: Third-party CSS management:**
```css
@layer vendor, custom;

@import "bootstrap.css" layer(vendor);
@import "tailwind.css" layer(vendor);

@layer custom {
  /* Your styles always win over vendor */
  .button {
    background: var(--brand-color);
  }
}
```

---

## 5. Browser Support Summary (as of May 2026)

| Feature | Chrome | Firefox | Safari | Baseline |
|---------|--------|---------|--------|----------|
| CSS scroll-driven animations | 115+ | 110+ | 18+ (partial) | Not Baseline |
| Container queries | 105+ | 110+ | 16+ | Widely available |
| `:has()` | 105+ | 121+ | 15.4+ | Widely available (Dec 2023) |
| View Transitions (SPA) | 111+ | Behind flag | 18+ | Limited |
| View Transitions (MPA) | 126+ | No | 18+ | Limited |
| `color-mix()` | 111+ | 113+ | 16.2+ | Widely available (May 2023) |
| OKLCH | 111+ | 113+ | 15.4+ | Widely available (May 2023) |
| CSS nesting | 120+ | 117+ | 17.2+ | Widely available |
| `@layer` | 99+ | 97+ | 15.4+ | Widely available (Mar 2022) |

---

## Sources

- MDN Web Docs: CSS scroll-driven animations, container queries, `:has()`, View Transitions API, `color-mix()`, OKLCH, `@layer`, CSS nesting (accessed 2026-05-20)
- Three.js Fundamentals: https://threejs.org/manual/en/fundamentals.html (accessed 2026-05-20)
- Three.js ShaderMaterial docs: https://threejs.org/docs/ (accessed 2026-05-20)
- GSAP Documentation: https://gsap.com/docs/v3/ (referenced)
- CSS Scroll-driven Animations Spec: https://drafts.csswg.org/scroll-animations-1/
- CSS Color Module Level 5: https://drafts.csswg.org/css-color-5/
