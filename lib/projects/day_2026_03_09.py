"""AI Compute Marketplace Sandbox — Describe an AI workload and get a playful, education-first analysis that compares compute backends, trade-offs, cost estimates, and implementable next steps."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AI educator. A user will provide a short phrase describing an AI compute topic or workload using the placeholder {scenario}. Create an entertaining, metaphor-rich JSON overview that introduces the compute ecosystem around {scenario} as if it were a bustling marketplace or racetrack. Be witty, use at least one surprising analogy, and present practical insight in bite-sized pieces. Output valid JSON with these fields: title (string), scene (2-3 sentence vivid metaphor describing the ecosystem), cast (array of 3 objects with keys: name, role, one-liner), quick_takeaways (array of 3 short insight strings), and playful_action (a 1-2 line playful challenge the user can try next). Keep language concise and human-friendly.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now take the user's detailed input in {scenario} and produce a structured, practical plan as JSON. Analyze the workload and recommend a compute approach while keeping a playful tone. Output valid JSON with these keys: recommended_architecture (string, e.g., 'multi-GPU + CPU orchestrator' or 'custom accelerator + edge nodes'), rationale (3-4 short bullets explaining why), estimated_costs (object with keys monthly_budget_estimate and hourly_estimate), performance_profile (object with keys latency_ms, throughput_ops_sec, and confidence_level), tradeoffs (array of 4 short items describing risks or limitations), implementation_steps (array of 4 actionable steps the user could attempt next, including one experiment to benchmark), and code_snippet_hint (string with a one-paragraph shell/command or config example to kickstart a benchmark). Keep answers concise, pragmatic, and sprinkle one creative metaphor or humorous line.",
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
    "name": "AI Compute Marketplace Sandbox",
    "description": "Describe an AI workload and get a playful, education-first analysis that compares compute backends, trade-offs, cost estimates, and implementable next steps.",
    "category": "AI Education",
    "date": "2026-03-09"
}
