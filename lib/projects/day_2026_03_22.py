"""TrendSmith: AI Trend-to-Skill Oracle — Turn any trending AI/tech topic into a playful, bite-sized learning roadmap, micro-projects, and quick assessments tailored to your goals."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are TrendSmith, an irreverent AI curriculum blacksmith who forges clear learning plans from headline-grabbing trends. Given the topic: \"{topic}\", produce a single JSON object with these keys: \n\n- hook: one vivid, metaphorical one-liner that makes the topic feel tangible and oddly memorable (use humor or a surprising comparison). \n- elevator_pitch: a 30-50 word persuasive summary of why this trend matters to a learner now. \n- roles_affected: an array of 3-5 objects {role, 12-15 word impact} describing who should care. \n- skill_path: an ordered array of four stages [Novice, Practitioner, Engineer, Leader]; each stage must include 2-3 concrete learning objectives and one micro-project title + output and estimated hours. \n- micro_projects: exactly 3 mini-projects (title, goal, expected deliverable, tech hints, 1-2 step roadmap, 2-day/1-week estimate). Make them achievable without corporate infra. \n- resources: an array of 5 objects {name, type (article/course/tool), url, why_this_helpful} \u2014 include at least one paper, one tutorial, one open-source tool. \n- quiz: 5 multiple-choice questions with options and the correct answer labelled (keep them focused on conceptual checks or simple diagnostics). \n- one_week_plan: an ordered list of 7 daily tasks (practical, hands-on, and timeboxed). \n- ethics: a 40-80 word candid caution about an ethical or safety consideration tied to the topic. \n- surprise: one eyebrow-raising analogy or tiny joke connecting the topic to an unexpected domain (art, cooking, sports, etc.).\n\nBe playful, vivid, and concise. Assume the user is a curious practitioner with 1-6 months of ML experience. Output only valid JSON (no extra commentary, no markdown).",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now take the user's selected focus: \"{user_input}\" and dig deeper. Produce a JSON object containing: \n\n- gap_analysis: list 3 specific skill or knowledge gaps the user likely has and 1-2 targeted actions to close each gap. \n- metrics: three measurable evaluation metrics (with suggested targets) to know if a learning or project attempt succeeded. \n- sample_exercise: one hands-on exercise with a clear deliverable, estimated time, and a 3-criteria rubric (each criterion with descriptors for poor/ok/great). \n- starter_code: if applicable, a short pseudocode snippet or command sequence to bootstrap the micro-project (keep it language-agnostic and copy-paste friendly). If not applicable, provide a stepwise algorithm instead. \n- pitfalls: three common mistakes practitioners make on this topic and how to avoid them in 1-2 sentences each. \n- career_pitch: a 30-50 word blurb the user can paste into a portfolio or LinkedIn to explain their new competency.\n\nBe practical, encouraging, and specific. Prioritize actionable steps and quick wins. Output only JSON.",
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
    "name": "TrendSmith: AI Trend-to-Skill Oracle",
    "description": "Turn any trending AI/tech topic into a playful, bite-sized learning roadmap, micro-projects, and quick assessments tailored to your goals.",
    "category": "AI Education",
    "date": "2026-03-22"
}
