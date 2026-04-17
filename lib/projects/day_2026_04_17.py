"""Human–Machine Collaboration Maze (2026) — Guide a simulated team of humans and AI through a decision labyrinth to see how different collaboration strategies affect outcomes."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Create an interactive, game-like educational content pack about human\u2013machine collaboration strategies titled \u201cHuman\u2013Machine Collaboration Maze (2026)\u201d. The user will input: {topic}. Generate a scenario where a human team and an AI system must cooperate to complete a mission related to {topic}.\n\nRules:\n- Use a maze metaphor with 7\u20139 \u201crooms\u201d (steps) the user navigates.\n- Each room must offer 3 choices (A/B/C) with short consequences.\n- Include at least one \u201csurprise room\u201d where the best choice depends on a hidden factor the AI reveals (e.g., missing context, misaligned goals, data bias, or overconfidence).\n- Every choice must update a small scoreboard using exactly these metrics: quality, speed, and risk.\n- Add a humorous \u201cCollab Coach\u201d character that comments like a sarcastic but helpful guide.\n- Finish with a personalized debrief that links the user\u2019s {topic}-specific mission to practical collaboration principles (role clarity, verification, feedback cadence, and escalation paths), but do not use generic textbook phrasing\u2014use analogies (e.g., jazz improvisation, restaurant kitchen tickets, autopilot with a vigilant pilot).\n\nOutput format requirements:\nReturn a JSON object only with keys: title, mission_summary, maze_rooms (array of rooms with id, description, choices), starting_scoreboard (quality/speed/risk), and personalized_debrief (including which choice patterns the user effectively used).\n\nThink outside the box and make it memorable; no boilerplate explanations.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Using the collaboration maze concept, take the user\u2019s input {user_input} and produce a deeper analysis in JSON.\n\nRequirements:\n- Ask the AI to treat {user_input} as the user\u2019s chosen mission and prior choices (if present). If choices are not present, infer 2 plausible collaboration paths and compare them.\n- Provide a \u201cStrategy Map\u201d with exactly 5 labeled nodes: Role Clarity, Handoff Protocol, Feedback Tempo, Verification/Checks, and Escalation Rules.\n- For each node, generate: (1) a one-liner analogy, (2) a concrete tactic tailored to {user_input}, and (3) a likely failure mode.\n- Provide a final section called \u201cIf I Had 10 Minutes\u2026\u201d giving a short actionable checklist that the user could apply immediately.\n\nReturn ONLY valid JSON with keys: strategy_map (array of 5 nodes), inferred_paths (array of 2 paths with name and expected outcome), and if_i_had_10_minutes (array of checklist strings).",
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
    "name": "Human–Machine Collaboration Maze (2026)",
    "description": "Guide a simulated team of humans and AI through a decision labyrinth to see how different collaboration strategies affect outcomes.",
    "category": "AI Education",
    "date": "2026-04-17"
}
