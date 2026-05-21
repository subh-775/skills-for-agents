# Composition

The core power of Skills for Agents: skills compose without breaking each other.

## Composition Modes

### Pipeline (Sequential)

One skill's output feeds into the next. Order matters.

```
/postmortem → /compress
```

Postmortem generates a full incident report, then Compress shrinks it for storage.

**Signal words:** "then", "after that", "once done", "now compress it"

### Layered (Simultaneous)

Multiple skills apply to the same output at once, each handling its domain.

```
/blog technical + /caveman lite
```

Blogger handles voice and content structure. Caveman handles density. Both apply to the same output.

**Signal words:** "in X mode", "using X", "with X"

### Handoff (Delegated)

One skill recognizes it needs another skill's capability and explicitly calls for it.

```
Skill (postmortem): "This incident involved a UI regression.
                     Invoking painter for the visual audit section."
```

### Advisory (Consult)

A skill references another skill's principles without fully activating it.

```
Skill (blogger): Writing a technical blog about UI decisions.
                 References painter's heuristics for accuracy,
                 but voice stays in blogger's domain.
```

## How It Works

Every skill declares:

```yaml
domain: voice | density | craft | process | content
composable: true
yields_to: [list of domains]
```

- **domain** — what this skill controls
- **composable** — whether it works with other skills
- **yields_to** — which domains this skill defers to

When multiple skills are active, each handles its domain and stays out of the others'.

## Precedence Rules

When skills conflict, resolution follows this hierarchy:

1. **Safety/Accuracy** — always wins, no exceptions
2. **User's explicit instruction** — "make it terse" overrides default verbosity
3. **Domain owner** — voice conflicts go to voice skill, density to density skill
4. **Most recently invoked** — tiebreaker for same-domain skills
5. **Specificity** — narrow scope beats broad

## Real-World Examples

### Terse Technical Writing
```bash
/blog technical + /caveman lite
```
Blogger writes technical post, caveman compresses it.

### Production-Ready Code
```bash
/refactor → /harden
```
Refactor establishes structure, harden adds production patterns.

### Comprehensive Docs
```bash
/documenter + /researcher
```
Researcher gathers context, documenter structures it into docs.

### Incident Response
```bash
/postmortem → /compress
```
Postmortem generates report, compress shrinks it for storage.

### ML Research
```bash
/ml-engine + /researcher
```
Researcher finds prior work, ml-engine implements experiments.

## Conflict Resolution Matrix

| Skill A | Skill B | Resolution |
|---------|---------|------------|
| blogger (voice) | caveman (density) | Caveman density wins, blogger voice preserved |
| blogger (voice) | postmortem (process) | Postmortem structure wins, blogger voice within sections |
| painter (craft) | blogger (voice) | Painter advisory for UI accuracy, blogger owns voice |
| caveman (density) | compress (density) | Most recently invoked wins |
| postmortem (process) | compress (density) | Pipeline: postmortem first, compress second |

## The Litmus Test

> Can two skills that have never seen each other's code work together on a single user request without breaking each other's output?

If yes, the protocol works.
