---
name: chat-capture
description: Automatically detect and capture strategic decisions, frameworks, and tactics from conversations into workspace documentation. I will proactively suggest capture when valuable content is detected.
---

# Chat Capture Skill

## Automatic Detection Triggers

I will **proactively suggest capture** when the conversation contains:

| Trigger | Example | Target |
|---------|---------|--------|
| **Decision Made** | "Let's go with Option A" | `logs/decisions.jsonl` |
| **Framework Defined** | "The 3-step process is..." | Tactic card or knowledge base |
| **Tactic Documented** | "Here's how Push-Pull works..." | `SOW_TACTICS_SUMMARY.md` or similar |
| **Policy Set** | "From now on, always do X" | `CONTROL_PLANE_SOT.md` |
| **Entity Classification** | "B&B Filters is a client" | Entity Registry |
| **Script/Prompt Created** | System prompts, sales scripts | Target workspace |
| **Mental Model Discovered** | "This is an example of the Cobra Effect" | `Master_Mental_Models_Catalog.md` |

## Capture Protocol

### Step 1: Detect Capturable Content
When I detect valuable content, I will:
1. Suggest: "This looks like a good candidate for permanent documentation. Shall I capture it?"
2. If approved (or by default), proceed to capture

### Step 2: Classify & Route
```
DECISION      → logs/decisions.jsonl
TACTIC        → knowledge_base/ or workspace tactic file
FRAMEWORK     → doc-generator SYSTEM_INTELLIGENCE_SPEC
POLICY        → CONTROL_PLANE_SOT.md
KNOWLEDGE     → Antigravity Sidebar (via Synthesis)
SCRIPT/PROMPT → target workspace
MENTAL MODEL  → Project Factory/02_Areas/Knowledge_Base/Mental_Models/Master_Mental_Models_Catalog.md
```

### Step 3: Write to Target
- Use atomic append for JSONL files
- Use section append for markdown files
- Always include timestamp and conversation context

### Step 4: Confirm Capture
Brief confirmation: "✓ Captured to `{target_file}`"

## decisions.jsonl Schema

```json
{
  "timestamp": "ISO8601",
  "conversation_id": "string (from chat metadata)",
  "decision_type": "TACTIC | FRAMEWORK | POLICY | CONFIG | SCRIPT | MENTAL_MODEL",
  "summary": "string (1-2 sentences)",
  "target_file": "string (path to doc that was updated)",
  "workspace": "string (e.g. Roadmap, Project Factory)"
}
```

## Mental Model Capture Schema

When capturing a new mental model, append it to `Master_Mental_Models_Catalog.md` using exactly this format:
```markdown
### [Model Name]
**Category:** [Layer/Domain]
**Source:** [Where it was found/Conversation context]

**Explanation:**
[Detailed explanation]

**How to Apply It:**
[Practical, step-by-step application guide]

---
```

## Integration with Existing Skills

| Skill | Integration |
|-------|-------------|
| `doc-generator` | Use templates for framework documentation |
| `manifest-sync` | Check for existing entries before creating duplicates |

## Proactive Suggestion Template

When I detect capturable content, I'll suggest:

> 💾 **Knowledge Capture**: I noticed [description of content]. This should be documented in `[target]`. Capturing now...

For decisions requiring your input on target:

> 💾 **Knowledge Capture**: You just defined [description]. Where should this live?
> 1. `Project Factory/...` (operational)
> 2. `Roadmap/...` (product)
> 3. `knowledge_base/...` (training)
