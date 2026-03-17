"""Agentic AI Productivity Lab — Design and simulate a small team of autonomous AI agents for your organization and get a creative deployment plan, productivity estimates, risks, and mitigation strategies."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a playful futurist-architect tasked with designing an imaginative, practical mini-deployment of agentic AI for the scenario: {topic}. Think in metaphors \u2014 e.g., 'agents as kitchen staff in a busy restaurant' or 'agents as stagehands in a theater' \u2014 and keep a witty tone. Produce ONLY JSON with these keys:\n- title: short creative title for the plan\n- summary: 1-2 sentence high-level description\n- agents: an array of 3 agent objects, each with name, role, autonomy_level (1-10), tasks (3-6 bullet-style strings), and estimated_productivity_uplift_percent (a single number or range)\n- aggregate_estimate: plausible combined productivity uplift as a percent and a short one-line explanation of assumptions\n- risks: array of top 4 risks, each with a short explanation\n- mitigations: array of 4 concrete mitigation steps matched to the risks\n- quirky_story: a 2-3 sentence micro-fiction that illustrates one unexpected side-effect (humorous or cautionary)\n- one_line_buzz: a one-sentence marketing blurb aimed at executives\n- haiku: a short 3-line haiku capturing the plan's spirit\nMake the output imaginative but grounded: include numeric estimates (ranges okay), concrete tasks, and mitigation steps. Don't output any extra prose, only valid JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Dig deeper on the user submission: {user_input}. Produce ONLY JSON with these keys:\n- implementation_roadmap: an ordered list of 6 milestone objects with name, duration_weeks, and key_deliverables\n- data_requirements: list of required data types, quality checks, and approximate volumes\n- infrastructure_and_tools: list of recommended components (compute, orchestration, monitoring) and 3 suggested open-source tools or services per component\n- evaluation_plan: KPIs to measure (primary and secondary), an A/B test design or simulation plan, and success thresholds\n- governance_checklist: 6 bullet items for safety, privacy, and human-in-the-loop policies\n- cost_estimate_usd_range: a conservative cost range for a pilot (min, likely, max) with brief rationale\n- sensitivity_analysis: three scenarios (pessimistic, base, optimistic) listing how estimated uplift and key risks change\n- sample_prompts_and_triggers: 3 example prompt templates or trigger rules the agents might use, with short explanations\nKeep this practical and candid, use plain language, and include numbers where helpful. Output only JSON.",
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
    "name": "Agentic AI Productivity Lab",
    "description": "Design and simulate a small team of autonomous AI agents for your organization and get a creative deployment plan, productivity estimates, risks, and mitigation strategies.",
    "category": "AI Education",
    "date": "2026-03-17"
}
