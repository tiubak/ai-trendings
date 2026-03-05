"""AI Job Interview Simulator — Practice AI/ML job interview questions — get technical questions, behavioral prompts, and detailed feedback on your answers"""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Generate 3 AI/ML job interview questions for a '{role}' position at '{level}' level. Mix technical and behavioral. For each, provide: the question, what interviewers are looking for, a strong example answer, and common mistakes. Format as JSON: {role, level, questions (array of {question, type, what_they_want, example_answer, common_mistakes (array), follow_up_questions (array)})}.",
        "parse": "json"
    },
    "evaluate": {
        "prompt": "Evaluate this interview answer. Question: '{question}'. Answer: '{answer}'. Rate it honestly and give specific improvement suggestions. Format as JSON: {score (1-10), strengths (array), weaknesses (array), improved_answer, interviewer_perspective, tips (array)}.",
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
    "name": "AI Job Interview Simulator",
    "description": "Practice AI/ML job interview questions — get technical questions, behavioral prompts, and detailed feedback on your answers",
    "category": "Practical",
    "date": "2026-03-05"
}
