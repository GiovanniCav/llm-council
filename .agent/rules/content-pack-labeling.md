# Rule: Content Pack Labeling in Communication

**Status:** Active. Workspace-wide. Applies to all clients (Doug, Lisa, TGBW, future).
**First codified:** 2026-05-05
**Source:** Giovanni directive 2026-05-05.
**Universal guardrail:** UG-021.

---

## The rule

When referring to a content pack in any communication with Giovanni (chat replies, Slack drafts, status updates, email drafts, summaries, refinement prompts addressed to him), lead with the human-readable date format. The internal cycle code can follow in parentheses if disambiguation is useful, but it is never the primary label.

## Approved formats

In order of preference:

1. **"w/o [date] content pack"** — preferred. Example: "w/o 5/11 content pack."
2. **"[date] content pack"** — also fine. Example: "5/11 content pack."
3. **"week of [date]"** — fine in body prose. Example: "the week of 5/11."
4. **"[date] pack (C1BxWy)"** — only when disambiguation is genuinely needed (e.g., comparing two future weeks). Example: "5/11 pack (C1B2W2)."

## What NOT to do

- Do not lead with "C1B2W2" in any reply, summary, or message addressed to Giovanni.
- Do not say "the C1B2W2 content pack" without a leading date label.
- Do not mix the formats inconsistently within a single message. Pick one and stick with it.

## Scope

**Applies to:**
- Chat replies in Cowork.
- Slack drafts addressed to Giovanni or the team.
- Email drafts addressed to Giovanni.
- Status updates, summaries, handoff messages, refinement prompts directed at Giovanni.
- Session log prose addressed to a human reader (not the metadata blocks).

**Does NOT apply to:**
- File names (e.g., `C1B2W2_Content_Pack.md`, `C1B2W2_Artifacts/`). File names keep the cycle code for sortability and folder consistency with the existing artifact convention.
- Governance file change-log entries (e.g., `OPERATIONAL_STATE.md` change log, `universal_guardrails.md` change log). These are technical audit trails and use the cycle code for precision.
- Internal CB Instruction Set technical headers (e.g., the CB brief header `# C1B2W2 Copy Bot Instruction Set`). The CB consumes the technical label; the user does not.
- The Google Sheet (`Doug Noll - Content Pillars - 2026.04.13`) row labels. The sheet uses the cycle code as the primary key.

## Rationale

The cycle code (C1B2W2) is internally precise and useful for governance, tracking, and folder structure. It is also opaque to a human reader: Giovanni cannot tell from the code alone which week of the calendar a pack ships in, which forces a sheet lookup. Date-led labels eliminate the lookup tax in routine communication while preserving the cycle code where machine-precision matters.

## Date conventions

- Use the Monday of the ship week as the date. Example: a pack that ships May 11-15 is "w/o 5/11."
- US date format (M/D), not ISO. Match Giovanni's natural usage.
- No year unless the year is ambiguous in context (e.g., year-end transitions, multi-year retrospectives).

## Examples

**Good:**
- "The w/o 5/11 content pack is built and QC'd."
- "I QC'd the 5/11 pack. Two mechanical fixes applied."
- "Refinement prompt for the 5/11 LinkedIn openers is ready."
- "Carousel image prompts for the w/o 5/11 pack still owed."

**Bad:**
- "C1B2W2 is built and QC'd." → Confusing without sheet lookup.
- "I QC'd the C1B2W2 pack. Two mechanical fixes applied." → Same problem.
- "The next pack (C1B2W3) needs survey input." → Should be "the w/o 5/18 pack (C1B2W3)" or just "the w/o 5/18 pack."

## Cross-client mapping

The same rule applies to Lisa and TGBW. Their cycle codes (Lisa C1W06, TGBW Week_09, etc.) follow the same treatment: lead with "w/o [date]" in communication, keep the technical code in file names and governance.
