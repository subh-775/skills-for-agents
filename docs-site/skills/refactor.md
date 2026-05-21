<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Density, Craft</span>
</div>

# Refactor

Restructure messy, monolithic, or legacy codebases into clean, modular structures.

## When to Use

- User says "refactor my project", "clean up my code", "split this file"
- Legacy code needs modernization
- Monolith needs to be broken into modules

## Triggers

```
"refactor my project", "clean up my code", "split this file",
"restructure my files", "modularize this"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Split a monolithic file</div>
<div class="example-desc">Break a 2000-line file into focused modules.</div>

**Before:** `server.js` (2000 lines — routes, middleware, DB, utils)

**After `/refactor`:**
```
server/
├── index.js           # App setup and listen
├── routes/
│   ├── users.js       # User routes
│   ├── auth.js        # Auth routes
│   └── health.js      # Health check
├── middleware/
│   ├── auth.js        # Auth middleware
│   ├── rateLimit.js   # Rate limiting
│   └── errorHandler.js
├── db/
│   ├── connection.js  # DB connection
│   └── models/        # Data models
└── utils/
    └── logger.js      # Structured logging
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Refactor then harden pipeline</div>
<div class="example-desc">Clean structure first, then add production patterns.</div>

```
/refactor → /harden

Refactor splits the monolith into clean modules.
Harden adds: rate limiting per route, graceful shutdown
in index.js, health checks, error boundaries per module,
structured logging, input validation.
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Modernize legacy code</div>
<div class="example-desc">Update old patterns to current idioms.</div>

```
/refactor modernize this callback-based code to async/await

The agent:
- Converts callback chains to async/await
- Replaces var with const/let
- Updates require() to import (if ESM target)
- Extracts reusable utility functions
- Adds proper error handling with try/catch
```
</div>
