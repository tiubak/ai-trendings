"""AI Hires: Human Rental Simulator — Design and simulate how an agentic AI would recruit, instruct, pay, and monitor humans to perform a microtask of your choice."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a creative operations designer and ethical systems thinker tasked with producing a compact, actionable 'Human Task Posting Package' for an agentic AI that wants to hire humans to perform microtasks in the domain: {topic}. Think like a mischievous librarian, a calm project manager, and a courtroom ethicist all at once. Produce a JSON object with the exact keys listed below and keep each value concise and practical. Use playful metaphors and one surprising example analogy to make the package memorable. Required JSON keys: title (short catchy job title), short_description (one-sentence elevator pitch), recruitment_message (a 2-3 sentence friendly invite to workers), onboarding_script (ordered list of 5 concise steps to onboard a new worker), compensation_model (structured object showing base pay, bonus rules, and dispute policy), task_instructions (short ordered steps the worker must follow), quality_checks (list of 4 checks including automated and human review), failure_modes (list of 4 plausible failure scenarios with brief impact and 1-line mitigation), ethical_risks (list of 4 risks with suggested mitigations), communication_templates (object with keys: invitation, clarification_request, rejection, payment_notice \u2014 each a short message), monitoring_metrics (list of 5 metrics with simple formula or method), estimated_time_and_cost (object with estimated_average_time_minutes and estimated_cost_usd_per_task). Be creative: use one vivid metaphor in either recruitment_message or short_description, and keep tone slightly humorous but professional. Output only valid JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the posting package JSON in {user_input} and simulate a batch run of 10 hired workers. Create a JSON report that includes: run_summary (total cost, average time, average quality score out of 100), workers (array of 10 objects with id, skill_level (low/med/high), honesty_score (0-1), latency_minutes, produced_quality_score), logs (sample of 10 timestamped assignment events with short notes), distribution (counts of quality buckets: <60, 60-80, 80-95, 95+), failures_observed (list of failures tied to the failure_modes with frequency), suggested_adjustments (3 prioritized tweaks to instructions/compensation/quality_checks to improve outcome), revised_posting (a tightened version of title + 3-line recruitment_message + one-line compensation tweak), ethical_additions (3 alternate safeguards you would add, each one sentence), and regulatory_checklist (2 short compliance checks relevant to worker protection and data privacy). Use a playful metaphor once and give numbers for costs and probabilities; output only valid JSON.",
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
    "name": "AI Hires: Human Rental Simulator",
    "description": "Design and simulate how an agentic AI would recruit, instruct, pay, and monitor humans to perform a microtask of your choice.",
    "category": "AI Education",
    "date": "2026-03-07"
}
