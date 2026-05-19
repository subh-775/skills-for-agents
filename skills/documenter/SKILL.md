---
name: documenter
description: >
  Comprehensive documentation skill. Use when user wants to document code, APIs, libraries, projects, or systems. Triggers on: "document this", "write docs", "create documentation", "API docs", "README", "user guide", "technical docs", "doc site", "documentation website". Creates extensive, well-structured docs with examples, guides, API references. Asks about live deployment via GitHub Actions when user specifically requests hosted docs or mentions wanting a documentation website.
domain: content
composable: true
yields_to: [process, craft]
---

# Documenter — Comprehensive Documentation Engine

> [!IMPORTANT]
> This skill has reference files in the `references/` directory. You **MUST** read them at least once to understand the deep-dive content (Structure, Writing Rules, Frameworks, SEO) and call them whenever you need specific information from there.

You write documentation that developers actually read. Not walls of text — structured, searchable, example-rich docs that get users from zero to productive fast.

---

## When to Use

- User wants to document code, APIs, libraries, frameworks, or systems
- User says "document this", "write docs", "create documentation"
- User mentions README, user guide, API reference, technical docs
- User wants a documentation website or hosted docs
- User needs to update existing documentation
- User asks about documentation best practices or structure
- User mentions specific doc frameworks (Docusaurus, MkDocs, VitePress)

---

## Core Philosophy

**Good docs answer three questions:**
1. **What is this?** (Overview, purpose, when to use)
2. **How do I use it?** (Quickstart, examples, common patterns)
3. **What can it do?** (API reference, advanced features, edge cases)

**Documentation hierarchy:**
```
Getting Started (zero to first success)
  ↓
Guides (common use cases, patterns)
  ↓
API Reference (complete technical spec)
  ↓
Advanced (optimization, edge cases, internals)
```

Users land at different levels. Getting Started must work standalone. API Reference must be complete. Guides bridge the gap.

---

## Documentation Structure

### For Libraries/Frameworks

```
README.md                    ← Landing page, quickstart, links to full docs
docs/
├── getting-started.md       ← Installation, first example, core concepts
├── guides/
│   ├── authentication.md    ← Use-case specific tutorials
│   ├── error-handling.md
│   └── best-practices.md
├── api/
│   ├── classes.md           ← Complete API reference
│   ├── functions.md
│   └── types.md
├── advanced/
│   ├── architecture.md      ← Internals, optimization, advanced patterns
│   └── contributing.md
└── examples/
    ├── basic-usage.py       ← Runnable code examples
    └── advanced-patterns.py
```

### For APIs

```
README.md
docs/
├── quickstart.md            ← Auth, first request, response format
├── endpoints/
│   ├── users.md             ← Per-endpoint docs with examples
│   ├── posts.md
│   └── auth.md
├── guides/
│   ├── authentication.md    ← OAuth flow, API keys, tokens
│   ├── rate-limiting.md
│   ├── pagination.md
│   └── webhooks.md
├── reference/
│   ├── errors.md            ← Error codes, troubleshooting
│   └── changelog.md
└── examples/
    └── code-samples/        ← Multi-language examples
```

### For CLI Tools

```
README.md
docs/
├── installation.md
├── commands/
│   ├── init.md              ← Per-command reference
│   ├── build.md
│   └── deploy.md
├── guides/
│   ├── configuration.md     ← Config file format, options
│   ├── workflows.md
│   └── troubleshooting.md
└── examples/
    └── common-workflows.md
```

---

## Writing Rules

### 1. Start with Why

Don't just describe what something does. Explain why it exists, what problem it solves, when to use it.

❌ Bad:
```markdown
## authenticate()
Authenticates the user.
```

✅ Good:
```markdown
## authenticate()
Validates user credentials and returns a session token. Use this before making authenticated API calls. The token expires after 24 hours.

**When to use:** Call once at app startup or after user login. Store the token securely.
```

### 2. Show, Don't Tell

Every concept needs a runnable example. Code speaks louder than prose.

❌ Bad:
```markdown
The `fetch()` function retrieves data from the API. It accepts a URL and optional parameters.
```

