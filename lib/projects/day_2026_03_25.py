"""Self-Verifier Lab — Design and iterate a playful, implementation-ready self-verification blueprint for an AI agent that performs any user-specified task."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AI systems architect and stage magician who must explain self-verification to engineers and curious humans alike. For an autonomous agent assigned to perform the task: {topic}, craft a playful yet rigorous '3-act' self-verification blueprint named 'Detect, Doubt, Defend'. Produce the following as a single JSON object: {\n  \"title\": short catchy name,\n  \"tagline\": one-sentence marketing-style tag,\n  \"mascot\": one-line quirky mascot description,\n  \"acts\": {\n    \"Detect\": {\"one_line\": \"the theatrical summary\", \"steps\": [\"concrete algorithmic steps an engineer could implement\"], \"unit_tests\": [{\"input\": \"..\", \"expected\": \"..\"}, ...], \"confidence_heuristic\": \"brief rule\"},\n    \"Doubt\": {...},\n    \"Defend\": {...}\n  },\n  \"failure_modes\": [{\"name\": \"..\", \"symptoms\": \"..\", \"mitigation\": \"..\"}, ...],\n  \"manifest\": {\"name\": \"module-name\", \"purpose\": \"short\", \"components\": [\"component names\"], \"estimated_latency_ms\": number, \"sample_prompt\": \"a one-line prompt to call this agent\"}\n}\nUse metaphors, humor, and at least one surprising real-world analogy (e.g., detective novel, baking, or airport security) to make the design memorable. For each act include two concise unit test examples with inputs and expected outputs. Keep outputs concrete and implementation-minded but playful. Return only valid JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the JSON blueprint produced earlier as {user_input} and expand it into an implementation-ready plan. Return a single JSON object with these top-level keys: {\n  \"pseudocode\": {\"Detect\": \"function-level pseudocode\", \"Doubt\": \"...\", \"Defend\": \"...\"},\n  \"harness\": {\"test_harness_code_snippet\": \"pseudo-code showing a minimal runtime that runs a two-step workflow and where verification hooks in\", \"simulation_inputs\": [..]},\n  \"metrics\": {\"definitions\": {\"precision\":\"..\",\"recall\":\"..\",\"rollback_rate\":\"..\"}, \"target_thresholds\": {\"precision\":0.9, \"recall\":0.85}},\n  \"datasets\": [\"suggested real or synthetic datasets, augmentation tricks, and a simple data-generator recipe\"],\n  \"adversarial\": {\"red_team_test\": \"describe an adversarial failure case and step-by-step recovery sequence\"},\n  \"trace\": \"a short (6-10 step) sample execution trace or conversation where the agent detects a mistake, doubts, and defends by correcting it\"\n}\nBe precise and pragmatic: include clear function names, data shapes, and where checks/rollbacks happen. Provide one small code-like pseudocode block per component. Keep a playful voice in low-overhead comments. Return only valid JSON.",
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
    "name": "Self-Verifier Lab",
    "description": "Design and iterate a playful, implementation-ready self-verification blueprint for an AI agent that performs any user-specified task.",
    "category": "AI Education",
    "date": "2026-03-25"
}
