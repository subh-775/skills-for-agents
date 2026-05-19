# Documenter

Comprehensive documentation engine. Creates extensive, well-structured docs with examples, guides, and API references.

## Domain

**Content** — substance of documentation, structure of information, examples, explanations.

## When to Use

- "document this", "write docs", "create documentation"
- "API docs", "README", "user guide", "technical docs"
- "doc site", "documentation website"

## What It Creates

- README.md (landing page)
- Getting Started guides
- API Reference (complete spec)
- Tutorials and guides
- Troubleshooting / FAQ
- Documentation websites (optional)

## Documentation Frameworks

When user wants hosted docs:

- **Docusaurus** — React teams, versioned docs
- **MkDocs Material** — Python teams, fast setup
- **VitePress** — Vue teams, blazing fast
- **Astro Starlight** — Zero JS, framework-agnostic

## Commands

```bash
/documenter              # Create docs structure
/documenter [framework]  # Setup doc site with framework
```

## Composability

```yaml
domain: content
composable: true
yields_to: [process, craft]
```

## Related Skills

- [Researcher](./researcher) — gathers context for docs
- [Painter](./painter) — styles hosted docs
- [Compress](./compress) — shrinks docs for storage

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/documenter/SKILL.md)
