# Documentation Framework Configurations

Deep-dive configs for Docusaurus, MkDocs Material, VitePress. Use when user wants to customize beyond defaults.

---

## Docusaurus Configuration

### docusaurus.config.js

```javascript
// @ts-check
const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Your Project',
  tagline: 'One sentence description',
  favicon: 'img/favicon.ico',
  url: 'https://yourusername.github.io',
  baseUrl: '/your-repo/',
  organizationName: 'yourusername',
  projectName: 'your-repo',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/yourusername/your-repo/tree/main/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
        },
        blog: false, // Disable if not needed
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.jpg',
      navbar: {
        title: 'Your Project',
        logo: {
          alt: 'Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            href: 'https://github.com/yourusername/your-repo',
            label: 'GitHub',
            position: 'right',
          },
          {
            type: 'docsVersionDropdown',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/getting-started',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/yourusername/your-repo',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Your Project.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
        additionalLanguages: ['bash', 'python', 'javascript', 'typescript'],
      },
      algolia: {
        appId: 'YOUR_APP_ID',
        apiKey: 'YOUR_SEARCH_API_KEY',
        indexName: 'YOUR_INDEX_NAME',
      },
    }),
};

module.exports = config;
```

### sidebars.js

```javascript
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'getting-started',
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/authentication',
        'guides/error-handling',
        'guides/best-practices',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/classes',
        'api/functions',
        'api/types',
      ],
    },
    {
      type: 'category',
      label: 'Advanced',
      items: [
        'advanced/architecture',
        'advanced/contributing',
      ],
    },
  ],
};

module.exports = sidebars;
```

### Custom CSS (src/css/custom.css)

```css
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-color-primary-darker: #277148;
  --ifm-color-primary-darkest: #205d3b;
  --ifm-color-primary-light: #33925d;
  --ifm-color-primary-lighter: #359962;
  --ifm-color-primary-lightest: #3cad6e;
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}

[data-theme='dark'] {
  --ifm-color-primary: #25c2a0;
  --ifm-color-primary-dark: #21af90;
  --ifm-color-primary-darker: #1fa588;
  --ifm-color-primary-darkest: #1a8870;
  --ifm-color-primary-light: #29d5b0;
  --ifm-color-primary-lighter: #32d8b4;
  --ifm-color-primary-lightest: #4fddbf;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}

/* Custom styles */
.markdown > h2 {
  --ifm-h2-font-size: 2rem;
  margin-top: 3rem;
}

.markdown > h3 {
  --ifm-h3-font-size: 1.5rem;
  margin-top: 2rem;
}

code {
  border-radius: 4px;
  padding: 0.2rem 0.4rem;
}
```

### Versioning

```bash
# Create a new version
npm run docusaurus docs:version 1.0.0

# This creates:
# - versioned_docs/version-1.0.0/ (snapshot of docs)
# - versions.json (list of versions)
```

---

## MkDocs Material Configuration

### mkdocs.yml

```yaml
site_name: Your Project
site_url: https://yourusername.github.io/your-repo/
site_description: One sentence description
site_author: Your Name
repo_url: https://github.com/yourusername/your-repo
repo_name: yourusername/your-repo
edit_uri: edit/main/docs/

theme:
  name: material
  language: en
  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: Roboto
    code: Roboto Mono
  features:
    - navigation.instant      # Instant loading
    - navigation.tracking     # URL updates with scroll
    - navigation.tabs         # Top-level tabs
    - navigation.sections     # Collapsible sections
    - navigation.expand       # Expand all sections by default
    - navigation.top          # Back to top button
    - search.suggest          # Search suggestions
    - search.highlight        # Highlight search terms
    - content.code.copy       # Copy button on code blocks
    - content.action.edit     # Edit button
    - content.action.view     # View source button
  icon:
    repo: fontawesome/brands/github

plugins:
  - search:
      lang: en
  - minify:
      minify_html: true

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Guides:
    - Authentication: guides/authentication.md
    - Error Handling: guides/error-handling.md
    - Best Practices: guides/best-practices.md
  - API Reference:
    - Classes: api/classes.md
    - Functions: api/functions.md
    - Types: api/types.md
  - Advanced:
    - Architecture: advanced/architecture.md
    - Contributing: advanced/contributing.md

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/yourusername
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/yourusername
  version:
    provider: mike
```

