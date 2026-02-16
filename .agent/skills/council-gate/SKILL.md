---
name: council-gate
description: Run blind peer reviews on AI outputs using the Council architecture. Use to verify high-stakes content or code.
---

# Council Gate Skill

## The Process
1. **Submission**: Content is submitted to the Council API (Port 8010).
2. **Review**: 3 distinct Personas (Skeptic, Optimist, Realist) critique it.
3. **Synthesis**: The "Chairman" aggregates scores.

## Usage
- **Draft Review**: "Run this email through the Council."
- **Code Audit**: "Ask the Council if this architecture is sound."

## Output
Returns a **Council Report** with:
- Score (0-100)
- Key Risks
- Improvement Suggestions