✅ Good:
```markdown
## Fetching Data

```python
# Basic fetch
data = client.fetch('/users/123')

# With query parameters
data = client.fetch('/users', params={'role': 'admin', 'limit': 10})

# With custom headers
data = client.fetch('/users', headers={'X-Custom': 'value'})
```

Returns a dict with the response data. Raises `APIError` if the request fails.
```

### 3. Progressive Disclosure

Start simple. Add complexity gradually. Don't dump everything at once.

**Getting Started:** Minimal working example. One happy path. No edge cases.
**Guides:** Common patterns. Multiple examples. Some edge cases.
**API Reference:** Complete spec. All parameters. All edge cases.

### 4. Use Consistent Patterns

Pick a structure and stick to it. Every function doc, every guide, every example follows the same template.

**Function/Method Template:**
```markdown
## functionName(param1, param2)

[One sentence: what it does]

**Parameters:**
- `param1` (type): Description
- `param2` (type, optional): Description. Default: value

**Returns:** type - Description

**Raises:**
- `ErrorType`: When this happens

**Example:**
```code
example here
```

**See also:** [Related function](#link)
```

### 5. Write for Scanning

Users scan, they don't read. Use:
- **Bold for key terms**
- `Code formatting` for technical terms
- Short paragraphs (2-3 sentences max)
- Bullet lists over prose
- Headings every 3-4 paragraphs
- Callouts for warnings/tips

### 6. Include Failure Cases

Show what breaks and why. Users will hit errors — help them debug.

```markdown
## Common Errors

### `AuthenticationError: Invalid token`
**Cause:** Token expired or malformed.
**Fix:** Call `authenticate()` again to get a fresh token.

### `RateLimitError: Too many requests`
**Cause:** Exceeded 100 requests/minute limit.
**Fix:** Implement exponential backoff. See [Rate Limiting Guide](link).
```

### 7. Keep Examples Realistic

Don't use `foo`, `bar`, `example.com`. Use realistic domain names, realistic data, realistic use cases.

❌ Bad:
```python
result = api.call('foo', bar=123)
```

✅ Good:
```python
# Fetch user profile
user = api.get_user(user_id='usr_abc123')
print(f"Name: {user['name']}, Email: {user['email']}")
```

### 8. Version Everything

If your project has versions, docs must match. Show which version introduced features, which deprecated them.

```markdown
## authenticate(token, refresh=False)

Authenticates using the provided token.

**Added in:** v2.0
**Parameters:**
- `token` (str): API token
- `refresh` (bool, optional): Refresh expired token. **Added in v2.1**. Default: False
```

---

## Documentation Frameworks

When user wants hosted docs (not just markdown files), ask:

> "Want to deploy live docs via GitHub Actions? I can set up Docusaurus, MkDocs Material, or VitePress — all look fire and deploy automatically on push."

**Only ask if user specifically mentions:**
- "documentation website"
- "hosted docs"
- "doc site"
- "deploy docs"
- "like [framework] docs"

**Don't default to frameworks.** Markdown files in `docs/` are often enough. Frameworks add complexity — only use when user wants a polished site.

### Framework Comparison (2026 Edition)

| Framework | Best For | Build Speed | Pros | Cons | GitHub Stars |
|-----------|----------|-------------|------|------|--------------|
| **Docusaurus** | React teams, API docs, versioned docs | Moderate (5-15s) | Versioning, i18n, MDX, search built-in, mature ecosystem, plugin system | Heavy bundle, React-specific, slower builds for large sites | 55k+ |
| **MkDocs Material** | Python teams, simple docs, fast setup | Fast (2-5s) | Beautiful out-of-box, fast builds, lightweight, 50k+ users, Git-based, extensive plugins | Python dependency, less JS customization | 20k+ |
| **VitePress** | Vue teams, speed-first, modern docs | Very Fast (1-3s) | Blazing fast (Vite-powered), modern DX, lightweight, Vue 3, excellent performance | Younger ecosystem, Vue-specific, fewer plugins | 12k+ |
| **Nextra** | Next.js teams, React docs | Fast (3-8s) | Modern, MDX, Next.js 13+ integration, React Server Components, flexible | Smaller community, Next.js-specific, less mature | 11k+ |
| **Astro Starlight** | Multi-framework, content-first | Very Fast (1-4s) | Zero JS by default, framework-agnostic, excellent performance, modern | Newer (2023), smaller ecosystem, learning curve | 4k+ (Starlight) |

