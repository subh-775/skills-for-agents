# Composition Contract

Every skill MUST follow these rules to be composable.

## The Five Rules

### 1. Input Agnosticism

A skill must be able to operate on output from ANY other skill. Don't assume your input is raw user text — it might be pre-processed by another skill.

```
# Bad: Assumes input is raw user text
"Take the user's request and..."

# Good: Accepts any input
"Given the current context..."
```

### 2. Domain Respect

Never modify aspects outside your domain:

| Skill Type | Stays In Its Lane |
|------------|-------------------|
| Voice skills | Don't restructure layout or process steps |
| Density skills | Don't change tone, personality, or factual content |
| Craft skills | Don't rewrite prose that isn't UI copy |
| Process skills | Don't impose voice or density preferences |

### 3. Marker Preservation

If a skill produces structured output (tables, code blocks, frontmatter, templates), downstream skills must preserve that structure.

Compress the content INSIDE structures, not the structures themselves.

```
# Input from postmortem:
| Timeline | Event |
|----------|-------|
| 14:00 | Alert fired |
| 14:05 | Team notified |

# Compress must preserve the table structure
# Only compress the content inside cells
```

### 4. Signal Emission

When a skill recognizes it's in a multi-skill context, it should:

- State which domain it's handling
- Note if it's deferring on any aspect
- Flag conflicts it can't resolve alone

```
[density: caveman handling compression]
[voice deferred to blogger]
```

### 5. Graceful Degradation

If a skill can't fully operate alongside another (e.g., caveman + blogger have conflicting density preferences), it should:

1. Identify the conflict
2. Apply the precedence rules
3. Note what was deferred: `[density deferred to caveman]`

## Anti-Patterns

### Don't

- Hardcode references to specific other skills ("if blogger is active, do X")
- Override another skill's domain silently
- Assume you're the only skill running
- Drop structured output from upstream skills
- Refuse to operate because another skill's output "looks weird"
- Double-process (if input is already compressed, don't compress again)

### Do

- Check if your domain is already handled — defer if so
- Preserve structure you didn't create
- State what you're handling and what you're not
- Accept pre-processed input gracefully
- Flag conflicts explicitly rather than silently resolving

## The Litmus Test

> Can two skills that have never seen each other's code work together on a single user request without breaking each other's output?

If yes, the protocol works. If no, one of them is violating the composition contract.
