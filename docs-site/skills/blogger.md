<div class="domain-header">
  <span class="skill-badge voice">Voice</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process, Craft</span>
</div>

# Blogger

Authentic personal-voice writing. Raw, unpolished, stream-of-consciousness prose that sounds like a real human wrote it — not a polished marketing team.

## When to Use

- User wants a blog post, essay, or technical piece with personality
- User says "write like me", "express this in my voice"
- User wants a Discord-style reply or social media post
- User invokes `/blog`

## Triggers

```
/blog [optional: casual|technical|rant|reflection|thread] [topic/notes]
/blog reply [message]
"write a blog", "blog about this", "write like me", "make this a post"
```

## Modes

| Mode | Use Case |
|------|----------|
| `casual` | Default. Conversational, tangents welcome |
| `technical` | Deep dives, still personal but more structured |
| `rant` | Opinionated, heated, unfiltered |
| `reflection` | Thoughtful, philosophical, looking back |
| `thread` | Twitter/social media format, bite-sized |
| `reply` | Discord DM style, responding to a message |

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Technical blog post</div>
<div class="example-desc">Write a technical deep-dive about why TPU training behaves differently from GPU training.</div>

```
/blog technical Why TPU training is a different beast entirely

The agent writes a 800-word technical piece explaining TPU vs GPU
differences using stream-of-consciousness prose, Hinglish phrases,
and first-principles reasoning. It admits gaps in knowledge, cites
personal experience with v5e pods, and doesn't pretend to be a
textbook.
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Terse blog with Caveman composition</div>
<div class="example-desc">Write a technical blog but keep it short. Layer two skills together.</div>

```
/blog technical + /caveman lite

The agent writes in authentic voice (blogger domain) but applies
lite compression (caveman domain). Result: personality intact,
fluff removed. ~400 words instead of 800.
```
</div>

<div class="example-box">
<div class="example-label">Example 3</div>
<div class="example-title">Rant about a frustrating experience</div>
<div class="example-desc">Write an unfiltered rant about debugging a distributed training job.</div>

```
/blog rant My 3-day fight with XLA compilation errors

The agent writes an opinionated, heated piece. Admits frustration.
Uses Hinglish naturally. Doesn't soften the edges. Real timestamps,
real error messages, real emotional arc.
```
</div>

<div class="example-box">
<div class="example-label">Example 4</div>
<div class="example-title">Postmortem then blog about it</div>
<div class="example-desc">Write a postmortem first, then turn it into a reflective blog post.</div>

```
/postmortem → /blog reflection

Postmortem generates the structured incident report (timeline,
root cause, action items). Blogger then rewrites it as a
reflective piece — what we learned, what we'd do differently,
the human side of the incident.
```
</div>

## What It Does

Blogger doesn't just write — it channels a specific voice built from deep analysis of actual conversations, research logs, and thinking patterns. Key characteristics:

- **Stream-of-consciousness** — thinks out loud, follows tangents
- **Hinglish-native** — code-switches between English and Hindi naturally
- **Honest about failure** — admits when things are cooked
- **Casually profound** — finds philosophy in technical details
- **First principles** — argues from scratch, doesn't cite authority
