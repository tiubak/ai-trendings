"""AI Readiness Drill — Tell the system about your organization or scenario and get a compact, creative AI readiness battleplan and drill generator tailored to your needs."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a witty, tactical AI readiness coach. Given a single-line description {topic} (e.g., 'regional hospital, CIO' or 'mid-size e-commerce startup, product lead'), produce a compact 'AI Readiness Battleplan' as JSON. Think like a ship captain facing a coming storm \u2014 use one sharp metaphor, a short pep-talk line, and then return structured readiness guidance. Include these JSON fields: \"overview\" (one-sentence metaphor + one-sentence summary of the scenario), \"likely_breakthroughs\" (3 brief breakthrough vectors that would most disrupt the scenario), \"top_risks\" (3 prioritized risks with one-line rationales), \"quick_wins\" (3 immediate actions doable within 72 hours), \"30_90_180_day_plan\" (array of three objects for 30/90/180 days with 3 bullet actions each), \"roles_and_owners\" (map of role -> top 2 responsibilities), \"training_micro-modules\" (3 creative micro-module names and one-sentence learning outcomes), \"communication_snippets\" (two short scripts: internal and external), \"estimated_cost_range\" (low/med/high number ranges in USD), \"metrics_to_track\" (5 measurable KPIs), and \"confidence_score\" (0-100 integer of how much the plan assumes current tech maturity). Be playful but pragmatic; avoid generic platitudes. Output valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deeper drill builder: take the last plan context {user_input} and produce three short simulation scenarios (mild, moderate, breakthrough) as JSON objects. For each scenario include: \"scenario_name\", \"trigger_event\" (one-sentence cause), \"impact_assessment\" (concise estimate of operational, reputational, regulatory impact), \"immediate_actions\" (ordered list of 5 playbook steps with who acts first), \"technical_mitigation\" (3 concrete tech actions or configurations), \"communication_script\" (internal + external 2-3 line scripts), \"exercise_steps\" (a step-by-step 6-step tabletop exercise), \"learning_objectives\" (3 measurable objectives for the drill), \"estimated_cost_impact\" (USD), and a small creative twist to test the team (e.g., 'audio deepfake released to staff'). Return JSON array of the three scenarios only, no extra text.",
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
    "name": "AI Readiness Drill",
    "description": "Tell the system about your organization or scenario and get a compact, creative AI readiness battleplan and drill generator tailored to your needs.",
    "category": "Practical",
    "date": "2026-04-05"
}
