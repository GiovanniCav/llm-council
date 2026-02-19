---
description: Initialize a new project using the BLAST framework
---

# BLAST Project Initialization
> **Blueprint → Linkage → Architect → Stylize → Trigger**
> Use this workflow to start ANY new project with the correct structure and context.

---

## 1. Blueprint (The "What" & "Why")
> *Define the outcome before the output.*

1. **Create the Project Folder**:
   - create a new folder in `01_Projects/` (e.g., `01_Projects/My_New_Project`)
   - `cd` into it.

2. **Create `project_charter.md`**:
   - Create a file named `project_charter.md`.
   - Paste the following template and fill it out:

```markdown
# Project Charter: [Project Name]

## 1. Objective
*   **What**: [One sentence description of the deliverable]
*   **Why**: [The business value or problem solved]
*   **Success Criteria**: [Bullet points of what "done" looks like]

## 2. Constraints
*   **Deadline**: [Date]
*   **Budget/Resources**: [Time, money, people]
*   **Non-Negotiables**: [What must NOT happen?]

## 3. Stakeholders
*   **Owner**: [Who is responsible?]
*   **Approver**: [Who signs off?]
```

---

## 2. Linkage (The "Who" & "Where")
> *Connect the dots before building the walls.*

1. **Identify Dependencies**:
   - Does this project depend on other active projects?
   - Does it block anything?
   - Update `project_charter.md` with a "Dependencies" section if needed.

2. **Connect to Knowledge Base**:
   - Identify which `03_Resources/` or `brain/` files are relevant.
   - *Example*: "Reference `brand_guidelines.md` for voice."
   - *Example*: "Reference `client_intel.md` for background."

---

## 3. Architect (The "How")
> *Structure the work.*

1. **Create the Work Plan**:
   - Create a file named `work_plan.md` (or use `task.md` if preferred).
   - Break the project into phases (Phase 1, Phase 2, Phase 3).
   - List specific tasks for Phase 1.

2. **Scaffold the Directory**:
   - Create necessary subfolders (e.g., `drafts/`, `assets/`, `research/`).
   - *Note*: Keep it flat if possible (max 3 levels deep).

---

## 4. Stylize (The "Vibe")
> *Align with identity.*

1. **Review Brand Guidelines**:
   - Open `brand_guidelines.md` (if CLIENT workspace) or `IDENTITY.md` (if ENGINE).
   - Confirm the voice/tone for this specific project.

2. **Set the Tone**:
   - In your `project_charter.md`, add a "Voice/Tone" section.
   - *Example*: "This should sound like Doug Noll — clinical, direct, no fluff."

---

## 5. Trigger (The "Go")
> *Start the engine.*

1. **First Action**:
   - Identify the immediate next physical action (GTD style).
   - *Example*: "Draft outline," "Send email," "Run script."

2. **Log It**:
   - Add the project to your `task.md` or active project list.
   - Start working on Step 1.
