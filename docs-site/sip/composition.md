# Composition Modes

When the user invokes or triggers multiple skills, they compose in one of four modes.

## Mode A: Pipeline (Sequential)

One skill's output feeds into the next. Order matters.

```
User: "Write a postmortem, then compress it"
Flow: postmortem → generates report → compress → shrinks the report
```

**Signal words:** "then", "after that", "once done", "now compress it"

### Example

```bash
/postmortem → /compress
```

Postmortem generates a full incident report with root cause analysis, action items, and timeline. Then Compress shrinks it for storage or distribution.

## Mode B: Layered (Simultaneous)

Multiple skills apply to the same output at once, each handling its domain.

```
User: "Write a blog post in caveman mode"
Flow: blogger handles voice + content structure
      caveman handles density
      Both apply to the same output
```

**Signal words:** "in X mode", "using X", "with X", simultaneous invocation

### Example

```bash
/blog technical + /caveman lite
```

Blogger writes with authentic voice and content structure. Caveman applies lite compression to reduce verbosity. Both operate on the same output simultaneously.

## Mode C: Handoff (Delegated)

One skill recognizes it needs another skill's capability and explicitly calls for it.

```
Skill (postmortem): "This incident involved a UI regression.
                     Invoking painter for the visual audit section."
```

**Signal:** Skill detects content outside its domain that another skill could handle better.

### When Handoff Happens

- A process skill encounters visual/design content → hands off to craft
- A content skill needs specific voice → hands off to voice
- A craft skill needs structured output → hands off to process

## Mode D: Advisory (Consult)

A skill references another skill's principles without fully activating it.

```
Skill (blogger): Writing a technical blog about UI decisions.
                 References painter's heuristics for accuracy,
                 but voice stays in blogger's domain.
```

**Signal:** Domain overlap in content (not output style).

### Advisory vs Handoff

| Aspect | Advisory | Handoff |
|--------|----------|---------|
| Activation | Partial — references principles | Full — delegates section |
| Control | Original skill retains control | Receiving skill takes control |
| Scope | Background influence | Specific content section |

## Syntax

```
# Pipeline
/skill1 → /skill2

# Layered
/skill1 + /skill2

# Natural language (parsed by context)
"Write a blog in caveman mode"
```

The `→` operator means pipeline. The `+` operator means layered. Natural language is parsed by context.
