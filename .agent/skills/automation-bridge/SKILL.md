---
name: automation-bridge
description: Safely trigger n8n workflows, enforcing rate limits and human-in-the-loop approvals for the AIOS.
---

# Automation Bridge Skill

This skill provides the standard, safe protocol for AI agents to trigger external automations (primarily n8n) without causing runaway loops, spam, or accidental deployments.

## The Prime Directives

1. **NO HARDCODED URLS**: Never hardcode a webhook URL in your scripts, workflows, or markdown files. All webhook URLs are air-gapped into the system `.env` file and must be loaded dynamically.
2. **RATE LIMITING IS MANDATORY**: Do not blindly loop webhook calls. Use the `trigger_n8n.py` script, which enforces a built-in rate limit (e.g., max 5 calls per hour per workspace).
3. **HUMAN IN THE LOOP**: For high-stakes actions (deployments, mass client emails, financial transactions, or major infrastructure changes), you MUST queue the action for human approval rather than executing it directly.

## Usage Matrix

When you determine that an automation needs to be triggered, follow this matrix:

### Scenario A: Low-Stakes / Informational
*Examples: Sending a notification to Slack, updating a low-priority spreadsheet, fetching minor data.*
1. Prepare a JSON payload.
2. Run the trigger script: `python3 .agent/skills/automation-bridge/scripts/trigger_n8n.py --webhook "slack-notify" --payload payload.json`
3. The script will handle the API call using the `.env` base URL and record the rate limit.

### Scenario B: High-Stakes / Destructive / Public-Facing
*Examples: Sending an email to a client list, deploying code to production, modifying billing.*
1. **DO NOT run the trigger script.**
2. Instead, add an entry to the `pending_approvals` array in your workspace's `status.json` file.
3. Use the `notify_user` tool to inform the user that the action is staged and awaiting their approval on the CEO Dashboard.
4. Once the user approves, *then* you may execute the trigger.

## The Script
The universal trigger script is located at `.agent/skills/automation-bridge/scripts/trigger_n8n.py`.
Run it with `--help` for exact usage syntax if you forget.
