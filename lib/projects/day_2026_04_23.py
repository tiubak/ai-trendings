"""Underwater AI Sworn Navigators — Train a tiny “mission brief” generator that pairs an autonomous underwater vehicle (AUV) with a diver using AI coordination principles and produces a personalized checklist and strategy."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are designing an interactive educator for an AI portfolio project. Create a personalized, story-driven \u201cmission briefing\u201d for {topic} focused on collaboration between a human diver and an autonomous underwater vehicle (AUV). Use a playful framework: the diver is the \u201cCaptain,\u201d the AUV is the \u201cNavigator,\u201d and the AI is the \u201cInterpreter of Bubbles.\u201d\n\nUser provides: {user_input}. From it, generate:\n1) A short myth-like scene (2-4 sentences) that describes the scenario using surprising metaphors (e.g., submarine as a nightclub with spotlights; sensors as gossiping pigeons).\n2) A roles-and-protocol table with 4 rows: Diver actions, AUV actions, AI coordination signals, and Safety override trigger\u2014each row must be 1-2 lines and include at least one measurable example (distance, time window, confidence score, battery budget, or comms latency).\n3) A \u201c3-layer plan\u201d called: Sense \u2192 Negotiate \u2192 Act. Each layer must include: what inputs are used, what outputs are produced, and a \u201cwhat could go wrong\u201d bullet.\n4) A compact checklist the user can follow before the mission (5 items max).\n5) A playful final twist: one unlikely but useful lesson learned (e.g., why \u201cslow blinking\u201d beats rapid toggling) tied back to the coordination problem.\n\nConstraints:\n- Avoid generic textbook phrasing; make it memorable and specific.\n- Include at least one analogy and one humorous line.\n- Output must be valid JSON with keys: \"scene\", \"protocol_table\", \"three_layer_plan\", \"checklist\", \"twist\", \"assumptions\".\n- \"protocol_table\" should be an array of objects with keys: diver, auv, ai_signals, safety_override.\n- \"three_layer_plan\" should be an array of objects with keys: layer, inputs, outputs, what_could_go_wrong.\n- \"assumptions\" should be an array of strings derived from {user_input} (e.g., comms quality, depth range, sensor availability).\n\nThink outside the box: treat the coordination as a conversation with rules, not a one-time command.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the exploration of the same scenario by generating a JSON \u201cdebugger\u201d for {user_input}. Ask the AI to behave like a QA engineer and safety officer.\n\nInput: {user_input}\nOutput JSON must include:\n1) \"assumption_challenges\": array of 3 questions that could falsify the mission plan (e.g., what if the diver\u2019s visibility drops, what if comms delay increases).\n2) \"failure_catalog\": array of 4 failure modes. Each failure mode object must have keys: name, likely_cause, detection_signal, mitigation_step, severity (1-5).\n3) \"training_prompts\": array of 3 micro-experiments the user can run conceptually (no external tools needed). Each object must include: goal, what_to_vary, expected_effect.\n4) \"coordination_policy_nugget\": one concise rule-of-thumb that links uncertainty to action (must reference both human and AUV perspectives).\n5) \"short_answer_question\": a single question to ask the user that would improve personalization next run.\n\nRules:\n- Keep everything tied to collaboration between diver and AUV and to AI/ML coordination concepts.\n- Be concrete (mention at least one measurable signal or timing condition per failure mode).\n- Output must be valid JSON only.",
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
    "name": "Underwater AI Sworn Navigators",
    "description": "Train a tiny “mission brief” generator that pairs an autonomous underwater vehicle (AUV) with a diver using AI coordination principles and produces a personalized checklist and strategy.",
    "category": "AI Education",
    "date": "2026-04-23"
}
