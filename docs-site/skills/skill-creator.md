# Skill Creator

Creates new skills, improves existing skills, and ensures SIP compliance across the skill ecosystem. The meta-skill: the skill that builds skills.

## Domain

**Process** — controls the workflow for creating, improving, and auditing skills.

## When to Use

- `/create-skill` or "make a skill", "turn this into a skill", "new skill"
- "improve this skill", "audit this skill", "skill for X"
- User describes a repeatable workflow and says "I wish this was automatic"
- Adding SIP composability to a skill that's missing it
- Discussion about skill architecture or best practices

## The Creation Pipeline

### Phase 1: Capture Intent

Determine where the user is:
- **Vague idea** — "I want a skill for X" -> full interview
- **Workflow in conversation** — "turn what we just did" -> extract from history
- **Existing draft** — "here's my skill, make it better" -> skip to Phase 3
- **Reference skill** — "something like painter but for Y" -> use as template

**Questions to resolve** (extract from context first):
1. What does this skill do? (one sentence)
2. What domain does it own? (voice / density / craft / process / content / analysis / testing)
3. When should it trigger? (be generous)
4. What does it yield to?
5. What's the output format?
6. What are the boundaries?

### Phase 2: Write the Skill

**File structure:**
```
skill-name/
+-- SKILL.md              # Required. Primary instruction surface.
+-- references/           # Optional. Deep-dive docs on demand.
+-- scripts/              # Optional. Helper scripts.
+-- templates/            # Optional. Reusable output templates.
+-- examples/             # Optional. Real-world usage examples.
```

Only `SKILL.md` is required. Put all critical instructions in SKILL.md -- it gets significantly more model attention than reference files.

**SKILL.md anatomy:**
1. **Frontmatter** — name, description, domain, composable, yields_to
2. **Identity** — 1-2 sentence statement
3. **When to Use** — generous trigger list
4. **Core Instructions** — clear, actionable, opinionated
5. **Domain-Specific Sections** — patterns, rules, references
6. **Boundaries** — what it does NOT do
7. **Composability** — SIP compliance section

### Phase 3: SIP Compliance

Every skill must end with a composability section. Non-negotiable.

**yields_to decisions:**
- Voice skill -> `[process, craft]`
- Density skill -> `[process]`
- Process skill -> `[]` (skeleton is sacred)
- Craft skill -> `[voice, process]`
- Safety/accuracy always wins (implicit)

### Phase 4: Review and Iterate

Run 8 audits: position, example, framing, reasoning, token, constraint anchoring, mirror, composition.

## The 12 Instruction Rules

| # | Rule | One-Liner |
|---|------|-----------|
| 1 | Position deliberately | Critical rules at top, restated at bottom |
| 2 | Show, then tell | Lead with examples, follow with principles |
| 3 | Frame positively | "Do X" > "Don't Y" |
| 4 | Include the because | Reasoning makes rules generalizable |
| 5 | Structure is attention | Headers, bullets, tables > prose walls |
| 6 | Group constraints | Related rules together |
| 7 | Earn every token | If deleting doesn't change output, delete it |
| 8 | Imperative voice | "Check X" > "X should be checked" |
| 9 | Anchor constraints | Concrete micro-examples > abstract requirements |
| 10 | Mirror training data | Skill quality = output quality signal |
| 11 | Outcome before process | Define success criteria, not just steps |
| 12 | Self-verification | Add verification for high-cost constraints |

## Size Guidelines

| Type | SKILL.md Lines | What Goes in SKILL.md |
|------|---------------|----------------------|
| **Focused** | 50-150 | Everything |
| **Standard** | 150-400 | Core instructions, key examples, critical rules |
| **Comprehensive** | 400-700 | Core instructions, primary examples, all decision logic |

**Attention hierarchy:** Lines 1-100 = highest attention. Lines 100-300 = strong. Lines 300-600 = moderate. Reference files = loaded on demand.

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

Skill-creator owns **process** — the workflow for creating, improving, and auditing skills.

### When Skill-Creator Leads

- Any request to create a new skill
- Any request to improve or audit an existing skill
- Discussion about skill architecture or SIP compliance
- User describes a workflow and wants to capture it

### When Skill-Creator Defers

| Other Skill's Domain | What Skill-Creator Does |
|---------------------|------------------------|
| **Voice** | Structures the creation process. Voice handles SKILL.md prose tone. |
| **Density** | Generates full drafts. Density compresses explanations, not skill content. |
| **Craft** | Provides structural template. Craft fills design-specific content. |

## Related Skills

- [Planner](./planner) — AGENTS.md follows similar conventions to SKILL.md
- [Refactor](./refactor) — improving existing skills follows similar patterns
- [Researcher](./researcher) — gather best practices for skill design
- [Documenter](./documenter) — documentation patterns inform skill writing

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/skill-creator/SKILL.md) — complete guide with reference files
- [SIP Framework](/guide/sip-framework) — how skills compose
