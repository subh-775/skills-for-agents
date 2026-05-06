# Instruction Science — Research Backing for the 12 Rules

> Deep-dive reference for the instruction psychology rules in SKILL.md. Read when you need research details, edge case guidance, or to explain the science to a user.

---

## Research Landscape

Five research streams converge on how LLMs process instructions:

1. **Position Bias** — "Lost in the Middle" (NeurIPS 2023), HIPO (arXiv:2603.16152)
2. **Structured Prompting** — LangGPT (arXiv:2402.16929), Chinese tech community (知乎/CSDN/掘金)
3. **Cognitive Load Theory** — Applied to LLM attention budgets
4. **Instruction Hierarchy** — OpenAI (arXiv:2404.13208), IH-Challenge (arXiv:2603.10521)
5. **Multi-Constraint Following** — AgentIF (arXiv:2505.16944), AdvancedIF (arXiv:2511.10507)

---

## Rules 1-8: Original Science (Summary)

### Rule 1: Position — The U-Shaped Curve
- Beginning: ~95% retrieval accuracy | Middle: ~50-70% | End: ~85-90%
- Caused by positional encodings, causal attention masks, training distribution
- HIPO research confirms: constrained RL drives models to shift attention toward long-range system tokens

### Rule 2: Examples — Pattern Matching vs Instruction Parsing
- Examples activate pattern completion circuitry (direct input→output mapping)
- Prose instructions require interpretation (introduces ambiguity)
- 2 high-quality examples ≈ 500 words of verbal instruction
- 3 edge-case examples > 10 easy-case examples
- Examples showing reasoning process > examples showing output only

### Rule 3: Positive Framing — The Pink Elephant Problem
- "Don't think of X" activates X in attention → suppression is unreliable
- OpenAI guide: "State what to do rather than what to avoid"
- Anthropic docs: "Focus on what Claude *should* do rather than what it *should not*"

### Rule 4: Reasoning — Constitutional AI Connection
- Rule without reasoning: ~70% adherence in matching scenarios
- Rule with reasoning: ~85% adherence + correctly broken ~60% of the time when reasoning doesn't apply
- Three-part structure: [What to do] because [why] unless [exception]

### Rule 5: Structure — Delimiter Science
- LangGPT: Structured prompts outperform unstructured by 15-30% on task accuracy
- Delimiter research: 16-24% instruction-following improvement with clear section boundaries
- Code blocks for format specs: near-100% compliance vs ~70% for prose descriptions
- Tables for decision logic: ~35% more reliable than prose conditionals
- XML tags considered most robust for complex prompts (Anthropic fine-tunes for them)

### Rule 6: Grouping — Attention Clustering
- Scattered rules lose to grouped rules consistently
- Chinese community ablation: Markdown headers improve section-specific adherence by ~20%

### Rule 7: Token Economy — Cognitive Load Theory
- Intrinsic load (task complexity): manage by decomposition
- Extraneous load (filler, redundancy): eliminate ruthlessly
- Germane load (actual instruction processing): maximize by clearing extraneous

### Rule 8: Imperative Voice
- "Check X" = unambiguous instruction
- "X should be checked" = ambiguous (requirement? suggestion? background fact?)

---

## Rules 9-12: New Research (Detailed)

### Rule 9: Constraint Anchoring — AgentIF Evidence

The AgentIF benchmark (arXiv:2505.16944, May 2025) evaluates LLM instruction following in real agentic scenarios:
- 707 human-annotated instructions across 50 agentic tasks
- Average instruction: 1,723 words, 11.9 constraints per instruction
- Maximum: 15,630 words per instruction

**Key finding**: Models fail most on abstract constraints and complex constraint structures. Concrete, anchored constraints with micro-examples achieve dramatically higher adherence than abstract statements.

**Failure modes by constraint type** (from AgentIF analysis):
| Constraint Type | Failure Rate | Mitigation |
|----------------|-------------|------------|
| Tool specifications (parameter types, required fields) | Highest | Provide exact schema with example values |
| Conditional constraints ("if X then Y") | High | Use table format instead of prose conditionals |
| Format constraints (JSON, specific structure) | Medium | Show exact output example, use code blocks |
| Content constraints (include/exclude topics) | Lower | List explicitly with examples |

