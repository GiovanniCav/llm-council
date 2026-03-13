---
description: Manually trigger knowledge capture from current conversation to permanent documentation
---

# Chat Capture Workflow

## When to Use
- Explicitly capture something from the current conversation
- Force capture of content that wasn't auto-detected
- Batch capture multiple items at once

## Steps

### 1. Identify Content to Capture
List the specific decisions, frameworks, or tactics from this conversation that should be documented.

### 2. Classify Each Item
For each item, determine:
- **Type**: DECISION | TACTIC | FRAMEWORK | POLICY | SCRIPT
- **Target Workspace**: Based on `CONTROL_PLANE_SOT.md` Entity Registry
- **Target File**: Specific file path

### 3. Execute Capture
// turbo
For each item:
```bash
# Append to decisions.jsonl
echo '{"timestamp": "...", "decision_type": "...", ...}' >> logs/decisions.jsonl
```

For markdown targets:
- Append new section with timestamp header
- Include source conversation reference

### 4. Confirm
List all captured items with their target paths.

## Example Usage
User: "/chat-capture"
Response: "Scanning current conversation... Found 3 capturable items:
1. ✓ Push-Pull tactic → `SOW_TACTICS_SUMMARY.md`
2. ✓ Clinical Authority positioning → `Roadmap/README.md`
3. ✓ Grandmaster Council framework → `CONTROL_PLANE_SOT.md`

All captured."
