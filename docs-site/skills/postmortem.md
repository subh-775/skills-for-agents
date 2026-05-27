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

All postmortem reports are saved as **visual HTML dashboards** — not plain text.

### Folder Structure

```
postmortem/YYYY-MM-DD-<slug>/
├── index.html          # Incident dashboard (entry point)
├── timeline.html       # Detailed timeline + charts
├── root-cause.html     # 5 Whys deep dive + system diagrams
├── action-items.html   # Action item tracker
├── assets/
│   ├── style.css       # Dark-theme stylesheet
│   └── charts.js       # Chart.js visualizations
└── data/
    └── incident.json   # Machine-readable backup
```

### Visual Design

- **Dark theme** (#0d1117 background, light text, severity accents)
- **Severity badges** — red (SEV1), orange (SEV2), yellow (SEV3), blue (SEV4)
- **Impact stat cards** — severity, duration, users affected, revenue impact, TTD, TTR
- **Visual timeline** — vertical timeline with colored event markers (not a boring table)
- **5 Whys cascade** — cascading card chain with deepening colors (not a table)
- **System diagram** — CSS/SVG showing affected flow with failure point highlighted
- **Action item cards** — priority badges, owner, due date, status
- **Self-contained** — Chart.js (CDN) is the only external dependency

### index.html Dashboard

Opens with severity badge and impact stat cards, a visual timeline, system diagram, root cause cascade, and top action items. Links to supporting pages (timeline, root-cause, action-items).
