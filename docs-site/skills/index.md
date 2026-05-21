# Skills Catalog

15 composable skills organized by domain. Each skill is a self-contained instruction set that works with any LLM agent.

## Voice

| Skill | Description | Triggers |
|-------|-------------|----------|
| [**Blogger**](/skills/blogger) | Authentic personal-voice writing. Raw, unpolished, stream-of-consciousness prose. | `/blog`, "write a blog", "write like me" |

## Density

| Skill | Description | Triggers |
|-------|-------------|----------|
| [**Caveman**](/skills/caveman) | Ultra-terse communication. Cuts token usage ~75%. | `/caveman`, "talk like caveman", "less tokens" |
| [**Compress**](/skills/compress) | File compression. 4 intensity levels. Preserves all meaning. | `/compress`, "compress this", "reduce tokens" |

## Craft

| Skill | Description | Triggers |
|-------|-------------|----------|
| [**Painter**](/skills/painter) | Max pro UI/UX design. Animation, color, typography, accessibility. 20+ commands. | `/painter`, "make it look pro", "fix the ui" |
| [**Harden**](/skills/harden) | Production-harden code for 1M+ users. Caching, rate limiting, graceful shutdown. | "harden my code", "prepare for launch", "make it scalable" |

## Process

| Skill | Description | Triggers |
|-------|-------------|----------|
| [**Memory**](/skills/memory) | Persistent context engine. Daily journal rotation, manifest indexing, identity tracking. | Startup (mandatory), "I like X", "Here is my key" |
| [**ML Engine**](/skills/ml-engine) | TPU-first ML research. Distributed training, MoE, Pallas kernels. 12+ commands. | `/ml`, TPU mentions, distributed training |
| [**Planner**](/skills/planner) | Project plans with PRDs, design docs, architecture flows, task breakdowns. | `/plan`, "create a PRD", "design the architecture" |
| [**Postmortem**](/skills/postmortem) | Blameless incident documentation. 5 Whys, action items. | `/postmortem`, "incident review", "what broke and why" |
| [**Refactor**](/skills/refactor) | Restructure messy codebases into clean, modular architecture. | "refactor my project", "clean up my code", "split this file" |
| [**Skill Creator**](/skills/skill-creator) | Meta-skill for creating, auditing, and improving other skills. | `/create-skill`, "make a skill", "turn this into a skill" |
| [**Slidify**](/skills/slidify) | End-to-end PowerPoint generator. JSON specs, templates, auto speaker notes. | `/slidify`, "make a presentation", "create slides", "generate pptx" |

## Content

| Skill | Description | Triggers |
|-------|-------------|----------|
| [**Documenter**](/skills/documenter) | Comprehensive documentation. Examples, guides, API references. | "document this", "write docs", "create documentation" |
| [**Learn**](/skills/learn) | Structured study plans, topic guides, exam prediction, and active recall. | `/learn`, "teach me X", "how do I learn Y" |
| [**Researcher**](/skills/researcher) | Deep web research. Diverse sources, cross-referencing, synthesis. | "research X", "find info about Y", "what's the latest on Z" |

## Installation

```bash
# Install all skills
npx skills-for-agents install

# Install specific skills
npx skills-for-agents install --only caveman,blogger,slidify
```

## Composition

Skills compose without conflict through the SIP framework. See [Composition](/guide/composition) for details.
