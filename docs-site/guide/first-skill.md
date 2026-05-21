# Your First Skill

Walk through using your first skill — from install to invocation.

## Step 1: Install

```bash
npx skills-for-agents install --tool claude
```

## Step 2: Invoke a Skill

Open your AI coding agent and try:

```
/caveman full
```

Your agent will now respond in ultra-terse caveman mode — cutting token usage by 30-95% while keeping full technical accuracy.

## Step 3: Try Composition

Layer two skills together:

```
/blog technical + /caveman lite
```

This tells the agent to write a technical blog post (using the Blogger skill's voice) while applying caveman-lite compression to reduce verbosity.

## Step 4: Use Natural Language

You don't always need slash commands. Skills trigger on natural language too:

```
"Write a blog post about our deployment incident, make it terse"
```

The agent auto-detects: **Blogger** (voice + content) + **Caveman** (density).

## Understanding What Happened

When you invoke `/caveman full`:

1. The agent loads the Caveman skill's `SKILL.md` as a system prompt
2. The skill declares its domain: `density`
3. It applies compression rules to all output
4. Technical accuracy is preserved — only fluff is removed

When you compose skills:

1. Each skill handles its own domain
2. SIP (Skills Interoperability Protocol) resolves any conflicts
3. Domain ownership is respected — voice skills don't touch density, density skills don't touch voice

## Next Steps

- [Composition](/guide/composition) — Deep dive into how skills compose
- [Creating Skills](/guide/creating-skills) — Build your own skills
- [Skills Catalog](/skills/) — Explore all 15 skills
