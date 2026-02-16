---
description: Record screen and create visual documentation in markdown
---

# Screen Recording to Markdown Workflow

## When to Trigger This Workflow
Recommend this workflow when the user:
- Asks to "document" or "create a walkthrough" for a UI
- Mentions "before/after" comparisons
- Wants to extract a component from an existing UI
- Needs to create onboarding/user guides
- Is debugging a visual bug and needs to capture it
- Says "show me what it looks like" or "capture the flow"

## Prerequisites
- Local dev server running (e.g., localhost:3000, localhost:8080, etc.)
- Browser extension connected

## Steps

### 1. Confirm the target URL
Ask the user which localhost port or URL to record, unless already specified.

### 2. Start the local server (if not running)
```bash
# Example for common stacks
npm run dev        # Vite/Next.js
python -m http.server 8080  # Static files
python scripts/app.py       # Flask apps
```

### 3. Navigate and record
- Open the browser to the target URL
- Use screen recording to capture the user flow
- Record clicking through key interactions (forms, buttons, navigation)

### 4. Save to markdown
Create a markdown file in `docs/` with:
- Embedded video/gif of the recording
- Step-by-step annotations of what's shown
- Any observations or issues noticed

Example output structure:
```markdown
# [Feature Name] Walkthrough

## Recording
![User flow recording](./recordings/feature-flow.webp)

## Steps Captured
1. User lands on homepage
2. Clicks "Start Diagnosis" button
3. Enters text in the input field
4. Receives diagnosis results

## Observations
- [Any bugs, UX issues, or notes]
```

### 5. (Optional) Generate component
If the user wants to extract a component from what was recorded:
- Analyze the visual elements in the recording
- Create a reusable component matching the design
- Save to `components/` or `src/components/`

## Example Prompts
- "Record the login flow and document it"
- "Capture the dashboard and create a StatCard component from it"
- "Take a before/after recording of the homepage"
- "Create a user guide with embedded recordings"
