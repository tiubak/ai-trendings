"""AI Release Time‑Machine — Type a model, provider, or AI feature and get a playful, data‑driven timeline, impact analysis, and hands‑on micro‑challenges you can interact with."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a witty AI historian and product designer. Given a {topic} (a model name, model family, provider, or AI feature), produce a compact, imaginative JSON 'time-travel packet' that a web UI can render as a narrated timeline plus actionable learning items. Start with a 2\u20133 sentence hook that uses a surprising metaphor (e.g., 'orchard', 'space race', 'neighborhood gossip'), then output ONLY valid JSON with these top-level keys: \"hook\": string, \"timeline\": array of event objects, \"eli5\": one-sentence explanation for a 10-year-old, \"dev_notes\": array of 3 short technical bullets, \"micro_challenges\": array of 3 interactive tasks. Each timeline event object must contain: \"date\" (ISO-ish string), \"title\" (short), \"short_description\" (1\u20132 sentences using humor or an analogy), \"technical_note\" (concise technical detail or metric), \"change_type\" (one of: \"model\",\"api\",\"pricing\",\"feature\",\"research\",\"ecosystem\"), \"impact_score\" (1\u201310 integer for learner impact), and \"visual_hint\" (one of: \"spark\",\"rising-bar\",\"fork\",\"heartbeat\",\"wave\"). The micro_challenges should be short, specific, and runnable by a learner in 10\u201345 minutes and include required inputs. Use creative framing, unexpected metaphors, and playful tone, but keep technical notes accurate and concise. Provide only the JSON object as output\u2014no extra text.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the JSON timeline or packet from the first step as {user_input} and produce a deeper JSON exploration that contains three alternative future arcs: \"Conservative\", \"Optimistic\", and \"Disruptive\". For each arc include: \"name\", \"projected_window\" (e.g., \"2026\u20132028\"), \"key_events\" (array of 3 event objects with date,title,impact_summary), \"top_risks\" (array of 2 short risks), \"top_opportunities\" (array of 2 short opportunities), and a recommended \"mini_project\" with a 5\u20137 line pseudocode outline and a short list of required APIs/tools. Also include a compact \"viz_instructions\" object that suggests how a frontend could animate the arc (e.g., color, speed, node-style). Keep tone imaginative but keep technical suggestions feasible. Return ONLY valid JSON.",
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
    "name": "AI Release Time‑Machine",
    "description": "Type a model, provider, or AI feature and get a playful, data‑driven timeline, impact analysis, and hands‑on micro‑challenges you can interact with.",
    "category": "AI Education",
    "date": "2026-03-21"
}
