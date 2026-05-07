# Planner — Document Templates Reference

Full pre-filled templates for all 8 planning documents.
Fill in `[BRACKETS]` with actual project context.

> **Read `references/research-foundations.md` for the academic research informing these templates.**

---

## PRD.md Template

```markdown
# PRD.md — [Project Name]
> Version: 1.0 | Status: Draft | Last Updated: [DATE]

---

## Product Vision

**One-liner:** [One sentence describing the product]

**Problem Statement:**
[2–3 sentences: What specific pain exists? Who feels it? Why is now the right time?]

**Solution:**
[2–3 sentences: How does this product solve it? What's the key insight?]

---

## Target Users & Personas

### Persona 1: [Name / Role]
- **Who:** [Age range, occupation, technical level]
- **Goal:** [What they want to accomplish]
- **Pain:** [What frustrates them today]
- **Success looks like:** "I want to..."

### Persona 2: [Name / Role]
- **Who:** [...]
- **Goal:** [...]
- **Pain:** [...]
- **Success looks like:** [...]

---

## Feature Requirements

| # | Feature | Description | Priority | Acceptance Criteria | Phase |
|---|---------|-------------|----------|---------------------|-------|
| F1 | [Name] | [What it does] | P0/P1/P2 | [Done when...] | 1 |
| F2 | [Name] | [What it does] | P0/P1/P2 | [Done when...] | 1 |
| F3 | [Name] | [What it does] | P0/P1/P2 | [Done when...] | 2 |

**Priority Guide:** P0 = blocking launch | P1 = launch requirement | P2 = post-launch

---

## User Stories

As a [persona], I want to [action] so that [outcome].

Acceptance Criteria:
- GIVEN [context] WHEN [action] THEN [result]
- GIVEN [context] WHEN [action] THEN [result]

---

## Success Metrics

| Metric | Target | Measurement Method | Timeframe |
|--------|--------|--------------------|-----------|
| [e.g. Signup conversion] | [e.g. >30%] | [e.g. Analytics funnel] | [e.g. 30 days post-launch] |
| [e.g. API p95 latency] | [e.g. <200ms] | [e.g. APM monitoring] | [e.g. Continuous] |
| [e.g. DAU/MAU ratio] | [e.g. >0.4] | [e.g. Product analytics] | [e.g. 60 days post-launch] |

---

## Non-Goals (Explicit Out-of-Scope)

These will NOT be built in v1:
- [ ] [Feature X] — rationale: [why excluded]
- [ ] [Feature Y] — rationale: [why excluded]

---

## Technical Constraints

- **Stack:** [Frontend / Backend / DB / Hosting]
- **Auth:** [Clerk / NextAuth / Supabase Auth / custom]
- **Timeline:** [Target launch date or sprint count]
- **Team:** [Solo / 2-person / startup team]
- **Budget:** [Free tier only / $X/month infra budget]

---

## Open Questions

| Question | Owner | Due Date | Status |
|---------|-------|----------|--------|
| [Question needing resolution] | [Person] | [Date] | Open |

---

## Context for AI Agents

> **Note:** Machine-readable context for Cursor/Claude Code/Codex.

**Project:** [Name] — [One-line description]
**Stack:** [tech list]
**MVP Features:** [comma-separated list of P0 features]
**Users:** [primary persona] and [secondary persona]
**Success:** [top 1-2 metrics]
**Phase 1 focus:** [what gets built first]
**Not building:** [top 1-2 non-goals]
```

---

## DESIGN.md Template