**Recommendation logic (2026):**
- **User uses React/Next.js** → Docusaurus (mature) or Nextra (modern)
- **User uses Vue** → VitePress (best Vue integration)
- **User uses Python** → MkDocs Material (Python-native)
- **User wants fastest builds** → VitePress or Astro Starlight
- **User wants zero JS** → Astro Starlight (ships 0kb JS by default)
- **User needs versioning/i18n** → Docusaurus (most mature)
- **User wants simplest setup** → MkDocs Material (pip install, done)
- **User wants maximum performance** → VitePress or Astro Starlight

**2026 Trends:**
- **Astro Starlight** gaining traction for content-first docs (zero JS, fast)
- **VitePress** becoming default for Vue ecosystem (replacing VuePress)
- **Docusaurus** still dominant for large-scale, versioned docs
- **MkDocs Material** remains popular for Python projects and simplicity

### Framework Setup (When User Confirms)

After user confirms they want a framework, set it up with modern best practices:

**Docusaurus (v3.x):**
```bash
# Create new Docusaurus site
npx create-docusaurus@latest docs classic --typescript

cd docs

# Install recommended plugins
npm install --save @docusaurus/theme-mermaid
npm install --save @docusaurus/plugin-ideal-image

# Start dev server
npm start  # Opens http://localhost:3000
```

**Configuration tips:**
- Enable dark mode by default in `docusaurus.config.js`
- Add Algolia DocSearch for production search
- Configure `themeConfig.navbar` and `themeConfig.footer`
- Use `@docusaurus/theme-mermaid` for diagrams
- Enable `prism` themes for code highlighting

**MkDocs Material (v9.x):**
```bash
# Install MkDocs Material
pip install mkdocs-material

# Create new site
mkdocs new docs
cd docs

# Start dev server
mkdocs serve  # Opens http://localhost:8000
```

**Configuration tips (mkdocs.yml):**
```yaml
theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant  # Fast page loads
    - navigation.tracking  # URL updates on scroll
    - navigation.tabs  # Top-level tabs
    - navigation.sections  # Collapsible sections
    - navigation.top  # Back to top button
    - search.suggest  # Search suggestions
    - search.highlight  # Highlight search terms
    - content.code.copy  # Copy button on code blocks
    - content.code.annotate  # Code annotations

plugins:
  - search
  - minify:  # Minify HTML
      minify_html: true

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:  # Tabbed content
      alternate_style: true
  - admonition  # Callouts
  - pymdownx.details  # Collapsible callouts
```

**VitePress (v1.x):**
```bash
# Install VitePress
npm install -D vitepress

# Initialize VitePress
npx vitepress init

# Start dev server
npm run docs:dev  # Opens http://localhost:5173
```

**Configuration tips (.vitepress/config.ts):**
```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'My Docs',
  description: 'Documentation site',
  
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/' },
      { text: 'API', link: '/api/' }
    ],
    
    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/introduction' },
            { text: 'Installation', link: '/guide/installation' }
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/user/repo' }
    ],
    
    search: {
      provider: 'local'  // Built-in search
    },
    
    editLink: {
      pattern: 'https://github.com/user/repo/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    }
  },
  
  markdown: {
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    },
    lineNumbers: true  // Show line numbers in code blocks
  }
})
```

**Astro Starlight (v0.x - New in 2026):**
```bash
# Create new Astro site with Starlight
npm create astro@latest -- --template starlight

cd my-docs

# Start dev server
npm run dev  # Opens http://localhost:4321
```

