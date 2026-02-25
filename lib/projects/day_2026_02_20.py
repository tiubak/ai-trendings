"""AI Model Showdown — Compare AI models side-by-side with real specs — context windows, cost, benchmarks, and open-source status from our database of 13+ models"""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You have access to this AI model data (JSON). Analyze it and create an interesting comparison. Pick the 3 best value-for-money models and the 3 most powerful models. Explain trade-offs. Data: {db_models}. Format as JSON: {best_value (array of {name, why}), most_powerful (array of {name, why}), surprise_findings (array), advice_for_developers}.",
        "parse": "json",
        "db_query": "SELECT * FROM models ORDER BY mmlu_score DESC"
    },
    "compare": {
        "prompt": "Compare these specific AI models in detail: {models_to_compare}. Use this data: {db_models}. Cover: performance, cost, context window, open-source availability, best use cases. Format as JSON: {models (array of {name, verdict}), winner_by_category (object), recommendation}.",
        "parse": "json",
        "db_query": "SELECT * FROM models"
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
    "name": "AI Model Showdown",
    "description": "Compare AI models side-by-side with real specs — context windows, cost, benchmarks, and open-source status from our database of 13+ models",
    "category": "AI Education",
    "date": "2026-02-20"
}
