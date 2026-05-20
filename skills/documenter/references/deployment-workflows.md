# Deployment Workflows

Full GitHub Actions YAML configs for deploying documentation sites. Referenced from SKILL.md.

---

## Docusaurus Deployment (GitHub Pages)

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
1. Enable GitHub Pages: Settings -> Pages -> Source: GitHub Actions
2. Push workflow file to `.github/workflows/deploy-docs.yml`
3. Trigger deployment (push to main or manual trigger)
4. Docs live at `https://<username>.github.io/<repo>/`

**Optimization tips:**
- Use `npm ci` instead of `npm install` (faster, deterministic)
- Cache npm dependencies with `cache: 'npm'`
- Separate build and deploy jobs (better error isolation)
- Use `fetch-depth: 0` for git-based features (last updated dates)

---

## MkDocs Material Deployment (GitHub Pages)

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
1. Enable GitHub Pages: Settings -> Pages -> Source: Deploy from branch -> Branch: gh-pages
2. Push workflow file
3. MkDocs automatically creates and pushes to `gh-pages` branch
4. Docs live at `https://<username>.github.io/<repo>/`

**Optimization tips:**
- Use `cache: 'pip'` for faster installs
- Add `--clean` flag to remove stale files
- Use `--force` to overwrite gh-pages branch
- Install only required plugins (faster builds)

---

## VitePress Deployment (GitHub Pages)

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

## Astro Starlight Deployment (GitHub Pages)

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

## Advanced Deployment Options

### Deploy to Vercel (All Frameworks)

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

### Deploy to Netlify (All Frameworks)

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

### Deploy to Cloudflare Pages (All Frameworks)

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

## Deployment Checklist

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

## Troubleshooting Deployment

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
