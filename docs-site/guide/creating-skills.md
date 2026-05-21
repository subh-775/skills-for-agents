# Creating Skills

Build your own composable skill that works with the entire ecosystem.

## Quick Start

Use the Skill Creator meta-skill:

```
/create-skill
```

Or create manually following this guide.

## Skill Structure

```
skills/
  my-skill/
    SKILL.md          # Required: the skill definition
    references/       # Optional: deep-dive content
      detail.md
```

## SKILL.md Template

Every skill starts with YAML frontmatter:

```markdown
---
name: my-skill
description: >
  What this skill does. When to use it. Specific triggers.
  Must be under 1000 characters.
domain: voice | density | craft | process | content
composable: true
yields_to: [list of domain types]
---

# My Skill

[Skill instructions here]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Kebab-case identifier |
| `description` | Yes | What it does + triggers. Under 1000 chars |
| `domain` | Yes | One of: voice, density, craft, process, content |
| `composable` | Yes | `true` if it works with other skills |
| `yields_to` | Yes | Domain types this skill defers to |
| `scope` | No | e.g., "responses" for density skills |

## Domain Selection

Choose the right domain for your skill:

| Domain | Controls | Examples |
|--------|----------|----------|
| **Voice** | Tone, vocabulary, personality | Writing styles, personas |
| **Density** | Token count, verbosity | Compression, expansion |
| **Craft** | Visual design, code quality | UI/UX, code standards |
| **Process** | Workflow, templates, structure | Reports, plans, presentations |
| **Content** | Substance being produced | Documentation, research, learning |

## Composition Contract

Your skill MUST follow these rules:

### 1. Input Agnosticism
Accept output from ANY other skill. Don't assume raw user text.

### 2. Domain Respect
Never modify aspects outside your domain.

### 3. Marker Preservation
Preserve structured output from upstream skills (tables, code blocks, frontmatter).

### 4. Signal Emission
In multi-skill contexts, state which domain you're handling.

### 5. Graceful Degradation
If conflicts arise, apply precedence rules and note what was deferred.

## Writing Effective Triggers

In your `description` field, include specific trigger phrases:

```yaml
description: >
  Ultra-terse communication mode. Cuts token usage 30-95%.
  Use when user says "caveman mode", "talk like caveman",
  "less tokens", "be brief", or invokes /caveman.
```

## Adding References

For complex skills, add a `references/` directory:

```
my-skill/
  SKILL.md
  references/
    deep-dive.md
    examples.md
    patterns.md
```

Reference files are supplementary — the skill must work without them, but they provide depth when needed.

## Testing Your Skill

1. Install locally: `npx skills-for-agents install --project`
2. Test standalone: invoke your skill directly
3. Test composition: combine with 2-3 other skills
4. Test conflicts: try with skills in the same domain
5. Check domain respect: verify it doesn't bleed into other domains

## Submitting

1. Follow the [Contributing Guide](/guide/contributing)
2. Ensure SIP compliance (frontmatter + composition contract)
3. Include examples in your SKILL.md
4. Add a row to SIP's Known Issues section if you found gaps
