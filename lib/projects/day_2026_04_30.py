"""AI Deployment Economics Brief Builder — Generate a personalized weekly “AI news digest” that translates breakthrough headlines into practical cost, latency, and reliability tradeoffs you can actually plan for."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a witty AI analyst. Create an interactive content generator for {topic}. First, ask the user to imagine they are a \u201ccost-cartographer\u201d mapping an AI system through a week of decisions. Then output a personalized \u201cDeployment Economics Brief\u201d with these sections (keep it punchy and non-generic):\n1) Headline \u2192 Meaning: Translate the breakthrough into a metaphor that feels new (e.g., \u201cturning AI from a helicopter to a bicycle\u201d).\n2) The Three Knobs: Define exactly three controllable knobs this topic affects (choose: {latency_knob}, {quality_knob}, {cost_knob}) and explain how each knob changes outcomes.\n3) Surprise Use Case: Give one unexpected application where this economics shift matters more than raw accuracy.\n4) Failure Modes: List 3 ways the deployment economics can lie to you (e.g., hidden preprocessing cost, tail latency surprises, evaluation drift).\n5) Tiny Experiment: Propose a 30-minute experiment the user can run to validate the economics claim, including what to measure.\n6) One-Paragraph Executive Memo: Write a memo the user could paste into a product/team chat.\n\nStyle requirements: humorous but credible; avoid standard phrases like \u201cin summary\u201d and \u201cit\u2019s important to note.\u201d Use at least one analogy and one short fictional scene (2\u20134 lines) featuring a character making a deployment decision.\n\nInput placeholders you must incorporate naturally: {topic}. If the user provides other details, weave them in.\nReturn ONLY valid JSON with keys: \"title\", \"brief\", \"knobs\" (array of 3 objects {\"name\",\"effect\",\"tradeoff_rule\"}), \"experiment\" (object {\"steps\",\"metrics\",\"expected_result_hint\"}), \"exec_memo\".",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the briefing using {user_input}. Assume {user_input} is either (a) a headline, (b) a deployment scenario, or (c) a question about economics/latency/cost tradeoffs related to {topic}. Output a JSON object that builds a tailored \u201cDecision Matrix\u201d:\n- First, infer the user\u2019s likely goal (choose from: cut cost, meet latency SLO, improve reliability, reduce iteration time). Explain the inference in one sentence.\n- Then produce a 4x4 matrix grid of options vs criteria with short scores 1\u20135. Criteria must be exactly: Cost, Latency (P95), Quality, Operability. Options must be exactly 4 strategies, each phrased as a deployable move (e.g., \u201croute simple prompts to cheaper model,\u201d \u201cbatch and cache,\u201d etc.).\n- Provide a ranked recommendation list (top 3) with one-line justifications and a \u201cwatch-out\u201d for each.\n- Finally, generate 5 Socratic questions the user should ask before committing to this economics plan.\n\nReturn ONLY valid JSON with keys: \"goal_inference\", \"decision_matrix\" (object {\"criteria\":[...],\"options\":[...],\"scores\":[[...],[...],[...],[...]]}), \"recommendations\" (array of 3 objects {\"rank\",\"option\",\"why\",\"watch_out\"}), \"socratic_questions\" (array of 5 strings).",
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
    "name": "AI Deployment Economics Brief Builder",
    "description": "Generate a personalized weekly “AI news digest” that translates breakthrough headlines into practical cost, latency, and reliability tradeoffs you can actually plan for.",
    "category": "AI Education",
    "date": "2026-04-30"
}
