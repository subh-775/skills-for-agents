# UX Patterns Reference

Dashboards, user flows, navigation, forms, tables, empty states, loading states — the patterns that make products actually usable.

---

## Dashboard Design

### Types

| Type | Purpose | Key Widgets |
|------|---------|-------------|
| **Analytics** | Understand data, spot trends | Line/bar charts, KPI cards, filters |
| **Admin** | Manage users, content, settings | Data tables, stat cards, activity feeds |
| **Monitoring** | Real-time health, alerts | Status badges, real-time charts, alert lists |
| **Project** | Track tasks, timelines, team | Kanban boards, Gantt charts, burndown |
| **E-commerce** | Sales, inventory, orders | Revenue charts, order tables, funnels |

### Layout Pattern

```
┌─────────────────────────────────────────────┐
│  [Filter Bar: date range, segments, export] │
├──────────┬──────────┬──────────┬────────────┤
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4    │
│  ↑ 12%   │  ↓ 3%    │  ↑ 8%    │  → 0%     │
├──────────┴──────────┴──────────┴────────────┤
│         Primary Chart (line/area)           │
├──────────────────────┬──────────────────────┤
│   Bar Chart          │   Donut Chart        │
├──────────────────────┴──────────────────────┤
│   Detailed Data Table with pagination       │
└─────────────────────────────────────────────┘
```

### KPI Card Anatomy

- Label (what it is)
- Large number (current value)
- Trend indicator (arrow + percentage + "vs last period")
- Optional: sparkline showing recent trend
- Optional: target/progress bar

Responsive: 4 cards → 2x2 grid → stacked vertically.

### Chart Selection

| Data Relationship | Best Chart | Avoid |
|-------------------|------------|-------|
| Trend over time | Line chart | Pie chart |
| Comparison (few items) | Bar chart | Line chart |
| Part of whole | Donut chart | 3D charts |
| Distribution | Histogram | Bar chart |
| Correlation | Scatter plot | Line chart |
| Flow/Funnel | Funnel chart | Bar chart |
| Geographic | Choropleth map | Table |

### Data Viz Rules

- Remove chart junk (3D, decorative icons, heavy borders, gradient fills)
- Start Y-axis at zero for bar charts (truncating distorts comparison)
- Line charts can start at non-zero if showing subtle changes
- Use tooltips for exact values
- Place legends inside chart area (top-right) or use direct labels
- Show empty and loading states (skeleton > spinner)
- Color: sequential (low→high), diverging (two extremes), categorical (distinct groups)
- Never rely on color alone (add patterns, labels, or icons)

---

## Sidebar Navigation

```
┌──────────────────────┐
│  Logo                │
│                      │
│  ▸ Dashboard         │  ← active (highlighted)
│  ▸ Analytics         │
│  ▸ Users             │  ← has submenu
│    ├─ All Users      │
│    ├─ Roles          │
│    └─ Permissions    │
│  ▸ Settings          │
│  ────────────────    │
│  ▸ Help              │
│  ▸ Logout            │
└──────────────────────┘
```

**Collapsed state** (icon-only): 60-80px, tooltip on hover.
**Mobile**: hamburger → overlay drawer.
**Keyboard**: arrow keys move, Enter selects, Escape closes.
**Shortcut**: Ctrl+B to toggle collapse.

### Command Palette (Cmd+K)

```
┌─────────────────────────────────────────┐
│ 🔍 Search or type a command...          │
├─────────────────────────────────────────┤
│ Recent                                  │
│   📊 Dashboard                          │
│ Actions                                 │
│   ➕ Create New User                    │
│   📤 Export Data                        │
└─────────────────────────────────────────┘
```

Fuzzy search, grouped results, keyboard shortcuts shown, recent items at top.
Libraries: cmdk (React), kbar.

### Mobile Bottom Nav

```
├──────┬──────┬──────┬──────┬─────────┤
│  🏠  │  📊  │  ➕  │  🔔  │  👤    │
│ Home │ Stats│ Add  │ Alert│ Profile │
└──────┴──────┴──────┴──────┴─────────┘
```

3-5 items max. Center item can be FAB. Active = filled icon + color. Inactive = outline + gray.

---

## User Flows

### Onboarding

```
Welcome → Value Prop → Setup → First Action → Success
```

- Progress indicator at top
- Save progress if user closes midway
- Skip option for returning users
- Confetti/animation on success
- Time to value ASAP

### Task Completion

```
Entry → Action Form → Confirmation → Next Step
```

- Button loading state during save
- Toast notification for success
- Undo option for destructive actions (5-second toast)
- Suggested next actions after completion

### Error Recovery

```
Error → Explanation → Suggestion → Retry
```

