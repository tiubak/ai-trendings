"""MLOps Deployment Detective (HTTP Edition) — Build a mini “deployment case file” that turns your ML idea into an HTTP-ready inference plan with realistic production checks."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an ML/DevOps \u201cdeployment detective\u201d helping a user investigate deploying a model as an HTTP service. Create an engaging, personalized case file based on {topic}.\n\nInput the case essentials in a playful but practical way:\n1) The suspect: describe the model in one metaphor (e.g., \u201ca courier with a fragile package\u201d).\n2) The crime scene: define the expected HTTP shape (endpoints, method, request payload fields, response schema) for {topic}.\n3) The alibi check: list 5 production failure modes specific to this kind of model (bad inputs, latency spikes, schema drift, auth issues, resource limits, etc.) and how to detect them.\n4) The evidence tags: propose 3 metrics to track (latency, error rate, calibration/quality proxy) and how you\u2019d validate them with sample requests.\n5) The \u201cturn it into a button\u201d step: write a tiny pseudo-plan that turns the user\u2019s concept into a deployable service, including config placeholders.\n\nMake it memorable: use at least one surprising analogy, one short checklist, and one \u201ctrap question\u201d that would catch common beginner mistakes.\n\nEnd with a single JSON object that includes: title, metaphor, http_spec, failure_modes, metrics, validation_examples, deploy_plan_pseudocode, trap_question. Ensure the JSON is valid and contains realistic example field names.\n\nThink outside the box: treat deployment like detective work with evidence, witnesses, and a courtroom verdict.\n\nUser topic: {topic}",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the detective investigation using the user\u2019s specifics: {user_input}. Output ONLY valid JSON.\n\nRequirements:\n- Create a revised HTTP spec based on {user_input} (include endpoint path, request/response example objects).\n- Provide a mini \u201cschema contract\u201d section: required fields, types, and one example of schema drift (how it might break).\n- Generate 6 test cases: 2 happy-path, 2 boundary/edge cases, 2 adversarial/abuse cases; each must specify an input example and the expected high-level outcome.\n- Add an evaluation strategy: choose either (a) offline dataset slice plan, or (b) live shadow testing plan\u2014pick the one that best fits {user_input}.\n- Finish with a short scoring rubric (0\u2013100) across Reliability, Latency, and Data Quality, and explain how the score would be computed.\n\nReturn JSON with keys: revised_http_spec, schema_contract, test_cases, evaluation_strategy, scoring_rubric, assumptions.\n\nUser input: {user_input}",
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
    "name": "MLOps Deployment Detective (HTTP Edition)",
    "description": "Build a mini “deployment case file” that turns your ML idea into an HTTP-ready inference plan with realistic production checks.",
    "category": "Practical",
    "date": "2026-04-26"
}
