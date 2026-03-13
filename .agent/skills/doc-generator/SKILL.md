---
name: doc-generator
description: Generate technical documentation, handover specs, or system intelligence reports. Use when documenting projects, creating walkthroughs, or preparing handover materials.
---

# Documentation Generator Skill

## When to Use
- User asks to "document" a project or feature
- User mentions "handover", "handoff", or "transition"
- User wants a "technical spec" or "system report"
- User asks for a "walkthrough" of functionality
- Project is complete and needs final documentation

## Document Types

### 1. SYSTEM_INTELLIGENCE_SPEC
**Purpose**: Deep technical dive into how a system works.

**Template Structure**:
```markdown
# 🧠 Technical Intelligence Report: [Project Name]
**Version**: 1.0  
**Context**: [One-line description]

## 📋 Executive Summary
[2-3 sentence overview of what was built and why]

## 🏗 System Architecture
[Diagram or description of components]

## 🔎 Core Logic
[Explanation of main algorithms/processes]

## 🛠 Lessons Learned & Anti-Patterns
### ❌ How NOT to do it:
[List of mistakes and why they failed]

### ✅ How to do it right:
[Best practices discovered]

## 📊 Technical Specs & Data
[Metrics, IDs, configurations]

## 🚀 Future Scaling Recommendations
[What to do as the system grows]
```

---

### 2. HANDOVER_SPEC
**Purpose**: Enable someone else to take over the project.

**Template Structure**:
```markdown
# [Project Name] Handover Specification

## Quick Start
[How to get up and running in < 5 minutes]

## Architecture Overview
[Key components and how they connect]

## Key Files
| File | Purpose |
|------|---------|
| ... | ... |

## Environment Variables
| Variable | Purpose | Example |
|----------|---------|---------|
| ... | ... | ... |

## Common Operations
[How to do the most frequent tasks]

## Known Issues
[Active bugs or limitations]

## Contacts
[Who to ask for help]
```

---

### 3. WALKTHROUGH
**Purpose**: Step-by-step guide for a specific flow.

**Template Structure**:
```markdown
# [Feature] Walkthrough

## Overview
[What this walkthrough covers]

## Prerequisites
[What needs to be set up first]

## Steps

### Step 1: [Action]
[Description]
![Screenshot](./recordings/step1.webp)

### Step 2: [Action]
[Description]

## Expected Outcome
[What success looks like]

## Troubleshooting
[Common issues and fixes]
```

## Execution Checklist

1. **Identify Type**: Which template fits the user's need?
2. **Gather Sources**:
   - Existing code and comments
   - `logs/activity.jsonl` for history
   - Screenshots/recordings if available
   - User conversations for context
3. **Apply Template**: Fill in each section
4. **Output Location**:
   - Root of workspace (for specs)
   - `/docs/` directory (for walkthroughs)
5. **Log Creation**: Append to activity log

## Quality Checklist
- [ ] All code snippets are tested/accurate
- [ ] No placeholder text remains
- [ ] Links to files use absolute paths
- [ ] Mermaid diagrams render correctly
- [ ] Emoji usage is consistent with existing docs

## Integration with Screen Recording
If visual documentation is needed:
1. Use `/screen-record-to-md` workflow
2. Embed `.webp` recordings in walkthrough
3. Add step-by-step annotations
