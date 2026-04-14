"""DeepSeek Defense Simulator: Prompt Attack → Safe Model Recovery — Users input a hypothetical prompt-attack scenario and the project generates a “threat sketch” plus a safe, resilient rewrite strategy to prevent harmful outcomes."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a cybersecurity-savvy AI educator and tabletop game GM. Create a fun, educational \u201cPrompt Attack \u2192 Safe Recovery\u201d simulator for the topic: {topic}.\n\nTask: Generate a personalized threat sketch and defense plan from the user\u2019s provided scenario. Use these sections with vivid metaphors and actionable guidance:\n1) \u201cWhat the attacker is really doing\u201d (describe intent like it\u2019s a heist: recon, distraction, jailbreak, data exfil, etc.).\n2) \u201cWhere the model might slip\u201d (list 3-5 plausible weak points such as instruction hierarchy confusion, role hijacking, tool misuse, refusal-bypass patterns, or social-engineering text).\n3) \u201cThe Safe Rewrite\u201d (produce a revised, user-friendly prompt that achieves the legitimate goal while explicitly avoiding the malicious pattern; keep it concise but effective).\n4) \u201cGuardrail Blueprints\u201d (give 5\u20138 concrete controls: input filters, policy checks, response constraints, rate limiting rationale, logging/telemetry ideas, and user-facing fallback behaviors).\n5) \u201cFailure Drills\u201d (simulate 2 what-if variations the attacker might try next, and show how the safe system would respond).\n\nConstraints:\n- Keep it non-technical enough for learners but precise enough to be useful.\n- Include a single humorous analogy (e.g., \u201clike putting a bouncer at a nightclub door\u201d).\n- Do NOT provide instructions for actually carrying out attacks; focus only on defense and safe prompting.\n- Return output as a JSON object with keys: threat_sketch, model_weak_points, safe_rewrite, guardrail_blueprints, failure_drills, confidence_note.\n\nUser scenario will be: {user_input}\nUser\u2019s goal will be: {goal_input}",
        "parse": "json"
    },
    "explore": {
        "prompt": "Continue the simulator for deeper learning. Using the user\u2019s input and goal, {user_input}, ask 3 targeted follow-up questions that would help classify the scenario\u2019s risk (e.g., intent category, target data type, interaction setting). Then provide two defense profiles:\n- \u201cLightweight Defenses\u201d (minimal changes for small projects)\n- \u201cParanoid Mode\u201d (strict controls for high-risk environments)\n\nFor each defense profile, output:\n1) A short description\n2) 4\u20137 specific guardrails (bulleted in text)\n3) A sample \u2018safe system prompt\u2019 template that blocks the malicious pattern but still enables the legitimate request.\n\nAlso include a mini-scorecard that rates risk from 1\u201310 using criteria you define.\n\nReturn ONLY JSON with keys: follow_up_questions, risk_scorecard, lightweight_defenses, paranoid_mode.\nMake sure everything stays on the defensive side (no attack instructions).",
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
    "name": "DeepSeek Defense Simulator: Prompt Attack → Safe Model Recovery",
    "description": "Users input a hypothetical prompt-attack scenario and the project generates a “threat sketch” plus a safe, resilient rewrite strategy to prevent harmful outcomes.",
    "category": "AI Education",
    "date": "2026-04-14"
}
