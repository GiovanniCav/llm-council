---
name: copywriting-styles
description: Consult the Copywriting Styles Ultimate reference early in any copy project. Use this to select which copywriters' voices and techniques are best for the given deliverable, then apply their writing styles via LLM prompt fragments.
---

# Copywriting Styles Skill

## When to Use

Consult this skill **at the start of any copy project** — before drafting headlines, emails, landing pages, sales pages, content packs, or website copy. The goal is to deliberately select the right copywriter voices for the job rather than defaulting to generic output.

## Reference File

The master reference lives inside this skill directory:

```
.agent/skills/copywriting-styles/resources/Copywriting_Styles_Ultimate.md
```

This file contains **166 copywriter profiles** with:
- Voice & style descriptions
- LLM prompt fragments (ready to paste)
- Key techniques / signature moves
- Best use cases
- A use-case → top voices matrix
- Blending instructions (combine 2–3 max)
- Funnel-stage matching guide

## Workflow

### Step 1: Identify the Deliverable Type

What are you writing? Match to one of these categories from the use-case matrix:

| Deliverable | Top Voices |
|---|---|
| Email sequences / nurture | Andre Chaperon, Ben Settle, Ian Stanley, Daniel Throssell, Troy Ericson, Robert Collier, Dean Jackson |
| Sales pages / long-form DR | Gary Halbert, Eugene Schwartz, John Carlton, Clayton Makepeace, Stefan Georgi, Dan Kennedy |
| Video sales letters (VSLs) | Jon Benson, Craig Clemens, Stefan Georgi, Chris Haddad, Frank Kern |
| Social media / short-form | Alex Hormozi, Harry Dry, Seth Godin, Eddie Shleyner, Neville Medhora, Laura Belgray |
| Authority / thought leadership | Seth Godin, Ann Handley, David Ogilvy, Brian Clark, Joe Pulizzi, Demian Farnworth, Jay Abraham |
| Landing pages / conversion | Joanna Wiebe, Michel Fortin, Jen Havice, Amy Harrison, Sabri Suby |
| High-ticket / consulting | Jay Abraham, Taki Moore, Dan Kennedy, Dan Lok, Alex Hormozi, Russell Brunson |
| Brand voice / positioning | Donald Miller, Bill Bernbach, Ash Ambirge, Hillary Weiss, Laura Belgray, Shirley Polykoff |
| B2B / technical | Bob Bly, Perry Marshall, Aaron Orendorff, Henneke Duistermaat, Eddie Shleyner |
| Coaching / course marketing | Taki Moore, Ray Edwards, Russell Brunson, Eben Pagan, Marie Forleo, Ramit Sethi |
| Website / UX copy | Joanna Wiebe, Jen Havice, Donald Miller, Dean Jackson, Henneke Duistermaat |

### Step 2: Select 2–3 Voices

Choose 2–3 writers whose styles fit the project. More than 3 gets muddled. Consider:

- **Primary voice** — sets the overall tone
- **Secondary voice** — adds a specific technique (e.g., proof-stacking, humor, urgency)
- **Accent voice** (optional) — a splash of something unexpected

### Step 3: Pull Prompt Fragments

Open the reference file (`.agent/skills/copywriting-styles/resources/Copywriting_Styles_Ultimate.md`) and search for the selected writers. Each entry includes an LLM prompt fragment (starts with "Write in the style of..."). Use these directly in prompts to the copybot or other LLMs.

### Step 4: Present the Style Plan

Before writing, present the style plan to the user:
- Which writers you selected for each section/deliverable
- Why each voice fits
- What the blended tone will feel like

Get approval before drafting.

## Funnel Stage Matching

| Stage | Recommended Voices |
|---|---|
| **Top of Funnel** (awareness) | Seth Godin, Harry Dry, Ann Handley — thought-provoking, shareable |
| **Middle of Funnel** (consideration) | Andre Chaperon, Robert Collier, Eben Pagan — trust-building |
| **Bottom of Funnel** (decision) | Gary Halbert, Dan Kennedy, Clayton Makepeace — urgency-driven |
| **Post-Purchase** (retention) | Laura Belgray, Ian Stanley, Ben Settle — ongoing engagement |

## Pro Tips

1. Always provide context about audience, offer, and desired outcome alongside style direction
2. Use the Key Technique column to understand WHAT makes each voice distinctive, then ask for that specifically
3. For client work, match the client's brand personality to the closest copywriter voice as a starting point
4. Test different voices for the same piece — the same offer can perform very differently depending on voice
5. Avoid asking for styles of obscure copywriters the LLM may not know well — stick to well-known names or provide examples
