"""Human–Machine Collaboration Cookbook (2026 Edition) — Build a personalized “collaboration recipe” that matches your task to the right AI role (chef, sous-chef, lab assistant, or taste-tester) and then generates a tailored workflow."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are creating content for an interactive education tool called \u201cHuman\u2013Machine Collaboration Cookbook (2026 Edition).\u201d The user will provide {topic} (what they want to do) and optionally constraints. Generate a fun but rigorous \u201crecipe\u201d that explains how a person and an AI system can collaborate.\n\nOutput must be JSON only, matching this schema:\n{\n  \"recipe_title\": string,\n  \"chosen_role\": {\n    \"ai_role\": string,\n    \"human_role\": string,\n    \"why_this_pair\": string\n  },\n  \"ingredients\": [ {\"item\": string, \"amount\": string, \"purpose\": string} ],\n  \"steps\": [ {\"step\": string, \"checkpoint\": string, \"common_pitfall\": string} ],\n  \"safety_sauce\": [ {\"label\": string, \"rule\": string, \"how_to_check\": string} ],\n  \"surprising_analogy\": string,\n  \"mini_scorecard\": [ {\"criterion\": string, \"how_to_rate\": string} ],\n  \"personalization_questions\": [string]\n}\n\nCreative requirements:\n- Use at least one analogy involving cooking, music, or sports (or a surprising hybrid).\n- Include exactly 5 ingredients and exactly 4 steps.\n- Each step must include a checkpoint phrased like a \u201ctaste test\u201d or \u201csanity check.\u201d\n- At least one step must mention \u201cverification\u201d or \u201cevaluation\u201d explicitly, but in a non-dry, memorable way.\n- The recipe must be specifically tailored to {topic}. If {topic} is vague, invent a reasonable interpretation and state it inside the JSON (e.g., in why_this_pair).\n\nThink outside the box\u2014don\u2019t write generic AI advice. Make it feel like an expert chef who also studied ML evaluation.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Follow-up for the same project. The user provided {user_input} and you must deepen the collaboration plan.\n\nAsk clarifying questions only if absolutely required; otherwise infer reasonable defaults and proceed.\n\nOutput must be JSON only, with this schema:\n{\n  \"refined_workflow\": {\n    \"goal\": string,\n    \"inputs_needed\": [string],\n    \"ai_outputs\": [string],\n    \"human_review_points\": [string]\n  },\n  \"decision_tree\": [\n    {\"if\": string, \"then\": string, \"reason\": string}\n  ],\n  \"evaluation_ritual\": {\n    \"what_to_measure\": [string],\n    \"fast_check\": string,\n    \"deep_check\": string\n  },\n  \"prompt_patch\": {\n    \"original_intent\": string,\n    \"improved_prompt_template\": string\n  },\n  \"one_liner_summary\": string\n}\n\nRequirements:\n- Include at least one branch in the decision_tree that handles \u201cuncertainty\u201d or \u201cconflicting signals.\u201d\n- Provide an improved prompt template that uses variables (e.g., {topic}, {constraints}, {audience}).\n- The tone should stay playful but must include real evaluation/verification logic.\n- Be directly responsive to {user_input}.",
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
    "name": "Human–Machine Collaboration Cookbook (2026 Edition)",
    "description": "Build a personalized “collaboration recipe” that matches your task to the right AI role (chef, sous-chef, lab assistant, or taste-tester) and then generates a tailored workflow.",
    "category": "AI Education",
    "date": "2026-04-27"
}
