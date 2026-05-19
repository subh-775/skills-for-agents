# Researcher

Deep web research skill. Investigates, cross-references, synthesizes, and surfaces information the user can act on. Every session produces verifiable claims with sources.

## Domain

**Content** — controls the substance of gathered information, sources, synthesis, and findings.

## When to Use

- "research X", "find info about Y", "what's the latest on Z"
- "look up", "investigate", "gather context on", "deep dive", "explore topic"
- Comparing technologies, frameworks, or approaches
- Exploring unfamiliar territory (new hardware, library, paradigm)
- Benchmarks, ablation studies, performance comparisons
- ML research, bug investigation, optimization research

## Goal Detection

| User Goal | Depth | Searches |
|-----------|-------|----------|
| **Context feed** | Enough to start coding | 3-4 |
| **Overview** | Mental model of a domain | 5-7 |
| **Deep dive** | Expert-level understanding | 10-18 |
| **Comparison** | Decision-making data | 6-8 |
| **Troubleshooting** | Fix a specific problem | 4-6 |
| **Cutting-edge** | Bleeding-edge info | 10-18 |
| **Hypothesis test** | Validate idea before building | 5-8 |

## Search Strategy (6 Layers)

| Layer | Source | When |
|-------|--------|------|
| **1. Ground Truth** | Official docs, GitHub repos, release notes | Always start here |
| **2. Community** | Reddit, HN, Discord, Stack Overflow | Real-world experience |
| **3. Chinese Tech** | Zhihu, CSDN, Juejin, WeChat | ML/AI/hardware depth |
| **4. Video** | Bilibili, YouTube | Intuition and walkthroughs |
| **5. Academic** | arxiv MCP, Semantic Scholar | Papers and citation graphs |
| **6. Expert** | Engineering blogs, grey literature, Internet Archive | Production signal |

**Chinese search keywords:** `[topic] 原理` (principle), `[topic] 实战` (practical), `[topic] 踩坑` (pitfalls), `[topic] 消融实验` (ablations).

**Multi-Angle Pattern:** Paraphrase every query 2-3 ways using different terminology. Improves retrieval by up to 18%.

## Key Concepts

**Cross-referencing**: A claim from one source is a hypothesis. Same claim from three independent sources is a finding. Flag contradictions explicitly.

**Date everything**: Stamp every finding with source date. Flag anything >18 months old unless foundational.

**Authority ranking**: Maintainers > company engineers > experienced users > random blogs > AI-generated content.

**Source diversity**: If you're only finding English sources on an ML/AI topic, you've missed half the signal. Chinese sources are primary for ML/AI/hardware.

**Sentiment mining**: Search for "I regret", "pain point", "migrated away", "in production", "wish I knew" to find real experience.

## Output Formats

| Goal | Format |
|------|--------|
| Context feed | Quick summary + getting-started links + gotchas |
| Overview | What, how, key features, ecosystem, getting started, gotchas |
| Deep dive | Executive summary, architecture, benchmarks, implementation, comparisons |
| Comparison | Quick recommendation, feature matrix, performance data |
| Hypothesis test | Prior work, limitations, failure modes, skeptical review |
| Diagnostic | Symptom, likely causes + verification, known solutions |

Every output ends with a **Sources section** organized by type with dates.

## Composability

```yaml
domain: content
composable: true
yields_to: [process, voice]
```

Researcher owns **content** — the substance of gathered information. It provides data for decisions but does not make decisions.

### When Researcher Leads

- Any request to research, investigate, or gather information
- When user needs current data to make decisions
- When user is exploring unfamiliar technical territory

### When Researcher Defers

| Other Skill's Domain | What Researcher Does |
|---------------------|----------------------|
| **Process** (e.g. planner, postmortem) | Gathers information. Process controls output structure. |
| **Voice** (e.g. blogger, caveman) | Produces neutral prose. Voice adjusts tone. |
| **Density** (e.g. caveman) | Gathers comprehensive information. Density compresses. |

## Related Skills

- [Planner](./planner) — upstream: research feeds into stack decisions and DESIGN.md
- [Postmortem](./postmortem) — gather context for root cause analysis
- [Blogger](./blogger) — compose: research findings turned into blog posts
- [Documenter](./documenter) — research feeds into technical documentation

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skills/researcher/SKILL.md) — complete guide with all search strategies
- [SIP Framework](/guide/sip-framework) — how researcher composes