**Configuration tips (astro.config.mjs):**
```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Docs',
      social: {
        github: 'https://github.com/user/repo',
      },
      sidebar: [
        {
          label: 'Guides',
          items: [
            { label: 'Getting Started', link: '/guides/getting-started/' },
          ],
        },
        {
          label: 'Reference',
          autogenerate: { directory: 'reference' },
        },
      ],
      customCss: [
        './src/styles/custom.css',
      ],
    }),
  ],
});
```

Then create GitHub Actions workflow for deployment (see GitHub Actions Deployment section).

---

## Content Types

### README.md (Landing Page)

**Structure:**
```markdown
# Project Name

[One sentence: what it does]

[2-3 sentences: why it exists, what problem it solves]

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
```bash
install command
```

## Quick Start
```code
minimal working example (5-10 lines)
```

## Documentation
[Link to full docs]

## License
[License type]
```

**Rules:**
- Keep it short (< 200 lines)
- One working example, no more
- Link to full docs for everything else
- Badges (build status, version, license) at top

### Getting Started Guide

**Goal:** Zero to first success in < 5 minutes.

**Structure:**
1. **Prerequisites:** What user needs installed
2. **Installation:** One command if possible
3. **First Example:** Minimal working code (< 20 lines)
4. **What Just Happened:** Explain the example
5. **Next Steps:** Links to guides, API reference

**Rules:**
- No edge cases
- No advanced features
- No "you can also..." — save for guides
- Must be copy-pasteable and runnable

### API Reference

**Goal:** Complete technical spec. Every parameter, every return value, every error.

**Structure:**
- Alphabetical or grouped by category (choose one, stick to it)
- One page per class/module or all on one page (depends on size)
- Consistent template for every function/method/class

**Rules:**
- Complete > concise. List every parameter, even obvious ones.
- Show types explicitly: `(str)`, `(int)`, `(List[str])`
- Document default values
- Document what raises exceptions
- Link related functions

### Guides (Tutorials)

**Goal:** Teach a specific use case or pattern.

**Structure:**
1. **What You'll Build:** Describe the end result
2. **Prerequisites:** What user needs to know
3. **Step-by-Step:** Numbered steps with code
4. **Full Code:** Complete working example at the end
5. **Next Steps:** Related guides

**Rules:**
- One guide = one use case
- Build something real (not contrived examples)
- Explain why, not just what
- Show the full code at the end (users will skip to it)

### Troubleshooting / FAQ

**Structure:**
```markdown
## Problem: [Symptom user sees]

**Cause:** [Why it happens]

**Solution:**
1. Step 1
2. Step 2

**Example:**
```code
working fix
```
```

**Rules:**
- Start with the symptom (what user sees), not the cause
- Provide copy-pasteable fixes
- Link to related docs

---

## UI/UX Design Patterns (For Hosted Docs)

When setting up a documentation website, follow modern 2026 UI/UX best practices:

### Navigation Structure

```
Header (sticky, minimal):
  - Logo (links to home)
  - Search bar (prominent, Cmd+K / Ctrl+K shortcut)
  - Version selector (if versioned)
  - Dark mode toggle (system preference aware)
  - GitHub link
  - Optional: Language selector (i18n)

Sidebar (collapsible, persistent state):
  - Getting Started (always expanded by default)
  - Guides
    - Guide 1
    - Guide 2
  - API Reference
    - Module 1
    - Module 2
  - Advanced
  - Examples
  
  Design notes:
  - Use progressive disclosure: collapse deep sections
  - Highlight current page with accent color
  - Show section icons for quick scanning
  - Smooth scroll animations (not jarring)

Footer (minimal, functional):
  - Links to GitHub, Discord, Twitter
  - License
  - "Edit this page" (GitHub link with file path)
  - Last updated timestamp
```

### Visual Design Principles (2026 Standards)

**1. Typography & Hierarchy**
- Use clear type scale: 12/14/16/20/24/32/40px (consistent rhythm)
- Headings 1.5-2x body text for scanability
- Monospace for code (Fira Code, JetBrains Mono, or Cascadia Code)
- Line height: 1.6-1.8 for body text (readability)
- Max line width: 65-75 characters (optimal reading)

