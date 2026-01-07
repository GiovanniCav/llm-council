"""Logging module for transaction logging."""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Log file path - use CWD to ensure it ends up in project root
LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOG_DIR, "activity.jsonl")


def ensure_log_dir():
    """Ensure the log directory exists."""
    if not os.path.exists(LOG_DIR):
        print(f"LOGGER: Creating log directory at {LOG_DIR}")
        os.makedirs(LOG_DIR, exist_ok=True)


def log_transaction(
    conversation_id: str,
    prompt: str,
    stage3_result: Dict[str, Any],
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]] = None,
    aggregate_rankings: List[Dict[str, Any]] = None
):
    """
    Log a completed transaction to the JSONL file.
    
    Args:
        conversation_id: The UUID of the conversation
        prompt: The user's input prompt
        stage3_result: The final synthesized result from the chairman
        stage1_results: The list of initial responses from council members
        stage2_results: (Optional) The list of peer rankings and critiques
        aggregate_rankings: (Optional) The calculated aggregate scores
    """
    ensure_log_dir()
    
    # Extract detailed model usage info
    models_used = [r.get("model", "unknown") for r in stage1_results]
    
    # Construct comprehensive log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "conversation_id": conversation_id,
        "input_prompt": prompt,
        "final_synthesis": {
            "model": stage3_result.get("model", "unknown"),
            "response": stage3_result.get("content", "") or stage3_result.get("response", "")
        },
        "council_deliberations": {
            "stage1_individual_opinions": [
                {
                    "model": r.get("model"),
                    "response": r.get("response")
                }
                for r in stage1_results
            ],
            "stage2_peer_reviews": [
                {
                    "reviewer_model": r.get("model"),
                    "critique_and_ranking": r.get("ranking")
                }
                for r in (stage2_results or [])
            ],
            "aggregate_scores": aggregate_rankings
        },
        "metadata": {
            "model_count": len(models_used),
            "participating_models": models_used
        }
    }
    
    # Append to log file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
