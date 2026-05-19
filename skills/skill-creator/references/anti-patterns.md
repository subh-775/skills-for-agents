# Skill Anti-Patterns

This catalog identifies common pitfalls in skill design and provides concrete fixes to ensure your skills are effective and SIP-compliant.

| Anti-Pattern | Symptom | Fix |
|-------------|---------|-----|
| **The Vague Skill** | "Make the code better." | Be specific. What does "better" mean? Pick one dimension (readability, performance, security) and give concrete steps with examples. |
| **The Dictator** | "ALWAYS do X. NEVER do Y. MUST follow Z." | Include reasoning. `Use X because Y` is followed more reliably than `ALWAYS use X`. |
| **Negative Nancy** | "Don't use var. Don't write long functions." | Reframe positively: "Use `const` by default because immutable bindings prevent accidental mutation." |
| **The Middle Child** | Critical rule buried on line 250. | Front-load critical rules. The first 30 lines are prime real estate. |
| **The Novel** | 2000-line SKILL.md. | Extract deep-dive content to `references/`. SKILL.md is the router, not the encyclopedia. |
| **Tell-Don't-Show** | 500 lines of prose, zero examples. | Lead with examples. Model pattern-matches on examples more reliably than it parses prose. |
| **The Island** | No composability section. | Every skill composes. Even standalone skills need to know how to behave when density or voice skills are active. |
| **The Scatter-Brain** | Related rules scattered across 10 sections. | Group related constraints together in a single block for better attention anchoring. |
| **The Overfit** | Works for 3 test cases, breaks on everything else. | Generalize from examples. Explain the principle, not just the pattern. |
| **The Abstract** | "Ensure quality output" with no anchor. | Add concrete micro-examples for every constraint (Rule 9). |
| **The Shadow** | Domain overlap with existing skills. | Differentiate scope or make one yield to the other. |
| **The Echo** | Redundant instructions the AI follows by default. | Earn every token. If removing it doesn't change output, delete it. |
