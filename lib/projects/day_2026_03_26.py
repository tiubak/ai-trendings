"""On-Device vs Cloud AI Playground — Describe an app or dataset and get a playful, personalized analysis and deployment plan recommending on-device, cloud, or hybrid execution with privacy, latency, and energy tradeoffs."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a playful, expert AI deployment guide \u2014 part carnival barker, part systems engineer. Given the user topic {topic}, produce a single JSON object (no extra text) with these keys: \n- microstory: a 2-sentence, imaginative analogy that compares running the model on-device vs in the cloud for this scenario (use humor or surprise). \n- recommendation: one of \"on-device\", \"cloud\", or \"hybrid\". \n- rationale: 1-2 sentences (clear, slightly witty) explaining the choice. \n- privacy_score: integer 0-10 estimating sensitivity (10 = highest privacy concern). \n- pros: array of up to 5 short pros for the recommended option. \n- cons: array of up to 5 short cons. \n- quick_deploy_steps: array of 3-5 concrete, ordered steps to try a minimal prototype. \n- tiny_code_snippet: a 2-6 line pseudocode snippet showing the minimal data flow labeled \"local\" or \"remote\".\nKeep each field concise (<=300 chars). Use vivid metaphors, surprising examples, and a dash of humor. Return valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Dive deeper on this deployment scenario: {user_input}. Reply with a JSON object only that contains: \n- architecture: an outline mapping components to \"on-device\"/\"edge\"/\"cloud\" with 3-6 components. \n- latency_ms: realistic expected latency range as \"min-max ms\" for interactive use. \n- bandwidth_kbps: estimated average bandwidth per user (low/med/high with numeric range). \n- model_suggestions: list of 2-3 model types/sizes (e.g., 20M quantized, 1B sparse) and whether they fit on modern phones. \n- privacy_measures: ordered list of practical measures (e.g., encrypt-at-rest, client-side aggregation, DP) with 1-line rationale each. \n- fallback_policy: a short JSON describing when to fall back to server (conditions and reason). \n- cost_estimate: quick monthly cost band (free/minimal/moderate/high) with a short justification. \n- migration_steps: 4 short milestones to move from prototype to production.\nBe concrete and inventive \u2014 use a metaphor for the architecture if helpful. Return JSON only.",
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
    "name": "On-Device vs Cloud AI Playground",
    "description": "Describe an app or dataset and get a playful, personalized analysis and deployment plan recommending on-device, cloud, or hybrid execution with privacy, latency, and energy tradeoffs.",
    "category": "AI Education",
    "date": "2026-03-26"
}
