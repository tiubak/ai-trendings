"""AI Startup Blueprint Studio — Turn a nascent AI idea into a playful, actionable startup blueprint — pitch, research roadmap, safety plan, compute & hiring estimates, and investor-ready bullets."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a scrappy, charming AI startup sherpa with a streak of mad-scientist creativity and a CFO who drinks black coffee. I will give you a core idea or topic: \"{topic}\". Invent a compact, original startup blueprint as JSON that a founder could use to sketch a first week plan. Use bold metaphors, a touch of humor, and at least one surprising analogy (e.g., 'your model is a sous-chef for data' or 'your safety layers are like airbags for user trust'). Think beyond generic buzzwords \u2014 propose concrete experiments and deliverables. Output JSON with the following keys: {\n  \"elevator_pitch\": short (1-2 sentences) surprising hook,\n  \"founder_story\": 2-4 sentence narrative in a memorable voice,\n  \"mission_statement\": one punchy sentence,\n  \"unique_tech\": 3 bullet ideas (short strings) that could differentiate the product technically,\n  \"early_research_roadmap\": list of 4 milestone objects {\"name\",\"goal\",\"metric\",\"weeks\"},\n  \"safety_and_ethics\": list of 3 concrete measures (not generic) to reduce misuse or bias,\n  \"compute_and_cost_estimate\": object with {\"prototype_hours_on_gpu\": number, \"monthly_dev_cost_usd\": number, \"note\": string},\n  \"hiring_plan\": list of 4 roles with short rationale,\n  \"funding_ask_and_use\": {\"seed_amount_usd\": number, \"use_case_breakdown\": {\"research\": pct, \"engineering\": pct, \"ops\": pct, \"go_to_market\": pct}},\n  \"one_weird_analogy\": one sentence metaphor that makes the tech feel real and playful\n}\nMake content original and concrete. Keep fields concise. Return valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take this input as the basis for a deeper, technical project plan: \"{user_input}\". Produce a JSON object with detailed, practical next steps for validation and scaling, suitable for a small research team. Include keys: {\n  \"prototype_experiments\": array of 4 experiment objects {\"name\",\"objective\",\"method\",\"success_metric\",\"estimated_hours\"},\n  \"validation_datasets_and_tasks\": list of dataset/task pairs with brief rationale,\n  \"model_architecture_choices\": list of 3 options with tradeoffs,\n  \"training_schedule_and_milestones\": array of week-by-week milestones for 12 weeks,\n  \"compute_budget_and_bids\": object with {\"total_gpu_hours\", \"preferred_instance_type\", \"estimated_cost_usd\"},\n  \"safety_red_team_plan\": list of 5 attack scenarios and a mitigating test for each,\n  \"3_potential_partners_or_customers\": list with short why-they-fit,\n  \"go_to_market_minimum\": short checklist of what must be demonstrable to early customers,\n  \"investor_pitch_bullets\": 6 crisp bullets that fit on a single slide,\n  \"pivot_options\": 3 alternate directions with one-line rationales\n}\nBe practical and specific: include numbers, clear tests, and short timelines. Reply only with JSON.",
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
    "name": "AI Startup Blueprint Studio",
    "description": "Turn a nascent AI idea into a playful, actionable startup blueprint — pitch, research roadmap, safety plan, compute & hiring estimates, and investor-ready bullets.",
    "category": "AI Education",
    "date": "2026-03-24"
}