**Error message formula**: What happened? Why? How to fix?

- Bad: "Error 500"
- Good: "We couldn't process your payment. Your card was declined. Please check your card details or try a different payment method."

### Search

```
Input → Suggestions → Results → Detail
```

- Debounce input (300ms)
- Keyboard navigation (arrows + Enter)
- Highlight matching text
- Show result count
- No-results: suggest alternatives, clear button

---

## Form Design

### Rules

- **Single column** layout (faster completion than multi-column)
- **Logical grouping**: personal info, address, payment (with section headers)
- **Inline validation**: on blur (not on every keystroke)
- **Error messages**: below field, specific and actionable
- **Smart defaults**: pre-fill when possible (country from IP, date to today)
- **Progressive disclosure**: show advanced options on demand
- **Multi-step**: progress indicator, save draft, allow back, summary before submit

### Error Messages

- Bad: "Invalid input" → Good: "Email must include @ and a domain"
- Bad: "Required field" → Good: "Please enter your first name"
- Bad: "Error" → Good: "Password must be at least 8 characters with one uppercase letter and one number"

### Floating Label

```css
.form-group { position: relative; }
.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  top: -0.5rem;
  font-size: 0.75rem;
  color: var(--primary);
}
```

---

## Table Design

### Column Sizing

- **Fixed**: dates, status badges, actions (predictable content)
- **Flexible**: names, descriptions (use `flex-grow`)

### Features

- **Sort**: click header, cycle ascending → descending → none
- **Filter**: dropdown per column, active filter chips
- **Search**: debounced, highlight matches, result count
- **Row actions**: three-dot menu (⋮) on hover, or inline buttons
- **Bulk actions**: appear when rows selected (Export, Delete, Cancel)
- **Pagination**: for large datasets (Page 1 of 10 | Showing 1-20 of 184)
- **Virtual scrolling**: for 1000+ rows (react-window)

### Responsive Tables

Desktop: full table. Tablet: hide less important columns. Mobile: convert to cards.

```
MOBILE CARD VIEW:
┌─────────────────────────────────────┐
│ John Doe                            │
│ Status: Active                      │
│ Date: Jan 2024                      │
│ [View] [Edit]                       │
└─────────────────────────────────────┘
```

---

## Empty State Design

### Anatomy

```
┌─────────────────────────────────────┐
│    [Illustration]                   │
│    Headline (what's missing)        │
│    Description (why, what to do)    │
│    [Primary Action Button]          │
└─────────────────────────────────────┘
```

### Types

- **First-use**: "No analytics data yet. Install the tracking script to start collecting data."
- **No-results**: "No results for 'xyz'. Try different keywords or adjust your filters."
- **Error**: "Couldn't load data. Something went wrong. Please try again."
- **Cleared**: "All items removed. You've cleared this list."

Use custom illustrations, not generic stock. Keep text concise. Always include a primary action.

---

## Loading State Design

### Skeleton Screens

Better than spinners — users see layout before content loads.

```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Progressive Loading

Priority order:
1. Navigation + page structure
2. Primary content (above fold)
3. Secondary content (below fold)
4. Enhancements (animations, images, charts)

### Optimistic Updates

Show result immediately, before server confirms:
- User clicks "Like" → immediately show filled heart + count+1
- Send request to server
- If server fails, revert and show error toast

### Stale-While-Revalidate

Show cached data immediately, update in background. Visual indicator: "Last updated: 2 minutes ago [Refresh]".

---

## Navigation Patterns

### Breadcrumbs

For deep hierarchies (3+ levels): `Home > Section > Subsection > Current Page`

Each level clickable except current page.

### Tabs

For related views of same data. Active tab has indicator (underline or pill). Content crossfade on switch.

### Mega Menu

For complex navigation with many categories. Grouped links, featured items, icons.

---

## Wayfinding

Help users answer: Where am I? Where can I go? Where have I been?

- **Current location**: highlight active nav, show breadcrumb
- **Available destinations**: visible navigation, clear labels
- **History**: visited link color, recent items in search
- **Orientation**: page title matches nav label

---

## Information Architecture

### Card Sorting

**Open**: users group items into categories and name them. Reveals mental models.
**Closed**: pre-defined categories, users sort items into them. Validates structure.

### Progressive Disclosure

- **Show/Hide**: click to expand additional fields
- **Stepper**: only show relevant fields per step
- **Drill-down**: overview → category → item → details
- **Inline expansion**: expand row to show details

### Information Scent

Labels should clearly communicate what users will find.

- Good: "View Invoice #1234", "Download PDF Report", "Edit Profile Photo"
- Bad: "Click Here", "More", "Info"

Use action verbs + nouns: "Manage Billing" not "Billing".
