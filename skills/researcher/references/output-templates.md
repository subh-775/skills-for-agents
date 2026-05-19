# Output Templates — Structured Research Deliverables

Reference templates for different research output types. Adapt based on findings and user needs.

---

## Template Selection Guide

| User Goal | Template | When to Use |
|-----------|----------|-------------|
| Quick context to start coding | Context Feed | User needs to start implementing soon |
| Understanding how something works | Overview | User is exploring, learning |
| Expert-level deep knowledge | Deep Dive | User optimizing, architecting, or researching |
| Choosing between options | Comparison | User making technology decisions |
| Solving specific problem | Troubleshooting | User has error or issue |
| Tracking new developments | Cutting-Edge | User wants bleeding-edge info |
| Hardware/infrastructure decisions | Hardware Analysis | User evaluating TPUs, GPUs, cloud |

---

## Context Feed Template

**Goal**: Get user coding quickly with minimal reading.

```markdown
# [Topic] — Quick Context

## What It Is
[1-2 sentences: what is it, what problem does it solve]

## Key Concepts
- **[Concept 1]**: [One sentence explanation]
- **[Concept 2]**: [One sentence explanation]
- **[Concept 3]**: [One sentence explanation]

## Quick Start

### Installation
```bash
[installation command]
```

### Basic Usage
```[language]
[minimal working example — 10-20 lines max]
```

### Common Patterns
```[language]
[2-3 common patterns user will need]
```

## Gotchas
- **[Issue 1]**: [Problem + quick fix]
- **[Issue 2]**: [Problem + quick fix]

## Next Steps
- [Link to official tutorial]
- [Link to examples repo]
- [Link to API reference]

## Sources
- [Official docs](link)
- [Best tutorial found](link)
- [GitHub examples](link)
```

**Length target**: 200-400 words

---

## Overview Template

**Goal**: Build mental model of how it works.

```markdown
# [Topic] — Overview

## What It Is
[2-3 paragraphs:
- What is it?
- What problem does it solve?
- When should you use it?
- When should you NOT use it?]

## How It Works

### Architecture
[Explain internal structure — use analogies if helpful]

[If diagram found, include it or describe it]

### Key Components
- **[Component 1]**: [What it does, why it matters]
- **[Component 2]**: [What it does, why it matters]
- **[Component 3]**: [What it does, why it matters]

### Data Flow
[Explain how data moves through the system]

## Key Features

### [Feature 1]
[What it is, why it matters, when to use]

```[language]
[code example]
```

### [Feature 2]
[What it is, why it matters, when to use]

```[language]
[code example]
```

### [Feature 3]
[What it is, why it matters, when to use]

```[language]
[code example]
```

## Use Cases

### [Use Case 1]
**When**: [Scenario]
**Why**: [Reason this tool fits]
**Example**: [Brief example or link]

### [Use Case 2]
**When**: [Scenario]
**Why**: [Reason this tool fits]
**Example**: [Brief example or link]

## Ecosystem

### Related Tools
- **[Tool 1]**: [How it relates]
- **[Tool 2]**: [How it relates]

### Integrations
- [Integration 1]
- [Integration 2]

## Getting Started

### Setup
```bash
[installation and setup commands]
```

### Hello World
```[language]
[complete working example]
```

### Common Patterns

#### [Pattern 1]
```[language]
[code example]
```

#### [Pattern 2]
```[language]
[code example]
```

## Best Practices
- **[Practice 1]**: [Why it matters]
- **[Practice 2]**: [Why it matters]
- **[Practice 3]**: [Why it matters]

## Common Pitfalls
- **[Pitfall 1]**: [Problem + solution]
- **[Pitfall 2]**: [Problem + solution]
- **[Pitfall 3]**: [Problem + solution]

## Performance Considerations
[Key performance characteristics, when it's fast, when it's slow]

## Sources

### Official
- [Docs](link)
- [GitHub](link)

### Tutorials
- [Tutorial 1](link)
- [Tutorial 2](link)

### Community
- [Discussion 1](link)
- [Discussion 2](link)
```

**Length target**: 800-1500 words

---

## Deep Dive Template

**Goal**: Expert-level understanding for optimization and architecture.

