# Compress

Compresses text files to reduce token count while preserving all meaning and technical accuracy.

## Domain

**Density** (files) — controls token count of text-based files.

## When to Use

- `/compress [path] [level]`
- "compress this", "shrink this file", "reduce tokens"
- Preparing files for LLM context windows

## Intensity Levels

| Level | Reduction | Use When |
|-------|-----------|----------|
| **lite** | ~30% | Light cleanup, keep readability |
| **standard** | ~50% | General compression, good balance |
| **aggressive** | ~65% | Heavy compression, fragments OK |
| **extreme** | ~80% | Maximum compression, telegraphic |

## Supported Files

`.md`, `.txt`, `.rst`, `.yaml`, `.json`, `.csv`, `.log`, `.toml`, `.cfg`, `.ini`

**Never touches:** source code files (`.py`, `.js`, `.ts`, etc.)

## Commands

```bash
/compress [path]              # Standard level
/compress [path] lite         # Light cleanup
/compress [path] aggressive   # Heavy compression
/compress [path] extreme      # Maximum compression
```

## What Gets Compressed

- Filler words, articles, hedging
- Redundant sentences
- Verbose synonyms → short equivalents
- Prose → tables (when appropriate)
- Multi-paragraph → bullet points

## What's Preserved

- All code blocks (verbatim)
- All URLs and paths
- All numbers, versions, dates
- All technical terms
- Table structure
- Heading hierarchy

## Composability

```yaml
domain: density
scope: files
composable: true
yields_to: [process, craft]
```

Compress owns **file-level density**. NOT live responses (that's caveman).

## Related Skills

- [Caveman](./caveman) — density for live responses
- [Documenter](./documenter) — content skill that yields to compress

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/compress/SKILL.md)
