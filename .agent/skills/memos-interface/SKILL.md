---
name: memos-interface
description: Universal structured memory interface for AIOS workspaces. Import MemOS to persist state across sessions (Layer 1) and query deep knowledge via NotebookLM (Layer 2).
---

# MemOS Interface — Structured Memory for AIOS

## Overview
MemOS provides **two layers** of memory to every AIOS workspace:

| Layer | Purpose | Speed | Tool |
|-------|---------|-------|------|
| **Layer 1 (KV Store)** | Current state, configs, counters, IDs | Instant | `memos_core.py` |
| **Layer 2 (Semantic)** | Deep knowledge, transcripts, research | 5-30s | NotebookLM MCP |

## Layer 1: KV Store (Python)

### Setup
```python
import sys
sys.path.insert(0, "/Users/giovanni/Antigravity Projects/AIOS/scripts")
from memos_core import MemOS

memos = MemOS("/Users/giovanni/Antigravity Projects/<WorkspaceName>")
```

### Core Operations
```python
# Write (source is REQUIRED to prevent feedback loops)
memos.set("marketing.q2_budget", 5000, source="human")
memos.set("pipeline.active_leads", 12, source="agent_eval")

# Read
budget = memos.get("marketing.q2_budget")  # -> 5000

# Delete (prevents state bloat)
memos.delete("temp.scratch_value", source="agent_cleanup")

# List keys (discover state without loading payloads)
keys = memos.get_keys()           # all keys
keys = memos.get_keys("marketing")  # filtered
```

### Rules (MANDATORY)
1. **Layer 1 is for CURRENT STATE ONLY.** Never store transcripts, logs, or documents here.
2. **Always provide `source`.** This prevents infinite automation loops.
3. **Payload limit: 1000 characters.** If your data is larger, use Layer 2.
4. **Clean up ephemeral keys.** When a workflow completes, delete temporary keys.
5. **Query Layer 1 FIRST** for any factual/current data before falling back to Layer 2.

## Layer 2: Semantic Memory (NotebookLM)

### Setup
Each workspace can register one primary NotebookLM notebook:
```python
memos.set_notebook_id("your-notebook-uuid-here", source="human")
```

### Querying
Use the NotebookLM MCP tool with the stored notebook ID:
```
notebook_id = memos.get_notebook_id()
# Then use: mcp_notebooklm_notebook_query(notebook_id=notebook_id, query="...")
```

### Rules (MANDATORY)
1. **Layer 2 is for HISTORICAL CONTEXT and DEEP RESEARCH.** Never use it for current state.
2. **Handle 404s gracefully.** If the notebook was deleted, inform the user and offer to create a new one.
3. **Use `wait=True, wait_timeout=120`** when adding sources to avoid timeout crashes.
4. **Synthesize and Compact periodically.** Every ~10 raw meeting logs, summarize them into a "Quarterly Synthesis" document and delete the originals to maintain semantic density.

## Meeting Logger
```python
memos.log_meeting(
    attendees=["Giovanni", "Client"],
    topic="Q2 Strategy",
    summary="Discussed budget allocation...",
    decisions=["Increase ad spend by 20%"],
    source="human"
)
```
Meetings are saved as markdown in `<workspace>/brain/meeting_logs/`.

## Architecture Diagram
```
┌─────────────────────────────────────────┐
│              AIOS Agent                 │
│                                         │
│   "What's our Q2 budget?"              │
│         │                               │
│         ▼                               │
│   ┌─── Layer 1 (KV) ───┐               │
│   │ memos.get(key)      │── Fast, exact │
│   │ memos_state.json    │              │
│   └─────────────────────┘               │
│         │                               │
│   Not found? Need context?              │
│         │                               │
│         ▼                               │
│   ┌─── Layer 2 (RAG) ──┐               │
│   │ NotebookLM query    │── Deep, fuzzy │
│   │ primary_notebook_id │              │
│   └─────────────────────┘               │
└─────────────────────────────────────────┘
```
