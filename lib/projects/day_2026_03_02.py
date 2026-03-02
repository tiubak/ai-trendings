"""AI Trends Impact Simulator — Enter an industry or topic to get a concise, hands-on analysis of current AI trends, practical applications, a learning path, and a mini-project idea."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert AI educator. Given a user-specified industry or topic {topic}, generate a single JSON object (no extra text) that teaches a learner about current AI trends affecting that topic and gives actionable next steps. Include the exact fields below and follow types and short formats. Keep entries concise and practical.\n\nRequired JSON fields and formats:\n- topic: string (echo the input)\n- trend_summary: string (2-3 sentences describing how current AI trends relate to the topic)\n- top_applications: array of objects [{\"name\":string, \"description\":string, \"impact_level\":\"Low\"|\"Medium\"|\"High\"}]\n- maturity_level: string (one of 'Research', 'Early adoption', 'Scaling', 'Mainstream')\n- impact_score: number (1-10)\n- required_skills: array of strings (key skills to work on)\n- beginner_learning_path: array of objects [{\"step_number\":int, \"title\":string, \"duration_weeks\":int, \"resources\": [{\"title\":string, \"url\":string}]}]\n- prototype_idea: object {\"title\":string, \"description\":string, \"tech_stack\": [strings], \"estimated_time_days\":int}\n- datasets_and_tools: array of objects [{\"name\":string, \"type\":\"dataset\"|\"tool\"|\"api\", \"url\":string}]\n- ethical_and_regulatory_notes: array of short strings (major concerns or regs)\n- quick_exercise: object {\"exercise_description\":string, \"expected_outcome\":string, \"difficulty\":\"Easy\"|\"Medium\"|\"Hard\"}\n- confidence: string ('low'|'medium'|'high') indicating how confident you are in the recommendations\n\nConstraints: return only valid JSON matching these keys and types. Do not include commentary, examples, or extra keys. Use the user's {topic} to tailor all sections.",
        "parse": "json"
    },
    "explore": {
        "prompt": "The user will supply {user_input} as a focus area or follow-up directive (examples: 'technical deep dive', 'business case', 'prototype plan', 'ethics and policy', 'curriculum for beginners'). Based on the original topic context, produce a JSON object (only JSON) for deeper exploration with these exact fields:\n\n- focus: string (echo {user_input})\n- detailed_plan: array of steps [{\"step_number\":int, \"title\":string, \"description\":string, \"time_estimate_hours\":int}]\n- deliverables: array of objects [{\"name\":string, \"description\":string}]\n- sample_code_snippet: string (short, include language tag like \"python:\" then code; if not applicable, supply empty string)\n- evaluation_metrics: array [{\"metric\":string, \"how_to_measure\":string, \"target_value\":string}] (if not applicable, return empty array)\n- further_reading: array [{\"title\":string, \"url\":string}]\n- confidence: string ('low'|'medium'|'high')\n\nRules: tailor the plan to {user_input} and the original topic context, be practical, list measurable steps and deliverables, and return only the JSON object. Do not add commentary.",
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
    "name": "AI Trends Impact Simulator",
    "description": "Enter an industry or topic to get a concise, hands-on analysis of current AI trends, practical applications, a learning path, and a mini-project idea.",
    "category": "AI Education",
    "date": "2026-03-02"
}
