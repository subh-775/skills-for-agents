import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Skills for Agents',
  description: 'Composable, domain-specific instruction sets for AI coding agents',
  base: '/skills-for-agents/',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/skills-for-agents/logo.svg' }],
    ['meta', { property: 'og:title', content: 'Skills for Agents' }],
    ['meta', { property: 'og:description', content: '17 composable skills for AI coding agents' }],
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Skills', link: '/skills/' },
      { text: 'SIP', link: '/sip/' },
      {
        text: 'v1.0.5',
        items: [
          { text: 'Changelog', link: 'https://github.com/IsNoobgrammer/skills-for-agents/releases' },
          { text: 'npm', link: 'https://www.npmjs.com/package/skills-for-agents' },
        ]
      }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/getting-started' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Your First Skill', link: '/guide/first-skill' },
          ]
        },
        {
          text: 'Core Concepts',
          items: [
            { text: 'Composition', link: '/guide/composition' },
            { text: 'Creating Skills', link: '/guide/creating-skills' },
            { text: 'SIP Framework', link: '/sip/' },
          ]
        },
        {
          text: 'Advanced',
          items: [
            { text: 'Architecture', link: '/guide/architecture' },
            { text: 'Contributing', link: '/guide/contributing' },
          ]
        }
      ],
      '/skills/': [
        {
          text: 'Skills Catalog',
          items: [
            { text: 'Overview', link: '/skills/' },
          ]
        },
        {
          text: 'Voice',
          collapsed: false,
          items: [
            { text: 'Blogger', link: '/skills/blogger' },
          ]
        },
        {
          text: 'Density',
          collapsed: false,
          items: [
            { text: 'Caveman', link: '/skills/caveman' },
            { text: 'Compress', link: '/skills/compress' },
          ]
        },
        {
          text: 'Craft',
          collapsed: false,
          items: [
            { text: 'Painter', link: '/skills/painter' },
            { text: 'Harden', link: '/skills/harden' },
          ]
        },
        {
          text: 'Process',
          collapsed: false,
          items: [
            { text: 'Memory', link: '/skills/memory' },
            { text: 'ML Engine', link: '/skills/ml-engine' },
            { text: 'Planner', link: '/skills/planner' },
            { text: 'Postmortem', link: '/skills/postmortem' },
            { text: 'Refactor', link: '/skills/refactor' },
            { text: 'Skill Creator', link: '/skills/skill-creator' },
            { text: 'Slidify', link: '/skills/slidify' },
          ]
        },
        {
          text: 'Content',
          collapsed: false,
          items: [
            { text: 'Documenter', link: '/skills/documenter' },
            { text: 'Learn', link: '/skills/learn' },
            { text: 'Researcher', link: '/skills/researcher' },
          ]
        },
        {
          text: 'Analysis',
          collapsed: false,
          items: [
            { text: 'OSINT', link: '/skills/osint' },
            { text: 'Godmode', link: '/skills/godmode' },
          ]
        }
      ],
      '/sip/': [
        {
          text: 'SIP Framework',
          items: [
            { text: 'Overview', link: '/sip/' },
            { text: 'Domains', link: '/sip/domains' },
            { text: 'Composition Modes', link: '/sip/composition' },
            { text: 'Precedence Rules', link: '/sip/precedence' },
            { text: 'Contract', link: '/sip/contract' },
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/IsNoobgrammer/skills-for-agents' },
      { icon: 'npm', link: 'https://www.npmjs.com/package/skills-for-agents' },
    ],

    editLink: {
      pattern: 'https://github.com/IsNoobgrammer/skills-for-agents/edit/main/docs-site/:path',
      text: 'Edit this page on GitHub'
    },

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright 2026-present Shaurya Sharthak'
    },

    search: {
      provider: 'local'
    },

    outline: {
      level: [2, 3],
      label: 'On this page'
    },

    lastUpdated: {
      text: 'Last updated'
    },
  },

  markdown: {
    lineNumbers: true
  }
})