**AdvancedIF** (arXiv:2511.10507) further validates: rubric-based instruction following with explicit criteria produces 6.7% absolute gains over unstructured instruction.

### Rule 10: Training Data Quality Signal

**Origin**: Chinese prompt engineering community — the "小红帽原则" (Red Riding Hood Principle), widely discussed on 知乎 and CSDN.

**The mechanism**: LLMs are trained on internet text. They learn to associate formatting patterns with content quality:
- Well-structured markdown with consistent formatting → technical documentation, quality content
- Messy, inconsistent formatting → forum posts, casual text, lower quality

When your skill uses clean, consistent formatting, the model's attention patterns align with "high-quality technical document" mode. When the skill is messy, the model defaults to "casual response" mode.

**Validation**: Structured prompts (LangGPT framework) consistently outperform unstructured ones across all tested models, even when the semantic content is identical.

### Rule 11: Outcome-First Prompting

**Origin**: OpenAI's GPT-4.1 prompt engineering guidelines (2025).

**The shift**: Newer models (GPT-4.1, Claude 3.7+, Gemini 2.5) are significantly better at determining optimal paths to solutions. Over-specifying process steps:
- Constrains the model's reasoning space
- Can introduce noise and contradictions
- Leads to overly mechanical outputs

**When outcome-first works**: Most tasks where the model has strong baseline competence.

**When process-heavy is still needed**:
- Multi-step workflows where step order is critical
- Domains where the model consistently takes wrong paths
- Tasks involving tool use sequences
- Novel domains outside the model's training distribution

**Practical implication for skills**: Define what "success" looks like (criteria, constraints, quality bar) rather than scripting every decision. Add process guidance only where the model reliably fails without it.

### Rule 12: Self-Verification Loops

**Origins**: 
- Anthropic's recursive self-improvement research
- Chinese dev community: "验证与循环" (verification and loop) pattern, documented on CSDN and 知乎
- OpenAI's "Chain of Verification" (CoVe) technique

**The pattern**: Generate → Verify → Fix

When used in skills:
```markdown
After generating [output type], verify:
- [ ] [Constraint 1]
- [ ] [Constraint 2]
If any check fails, fix before presenting to user.
```

**When to use**: Only for constraints where:
1. Violations are costly (wrong format breaks downstream systems)
2. The model commonly fails without verification (empirically observed)
3. The constraint is objectively checkable (not subjective quality)

**When NOT to use**: Subjective quality judgments, constraints the model already follows reliably, or when verification would double the output length for marginal benefit.

---

## Chinese Prompt Frameworks Comparison

The Chinese community has developed three major structured prompting frameworks, each with different strengths:

| Framework | Core Elements | Best For |
|-----------|--------------|----------|
| **LangGPT** | Modular templates, variables, Markdown-as-code | Agent system prompts, complex workflows |
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | Content creation, brand voice, marketing |
| **CRISPE** | Capacity/Role, Insight, Statement, Personality, Experiment | Strategic analysis, multi-perspective evaluation |

**Key insight from framework comparison**: Task complexity should be proportional to framework complexity. Simple tasks suffer from over-engineering; complex tasks benefit from structured scaffolding.

---

## Key Papers Reference

| Paper | Year | Key Finding |
|-------|------|-------------|
| Lost in the Middle (NeurIPS) | 2023 | U-shaped attention curve in long contexts |
| LangGPT (arXiv:2402.16929) | 2024 | Structured prompts outperform unstructured by 15-30% |
| Instruction Hierarchy (arXiv:2404.13208) | 2024 | System > Developer > User > Tool priority |
| AgentIF (arXiv:2505.16944) | 2025 | Models fail on complex constraint structures |
| AdvancedIF (arXiv:2511.10507) | 2025 | Rubric-based IF training yields 6.7% gains |
| HIPO (arXiv:2603.16152) | 2026 | Constrained RL shifts attention to system tokens |
| IH-Challenge (arXiv:2603.10521) | 2026 | +10% IH robustness with adversarial training |
