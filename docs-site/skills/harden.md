<div class="domain-header">
  <span class="skill-badge craft">Craft</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Process</span>
</div>

# Harden

Production-harden code for 1M+ users. Adds caching, rate limiting, graceful shutdown, error handling, and scalability patterns.

## When to Use

- User says "harden my code", "prepare for launch", "make it scalable"
- Code needs caching, rate limiting, or error handling
- Preparing for high traffic

## Triggers

```
"harden my code", "prepare for launch", "add caching",
"add rate limiting", "make it production-ready"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Harden an API endpoint</div>
<div class="example-desc">Add production patterns to a simple Express endpoint.</div>

**Before:**
```javascript
app.get('/api/users/:id', async (req, res) => {
  const user = await db.findUser(req.params.id);
  res.json(user);
});
```

**After `/harden`:**
```javascript
const rateLimit = require('express-rate-limit');
const cache = new NodeCache({ stdTTL: 60 });

const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100 });

app.get('/api/users/:id', limiter, async (req, res) => {
  const cacheKey = `user:${req.params.id}`;
  const cached = cache.get(cacheKey);
  if (cached) return res.json(cached);

  try {
    const user = await db.findUser(req.params.id);
    if (!user) return res.status(404).json({ error: 'User not found' });
    cache.set(cacheKey, user);
    res.json(user);
  } catch (err) {
    logger.error('User fetch failed', { id: req.params.id, err });
    res.status(500).json({ error: 'Internal server error' });
  }
});
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Refactor then harden</div>
<div class="example-desc">Clean up messy code, then add production patterns.</div>

```
/refactor → /harden

Refactor splits a 2000-line monolith into focused modules.
Harden adds: rate limiting per module, graceful shutdown
handlers, health check endpoints, structured logging,
input validation, and error boundaries.
```
</div>

## What It Adds

| Pattern | Description |
|---------|-------------|
| **Caching** | In-memory, Redis, CDN, cache invalidation |
| **Rate Limiting** | Token bucket, sliding window, per-user limits |
| **Graceful Shutdown** | Signal handling, connection draining, cleanup |
| **Error Handling** | Retry logic, circuit breakers, fallbacks |
| **Monitoring** | Health checks, metrics, logging |
| **Security** | Input validation, CORS, CSP, auth |
