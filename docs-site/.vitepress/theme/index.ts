import DefaultTheme from 'vitepress/theme'
import { h, onMounted, onUnmounted, watch, defineComponent } from 'vue'
import { useRoute, useData } from 'vitepress'
import HeroScene from './HeroScene.vue'
import WaveFooter from './WaveFooter.vue'
import './style.css'

const HeroSceneWrapper = defineComponent({
  name: 'HeroSceneWrapper',
  setup() {
    const { frontmatter } = useData()
    return () => {
      if (frontmatter.value.layout === 'home') {
        return h(HeroScene)
      }
      return null
    }
  }
})

const FooterWrapper = defineComponent({
  name: 'FooterWrapper',
  setup() {
    return () => h(WaveFooter)
  }
})

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'home-hero-before': () => h(HeroSceneWrapper),
      'layout-bottom': () => h(FooterWrapper)
    })
  },
  setup() {
    const route = useRoute()

    let observer: IntersectionObserver | null = null
    let progressBar: HTMLDivElement | null = null

    function initScrollReveal() {
      observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('revealed')
              observer?.unobserve(entry.target)
            }
          })
        },
        { threshold: 0.1, rootMargin: '-5% 0px' }
      )

      document.querySelectorAll('.reveal').forEach((el) => {
        observer?.observe(el)
      })
    }

    function initScrollProgress() {
      if (!progressBar) {
        progressBar = document.createElement('div')
        progressBar.className = 'scroll-progress'
        document.body.appendChild(progressBar)
      }

      function updateProgress() {
        const scrollTop = window.scrollY
        const docHeight = document.documentElement.scrollHeight - window.innerHeight
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0
        if (progressBar) {
          progressBar.style.width = `${progress}%`
        }
      }

      window.addEventListener('scroll', updateProgress, { passive: true })
      updateProgress()

      return () => window.removeEventListener('scroll', updateProgress)
    }

    let cleanupScroll: (() => void) | null = null

    function init() {
      setTimeout(() => {
        initScrollReveal()
        cleanupScroll = initScrollProgress()
      }, 100)
    }

    onMounted(init)

    watch(() => route.path, () => {
      observer?.disconnect()
      setTimeout(() => initScrollReveal(), 150)
    })

    onUnmounted(() => {
      observer?.disconnect()
      cleanupScroll?.()
      progressBar?.remove()
      progressBar = null
    })
  }
}