```markdown
# DESIGN.md — [Project Name] Technical Design
> Version: 1.0 | References: PRD.md | Last Updated: [DATE]

---

## System Overview

[2–3 paragraphs: What does the system do at a high level? What are the major subsystems?
How do they relate? What's the data lifecycle?]

---

## Component Breakdown

### [Component 1: e.g. Frontend / Client]
- **Technology:** [Next.js 15 / React 19 / etc.]
- **Responsibility:** [What it owns]
- **Key interactions:** [What it calls/receives]

### [Component 2: e.g. API / Backend]
- **Technology:** [...]
- **Responsibility:** [...]
- **Key interactions:** [...]

### [Component 3: e.g. Database]
- **Technology:** [...]
- **Responsibility:** [...]
- **Key interactions:** [...]

---

## Data Flows

### [Flow 1: e.g. User Authentication]
1. User submits credentials to `[frontend route]`
2. Frontend calls `POST /api/auth/login`
3. Backend validates via `[auth provider]`
4. Session token returned, stored in `[cookie/localStorage/etc.]`
5. Subsequent requests include token in `Authorization` header

### [Flow 2: e.g. Core Feature Flow]
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Key Design Decisions

| Decision | Option Chosen | Alternatives Considered | Rationale |
|---------|--------------|------------------------|-----------|
| [e.g. Auth provider] | [Clerk] | [NextAuth, custom JWT] | [Why] |
| [e.g. ORM] | [Drizzle] | [Prisma, raw SQL] | [Why] |
| [e.g. State management] | [Zustand] | [Redux, Context API] | [Why] |

---

## Error Handling Strategy

**Client-side:**
- All API calls wrapped in try/catch
- User-facing errors: toast notifications (non-blocking)
- Fatal errors: error boundary → fallback UI
- Form validation: client-side first, server validation as truth

**Server-side:**
- All endpoints return structured `{ success, data, error }` response
- Unhandled exceptions: logged to [logging service], 500 returned to client
- Rate limiting: [X requests/minute per IP/user]

**Database:**
- Transactions for multi-table writes
- Soft deletes preferred over hard deletes for user data

---

## Security Considerations

- [ ] **Auth:** All protected routes require valid session
- [ ] **Authorization:** Row-level security via [Supabase RLS / middleware]
- [ ] **Input validation:** Zod schemas on all API inputs
- [ ] **SQL injection:** Prevented via ORM parameterized queries
- [ ] **XSS:** Content Security Policy headers
- [ ] **CSRF:** [Strategy: SameSite cookies / CSRF tokens]
- [ ] **Secrets:** All API keys in environment variables, never in code
- [ ] **Rate limiting:** [Library/service used]

---

## Scalability Notes

**Current design targets:** [e.g. 0–1000 users, <100 RPS]

**Bottlenecks at scale:**
- [Component X]: will need [caching/sharding/CDN] beyond [scale threshold]

**Not premature-optimizing:** [List what's intentionally simple for MVP]
```

---

## ARCH.md Template

```markdown
# ARCH.md — [Project Name] Architecture
> Version: 1.0 | References: PRD.md, DESIGN.md | Last Updated: [DATE]

---

## System Diagram

[Mermaid graph TD diagram showing all components: Frontend, API, DB, Cache, External Services]

---

## Component Responsibilities

| Component | Owns | Does NOT own |
|-----------|------|-------------|
| Frontend | UI rendering, client state, routing | Business logic, data persistence |
| API Layer | Request routing, auth middleware, validation | UI rendering, direct DB queries |
| Services | Business logic, orchestration | HTTP concerns, DB connection management |
| Data Layer | Persistence, queries, transactions | Business rules |

---

## Critical User Flow

[Mermaid sequenceDiagram showing primary user journey: User → Frontend → API → Auth → DB → response]

---

## Data Model Overview

[Mermaid erDiagram showing entity relationships]

---

## Deployment Topology

| Layer | Service | Config |
|-------|---------|--------|
| DNS | [Vercel / Cloudflare] | [Domain routing] |
| Frontend | [Vercel / Netlify] | [Next.js / static] |
| API | [Vercel Functions / Railway] | [Runtime config] |
| Database | [Supabase / Neon] | [Connection pooling] |

---

## External Dependencies

| Dependency | Purpose | Fallback if unavailable |
|-----------|---------|------------------------|
| [Clerk] | Authentication | Block all authed routes |
| [Supabase] | Database + storage | Service unavailable page |

---

## Failure Modes & Mitigations

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| DB unavailable | All data reads/writes fail | Circuit breaker, health page |
| Auth provider down | Login fails | Cached sessions for active users |
| Third-party API timeout | Feature degraded | Timeout + graceful fallback |
```

