---
description: Canonical spellings for client and team names. Apply across all workspaces, all content types, all files.
---

# Name Spelling Rule

## Scope
All workspaces. All content types. All files generated or edited by the agent. Includes auto-generated transcripts, AI-generated summaries, agent-written drafts, internal docs, and client-facing communications.

## Canonical Spellings

| Correct | Common Misspellings to Catch and Fix |
|:---|:---|
| **Susanne Goldstein** (client, EnergyOS / Human App Store) | Suzanne, Susan, Sue Anne |
| **ShaRhanda** (team, BCV/ReachCraft) | Sharonda, Sharanda, Shaorhanda, Sharhanda (lowercase r) |
| **Kelley** (team, Lisa Campion content loader) | Kelly (transcripts and auto-captions render this wrong; this is drift pattern DP-012) |
| **Lisa Campion** (client, healer / psychic / author) | Lisa Campian, Lisa Champion |

The capital "R" in **ShaRhanda** is intentional. It is part of how she spells her name. Preserve the capital "R" in all written references unless the user provides an explicit override.

## Capitalization Locks (Domain Terms)

Some non-person terms require consistent casing across all client workspaces because they are proper nouns, brand-program names, or both. Capitalize these in all agent-generated content, including session logs, governance files, internal notes, and audience-facing copy. Lowercase only inside verbatim third-party content.

| Term | Why | Examples |
|:---|:---|:---|
| **Reiki** | Proper noun (Japanese energy-healing tradition) and used inside multiple Lisa Campion branded program names (Psychic Reiki, Reiki Level I, Reiki master teacher). Lisa's own Kripalu bio uses "Reiki master teacher." | "Reiki Level I," "Psychic Reiki," "Frustrated Reiki Students" vertical. Never "reiki" in agent prose, even casual. |
| **Kajabi** | Brand / platform name. | "load to Kajabi," "Kajabi page." Never "kajabi." |
| **Skool** | Brand / platform name. | "Skool community," "The Psychic Society on Skool." Never "skool." |
| **Kripalu** | Proper noun (Kripalu Center for Yoga & Health). | "Kripalu workshop," "the Kripalu immersion." Never "kripalu." |

## Triggers

When generating any content that references these people, default to the canonical spelling. When editing existing files that contain misspellings, fix them. When ingesting auto-generated transcripts (Otter, Fathom, Zoom), run a name-correction pass before saving the transcript.

## Detection Pattern

Before saving any draft, run a check for the misspelling list above. If any misspelling appears in agent-generated content, replace it. If it appears inside a verbatim quote from a third party (e.g., a court document, an article, a screenshot of someone else's text), preserve the original spelling and add a `[sic]` annotation if clarity requires it.

## Exceptions

- Verbatim third-party content where the misspelling is part of the source record (rare, log in session log).
- File and folder names already created with the misspelling that have downstream dependencies (rename when safe; otherwise, leave and document).

## Enforcement

This rule is part of the Session Read Order in `/Antigravity Projects/CLAUDE.md`. Apply during:

- Content pack generation
- Slack, email, and text drafting
- Session log creation
- Transcript ingestion and processing
- Governance and rule file edits
- Any new file written into a client or team workspace

## Updating This List

If a new client or team member is added whose name is regularly misspelled, append them here with the same structure. Do not remove entries unless a person leaves the team and is unlikely to be referenced in future work.
