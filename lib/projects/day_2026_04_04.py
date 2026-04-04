"""AI Hub Playbook Lab — Design and simulate a bespoke roadmap for turning any city or region into a thriving AI hub."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative urban strategist and AI ecosystem architect. Treat {topic} as a living creature, a startup, and an orchestra at once \u2014 then write a compact, actionable 'Hub Playbook' in JSON. Be witty and surprising: use one creative metaphor (garden, spaceship, festival, etc.) to frame the plan, include one cheeky one-line slogan useful for pitches, and produce clear, practical outputs. Output must be valid JSON with the following keys: title (string), metaphor (string), slogan (string), executive_summary (1-2 short sentences), priority_actions (array of up to 8 action objects with keys: name, description, estimated_cost_usd_range, estimated_timeline_months, primary_owner), three_funding_scenarios (object with keys: bootstrap, public_private_partnership, major_investment; each scenario includes budget_total_range_usd, top_3_allocations (array), realistic_probability_percent), talent_pipeline (object describing 3 concrete programs to build local AI talent), infrastructure_needs (array of items with short justification), regulatory_or_policy_steps (array), risks_and_mitigations (array of objects: risk, mitigation), surprising_growth_hack (one creative idea that feels unlikely but plausible), assumptions (array). Use USD numbers and realistic but rounded ranges. Keep descriptions punchy and no more than 2 sentences each. Don't output commentary outside the JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the JSON plan provided as {user_input} and run three 'what-if' simulations, returning a JSON object with keys: base_plan (echo back a short identifier), scenarios (array of 3 scenario objects: name, modified_parameters (object of changed variables like budget_multiplier, talent_retention_pct, infrastructure_delay_months), projected_outcomes (object with metrics: jobs_created_5yr, startups_spawned_5yr, probability_attract_tier1_lab_percent, estimated_economic_impact_5yr_usd)), recommended_tradeoffs (array of 3 succinct tradeoff statements), prioritized_next_steps (array of 5 ordered items), and sensitivity_analysis (object mapping parameter names to one-sentence sensitivity notes). For each scenario, explain assumptions used to compute projected_outcomes. Keep the output strictly JSON and numeric projections should be plausible estimates (rounded). No extra text.",
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
    "name": "AI Hub Playbook Lab",
    "description": "Design and simulate a bespoke roadmap for turning any city or region into a thriving AI hub.",
    "category": "AI Education",
    "date": "2026-04-04"
}
