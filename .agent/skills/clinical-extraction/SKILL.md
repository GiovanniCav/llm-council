---
name: clinical-extraction
description: Transform raw transcripts into "Clinical Authority" content packs (Segmenters, Advertorials, 5130 Offers) based on the Doug Noll model.
---

# Clinical Extraction Skill

## When to Use
- When a new transcript is added to a workspace (e.g., MacWhisper output).
- When asked to "Generate a content pack" or "Doug Noll-ify this transcript."
- User mentions "narrative arc," "segmenters," or "5130 harvest."

## The Protocol

### 1. Identify the Vertical
Analyze the transcript for the highest-leverage niche mentioned.
- **Goal**: Find the "One Thing" they need most right now.
- **Framework**: Use the "Diagnostic Triage" model to identify the specific friction point.

### 2. Map the 5-Day Arc
Create a Narrative Arc following this structure:
- **Day 1 (The Segmenter)**: Soft handraiser question for the specific niche.
- **Day 2 (The Advertorial)**: Case study/War story highlighting the niche problem.
- **Day 3 (Mechanism)**: High-status explanation of *why* the product/service solves it (Affect Labeling, 98-2 logic).
- **Day 4 (Micromagnet)**: Offer a specific resource (PDF/Checklist) to identify demand.
- **Day 5 (The 5130 Offer)**: Direct, low-fluff sorting post for the "5 who want it in 30 days."

### 3. Apply Clinical Tone
Ensure all copy avoids GPT-isms and uses "Clinical Density."
- **Bad**: "I'm so excited to help you de-escalate!"
- **Clinical**: "We are stabilizing the diagnostic path for founders facing structural friction in high-conflict boardrooms."

## Tooling
- **Engine**: `$ANTIGRAVITY_ROOT/Project Factory/scripts/clinical-extraction.py`
- **Doctrine**: `$ANTIGRAVITY_ROOT/Project Factory/GLOBAL_DOCTRINE.md`
- **Reference**: `$ANTIGRAVITY_ROOT/Project Factory/SOW_TACTICS_SUMMARY.md`
