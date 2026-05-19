# Memory

Persistent context engine. Maintains continuity between turns and sessions.

## Domain

**Process** — management of persistent state, session continuity, user-specific knowledge lifecycle.

## When to Use

**Mandatory startup skill.** Read `memory/data/manifest.json` at start of every complex task.

Also triggers on:
- "I like X", "I hate Y", "Use Z"
- "Here is my key" (secret storage)
- Implicit preference capture

## What It Manages

- **Identity** — who the user is, how they work
- **Preferences** — tooling, coding style, UI, workflow
- **Secrets** — API keys, tokens (vaulted)
- **Daily Journal** — session handovers, decisions, preferences captured
- **Playbooks** — step-by-step guides for fragile procedures

## File Structure

```
memory/data/
├── manifest.json          # Index of everything
├── identity.md            # User profile
├── journal/
│   └── YYYY-MM-DD.md     # Daily entries
├── prefs/
│   ├── tooling.md
│   ├── coding-style.md
│   └── workflow.md
├── vault/
│   └── service-name.enc  # Credentials
└── playbooks/
    └── procedure-name.md
```

## Startup Protocol

1. Read `manifest.json` — get full index
2. Read `identity.md` — know the user
3. Check today's journal — continuity from last session
4. Scan for stale journals — archive if >7 days old

## Composability

```yaml
domain: process
composable: true
yields_to: [voice, craft]
```

## Related Skills

- All skills benefit from memory's context
- Memory stores metadata about other skills' outputs

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/memory/SKILL.md)
