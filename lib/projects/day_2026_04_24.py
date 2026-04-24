"""Cursor Coding Quest: The Option-Deal Lab — Users enter a coding goal and a “deal constraint,” and the project generates an AI-assisted plan that mirrors real startup investment-option reasoning (what to buy, what to test, and what to measure)."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Imagine you\u2019re building a tiny sci-fi investment committee inside a code editor. The committee is deciding whether to \u201coption\u201d an AI coding startup like {topic} for your next project. \n\nFirst, ask the user for two inputs: (1) their goal in plain language (what they want the AI to build/fix) and (2) a deal constraint like a budget, time limit, or risk tolerance. Then generate:\n- A whimsical \u201cOption Memo\u201d template filled with the user\u2019s goal and constraint.\n- Three test sprints the committee would demand from the AI coding assistant (e.g., build a feature, refactor a messy module, write tests) with clear acceptance criteria.\n- A scoring rubric (0\u201310) for \u201cusefulness,\u201d \u201csafety,\u201d and \u201cshipping speed,\u201d using unexpected but memorable metaphors (e.g., usefulness is \u201chow many minutes you save per wizard hat,\u201d safety is \u201cwhether the dragons get access to prod\u201d).\n- One creative example interaction the user could have with an AI (include a short pseudo-conversation) that would produce a measurable outcome.\n\nConstraints: \n- Keep it practical enough to be usable, but entertaining enough to read.\n- Avoid generic explanations; make the content feel like it\u2019s written by a team that negotiates deals with robots.\n- End with a single actionable checklist the user can run immediately.\n\nOutput format: Return ONLY valid JSON with keys: goal_understanding, deal_constraint_understanding, option_memo, test_sprints (array of 3 objects with sprint_name, acceptance_criteria (array), expected_artifacts), scoring_rubric (array of 3 objects with metric, what_it_means, how_to_measure), sample_ai_exchange (array of {speaker, message}), immediate_checklist (array of strings).",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now deepen the simulation. The user will provide: {user_input}.\n\nUse {user_input} to generate an \u201cEvidence Pack\u201d for the same option-deal concept: \n- Produce a set of 5 probes (prompts or tasks) that would reveal the AI coding assistant\u2019s strengths/weaknesses specifically for this user_input.\n- For each probe, specify: (a) what signal to look for, (b) a pass/fail condition, and (c) the artifact the assistant should output.\n- Then create a personalized \u2018Go/No-Go\u2019 decision explanation that is contingent on the scoring rubric (you may reference usefulness, safety, shipping speed).\n\nAsk for zero additional inputs; only use {user_input}. \n\nReturn ONLY valid JSON with keys: evidence_pack_name, probes (array of 5 objects with probe_name, prompt_idea, signal_to_look_for, pass_fail_condition, expected_artifact), decision_logic (array of strings), go_no_go_summary (string).",
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
    "name": "Cursor Coding Quest: The Option-Deal Lab",
    "description": "Users enter a coding goal and a “deal constraint,” and the project generates an AI-assisted plan that mirrors real startup investment-option reasoning (what to buy, what to test, and what to measure).",
    "category": "AI Education",
    "date": "2026-04-24"
}