### Advanced Features

**Admonitions (Callouts):**
```markdown
!!! note
    This is a note.

!!! warning
    This is a warning.

!!! tip
    This is a tip.

!!! danger
    This is dangerous.
```

**Tabs (Multi-language examples):**
```markdown
=== "Python"
    ```python
    print("Hello")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello");
    ```
```

**Code with line numbers:**
```markdown
```python linenums="1"
def hello():
    print("Hello")
```
```

---

## VitePress Configuration

### .vitepress/config.js

```javascript
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Your Project',
  description: 'One sentence description',
  base: '/your-repo/',
  
  themeConfig: {
    logo: '/logo.svg',
    
    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'API', link: '/api/classes' },
      { text: 'GitHub', link: 'https://github.com/yourusername/your-repo' }
    ],
    
    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/getting-started' },
            { text: 'Installation', link: '/guide/installation' }
          ]
        },
        {
          text: 'Guides',
          items: [
            { text: 'Authentication', link: '/guide/authentication' },
            { text: 'Error Handling', link: '/guide/error-handling' },
            { text: 'Best Practices', link: '/guide/best-practices' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API Reference',
          items: [
            { text: 'Classes', link: '/api/classes' },
            { text: 'Functions', link: '/api/functions' },
            { text: 'Types', link: '/api/types' }
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/yourusername/your-repo' }
    ],
    
    editLink: {
      pattern: 'https://github.com/yourusername/your-repo/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
    
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026-present Your Name'
    },
    
    search: {
      provider: 'local'
    }
  },
  
  markdown: {
    lineNumbers: true
  }
})
```

### Custom Theme (Optional)

```javascript
// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // Register custom components
  }
}
```

### Custom CSS

```css
/* .vitepress/theme/custom.css */
:root {
  --vp-c-brand: #646cff;
  --vp-c-brand-light: #747bff;
  --vp-c-brand-lighter: #9499ff;
  --vp-c-brand-dark: #535bf2;
  --vp-c-brand-darker: #454ce1;
}

.dark {
  --vp-c-brand: #747bff;
  --vp-c-brand-light: #9499ff;
  --vp-c-brand-lighter: #b4b9ff;
  --vp-c-brand-dark: #646cff;
  --vp-c-brand-darker: #535bf2;
}

/* Custom styles */
.vp-doc h2 {
  margin-top: 48px;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 24px;
}
```

---

## Comparison: Which to Choose?

| Feature | Docusaurus | MkDocs Material | VitePress |
|---------|-----------|----------------|-----------|
| **Setup Time** | 5 min | 2 min | 3 min |
| **Build Speed** | Slow (React) | Fast (Python) | Blazing (Vite) |
| **Versioning** | Built-in | Plugin (mike) | Manual |
| **i18n** | Built-in | Built-in | Manual |
| **Search** | Algolia/local | Built-in | Built-in |
| **Customization** | High (React) | Medium (Python) | High (Vue) |
| **Learning Curve** | Medium | Low | Low |
| **Ecosystem** | Large | Large | Growing |
| **Best For** | React teams, versioned APIs | Python teams, simple docs | Vue teams, speed-first |

**Recommendation:**
- **Docusaurus** if you need versioning, i18n, and are comfortable with React
- **MkDocs Material** if you want beautiful docs fast with minimal config
- **VitePress** if you want blazing speed and modern tooling

---

## Advanced Patterns

### Multi-language Code Examples

**Docusaurus:**
```mdx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="python" label="Python">
    ```python
    print("Hello")
    ```
  </TabItem>
  <TabItem value="js" label="JavaScript">
    ```javascript
    console.log("Hello");
    ```
  </TabItem>
</Tabs>
```

