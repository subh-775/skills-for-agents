# UI/UX Design Patterns for Documentation Sites

Modern 2026 UI/UX best practices for hosted documentation. Referenced from SKILL.md.

---

## Navigation Structure

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

---

## Visual Design Principles (2026 Standards)

### 1. Typography & Hierarchy
- Use clear type scale: 12/14/16/20/24/32/40px (consistent rhythm)
- Headings 1.5-2x body text for scanability
- Monospace for code (Fira Code, JetBrains Mono, or Cascadia Code)
- Line height: 1.6-1.8 for body text (readability)
- Max line width: 65-75 characters (optimal reading)

### 2. Color & Contrast
- WCAG AAA compliance: 7:1 contrast for body text, 4.5:1 minimum
- Dark mode as first-class citizen (not afterthought)
- Use semantic color tokens: `--text-primary`, `--bg-surface`, `--accent-primary`
- Avoid pure black (#000) -- use `#0a0a0a` or `#121212` for dark mode
- Accent colors: one primary, one for success/error states

### 3. Spacing & Whitespace
- Use 4pt/8pt spacing system for consistency
- Generous whitespace between sections (don't cram)
- Breathing room around code blocks (16-24px padding)
- Consistent margins: headings, paragraphs, lists

### 4. Code Blocks (Critical for Docs)
- Syntax highlighting with accessible color schemes
- Copy button (top-right, always visible on hover)
- Language label (top-left badge)
- Line numbers (optional, toggle-able)
- Line highlighting for emphasis
- Diff support for before/after examples
- Terminal/shell styling for command examples

### 5. Callouts & Alerts
- Visual hierarchy: Icon + Color + Border
- Types: Info (blue), Warning (orange), Error (red), Success (green), Tip (purple)
- Use icons from consistent set (Lucide, Heroicons, or Phosphor)
- Subtle background tint, not overwhelming
- Collapsible for long warnings

### 6. Mobile-First & Responsive
- Hamburger menu on mobile (< 768px)
- Touch-friendly tap targets (44x44px minimum)
- Readable font sizes on mobile (16px minimum, no zoom)
- Sticky header collapses on scroll (save screen space)
- Sidebar becomes drawer on mobile

---

## Interactive Elements (Modern UX)

### 1. Search (Critical)
- Instant, client-side search (Algolia DocSearch, Pagefind, or Flexsearch)
- Keyboard shortcut: Cmd+K / Ctrl+K (universal standard)
- Fuzzy matching, typo tolerance
- Search results show context (snippet preview)
- Keyboard navigation (arrow keys, Enter to select)
- Recent searches saved locally

### 2. Code Interactions
- Copy button with feedback ("Copied!" toast)
- Expand/collapse for long code blocks
- Tabs for multi-language examples (Python | JavaScript | Go | Rust)
- Live code playgrounds (optional, for interactive docs)
- Syntax highlighting themes match site theme (light/dark)

### 3. Navigation Enhancements
- Breadcrumbs (Home > Section > Page) for deep hierarchies
- Table of contents (right sidebar, auto-generated from H2/H3)
- Smooth scroll to anchors (not jarring jumps)
- Scroll spy: highlight current section in TOC
- "Back to top" button (appears after scrolling)

### 4. Feedback Mechanisms
- "Was this helpful?" at bottom of pages (Yes/No)
- "Edit this page" link (GitHub, with pre-filled issue template)
- Inline comments or discussions (optional, via Giscus or Utterances)
- Report issue button (pre-fills GitHub issue with page URL)

### 5. Progressive Disclosure
- Collapsible sections for long API references
- "Show more" for lengthy examples
- Lazy-loaded images and heavy content
- Skeleton screens while loading (not blank white)

---

## Performance (2026 Standards)

### Speed Targets
- First Contentful Paint (FCP): < 1.2s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.5s
- Cumulative Layout Shift (CLS): < 0.1

### Optimization Techniques
1. **Static Site Generation (SSG)** -- pre-render everything at build time
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

---

## Accessibility (Non-Negotiable)

- **Keyboard Navigation:** All interactive elements tab-able, logical order
- **Screen Readers:** Proper ARIA labels, semantic HTML, alt text for images
- **Focus Indicators:** Visible focus states (not `outline: none`)
- **Color Contrast:** WCAG AAA compliance (7:1 for body text)
- **Skip Links:** "Skip to main content" for keyboard users
- **Reduced Motion:** Respect `prefers-reduced-motion` (disable animations)
- **Font Scaling:** Support browser zoom up to 200%

---

## Design Patterns by Doc Type

### API Documentation
- Structure: Endpoint -> Method -> Parameters -> Response -> Examples
- Interactive API explorer (Swagger UI, Redoc, or custom)
- Request/response tabs (cURL | Python | JavaScript)
- Authentication section prominent (top of sidebar)
- Rate limiting info visible
- Error codes reference (searchable table)

### Library/Framework Docs
- Structure: Quickstart -> Guides -> API Reference -> Advanced
- Component showcase (live examples with code)
- Props/options tables (sortable, filterable)
- Migration guides (version-to-version)
- Comparison tables (vs alternatives)

### CLI Tool Docs
- Structure: Installation -> Commands -> Configuration -> Examples
- Command reference (alphabetical or by category)
- Flag/option tables (with defaults, types)
- Example workflows (common use cases)
- Troubleshooting section (common errors)
