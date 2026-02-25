"""AI Training Cost Calculator — Estimate how much it costs to train AI models — from GPT-scale to small fine-tunes — covering GPU hours, electricity, and carbon footprint"""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Explain AI training costs in simple terms. Include: cost breakdown for training a large model (GPUs, electricity, cooling, engineering), comparison of training costs for GPT-4 (~$100M), Llama 3 (~$30M), and a small fine-tune (~$100). Include carbon footprint data. Format as JSON: {overview, cost_breakdown (array of {component, percentage, description}), model_comparisons (array of {model, estimated_cost, gpu_hours, parameters, year}), carbon_impact, fun_facts (array)}.",
        "parse": "json"
    },
    "estimate": {
        "prompt": "Estimate the training cost for a model with these specs: {parameters} parameters, trained on {tokens} tokens, using {gpu_type} GPUs. Calculate approximate: GPU hours, electricity cost, total cost, and CO2 emissions. Format as JSON: {specs, estimated_gpu_hours, electricity_kwh, cost_usd, co2_kg, comparison (e.g. 'equivalent to X car trips'), tips_to_reduce_cost (array)}.",
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
    "name": "AI Training Cost Calculator",
    "description": "Estimate how much it costs to train AI models — from GPT-scale to small fine-tunes — covering GPU hours, electricity, and carbon footprint",
    "category": "AI Education",
    "date": "2026-02-17"
}
