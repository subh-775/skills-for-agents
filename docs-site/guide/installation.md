# Installation

## Via npx (Recommended)

```bash
npx skills-for-agents install
```

This auto-detects installed AI coding tools and installs all skills.

### Target Specific Tools

```bash
# Single tool
npx skills-for-agents install --tool claude

# Multiple tools
npx skills-for-agents install --tool cursor --tool windsurf

# New tools
npx skills-for-agents install --tool kiro --global
npx skills-for-agents install --tool zed --project
npx skills-for-agents install --tool aider --project
npx skills-for-agents install --tool copilot --project

# All supported tools
npx skills-for-agents install --all
```

### Install Scope

```bash
# Global install (default for Claude Code, OpenClaude)
npx skills-for-agents install

# Project-level install
npx skills-for-agents install --project

# Force overwrite existing files
npx skills-for-agents install --force
```

### Selective Install

```bash
# Install only specific skills
npx skills-for-agents install --only caveman,blogger,slidify

# List available skills
npx skills-for-agents list
```

## Via Git Clone

```bash
git clone https://github.com/IsNoobgrammer/skills-for-agents.git
```

Each skill is a self-contained folder with a `SKILL.md` file. Point your agent to load these files as system prompts.

## Installation Paths

| Tool | Global Path | Project Path | Format |
|------|------------|--------------|--------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Folder |
| Cursor | — | `.cursor/rules/` | Files |
| Windsurf | — | `.windsurf/rules/` | Files |
| Codex | — | `codex.md` | Merged |
| OpenClaude | `~/.openclaude/skills/` | — | Folder |
| Kiro | `~/.kiro/steering/` | `.kiro/steering/` | Folder |
| Zed | — | `.rules` | Merged |
| Cline | — | `.clinerules/` | Folder |
| Aider | — | `CONVENTIONS.md` | Merged |
| Copilot | — | `.github/copilot-instructions.md` | Merged |
| Continue | `~/.continue/rules/` | `.continue/rules/` | Folder |

## Verify Installation

```bash
npx skills-for-agents list
```

Should output all 15 skills with their domains and descriptions.

## Updating

```bash
# Re-run install with force flag
npx skills-for-agents install --force
```

## Troubleshooting

**"No AI coding tools detected"**

Use `--tool <name>` to specify manually:
```bash
npx skills-for-agents install --tool claude --project
```

**Skills not appearing as commands**

Ensure your agent loads skills from the correct directory. Check your tool's configuration for custom skill paths.
