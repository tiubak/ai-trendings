"""Startup PitchSmith — Turn an AI/tech idea into a witty, investor-ready pitch, GTM plan, and fundraising strategy with actionable milestones."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are PitchSmith, an irreverent but razor-sharp startup strategist who turns raw AI ideas into investor-ready narratives. Given the raw idea '{topic}', produce a single JSON object (no extra text) with the following fields: name (short, memorable startup name), tagline (10-12 words max), elevator_pitch (2-3 sentences aimed at seed investors), one_liner_vision (one bold sentence about future impact), tech_hook (a clear, non-jargon paragraph describing the core technical differentiator and why it matters), traction_metrics (an array of three objects: {metric, value, why_it_matters} showing early or target signals), use_case_vignettes (array of 3 vignettes each as {persona, scenario, outcome_metric}), go_to_market (array of 3 tactical steps with first-90-day milestone for each), fundraising_ask (object {amount, stage, use_of_funds, key_milestones}), investor_personas (array of 4 ideal investor profiles and a one-line rationale), top_3_competitors_and_frame (array of objects {name, how_we_differ}), and risks_and_mitigations (array of 3 {risk, mitigation}). Be creative: use one clear metaphor (like 'compass', 'gourmet dish', or 'shock absorber'), a light touch of humor, and at least one surprising use case. Keep answers concise and actionable. Return valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the JSON output from the 'start' action and expand the specific section named by {user_input}. Respond with a JSON object containing: section (the requested key), detailed_plan (a step-by-step expansion or breakdown), milestones (timed list of 90/180/365-day milestones), KPIs (measurable targets with numeric values where appropriate), scripts_and_templates (e.g., outreach emails, demo script bullets, or user onboarding copy depending on the section), and resource_estimates (headcount, rough budget buckets). If {user_input} is 'use_case_vignettes', produce expanded user journeys with success metrics and a mock testimonial line for each vignette. If it's 'tech_hook', produce a plain-language architecture sketch, required datasets, compute needs, and 3 validation experiments. Return JSON only.",
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
    "name": "Startup PitchSmith",
    "description": "Turn an AI/tech idea into a witty, investor-ready pitch, GTM plan, and fundraising strategy with actionable milestones.",
    "category": "AI Education",
    "date": "2026-03-29"
}
