<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Voice, Density, Craft</span>
</div>

# Memory

Persistent context engine. Maintains continuity between turns and sessions through daily journal rotation, manifest indexing, and identity tracking.

## When to Use

- **Startup** — mandatory, runs at the beginning of every session
- User says "I like X", "remember this", "here is my key"
- Session continuity is needed

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">User preference tracking</div>
<div class="example-desc">Memory captures and persists user preferences across sessions.</div>

```
User: "I prefer dark mode and use Neovim as my editor"

Memory saves to manifest:
- preference: dark mode
- editor: neovim
- likely: terminal-native user, prefers CLI tools

Next session, the agent knows to:
- Default to dark mode in generated UIs
- Suggest CLI solutions over GUI
- Use vim-style keybindings in examples
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Project context continuity</div>
<div class="example-desc">Memory tracks project state across interrupted sessions.</div>

```
Session 1: User is debugging a TPU training job, mentions
the error happens at step 5000, suspects data pipeline.

Session 2 (next day): Memory loads context.
Agent says: "Last time you were debugging the TPU training
job — the one failing at step 5000. Did the data pipeline
fix work?"

No re-explaining needed. Context is preserved.
```
</div>

## How It Works

1. Reads `memory/data/manifest.json` at session start
2. Loads relevant context for the current task
3. Updates journal entries as new information arrives
4. Periodically rotates old entries to archive
