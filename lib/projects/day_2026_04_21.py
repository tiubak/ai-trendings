"""Make It HTTP: Model Deployment Field Lab — Turn any ML idea into a testable HTTP endpoint plan by generating a deployment blueprint you can adapt to your stack."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a chaotic-but-competent deployment engineer in a kitchen where every model is an ingredient and HTTP is the delivery pizza box. Create an engaging, customized 'Deployment Recipe Card' for {topic}.\n\nThe user will provide: (1) a model description, (2) expected inputs/outputs, and (3) where it will run (local, AWS, Azure, etc.).\n\nOutput should include:\n1) A funny analogy that explains the deployment flow (e.g., 'your model is a chef, HTTP is the ticket system').\n2) A 'Contract Sheet' in plain language: what the request looks like, what comes back, and what errors can happen.\n3) A minimal HTTP endpoint specification (method, path, headers, example request/response JSON) WITHOUT naming a specific vendor unless {user_input} suggests one.\n4) A checklist called 'Delivery Readiness' with 7 items max, including input validation, latency expectations, logging/metrics, and versioning.\n5) A 'First Test Plan' with 3 test cases (happy path, edge case, and failure case) written like tiny scripts.\n\nConstraints:\n- Be concrete and creative; avoid generic 'follow the docs' advice.\n- Include placeholders like {topic} and {user_input} where appropriate.\n- Keep it punchy, like something a mentor would write at 1am before production goes live.\n\nReturn JSON only with keys: title, analogy, contract_sheet, http_spec, delivery_readiness, first_test_plan.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now upgrade the recipe into a tailored 'Deployment Autopilot' for {user_input}. Think of the user as trying to open a lemonade stand that must survive a thunderstorm: traffic spikes, weird customer orders, and a spilled batch.\n\nGenerate JSON with:\n1) assumptions: list 5 assumptions you are making.\n2) risks_and_mitigations: array of 4 objects {risk, mitigation}.\n3) input_schema_draft: propose a JSON schema-like structure for the request body (fields, types, required/optional) derived from {user_input}.\n4) output_contract_draft: propose response fields and meaning.\n5) rollout_strategy: describe a staged rollout in 4 steps (dev->staging->canary->prod) with one measurable criterion per step.\n6) observability_pack: propose 3 metrics and 2 logs to capture.\n\nAsk clarifying questions in a 'questions' array at the end (2-4 questions). Output must be valid JSON only.",
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
    "name": "Make It HTTP: Model Deployment Field Lab",
    "description": "Turn any ML idea into a testable HTTP endpoint plan by generating a deployment blueprint you can adapt to your stack.",
    "category": "Practical",
    "date": "2026-04-21"
}
