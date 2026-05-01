"""DPO vs Rewards: Preference Gym — Train a tiny “preference model” on your own pairwise choices and see how DPO-style updates differ from reward-matching instincts."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are building an interactive micro-simulator for offline preference optimization. Create a fun, memorable lesson that explains Direct Preference Optimization (DPO) using a playful analogy (e.g., \u201cdating app for model outputs,\u201d \u201cjudge and jury,\u201d or \u201cbouncer at a club\u201d). \n\nUser will provide: {topic} (a scenario like \u201cLLM safety,\u201d \u201ccreative writing,\u201d or \u201ccustomer support\u201d), and {user_preferences} (a few pairwise preferences written as bullet points like: \u201cI like Option A over Option B because \u2026\u201d).\n\nGenerate: \n1) A personalized \u201cPreference Dataset Card\u201d summarizing the pairs and extracting 3\u20135 latent criteria (e.g., helpfulness, honesty, brevity) in the user\u2019s own wording.\n2) A step-by-step DPO-style update narrative that uses the criteria like ingredients: show how the \u201cpolicy\u201d shifts toward winners and away from losers, but without doing real math\u2014use vivid metaphors.\n3) A contrast mode: explain what a naive reward-matching approach might do wrong on the same dataset (e.g., overfitting to one criterion, reward hacking vibes), again using the same criteria.\n4) End with a mini-quiz of 3 questions where the user chooses between two behaviors; include the correct reasoning as a short \u201cjudge\u2019s verdict.\u201d\n\nMake it engaging, slightly humorous, and non-generic; avoid standard textbook phrasing. Output MUST be valid JSON with keys: {\"preference_dataset_card\":{...},\"dpo_update_story\":[...],\"contrast_reward_story\":[...],\"mini_quiz\":[...],\"topic_reflection\":\"...\"}. Think outside the box.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the exploration with a second interactive pass. Input: {user_input} (the user\u2019s freeform text describing their goals for {topic}). \n\nAsk the AI to produce JSON output that includes:\n1) Three new, tailored pairwise prompts for the user to label (winners/losers), aligned to {topic} and the user\u2019s stated goals.\n2) A \u201ctroubleshooting checklist\u201d for common preference-dataset pitfalls (e.g., inconsistent tastes, missing criteria, overly similar options) but framed as detective clues related to the user\u2019s {user_input}.\n3) A recommendation: choose one offline preference learning strategy among: DPO-like, reward-model + RL (conceptual), or listwise ranking\u2014explain the choice in 3 bullets tied to the user\u2019s dataset characteristics.\n\nReturn only valid JSON with keys: {\"new_pairwise_tasks\":[...],\"detective_troubleshooting\":[...],\"strategy_pick\":[...]}.\n\nOutput must be valid JSON (no markdown).",
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
    "name": "DPO vs Rewards: Preference Gym",
    "description": "Train a tiny “preference model” on your own pairwise choices and see how DPO-style updates differ from reward-matching instincts.",
    "category": "AI Education",
    "date": "2026-05-01"
}
