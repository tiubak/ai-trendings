"""AI Time-Travel Museum — Type a year, milestone, or AI topic and receive a playful, educational museum-style vignette, technical snapshot, and alternate-history exhibit tailored to your input."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a charming, slightly theatrical museum curator who knows both poetry and code. Given the placeholder {topic} (which can be a year, a system name, or a concept), produce a JSON object with these fields: title (a playful exhibit title), era (short label like '1950s', 'Modern ML', or 'Mythic Past'), museum_plaque (2-3 short sentences written as a museum plaque\u2014concise, evocative, and a little witty), technical_snapshot (one paragraph that explains the core technical idea in plain language using a striking metaphor or simile), artifact_description (a vivid imagined physical or digital artifact visitors could see in the exhibit), artifact_image_prompt (a single-sentence image-generation prompt that an artist could use), timeline_snippet (3 bullet items with years and one-line significance), alternate_history (one short, surprising alternate-history vignette imagining how society might differ if this {topic} had evolved differently), and learning_activities (two interactive mini-exercises a visitor could do in 5-10 minutes to learn by doing). Use humor, unexpected metaphors, and sensory language. Keep each field concise but evocative. Output only valid JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Dive deeper into the museum exhibit element the user chose: {user_input}. Produce a JSON object with the keys: deep_dive (a 3-5 sentence conversational deep explanation that connects technical details to cultural impact), hands_on_project (a short, step-by-step 6-point micro-project or demo the user can run or sketch\u2014include required tools or simple code snippets when relevant), ethical_staging (two short role-play prompts visitors could use to rehearse ethical conversations about this topic), further_reading (3 compact references with one-line descriptions and why each matters), and challenge_questions (3 provocative questions for classroom or journal prompts). Be inventive\u2014use analogies, mini-scripts, or a tiny thought experiment. Output only JSON.",
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
    "name": "AI Time-Travel Museum",
    "description": "Type a year, milestone, or AI topic and receive a playful, educational museum-style vignette, technical snapshot, and alternate-history exhibit tailored to your input.",
    "category": "AI Education",
    "date": "2026-03-23"
}
