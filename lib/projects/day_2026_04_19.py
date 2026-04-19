"""Hiro Finance AI StoryLab — Enter a personal finance moment and generate a short, portfolio-ready AI product story that turns it into a safe, believable AI use-case—complete with risks and an evaluation plan."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a creative AI product strategist and educator. Build an interactive \u201cAI acquisition pitch story\u201d about {topic} (use the user\u2019s specific input: {user_input}).\n\nWrite a short, engaging mini-story (max 220 words) set like a pitch meeting where an AI product team explains how they\u2019d build a next-gen feature inspired by the {topic} acquisition. Twist it with a metaphor: money decisions as \u201ctraffic control for your future self.\u201d\n\nInclude these sections inside the story with playful headings:\n1) \u201cThe Moment\u201d \u2014 describe the user\u2019s scenario from {user_input} in 1-2 sentences.\n2) \u201cThe AI Mechanic\u201d \u2014 explain what the AI would do (1 metaphor + 2 concrete behaviors).\n3) \u201cThe Safety Rails\u201d \u2014 list 3 guardrails (privacy, hallucinations, and harm prevention) as if they\u2019re physical seatbelts.\n4) \u201cHow We\u2019d Test It\u201d \u2014 propose 3 evaluation checks (accuracy, robustness, and user outcome).\n5) \u201cThe One-Sentence Product\u201d \u2014 end with a punchy sentence the user could put on a portfolio.\n\nBe surprising, non-generic, and memorable. Avoid textbook phrasing. Output ONLY valid JSON with keys: title, story, risks, evaluation_checks, one_sentence_product.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the analysis of {topic} using the user\u2019s prior scenario {user_input}. Return JSON only.\n\nAsk the model to generate:\n- 5 alternate feature directions (each 1 sentence) that could plausibly follow from the same scenario.\n- 3 dataset ideas the team would need (each with: name, what signals it contains, and what could go wrong).\n- 1 \u201cred-team prompt\u201d that a tester would use to try to break the system (include the exact attacker goal).\n- A scoring rubric with 4 criteria (each 0-5 scale description) for deciding whether the feature is ready.\n\nStrictly respond in JSON with keys: feature_directions, dataset_ideas, red_team_prompt, scoring_rubric.",
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
    "name": "Hiro Finance AI StoryLab",
    "description": "Enter a personal finance moment and generate a short, portfolio-ready AI product story that turns it into a safe, believable AI use-case—complete with risks and an evaluation plan.",
    "category": "AI Education",
    "date": "2026-04-19"
}
