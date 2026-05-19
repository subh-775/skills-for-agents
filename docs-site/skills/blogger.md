# Blogger

Writes blog posts, essays, technical pieces, rants, and reflections in authentic personal voice.

## Domain

**Voice** — controls tone, vocabulary, personality, emotional register.

## When to Use

- User says `/blog`, "write a blog", "blog about this"
- User wants "write like me", "express this in my voice", "make this a post"
- Personal-voice writing needed

## Post Types

| Type | Length | Style | Use When |
|------|--------|-------|----------|
| **default** | 600–1200 words | Balanced technical + personal | General blog posts |
| **casual** | 300–600 words | More Hinglish, more fragments | Quick takes, observations |
| **technical** | 800–1600 words | More code, more numbers | Deep dives, tutorials |
| **rant** | 400–800 words | Direct, honest critique | Strong opinions |
| **reflection** | 500–1000 words | Human layer, journey posts | Learning moments |
| **thread** | 8–15 items | Short punchy items | Twitter/X threads |

## Commands

```bash
/blog [type] [topic]

/blog                    # Default style
/blog casual             # Quick take
/blog technical          # Deep dive
/blog rant               # Strong opinion
/blog reflection         # Journey post
/blog thread             # Twitter thread
```

## Voice Characteristics

- **Hinglish-native** — English default, Hindi enters at emotional triggers
- **Stream-of-consciousness** — thoughts as they form
- **Honest about failure** — `sed` when disappointed, `fk` when frustrated
- **Casually profound** — finds philosophy in perplexity scores
- **Never polished for politeness** — raw, unfiltered

## Composability

### Domain Declaration

```yaml
domain: voice
composable: true
yields_to: [process, craft]
```

Blogger owns **voice** — tone, personality, vocabulary, emotional register.

### When Blogger Leads

- Personal-voice writing
- Blog posts, essays, reflections
- Authentic expression

### When Blogger Defers

| Other Skill's Domain | What Blogger Does |
|---------------------|-------------------|
| **Process** | Blogger fills content sections but preserves structural skeleton. |
| **Craft** | Blogger provides prose; craft skill handles visual design. |
| **Density** | Blogger writes full-length; density skill compresses. |

## Tips

1. **Specify type** — `/blog technical` for deep dives
2. **Compose with caveman** — `/blog + /caveman lite` for terse posts
3. **Let voice emerge** — don't force Hinglish, it enters naturally
4. **Embrace fragments** — short sentences land hard

## Related Skills

- [Caveman](./caveman) — density skill that composes well with blogger
- [Postmortem](./postmortem) — process skill for incident writing
- [Documenter](./documenter) — content skill for technical docs
- [Compress](./compress) — file compression for blog drafts
- [Researcher](./researcher) — gather context before writing

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/blogger/SKILL.md) — complete voice guide
- [SIP Framework](/guide/sip-framework) — how blogger composes
