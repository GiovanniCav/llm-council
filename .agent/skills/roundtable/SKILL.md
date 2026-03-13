---
name: roundtable
description: Multi-expert deliberation engine. Auto-selects domain experts, runs structured debate rounds (the gauntlet), and delivers actionable synthesis in Why/What/How/Now format with linked Minto Pyramid.
---

> [!WARNING]
> **AUTO-SYNCED FILE - DO NOT EDIT LOCALLY**
> This file is distributed via `infrastructure_sync.py` from the `Project Factory` workspace. Any local changes made here will be overwritten during the next global sync. Ensure all edits are made in the Project Factory source repository.

# The Roundtable — Multi-Expert Deliberation Engine

## When to Use

Invoke the Roundtable when facing:
- **Strategic decisions** with multiple valid approaches and non-obvious tradeoffs
- **Complex problems** spanning multiple domains (business + psychology + marketing, etc.)
- **High-stakes choices** where a premortem would add value
- **Creative challenges** that benefit from diverse expert lenses

Not for: simple factual lookups, routine tasks, or questions with obvious single answers.

## How to Invoke

### Via Command
```
/roundtable [your question or challenge]
```

### Via Natural Language
The agent will recognize roundtable-appropriate queries and offer to convene a panel. Examples:
- "Should I raise my consulting prices by 30%?"
- "How should I position my new SaaS product against established competitors?"
- "My client's funnel is converting at 2%. What's wrong and what do I do?"

## What Happens

### Phase 1: Panel Assembly
The engine analyzes your query, classifies its Cynefin domain (Simple/Complicated/Complex/Chaotic), and auto-selects 3-7 domain experts. You'll see a panel preview with rationale before the debate begins.

**Permanent Seats** (always present):
- **The Contrarian** (Charlie Munger) — Inversion, second-order effects, frame challenges
- **The Synthesizer** (Moderator) — Manages flow, produces final synthesis

**Conditional Seat** (strategic/high-stakes queries only):
- **The Risk Assessor** (Premortem Protocol) — "Imagine this failed. Why?"

**Domain Experts** — Auto-selected from the expert roster based on query domain. Sources include business strategy, negotiation, psychology, direct response, positioning, product design, coaching, investment, and 166 copywriting voices.

### Phase 2: Opening Positions
Each expert delivers their initial take in character through their signature lens.

### Phase 3: The Gauntlet (2-3 rounds)
- **Round 1**: Challenge/Build — experts directly respond to each other's specific points
- **Round 2**: Convergence + Premortem — where do we agree? What could go catastrophically wrong?
- **Round 3** (complex queries only): Epiphany crystallization

### Phase 4: Structured Output

**Compact output** (delivered to chat):
```
🎯 EPIPHANY
[One-sentence breakthrough]

📍 CYNEFIN DOMAIN
[Simple / Complicated / Complex / Chaotic]

🔑 WHY THIS MATTERS
[2-3 sentences]

📋 WHAT TO DO
[Numbered action steps]

🔧 HOW TO EXECUTE
[Key implementation detail per step]

⏰ NOW (First 24 Hours)
[Single most important next action]
```

**Full synthesis** (saved to `brain/`): Minto Pyramid, workshop transcript with expert attributions, mental models applied, risk assessment, dissenting views.

## Expert Panel Customization

After seeing the panel preview, you can:
- **Swap experts**: "Replace Hormozi with Dan Kennedy"
- **Add experts**: "Also bring in Robert Cialdini"
- **Adjust count**: "Use only 3 experts for this one"
- **Approve**: "Looks good, run it"

## Model Configuration

Each phase can use a different LLM model. Default is Gemini 3 Flash Preview (free input). Use `compare: true` to A/B test the same query across two model configs.

## Resources

- `resources/expert_roster.md` — Master expert archetypes with LLM prompt fragments
- `resources/workshop_protocol.md` — Full deliberation protocol and output templates
- `resources/mental_models.csv` — 375-entry seed catalog of mental models
