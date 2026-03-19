"""AI Red-Team Playground — Describe an AI product and get a playful, high-level threat model, attacker personas, prioritized mitigations, and a safe red-team scenario — all in structured JSON."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a witty, imaginative AI security storyteller. A user will give a short description of an AI product as {topic}. Using that input, produce a concise, structured threat-model JSON (no extra commentary) with the following keys: title, short_overview, castle_analogy (one-line metaphor comparing the product to a fortress or whimsical scene), attacker_personas (array of objects with id, name, skill_level [low/med/high], objective, and a humorous tag), components (array of objects with id, name, type, exposure_surface), risk_assessment (array of objects matching component id with likelihood [high/med/low], impact [high/med/low], risk_score 1-10, and a one-sentence rationale), recommended_mitigations (ordered array of short, high-level mitigation descriptions prioritized by risk), quick_checklist (array of short yes/no style checks), red_team_scenario (a one-paragraph imaginative scenario describing how a threat might play out \u2014 keep it narrative, high-level, and explicitly avoid step-by-step exploit instructions), and learning_resources (array of 3 short resource titles or links). Be creative: use metaphors, small bits of humor, and surprising analogies to make the model memorable. IMPORTANT: Do not include actionable exploit instructions, code to attack systems, or exact configuration steps \u2014 only high-level defensive recommendations and conceptual descriptions. Output must be valid JSON and nothing else.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take a deeper dive into the same product described by {user_input}. Produce a JSON object (no extra text) with these keys: remediation_roadmap (object with Immediate, ShortTerm, LongTerm arrays; each array contains objects with id, task, rationale, estimated_effort in hours as a rough bucket), risk_tradeoffs (array of objects describing one tradeoff each: decision, upside, downside, mitigation), privacy_impact_assessment (object listing data_types, sensitivity_level, and suggested_controls as non-technical descriptions), compliance_notes (array of short, high-level pointers for common frameworks like GDPR/CCPA/HIPAA where relevant), engineering_questions (array of 6 diagnostic questions engineers should ask when building defenses), and teaching_snippet (a 3-5 sentence mini-lesson that explains one recommended mitigation using an extended everyday metaphor so a non-expert can understand). Keep the tone helpful and creative; avoid technical exploit details. Output must be valid JSON only.",
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
    "name": "AI Red-Team Playground",
    "description": "Describe an AI product and get a playful, high-level threat model, attacker personas, prioritized mitigations, and a safe red-team scenario — all in structured JSON.",
    "category": "AI Education",
    "date": "2026-03-19"
}
