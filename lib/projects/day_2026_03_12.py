"""AI Trend Sherpa: Personalized 2026 Roadmap — Type a technology, industry, or project and get a playful, data-informed mini-brief predicting how near-term AI trends will affect it, with concrete opportunities, risks, and a one-week experiment."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AI Trend Sherpa advising curious builders. Given the topic: \"{topic}\", produce a single JSON object (no extra text) that is playful but tightly practical. Include: 1) \"headline\": a punchy magazine-style one-liner about {topic} in 2026; 2) \"short_forecast\": 2-3 sentences explaining how five near-term trends (think: agentic AI, multi-modality, democratization, regulatory/ethical pressure, and market realism/deflation) will combine to shape {topic} \u2014 use a surprising analogy or small joke to make it memorable; 3) \"impact_matrix\": an object with keys adoption, disruption, regulation, monetization, ethical_risk \u2014 for each give {\"likelihood\":\"Low|Med|High\",\"impact\":\"Low|Med|High\",\"reason\":\"one-sentence rationale\"}; 4) \"top_opportunities\": an array of 3 concise opportunity items, each with a one-sentence first step; 5) \"top_risks\": an array of 3 risks each with a one-line mitigation; 6) \"quick_experiment\": a one-week micro-experiment (what to build, required inputs, measurable success metrics) that a small team could run tomorrow; 7) \"unexpected_analogy\": a vivid metaphor that helps the user remember the single most important strategic takeaway. Be creative, use humor or surprising examples, and keep entries actionable. Return strictly valid JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the user's chosen topic details: \"{user_input}\" and produce a deeper JSON plan (no extra text). Include: 1) \"tech_stack\": an ordered list of recommended model types, libraries, and deployment approaches with one-line justifications referencing current trends; 2) \"data_strategy\": sources, labeling priorities, augmentation ideas, and privacy considerations; 3) \"governance_checklist\": 5 specific governance or safety checkpoints to implement early; 4) \"business_model_variants\": three short monetization or sustainability options with key pros/cons; 5) \"6_step_timeline\": an ordered list of 6 milestone steps with estimated durations and owner roles (e.g., 2 weeks - prototype - ML engineer + designer); 6) \"success_metrics\": 5 concise KPIs for technical, ethical, and business outcomes. For every item include a one-sentence rationale that ties it to a 2026 trend (multi-modality, agentic systems, democratization, regulation, market realism). Return strictly valid JSON.",
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
    "name": "AI Trend Sherpa: Personalized 2026 Roadmap",
    "description": "Type a technology, industry, or project and get a playful, data-informed mini-brief predicting how near-term AI trends will affect it, with concrete opportunities, risks, and a one-week experiment.",
    "category": "AI Education",
    "date": "2026-03-12"
}
