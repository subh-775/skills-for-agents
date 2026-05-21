# Contributing

We welcome contributions to the Skills for Agents ecosystem.

## Ways to Contribute

- **Create new skills** — add capabilities to the ecosystem
- **Improve existing skills** — better instructions, more examples, fix edge cases
- **Fix bugs** — in the CLI, installer, or documentation
- **Enhance docs** — improve guides, add examples, fix typos
- **Build tooling** — integrations, validators, generators

## Creating a New Skill

1. Use the Skill Creator: `/create-skill`
2. Or manually create a folder under `skills/` with a `SKILL.md`
3. Follow the [Creating Skills](/guide/creating-skills) guide
4. Ensure SIP compliance

## Development Setup

```bash
# Clone the repo
git clone https://github.com/IsNoobgrammer/skills-for-agents.git
cd skills-for-agents

# Install docs dependencies
cd docs-site && npm install

# Run docs locally
npm run dev
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b my-skill`
3. Make your changes
4. Test your skill with multiple other skills
5. Submit a pull request

### PR Guidelines

- One skill per PR (for new skills)
- Include examples in SKILL.md
- Test composition with at least 2 other skills
- Update SIP's Known Issues section if you found protocol gaps

## Skill Quality Checklist

Before submitting a new skill:

- [ ] Frontmatter has all required fields
- [ ] Description is under 1000 characters
- [ ] Domain is correctly chosen
- [ ] `yields_to` makes sense for the domain
- [ ] Composition contract rules are followed
- [ ] Examples are realistic (no foo/bar)
- [ ] Works standalone and in composition
- [ ] Doesn't bleed into other domains

## Code Style

- JavaScript: CommonJS modules, no build step
- Markdown: Follow existing skill format
- YAML frontmatter: All required fields present

## Reporting Issues

Found a bug or have a suggestion? Open an issue on [GitHub](https://github.com/IsNoobgrammer/skills-for-agents/issues).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