---

## IMPL-PLAN.md Template

```markdown
# IMPL-PLAN.md — [Project Name] Implementation Plan
> Version: 1.0 | References: PRD.md, ARCH.md | Last Updated: [DATE]

## Build Strategy: Vertical Slices
Each phase ships end-to-end working functionality — from database to UI.

---

## Phase 0: Foundation (Week 1)
**Goal:** Skeleton is deployable. CI/CD works. Auth exists.

- [ ] Initialize repo + push to GitHub
- [ ] Set up framework ([Next.js / FastAPI / etc.])
- [ ] Configure environment variables (local + staging)
- [ ] Deploy empty app to [Vercel / Railway]
- [ ] Integrate auth provider
- [ ] Create DB schema (migration 001: users table)
- [ ] Set up DB connection + ORM
- [ ] Create AGENTS.md in project root
- [ ] Configure linter + formatter
- [ ] Basic CI (lint + typecheck on PR)

**Done when:** `/` renders, `/login` works, `/dashboard` is auth-gated.

---

## Phase 1: MVP Core Loop (Week 2–3)
**Goal:** [Primary user story] works end-to-end.

### Feature: [First Core Feature]
- [ ] DB: migration for [entity]
- [ ] API: CRUD endpoints for [resource]
- [ ] UI: List/Dashboard page
- [ ] UI: Create/Edit form
- [ ] UI: Detail view
- [ ] Tests: API endpoint tests
- [ ] Tests: UI smoke test

**Done when:** User can [create / view / edit / delete] [entity].

---

## Phase 2: Feature Expansion (Week 4–5)
**Goal:** Add P1 features. Enhance Phase 1 slices.

### Feature: [Second Feature]
- [ ] [Tasks...]

### Enhancements:
- [ ] Add pagination to [list endpoint]
- [ ] Add search/filter to [resource]

---

## Phase 3: Production Hardening (Week 6)
**Goal:** Ship-ready. Secure. Observable.

- [ ] Security audit (auth on all routes, input validation)
- [ ] Error boundary + fallback UI
- [ ] Loading states on all async operations
- [ ] Rate limiting on API endpoints
- [ ] Error monitoring ([Sentry / LogRocket])
- [ ] Analytics ([PostHog / Mixpanel])
- [ ] Performance audit (Lighthouse > 90)
- [ ] E2E test for critical path
- [ ] Update all docs to reflect final state

**Done when:** Launch checklist is green.
```

---

## AGENTS.md Template

```markdown
# AGENTS.md — [Project Name]
> AI coding agent context file. Read this before writing any code.
> See also: docs/PRD.md (requirements), docs/ARCH.md (architecture)

## Project Context
**What we're building:** [One paragraph]
**Stack:** [Frontend] + [Backend] + [DB] + [Auth] + [Hosting]
**Current phase:** Phase [N] — [Phase name]

## Project Structure
[File tree showing src/ layout with brief annotations]

## Code Conventions
- **Language:** TypeScript strict mode. No `any`. No untyped returns.
- **Components:** Functional only. Named exports. Props typed with interface.
- **API responses:** Always `{ success: boolean, data?: T, error?: string }`
- **Error handling:** Every async function has try/catch. Errors logged, not swallowed.
- **Naming:** camelCase vars/fns, PascalCase components/types, kebab-case files
- **Imports:** Absolute imports via `@/` alias

## Database Rules
- All DB access through ORM, no raw SQL
- UUID primary keys
- Every table has `created_at` and `updated_at`
- Soft deletes via `deleted_at`, never hard delete user data

## Auth Rules
- All routes under `/dashboard` require auth
- Get current user via `[getUser()]` — never trust client-passed user IDs
- Row-level security: users can only access their own data

## Testing
- Unit tests for all business logic functions
- API tests for happy + error paths
- Tests must pass before marking any task done

## Git Workflow
- Branch: `feature/[description]`, `fix/[description]`
- Commits: conventional commits (`feat:`, `fix:`, `chore:`)
- Never commit `.env` or secrets

## Explicit Boundaries
- ❌ Don't modify DB schema without a migration file
- ❌ Don't hardcode API keys in source files
- ❌ Don't use `any` type
- ❌ Don't build UI before the API endpoint exists
- ❌ Don't skip error handling on async calls
```

