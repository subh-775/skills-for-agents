# Precedence Rules

When skills conflict, resolve with this hierarchy.

## The Rules

### 1. Safety/Accuracy — Always Wins

Implicit and absolute. No skill can override this, even with `yields_to: []`.

If caveman compression would make a security warning ambiguous, expand it. If blogger's casual tone would make a postmortem blame someone, override it.

This rule applies even when a skill declares it yields to nothing.

### 2. User's Explicit Instruction

Second priority. "Write this in caveman mode" means caveman density overrides blogger's default verbosity.

User instructions always take precedence over skill defaults.

### 3. Domain Owner

Each skill is authoritative in its domain:

- Voice conflicts → voice skill wins
- Density conflicts → density skill wins
- Craft conflicts → craft skill wins
- Process conflicts → process skill wins
- Content conflicts → content skill wins

### 4. Most Recently Invoked

If two skills share a domain and no explicit priority, the last one invoked takes precedence.

```bash
/caveman full + /compress lite
# If both are density: compress wins (most recent)
```

### 5. Specificity

A skill with narrow scope beats a skill with broad scope in the overlap area.

## Conflict Resolution Matrix

| Skill A | Skill B | Conflict | Resolution |
|---------|---------|----------|------------|
| blogger (voice) | caveman (density) | Blogger wants 600-1200 words; caveman wants minimal | Caveman density wins, blogger voice/personality preserved in fewer words |
| blogger (voice) | compress (density) | Same as above but for file output | Compress density wins on the file; blogger voice preserved |
| blogger (voice) | postmortem (process) | Blogger hates headers like "Introduction"; postmortem needs structured sections | Postmortem structure wins (process domain), blogger voice applies within sections |
| painter (craft) | blogger (voice) | Blog post about UI decisions | Painter is advisory — provides technical accuracy for UI claims. Blogger owns the voice |
| caveman (density) | compress (density) | Both want to reduce tokens | Most recently invoked wins. If simultaneous: caveman for live responses, compress for files |
| postmortem (process) | compress (density) | Postmortem generates report, compress shrinks it | Pipeline: postmortem first, compress second. Structure preserved, content compressed |
| painter (craft) | postmortem (process) | Postmortem about a UI incident | Painter provides craft expertise for the UI analysis section. Postmortem owns the overall structure |

## Practical Examples

### Example 1: Voice vs Density

```
User: "Write a blog about the outage, keep it short"
```

- Blogger wants to write 600-1200 words with authentic voice
- User says "keep it short" → density instruction
- Resolution: Blogger writes in authentic voice but at compressed length
- Rule applied: #2 (User's explicit instruction) overrides #3 (Domain owner defaults)

### Example 2: Process vs Voice

```
User: "Write a postmortem in my voice"
```

- Postmortem needs structured sections (Timeline, Root Cause, Action Items)
- Blogger wants stream-of-consciousness prose
- Resolution: Postmortem structure wins, blogger voice applies within sections
- Rule applied: #3 (Domain owner — postmortem owns process)

### Example 3: Same Domain Conflict

```
User: "/caveman full + /compress lite"
```

- Both are density skills
- Resolution: Most recently invoked wins (compress lite)
- Rule applied: #4 (Most recently invoked)