**MkDocs Material:**
```markdown
=== "Python"
    ```python
    print("Hello")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello");
    ```
```

**VitePress:**
```markdown
::: code-group
```python [Python]
print("Hello")
```

```javascript [JavaScript]
console.log("Hello");
```
:::
```

### API Auto-generation

**From TypeScript:**
```bash
npm install -D typedoc typedoc-plugin-markdown
npx typedoc --plugin typedoc-plugin-markdown --out docs/api src/index.ts
```

**From Python:**
```bash
pip install pdoc3
pdoc --html --output-dir docs/api your_module
```

**From OpenAPI:**
```bash
npm install -g redoc-cli
redoc-cli bundle openapi.yaml -o docs/api.html
```

### Versioning with MkDocs (mike)

```bash
pip install mike

# Deploy version 1.0
mike deploy 1.0 latest --update-aliases

# Deploy version 2.0
mike deploy 2.0 latest --update-aliases

# Set default version
mike set-default latest

# List versions
mike list

# Delete version
mike delete 1.0
```

### Search Optimization

**Docusaurus (Algolia):**
1. Apply for Algolia DocSearch: https://docsearch.algolia.com/apply/
2. Add config to `docusaurus.config.js` (see above)
3. Algolia crawls your site automatically

**MkDocs Material (Built-in):**
- Works out of the box
- Customize in `mkdocs.yml`:
```yaml
plugins:
  - search:
      lang: en
      separator: '[\s\-\.]+'
```

**VitePress (Built-in):**
- Works out of the box
- Customize in `config.js`:
```javascript
search: {
  provider: 'local',
  options: {
    miniSearch: {
      searchOptions: {
        fuzzy: 0.2,
        prefix: true
      }
    }
  }
}
```

---

## Performance Optimization

### Image Optimization

**Docusaurus:**
```javascript
// docusaurus.config.js
module.exports = {
  plugins: [
    [
      '@docusaurus/plugin-ideal-image',
      {
        quality: 70,
        max: 1030,
        min: 640,
        steps: 2,
      },
    ],
  ],
};
```

**MkDocs Material:**
```bash
pip install mkdocs-glightbox
```
```yaml
# mkdocs.yml
plugins:
  - glightbox
```

**VitePress:**
```javascript
// .vitepress/config.js
export default {
  vite: {
    plugins: [
      // Add image optimization plugin
    ]
  }
}
```

### Lazy Loading

All three frameworks support lazy loading by default for images and code blocks.

### CDN

Deploy to:
- **GitHub Pages** (free, automatic with Actions)
- **Netlify** (free tier, automatic builds)
- **Vercel** (free tier, automatic builds)
- **Cloudflare Pages** (free, fast CDN)

---

## Troubleshooting

### Docusaurus

**Problem:** Build fails with "Cannot find module"
**Fix:** Delete `node_modules` and `package-lock.json`, run `npm install`

**Problem:** Broken links in production
**Fix:** Check `baseUrl` in `docusaurus.config.js` matches your GitHub Pages URL

### MkDocs Material

**Problem:** Theme not found
**Fix:** `pip install mkdocs-material` (not just `mkdocs`)

**Problem:** Plugins not working
**Fix:** Check plugin is installed: `pip list | grep mkdocs`

### VitePress

**Problem:** 404 on GitHub Pages
**Fix:** Set correct `base` in `.vitepress/config.js`

**Problem:** Search not working
**Fix:** Ensure `search: { provider: 'local' }` in config

---

## Resources

- [Docusaurus Docs](https://docusaurus.io/)
- [MkDocs Material Docs](https://squidfunk.github.io/mkdocs-material/)
- [VitePress Docs](https://vitepress.dev/)
- [GitHub Pages Docs](https://docs.github.com/pages)
- [Write the Docs](https://www.writethedocs.org/)