```markdown
# [Topic] — Deep Dive

## Executive Summary
[3-4 sentences: what is it, key findings, main takeaways, recommendation]

## Background

### History
[How it came to be, what problem it solved, evolution]

### Motivation
[Why it exists, what alternatives existed, what gap it filled]

### Current State
[Where it is now, adoption, maturity, future direction]

## Architecture

### High-Level Design
[Overall structure, design philosophy, key decisions]

### Internal Components

#### [Component 1]
**Purpose**: [What it does]
**Implementation**: [How it works internally]
**Tradeoffs**: [What was sacrificed for what benefit]

#### [Component 2]
[Same structure]

### Data Flow
[Detailed explanation of how data moves through system]

### Design Decisions
- **[Decision 1]**: [What was chosen, why, what was sacrificed]
- **[Decision 2]**: [Same]

## Performance Characteristics

### Benchmarks

#### [Benchmark 1]
**Setup**: [Hardware, software, configuration]
**Results**: [Numbers with units]
**Source**: [Link to benchmark]

[Table of results if multiple scenarios]

#### [Benchmark 2]
[Same structure]

### Ablation Studies

[If found, especially from Chinese sources]

**Study**: [What was tested]
**Findings**: [Key results]
**Implications**: [What this means for users]

### Performance Analysis
- **Strengths**: [Where it excels, why]
- **Weaknesses**: [Where it struggles, why]
- **Scaling**: [How it behaves at scale]

## Implementation Guide

### Basic Usage
```[language]
[complete working example]
```

### Advanced Patterns

#### [Pattern 1]
**Use Case**: [When to use this]
**Implementation**:
```[language]
[code example]
```
**Tradeoffs**: [What you gain/lose]

#### [Pattern 2]
[Same structure]

### Production Considerations
- **[Consideration 1]**: [What to watch for, how to handle]
- **[Consideration 2]**: [Same]

## Optimization Techniques

### [Optimization 1]
**Problem**: [What you're optimizing]
**Technique**: [How to optimize]
**Impact**: [Expected improvement]
**Source**: [Where this came from]

```[language]
[code example]
```

### [Optimization 2]
[Same structure]

## Comparisons

### vs [Alternative 1]

#### Feature Comparison
| Feature | [Topic] | [Alternative 1] |
|---------|---------|-----------------|
| [Feature 1] | [Status] | [Status] |
| [Feature 2] | [Status] | [Status] |

#### Performance Comparison
[Benchmark data comparing the two]

#### When to Choose [Topic]
- [Scenario 1]
- [Scenario 2]

#### When to Choose [Alternative 1]
- [Scenario 1]
- [Scenario 2]

### vs [Alternative 2]
[Same structure]

## Edge Cases & Gotchas

### [Edge Case 1]
**Scenario**: [When this happens]
**Problem**: [What goes wrong]
**Solution**: [How to handle]
**Source**: [GitHub issue, discussion, etc.]

### [Edge Case 2]
[Same structure]

## Real-World Usage

### Case Study 1: [Company/Project]
**Context**: [What they were building]
**Challenge**: [Problem they faced]
**Solution**: [How they used this tool]
**Results**: [Outcome]
**Source**: [Link]

### Case Study 2
[Same structure]

## Current State & Future

### Recent Developments
- [Development 1] — [Date, impact]
- [Development 2] — [Date, impact]

### Roadmap
[Planned features, timeline if known]

### Community Sentiment
[What community thinks, common complaints, praise]

## Recommendations

### When to Use
- [Scenario 1]
- [Scenario 2]

### When to Avoid
- [Scenario 1]
- [Scenario 2]

### Migration Path
[If coming from alternative, how to migrate]

## Sources

### Official Documentation
- [Link] — [Description]

### GitHub Repositories
- [Link] — [Description]

### English Blogs & Tutorials
- [Link] — [Description]

### Chinese Sources
- [Link] — [Description]

### Academic Papers
- [Link] — [Description]

### Benchmarks
- [Link] — [Description]

### Community Discussions
- [Link] — [Description]

### Case Studies
- [Link] — [Description]
```

**Length target**: 2000-4000 words

---

## Comparison Template

**Goal**: Help user choose between options.

