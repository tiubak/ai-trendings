"""AI Risk Mirror Simulator — Users enter an AI scenario and receive a personalized “risk reflection” report that highlights failure modes, missing safeguards, and safer redesign options."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a creative AI safety coach running a \u201cRisk Mirror\u201d for {topic}. Generate a personalized, engaging report based on the user-provided scenario below: Scenario: {user_input}\n\nRequirements:\n- Think outside the box: use a metaphor like a carnival mirror that reveals distortions (e.g., \u201ctruthful,\u201d \u201coptimistic,\u201d \u201cconfident-but-wrong\u201d) rather than a standard checklist.\n- Include exactly 5 risk categories (you choose names), each with:\n  1) a short, punchy description (1 sentence)\n  2) one concrete example of how the scenario could go wrong (specific to {user_input})\n  3) one mitigation idea that a builder could implement (practical, but creative)\n- Add a \u201cRed Team Micro-Drill\u201d section: propose 3 adversarial tests the user could run (each test described as an input tweak or evaluation step).\n- Add a \u201cSafety Patch Notes\u201d section: output 3 revised prompts/rules that would reduce risk in this specific scenario.\n- End with a single playful line: \u201cIf this AI were a character, it would\u2026 because\u2026\u201d tailored to {user_input}.\n\nReturn your output as valid JSON only with this schema:\n{\n  \"title\": \"string\",\n  \"mirror_summary\": \"string\",\n  \"risks\": [\n    {\n      \"category\": \"string\",\n      \"distortion\": \"string\",\n      \"failure_example\": \"string\",\n      \"mitigation\": \"string\"\n    }\n  ],\n  \"red_team_micro_drill\": [\n    {\"test_name\": \"string\", \"how_to_run\": \"string\", \"what_to_watch\": \"string\"}\n  ],\n  \"safety_patch_notes\": [\n    {\"patch_name\": \"string\", \"revised_prompt_or_rule\": \"string\"}\n  ],\n  \"character_line\": \"string\"\n}\n\nMake it unique and not like generic AI safety articles.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the Risk Mirror for {topic} using the user\u2019s latest scenario details.\n\nUser input: {user_input}\nUser focus (if any): {focus}\n\nTask:\n- Output a JSON risk-refinement plan.\n- Create exactly 4 \u201cassumption probes.\u201d Each probe must include:\n  - the assumption being tested\n  - the fastest way to test it (one step)\n  - the likely failure signal (what evidence would show it\u2019s broken)\n- Create exactly 3 \u201cguardrail upgrades.\u201d Each must include:\n  - guardrail type (e.g., policy, retrieval filtering, refusal logic, uncertainty thresholding, human-in-the-loop)\n  - where it should be placed in the pipeline\n  - a short example behavior change tailored to {user_input}\n- Finally, generate a one-paragraph \u201csafer version\u201d of the scenario description (rewrite {user_input} as if redesigned with mitigations).\n\nReturn ONLY valid JSON using this schema:\n{\n  \"assumption_probes\": [\n    {\"assumption\": \"string\", \"fast_test\": \"string\", \"failure_signal\": \"string\"}\n  ],\n  \"guardrail_upgrades\": [\n    {\"guardrail_type\": \"string\", \"placement\": \"string\", \"behavior_change_example\": \"string\"}\n  ],\n  \"safer_scenario_rewrite\": \"string\"\n}\n\nDo not include any text outside JSON.",
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
    "name": "AI Risk Mirror Simulator",
    "description": "Users enter an AI scenario and receive a personalized “risk reflection” report that highlights failure modes, missing safeguards, and safer redesign options.",
    "category": "AI Education",
    "date": "2026-05-03"
}
