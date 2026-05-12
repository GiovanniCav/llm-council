---
name: llm-router
description: Cost-control middleware that routes LLM requests to the cheapest appropriate model based on task complexity. Supports Google, Anthropic, OpenAI, and OpenRouter providers.
---

# LLM Router Skill

This skill provides a **cost-control middleware** for programmatic LLM calls. Instead of defaulting every task to the most expensive model, the router maps task types to the cheapest model that can handle them reliably.

## The 3-Tier Model

| Tier | Default Model | Use When | Approx. Cost |
|------|--------------|----------|-------------|
| **Fast** | Gemini 2.0 Flash | Formatting, classification, typo fixes, short extraction | **Free** |
| **Standard** | Gemini 2.5 Flash | Summarization, rewriting, translation, drafting | ~$0.60/1M out |
| **Deep** | Claude Sonnet 4 | Strategy, analysis, code gen, creative writing, debugging | ~$15/1M out |

## How to Use (Python)

```python
from llm_router import route, call_llm

# 1. Check which model a task type maps to
tier = route("summarize")  # Returns: {"tier": "standard", "model": "gemini-2.5-flash-preview-05-20", ...}

# 2. Make a routed LLM call (handles provider API differences automatically)
response = call_llm("format", "Fix capitalization: hello world")

# 3. Override the tier for a specific call
response = call_llm("format", "Complex formatting task", tier_override="deep")
```

## Supported Task Types

### Fast Tier (Free)
`format`, `classify`, `extract`, `typo_fix`

### Standard Tier (~$0.60/1M output tokens)
`summarize`, `rewrite`, `translate`, `draft`

### Deep Tier (~$15/1M output tokens)
`analyze`, `strategize`, `generate_code`, `creative_write`, `debug`

**Unknown task types** automatically fall back to the `standard` tier.

## Configuration

The routing rules are defined in `config/routing_config.json`. To change which model handles which task type, edit that file — no code changes required.

All API keys are loaded from the centralized `AIOS/config/.env` file via `load_dotenv`. **Never hardcode API keys.**

### Available Providers
- **Google** (`GOOGLE_API_KEY`) — Gemini models
- **Anthropic** (`ANTHROPIC_API_KEY`) — Claude models
- **OpenAI** (`OPENAI_API_KEY`) — GPT models
- **OpenRouter** (`OPENROUTER_API_KEY`) — Multi-provider gateway (300+ models)

## Cost Logging

Every routed call is logged to `AIOS/logs/llm_router.log` with:
- Timestamp, task type, tier, model used
- Input/output token counts
- Estimated cost

Use this log to audit spending and optimize routing rules over time.

## Adding New Task Types

1. Open `config/routing_config.json`
2. Add your task type to the `routing_rules` object
3. Map it to `fast`, `standard`, or `deep`
4. The router picks it up immediately — no restart needed

## Switching Models

To change which model handles a tier (e.g., swap Standard from Gemini to GPT-4o-mini):

1. Open `config/routing_config.json`
2. Edit the `tiers.standard.model` and `tiers.standard.provider` fields
3. Save — the router uses the new model on the next call
