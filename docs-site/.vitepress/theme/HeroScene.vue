<template>
  <div ref="container" class="hero-canvas-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const container = ref(null)
let renderer = null
let animationId = null

onMounted(async () => {
  if (!container.value || typeof window === 'undefined') return

  const THREE = await import('three')

  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.set(0, 0, 6)

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x000000, 0)
  container.value.appendChild(renderer.domElement)

  const isDark = document.documentElement.classList.contains('dark')
  const brandHex = isDark ? 0x747bff : 0x646cff
  const accentHex = isDark ? 0x34d399 : 0x2dd4bf
  const mutedHex = isDark ? 0x8892b0 : 0x94a3b8

  // ─── Central wireframe sphere ───────────────────────────
  const sphereGeo = new THREE.IcosahedronGeometry(1.6, 2)
  const sphereMat = new THREE.MeshBasicMaterial({
    color: brandHex,
    wireframe: true,
    transparent: true,
    opacity: isDark ? 0.12 : 0.08
  })
  const sphere = new THREE.Mesh(sphereGeo, sphereMat)
  scene.add(sphere)

  // Inner sphere
  const innerGeo = new THREE.IcosahedronGeometry(1.1, 1)
  const innerMat = new THREE.MeshBasicMaterial({
    color: accentHex,
    wireframe: true,
    transparent: true,
    opacity: isDark ? 0.1 : 0.06
  })
  const innerSphere = new THREE.Mesh(innerGeo, innerMat)
  scene.add(innerSphere)

  // ─── Orbiting rings ─────────────────────────────────────
  const rings = []
  for (let i = 0; i < 3; i++) {
    const ringGeo = new THREE.TorusGeometry(2.2 + i * 0.5, 0.015, 8, 80)
    const ringMat = new THREE.MeshBasicMaterial({
      color: i === 1 ? accentHex : brandHex,
      transparent: true,
      opacity: isDark ? 0.18 : 0.1
    })
    const ring = new THREE.Mesh(ringGeo, ringMat)
    ring.rotation.x = Math.PI * 0.35 + i * 0.3
    ring.rotation.y = i * 0.5
    ring.userData = { speed: 0.15 + i * 0.08, axis: i }
    scene.add(ring)
    rings.push(ring)
  }

  // ─── Particle field — dense, layered ────────────────────
  function createParticles(count, spread, size, color, opacity) {
    const positions = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)
      const r = spread * (0.5 + Math.random() * 0.5)
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta)
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      positions[i * 3 + 2] = r * Math.cos(phi)
    }
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    const mat = new THREE.PointsMaterial({
      size,
      color,
      transparent: true,
      opacity,
      sizeAttenuation: true
    })
    const pts = new THREE.Points(geo, mat)
    scene.add(pts)
    return pts
  }

  const outerParticles = createParticles(300, 5, isDark ? 0.02 : 0.018, mutedHex, isDark ? 0.5 : 0.3)
  const midParticles = createParticles(150, 3.5, isDark ? 0.025 : 0.02, brandHex, isDark ? 0.4 : 0.25)
  const innerParticles = createParticles(80, 2, isDark ? 0.03 : 0.025, accentHex, isDark ? 0.35 : 0.2)

  // ─── Floating shards ────────────────────────────────────
  const shards = []
  const shardGeo = new THREE.OctahedronGeometry(0.12, 0)

  for (let i = 0; i < 12; i++) {
    const mat = new THREE.MeshBasicMaterial({
      color: i % 3 === 0 ? accentHex : brandHex,
      wireframe: true,
      transparent: true,
      opacity: isDark ? 0.25 : 0.15
    })
    const shard = new THREE.Mesh(shardGeo, mat)
    const angle = (i / 12) * Math.PI * 2
    const radius = 3 + Math.random() * 1.5
    shard.position.set(
      Math.cos(angle) * radius,
      (Math.random() - 0.5) * 3,
      Math.sin(angle) * radius - 2
    )
    shard.userData = {
      angle,
      radius,
      speed: 0.1 + Math.random() * 0.15,
      yFloat: Math.random() * Math.PI * 2,
      rotSpeed: (Math.random() - 0.5) * 0.02
    }
    scene.add(shard)
    shards.push(shard)
  }

  // ─── Mouse ──────────────────────────────────────────────
  const mouse = { x: 0, y: 0 }

  function onMouseMove(e) {
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1
  }
  window.addEventListener('mousemove', onMouseMove, { passive: true })

  // ─── Animation ──────────────────────────────────────────
  const clock = new THREE.Clock()

  function animate() {
    animationId = requestAnimationFrame(animate)
    const t = clock.getElapsedTime()

    // Camera follows mouse gently
    camera.position.x += (mouse.x * 0.5 - camera.position.x) * 0.015
    camera.position.y += (mouse.y * 0.3 - camera.position.y) * 0.015
    camera.lookAt(0, 0, 0)

    // Central sphere rotation
    sphere.rotation.y = t * 0.08
    sphere.rotation.x = Math.sin(t * 0.05) * 0.15

    innerSphere.rotation.y = -t * 0.12
    innerSphere.rotation.z = Math.sin(t * 0.07) * 0.2

    // Rings orbit
    for (const ring of rings) {
      ring.rotation.z = t * ring.userData.speed
    }

    // Particles slow rotation
    outerParticles.rotation.y = t * 0.015
    outerParticles.rotation.x = t * 0.008
    midParticles.rotation.y = -t * 0.02
    innerParticles.rotation.y = t * 0.03

    // Shards orbit and float
    for (const shard of shards) {
      const { angle, radius, speed, yFloat, rotSpeed } = shard.userData
      const a = angle + t * speed
      shard.position.x = Math.cos(a) * radius
      shard.position.z = Math.sin(a) * radius - 2
      shard.position.y += Math.sin(t * 0.8 + yFloat) * 0.002
      shard.rotation.x += rotSpeed
      shard.rotation.y += rotSpeed * 0.7
    }

    renderer.render(scene, camera)
  }

  animate()

  // ─── Resize ─────────────────────────────────────────────
  function onResize() {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  }
  window.addEventListener('resize', onResize, { passive: true })

  // ─── Theme observer ─────────────────────────────────────
  const themeObserver = new MutationObserver(() => {
    const nowDark = document.documentElement.classList.contains('dark')
    const nb = nowDark ? 0x747bff : 0x646cff
    const na = nowDark ? 0x34d399 : 0x2dd4bf
    const nm = nowDark ? 0x8892b0 : 0x94a3b8

    sphereMat.color.setHex(nb)
    sphereMat.opacity = nowDark ? 0.12 : 0.08
    innerMat.color.setHex(na)
    innerMat.opacity = nowDark ? 0.1 : 0.06

    rings.forEach((r, i) => {
      r.material.color.setHex(i === 1 ? na : nb)
      r.material.opacity = nowDark ? 0.18 : 0.1
    })

    outerParticles.material.color.setHex(nm)
    outerParticles.material.opacity = nowDark ? 0.5 : 0.3
    midParticles.material.color.setHex(nb)
    midParticles.material.opacity = nowDark ? 0.4 : 0.25
    innerParticles.material.color.setHex(na)
    innerParticles.material.opacity = nowDark ? 0.35 : 0.2

    shards.forEach((s, i) => {
      s.material.color.setHex(i % 3 === 0 ? na : nb)
      s.material.opacity = nowDark ? 0.25 : 0.15
    })
  })

  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })

  onUnmounted(() => {
    cancelAnimationFrame(animationId)
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('resize', onResize)
    themeObserver.disconnect()
    renderer.dispose()
    container.value?.removeChild(renderer.domElement)
  })
})
</script>
