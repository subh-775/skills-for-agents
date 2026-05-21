<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Density, Craft</span>
</div>

# Skill Creator

Meta-skill for creating, auditing, and improving other skills. Ensures SIP compliance across the ecosystem.

## When to Use

- User says "make a skill", "turn this into a skill"
- User invokes `/create-skill`
- Auditing existing skills for SIP compliance

## Triggers

```
/create-skill
"make a skill", "turn this into a skill", "create a new skill",
"audit this skill", "improve this skill"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Create a new skill from scratch</div>
<div class="example-desc">Build a skill for generating API documentation from code.</div>

```
/create-skill I want a skill that generates API docs from
source code comments

The agent scaffolds:
skills/api-doc-gen/
├── SKILL.md           # Full skill definition with frontmatter
└── references/
    └── doc-templates.md

SKILL.md includes:
- name: api-doc-gen
- description: triggers and when to use
- domain: content
- composable: true
- yields_to: [process, craft]
- Instructions for parsing code comments, generating
  structured docs, handling multiple languages
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Audit an existing skill</div>
<div class="example-desc">Check a skill for SIP compliance and quality issues.</div>

```
/create-skill audit skills/my-custom-skill/SKILL.md

The agent checks:
- Frontmatter: all required fields present?
- Description under 1000 chars?
- Domain correctly chosen?
- yields_to makes sense?
- Composition contract followed?
- Examples realistic (no foo/bar)?
- Doesn't bleed into other domains?

Output: pass/fail per check with specific fix suggestions.
```
</div>

## Anti-Patterns It Catches

- Missing frontmatter fields
- Description over 1000 characters
- Wrong domain selection
- Missing `yields_to` declaration
- Hardcoded references to specific skills
- Domain boundary violations
