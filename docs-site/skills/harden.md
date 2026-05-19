# Harden

Production-harden code for 1M+ users. Adds caching, rate limiting, connection pooling, graceful shutdown.

## Domain

**Craft** — technical reliability and infrastructure patterns.

## When to Use

- "harden my code", "prepare for launch", "make it scalable"
- "add caching/rate limiting"
- Production readiness needed

## What It Adds

- Connection pooling
- Caching layers
- Rate limiting
- Graceful shutdown (SIGTERM handling)
- Health check endpoints (`/health`)
- Structured logging
- Error boundaries
- Async I/O optimization

## Prerequisite

**Codebase must be modular.** If messy, use [Refactor](./refactor) first.

## Workflow

1. **Audit** — scan for scale/reliability gaps
2. **Plan** — list files to modify, patterns to add
3. **Execute** — inject patterns (preserve structure)
4. **Verify** — checklist confirms production readiness

## Composability

```yaml
domain: craft
composable: true
yields_to: [process]
```

## Related Skills

- [Refactor](./refactor) — establishes structure first
- [Painter](./painter) — craft for visual, harden for infrastructure

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/harden/SKILL.md)
