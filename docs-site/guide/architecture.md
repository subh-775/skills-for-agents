# Architecture

How Skills for Agents is built and how the pieces fit together.

## Project Structure

```
skills-for-agents/
├── bin/
│   └── cli.js              # npx entry point
├── src/
│   └── installer.js         # Core installation logic
├── skills/
│   ├── PROTOCOL.md          # SIP specification
│   ├── blogger/             # Voice domain
│   ├── caveman/             # Density domain
│   ├── compress/            # Density domain
│   ├── painter/             # Craft domain
│   ├── harden/              # Craft domain
│   ├── memory/              # Process domain
│   ├── ml-engine/           # Process domain
│   ├── planner/             # Process domain
│   ├── postmortem/          # Process domain
│   ├── refactor/            # Process domain
│   ├── skill-creator/       # Process domain
│   ├── slidify/             # Process domain
│   ├── documenter/          # Content domain
│   ├── learn/               # Content domain
│   └── researcher/          # Content domain
├── docs-site/               # VitePress documentation
├── .github/workflows/
│   ├── deploy-docs.yml      # Docs deployment
│   └── publish-npm.yml      # npm publishing
├── package.json
├── PROTOCOL.md              # SIP specification (root copy)
└── README.md
```

## CLI Architecture

The CLI (`bin/cli.js`) is a thin entry point that:

1. Parses command-line arguments
2. Delegates to `installer.js` for the actual work

### Installation Modes

The installer supports three formats depending on the target tool:

| Format | Tool | How It Works |
|--------|------|-------------|
| **folder** | Claude Code, OpenClaude | Copies entire skill directories |
| **files** | Cursor, Windsurf | Copies SKILL.md files as individual `.md` files |
| **merged** | Codex | Merges all skills into a single `codex.md` |

### Tool Detection

Each tool has a `detect()` function that checks for tool-specific markers:

```javascript
claude: {
  detect() {
    return fs.existsSync('.claude') || fs.existsSync(path.join(HOME, '.claude'));
  }
}
```

## Skill Format

Every skill is a Markdown file with YAML frontmatter. The frontmatter declares metadata for the SIP framework:

```yaml
---
name: skill-name
description: What it does and when to trigger
domain: voice | density | craft | process | content
composable: true
yields_to: [domains]
---
```

The body contains the actual instructions loaded as a system prompt.

## SIP Framework

The Skills Interoperability Protocol is defined in `PROTOCOL.md` at the skills root. It's automatically copied during installation so every agent has access to the composition rules.

Key components:
- **Domains** — non-overlapping ownership areas
- **Composition Modes** — pipeline, layered, handoff, advisory
- **Precedence Rules** — conflict resolution hierarchy
- **Composition Contract** — rules every skill must follow

## Deployment

- **Docs**: VitePress site deployed to GitHub Pages via GitHub Actions
- **npm**: Auto-published on push to main with automatic version bumping
- **Skills**: Distributed as Markdown files via npm package
