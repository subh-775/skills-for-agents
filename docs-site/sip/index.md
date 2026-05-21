# SIP — Skills Interoperability Protocol

The composability contract that makes multi-skill execution possible.

## Core Principle

> A skill owns its **domain**. It does not own the **conversation**.

When multiple skills are active, each one handles its domain and stays out of the others'. No skill overrides another. No skill assumes it's the only one running.

## Why SIP Exists

Without a protocol, combining AI capabilities means conflict. One skill wants verbose output, another wants terse. One wants formal tone, another wants casual. SIP resolves this by giving each skill a clear domain and explicit composition rules.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Domains** | Non-overlapping areas of ownership (voice, density, craft, process, content) |
| **Composition Modes** | How skills combine: pipeline, layered, handoff, advisory |
| **Precedence Rules** | Conflict resolution hierarchy |
| **Composition Contract** | Rules every skill must follow |

## How It Works

1. Each skill declares its domain in frontmatter
2. Skills declare what they yield to (`yields_to`)
3. When composing, each skill handles its domain
4. Conflicts are resolved by precedence rules
5. Structure from upstream skills is preserved

## Quick Example

```
/blog technical + /caveman lite
```

- **Blogger** (domain: voice) handles tone, personality, content structure
- **Caveman** (domain: density) handles token count, verbosity
- No conflict — each owns its domain

## Learn More

- [Domains](/sip/domains) — The five domain types
- [Composition Modes](/sip/composition) — How skills combine
- [Precedence Rules](/sip/precedence) — Conflict resolution
- [Contract](/sip/contract) — Rules every skill must follow
