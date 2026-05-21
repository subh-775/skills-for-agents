<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Density, Craft</span>
</div>

# Postmortem

Blameless incident documentation. Structured postmortem reports with root cause analysis, 5 Whys, and action items.

## When to Use

- User says "incident review", "what broke and why", "write a postmortem"
- User invokes `/postmortem`
- After an outage, bug, or incident

## Triggers

```
/postmortem
"incident review", "what broke and why", "write a postmortem",
"root cause analysis", "5 whys"
```

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Standard incident postmortem</div>
<div class="example-desc">Document a production incident with full analysis.</div>

```
/postmortem Auth service outage on May 15, 2026

The agent generates:
- Summary: Auth service down for 23 minutes, 12% of
  users affected
- Timeline: 14:00 deploy → 14:03 first errors → 14:05
  alert → 14:10 on-call paged → 14:18 root cause found
  → 14:23 rollback deployed
- Root cause: null pointer in middleware after config change
- 5 Whys analysis
- Action items with owners and deadlines
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Terse postmortem for quick distribution</div>
<div class="example-desc">Postmortem then compress for Slack/email.</div>

```
/postmortem → /caveman

Full postmortem compressed to 3-4 sentences:
"14:00 deploy pushed. 14:03 auth crashed. Root cause:
null in middleware. Fix: null guard added. 23min downtime.
Action: add auth integration tests, canary deploys."
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Postmortem with UI incident analysis</div>
<div class="example-desc">When the incident involves a visual regression.</div>

```
/postmortem + /painter (advisory)

Postmortem documents the incident structure. Painter
provides advisory input for the UI regression analysis —
what visual testing should have caught, accessibility
impact, and design system gaps that enabled the bug.
```
</div>

## Report Structure

| Section | Content |
|---------|---------|
| **Summary** | One-paragraph overview |
| **Timeline** | Chronological event log |
| **Impact** | Users affected, duration, severity |
| **Root Cause** | Technical root cause with 5 Whys |
| **Action Items** | Next steps with owners and deadlines |
| **Lessons Learned** | What we learned |
