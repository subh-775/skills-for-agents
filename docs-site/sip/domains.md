# Domains

Every skill has a **domain** — the specific aspect of the output it controls. Domains do NOT overlap.

## The Five Domains

| Domain | Controls | Example Skills |
|--------|----------|----------------|
| **Voice** | Tone, vocabulary, personality, emotional register | Blogger |
| **Density** | Token count, verbosity, compression level | Caveman, Compress |
| **Craft** | Visual design, UI/UX, code quality of frontend output | Painter, Harden |
| **Process** | Workflow steps, templates, structured output format | Postmortem, Memory, ML Engine, Skill Creator, Refactor |
| **Content** | The actual substance being written about | Documenter, Researcher, Learn |

## Domain Rules

1. **No overlap** — if two skills share a domain type, the user's most recent invocation wins
2. **Domain ownership** — each skill is authoritative in its domain
3. **Respect boundaries** — never modify aspects outside your domain

## Domain Boundaries

### Voice Skills
- Control: tone, personality, vocabulary, emotional register
- Don't touch: layout, process steps, token count

### Density Skills
- Control: token count, verbosity, compression level
- Don't touch: tone, personality, factual content

### Craft Skills
- Control: visual design, UI/UX, code quality
- Don't touch: prose that isn't UI copy, workflow steps

### Process Skills
- Control: workflow steps, templates, structured output
- Don't touch: voice, density preferences

### Content Skills
- Control: what is being written about, substance, research
- Don't touch: how it sounds (voice), how long it is (density)

## Future Domains

The protocol supports additional domains for future skills:

- **Analysis** — how to examine or evaluate something
- **Testing** — how to verify correctness

New domains can be added by declaring them in skill frontmatter.
