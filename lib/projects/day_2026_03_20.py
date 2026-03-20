"""Subagent Sandbox: Build Your Mini AI Team — Design a tiny team of specialized AI subagents for any task, see their orchestration plan, failure modes, and a pseudocode conductor — all customized to your prompt."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative agent architect and storyteller. A user gives you a single-line task: \"{task}\". Invent a playful, memorable mini-team of 3\u20136 specialized subagents to accomplish it. For each subagent provide: name, core role, short quirky personality (a 1-sentence metaphor), preferred model type (e.g., tiny local embedder, mid-size instruction-tuned model, large grounding model), compute/memory budget (low/medium/high), the exact subtask it performs, input and output formats, and one line of defensive programming (how it validates its outputs). Describe how subtasks are split so some run in parallel \u2014 draw an ASCII-style concurrency diagram or timeline. Also include: a one-paragraph orchestration pseudocode (clear, human-friendly steps), three likely failure modes with pragmatic fallbacks, an estimated resource & latency summary, and a 10-word elevator pitch for the team. Use humorous analogies, surprising metaphors, or mini-scenarios to make it memorable. Output EVERYTHING as JSON with these top-level keys: \"task\",\"team\" (array of agents),\"concurrency_diagram\",\"orchestration_pseudocode\",\"failure_modes\",\"resource_estimate\",\"elevator_pitch\". Be inventive \u2014 think of agents as quirky specialists in a heist, a kitchen brigade, or a band. Do not include any markdown \u2014 only JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "You received the user's last agent spec JSON as {user_input}. Simulate a single realistic run of that team accomplishing the task: produce a step-by-step execution trace showing messages exchanged, which subagents run concurrently (with millisecond-ish timing), intermediate data shapes, and one injected failure at a plausible point. Then show how the team recovers using the fallback behaviors defined, and produce an \"optimized_spec\" JSON recommending two concrete improvements (e.g., swap model X for Y, add caching, split a subtask) with estimated gains in latency, cost, or robustness. Return a JSON with keys: \"trace\" (array of ordered steps with timestamps), \"recovery_path\" (how failure was handled), \"optimized_spec\" (full updated spec), and \"estimates\" (before/after latency and cost). Keep the tone witty but technical, and only output JSON.",
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
    "name": "Subagent Sandbox: Build Your Mini AI Team",
    "description": "Design a tiny team of specialized AI subagents for any task, see their orchestration plan, failure modes, and a pseudocode conductor — all customized to your prompt.",
    "category": "AI Education",
    "date": "2026-03-20"
}
