"""Release Orchestra: Model Playback & Briefings — Type a model, vendor, or release trend and get a playful, teachable 'release briefing' plus a deeper comparative analysis you can use in lessons or demos."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an eccentric technology archivist and theatrical science teacher. Given the topic {topic} (this could be a model name, vendor announcement, benchmark report, or general release trend), produce a compact, creative 'Release Brief' as a JSON object that educators and curious engineers can use immediately. Think of the release as an instrument in an orchestra: describe its sound, rhythm, and where it sits in the ensemble. Use humor, surprising analogies, and one memorable metaphor that ties technical tradeoffs to a real-world scene. Produce the following JSON fields: \"headline\" (one catchy title), \"one_liner\" (one sentence summary), \"metaphor\" (single vivid metaphor), \"three_quick_facts\" (array of 3 bullet facts about impact, novelty, or risk), \"mini_timeline\" (array of up to 3 timeline items: {\"date\",\"event\",\"why_it_matters\"}), \"tech_snapshot\" (object with keys: \"approx_scale\",\"latency_profile\",\"on_device_feasibility\",\"cost_tier\",\"best_use_cases\" \u2014 keep values short), \"classroom_activity\" (one interactive 5\u201310 minute activity teachers can run with students), and \"quiz\" (array of 2 multiple-choice questions with choices and the correct answer). Keep entries concise, witty, and practical. Output valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the user's selection {user_input} and run a short investigative comparison against three representative contemporaries (choose sensible peers from recent trending models). Return a JSON object with: \"comparisons\" (array of 3 objects each containing: \"name\",\"release_date\",\"estimated_params_or_scale\",\"strengths\" (3 short bullets),\"weaknesses\" (2 short bullets),\"best_fit_scenarios\"), \"visualization_points\" (array of timeline datapoints suitable for plotting: {\"label\",\"x_date\",\"y_metric_priority\" where y_metric_priority is a simple tag like 'latency','accuracy','on_device'}), \"presentation_slides\" (array of 5 slide titles + one-sentence speaker note each), and \"mini_lab\" (3-step hands-on lab instructions to compare inference latency or cost between two choices using simple commands or pseudo-APIs). Use vivid analogies and two concise risk/ethics pointers at the end. Output valid JSON only.",
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
    "name": "Release Orchestra: Model Playback & Briefings",
    "description": "Type a model, vendor, or release trend and get a playful, teachable 'release briefing' plus a deeper comparative analysis you can use in lessons or demos.",
    "category": "AI Education",
    "date": "2026-03-31"
}
