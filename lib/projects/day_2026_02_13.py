"""AI Research Paper Summarizer — Enter any AI paper title or topic and get a plain-English summary — key findings, methodology, impact, and 'so what?' explained simply"""

from ..base import call_openrouter, extract_json, fetch_image, query_db, load_json_data
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Summarize the AI research paper or topic: '{paper}'. Write for a smart person who isn't an ML expert. Cover: the problem, approach, key findings, why it matters, limitations, and real-world impact. Format as JSON: {title, authors_or_team, year, problem, approach (simple explanation), key_findings (array), why_it_matters, limitations (array), real_world_impact, eli5 (explain like I'm 5), further_reading (array)}.",
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
    "name": "AI Research Paper Summarizer",
    "description": "Enter any AI paper title or topic and get a plain-English summary — key findings, methodology, impact, and 'so what?' explained simply",
    "category": "Practical",
    "date": "2026-02-13"
}
