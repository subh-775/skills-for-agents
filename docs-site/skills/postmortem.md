# Postmortem

Blameless postmortem workflow. Gathers incident context, writes a structured report, saves it to a gitignored `postmortem/` folder, and creates action items.

## Domain

**Process** — controls the workflow, template, required sections, review checklist, and file structure. The skeleton is sacred.

## When to Use

- `/postmortem` or "write a postmortem", "incident review", "post-incident"
- "blameless review", "what broke and why", "SEV1/SEV2 report"
- Any mention of documenting an outage, incident, or system failure
- "help me write up what happened"

## Workflow

### Step 0: Setup

```bash
mkdir -p postmortem
# Auto-adds postmortem/ to .gitignore
```

### Step 1: Gather Context

**Required:** Incident title, severity (SEV1-SEV4), date + time, duration, what broke, root cause, who responded.

**Optional:** Timeline, metrics, existing action items, related past incidents.

If user gives a wall of text / Slack dump / runbook notes — parse it. Don't make them re-type.

### Step 2: Generate Report

File: `postmortem/YYYY-MM-DD-<slug>.md`

**Template sections:**
- TL;DR (one paragraph, <100 words)
- Impact snapshot (users affected, duration, revenue, data loss, security)
- Timeline (precise times, no gaps >10 min)
- Root Cause with 5 Whys table
- Detection (time to detect, what worked, what didn't)
- Response (time to resolve, what worked, what could be faster)
- Lessons (went well, went wrong, got lucky)
- Action Items (P0 = before next deploy, P1 = this sprint, P2 = this quarter)

### Step 3: Review Pass

- No person blamed — system blamed, always
- Timeline has no gaps >10 min without explanation
- 5 Whys went deep (Why 3 is still a person's mistake = go deeper)
- Every action item has an owner
- "Got lucky" section is honest
- TL;DR is actually a TL;DR (<100 words)

### Step 4: Save and Confirm

Tells user: file location, that it's gitignored, suggests sharing in incident channel and creating tickets for P0s.

## Blameless Culture

| Don't say | Say instead |
|-----------|-------------|
| "Alice pushed broken code" | "The deploy lacked a canary stage" |
| "Bob missed it in review" | "The review checklist didn't cover infra changes" |
| "On-call was slow" | "Alert threshold was too high to fire early" |

## Edge Cases

- **Minor incident** — still write it. SEV3s reveal patterns SEV1s don't.
- **Unknown root cause** — write what you know. Mark as `[INVESTIGATION IN PROGRESS]`.
- **Third-party issue** — root cause = vendor. Action items = circuit breakers, fallbacks, SLA review.
- **No action items needed** — wrong. There's always at least one. "Monitor X metric" counts.

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

Postmortem owns **process** — the workflow, template, required sections, review checklist. Nobody overrides the structure.

### When Postmortem Leads

- Any incident documentation request
- Structured blameless analysis needed
- SEV reports, outage reviews, failure documentation

### When Postmortem Defers

| Other Skill's Domain | What Postmortem Does |
|---------------------|-------------------|
| **Voice** | Provides structure and required content. Voice fills prose within sections. Timeline still has precise times. 5 Whys still go 5 deep. |
| **Density** | Generates full report first. Density compresses as post-processing. Never skip sections for brevity. |
| **Craft** | If incident involved UI issues, invites craft skills to fill technical analysis sections. |

## Related Skills

- [Blogger](./blogger) — compose: "write a blog about what we learned from this incident"
- [Painter](./painter) — advisory mode for UI-related incidents
- [Caveman](./caveman) — compress the postmortem for knowledge base
- [Researcher](./researcher) — gather context for root cause analysis

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/postmortem/SKILL.md) — complete guide with full template
- [SIP Framework](/guide/sip-framework) — how postmortem composes
