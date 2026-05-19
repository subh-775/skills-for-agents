# Planner

Project blueprint generator for vibe coding. Produces PRDs, design docs, architecture flows, task breakdowns, and project constitutions before any code is written.

## Domain

**Process** — controls the workflow for generating project specifications and planning documents. The planning skeleton is sacred.

## When to Use

- `/plan [doc]` or "plan this project", "create a PRD", "write a design doc"
- "architecture for", "break this into tasks", "spec this out", "project blueprint"
- User describes an app idea and needs structure before implementation
- Preparing a codebase for AI-agent-assisted development

## Commands

| Command | Output |
|---------|--------|
| `/plan` | Full intake + all 8 docs |
| `/plan prd` | PRD.md only — vision, personas, features, metrics |
| `/plan design` | DESIGN.md only — technical decisions and rationale |
| `/plan arch` | ARCH.md only — diagrams, components, deployment |
| `/plan impl` | IMPL-PLAN.md only — phased vertical slice plan |
| `/plan agents` | AGENTS.md only — AI coding agent config |
| `/plan api` | API.md only — endpoint contracts |
| `/plan db` | DB.md only — schema + ERD |
| `/plan flow` | FLOW.md only — user journeys + diagrams |
| `/plan stack` | Stack recommendation only (no docs) |
| `/plan review` | Review existing plan for gaps |
| `/plan update [doc]` | Revise a specific doc given new context |

## The Planning Pipeline

Documents generate in strict order — each phase builds on the previous:

```
PRD (What) -> DESIGN (How) -> ARCH (Map) -> IMPL-PLAN (Steps) -> AGENTS (Rules) -> API (Spec) -> DB (Data) -> FLOW (UX)
```

**Output structure:**
```
project-root/
+-- AGENTS.md              # Project root (AI agent config)
+-- docs/
    +-- PRD.md             # Product requirements: what & why
    +-- DESIGN.md          # Technical design: decisions & rationale
    +-- ARCH.md            # Architecture: diagrams & components
    +-- IMPL-PLAN.md       # Build plan: phased vertical slices
    +-- API.md             # Endpoint contracts
    +-- DB.md              # Schema + ERD
    +-- FLOW.md            # User journeys & screen inventory
```

## Key Concepts

**Entry Protocol**: Intake Interview (9 questions) -> Stack Recommendation (if needed) -> Document Generation. Extract answers from context before asking.

**Stack Recommendations**: SaaS = Next.js + Supabase, Mobile = Expo + Supabase + Clerk, AI/ML = FastAPI + Postgres, Dashboard = Next.js + Drizzle + Neon, API = Hono/FastAPI + Postgres, Realtime = Next.js + Supabase Realtime.

**Task Sizing**: XS (<1hr), S (2-4hr), M (1-2 days), L (3-5 days), XL (1+ week). Each task touches 1-3 files max, under 2 hours, with testable acceptance criteria.

**Plan Depth**: Quick prototype (5-10 tasks, 50-line AGENTS.md), Side project (15-30 tasks, 100 lines), Production app (30-60+ tasks, 150 lines).

**Living Documents**: Docs are not write-once. After each coding phase, run `/plan update [doc]` to sync with reality.

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

Planner owns **process** — the planning skeleton. Nobody overrides the document pipeline order or required sections.

### When Planner Leads

- Any greenfield project planning
- Feature design before implementation
- Generating context docs for AI coding agents
- PRD/spec creation from scratch

### When Planner Defers

| Other Skill's Domain | What Planner Does |
|---------------------|-------------------|
| **Voice** | Planner structures all documents. Voice adjusts tone within sections. |
| **Craft** | Planner defines UI requirements in PRD. Painter fills design-specific details. |
| **Content** | If planning reveals unknown tech, researcher gathers context. Planner uses findings in DESIGN.md + ARCH.md. |
| **Density** | Planner generates full docs. Density compresses for context window efficiency. |

## Related Skills

- [Refactor](./refactor) — downstream: refactoring feeds into planner's IMPL-PLAN.md
- [Researcher](./researcher) — upstream: research findings feed into stack decisions
- [Painter](./painter) — UI requirements from PRD, painter fills design details
- [Skill Creator](./skill-creator) — AGENTS.md follows similar conventions

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/planner/SKILL.md) — complete planning guide
- [SIP Framework](/guide/sip-framework) — how planner composes
