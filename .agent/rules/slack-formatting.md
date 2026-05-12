---
description: Global Slack message formatting rules. Applies to ALL workspaces. Loaded at session start so it applies to any Slack message drafted mid-task.
---

# Slack Message Formatting Rules (Global)

## Presentation Layer (Claude to Giovanni)
Always wrap Slack messages, text messages, and similar short communications in a markdown code block (triple backticks) so Giovanni can copy/paste directly.

## Content Layer (What Goes Inside the Code Block)
Use plain text only. No formatting markup of any kind. Slack does not parse mrkdwn formatting when text is pasted from the clipboard, so asterisks, underscores, and other markup will show as literal characters.

### Rules
- No `*bold*` or `**bold**`. Use ALL CAPS for emphasis only when essential, or just use plain text.
- No `_italic_` underscores.
- No bullet characters (`-`, `*`, `+`). Use plain line breaks under a label (e.g., "Notes:").
- No headers (`#`, `##`). Use a label on its own line for structure.
- No `---` horizontal rules.
- No emoji shortcodes (`:rotating_light:` etc.).
- No placeholder brackets like `[Giovanni to add link]`. Just say "Content pack is here."
- No parenthetical details the team already knows.
- Structure with line breaks and labels only.

### Why Plain Text
When Giovanni copies text from a code block and pastes it into Slack's message composer, Slack's rich text editor does not parse mrkdwn markup from pasted clipboard content. Markup characters appear as literal text. Plain text with line breaks renders correctly every time.

## Tagging Convention (MANDATORY)

- **Primary recipient**: `@tag` at the very FIRST WORD of the message. This is the person you are talking to.
- **CC'd people**: `@tag` at the very BOTTOM of the message (last line or last section). These are people who need visibility but aren't the primary audience.
- Never pile all tags at the top. One recipient at top, observers at bottom.
- Do not tag the sender (Giovanni) unless the message is addressed to someone else and Giovanni needs to be CC'd.

## Openings, Closings, and Commitments

### No "Hi [Name]" greetings
The `@tag` at the first word IS the greeting. Do not add "Hi Lisa," or "Hey Kelley,". It is redundant and reads as formal/stiff.

### No name sign-offs
Do not end with "Giovanni" or similar. Slack already shows the sender. Sign-offs read as email conventions leaking into chat.

### Lead with acknowledgment when replying
When the message is a reply (to feedback, a question, a delivery), open with a short acknowledgment before the content. Examples:
- `@Lisa Campion Thanks for the review. v3 is in.`
- `@Kelley Got it. Content pack link below.`
- `@Mindy Good catch. Updated file attached.`
Keep it one line, one beat. Not sycophantic ("Great question!"), not performative. Just the human acknowledgment that lets the other person know they were heard before you move to the content.

### Version/deliverable naming
Use the SHIPPING name of the file or deliverable the recipient will see, not internal agent version tracking. If the file on disk is `W05_Content_Pack_V2.md` and the team calls it "v2," write "v2" in the Slack message even if the agent's internal process tracked it as V3. The client reads Slack against what they can see.

### Timing commitments: honest and conditional
Do not promise absolute turnaround if it depends on something outside your control. Use conditional phrasing:
- Yes: "If your edits come in by [time], I should be able to turn it around today."
- No: "I will turn any further changes around today." (overpromises if edits arrive at 4:55 PM)
- Yes: "Once Kelley sends the link, Kajabi load takes about an hour."
- No: "Kajabi will be live today." (ignores Kelley dependency)
Ownership framing does not mean absolute commitment. It means being the person who owns the piece you control AND naming the dependencies honestly.

## Voice
Write like the reader is smart but distracted. Get to the point, but don't skip the nuance.

- @ mention people directly. No "Hey team."
- State findings with confidence. No hedging ("it seems like," "it appears").
- No filler ("rough numbers are fine," "even estimates help").
- No repeating information the reader already knows.
- No em-dashes or en-dashes (follow no-dash-punctuation rule).
- Ask specific questions. Don't ask things the reader can't answer or that you could answer yourself.
- Don't claim completeness when there's still an open item. If something is pending, say "almost everything" or "most of what we need," not "everything we need."
- Don't present content pillars or deliverables as "confirmed" or "locked" when the client hasn't reviewed them yet. Use "for your review" or "proposed" until the client approves.
- Don't tag people who have their own intake channel or workflow for the same information. If Mindy already asked for the cadence in her own message, reply there or let the existing thread serve her. Don't pull extra people into a thread just to broadcast.

## Production Handoff Messages (Pack → Queue)

When a deliverable (content pack, asset, file) is being routed to a production teammate (George, Nicolai, etc.) to queue or post, keep the Slack message to 2-3 sentences. The deliverable contains the operational detail. The handoff message just routes attention.

Standard skeleton (when client approval is confirmed):

```
@Recipient The Content Pack for the week of [DATES] is approved and clear to queue. PDFs below. If anything is unclear, loop in @Giovanni. Thanks!
```

Skeleton when client did not respond in time but pack is shipping anyway:

```
@Recipient We didn't hear back from @client, so the Content Pack for the week of [DATES] is ready to queue. PDFs below. If anything is unclear, loop in @Giovanni. Thanks!
```

### Rules for Handoff Messages

1. **No internal codenames.** Production teammates do not think in "C1B1W4," "Block 2," or other agency-internal naming. Refer to the deliverable in plain language: "the Content Pack," "the deck," "the carousel." Internal codenames stay in file names and our session logs, not in Slack.

2. **Never claim approval state that isn't true.** "Approved" means the client has explicitly signed off. If the client went silent or did not respond by the deadline, write "ready to queue" and explicitly acknowledge the missing approval ("We didn't hear back from @client, so..."). Saying "approved" when the client didn't approve is a governance integrity violation.

3. **Tag the absent decision-maker.** When shipping without explicit client approval, tag the client (e.g., `@doug`) in the body of the message so they have visibility and a window to intervene if anything is wrong before it goes live.

4. **Do NOT restate in the Slack message:**
   - Week metadata (vertical, theme, offer details)
   - Keyword guidance, channel cadence, carousel days
   - Dual-CTA / version-selection logic
   - Anything else already documented in the linked pack

The recipient opens the pack and reads it. The message just opens the door.

Exception: pre-approval messages, mid-cycle escalations, or status updates where the recipient cannot yet read a final deliverable. Those follow the normal Voice rules above.

## Scope
Applies to all Slack messages, text messages, and any short-form communication drafted for Giovanni across all workspaces.
