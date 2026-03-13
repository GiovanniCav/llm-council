---
description: Launch a multi-expert Roundtable deliberation session on any strategic question
---

# Roundtable Deliberation

## 1. Read the Skill
Read `.agent/skills/roundtable/SKILL.md` and all resources in `.agent/skills/roundtable/resources/`.

## 2. Confirm the Query
If the user provided a query after `/roundtable`, use it. Otherwise, ask: "What question or challenge should the panel deliberate on?"

## 3. Run the Full Protocol
Follow the skill instructions exactly:
1. **Panel Assembly** — Classify Cynefin domain, assess stakes, auto-select 3-7 experts
2. **Show the panel** to the user and ask for approval or swaps before proceeding
3. **Opening Positions** — Each expert delivers their independent take
4. **Adversarial Sieve** — Each expert identifies fatal flaws in others' arguments
5. **Gauntlet Rounds** — Challenge/Build → Convergence/Premortem → Epiphany Crystallization
6. **Synthesis** — Produce the structured Why/What/How/Now output with elimination rules

## 4. Save the Session
Save the full session transcript to `brain/roundtable-[slug]-[timestamp].md` using the Minto Pyramid format documented in the skill.

## 5. Deliver the Compact Output
Present the structured output (Epiphany → Cynefin → Why → What → How → Now) to the user.
