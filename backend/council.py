"""3-stage LLM Council orchestration."""

import json
from typing import List, Dict, Any, Tuple
from .openrouter import query_models_parallel, query_model
from .config import COUNCIL_MODELS, CHAIRMAN_MODEL


async def stage1_collect_responses(user_query: str) -> List[Dict[str, Any]]:
    """
    Stage 1: Collect individual responses from all council models.

    Args:
        user_query: The user's question

    Returns:
        List of dicts with 'model' and 'response' keys
    """
    messages = [{"role": "user", "content": user_query}]

    # Query all models in parallel
    responses = await query_models_parallel(COUNCIL_MODELS, messages)

    # Format results
    stage1_results = []
    for model, response in responses.items():
        if response is not None:  # Only include successful responses
            stage1_results.append({
                "model": model,
                "response": response.get('content', '')
            })

    return stage1_results


async def stage2_collect_rankings(
    user_query: str,
    stage1_results: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Stage 2: Each model ranks the anonymized responses.

    Args:
        user_query: The original user query
        stage1_results: Results from Stage 1

    Returns:
        Tuple of (rankings list, label_to_model mapping)
    """
    # Create anonymized labels for responses (Response A, Response B, etc.)
    labels = [chr(65 + i) for i in range(len(stage1_results))]  # A, B, C, ...

    # Create mapping from label to model name
    label_to_model = {
        f"Response {label}": result['model']
        for label, result in zip(labels, stage1_results)
    }

    # Build the ranking prompt
    responses_text = "\n\n".join([
        f"Response {label}:\n{result['response']}"
        for label, result in zip(labels, stage1_results)
    ])

    ranking_prompt = f"""You are evaluating different responses to the following question using the Analysis of Competing Hypotheses (ACH) method:

Question: {user_query}

Here are the responses from different models (anonymized):

{responses_text}

Your task (ACH Falsification):
1. Treat each response as a COMPETING HYPOTHESIS about the best answer.
2. For each response, identify what DISCONFIRMING evidence exists: what does it get wrong, what does it miss, what assumptions does it make that could be false?
3. Focus on ELIMINATION, not confirmation. The goal is to identify which responses can be RULED OUT, not which one "feels" best.
4. Then, at the very end, provide a final ranking based on which responses have the LEAST disconfirming evidence (not the most confirming evidence).

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line should be: number, period, space, then ONLY the response label (e.g., "1. Response A")
- Do not add any other text or explanations in the ranking section

Example of the correct format for your ENTIRE response:

Response A assumes X, but this is contradicted by Y. Key weakness: ...
Response B avoids the error in A but introduces a new assumption about Z that is unsupported...
Response C has the fewest falsifiable claims and addresses the core question most directly...

FINAL RANKING:
1. Response C
2. Response A
3. Response B

Now provide your ACH falsification analysis and ranking:"""

    messages = [{"role": "user", "content": ranking_prompt}]

    # Get rankings from all council models in parallel
    responses = await query_models_parallel(COUNCIL_MODELS, messages)

    # Format results
    stage2_results = []
    for model, response in responses.items():
        if response is not None:
            full_text = response.get('content', '')
            parsed = parse_ranking_from_text(full_text)
            stage2_results.append({
                "model": model,
                "ranking": full_text,
                "parsed_ranking": parsed
            })

    return stage2_results, label_to_model


async def stage3_synthesize_final(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Stage 3: Chairman synthesizes final response.

    Args:
        user_query: The original user query
        stage1_results: Individual model responses from Stage 1
        stage2_results: Rankings from Stage 2

    Returns:
        Dict with 'model' and 'response' keys
    """
    # Build comprehensive context for chairman
    stage1_text = "\n\n".join([
        f"Model: {result['model']}\nResponse: {result['response']}"
        for result in stage1_results
    ])

    stage2_text = "\n\n".join([
        f"Model: {result['model']}\nRanking: {result['ranking']}"
        for result in stage2_results
    ])

    chairman_prompt = f"""You are the Chairman of an LLM Council. Multiple AI models have provided responses to a user's question, and then ranked each other's responses.

Original Question: {user_query}

STAGE 1 - Individual Responses:
{stage1_text}

STAGE 2 - Peer Rankings:
{stage2_text}

Your task as Chairman is to synthesize all of this information into a single, comprehensive, accurate answer to the user's original question. Consider:
- The individual responses and their insights
- The peer rankings and what they reveal about response quality
- Any patterns of agreement or disagreement

Provide a clear, well-reasoned final answer that represents the council's collective wisdom:"""

    messages = [{"role": "user", "content": chairman_prompt}]

    # Query the chairman model
    response = await query_model(CHAIRMAN_MODEL, messages)

    if response is None:
        # Fallback if chairman fails
        return {
            "model": CHAIRMAN_MODEL,
            "response": "Error: Unable to generate final synthesis."
        }

    return {
        "model": CHAIRMAN_MODEL,
        "response": response.get('content', '')
    }


def parse_ranking_from_text(ranking_text: str) -> List[str]:
    """
    Parse the FINAL RANKING section from the model's response.

    Args:
        ranking_text: The full text response from the model

    Returns:
        List of response labels in ranked order
    """
    import re

    # Look for "FINAL RANKING:" section
    if "FINAL RANKING:" in ranking_text:
        # Extract everything after "FINAL RANKING:"
        parts = ranking_text.split("FINAL RANKING:")
        if len(parts) >= 2:
            ranking_section = parts[1]
            # Try to extract numbered list format (e.g., "1. Response A")
            # This pattern looks for: number, period, optional space, "Response X"
            numbered_matches = re.findall(r'\d+\.\s*Response [A-Z]', ranking_section)
            if numbered_matches:
                # Extract just the "Response X" part
                return [re.search(r'Response [A-Z]', m).group() for m in numbered_matches]

            # Fallback: Extract all "Response X" patterns in order
            matches = re.findall(r'Response [A-Z]', ranking_section)
            return matches

    # Fallback: try to find any "Response X" patterns in order
    matches = re.findall(r'Response [A-Z]', ranking_text)
    return matches


def calculate_aggregate_rankings(
    stage2_results: List[Dict[str, Any]],
    label_to_model: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Calculate aggregate rankings across all models.

    Args:
        stage2_results: Rankings from each model
        label_to_model: Mapping from anonymous labels to model names

    Returns:
        List of dicts with model name and average rank, sorted best to worst
    """
    from collections import defaultdict

    # Track positions for each model
    model_positions = defaultdict(list)

    for ranking in stage2_results:
        ranking_text = ranking['ranking']

        # Parse the ranking from the structured format
        parsed_ranking = parse_ranking_from_text(ranking_text)

        for position, label in enumerate(parsed_ranking, start=1):
            if label in label_to_model:
                model_name = label_to_model[label]
                model_positions[model_name].append(position)

    # Calculate average position for each model
    aggregate = []
    for model, positions in model_positions.items():
        if positions:
            avg_rank = sum(positions) / len(positions)
            aggregate.append({
                "model": model,
                "average_rank": round(avg_rank, 2),
                "rankings_count": len(positions)
            })

    # Sort by average rank (lower is better)
    aggregate.sort(key=lambda x: x['average_rank'])

    return aggregate


async def generate_conversation_title(user_query: str) -> str:
    """
    Generate a short title for a conversation based on the first user message.

    Args:
        user_query: The first user message

    Returns:
        A short title (3-5 words)
    """
    title_prompt = f"""Generate a very short title (3-5 words maximum) that summarizes the following question.
The title should be concise and descriptive. Do not use quotes or punctuation in the title.

Question: {user_query}

Title:"""

    messages = [{"role": "user", "content": title_prompt}]

    # Use gemini-2.5-flash for title generation (fast and cheap)
    response = await query_model("google/gemini-2.5-flash", messages, timeout=30.0)

    if response is None:
        # Fallback to a generic title
        return "New Conversation"

    title = response.get('content', 'New Conversation').strip()

    # Clean up the title - remove quotes, limit length
    title = title.strip('"\'')

    # Truncate if too long
    if len(title) > 50:
        title = title[:47] + "..."

    return title


async def run_full_council(user_query: str) -> Tuple[List, List, Dict, Dict]:
    """
    Run the complete 3-stage council process.

    Args:
        user_query: The user's question

    Returns:
        Tuple of (stage1_results, stage2_results, stage3_result, metadata)
    """
    # Stage 1: Collect individual responses
    stage1_results = await stage1_collect_responses(user_query)

    # If no models responded successfully, return error
    if not stage1_results:
        return [], [], {
            "model": "error",
            "response": "All models failed to respond. Please try again."
        }, {}

    # Stage 2: Collect rankings
    stage2_results, label_to_model = await stage2_collect_rankings(user_query, stage1_results)

    # Calculate aggregate rankings
    aggregate_rankings = calculate_aggregate_rankings(stage2_results, label_to_model)

    # Stage 3: Synthesize final answer
    stage3_result = await stage3_synthesize_final(
        user_query,
        stage1_results,
        stage2_results
    )

    # Prepare metadata
    metadata = {
        "label_to_model": label_to_model,
        "aggregate_rankings": aggregate_rankings
    }

    return stage1_results, stage2_results, stage3_result, metadata

async def run_quality_gate(
    project: str,
    security_mode: str,
    user_prompt: str,
    draft_output: str,
    evidence: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run a specialized 3-stage deliberation for quality/security gating.
    """
    # Stage 1: Individual Evaluations
    eval_prompt = f"""You are a Quality Gate Auditor for the project: {project}.
Security Mode: {security_mode}

User Prompt: {user_prompt}
Draft Output: {draft_output}
Evidence: {json.dumps(evidence)}

Evaluate the draft output against the user prompt and provided evidence.
Identify any security risks, inaccuracies, or missing requirements.
Determine if the output should pass the quality gate.

Your evaluation MUST conclude with:
GATE_DECISION: PASS/FAIL
ISSUES: (list of issues or 'None')
FIXES: (list of required fixes or 'None')
"""
    
    # Reuse stage1 logic but with custom prompt
    eval_messages = [{"role": "user", "content": eval_prompt}]
    eval_responses = await query_models_parallel(COUNCIL_MODELS, eval_messages)
    
    stage1_results = []
    for model, response in eval_responses.items():
        if response is not None:
            stage1_results.append({
                "model": model,
                "response": response.get('content', '')
            })

    # Stage 2: Peer Review of Evaluations
    # Anonymize
    labels = [chr(65 + i) for i in range(len(stage1_results))]
    label_to_model = {f"Evaluator {label}": r['model'] for label, r in zip(labels, stage1_results)}
    
    evals_text = "\n\n".join([f"Evaluator {label}:\n{r['response']}" for label, r in zip(labels, stage1_results)])
    
    ranking_prompt = f"""You are peer-reviewing evaluations for a Quality Gate.
Project: {project}, Security Mode: {security_mode}
Original Prompt: {user_prompt}
Draft Output: {draft_output}

Evaluations from different auditors:
{evals_text}

Analyze which evaluations are most thorough and accurate.
At the end, provide a final ranking of the evaluations.

FINAL RANKING:
1. Evaluator X
2. Evaluator Y
...
"""
    
    peer_responses = await query_models_parallel(COUNCIL_MODELS, [{"role": "user", "content": ranking_prompt}])
    stage2_results = []
    for model, response in peer_responses.items():
        if response is not None:
            full_text = response.get('content', '')
            stage2_results.append({
                "model": model,
                "ranking": full_text
            })

    # Stage 3: Chairman Synthesis
    stage1_text = "\n\n".join([f"Model: {r['model']}\nEvaluation: {r['response']}" for r in stage1_results])
    stage2_text = "\n\n".join([f"Model: {r['model']}\nPeer Review: {r['ranking']}" for r in stage2_results])
    
    chairman_prompt = f"""You are the Lead Auditor (Chairman). You must synthesize the council's evaluations and peer reviews into a final Quality Gate decision.

Project: {project}
Security Mode: {security_mode}
User Prompt: {user_prompt}
Draft Output: {draft_output}

STAGE 1 - Auditor Evaluations:
{stage1_text}

STAGE 2 - Peer Reviews:
{stage2_text}

Provide the final synthesis in a STRICT JSON format.
Example Output:
{{
  "gate_passed": true/false,
  "final_synthesis": "Overall reasoning...",
  "issues_found": ["issue1", "issue2"],
  "required_fixes": ["fix1", "fix2"],
  "consensus_scores": {{ "model_a": score, ... }}
}}
"""
    
    final_response = await query_model(CHAIRMAN_MODEL, [{"role": "user", "content": chairman_prompt}])
    
    import re
    
    raw_content = final_response.get('content', '{}') if final_response else '{}'
    
    # Try to extract JSON from the chairman's response
    try:
        # Look for code blocks first
        json_match = re.search(r'```json\n(.*?)\n```', raw_content, re.DOTALL)
        if json_match:
            final_json = json.loads(json_match.group(1))
        else:
            final_json = json.loads(raw_content)
    except:
        # Fallback parsing
        final_json = {
            "gate_passed": "GATE_DECISION: PASS" in raw_content or '"gate_passed": true' in raw_content.lower(),
            "final_synthesis": raw_content,
            "issues_found": [],
            "required_fixes": [],
            "consensus_scores": {}
        }

    # Add deliberation history
    final_json["deliberation_history"] = {
        "stage1": stage1_results,
        "stage2": stage2_results
    }
    
    return final_json