```markdown
# [Topic A] vs [Topic B] — Comparison

## Quick Recommendation

**Choose [Topic A] if**: [Scenario 1], [Scenario 2]

**Choose [Topic B] if**: [Scenario 1], [Scenario 2]

**TL;DR**: [One sentence recommendation]

## Overview

### [Topic A]
[2-3 sentences: what it is, main strengths]

### [Topic B]
[2-3 sentences: what it is, main strengths]

## Feature Comparison

| Feature | [Topic A] | [Topic B] | Winner |
|---------|-----------|-----------|--------|
| [Feature 1] | [Status/Details] | [Status/Details] | [A/B/Tie] |
| [Feature 2] | [Status/Details] | [Status/Details] | [A/B/Tie] |
| [Feature 3] | [Status/Details] | [Status/Details] | [A/B/Tie] |
| [Feature 4] | [Status/Details] | [Status/Details] | [A/B/Tie] |

## Performance Comparison

### Benchmark: [Scenario 1]
**Setup**: [Hardware, software, configuration]

| Metric | [Topic A] | [Topic B] | Winner |
|--------|-----------|-----------|--------|
| [Metric 1] | [Number] | [Number] | [A/B/Tie] |
| [Metric 2] | [Number] | [Number] | [A/B/Tie] |

**Source**: [Link to benchmark]

### Benchmark: [Scenario 2]
[Same structure]

### Performance Summary
- **[Topic A] excels at**: [Scenarios]
- **[Topic B] excels at**: [Scenarios]

## Ease of Use

### Learning Curve
- **[Topic A]**: [Steep/Moderate/Gentle — explanation]
- **[Topic B]**: [Steep/Moderate/Gentle — explanation]

### Documentation Quality
- **[Topic A]**: [Rating/10 — why]
- **[Topic B]**: [Rating/10 — why]

### Community Support
- **[Topic A]**: [Size, activity, helpfulness]
- **[Topic B]**: [Size, activity, helpfulness]

### Developer Experience
- **[Topic A]**: [Pros and cons]
- **[Topic B]**: [Pros and cons]

## Ecosystem

### Libraries & Integrations
- **[Topic A]**: [Key libraries, integrations]
- **[Topic B]**: [Key libraries, integrations]

### Tooling
- **[Topic A]**: [Available tools]
- **[Topic B]**: [Available tools]

## Production Readiness

### Maturity
- **[Topic A]**: [Age, stability, breaking changes history]
- **[Topic B]**: [Age, stability, breaking changes history]

### Company Backing
- **[Topic A]**: [Who maintains it, funding, commitment]
- **[Topic B]**: [Who maintains it, funding, commitment]

### Production Usage
- **[Topic A]**: [Companies using it, scale]
- **[Topic B]**: [Companies using it, scale]

## Cost Considerations

### Development Cost
- **[Topic A]**: [Time to implement, complexity]
- **[Topic B]**: [Time to implement, complexity]

### Operational Cost
- **[Topic A]**: [Resource usage, infrastructure needs]
- **[Topic B]**: [Resource usage, infrastructure needs]

### Maintenance Cost
- **[Topic A]**: [Ongoing effort, upgrade frequency]
- **[Topic B]**: [Ongoing effort, upgrade frequency]

## Migration Stories

### [Company/Project] migrated from [A] to [B]
**Why**: [Reason for migration]
**Experience**: [How it went]
**Outcome**: [Result]
**Source**: [Link]

### [Company/Project] migrated from [B] to [A]
[Same structure]

## Decision Matrix

### Choose [Topic A] When:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

### Choose [Topic B] When:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

### Red Flags for [Topic A]:
- [Warning 1]
- [Warning 2]

### Red Flags for [Topic B]:
- [Warning 1]
- [Warning 2]

## Migration Path

### From [Topic A] to [Topic B]
**Difficulty**: [Easy/Moderate/Hard]
**Steps**: [High-level migration steps]
**Gotchas**: [Common issues]
**Resources**: [Migration guides, tools]

### From [Topic B] to [Topic A]
[Same structure]

## Final Recommendation

[2-3 paragraphs synthesizing everything into clear recommendation based on common scenarios]

## Sources

### Benchmarks
- [Link] — [Description]

### Migration Stories
- [Link] — [Description]

### Community Discussions
- [Link] — [Description]

### Official Docs
- [Topic A](link)
- [Topic B](link)
```

**Length target**: 1500-2500 words

---

## Troubleshooting Template

**Goal**: Solve specific problem quickly.

