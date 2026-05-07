# Research Foundations

Academic and industry research that informs the planner skill's design decisions.

---

## Academic Papers

### IACDM — Interactive Adversarial Convergence Development Methodology
**Paper:** arXiv:2604.16399 (March 2026)
**Authors:** Jasmine Moreira

**Key Findings:**
- Vibe coding exposes a "verification gap" — LLMs have zero internal semantic verification
- Experienced devs using AI were measurably slower despite believing they were faster
- 10.3% of AI-generated apps in production contained critical security flaws
- **Solution:** 8-phase framework with external verification agents at discrete gates

**Three Pillars:**
1. Deep problem discovery via Hierarchical Semantic Analysis BEFORE any technical solution
2. Persistent knowledge management across sessions
3. Systematic adversarial critique through specialized lenses before implementation

**Influence on Planner:** The adversarial self-review checklist and the strict separation of planning phases (never interleave planning and coding).

---

### REprompt — Requirements Engineering for AI Prompts
**Paper:** arXiv:2601.16507 (January 2026)
**Authors:** Shi et al.

**Key Findings:**
- Prompts serve dual role: guiding LLM behavior AND carrying user requirements
- Most prompt engineering ignores requirements engineering methodology
- System prompts = high-level steering; user prompts = requirements carriers
- Grounding prompts in RE principles significantly improves generated artifacts

**Influence on Planner:** The PRD template is designed to produce documents that function as effective prompts for AI coding agents, not just human-readable specs.

---

### CIAO — Code In Architecture Out
**Paper:** arXiv:2604.08293 (April 2026)
**Authors:** De Luca et al.

**Key Findings:**
- Structured architecture documentation templates (ISO/IEC/IEEE 42010 + C4 model) outperform free-form narratives
- LLMs can generate system-level architecture docs from codebases in minutes
- Developers rated generated docs as valuable and comprehensible
- Limitations: diagram quality, high-level context, deployment views

**Influence on Planner:** The design doc template uses C4 model hierarchy (Context → Container → Component) and Mermaid diagrams for architecture visualization.

---

### QoT — Questions-of-Thoughts
**Paper:** arXiv:2603.11082 (March 2026)
**Authors:** Liu & Tsai

**Key Findings:**
- Quality-driven self-questioning scaffold: user goal → ordered engineering steps → stepwise constraint verification
- ISO/IEC-inspired quality rubric: Scalability, Completeness, Modularity, Security
- Consistent quality improvements for larger models and complex domains
- Self-questioning reduces omission errors

**Influence on Planner:** The adversarial review checklist after each document phase, and the quality dimensions used in the risk register.

---

### SolidCoder — Bridging the Mental-Reality Gap
**Paper:** arXiv:2604.19825 (April 2026)
**Authors:** Lee & Huang

**Key Findings:**
- Two gap dimensions in LLM code generation:
  - **Specification Gap:** Overlooking edge cases during planning
  - **Verification Gap:** Hallucinating correct behavior for flawed code
- Edge-case awareness provides the largest quality improvement
- Execution grounding catches errors that better specs alone cannot

**Influence on Planner:** The emphasis on edge cases in acceptance criteria, and the separation of specification (planning) from verification (testing).

---

## Industry Frameworks

### Specification-Driven Development (SDD)
**Source:** EPAM, Builder.io, Augment Code (2025-2026)

The emerging standard for AI-assisted development:
1. **Specify** — Define requirements in structured documents
2. **Plan** — Generate technical architecture and implementation plan
3. **Decompose** — Break into granular, testable tasks
4. **Implement** — Feed tasks to AI incrementally, validate each

**Key principle:** The spec is the "source of truth." Code is a derivative of the spec, not the other way around.

### Project Constitution Pattern
**Source:** Anthropic (CLAUDE.md), Cursor (.cursorrules → .mdc), community patterns

A foundational governance file that AI agents read at session start:
- Architecture principles (immutable structural rules)
- Technology constraints (stack decisions with reasoning)
- Workflow rules (operational protocols)
- Quality standards (testing, documentation requirements)

**Key principle:** Include reasoning ("because...") for every rule so agents can generalize to novel situations.

### C4 Model
**Source:** Simon Brown (c4model.com)

Hierarchical architecture visualization:
- **Level 1: System Context** — The system as a black box + users + external systems
- **Level 2: Container** — Top-level deployable units + communication protocols
- **Level 3: Component** — Internal components of a single container
- **Level 4: Code** — Class/function level (rarely needed, use IDE instead)

**Key principle:** Don't mix abstraction levels. Each diagram should stay at one C4 level.

### Architecture Decision Records (ADRs)
**Source:** Michael Nygard (2011), widely adopted by 2025

Lightweight decision documents:
- **Title** — What was decided
- **Status** — Proposed / Accepted / Superseded / Deprecated
- **Context** — Why a decision was needed
- **Decision** — What was chosen
- **Consequences** — Pros, cons, and risks

**Key principle:** Only create ADRs for decisions that are hard to reverse, have multiple viable alternatives, or will be questioned later.

### Plan-Act-Reflect Framework
**Source:** Community best practices for AI-assisted development (2025)

Never interleave planning and execution:
1. **Plan** — Agent analyzes task, produces structured plan (NO code)
2. **Act** — Agent implements plan step-by-step
3. **Reflect** — Agent summarizes what was done, what issues arose, what remains

**Key principle:** If the agent can't write clear instructions for a step, the specification needs more work — don't let it start coding unclear requirements.
