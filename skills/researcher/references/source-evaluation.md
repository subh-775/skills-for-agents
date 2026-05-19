# Source Evaluation — Credibility & Authority Assessment

How to evaluate source quality, detect misinformation, and prioritize conflicting information.

---

## Authority Hierarchy

When sources conflict, use this hierarchy (highest authority first):

### Tier 1: Primary Sources
1. **Official documentation** — maintained by project creators
2. **Source code** — the ground truth
3. **Official release notes** — direct from maintainers
4. **Maintainer statements** — in issues, PRs, discussions

**Why trust**: Direct from source, no interpretation layer

**When to question**: If outdated, if contradicts code, if community reports bugs

### Tier 2: Expert Sources
1. **Papers by original authors** — creators explaining their work
2. **Talks by maintainers** — conference presentations, podcasts
3. **Engineering blogs from companies using it in production** — real-world experience at scale
4. **Known experts' blogs** — recognized authorities in the field

**Why trust**: Deep expertise, real-world validation

**When to question**: If outdated, if context differs from yours, if not reproducible

### Tier 3: Community Sources
1. **High-quality GitHub repos** — well-maintained, many stars, active
2. **Accepted Stack Overflow answers** — upvoted, marked correct
3. **Popular tutorials** — many upvotes/views, recent
4. **Chinese tech blogs with ablations** — detailed experiments, reproducible

**Why trust**: Crowd-validated, practical experience

**When to question**: If old, if low engagement, if contradicts higher tiers

### Tier 4: Unverified Sources
1. **Random blogs** — no clear author expertise
2. **Forum posts** — single user's experience
3. **Social media** — unless from known expert
4. **AI-generated content** — unless verified

**Why use**: Sometimes only source available, may contain useful hints

**When to question**: Always. Verify against higher tiers.

---

## Credibility Indicators

### Strong Credibility Signals

**Author Indicators:**
- ✅ Named author with verifiable identity
- ✅ Author is project maintainer
- ✅ Author works at company that created/uses the tech
- ✅ Author has track record (other quality content, GitHub profile, papers)
- ✅ Author responds to comments/questions

**Content Indicators:**
- ✅ Detailed explanations with reasoning
- ✅ Working code examples (tested, reproducible)
- ✅ Acknowledges limitations and edge cases
- ✅ Cites sources for claims
- ✅ Shows methodology for benchmarks
- ✅ Includes version numbers and dates
- ✅ Discusses tradeoffs, not just benefits

**Engagement Indicators:**
- ✅ High upvotes/stars/citations
- ✅ Positive comments from experts
- ✅ Referenced by other quality sources
- ✅ Active discussion in comments
- ✅ Corrections/updates from author

**Publication Indicators:**
- ✅ Published on reputable platform (official blog, known publication)
- ✅ Recent publication date
- ✅ Peer-reviewed (for academic)
- ✅ Edited/reviewed before publication

### Weak Credibility Signals

**Author Indicators:**
- ⚠️ Anonymous or pseudonymous author
- ⚠️ No verifiable expertise
- ⚠️ No other content from author
- ⚠️ Author doesn't respond to questions

**Content Indicators:**
- ⚠️ Vague explanations without details
- ⚠️ No code examples or broken examples
- ⚠️ Claims without evidence
- ⚠️ No version numbers or dates
- ⚠️ Only discusses benefits, ignores tradeoffs
- ⚠️ Contradicts official docs without explanation

**Engagement Indicators:**
- ⚠️ Low or no engagement
- ⚠️ Negative comments pointing out errors
- ⚠️ Not referenced by other sources
- ⚠️ No discussion

**Publication Indicators:**
- ⚠️ Self-published with no review
- ⚠️ Published on low-quality platform
- ⚠️ Old publication date (>3 years for fast-moving tech)
- ⚠️ Paywalled with no preview

### Red Flags (Likely Unreliable)

- 🚩 Clickbait title ("This ONE TRICK...", "You won't believe...")
- 🚩 No date or very old (>5 years for tech)
- 🚩 Contradicts multiple high-authority sources
- 🚩 No code examples for technical content
- 🚩 Obvious errors in code or explanations
- 🚩 SEO spam (keyword stuffing, auto-generated)
- 🚩 Plagiarized content (copied from other sources)
- 🚩 Affiliate links without disclosure
- 🚩 Claims that sound too good to be true
- 🚩 No methodology for benchmark claims

