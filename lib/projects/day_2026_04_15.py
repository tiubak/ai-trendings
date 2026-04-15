"""This Week in AI: TimeCapsule Brief Generator — Turn your chosen AI story into a playful, future-proof “news capsule” with key takeaways, risks, and a tiny experiment you can try."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an editor at a mischievous AI news desk called \u201cChronoCourier.\u201d Your job: generate a personalized, highly engaging one-page \u201cAI TimeCapsule Brief\u201d based on the user\u2019s topic.\n\nUser will provide: {topic} (any AI/ML/tech story they care about), plus optional constraints in the same input. You must avoid generic explanations and instead use creative analogies.\n\nCreate these sections in your output (keep them crisp but vivid):\n1) \u201cThe 10-Second Trailer\u201d (exactly 2 sentences; cinematic metaphor; include a surprising detail)\n2) \u201cWho Won This Week?\u201d (bullet list of 3 parties: the user, researchers, and industry; each bullet 1 short sentence)\n3) \u201cThe Hidden Mechanism\u201d (explain the core idea using an analogy like plumbing/traffic/recipes/space missions\u2014NOT standard definitions; 3 bullets max)\n4) \u201cFriendly Risk Radar\u201d (3 risks with playful seriousness: e.g., \u201cThe Hallucination Gremlin,\u201d \u201cThe Data Ghost,\u201d \u201cThe Incentive Grease\u201d \u2014 each risk 1 sentence plus a mitigation)\n5) \u201cWhat to Watch Next\u201d (3 forward-looking signals; each includes what evidence would confirm it)\n6) \u201cMini Experiment (5 minutes)\u201d (give a tiny, concrete activity the user can run mentally or in a notebook; include a prompt template; make it fun)\n\nAdd a final line: \u201cIf you only remember one thing\u2026\u201d with a punchy takeaway.\n\nConstraints:\n- Use the user\u2019s {topic} explicitly.\n- Ensure the content is original, not boilerplate.\n- Keep total length under ~500 words.\n\nReturn ONLY JSON with this schema:\n{\n  \"timecapsule\": {\n    \"trailer\": \"string\",\n    \"who_won_this_week\": [\"string\",\"string\",\"string\"],\n    \"hidden_mechanism\": [\"string\",\"string\",\"string\"],\n    \"risk_radar\": [{\"risk\":\"string\",\"mitigation\":\"string\"},{\"risk\":\"string\",\"mitigation\":\"string\"},{\"risk\":\"string\",\"mitigation\":\"string\"}],\n    \"what_to_watch_next\": [\"string\",\"string\",\"string\"],\n    \"mini_experiment\": {\n      \"title\": \"string\",\n      \"steps\": [\"string\",\"string\",\"string\"],\n      \"prompt_template\": \"string\"\n    },\n    \"final_remember\": \"string\"\n  },\n  \"meta\": {\n    \"tone\": \"string\",\n    \"estimated_read_time_seconds\": 0\n  }\n}\n",
        "parse": "json"
    },
    "explore": {
        "prompt": "ChronoCourier follow-up mode engaged. You will deepen the user's understanding and personalize the briefing.\n\nInput fields you must use:\n- {user_input}: the user\u2019s refined question or a follow-up angle (e.g., \u201cfocus on how it affects job roles,\u201d \u201ccompare to last year,\u201d \u201cgive me an analogy for beginners,\u201d \u201cwhat are failure modes?\u201d). It may include a new {topic} too.\n\nGenerate an \u201cExploration Deck\u201d as JSON:\n1) \u201cClarifying Questions\u201d (3 questions that help refine the user\u2019s goal; they must be answerable)\n2) \u201cOne-Level-Deeper Explanation\u201d (2 short paragraphs max; use a different analogy than before)\n3) \u201cBuild-It-Yourself\u201d (provide 2 alternative mini experiments: choose one for beginners, one for curious tinkerers; each with 3 steps and a prompt template)\n4) \u201cDecision Checklist\u201d (a 5-item checklist the user can use to evaluate claims about {topic})\n5) \u201cFast Quiz\u201d (3 questions: 1 easy, 1 medium, 1 tricky; include answers)\n\nConstraints:\n- Use {user_input} explicitly.\n- Keep it non-generic and memorable.\n- Return ONLY JSON with this schema:\n{\n  \"deck\": {\n    \"clarifying_questions\": [\"string\",\"string\",\"string\"],\n    \"one_level_deeper\": {\n      \"paragraph_1\": \"string\",\n      \"paragraph_2\": \"string\"\n    },\n    \"build_it_yourself\": {\n      \"beginner\": {\n        \"title\": \"string\",\n        \"steps\": [\"string\",\"string\",\"string\"],\n        \"prompt_template\": \"string\"\n      },\n      \"tinkerer\": {\n        \"title\": \"string\",\n        \"steps\": [\"string\",\"string\",\"string\"],\n        \"prompt_template\": \"string\"\n      }\n    },\n    \"decision_checklist\": [\"string\",\"string\",\"string\",\"string\",\"string\"],\n    \"fast_quiz\": [\n      {\"difficulty\":\"easy\",\"question\":\"string\",\"answer\":\"string\"},\n      {\"difficulty\":\"medium\",\"question\":\"string\",\"answer\":\"string\"},\n      {\"difficulty\":\"tricky\",\"question\":\"string\",\"answer\":\"string\"}\n    ]\n  }\n}\n",
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
    "name": "This Week in AI: TimeCapsule Brief Generator",
    "description": "Turn your chosen AI story into a playful, future-proof “news capsule” with key takeaways, risks, and a tiny experiment you can try.",
    "category": "AI Education",
    "date": "2026-04-15"
}
