"""AI Race Scenario Studio — Enter a company, sector, or policy and get a vivid near-term scenario of how a major AI breakthrough (e.g., GPT-5.4) could reshape it, plus a tactical playbook and risk score."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AI strategic writer tasked with turning the headline 'GPT-5.4 breakthrough + rising AI tensions' into a compact, memorable briefing about {topic}. Think like a meteorologist who forecasts not weather but technological storms \u2014 use vivid metaphors, a touch of humor, and surprising analogies (for example: 'like a neighborhood suddenly getting a lighthouse, then a helicopter, then a border checkpoint'). Produce a single JSON object (no extra commentary) with the following fields: \n\n- title: short, catchy one-liner summary (string)\n- one_paragraph_scenario: a creative, concrete 3-4 sentence narrative that shows a plausible near-term outcome for {topic} after a major AI breakthrough (string)\n- key_drivers: array of 3 concise drivers that push this scenario (array of strings)\n- primary_risks: array of 3 concise risks with one-sentence explanations (array of objects {\"risk\":\"\",\"impact\":\"\"})\n- 90_day_playbook: an ordered array of 5 tactical steps (each step is an object {\"step\":\"\",\"why\":\"\",\"who_to_involve\":\"\"}) aimed at practitioners in {topic}\n- risk_score: integer 0-100 assessing systemic disruption risk (higher means more urgent)\n- surprising_opportunities: array of 3 creative, non-obvious opportunities (array of strings)\n- quick_talking_points: array of 3 short comms lines tailored to executives, engineers, and regulators respectively (array of strings)\n\nBe original and avoid generic platitudes; use one clever metaphor in the one_paragraph_scenario. Remember the JSON schema exactly and output valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the earlier briefing for {user_input} and produce a deeper, structured exploration as JSON. Create three distinct near-term futures (give each a concise name) that could plausibly unfold in the next 12 months given accelerating model capabilities and geopolitical/market pressures. For each future include: {\"name\":\"\",\"description\":\"\",\"likelihood_percent\":number (0-100),\"leading_indicators\": [list of 4 observable signals],\"near_term_triggers\": [list of 3 events that would push this future into reality],\"recommended_actions\": [4 prioritized actions with an estimated time-to-impact],\"communications_snippets\": {\"exec\":\"\",\"engineer\":\"\",\"policy\":\"\"}}. Also include an overall recommended contingency: {\"trigger_thresholds\": [3 measurable thresholds], \"urgent_first_steps\": [3 actions]}. Output valid JSON only and avoid extra commentary.",
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
    "name": "AI Race Scenario Studio",
    "description": "Enter a company, sector, or policy and get a vivid near-term scenario of how a major AI breakthrough (e.g., GPT-5.4) could reshape it, plus a tactical playbook and risk score.",
    "category": "AI Education",
    "date": "2026-03-10"
}