---

## Evaluating Specific Source Types

### Official Documentation

**Check:**
- Last update date (is it current?)
- Completeness (API reference, examples, guides?)
- Accuracy (does code work? matches source code?)
- Maintenance (active project? recent releases?)

**Trust if:**
- ✅ Recently updated
- ✅ Comprehensive
- ✅ Examples work
- ✅ Active project

**Question if:**
- ⚠️ Outdated (no updates in >1 year)
- ⚠️ Incomplete (missing sections)
- ⚠️ Examples broken
- ⚠️ Abandoned project

### GitHub Repositories

**Check:**
- Stars (popularity indicator)
- Recent commits (active maintenance?)
- Issues (how are they handled?)
- PRs (community contributions?)
- Tests (code quality indicator)
- README (documentation quality)
- License (can you use it?)

**Trust if:**
- ✅ Stars >100 (niche) or >1000 (popular)
- ✅ Commits within last 6 months
- ✅ Issues responded to promptly
- ✅ PRs reviewed and merged
- ✅ Tests present and passing
- ✅ Good README with examples
- ✅ Permissive license

**Question if:**
- ⚠️ Low stars (<10)
- ⚠️ No recent commits (>1 year)
- ⚠️ Many open issues, no responses
- ⚠️ No tests
- ⚠️ Poor/no documentation
- ⚠️ Restrictive license

### Blog Posts

**Check:**
- Author credentials
- Publication date
- Code examples
- Reasoning depth
- Comments/discussion

**Trust if:**
- ✅ Author is known expert or maintainer
- ✅ Published recently (<2 years)
- ✅ Working code examples
- ✅ Explains why, not just what
- ✅ Positive engagement in comments

**Question if:**
- ⚠️ Unknown author
- ⚠️ Old post (>3 years)
- ⚠️ No code or broken code
- ⚠️ Surface-level explanation
- ⚠️ No engagement or negative comments

### Chinese Tech Blogs

**Check:**
- Platform (Zhihu, CSDN, personal blog?)
- Experiment methodology
- Reproducibility
- Data presentation
- Author background

**Trust if:**
- ✅ Published on known platform (Zhihu, CSDN)
- ✅ Detailed methodology (hardware, software versions, settings)
- ✅ Reproducible (code provided, clear steps)
- ✅ Data in tables/graphs with clear labels
- ✅ Author has other quality content

**Question if:**
- ⚠️ Unknown platform
- ⚠️ No methodology details
- ⚠️ Not reproducible
- ⚠️ Vague claims without data
- ⚠️ First/only post from author

**Special note**: Chinese blogs often have more detailed ablation studies than English sources, especially for hardware. Even if author is unknown, if methodology is solid and reproducible, can be valuable.

### Academic Papers

**Check:**
- Venue (top conference/journal?)
- Citation count
- Author affiliations
- Code availability
- Reproducibility

**Trust if:**
- ✅ Published at top venue (NeurIPS, ICML, ICLR, etc.)
- ✅ High citations (relative to age)
- ✅ Authors from reputable institutions
- ✅ Code available
- ✅ Results reproduced by others

**Question if:**
- ⚠️ Unknown venue or predatory journal
- ⚠️ Low/no citations (if not very recent)
- ⚠️ No code available
- ⚠️ Results not reproduced
- ⚠️ Contradicts established knowledge without strong evidence

**Special note**: Preprints (arxiv) are not peer-reviewed. Treat as Tier 3 (community) until published.

### Stack Overflow / Forums

**Check:**
- Answer score (upvotes)
- Accepted answer?
- Answerer reputation
- Date
- Comments

**Trust if:**
- ✅ High score (>10 upvotes)
- ✅ Accepted by questioner
- ✅ Answerer has high reputation
- ✅ Recent answer (<2 years)
- ✅ Positive comments confirming it works

**Question if:**
- ⚠️ Low/negative score
- ⚠️ Not accepted
- ⚠️ Low-rep answerer
- ⚠️ Old answer (>3 years)
- ⚠️ Comments saying it doesn't work

