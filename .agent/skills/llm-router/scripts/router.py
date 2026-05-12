"""
LLM Router — Cost-control middleware for the AIOS.

Routes LLM requests to the cheapest appropriate model based on task complexity.
Supports Google (Gemini), Anthropic (Claude), OpenAI (GPT), and OpenRouter.

Usage:
    from llm_router import route, call_llm

    tier_info = route("summarize")
    response = call_llm("format", "Fix capitalization: hello world")
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

from dotenv import load_dotenv

# ─── Configuration ───
BASE_DIR = os.environ.get("ANTIGRAVITY_ROOT", "/Users/giovanni/Antigravity Projects")
load_dotenv(os.path.join(BASE_DIR, "AIOS", "config", ".env"), override=True)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "routing_config.json")
LOG_PATH = os.path.join(BASE_DIR, "AIOS", "logs", "llm_router.log")


def _load_config():
    """Load the routing configuration."""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def route(task_type, config=None):
    """
    Determine which model tier and provider to use for a given task type.

    Args:
        task_type: One of the supported task types (e.g., "format", "summarize", "analyze")
        config: Optional pre-loaded config dict

    Returns:
        dict with keys: tier, provider, model, max_tokens, cost_per_1m_input, cost_per_1m_output
    """
    if config is None:
        config = _load_config()

    tier_name = config["routing_rules"].get(task_type, config["fallback_tier"])
    tier = config["tiers"][tier_name]

    return {
        "tier": tier_name,
        "provider": tier["provider"],
        "model": tier["model"],
        "max_tokens": tier["max_tokens"],
        "cost_per_1m_input": tier["cost_per_1m_input"],
        "cost_per_1m_output": tier["cost_per_1m_output"],
    }


def _call_google(model, prompt, max_tokens, api_key):
    """Call Google Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["candidates"][0]["content"]["parts"][0]["text"]
    usage = result.get("usageMetadata", {})
    return {
        "text": text,
        "input_tokens": usage.get("promptTokenCount", 0),
        "output_tokens": usage.get("candidatesTokenCount", 0),
    }


def _call_anthropic(model, prompt, max_tokens, api_key):
    """Call Anthropic Claude API."""
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["content"][0]["text"]
    usage = result.get("usage", {})
    return {
        "text": text,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
    }


def _call_openai_compatible(model, prompt, max_tokens, api_key, base_url="https://api.openai.com/v1"):
    """Call OpenAI or OpenRouter (both use the same chat completions API format)."""
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return {
        "text": text,
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
    }


def _log_call(task_type, tier_info, tokens_in, tokens_out, elapsed_ms):
    """Append a cost log entry to the router log file."""
    cost_in = (tokens_in / 1_000_000) * tier_info["cost_per_1m_input"]
    cost_out = (tokens_out / 1_000_000) * tier_info["cost_per_1m_output"]
    total_cost = cost_in + cost_out

    entry = {
        "timestamp": datetime.now().isoformat(),
        "task_type": task_type,
        "tier": tier_info["tier"],
        "provider": tier_info["provider"],
        "model": tier_info["model"],
        "input_tokens": tokens_in,
        "output_tokens": tokens_out,
        "estimated_cost_usd": round(total_cost, 6),
        "elapsed_ms": elapsed_ms,
    }

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def call_llm(task_type, prompt, tier_override=None, max_tokens_override=None):
    """
    Route and execute an LLM call.

    Args:
        task_type: The type of task (e.g., "format", "summarize", "analyze")
        prompt: The prompt to send to the LLM
        tier_override: Optional tier name to force (e.g., "deep")
        max_tokens_override: Optional max tokens override

    Returns:
        dict with keys: text, model, tier, input_tokens, output_tokens, estimated_cost_usd
    """
    config = _load_config()

    if tier_override:
        tier_info = {
            "tier": tier_override,
            "provider": config["tiers"][tier_override]["provider"],
            "model": config["tiers"][tier_override]["model"],
            "max_tokens": config["tiers"][tier_override]["max_tokens"],
            "cost_per_1m_input": config["tiers"][tier_override]["cost_per_1m_input"],
            "cost_per_1m_output": config["tiers"][tier_override]["cost_per_1m_output"],
        }
    else:
        tier_info = route(task_type, config)

    max_tokens = max_tokens_override or tier_info["max_tokens"]
    provider = tier_info["provider"]
    model = tier_info["model"]

    # Resolve the API key
    provider_config = config["providers"][provider]
    api_key = os.environ.get(provider_config["env_key"])
    if not api_key:
        raise ValueError(
            f"API key not found for provider '{provider}'. "
            f"Set {provider_config['env_key']} in AIOS/config/.env"
        )

    # Dispatch to the correct provider
    start = time.time()
    try:
        if provider == "google":
            result = _call_google(model, prompt, max_tokens, api_key)
        elif provider == "anthropic":
            result = _call_anthropic(model, prompt, max_tokens, api_key)
        elif provider in ("openai", "openrouter"):
            result = _call_openai_compatible(
                model, prompt, max_tokens, api_key, provider_config["base_url"]
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"LLM API Call Failed ({provider} - HTTP {e.code}): {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"LLM Network Error ({provider}): {e.reason}")

    elapsed_ms = int((time.time() - start) * 1000)

    # Log the call
    _log_call(task_type, tier_info, result["input_tokens"], result["output_tokens"], elapsed_ms)

    cost_in = (result["input_tokens"] / 1_000_000) * tier_info["cost_per_1m_input"]
    cost_out = (result["output_tokens"] / 1_000_000) * tier_info["cost_per_1m_output"]

    return {
        "text": result["text"],
        "model": model,
        "tier": tier_info["tier"],
        "provider": provider,
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "estimated_cost_usd": round(cost_in + cost_out, 6),
        "elapsed_ms": elapsed_ms,
    }


# ─── CLI Interface ───
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AIOS LLM Router")
    subparsers = parser.add_subparsers(dest="command")

    # Route command: show which tier/model a task maps to
    route_parser = subparsers.add_parser("route", help="Show routing for a task type")
    route_parser.add_argument("task_type", help="Task type to route (e.g., format, summarize, analyze)")

    # Call command: execute a routed LLM call
    call_parser = subparsers.add_parser("call", help="Execute a routed LLM call")
    call_parser.add_argument("task_type", help="Task type")
    call_parser.add_argument("prompt", help="Prompt text (or - to read from stdin)")
    call_parser.add_argument("--tier", help="Override tier (fast, standard, deep)")
    call_parser.add_argument("--max-tokens", type=int, help="Override max tokens")

    # Tiers command: list all tiers
    subparsers.add_parser("tiers", help="List all available tiers")

    args = parser.parse_args()

    if args.command == "route":
        info = route(args.task_type)
        print(json.dumps(info, indent=2))

    elif args.command == "call":
        prompt_text = sys.stdin.read() if args.prompt == "-" else args.prompt
        result = call_llm(args.task_type, prompt_text, tier_override=args.tier, max_tokens_override=args.max_tokens)
        print(result["text"])
        print(f"\n--- Router: {result['tier']} tier → {result['model']} | "
              f"{result['input_tokens']}+{result['output_tokens']} tokens | "
              f"${result['estimated_cost_usd']:.6f} | {result['elapsed_ms']}ms ---",
              file=sys.stderr)

    elif args.command == "tiers":
        config = _load_config()
        for name, tier in config["tiers"].items():
            print(f"  {name:10s}  {tier['provider']:12s}  {tier['model']:40s}  ${tier['cost_per_1m_output']:.2f}/1M out")

    else:
        parser.print_help()
