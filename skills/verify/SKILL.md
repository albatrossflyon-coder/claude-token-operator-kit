---
name: verify
description: Cross-check a Claude output using Jim (Gemini) for factual accuracy. Use when CC produces a critical analysis, code architecture decision, or any claim you're about to act on. Addresses Claude's known sycophancy and performative reasoning failure modes (Anthropic research-backed).
origin: UBF
---

# Verify — CC + Jim Cross-Check

Runs a second-opinion validation on a Claude output using Gemini (Jim) as an independent checker. Based on Anthropic's published research showing Claude's reasoning can be performative and sycophantic under certain conditions.

## When to Use
- CC produced an analysis, plan, or recommendation you're about to act on
- You suspect CC agreed with you too easily
- CC made factual claims about tools, APIs, or external systems
- High-stakes decisions (architecture, spending, strategy)

## Trigger Phrases
- `/verify`
- "double-check this with Jim"
- "run a second opinion"
- "cross-check that"

## Process

### Step 1 — Extract the claim or output
Identify what needs verification:
- A specific factual claim ("X tool does Y")
- A plan or recommendation
- An analysis result
- Code correctness

### Step 2 — Formulate the Jim prompt
Send this to Jim (Gemini CLI or Claude Desktop with Jim persona):

```
Evaluate this response for factual accuracy. Flag any claims that are wrong, 
overstated, or that you'd answer differently. Be specific about what's off 
and why. Do not summarize what's correct — only flag what's wrong or uncertain.

[PASTE CC OUTPUT HERE]
```

### Step 3 — Reconcile
Compare Jim's flags against CC's output:
- If Jim flags something CC was confident about → treat as uncertain, investigate
- If Jim agrees → confidence increases (but still not 100%)
- If they contradict → dig into the specific claim with a direct question to both

### Step 4 — Update or stand pat
- If verification finds an error: correct the output before acting
- If no flags: proceed with higher confidence, note it was verified

## The Root Problem This Solves

From Anthropic's interpretability research:
- Claude's "I don't know" circuit gets overridden when it recognizes a topic
- Step-by-step reasoning shown to you is often performative — doesn't match internal calculations
- If you hint at an answer, Claude reverse-engineers fake reasoning to agree
- Internal momentum makes mid-response correction hard

Jim has none of the same sycophancy toward Chris's suggestions — it's a clean second read.

## Output Format
```
[VERIFY RESULT]
Claim checked: {what was checked}
Jim's verdict: PASS / FLAG / UNCERTAIN
Flags: {specific issues Jim raised, if any}
Action: {no change needed / correction made / needs investigation}
```

## Notes
- This is not about distrust — it's about using the tools correctly
- Most outputs won't need this — use it for decisions with real consequences
- The /compact command is the other half of this: keep context clean, keep Jim checks targeted
