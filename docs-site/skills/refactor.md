# Refactor

Refactors messy, monolithic, or legacy codebases into clean, modular structures. FAANG-level staff engineer reviewing your code.

## Domain

**Process** — controls structural organization and architectural skeleton of the codebase. The folder structure is sacred.

## When to Use

- "refactor my project", "clean up my code", "split this file", "restructure my files"
- "my code is a mess" or "this file is too large (300+ lines)"
- Moving from monolithic single-file to proper project structure
- Extracting duplicated logic into reusable components
- Always use before `harden` if code is not yet modular

## The 4 Phases

### Phase 1: Project Health Report

Produces a report including:
- **Stack Detected** — frameworks and database
- **Files Needing Split** — oversized files with line counts
- **Risks** — scale and maintenance risks

Confirm with user before proceeding.

### Phase 2: Refactoring Plan

Produces a full plan including:
- **New Folder Structure** — visualization of target layout
- **File-by-File Mapping** — original file -> new file(s)
- **Reasoning** — why these specific changes

### Phase 3: Code Execution

Outputs refactored files in full. Uses index files for barrel exports. Ensures all imports are updated. Removes unused imports and dead code.

### Phase 4: Verification Checklist

Confirms:
- All original routes and UI components preserved
- No file exceeds the 300-line limit
- No business logic lost or rewritten

## Core Rules

1. **Analyze first** — map the project, identify files >300 lines, detect missing separation of concerns
2. **Modular layout** — `/components`, `/pages`, `/services`, `/utils`, `/routes` adapted to stack
3. **Single responsibility** — every file and function has one job. Extract helpers if function exceeds 80 lines
4. **Hard limit** — no file exceeds 300 lines. Split by sub-domain if necessary
5. **No breaking changes** — preserve all existing functionality

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

Refactor owns **process** — the structural organization and architectural skeleton. The folder structure is sacred.

### When Refactor Leads

- Structural overhauls, file splitting, or folder restructuring
- Early-stage cleanup of legacy or "messy" projects

### When Refactor Defers

| Other Skill's Domain | What Refactor Does |
|---------------------|-------------------|
| **Voice** | Provides architectural plan. Voice handles tone of health reports. |
| **Craft** (e.g. harden) | Refactor sets the stage — defines where things go. Harden fills them with production-ready patterns (pooling, caching, etc.). |

### Pipeline Behavior

- **Upstream**: Triggered after requirements gathering or when a project outgrows its structure
- **Downstream**: Feeds into `harden` for production readiness or `testing` for verification

## Related Skills

- [Harden](./harden) — downstream: harden follows refactor for production readiness
- [Planner](./planner) — upstream: planning feeds into refactoring strategy
- [Researcher](./researcher) — gather context on best practices for target architecture

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/refactor/SKILL.md) — complete guide with reference files
- [SIP Framework](/guide/sip-framework) — how refactor composes
