"""LLM Evolutionarium — Type a model name, release year, or brief release note and get a playful, data-driven 'evolution report' that explains what changed, why it matters, and how to adapt."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a time-traveling release biologist cataloging a newly discovered AI model species. Given the input {topic}, produce a single JSON object with these keys: title, one_sentence_summary, evolution_tree, spec_highlights, benchmark_implications, api_changes, migration_checklist, recommended_use_cases, ethical_considerations, creative_analogy, visual_ascii_timeline, mini_quiz. evolution_tree should be an array of 3-5 objects each with name, release_date, and short_trait. spec_highlights should include params, compute_profile, and modalities. migration_checklist should be an ordered list of practical steps with a short 'why' for each. Use witty metaphors, surprising examples (like comparing token behavior to bakery ingredients), and at least one humorous contrast between old and new models. Keep fields concise and focused on actionable insight. Output must be valid JSON and contain only the described object.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deep dive on {user_input}. Interpret this as either a model name/version, a migration pair (like 'GPT-4 -> GPT-5.4'), or a specific release note. Return a JSON object with fields: deep_dive (detailed paragraph explaining architecture shifts, likely error modes, and real-world implications), step_by_step_migration (array of numbered steps each with explanation and 'risk level'), sample_code_snippet (python snippet using placeholders {API_KEY} and {MODEL_NAME} demonstrating batching, streaming, and retry strategies), performance_estimates (table-like JSON with latency and cost tradeoffs for small/medium/large payloads), validation_tests (list of unit and behavioral tests to run), fallback_strategy (how to degrade gracefully), and references (short list of URLs or citations). Use concrete, actionable language and include tiny realistic code snippets. Output only the JSON object.",
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
    "name": "LLM Evolutionarium",
    "description": "Type a model name, release year, or brief release note and get a playful, data-driven 'evolution report' that explains what changed, why it matters, and how to adapt.",
    "category": "AI Education",
    "date": "2026-03-16"
}
