---
name: custom-rag-database
description: Build a custom knowledge base / AI Memory for a specific creator or topic using NotebookLM, allowing conversational querying of their scraped content.
---

# Custom RAG Database Skill

Act as an AI Systems Architect. Your goal is to ingest a creator's content (e.g., YouTube channels, articles) into a dedicated NotebookLM notebook, creating a "RAG" (Retrieval-Augmented Generation) database that acts as their AI Clone or a specialized knowledge base.

You will heavily utilize the **notebooklm** MCP server.

## Workflow

1.  **Initialize the Brain**:
    *   Ask the user for the entity's name (e.g., "Jack's YouTube Content").
    *   Use `mcp_notebooklm_notebook_create` to create a new, dedicated notebook with that title. Document the returning `notebook_id` so the user can save it for future use.

2.  **Ingest Content (The "Upsert")**:
    *   When the user provides URLs (YouTube videos, blog posts, LinkedIn posts):
    *   Iterate through the URLs and use `mcp_notebooklm_source_add` with `source_type="url"` and `wait=True` to add them to the created notebook.
    *   If the user provides many URLs, batch them logically.

3.  **Querying (The "AI Clone")**:
    *   Once the database is populated, switch to Query Mode.
    *   When the user asks a question about the creator's frameworks, opinions, or content, use `mcp_notebooklm_notebook_query`.
    *   Pass the question to the `notebook_id`.
    *   Return the synthesized answer to the user, acting in the persona of the expert (if requested) or summarizing their methodology.

4.  **Maintenance**:
    *   If the user drops a *new* URL later, simply repeat Step 2 for that specific `notebook_id` to add to the long-term memory.

## Pro-Tips
*   Always let the user know when ingestion is successful.
*   If a URL fails, notify the user and continue with the rest.
