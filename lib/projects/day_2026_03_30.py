"""Self-Verification Agent Lab — Design a multi-step AI agent for any task and get creative, testable self-verification checkpoints, failure modes, and automated recovery plans."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a playful, highly-practical system that helps engineers and learners design robust, self-verifying multi-step agents. Given a task description {topic}, produce a JSON object with the following keys: \n- agent_overview: a 1-2 sentence metaphorical summary (use a surprising analogy or humor). \n- steps: an ordered array of step objects; each step must have id (string), short_description, expected_output_format (one-line schema). Keep 3-8 steps. \n- verification_checkpoints: array of checkpoint objects mapping to step ids; each checkpoint must include checkpoint_id, step_id, verification_prompt (short prompt the agent uses to verify its own or another model's output), acceptance_criteria (clear, testable bullets), and confidence_threshold (number between 0 and 1). Make at least one checkpoint that cross-checks multiple earlier outputs. \n- failure_modes: list up to 6 concise failure modes with one-sentence example for each (e.g., hallucination, format drift, missing facts). \n- confidence_calibration: 2-3 sentences on how to interpret the agent's numeric confidences and when to escalate to human review. \n- test_cases: provide 3 diverse, small test cases (id, input_summary, expected_output_snippet). \n- recovery_strategy: 4-step automated recovery plan the agent should run when a checkpoint fails (include one creative action like 'ask a clarifying micro-question' or 'run a focused re-check with a different model'). \n- human_readable_tip: one clever tip for a developer implementing these checks.\nBe original, use metaphors or humor, and keep the JSON clean and machine-readable. Output only valid JSON (no extra commentary).",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the specific checkpoint or step described in {user_input} and produce a focused JSON response with these fields: \n- checkpoint_id (string)\n- refined_verification_prompt (a short, precise prompt that will be sent to a verifier model; the verifier must return structured JSON)\n- verifier_response_schema (the exact JSON keys the verifier should return, e.g., {\"ok\":boolean,\"errors\":[...],\"confidence\":0.0,\"suggested_corrections\":[...]})\n- simulated_verifier_output (an example run of the verifier as JSON conforming to the schema, showing a non-trivial error and a confidence number)\n- mitigation_plan (3-5 concrete, ordered actions the agent should take if 'ok' is false, including re-generation strategies, minimal clarifying questions, and escalation rules)\n- unit_tests (3 tiny test definitions that check the verifier and mitigation, each with name, input_example, expected_verifier_outcome)\nKeep the tone engaging (use an analogy or a one-line witty note) and keep the JSON strictly valid.",
        "parse": "json"
    }
}

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""
    if action == 'info':
        return {"name": META["name"], "description": META["description"], "actions": list(ACTIONS.keys())}
    
    action_config = ACTIONS.get(action)
    if not action_config:
        return {"error": f"Unknown action: {action}. Available: {list(ACTIONS.keys())}"}
    
    # Build prompt with user data
    prompt = action_config["prompt"]
    for key, value in data.items():
        prompt = prompt.replace("{" + key + "}", str(value))
    
    # Inject database data if action has a db_query
    db_query = action_config.get("db_query")
    if db_query:
        db_rows = query_db(db_query)
        # Replace {db_*} placeholders with JSON data
        for placeholder in ["db_models", "db_timeline", "db_glossary", "db_gpus", "db_datasets", "db_languages"]:
            if "{" + placeholder + "}" in prompt:
                prompt = prompt.replace("{" + placeholder + "}", _json.dumps(db_rows, default=str)[:3000])
    
    # Call AI
    raw = call_openrouter(prompt)
    
    # Parse response
    if action_config.get("parse") == "json":
        parsed = extract_json(raw)
        if parsed:
            return {"result": parsed, "date": META.get("date", "")}
        return {"result": {"text": raw}, "date": META.get("date", ""), "parse_note": "returned as text"}
    
    return {"result": {"text": raw}, "date": META.get("date", "")}

META = {
    "name": "Self-Verification Agent Lab",
    "description": "Design a multi-step AI agent for any task and get creative, testable self-verification checkpoints, failure modes, and automated recovery plans.",
    "category": "AI Education",
    "date": "2026-03-30"
}
