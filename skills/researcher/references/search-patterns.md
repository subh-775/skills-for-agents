# Search Patterns — Advanced Query Techniques

Deep reference for researcher skill. Loaded when user needs advanced search strategies or troubleshooting search failures.

---

## Query Construction

### Basic Patterns

```
[topic] official documentation
[topic] tutorial [year]
[topic] vs [alternative]
[topic] benchmark
[topic] best practices
[topic] getting started
```

### Site-Specific Patterns

```
site:github.com [topic] stars:>100
site:github.com [topic] is:issue [problem]
site:github.com [topic] is:pr [feature]
site:arxiv.org [topic]
site:reddit.com/r/MachineLearning [topic]
site:stackoverflow.com [topic] [error]
site:.cn [topic] (Chinese sources)
```

### Advanced Operators

```
"exact phrase" — force exact match
[topic] -[exclude] — exclude term
[topic] OR [alternative] — either term
[topic] * [term] — wildcard
[topic] AROUND(5) [term] — terms within 5 words
filetype:pdf [topic] — specific file type
```

### Chinese Search Patterns

```
[topic] 中文 — Chinese language results
[topic] 博客 — blogs
[topic] 教程 — tutorials
[topic] 性能 — performance
[topic] 对比 — comparison
[topic] 优化 — optimization
[topic] 实验 — experiments
[topic] 踩坑 — pitfalls/gotchas
[topic] zhihu — Zhihu (Chinese Quora)
[topic] csdn — CSDN (Chinese dev community)
[topic] site:zhihu.com
[topic] site:csdn.net
```

---

## Search Strategies by Topic Type

### Framework/Library Research

```
Phase 1: Official
- [framework] official docs
- site:github.com [framework] README
- [framework] quickstart

Phase 2: Learning
- [framework] tutorial [year]
- [framework] getting started
- [framework] examples

Phase 3: Real-World
- site:github.com [framework] stars:>500
- [framework] production
- [framework] best practices

Phase 4: Issues
- site:github.com [framework] is:issue label:bug
- [framework] common problems
- [framework] gotchas
```

### Hardware Research (TPU/GPU)

```
Phase 1: Official
- [hardware] official documentation
- [hardware] getting started guide
- [hardware] specifications

Phase 2: English Community
- [hardware] tutorial
- [hardware] benchmark
- [hardware] vs [alternative]
- site:github.com [hardware] training

Phase 3: Chinese Community (CRITICAL)
- [hardware] 性能 site:.cn
- [hardware] 对比 site:zhihu.com
- [hardware] 优化 site:csdn.net
- [hardware] 实验结果
- [hardware] MLPerf

Phase 4: Academic
- site:arxiv.org [hardware] training
- [hardware] paper [year]

Phase 5: Real-World
- [hardware] production experience
- [hardware] cost analysis
- site:github.com [hardware] is:issue performance
```

### Algorithm/Technique Research

```
Phase 1: Foundational
- [algorithm] paper
- site:arxiv.org [algorithm]
- [algorithm] original paper

Phase 2: Implementations
- site:github.com [algorithm] implementation
- [algorithm] code
- [algorithm] pytorch OR tensorflow

Phase 3: Explanations
- [algorithm] explained
- [algorithm] intuition
- [algorithm] tutorial

Phase 4: Comparisons
- [algorithm] vs [alternative]
- [algorithm] benchmark
- [algorithm] ablation study

Phase 5: Cutting-Edge
- [algorithm] [year]
- [algorithm] improvements
- [algorithm] variants
```

### Troubleshooting Research

```
Phase 1: Exact Error
- "[exact error message]"
- site:github.com "[error message]"
- site:stackoverflow.com "[error message]"

Phase 2: Contextual
- [library] [error keyword]
- [library] [error keyword] [year]

Phase 3: Related Issues
- site:github.com [library] is:issue [error keyword]
- [library] known issues
- [library] breaking changes [version]

Phase 4: Workarounds
- [error keyword] workaround
- [error keyword] fix
- [error keyword] solution
```

---

## Source Quality Indicators

### High-Quality Signals

**Official Docs:**
- ✅ Maintained by project maintainers
- ✅ Up-to-date (check last update date)
- ✅ Comprehensive API reference
- ✅ Working code examples

**GitHub Repos:**
- ✅ Stars >100 (for niche topics) or >1000 (for popular topics)
- ✅ Recent commits (within last 6 months)
- ✅ Active issues/PRs
- ✅ Good README with examples
- ✅ Tests present

**Blogs:**
- ✅ Author is maintainer or known expert
- ✅ Published recently (within 2 years for fast-moving tech)
- ✅ Working code examples
- ✅ Explains reasoning, not just steps
- ✅ Comments/discussion show engagement

