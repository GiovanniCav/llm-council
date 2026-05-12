---
name: infinite-brain-architecture
description: Official AI Memory SOP and "Infinite Brain" knowledge architecture for all Antigravity workspaces. Enforces atomic notes, 16 node types, multi-layered storage, and strict provenance.
---

# Infinite Brain Architecture (AI Memory SOP)

## Overview
This is the official knowledge management standard for all Antigravity workspaces. It replaces traditional PARA folder systems with an AI-native "Infinite Brain" architecture designed for token efficiency, high-fidelity persona emulation, and automated synthesis.

Whenever an AI agent acts on, reads, or updates knowledge in any workspace, it **must** adhere to this architecture.

## Multi-Layered Architecture

1. **Layer 1: Raw Source Archive (`Inbox/` and `05_Raw_Archive/`)**
   - **Purpose:** Full-fidelity preservation of raw transcripts, PDFs, and media.
   - **Mechanism:** Files are kept in their entirety to allow NotebookLM to ingest them. This enables deep semantic queries and persona emulation without lossy compression.

2. **Layer 2: The Atomic Infinite Brain (`04_Wiki/` - Obsidian Vault)**
   - **Purpose:** Fast, token-efficient, local knowledge retrieval for daily AIOS tasks.
   - **Mechanism:** The wiki consists exclusively of **Atomic Notes (50-300 lines max)**. Do not create massive monolithic files. Break down large concepts into separate notes connected by edges.

3. **Layer 2.5: Routing Tables (MOCs)**
   - **Purpose:** To aggregate atomic notes into human-readable and AI-traversable hubs.
   - **Mechanism:** Specific index notes (Maps of Content) that group abstracted edge-scenarios (e.g., `Routing_Table_Buyer_Data.md` linking to all individual pain point notes).

## The 16 Node Types
Every file created in Layer 2 (`04_Wiki/`) MUST be strictly categorized into one of these 16 types (often indicated in the frontmatter or folder structure):
1. Pillars
2. Decisions
3. Concepts
4. Questions
5. Playbooks
6. Tasks
7. Events
8. Patterns
9. Hypotheses
10. Facts
11. Sources
12. Bookmarks
13. Notes
14. Contacts
15. References
16. Custom

## YAML Frontmatter & Complex Edges
Instead of relying solely on standard wikilinks `[[Link]]`, relationships between nodes MUST be defined in the YAML frontmatter to allow programmatic parsing by agents.

```yaml
---
aliases: ["Alternative Name 1", "Alternative Name 2"]
node_type: Concept
source_files: ["raw_transcript_123.txt"]
last_updated: YYYY-MM-DD
edges:
  supports: ["[[Other_Concept_A]]"]
  contradicts: ["[[Old_Framework_B]]"]
  depends_on: ["[[Core_Pillar_C]]"]
  derived_from: ["[[Source_Raw_File]]"]
---
```

## Mandatory AI Agent Rules

### 1. The Corpus Cross-Validation Rule (No Premature Convergence)
Before establishing a "Foundational Concept" or drafting a new framework page, the AIOS **MUST** query the corpus (Layer 1 NotebookLM or Layer 2 Wiki) for contradictions, updates, or expanded versions to avoid treating an outdated/partial file as ground truth.

### 2. Strict Provenance
Every factual claim or core definition in a wiki page MUST include an inline citation linking back to the specific raw file. Rely on *verbatim quotes* rather than LLM paraphrasing to preserve the expert's exact voice.

### 3. Canonical Entity Enforcement
Before creating a new page, the AIOS MUST search existing aliases and indices to verify if a variation of that entity already exists to prevent "Graph Rot" (e.g., `Clairvoyance.md` vs `The Clairvoyance Concept.md`).