---

## API.md Template

```markdown
# API.md — [Project Name] API Specification
> Base URL: `/api` | Auth: Bearer token

## Authentication
All protected endpoints require `Authorization: Bearer <token>` header.

## Endpoints

### [Resource] — e.g. Users

#### GET /api/users/me
Get current authenticated user.
**Auth:** Required
**Response 200:** `{ success: true, data: { id, email, name, createdAt } }`

#### POST /api/[resource]
Create a new [resource].
**Auth:** Required
**Body:** `{ field1: "string (required)", field2: "number (optional)" }`
**Response 201:** `{ success: true, data: { id, ... } }`

## Error Response Format
All errors: `{ success: false, error: "message", code: "MACHINE_READABLE_CODE" }`

| Code | Meaning |
|------|---------|
| 400 | Invalid input |
| 401 | Not authenticated |
| 403 | Not authorized |
| 409 | Conflict (duplicate) |
| 429 | Rate limited |
| 500 | Server error |
```

---

## DB.md Template

```markdown
# DB.md — [Project Name] Database Schema
> Database: PostgreSQL | ORM: [Drizzle / Prisma]

## Entity Overview
| Table | Description | Key Relations |
|-------|-------------|---------------|
| users | Application users | — |
| [entity] | [Description] | belongs to users |

## ERD
[Mermaid erDiagram]

## Table Definitions

### users
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK, DEFAULT gen_random_uuid() | |
| email | TEXT | NOT NULL, UNIQUE | lowercase, trimmed |
| name | TEXT | | Display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMP | ON UPDATE NOW() | |
| deleted_at | TIMESTAMP | NULL | NULL = not deleted |

**Indexes:** `users_email_idx` on `(email)`, `users_created_at_idx` on `(created_at DESC)`

## Migration Strategy
- Migrations in `src/db/migrations/`
- Naming: `001_initial.sql`, `002_add_[feature].sql`
- Never edit existing migrations — create new ones
```

---

## FLOW.md Template

```markdown
# FLOW.md — [Project Name] User Flows
> References: PRD.md (personas), DESIGN.md (data flows)

## Primary User Journey: [Core Flow Name]

### Happy Path
1. User lands on [landing page]
2. User clicks [CTA]
3. [Auth step if needed]
4. User reaches [dashboard]
5. User completes [key action]
6. System responds with [confirmation]

[Mermaid flowchart TD for the happy path with decision nodes]

## Edge Cases & Error States

| Scenario | User sees | System does |
|----------|-----------|-------------|
| Session expired | Redirect to login + toast | Invalidate cookie |
| Network error on submit | Toast: "Failed to save" | No DB write, form preserved |
| Empty state (no data) | Empty state illustration + CTA | Return empty array |
| Server error | "Something went wrong" | 500 + error logged |

## Screen Inventory

| Screen | Route | Auth | Description |
|--------|-------|------|-------------|
| Landing | `/` | No | Marketing page |
| Login | `/login` | No | Auth form |
| Dashboard | `/dashboard` | Yes | Main app view |
| Settings | `/settings` | Yes | User preferences |
```