**Chinese Blogs:**
- ✅ Detailed ablation studies with tables/graphs
- ✅ Reproducible experiments with code
- ✅ Hardware-specific optimizations
- ✅ Performance numbers with methodology
- ✅ Published on known platforms (Zhihu, CSDN, personal blogs of researchers)

**Academic Papers:**
- ✅ Recent (within 2 years for ML, 5 years for foundational)
- ✅ High citation count (relative to age)
- ✅ Code available
- ✅ Reproducible results
- ✅ Published at top venues (NeurIPS, ICML, ICLR, etc.)

**Community Discussions:**
- ✅ Upvoted/accepted answers
- ✅ Responses from maintainers
- ✅ Recent activity
- ✅ Multiple people confirming solution

### Low-Quality Signals

- ❌ No date or very old (>3 years for fast-moving tech)
- ❌ No code examples or broken examples
- ❌ Vague explanations without reasoning
- ❌ Contradicts official docs without explanation
- ❌ No engagement (no comments, no stars, no upvotes)
- ❌ Clickbait titles ("This ONE TRICK...")
- ❌ Paywalled without preview
- ❌ Auto-generated content (SEO spam)

---

## Handling Search Failures

### No Results Found

**Diagnosis:**
- Query too specific?
- Wrong terminology?
- Topic too new?
- Topic too niche?

**Solutions:**
1. **Broaden query**: Remove constraints
   - `v5e-8 TPU pytorch training` → `v5e-8 TPU`
   - `specific-library-v2.3.1 bug` → `specific-library bug`

2. **Try synonyms**:
   - `TPU` → `tensor processing unit`
   - `GPU` → `graphics card` → `accelerator`
   - `optimization` → `performance tuning`

3. **Search parent topic**:
   - `specific-feature` → `library-name`
   - `v5e-8 TPU` → `TPU v5`

4. **Check if topic exists**:
   - Search for official announcement
   - Check if name/version is correct

### Too Many Irrelevant Results

**Diagnosis:**
- Query too broad?
- Common term with multiple meanings?
- SEO spam?

**Solutions:**
1. **Add specificity**:
   - `python` → `python machine learning`
   - `transformer` → `transformer neural network` (not electrical transformer)

2. **Use exclusions**:
   - `python -snake`
   - `transformer -electrical -power`

3. **Use site filters**:
   - `site:github.com [topic]`
   - `site:arxiv.org [topic]`

4. **Use date filters**:
   - `[topic] after:2024`
   - `[topic] [current year]`

### Conflicting Information

**Diagnosis:**
- Sources from different time periods?
- Different versions of library?
- Different use cases?
- One source is wrong?

**Solutions:**
1. **Check dates**: Newer info usually correct for fast-moving tech
2. **Check versions**: API may have changed between versions
3. **Check authority**: Maintainer > experienced user > random blog
4. **Cross-reference**: Find third source to break tie
5. **Note conflict**: Report both views with context

### Outdated Information

**Diagnosis:**
- All results are old?
- Library has changed significantly?
- Best practices have evolved?

**Solutions:**
1. **Force recent results**:
   - `[topic] [current year]`
   - `[topic] after:2024`

2. **Check release notes**:
   - `[library] changelog`
   - `[library] what's new`

3. **Check GitHub**:
   - Recent commits
   - Recent issues/PRs
   - Migration guides

4. **Flag as outdated**: Note in output that info may be dated

---

## Multi-Language Search Strategy

### When to Search Chinese Sources

**Always search Chinese for:**
- Hardware (TPUs, GPUs, accelerators)
- ML training optimization
- Distributed training
- Performance benchmarks
- Ablation studies
- Cost optimization
- Hardware comparisons

**Sometimes search Chinese for:**
- Popular frameworks (PyTorch, TensorFlow)
- Cloud platforms (especially Alibaba Cloud, Tencent Cloud)
- Mobile development (especially Android in China)
- Game development

**Rarely search Chinese for:**
- Web frameworks (unless China-specific)
- Frontend libraries (unless China-specific)
- General programming concepts

### Chinese Search Workflow

```
Step 1: Identify Chinese term
- Use English term + 中文 to find translation
- Or search English term on Zhihu/CSDN (they'll use Chinese term)

Step 2: Search with Chinese term
- [Chinese term] site:zhihu.com
- [Chinese term] site:csdn.net
- [Chinese term] 博客

Step 3: Search for specific content types
- [Chinese term] 性能对比 (performance comparison)
- [Chinese term] 实验结果 (experimental results)
- [Chinese term] 优化技巧 (optimization techniques)
- [Chinese term] 踩坑 (pitfalls)

Step 4: Verify with English sources
- Cross-reference findings
- Check if techniques apply to your context
```

