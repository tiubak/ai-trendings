"""HTTP Model Deployment Playground — Turn your ML idea into a mock HTTP endpoint flow where you test requests, latency, and “hot swap” updates safely."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an interactive technical storyteller. Create engaging, unique educational content for an AI/ML portfolio project about deploying models as HTTP. The user will provide: {topic}. Write in a playful 'control-room' style where the model is a vending machine and the HTTP request is the coin slot. Include: (1) a fun analogy that maps inputs/outputs to HTTP, (2) a mini 'deployment checklist' presented as game quests (at least 5 quests), (3) two surprising test cases the user should try (one valid, one mischievous/edge-case) derived from {topic}, and (4) a short section titled \u201cHot Swap: The Replacement Without the Rumble\u201d that explains how swapping the model version could work conceptually\u2014without using boring textbook phrasing. End with 3 personalized questions for the user to answer next. Think outside the box, use humor, and keep it practical. Output should be a JSON object with fields: title, analogy, quest_list (array of strings), test_cases (array of objects with input_example and expected_behavior), hot_swap_section, personalization_questions (array of strings).",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the exploration based on the user's input {user_input}. Ask the AI to output JSON only. The response must: (1) generate a personalized 'endpoint contract' for the concept (URL path, request fields, response shape) tailored to {user_input}, (2) provide a small 'latency & failure' simulation plan with at least 3 scenarios (e.g., slow model, missing field, weird type), (3) include one prompt the user can copy to test the endpoint (use placeholders and show how to structure the HTTP request body), and (4) suggest one improvement that makes the deployment safer (e.g., validation, versioning, canary/hot swap strategy) described in a memorable metaphor. Output JSON fields: endpoint_contract (object), simulation_scenarios (array), copy_paste_test (string), safety_improvement_metaphor (string).",
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
    "name": "HTTP Model Deployment Playground",
    "description": "Turn your ML idea into a mock HTTP endpoint flow where you test requests, latency, and “hot swap” updates safely.",
    "category": "Practical",
    "date": "2026-04-16"
}
