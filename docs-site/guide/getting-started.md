# Getting Started

Skills for Agents gives your AI coding agent superpowers. 15 composable skills that work together without conflict.

## What is Skills for Agents?

Traditional AI prompts are monolithic — one giant instruction set that tries to do everything. When you need multiple capabilities, they conflict.

Skills for Agents solves this with **domain-specific instruction sets** that compose through the SIP (Skills Interoperability Protocol) framework. Each skill owns one aspect of your agent's behavior:

| Domain | Controls | Example Skills |
|--------|----------|----------------|
| **Voice** | Tone, personality, vocabulary | Blogger |
| **Density** | Token count, verbosity | Caveman, Compress |
| **Craft** | Visual design, UI/UX | Painter, Harden |
| **Process** | Workflow, templates, structure | Postmortem, Planner, Slidify |
| **Content** | Substance being produced | Documenter, Researcher, Learn |

## Quick Install

```bash
# Install all skills to all detected tools
npx skills-for-agents install

# Install to a specific tool
npx skills-for-agents install --tool claude
npx skills-for-agents install --tool cursor
npx skills-for-agents install --tool windsurf
```

That's it. Skills are now available as slash commands in your agent.

## Your First Composition

Once installed, try invoking skills:

```
# Single skill
/caveman full

# Layered composition (both apply simultaneously)
/blog technical + /caveman lite

# Pipeline composition (sequential)
/postmortem → /compress

# Natural language (auto-detected)
"Write a blog about the UI incident, make it terse"
```

## Supported Tools

| Tool | Install Format | Scope |
|------|---------------|-------|
| **Claude Code** | Folder (`.claude/skills/`) | Global or project |
| **Cursor** | Files (`.cursor/rules/`) | Project only |
| **Windsurf** | Files (`.windsurf/rules/`) | Project only |
| **Codex (OpenAI)** | Merged (`codex.md`) | Project only |
| **OpenClaude** | Folder (`.openclaude/skills/`) | Global |
| **Kiro (Amazon)** | Folder (`.kiro/steering/`) | Global or project |
| **Zed** | Merged (`.rules`) | Project only |
| **Cline** | Folder (`.clinerules/`) | Project only |
| **Aider** | Merged (`CONVENTIONS.md`) | Project only |
| **GitHub Copilot** | Merged (`.github/copilot-instructions.md`) | Project only |
| **Continue** | Folder (`.continue/rules/`) | Global or project |

## Next Steps

- [Installation](/guide/installation) — Detailed install options
- [Your First Skill](/guide/first-skill) — Walk through using a skill
- [Composition](/guide/composition) — How skills work together
- [Skills Catalog](/skills/) — Browse all 15 skills