### Translation Tips

Common technical terms in Chinese:
- 性能 (xìngnéng) = performance
- 优化 (yōuhuà) = optimization
- 对比 (duìbǐ) = comparison
- 实验 (shíyàn) = experiment
- 训练 (xùnliàn) = training
- 模型 (móxíng) = model
- 教程 (jiàochéng) = tutorial
- 博客 (bókè) = blog
- 踩坑 (cǎikēng) = pitfalls (literal: stepping in holes)
- 深度学习 (shēndù xuéxí) = deep learning
- 机器学习 (jīqì xuéxí) = machine learning

---

## Source Organization

### During Research

Keep sources organized by type as you find them:

```
Official:
- [link] — [description]

GitHub:
- [link] — [description]

English Blogs:
- [link] — [description]

Chinese Blogs:
- [link] — [description]

Academic:
- [link] — [description]

Community:
- [link] — [description]

Benchmarks:
- [link] — [description]
```

### In Output

Present sources grouped by type, most authoritative first:

```
## Sources

### Official Documentation
- [Title](link) — [one sentence description]

### GitHub Repositories
- [Title](link) — [one sentence description]

### Tutorials & Guides
- [Title](link) — [one sentence description]

### Chinese Sources
- [Title](link) — [one sentence description]

### Academic Papers
- [Title](link) — [one sentence description]

### Community Discussions
- [Title](link) — [one sentence description]

### Benchmarks
- [Title](link) — [one sentence description]
```

---

## Quality Assurance Checklist

Before delivering research:

### Coverage
- [ ] Official docs found and reviewed
- [ ] GitHub examples found (if applicable)
- [ ] English blogs/tutorials found
- [ ] Chinese blogs checked (for hardware/ML topics)
- [ ] Community discussions checked
- [ ] Benchmarks found (if applicable)
- [ ] Academic papers checked (for algorithms/techniques)

### Recency
- [ ] All sources dated
- [ ] Outdated sources flagged
- [ ] Recent developments noted
- [ ] Version compatibility checked

### Authority
- [ ] Source credibility assessed
- [ ] Maintainer input prioritized
- [ ] Conflicts between sources resolved
- [ ] Unverified claims flagged

### Actionability
- [ ] Code examples included
- [ ] Next steps clear
- [ ] Links working
- [ ] Enough context to act

### Diversity
- [ ] Multiple source types
- [ ] Multiple perspectives
- [ ] Not just docs, not just blogs
- [ ] Chinese sources for hardware/ML

---

## Advanced Techniques

### Reverse Image Search

For diagrams, architecture images:
1. Find image in blog/paper
2. Reverse image search to find original source
3. Often leads to official docs or better explanations

### GitHub Code Search

For implementation patterns:
```
site:github.com [pattern] language:python
site:github.com "exact code snippet"
site:github.com [library] path:examples/
```

### Time-Based Search

For tracking evolution:
```
[topic] before:2023 — old approach
[topic] after:2024 — new approach
[topic] 2022..2024 — specific range
```

### Related Search

After finding one good source:
```
related:[url] — find similar pages
site:[domain] [topic] — more from same site
author:[name] [topic] — more from same author
```

### Academic Search Chains

1. Find key paper on topic
2. Check "Cited by" to find newer work
3. Check "References" to find foundational work
4. Check author's other papers
5. Check papers from same venue/year

---

## Emergency Fallbacks

### When All Searches Fail

1. **Search for the searchers**: `how to learn [topic]`, `[topic] resources`
2. **Search for communities**: `[topic] discord`, `[topic] slack`, `[topic] forum`
3. **Search for courses**: `[topic] course`, `[topic] tutorial series`
4. **Search for books**: `[topic] book`, `[topic] O'Reilly`
5. **Ask in output**: "Limited info found. Recommend asking in [community] or checking [related topic]."

### When Topic is Too New

1. **GitHub trending**: Check if repos exist but not documented yet
2. **Twitter/X**: Search for announcements
3. **Arxiv**: Check preprints
4. **Conference workshops**: Check recent conference proceedings
5. **Note in output**: "Cutting-edge topic. Info limited. Check back in [timeframe]."

### When Topic is Too Niche

1. **Search parent topic**: Learn general area first
2. **Search for similar**: `similar to [topic]`, `[topic] alternative`
3. **Search for use case**: `[use case] solution` might lead to topic
4. **Note in output**: "Niche topic. Limited resources. Here's what exists + related areas to explore."
