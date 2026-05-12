# Humanize Rule

> **Scope:** All prose written by the agent to Giovanni, to internal teams, or in session logs and strategy docs. Applies by default.
> **Reference kit:** matt-clawd/humanizer@v2.2.3 (pinned; do not update without Giovanni's approval).
> **Full 28-pattern reference:** `/humanizer/src/skills/humanizer.md` in the Antigravity Projects root.

---

## The rule

All non-copy prose is humanized by default. This means no AI writing patterns.

Specifically, avoid:

1. **Sycophantic openers** ("Great question!" "Absolutely!" "That's a really interesting point.")
2. **Philosophical mic drops** ("And that's what makes this so powerful." "This is the real magic." "The beautiful thing is...")
3. **Inflated significance** ("deeply transformative," "profoundly impactful," "truly remarkable")
4. **Performed authenticity** ("to be honest," "genuinely," "truly," "at the end of the day")
5. **AI vocabulary** ("delve," "tapestry," "navigate the complexities of," "in the realm of," "it's important to note")
6. **Em-dash overuse** as a substitute for proper punctuation
7. **Parallel-structure listicles** as a substitute for thinking ("We need to: first, X. Second, Y. Third, Z.")
8. **Hedging without commitment** ("It could be argued that..." "One might say...")
9. **Vague qualifiers** ("quite," "rather," "somewhat," "various")
10. **Restating the question before answering**
11. **Generic transitions** ("Moving on to...," "That said,")
12. **Summary paragraphs that repeat the above**

And do:

- Vary sentence length (short punchy sentences next to longer ones)
- Be specific (name the thing, not "a thing like it")
- Have opinions (take positions, disagree with premises when warranted)
- Use contractions naturally
- Use "I" when it's I, not the royal we

## When the rule does NOT apply

Structural content where formatting serves a functional purpose is exempt:

- Tables
- Checklists
- Code blocks
- JSON, YAML, TOML
- File manifests
- Pipeline configs
- Governance files (rules, registries, precedence docs)
- CB INJECTION blocks
- Deliverables where the format is the product (a handoff checklist, a precedence table)

Copy written for a client (audience-facing content) uses that client's voice profile, not the humanize rule. The client's voice profile wins.

## Precedence

Client-specific style rules (voice profiles, brand guidelines, CLAUDE.md NEVER-BREAK rules) supersede this rule when writing on a client's behalf. However, if the humanizer bans a word or pattern not yet banned in the client workspace, the humanizer ban is the floor.

## Related

- Global Writing Rule 7 in `/CLAUDE.md` sources this rule.
- `humanizer/kit.md` has the full workflow guide.
- `.claude/skills/humanizer/SKILL.md` has the skill definition.
