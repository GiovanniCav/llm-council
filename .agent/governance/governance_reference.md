# Governance Reference — LLM Council

> **Type:** Workspace. Inherits root-level governance; local rules add constraints without weakening universal rules.

---

## Inherited Governance

This workspace inherits all governance from the root Antigravity Projects layer:

- **Universal Guardrails:** `/Antigravity Projects/.agent/governance/universal_guardrails.md`
  - 26 active guardrails (UG-001 through UG-026)
  - Applies to all content, all workspaces, all channels

- **Known Drift Patterns:** `/Antigravity Projects/.agent/governance/known_drift_patterns.md`
  - Running log of failures observed with grep patterns to catch each

- **Precedence:** `/Antigravity Projects/.agent/governance/precedence.md`
  - Conflict resolution: LOCAL adds, never weakens UNIVERSAL
  - Rule hierarchy and file override order

- **Maturity Ladder:** `/Antigravity Projects/.agent/governance/maturity_ladder.md`
  - Stage rubric for workspace progression

## Audit Coverage

LLM Council is in scope for:
- **Weekly cross-workspace sweep** (Sundays 8 AM Pacific): covered under the "all in-scope workspaces" clause
- **Monthly retrospective** (first of month): read-only session-log scan

Conditional coverage:
- **Nightly governance audit**: follows the root nightly-audit scope. If this workspace is named there, that procedure wins.

## Local Rules

Local atomic rules in `.agent/rules/` add workspace constraints but do not weaken the universal layer. See the `CLAUDE.md` read order for precedence.