### Benchmarks

**Check:**
- Methodology transparency
- Hardware specs
- Software versions
- Reproducibility
- Funding/bias

**Trust if:**
- ✅ Detailed methodology (hardware, software, settings)
- ✅ Multiple runs, error bars
- ✅ Code/data available
- ✅ Independent (not vendor-funded)
- ✅ Reproduced by others

**Question if:**
- ⚠️ Vague methodology
- ⚠️ Single run, no error bars
- ⚠️ No code/data
- ⚠️ Vendor-funded (potential bias)
- ⚠️ Results not reproduced

---

## Handling Conflicts

### When Sources Disagree

**Step 1: Check dates**
- Newer info usually correct for fast-moving tech
- API may have changed between versions
- Best practices evolve

**Step 2: Check authority**
- Maintainer > expert > community > random blog
- Official docs > everything else (if current)

**Step 3: Check context**
- Different use cases?
- Different versions?
- Different environments?

**Step 4: Cross-reference**
- Find third source
- Check source code if possible
- Test yourself if feasible

**Step 5: Report conflict**
```markdown
⚠️ Conflicting information found:

**Source A** ([link], [date], [authority level]):
Claims X because Y.

**Source B** ([link], [date], [authority level]):
Claims Z because W.

**Analysis**:
[Why they differ, which is likely correct, or that both may be valid in different contexts]

**Recommendation**:
[Which to trust and why, or how to test yourself]
```

### Common Conflict Patterns

**Version Conflicts:**
- Source A describes v1.x behavior
- Source B describes v2.x behavior
- **Resolution**: Both correct for their versions. Note version in output.

**Context Conflicts:**
- Source A optimizes for speed
- Source B optimizes for memory
- **Resolution**: Both correct for their goals. Note tradeoff.

**Outdated vs Current:**
- Source A (old) describes deprecated approach
- Source B (new) describes current approach
- **Resolution**: Source B correct. Note that A is outdated.

**Theory vs Practice:**
- Source A (academic) describes ideal approach
- Source B (engineering) describes practical approach
- **Resolution**: Both valid. Note that B may sacrifice purity for practicality.

**Vendor Bias:**
- Source A (vendor) claims their product is best
- Source B (independent) shows mixed results
- **Resolution**: Trust independent source. Note vendor bias.

---

## Detecting Misinformation

### Common Misinformation Patterns

**Outdated Information Presented as Current:**
- Old blog post ranks high in search
- No date visible or buried
- Describes deprecated APIs as current
- **Detection**: Check dates, cross-reference with official docs

**Cargo Cult Programming:**
- "Always do X" without understanding why
- Copies patterns without context
- Superstitious practices
- **Detection**: Check if reasoning is provided, verify against authoritative sources

**Benchmark Manipulation:**
- Cherry-picked scenarios
- Unrealistic configurations
- Hidden vendor funding
- **Detection**: Check methodology, look for independent reproduction

**SEO Spam:**
- Keyword-stuffed content
- Auto-generated or plagiarized
- No real expertise
- **Detection**: Check author, look for original sources, verify claims

**Overgeneralization:**
- "X is always better than Y"
- Ignores tradeoffs and context
- One-size-fits-all advice
- **Detection**: Look for nuance, check if tradeoffs discussed

### Verification Strategies

**For Code Examples:**
1. Check if code is syntactically correct
2. Check if imports/dependencies are correct
3. Check if it matches current API (version check)
4. Look for comments confirming it works
5. Test yourself if critical

**For Performance Claims:**
1. Check methodology (hardware, software, settings)
2. Check if reproducible (code/data available)
3. Check if reproduced by others
4. Check for vendor bias
5. Look for independent benchmarks

**For Best Practices:**
1. Check if reasoning is provided
2. Check if official docs agree
3. Check if experts agree
4. Check if context-dependent
5. Look for counterexamples

**For Technical Explanations:**
1. Check if it matches official docs
2. Check if it matches source code
3. Check if experts agree
4. Check if it makes logical sense
5. Look for peer review or validation

---

## Source Quality Scoring

Use this rubric to score sources (0-10 scale):

