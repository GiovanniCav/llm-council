# Second-Brain Architecture for BCV Workspaces

> **Purpose:** Pattern for how to organize a workspace so the agent can retrieve high-value context quickly. Adapted from Andrej Karpathy's LLM-Wiki gist (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and Matt Wolfe's video walkthrough (https://www.youtube.com/watch/yke4fLQUsh4), reframed for client-engagement workflows rather than personal knowledge management.
> **Scope:** Workspace-level pattern. Applies after a workspace reaches Stage 1 maturity (has `.agent/`) and is on a path to Stage 2+. Not required at Stage 0.
> **Status:** Initial documentation, 2026-05-07. Refine as patterns settle.

---

## What Karpathy and Matt got right

Their structure is a flat directory tree:

- `raw/` — immutable source material the agent reads but doesn't edit
- `wiki/` — synthesized concept pages the agent generates from `raw/` and updates over time
- `agents.md` — the operational rulebook for what the agent does on each request
- `index.md` — catalog of what's in the wiki
- `log.md` — append-only event log
- Optional `journal/` and `CRM/` folders for personal use cases

What's good about it: the agent has explicit places to put new context (raw vs synthesized), explicit cross-linking between source material and the synthesis, and an event log so the agent can see what it has done before. The `agents.md` operational rulebook is closer to a runtime spec than a settings file.

What doesn't translate to BCV's client work: the personal-knowledge-management framing (web clipper, journal-grounded chat, scheduled cron). Client engagements have different success criteria: commitments tracked, decisions defensible, deliverables shipped. Single-user vs multi-author also matters — BCV workspaces are written by Giovanni, Mindy, Morgan, and the agent, so write conventions matter more than they do for a personal vault.

## How BCV's existing PARA + governance already covers most of it

BCV workspaces use PARA (Projects/Areas/Resources/Archive) plus a `.agent/` governance layer plus `session_logs/` plus a `MANIFEST.jsonl`. Mapped to Karpathy's vocabulary:

| Karpathy term | BCV equivalent |
|---|---|
| `raw/` | `02_Areas/Transcripts/` plus `00_INBOX/` |
| `wiki/` | `brain/` plus `01_Projects/` synthesis docs |
| `agents.md` | `IDENTITY.md` plus `.agent/` plus root `CLAUDE.md` |
| `index.md` | `MANIFEST.jsonl` plus `README.md` |
| `log.md` | `logs/decisions.jsonl` |
| `journal/` | `session_logs/` |
| `CRM/` | (gap; this pattern fills it) |

The PARA structure handles client work better than a flat wiki because client engagements have project lifecycle (active vs archived), area lifecycle (ongoing concerns like Brand or Compliance), and resource lifecycle (reference material). PARA encodes that lifecycle. Karpathy's wiki doesn't.

## What this pattern adds

Two things that PARA + `.agent/` don't already do:

### 1. `02_Areas/People/` — stakeholder context cards

One markdown file per active human in the engagement. The card answers "what do we know about this person" in one place instead of forcing the agent to scan transcripts, decisions, and session logs to assemble a profile each time.

Card structure (template at `.agent/templates/people_card.md`):
- Name (header) and role
- Working relationship to BCV (how we engage with them, what they own)
- Authority and decision rights (what they can sign off, what needs Ben/client lead)
- Key context (industry, geography, family, things relevant to the engagement, no personal/medical/financial detail)
- Recent updates (last interaction, current asks, next step)
- Source provenance (link to transcripts and decisions where this person was discussed)

Scope rules:
- Only people active in the engagement. Not every name mentioned in passing.
- No personal or sensitive information that wouldn't be in a LinkedIn-style profile. Even if a transcript captures something private, it doesn't belong in a shared card.
- Update on significant interaction, not on every mention.

### 2. `02_Areas/Concepts/` — cross-cutting concept pages

One markdown file per concept that gets referenced across three or more documents. Each page summarizes the concept and links to canonical sources rather than restating them.

Page structure (template at `.agent/templates/concept_page.md`):
- Concept name (header) and one-line definition
- Origin (where the concept came from in this engagement)
- Description (what it actually is, in plain language)
- How it applies in this workspace (the engagement-specific implementation)
- Status (active, parked, retired)
- Canonical source link (the doc that owns the truth)
- Cross-references (other concept pages, transcripts, decisions)

Scope rules:
- Only concepts referenced in three or more documents. One-off ideas live where they were introduced.
- Concept pages summarize, they don't duplicate. The canonical-source link points to the doc that owns the truth.
- Retire when no longer referenced. Don't accumulate dead concepts.

## What this pattern does NOT add

These pieces from the Karpathy/Matt setup don't apply and shouldn't be implemented:

- Scheduled automation (Codeex cron, GitHub auto-commit). Workspace updates are on-demand, not autonomous. The nightly governance audit handles the scheduled-pass need.
- Web clipper ingestion. Workspaces don't ingest random web content; sources are structured (calls, NotebookLM, attorney docs).
- Journal-grounded chat. The `session_logs/` folder serves the journal role and the agent reads it on session start; no separate chat layer needed.
- Single `agents.md` rulebook. The existing `.agent/` directory is more sophisticated (universal guardrails, drift patterns, precedence rules, three-tier audit architecture). Don't collapse that into a single file.
- Auto-generated graph view. The workspace is already an Obsidian Vault per CLAUDE.md, so the graph view is available without adding anything.

## When to apply this pattern

For a workspace currently at Stage 1 (has `.agent/`, no full CLAUDE.md with read order), apply the pattern when at least one of the following is true:

- Three or more active stakeholders need context that's currently scattered across transcripts and decisions.
- Three or more recurring concepts are referenced in three or more documents each (Mythos Method, IWT eligibility, etc.).
- The agent has lost context across sessions on the same questions twice (e.g., "remind me what Lillie's role is").

If none are true, the workspace doesn't need it yet. Karpathy's pattern earns its keep when retrieval cost gets high enough; before that, PARA alone is fine.

## Implementation steps

1. Run pre-fix Decision Quality Protocol analysis (premortem, red-team, de-risking) before adding directories.
2. Create `02_Areas/People/INDEX.md` plus one card per active stakeholder, sourced strictly from documented conversations and decisions.
3. Create `02_Areas/Concepts/INDEX.md` plus one page per cross-cutting concept, with canonical source links.
4. Update `MANIFEST.jsonl` with entries for each new file.
5. Append decision entries to `logs/decisions.jsonl` capturing the architecture decision.
6. Write a session log including post-fix postmortem and red-team.
7. Surface any spelling, governance, or stale-content issues observed during implementation as separate follow-up tasks.

## Tradeoffs and watch-outs

- **Folder proliferation.** Two new directories, multiple files. Watch for the temptation to keep adding (Companies/, Tools/, Frameworks/) without proven retrieval need. Add only when the three-place-reference threshold is met.
- **Drift between cards/pages and canonical sources.** The cards summarize the source of truth; they're not the source. If a fact changes (someone's role shifts, a decision is reversed), the agent must update the canonical source first and the card second.
- **Sensitive info leakage.** Cards live in a multi-author workspace. Nothing goes in a card that wouldn't be appropriate to share with the team. Strict rule.
- **Maintenance burden.** Each card and page needs review when the underlying engagement state changes. The nightly governance audit can scan for staleness; if a card hasn't been updated in 30+ days while the underlying transcripts have, surface it.

---

## Version History

| Date | Update |
|------|--------|
| 2026-05-07 | Initial documentation. Adapted from Karpathy LLM-Wiki gist and Matt Wolfe walkthrough. First applied to Ben Hein workspace. |
