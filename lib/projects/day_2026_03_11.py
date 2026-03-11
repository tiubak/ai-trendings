"""Model Release Lab — Interactively generate playful, practical debriefs and bespoke evaluation plans for any newly released AI model."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a theatrical tech critic and forensic scientist for AI models. Imagine {model_name} is making its debut on a neon-lit stage \u2014 write a concise, witty, and practical JSON 'debrief' that a curious engineer, product manager, or student could use immediately. Include these keys exactly: \"headline\" (one catchy sentence), \"elevator_pitch\" (one tight paragraph describing what this model is best at and who should care), \"signature_strengths\" (array of 3 concrete capabilities with one-line examples), \"surprising_analogy\" (one sentence comparing the model to an unexpected thing, e.g., \"like a librarian who also DJs\"), \"three_quirky_tests\" (array of 3 copy-paste prompts to poke for hallucination, reasoning, and style drift), \"failure_modes\" (array of 3 likely weaknesses with short mitigation tips), \"cost_and_context_tradeoff\" (one paragraph comparing latency, token cost, and context window tradeoffs), \"press_snippet\" (a playful one-paragraph mock press release), and \"suggested_visual\" (one-line idea for a simple chart or visual to showcase performance). Use humorous metaphors, concrete examples, and give ready-to-run prompts. Output only valid JSON\u2014no extra commentary.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the user input {user_input} (a model name, or a debrief attribute from the previous output) and produce a deeper JSON 'evaluation_package' that a small team could execute in one afternoon. Include these keys exactly: \"evaluation_plan\" (an ordered array of 5 hands-on steps, each with a short goal and an expected metric), \"probe_suite\" (array of 10 prompt templates to run against the model with one-line notes on what each probe reveals), \"scoring_rubric\" (an object mapping 4 categories like accuracy, robustness, factuality, cost to numeric scoring guidance and pass/fail thresholds), \"quick_bench_command\" (one example curl or pseudocode snippet showing a latency + cost measurement call), \"ethics_checklist\" (array of 6 short items to verify before launch), \"vendor_questions\" (array of 6 sharp questions to ask the model provider about training data, evals, and alignment), and \"visualization_specs\" (array of 3 visualization descriptions: chart type, x/y axes, and what insight it highlights). Be concrete, use a playful tone, and return only JSON.",
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
    "name": "Model Release Lab",
    "description": "Interactively generate playful, practical debriefs and bespoke evaluation plans for any newly released AI model.",
    "category": "AI Education",
    "date": "2026-03-11"
}