### Authority (0-3 points)
- 3: Official docs, maintainer, original author
- 2: Known expert, reputable company blog
- 1: Community source with validation
- 0: Unknown author, no credentials

### Recency (0-2 points)
- 2: <1 year old (or timeless)
- 1: 1-3 years old
- 0: >3 years old

### Depth (0-2 points)
- 2: Detailed explanation with reasoning
- 1: Surface-level but accurate
- 0: Vague or incomplete

### Evidence (0-2 points)
- 2: Working code, data, reproducible
- 1: Some examples or evidence
- 0: Claims without evidence

### Validation (0-1 point)
- 1: Peer-reviewed, high engagement, reproduced
- 0: No validation

**Scoring:**
- 9-10: Excellent source, highly trustworthy
- 7-8: Good source, trustworthy with minor caveats
- 5-6: Decent source, verify key claims
- 3-4: Weak source, use with caution
- 0-2: Poor source, avoid or verify everything

---

## Special Cases

### Evaluating Chinese Sources

**Additional checks:**
- Platform reputation (Zhihu > CSDN > unknown blogs)
- Experiment detail (more detail = more trust)
- Reproducibility (code + settings provided?)
- Cross-reference with English sources

**Common strengths:**
- Detailed ablation studies
- Hardware-specific optimizations
- Cost analysis
- Production experience at scale

**Common weaknesses:**
- May not translate well to Western cloud providers
- May assume Chinese-specific context
- May use different terminology

**Trust if:**
- Detailed methodology
- Reproducible experiments
- Matches patterns in English sources
- Published on reputable platform

### Evaluating Cutting-Edge Sources

For very new topics (preprints, GitHub repos, tweets):

**Lower the bar for:**
- Recency (new = good)
- Validation (may not be reproduced yet)

**Raise the bar for:**
- Authority (who is claiming this?)
- Evidence (code, data, methodology)

**Always:**
- Note that it's cutting-edge
- Flag as "not yet validated"
- Check back later for reproduction

### Evaluating Niche Sources

For very niche topics (few sources available):

**Accept:**
- Lower engagement (small community)
- Less validation (fewer people to validate)

**Still require:**
- Clear reasoning
- Working examples
- Author expertise (even if not famous)

**Always:**
- Note that it's niche
- Verify key claims if possible
- Look for related topics to cross-reference

---

## Documentation in Output

When presenting sources, include credibility indicators:

```markdown
## Sources

### Official Documentation
- [PyTorch Documentation](link) — Official docs, updated [date]

### GitHub Repositories
- [example-repo](link) — 2.3k stars, active maintenance, comprehensive examples

### Expert Blogs
- [Blog Title](link) by [Author Name] (PyTorch core contributor) — Published [date], detailed ablation study with reproducible code

### Chinese Sources
- [Blog Title](link) — Zhihu, detailed v5e-8 TPU benchmarks with methodology, published [date]

### Community Discussions
- [Stack Overflow Answer](link) — 45 upvotes, accepted answer, confirmed working by multiple users

### Academic Papers
- [Paper Title](link) — NeurIPS 2024, 150 citations, code available, reproduced by [other paper]
```

**Include:**
- Source type
- Authority indicators (stars, upvotes, author credentials)
- Recency (date)
- Validation (reproduced, confirmed, etc.)

**Flag concerns:**
```markdown
⚠️ Note: [Source] is from 2020 and may be outdated. Cross-referenced with [newer source] to verify current best practices.
```

---

## Quality Assurance Checklist

Before delivering research with sources:

### Authority
- [ ] Each source's authority level identified
- [ ] Highest-authority sources prioritized
- [ ] Conflicts resolved using authority hierarchy

### Recency
- [ ] All sources dated
- [ ] Outdated sources flagged
- [ ] Recent developments noted

### Validation
- [ ] Key claims cross-referenced across sources
- [ ] Conflicts noted and explained
- [ ] Unverified claims flagged

### Diversity
- [ ] Multiple source types
- [ ] Multiple perspectives
- [ ] Not over-reliant on single source

### Transparency
- [ ] Source credibility indicators included
- [ ] Limitations noted
- [ ] Uncertainty acknowledged where appropriate
