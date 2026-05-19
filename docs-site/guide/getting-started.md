# Getting Started

Skills are composable instruction sets for AI agents. Each skill owns one domain and works alongside other skills without conflict.

## What Are Skills?

A skill is a **dense compression of expertise into instructions an AI can follow**. Instead of one giant prompt that tries to do everything, you have focused skills that:

1. **Own a domain** — voice, density, craft, process, content
2. **Compose cleanly** — work together without breaking each other
3. **Explain reasoning** — teach the AI *why*, not just *what*

## Installation

### Via npx (recommended)

Install all skills to your AI coding tools with a single command:

```bash
npx antigravity-skills install
```

This auto-detects which tools you have installed and copies skills to the right places.

**Target a specific tool:**

```bash
npx antigravity-skills install --tool claude
npx antigravity-skills install --tool cursor
npx antigravity-skills install --tool windsurf
npx antigravity-skills install --tool codex
npx antigravity-skills install --tool antigravity
```

**Install to current project:**

```bash
npx antigravity-skills install --project
```

This creates tool-specific files in your project directory:
- **Cursor**: `.cursor/rules/*.md`
- **Windsurf**: `.windsurf/rules/*.md`
- **Codex**: `codex.md` (merged)
- **Claude Code**: `.claude/skills/*/SKILL.md`

**Install specific skills only:**

```bash
npx antigravity-skills install --only caveman,blogger,slidify
```

**List available skills:**

```bash
npx antigravity-skills list
```

### Via git clone (manual)

```bash
git clone https://github.com/IsNoobgrammer/skills-for-agents.git
```

Each skill is a self-contained folder with a `SKILL.md` file. Point your agent to load these files as system prompts.

### Multi-Tool Support

| Tool | Global Install | Project Install | Format |
|------|:---:|:---:|--------|
| Antigravity (OpenClaude) | `~/.openclaude/skills/` | — | Full skill folders |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Full skill folders |
| Cursor | — | `.cursor/rules/` | Individual `.md` files |
| Windsurf | — | `.windsurf/rules/` | Individual `.md` files |
| Codex | — | `codex.md` | Single merged file |

## Your First Skill

Let's use the **caveman** skill — ultra-terse communication that cuts token usage ~75%.

### Invoke the Skill

```
/caveman full
```

### What Happens

The AI now speaks in compressed mode:

**Before caveman:**
> "Sure! I'd be happy to help you with that. The issue you're experiencing is likely caused by a misconfiguration in your authentication middleware. Let me explain what's happening..."

**After caveman:**
> "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"

### Intensity Levels

Caveman has 4 levels:

| Level | Reduction | Use When |
|-------|-----------|----------|
| `lite` | ~30% | Light cleanup, keep readability |
| `full` | ~50% | General compression, good balance |
| `ultra` | ~75% | Maximum compression, telegraphic style |

```
/caveman lite   # Professional but tight
/caveman full   # Classic caveman (default)
/caveman ultra  # Extreme abbreviation
```

## Composing Skills

Skills work together. Here's how:

### Layered Composition (Simultaneous)

Multiple skills apply to the same output at once:

```
/blog technical + /caveman lite
```

Result: Blogger writes a technical post, caveman compresses it. Both active simultaneously.

### Pipeline Composition (Sequential)

One skill's output feeds into the next:

```
/postmortem → /compress
```

Result: Postmortem generates a report, compress shrinks it.

### Natural Language

You don't always need explicit commands:

```
"Write a blog about the UI incident, make it terse"
```

The AI detects:
- "blog" → blogger skill (voice)
- "terse" → caveman skill (density)
- "UI incident" → postmortem skill (content)

All three compose automatically.

## Domain Types

Every skill owns exactly one domain:

| Domain | Controls | Example Skills |
|--------|----------|----------------|
| **Voice** | Tone, personality, vocabulary | Blogger |
| **Density** | Token count, verbosity | Caveman, Compress |
| **Craft** | Visual design, code quality | Painter, Harden |
| **Process** | Workflow steps, templates | Memory, Postmortem, Refactor |
| **Content** | Substance being produced | Documenter, Researcher |

When skills from different domains compose, they don't conflict. When skills from the same domain compose, the most recent wins (or you can specify precedence).

## Conflict Resolution

What happens when two skills want different things?

**Example:** Blogger wants 600-1200 words. Caveman wants minimal output.

**Resolution:** Caveman (density) wins. Blogger's voice and personality are preserved, but in fewer words.

**Why?** The [SIP Framework](/guide/sip-framework) defines precedence rules. Each skill declares what it yields to.

## Next Steps

1. **[Learn SIP Framework](/guide/sip-framework)** — understand how skills compose
2. **[Explore Skills](/skills/)** — see what's available
3. **[Create Your Own](/guide/creating-skills)** — build custom skills

## Quick Reference

### Invoke a Skill

```
/skill-name [options]
```

### Compose Skills

```
/skill1 + /skill2           # Layered (simultaneous)
/skill1 → /skill2           # Pipeline (sequential)
"natural language request"  # Auto-detect
```

### Stop a Skill

```
stop skill-name
```

### List Active Skills

```
list skills
```

## Common Patterns

### Terse Technical Writing

```
/blog technical + /caveman lite
```

### Production-Ready Code

```
/refactor → /harden
```

### Comprehensive Docs

```
/documenter + /researcher
```

### Incident Response

```
/postmortem → /compress
```

### ML Research

```
/ml-engine + /researcher
```

## Troubleshooting

### Skill Not Triggering

Check the skill's `description` field in its frontmatter. It lists trigger phrases. If your request doesn't match, the skill won't activate.

### Skills Conflicting

Check their domains. If both are `voice` or both are `density`, they'll conflict. Specify which one wins:

```
/skill1 (primary) + /skill2
```

### Output Too Verbose

Add a density skill:

```
your-request + /caveman lite
```

### Output Too Terse

Remove density skills or use `stop caveman`.

## Best Practices

1. **Start simple** — use one skill at a time until you understand it
2. **Compose gradually** — add skills one by one, test each addition
3. **Read the skill docs** — each skill has specific commands and options
4. **Use natural language** — explicit commands are optional, natural requests work
5. **Check domains** — understand what each skill controls to avoid conflicts

## Resources

- [SIP Framework](/guide/sip-framework) — composability rules
- [Creating Skills](/guide/creating-skills) — build your own
- [Best Practices](/reference/best-practices) — advanced patterns
- [GitHub](https://github.com/IsNoobgrammer/skills-for-agents) — source code
