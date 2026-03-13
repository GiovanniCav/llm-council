---
name: infographic-engine
description: Generate intelligent, brand-aware NotebookLM infographic prompts.
---

# Infographic Engine Skill

Use this skill to transform raw content and brand data into "Master Single Source of Truth" prompts for NotebookLM's infographic feature.

## Capabilities

### `generate_infographic_prompt`
Generates a highly structured prompt based on client context and desired aesthetic.

**Parameters:**
- `brand_context`: (Object) Contains `brand_name`, `brand_palette`, `target_audience`, etc.
- `content_summary`: (String) Brief description of the information to be visualized.
- `preferred_style`: (String, Optional) One of the styles from `style_library.json`. If omitted, the engine will recommend the best fit.

**Usage:**
1. Read `resources/style_library.md` for inspiration.
2. Use the "Creative Director" mental model to assess which variables best suit the brand.
3. Call `scripts/infographic_maestro.py` or synthesize the response directly if in a high-context execution.

## Mental Models
- **Synthesize, Don't Just Hydrate**: If the brand is "Organic Tech", combine "Bento Grid" structure with "Watercolor" textures.
- **The Pillar Principle**: Every prompt MUST define Tone, Visual Identity, Image Style, Typography, and Categories.
