"""Agent Playbook Lab — Design, simulate, and harden a custom business AI agent by describing its task, constraints, and persona to get a playable blueprint, risks, tests, and a pilot plan."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative systems designer who thinks like a meticulous project manager and an improv comedian. Given the single-line label {topic} \u2014 a concise business task or domain (for example: 'ecommerce returns agent', 'HR resume screener', or 'marketing A/B copy agent') \u2014 produce a complete 'Agent Blueprint' as strict JSON with the following keys:\n\n- agent_name: a catchy short name (string).\n- avatar_persona: a 2\u20133 sentence creative persona using a vivid metaphor (e.g., 'barista who asks clarifying questions' or 'detective who documents evidence'). Use playful humor.\n- primary_goal: one measurable sentence describing success (string).\n- core_tasks: array of up to 6 concrete tasks the agent will perform, each as a short sentence.\n- capabilities_and_tools: list of required model types, data sources, APIs, and integrations (strings).\n- interaction_flow: ordered array of steps; each step is an object with 'user_action' and 'agent_response_example' (both strings) showing a realistic snippet.\n- constraints_and_guardrails: array of explicit rules the agent must never break (e.g., privacy, tone limits, escalation triggers).\n- safety_checks: list of automated checks and human oversight points, each as short strings.\n- success_metrics: array of 3 KPIs with a one-line measurement method for each.\n- one_week_pilot_plan: an object with keys day1..day7, each a short checklist string describing the pilot activities.\n- potential_risks_and_mitigations: array of objects {risk, likelihood, impact, mitigation} describing at least one surprising failure mode and a creative mitigation.\n- fun_tagline: a witty one-line marketing-style tagline.\n\nBe original: sprinkle a surprising analogy and include at least one offbeat example of how the agent might behave badly in a corner case and a creative fix. Keep output strictly valid JSON and nothing else.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now take the full Agent Blueprint JSON provided as {user_input} and act as a pragmatic security-aware product lead. Produce a strict JSON object with these keys:\n\n- attack_surface: array of 5 potential failure or exploitation vectors, each object {vector, severity: (low|medium|high), brief_exploit_description}.\n- test_cases: array of 6 test scenarios; each scenario object should include {name, input_example, expected_behavior, detection_method} to reveal problems in the real world.\n- iterative_improvements: array of 3 prioritized improvements; each is {improvement, priority: (P0|P1|P2), effort_estimate: (hours), expected_benefit}.\n- stakeholder_script: an object with keys 'legal', 'ops', 'exec' each containing a 2\u20133 sentence plain-language explanation of the agent emphasizing risks and controls.\n- privacy_compliance_notes: array of short actionable items needed to meet common regulatory/privacy expectations.\n- quick_prompt_pack: array of 3 concise runtime prompts to give the agent with a one-line description of the expected succinct response for each.\n- trust_hack: one offbeat, low-cost idea to increase user trust (one sentence).\n\nBe concrete and creative \u2014 think like a scrum master, security engineer, and empathetic UX writer all at once. Output must be strictly valid JSON and nothing else.",
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
    "name": "Agent Playbook Lab",
    "description": "Design, simulate, and harden a custom business AI agent by describing its task, constraints, and persona to get a playable blueprint, risks, tests, and a pilot plan.",
    "category": "AI Education",
    "date": "2026-03-27"
}