```markdown
# [Problem/Error] — Troubleshooting

## Problem Summary
[1-2 sentences describing the issue]

## Quick Fixes

### Fix 1: [Most Common Solution]
**Try this first** — solves [X]% of cases

```[language]
[code or command]
```

**Why this works**: [Explanation]

### Fix 2: [Second Most Common]
**If Fix 1 didn't work**

```[language]
[code or command]
```

**Why this works**: [Explanation]

## Root Causes

### Cause 1: [Most Common Cause]
**Symptoms**: [How to identify this is the cause]
**Solution**: [Detailed fix]
**Prevention**: [How to avoid in future]

### Cause 2: [Second Most Common]
[Same structure]

## Diagnostic Steps

1. **Check [Thing 1]**
   ```bash
   [diagnostic command]
   ```
   Expected output: [What you should see]
   If different: [What it means]

2. **Check [Thing 2]**
   [Same structure]

3. **Check [Thing 3]**
   [Same structure]

## Related Issues

### Similar Error: [Related Error 1]
**Difference**: [How to distinguish]
**Solution**: [Link or brief fix]

### Similar Error: [Related Error 2]
[Same structure]

## Version-Specific Issues

### [Version Range 1]
**Issue**: [What's broken]
**Workaround**: [How to fix]
**Status**: [Fixed in version X / still open]

### [Version Range 2]
[Same structure]

## Community Solutions

### Solution from [Source 1]
**Context**: [When this applies]
**Approach**: [What they did]
**Result**: [Did it work?]
**Source**: [Link]

### Solution from [Source 2]
[Same structure]

## When to Give Up

If none of the above work:
- [Alternative approach 1]
- [Alternative approach 2]
- [Where to ask for help — link to forum/Discord/issues]

## Prevention

To avoid this in future:
- [Prevention step 1]
- [Prevention step 2]

## Sources
- [GitHub issue](link)
- [Stack Overflow](link)
- [Blog post](link)
- [Official docs](link)
```

**Length target**: 500-1000 words

---

## Hardware Analysis Template

**Goal**: Evaluate hardware for specific use case.

```markdown
# [Hardware] — Analysis for [Use Case]

## Quick Verdict

**Recommendation**: [Use it / Consider alternatives / Avoid]

**Best for**: [Scenario 1], [Scenario 2]

**Avoid for**: [Scenario 1], [Scenario 2]

## Specifications

| Spec | Value | Comparison |
|------|-------|------------|
| [Spec 1] | [Value] | [vs alternative] |
| [Spec 2] | [Value] | [vs alternative] |
| [Spec 3] | [Value] | [vs alternative] |

## Performance Benchmarks

### [Benchmark 1]: [Task Type]
**Setup**: [Model, batch size, precision, etc.]

| Hardware | Throughput | Latency | Cost/Hour | Cost/Sample |
|----------|------------|---------|-----------|-------------|
| [This Hardware] | [Number] | [Number] | [Number] | [Number] |
| [Alternative 1] | [Number] | [Number] | [Number] | [Number] |
| [Alternative 2] | [Number] | [Number] | [Number] | [Number] |

**Source**: [Link]

### [Benchmark 2]: [Task Type]
[Same structure]

### Performance Summary
- **Strengths**: [Where it excels]
- **Weaknesses**: [Where it struggles]
- **Sweet spot**: [Optimal use case]

## Cost Analysis

### Training Cost
**Scenario**: [Specific training job]
- **[This Hardware]**: $[X]/hour × [Y] hours = $[Z]
- **[Alternative]**: $[X]/hour × [Y] hours = $[Z]
- **Savings**: [Percentage]

### Inference Cost
**Scenario**: [Specific inference workload]
- **[This Hardware]**: $[X]/1M requests
- **[Alternative]**: $[X]/1M requests
- **Savings**: [Percentage]

### Total Cost of Ownership
[Consider: hardware cost, power, cooling, maintenance, opportunity cost]

## Software Ecosystem

### Framework Support
- **PyTorch**: [Status, maturity, gotchas]
- **TensorFlow/JAX**: [Status, maturity, gotchas]
- **Other**: [Status]

### Library Compatibility
- **[Library 1]**: [Supported? Performance?]
- **[Library 2]**: [Supported? Performance?]

### Tooling
- **Profiling**: [Available tools]
- **Debugging**: [Available tools]
- **Monitoring**: [Available tools]

## Setup & Configuration

### Getting Started
```bash
[setup commands]
```

### Optimal Configuration
```python
[configuration code]
```

### Common Gotchas
- **[Gotcha 1]**: [Problem + solution]
- **[Gotcha 2]**: [Problem + solution]

## Optimization Techniques

### [Optimization 1]
**Impact**: [Expected speedup]
**Difficulty**: [Easy/Medium/Hard]
**Implementation**:
```[language]
[code]
```
**Source**: [Link, especially Chinese blogs]

### [Optimization 2]
[Same structure]

## Real-World Experience

### Case Study 1: [Company/Project]
**Use Case**: [What they're doing]
**Hardware**: [Configuration]
**Results**: [Performance, cost, experience]
**Source**: [Link]

### Case Study 2
[Same structure]

## Comparison with Alternatives

### vs [Alternative 1]

| Aspect | [This Hardware] | [Alternative 1] | Winner |
|--------|-----------------|-----------------|--------|
| Performance | [Details] | [Details] | [Winner] |
| Cost | [Details] | [Details] | [Winner] |
| Ease of Use | [Details] | [Details] | [Winner] |
| Ecosystem | [Details] | [Details] | [Winner] |

**Choose [This Hardware] when**: [Scenarios]
**Choose [Alternative 1] when**: [Scenarios]

### vs [Alternative 2]
[Same structure]

## Decision Factors

### Choose [This Hardware] If:
- [Factor 1]
- [Factor 2]
- [Factor 3]

### Consider Alternatives If:
- [Factor 1]
- [Factor 2]
- [Factor 3]

## Getting Started Guide

### Step 1: [Setup]
[Instructions]

### Step 2: [First Job]
[Instructions]

### Step 3: [Optimization]
[Instructions]

## Sources

### Official Documentation
- [Link]

### Benchmarks
- [Link] — [Description]

### Chinese Sources (Ablations)
- [Link] — [Description]

### Case Studies
- [Link] — [Description]

### Community Discussions
- [Link] — [Description]
```

