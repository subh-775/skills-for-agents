<template>
  <div class="wave-footer">
    <div class="wave-ocean">
      <svg class="wave-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <!-- Back wave — slow, tall -->
        <path class="wave wave-back" d="
          M0,160
          C120,100 240,200 360,160
          C480,120 600,200 720,160
          C840,120 960,200 1080,160
          C1200,120 1320,200 1440,160
          L1440,320 L0,320 Z
        " />
        <!-- Mid wave -->
        <path class="wave wave-mid" d="
          M0,180
          C160,130 320,230 480,180
          C640,130 800,230 960,180
          C1120,130 1280,230 1440,180
          L1440,320 L0,320 Z
        " />
        <!-- Front wave — fast, short -->
        <path class="wave wave-front" d="
          M0,200
          C180,160 360,240 540,200
          C720,160 900,240 1080,200
          C1260,160 1380,220 1440,200
          L1440,320 L0,320 Z
        " />
        <!-- Foam/surf line on front wave -->
        <path class="wave-foam" d="
          M0,200
          C180,160 360,240 540,200
          C720,160 900,240 1080,200
          C1260,160 1380,220 1440,200
        " fill="none" />
      </svg>
    </div>
    <div class="wave-content">
      <div class="wave-inner">
        <div class="wave-brand">
          <span class="wave-logo">SFA</span>
          <span class="wave-tagline">Skills for Agents</span>
        </div>
        <div class="wave-links">
          <a href="https://github.com/IsNoobgrammer/skills-for-agents" target="_blank" rel="noopener">GitHub</a>
          <a href="https://www.npmjs.com/package/skills-for-agents" target="_blank" rel="noopener">npm</a>
          <a href="/skills-for-agents/guide/getting-started">Docs</a>
          <a href="/skills-for-agents/sip/">SIP</a>
        </div>
        <div class="wave-copy">
          MIT License &middot; Shaurya Sharthak &middot; 2026
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.wave-footer {
  position: relative;
  margin-top: var(--space-24, 6rem);
  overflow: hidden;
}

.wave-ocean {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.wave-svg {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* ─── Wave layers ───────────────────────────────────────── */
.wave {
  stroke-width: 0;
}

.wave-back {
  fill: var(--brand, oklch(0.55 0.20 265));
  opacity: 0.06;
  animation: wave-rise 6s ease-in-out infinite;
}

.wave-mid {
  fill: var(--accent, oklch(0.68 0.16 175));
  opacity: 0.05;
  animation: wave-rise 4.5s ease-in-out infinite;
  animation-delay: -1.5s;
}

.wave-front {
  fill: var(--surface-sunken, oklch(0.945 0.012 75));
  animation: wave-rise 3.5s ease-in-out infinite;
  animation-delay: -0.8s;
}

:root.dark .wave-front {
  fill: var(--surface-sunken, oklch(0.09 0.008 250));
}

.wave-foam {
  stroke: var(--brand, oklch(0.55 0.20 265));
  stroke-width: 1.5;
  opacity: 0.15;
  animation: wave-rise 3.5s ease-in-out infinite;
  animation-delay: -0.8s;
  filter: blur(1px);
}

:root.dark .wave-foam {
  stroke: var(--brand-light, oklch(0.80 0.12 265));
  opacity: 0.1;
}

/* ─── Vertical wave motion ──────────────────────────────── */
@keyframes wave-rise {
  0%, 100% {
    transform: translateY(0px);
  }
  25% {
    transform: translateY(-12px);
  }
  50% {
    transform: translateY(8px);
  }
  75% {
    transform: translateY(-6px);
  }
}

/* ─── Content ───────────────────────────────────────────── */
.wave-content {
  position: relative;
  z-index: 2;
  background: var(--surface-sunken, oklch(0.945 0.012 75));
  padding: var(--space-12, 3rem) 0 var(--space-8, 2rem);
}

:root.dark .wave-content {
  background: var(--surface-sunken, oklch(0.09 0.008 250));
}

.wave-inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 var(--space-8, 2rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-6, 1.5rem);
  text-align: center;
}

.wave-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3, 0.75rem);
}

.wave-logo {
  font-family: var(--font-body, 'Montserrat', sans-serif);
  font-weight: 800;
  font-size: 1.25rem;
  letter-spacing: -0.04em;
  color: var(--ink, oklch(0.18 0.012 60));
  background: var(--brand-surface, oklch(0.96 0.012 80));
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid var(--border, oklch(0.88 0.012 70));
}

:root.dark .wave-logo {
  color: var(--ink, oklch(0.88 0.006 250));
  background: var(--surface-raised, oklch(0.16 0.012 250));
  border-color: var(--border, oklch(0.28 0.010 250));
}

.wave-tagline {
  font-family: var(--font-body, 'Montserrat', sans-serif);
  font-weight: 400;
  font-size: var(--text-sm, 0.875rem);
  color: var(--ink-muted, oklch(0.58 0.010 60));
}

.wave-links {
  display: flex;
  gap: var(--space-6, 1.5rem);
  flex-wrap: wrap;
  justify-content: center;
}

.wave-links a {
  font-family: var(--font-body, 'Montserrat', sans-serif);
  font-size: var(--text-sm, 0.875rem);
  font-weight: 500;
  color: var(--ink-secondary, oklch(0.42 0.012 60));
  text-decoration: none;
  transition: color 0.15s ease;
}

.wave-links a:hover {
  color: var(--brand, oklch(0.55 0.20 265));
}

.wave-copy {
  font-family: var(--font-body, 'Montserrat', sans-serif);
  font-size: var(--text-xs, 0.75rem);
  color: var(--ink-muted, oklch(0.58 0.010 60));
  padding-top: var(--space-4, 1rem);
  border-top: 1px solid var(--border, oklch(0.88 0.012 70));
  width: 100%;
}

@media (prefers-reduced-motion: reduce) {
  .wave-back, .wave-mid, .wave-front, .wave-foam {
    animation: none;
  }
}
</style>