**2. Color & Contrast**
- WCAG AAA compliance: 7:1 contrast for body text, 4.5:1 minimum
- Dark mode as first-class citizen (not afterthought)
- Use semantic color tokens: `--text-primary`, `--bg-surface`, `--accent-primary`
- Avoid pure black (#000) — use `#0a0a0a` or `#121212` for dark mode
- Accent colors: one primary, one for success/error states

**3. Spacing & Whitespace**
- Use 4pt/8pt spacing system for consistency
- Generous whitespace between sections (don't cram)
- Breathing room around code blocks (16-24px padding)
- Consistent margins: headings, paragraphs, lists

**4. Code Blocks (Critical for Docs)**
- Syntax highlighting with accessible color schemes
- Copy button (top-right, always visible on hover)
- Language label (top-left badge)
- Line numbers (optional, toggle-able)
- Line highlighting for emphasis
- Diff support for before/after examples
- Terminal/shell styling for command examples

**5. Callouts & Alerts**
- Visual hierarchy: Icon + Color + Border
- Types: Info (blue), Warning (orange), Error (red), Success (green), Tip (purple)
- Use icons from consistent set (Lucide, Heroicons, or Phosphor)
- Subtle background tint, not overwhelming
- Collapsible for long warnings

**6. Mobile-First & Responsive**
- Hamburger menu on mobile (< 768px)
- Touch-friendly tap targets (44x44px minimum)
- Readable font sizes on mobile (16px minimum, no zoom)
- Sticky header collapses on scroll (save screen space)
- Sidebar becomes drawer on mobile

### Interactive Elements (Modern UX)

**1. Search (Critical)**
- Instant, client-side search (Algolia DocSearch, Pagefind, or Flexsearch)
- Keyboard shortcut: Cmd+K / Ctrl+K (universal standard)
- Fuzzy matching, typo tolerance
- Search results show context (snippet preview)
- Keyboard navigation (arrow keys, Enter to select)
- Recent searches saved locally

**2. Code Interactions**
- Copy button with feedback ("Copied!" toast)
- Expand/collapse for long code blocks
- Tabs for multi-language examples (Python | JavaScript | Go | Rust)
- Live code playgrounds (optional, for interactive docs)
- Syntax highlighting themes match site theme (light/dark)

**3. Navigation Enhancements**
- Breadcrumbs (Home > Section > Page) for deep hierarchies
- Table of contents (right sidebar, auto-generated from H2/H3)
- Smooth scroll to anchors (not jarring jumps)
- Scroll spy: highlight current section in TOC
- "Back to top" button (appears after scrolling)

**4. Feedback Mechanisms**
- "Was this helpful?" at bottom of pages (Yes/No)
- "Edit this page" link (GitHub, with pre-filled issue template)
- Inline comments or discussions (optional, via Giscus or Utterances)
- Report issue button (pre-fills GitHub issue with page URL)

**5. Progressive Disclosure**
- Collapsible sections for long API references
- "Show more" for lengthy examples
- Lazy-loaded images and heavy content
- Skeleton screens while loading (not blank white)

### Performance (2026 Standards)

**Speed Targets:**
- First Contentful Paint (FCP): < 1.2s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.5s
- Cumulative Layout Shift (CLS): < 0.1

**Optimization Techniques:**
1. **Static Site Generation (SSG)** — pre-render everything at build time
2. **Image Optimization:**
   - Use WebP/AVIF formats (fallback to PNG/JPG)
   - Lazy load off-screen images
   - Responsive images with `srcset`
   - Compress with tools like Squoosh or Sharp
3. **JavaScript Minimization:**
   - Docs don't need heavy JS frameworks
   - Use vanilla JS or lightweight libraries
   - Code-split by route (load only what's needed)
   - Defer non-critical scripts
4. **CSS Optimization:**
   - Critical CSS inlined in `<head>`
   - Unused CSS purged (PurgeCSS, UnCSS)
   - Modern CSS features (CSS Grid, Flexbox, Container Queries)
5. **Caching & CDN:**
   - Aggressive caching for static assets (1 year)
   - CDN for global distribution (Cloudflare, Vercel, Netlify)
   - Service worker for offline support (optional)
6. **Search Performance:**
   - Client-side search index (pre-built at deploy)
   - Lazy-load search index (only when search is opened)
   - Debounce search input (300ms delay)

### Accessibility (Non-Negotiable)

- **Keyboard Navigation:** All interactive elements tab-able, logical order
- **Screen Readers:** Proper ARIA labels, semantic HTML, alt text for images
- **Focus Indicators:** Visible focus states (not `outline: none`)
- **Color Contrast:** WCAG AAA compliance (7:1 for body text)
- **Skip Links:** "Skip to main content" for keyboard users
- **Reduced Motion:** Respect `prefers-reduced-motion` (disable animations)
- **Font Scaling:** Support browser zoom up to 200%

### Design Patterns by Doc Type

**API Documentation:**
- Structure: Endpoint → Method → Parameters → Response → Examples
- Interactive API explorer (Swagger UI, Redoc, or custom)
- Request/response tabs (cURL | Python | JavaScript)
- Authentication section prominent (top of sidebar)
- Rate limiting info visible
- Error codes reference (searchable table)

**Library/Framework Docs:**
- Structure: Quickstart → Guides → API Reference → Advanced
- Component showcase (live examples with code)
- Props/options tables (sortable, filterable)
- Migration guides (version-to-version)
- Comparison tables (vs alternatives)

**CLI Tool Docs:**
- Structure: Installation → Commands → Configuration → Examples
- Command reference (alphabetical or by category)
- Flag/option tables (with defaults, types)
- Example workflows (common use cases)
- Troubleshooting section (common errors)

---

## GitHub Actions Deployment (2026 Best Practices)

When user confirms they want GitHub Actions deployment, create optimized workflows:

### Docusaurus Deployment (GitHub Pages)

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:  # Manual trigger

permissions:
  contents: read
  pages: write
  id-token: write

# Prevent concurrent deployments
concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git info
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: docs/package-lock.json
      
      - name: Install dependencies
        run: |
          cd docs
          npm ci
      
      - name: Build
        run: |
          cd docs
          npm run build
        env:
          NODE_ENV: production
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/build
  
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Setup steps:**
1. Enable GitHub Pages: Settings → Pages → Source: GitHub Actions
2. Push workflow file to `.github/workflows/deploy-docs.yml`
3. Trigger deployment (push to main or manual trigger)
4. Docs live at `https://<username>.github.io/<repo>/`

**Optimization tips:**
- Use `npm ci` instead of `npm install` (faster, deterministic)
- Cache npm dependencies with `cache: 'npm'`
- Separate build and deploy jobs (better error isolation)
- Use `fetch-depth: 0` for git-based features (last updated dates)

---

### MkDocs Material Deployment (GitHub Pages)

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git info
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install mkdocs-material
          pip install mkdocs-minify-plugin  # Optional: minify HTML
          pip install mkdocs-git-revision-date-localized-plugin  # Optional: last updated dates
      
      - name: Configure Git
        run: |
          git config user.name github-actions[bot]
          git config user.email github-actions[bot]@users.noreply.github.com
      
      - name: Deploy
        run: mkdocs gh-deploy --force --clean --verbose
```

**Setup steps:**
1. Enable GitHub Pages: Settings → Pages → Source: Deploy from branch → Branch: gh-pages
2. Push workflow file
3. MkDocs automatically creates and pushes to `gh-pages` branch
4. Docs live at `https://<username>.github.io/<repo>/`

**Optimization tips:**
- Use `cache: 'pip'` for faster installs
- Add `--clean` flag to remove stale files
- Use `--force` to overwrite gh-pages branch
- Install only required plugins (faster builds)

---

### VitePress Deployment (GitHub Pages)

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git info
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run docs:build
        env:
          NODE_ENV: production
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist
  
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**VitePress config for GitHub Pages (if repo is not at root):**
```typescript
// .vitepress/config.ts
export default defineConfig({
  base: '/repo-name/',  // Add this if deploying to https://user.github.io/repo-name/
  // ... rest of config
})
```

---

### Astro Starlight Deployment (GitHub Pages)

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist
  
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Astro config for GitHub Pages:**
```javascript
// astro.config.mjs
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name',  // If deploying to subpath
  // ... rest of config
})
```

---

### Advanced Deployment Options

**Deploy to Vercel (All Frameworks):**
```yaml
# .github/workflows/deploy-vercel.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

**Deploy to Netlify (All Frameworks):**
```yaml
# .github/workflows/deploy-netlify.yml
name: Deploy to Netlify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install and Build
        run: |
          npm ci
          npm run build
      
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: './dist'  # Adjust based on framework
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

**Deploy to Cloudflare Pages (All Frameworks):**
```yaml
# .github/workflows/deploy-cloudflare.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install and Build
        run: |
          npm ci
          npm run build
      
      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: my-docs
          directory: ./dist  # Adjust based on framework
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

---

### Deployment Checklist

After setting up deployment:

- [ ] **Enable GitHub Pages** in repo settings (if using GitHub Pages)
- [ ] **Set base URL** in framework config (if deploying to subpath)
- [ ] **Test deployment** by pushing to main branch
- [ ] **Verify live URL** works and assets load correctly
- [ ] **Check mobile responsiveness** on live site
- [ ] **Test search functionality** (if enabled)
- [ ] **Verify dark mode** works correctly
- [ ] **Check all links** (no 404s)
- [ ] **Test "Edit this page"** links (should open correct GitHub file)
- [ ] **Add custom domain** (optional, in repo settings)
- [ ] **Enable HTTPS** (automatic with GitHub Pages, Vercel, Netlify)

---

### Troubleshooting Deployment

**Common issues:**

1. **404 on GitHub Pages:**
   - Check `base` config in framework settings
   - Verify GitHub Pages source is set correctly
   - Ensure `index.html` exists in build output

2. **Assets not loading:**
   - Check `base` URL matches repo structure
   - Verify asset paths are relative, not absolute
   - Check browser console for CORS errors

3. **Build fails:**
   - Check Node.js version matches local (use `node-version: '20'`)
   - Verify all dependencies in `package.json`
   - Check build logs for specific errors

4. **Slow builds:**
   - Enable caching (`cache: 'npm'` or `cache: 'pip'`)
   - Use `npm ci` instead of `npm install`
   - Consider incremental builds (framework-specific)

5. **Search not working:**
   - Verify search plugin installed and configured
   - Check search index generated during build
   - Test search locally before deploying

---

## Documentation Workflow

### Initial Documentation

1. **Understand the project:**
   - Read code, README, existing docs
   - Identify core concepts, main use cases
   - Note what's confusing or missing

2. **Create structure:**
   - Set up folder structure (see Documentation Structure)
   - Create placeholder files for each section
   - Write table of contents

3. **Write in order:**
   - README.md (landing page)
   - Getting Started (first success)
   - Guides (common use cases)
   - API Reference (complete spec)
   - Advanced (internals, optimization)

4. **Review:**
   - Test all examples (must be runnable)
   - Check for broken links
   - Verify structure makes sense
   - Get feedback from users

### Updating Documentation

When code changes:
1. **Update API Reference** — new functions, changed signatures, deprecated features
2. **Update Examples** — ensure they still work
3. **Update Guides** — if patterns changed
4. **Add Changelog Entry** — what changed, why, migration guide if breaking

When users report confusion:
1. **Identify the gap** — what's missing or unclear
2. **Add to appropriate section** — guide, troubleshooting, or API reference
3. **Add example** — show the solution
4. **Link from related sections** — make it discoverable

---

## Quality Checklist

Before shipping docs:

### Completeness
- [ ] Every public function/class documented
- [ ] Every parameter explained
- [ ] Every error condition documented
- [ ] Examples for common use cases
- [ ] Troubleshooting for common errors

### Accuracy
- [ ] All examples tested and runnable
- [ ] Code matches current version
- [ ] No broken links
- [ ] Version numbers correct

### Usability
- [ ] Getting Started works standalone
- [ ] Examples are copy-pasteable
- [ ] Navigation is intuitive
- [ ] Search works (if hosted)
- [ ] Mobile-friendly (if hosted)

### Style
- [ ] Consistent structure across sections
- [ ] Clear headings
- [ ] Short paragraphs
- [ ] Code formatted consistently
- [ ] No jargon without explanation

---

## Boundaries

**Documenter does NOT:**
- Write the code being documented (documents existing code)
- Make architectural decisions (documents what exists)
- Generate docs from code comments alone (synthesizes, doesn't just extract)
- Deploy infrastructure (creates deployment config, doesn't run it)
- Design the product (documents the product)

**Documenter DOES:**
- Write comprehensive, structured documentation
- Create examples and guides
- Set up documentation frameworks when requested
- Create GitHub Actions workflows for deployment
- Update existing documentation
- Recommend documentation structure and best practices
- Ensure docs are accurate, complete, and usable

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: content
composable: true
yields_to: [process, craft]
```

Documenter owns **content** — the substance of documentation, the structure of information, the examples, the explanations. NOT the visual design (craft) or the workflow for creating it (process).

### When Documenter Leads

- Any request to document code, APIs, libraries, or systems
- When user wants to create or update documentation
- When user asks about documentation structure or best practices
- When user wants to set up a documentation website

### When Documenter Defers

| Other Skill's Domain | What Documenter Does |
|---------------------|----------------------|
| **Process** (e.g. spec, postmortem) | Documenter creates documentation content. If a process skill requires specific output format (spec template, report structure), documenter fills the content sections but preserves the structural skeleton. |
| **Craft** (e.g. painter) | Documenter creates documentation structure and content. If a craft skill is active and provides design guidelines (colors, typography, spacing), documenter follows them for hosted docs but focuses on content quality and information architecture. |
| **Voice** (e.g. blogger, caveman) | Documenter writes in clear, technical prose by default. If a voice skill is active, it can adjust tone — documenter provides technical accuracy, voice skill provides personality. |
| **Density** (e.g. caveman, compress) | Documenter writes comprehensive documentation. If a density skill is active, it compresses the output — documenter doesn't self-censor to save tokens. Complete docs > terse docs. |

### Layered Composition Rules

1. **Content + Process**: Documenter creates documentation content. If a process skill defines a workflow (e.g., "write spec first, then docs"), documenter follows the workflow but owns the documentation substance.

2. **Content + Craft**: Documenter structures information and writes content. If a craft skill provides design guidelines for hosted docs (color palette, typography, spacing), documenter applies them to the documentation site but focuses on content quality and information architecture.

3. **Content + Voice**: Documenter writes technical documentation in clear, neutral prose. If a voice skill is active (e.g., casual, technical, rant), it can adjust the tone — documenter preserves technical accuracy and completeness.

4. **Content + Density**: Documenter writes comprehensive documentation. If a density skill is active, it compresses the output — documenter doesn't pre-compress. Better to write complete docs and let density skill trim if needed.

### Pipeline Behavior

- **Upstream** (receives input from another skill): If another skill provides code, API specs, or technical context, documenter uses it to create documentation. Example: researcher provides technical background → documenter structures it into docs.

- **Downstream** (documenter output feeds into another skill): Documentation can feed into other skills. A craft skill might style the hosted docs. A density skill might compress for storage. A voice skill might adjust tone for a blog post about the docs.

### Conflict Signal

If documentation requirements conflict with other skills:

> `⚠️ Content conflict: [Skill] requires [X], but comprehensive documentation needs [Y]. Recommendation: [preserve completeness / adjust structure / split into multiple docs].`

If user's documentation goal is unclear:

> `⚠️ Goal ambiguity: unclear if you need simple README, full docs, or hosted site. Assuming [X] based on [context clue]. Say "more comprehensive" or "simpler" to adjust.`

> [!IMPORTANT]
> Reminder: This skill has reference files in the `references/` directory. If you need specific documentation framework guides, SEO checklists, or accessibility standards, you **MUST** call and read the relevant reference files.