**Length target**: 1500-2500 words

---

## Cutting-Edge Template

**Goal**: Track bleeding-edge developments.

```markdown
# [Topic] — Cutting-Edge Developments

## What's New

### [Development 1]
**Date**: [When announced]
**Source**: [Paper/GitHub/Blog]
**Status**: [Preprint/Released/In Development]

**What it is**: [Brief explanation]

**Why it matters**: [Significance]

**Availability**: [Can you use it? How?]

### [Development 2]
[Same structure]

## Key Papers (Last 6 Months)

### [Paper 1]
**Title**: [Full title]
**Authors**: [Key authors, affiliations]
**Venue**: [Arxiv/Conference]
**Date**: [Publication date]

**Contribution**: [What's new]

**Results**: [Key findings]

**Code**: [Available? Link]

**Impact**: [Why it matters]

**Link**: [Arxiv/venue link]

### [Paper 2]
[Same structure]

## Active Development

### [Project 1]
**Repository**: [Link]
**Activity**: [Commits, stars, recent PRs]
**Status**: [Alpha/Beta/Stable]

**What it does**: [Brief explanation]

**Why watch it**: [Potential impact]

**Try it**: [How to get started]

### [Project 2]
[Same structure]

## Community Buzz

### From Twitter/X
- [Tweet/thread link] — [Key point]
- [Tweet/thread link] — [Key point]

### From Reddit/HN
- [Discussion link] — [Key point]
- [Discussion link] — [Key point]

### From Discord/Slack
- [Community] discussing [topic] — [Key point]

## Benchmarks & Ablations

### [Benchmark 1]
**Source**: [Link, especially Chinese blogs]
**Date**: [When published]

**Setup**: [What was tested]

**Results**: [Key numbers]

**Takeaway**: [What this means]

### [Benchmark 2]
[Same structure]

## What to Watch

### Short-term (1-3 months)
- [Development 1] — [Expected milestone]
- [Development 2] — [Expected milestone]

### Medium-term (3-6 months)
- [Development 1] — [Expected milestone]
- [Development 2] — [Expected milestone]

### Long-term (6-12 months)
- [Development 1] — [Expected milestone]
- [Development 2] — [Expected milestone]

## How to Stay Updated

### Key Sources
- [Blog/Newsletter] — [What they cover]
- [Twitter account] — [Who to follow]
- [Subreddit] — [What's discussed]
- [GitHub org] — [What to watch]

### Search Queries
- [Query 1] — [What it finds]
- [Query 2] — [What it finds]

## Caveats

⚠️ **This is cutting-edge**: Not production-ready, may change, may not be reproduced yet.

- [Caveat 1]
- [Caveat 2]

## Sources

### Papers
- [Link]

### GitHub
- [Link]

### Blogs
- [Link]

### Chinese Sources
- [Link]

### Community
- [Link]
```

**Length target**: 1000-2000 words

---

## Template Adaptation Guidelines

**Always adapt templates to findings:**
- If no benchmarks found, skip benchmark section
- If no Chinese sources found (non-hardware topic), skip that section
- If topic is simple, use shorter template
- If topic is complex, expand sections

**Prioritize actionability:**
- Code examples over prose
- Links over descriptions
- Specific numbers over vague claims
- Recent sources over old sources

**Match user's goal:**
- Context feed → minimal, actionable
- Overview → balanced, educational
- Deep dive → comprehensive, expert-level
- Comparison → decision-focused
- Troubleshooting → solution-focused
