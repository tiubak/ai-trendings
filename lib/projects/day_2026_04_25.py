"""TurboQuant Memory Magic Lab — Turn your own mini-model into a “memory magician” by simulating what a TurboQuant-style efficiency breakthrough would do and generating a personalized optimization plan."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an AI performance-coach and stand-up comedian. Create an engaging interactive educational response about {topic} (TurboQuant-like memory-efficient quantization) for a user who inputs their own details. Use the creative framework: \u201cThe Museum of Bytes.\u201d\n\nStep 1: Ask the user for three inputs (but keep them as placeholders in your output): model_size_hint, batch_size_hint, and target_hardware (e.g., laptop GPU/CPU/server).\n\nStep 2: Produce a \u201cByte Tour\u201d that analogizes memory overhead as a cluttered museum storage room; explain how TurboQuant reduces that clutter.\n\nStep 3: Generate a personalized mini-plan with exactly 4 sections:\n1) \u201cWhere the RAM is hiding\u201d (identify likely memory hotspots in plain language)\n2) \u201cQuantization spellbook\u201d (propose 2-3 quantization/precision strategies consistent with memory reduction themes)\n3) \u201cSanity checks\u201d (3 quick checks to avoid quality collapse; be witty)\n4) \u201cTurbo upgrade path\u201d (a step-by-step order to try changes)\n\nStep 4: Include a short \u201cmyth-busting\u201d moment: one common misconception about quantization and memory, and then a corrected version.\n\nOutput must be JSON with keys: byte_tour (string), personalized_mini_plan (object with the 4 sections as strings), myth_bust (object with myth and correction), and questions (array of strings).",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the exploration with a hands-on follow-up. The user\u2019s previous answers are {user_input}. Generate a JSON response that includes:\n\n1) \u201cWhat-if Lab\u201d: provide 3 what-if scenarios that vary batch_size_hint and target_hardware constraints; each scenario must include an estimated directionality label for memory usage (e.g., decreases/moderate/unknown but justify) and a likely quality risk (low/medium/high) using short reasoning.\n2) \u201cDesign a test\u201d: propose a tiny evaluation protocol (exactly 5 steps) to compare baseline vs TurboQuant-like approach.\n3) \u201cCoach\u2019s one-liner\u201d: a single sentence guiding principle tailored to {user_input}.\n\nImportant: Output ONLY valid JSON with keys: what_if_lab (array of 3 objects with scenario, memory_direction, quality_risk, justification), test_protocol (array of 5 strings), coach_one_liner (string).",
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
    "name": "TurboQuant Memory Magic Lab",
    "description": "Turn your own mini-model into a “memory magician” by simulating what a TurboQuant-style efficiency breakthrough would do and generating a personalized optimization plan.",
    "category": "AI Education",
    "date": "2026-04-25"
}
