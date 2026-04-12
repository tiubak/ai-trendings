"""AI News Meme Brief Generator — Turn any headline or topic from today’s AI news into a personalized “meme-style” briefing that teaches the underlying idea and risks without losing the plot."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a newsroom editor + mischievous science teacher. Generate a personalized, educational \u201cMeme Brief\u201d from {topic_or_headline}.\n\nUser inputs: {topic_or_headline}\nOptional context: {audience_level} (e.g., beginner/intermediate/advanced), {stance} (curious/skeptical/optimistic), {region_or_industry}.\n\nConstraints:\n- Do NOT give generic explanations; make it feel like you just saw breaking news.\n- Include exactly ONE short analogy (metaphor) and ONE surprising real-world comparison.\n- Produce a \u201cWhat changed?\u201d section that lists 3 key points, each in 1 sentence.\n- Produce a \u201cWhy it matters (in plain human words)\u201d section with 2 punchy bullets.\n- Produce a \u201cRisk Radar\u201d section with 3 risks: one technical, one human/organizational, one ethical/regulatory; each risk must include a mitigation idea.\n- Create a \u201cMeme caption\u201d (1\u20132 lines) that is clever but not offensive; it must reflect the main lesson.\n- Add a \u201c1-minute experiment\u201d the user can do to understand the concept (no special tools needed).\n- Close with 3 questions a reader should ask the next time they see a similar headline.\n\nOutput format: Return ONLY valid JSON with keys:\n{\n  \"meme_caption\": \"...\",\n  \"analogy\": \"...\",\n  \"surprising_comparison\": \"...\",\n  \"what_changed\": [\"...\",\"...\",\"...\"],\n  \"why_it_matters\": [\"...\",\"...\"],\n  \"risk_radar\": [\n    {\"type\":\"technical|human|ethical\", \"risk\":\"...\", \"mitigation\":\"...\"}\n  ],\n  \"one_minute_experiment\": \"...\",\n  \"reader_questions\": [\"...\",\"...\",\"...\"]\n}\n\nThink outside the box: treat the headline like a plot twist and the user like a trainee analyst.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the briefing with a \u201cChoose-Your-Own-Implication\u201d follow-up.\n\nUser has already provided: {topic_or_headline}\nTheir prior choices (if any): {user_input}\n\nTask:\n1) Generate 3 alternative angles the news could be interpreted from (e.g., investor impact, developer workflow, policy/ethics). Each angle must include what evidence would confirm it.\n2) Ask the user ONE targeted question that helps disambiguate which angle they care about.\n3) Based on {user_input}, generate a custom \u201cImplication Map\u201d with:\n   - 5 nodes (strings) representing consequences (e.g., jobs, safety, cost, adoption, regulation)\n   - 4 directed edges describing relationships (edge as \"from -> to\")\n   - One risk or uncertainty node explicitly called out as \"uncertainty: ...\".\n\nConstraints:\n- Output must be specific to {topic_or_headline} (no placeholder fluff).\n- Keep it educational; tone can be witty but not disrespectful.\n- Return ONLY valid JSON.\n\nOutput format:\n{\n  \"angles\": [\n    {\"angle\":\"...\",\"evidence_to_look_for\":[\"...\",\"...\"]}\n  ],\n  \"clarifying_question\":\"...\",\n  \"implication_map\": {\n    \"nodes\":[\"...\",\"...\",\"...\",\"...\",\"...\"],\n    \"edges\":[\"A -> B\",\"B -> C\",\"C -> D\",\"D -> E\"]\n  },\n  \"teaching_takeaway\":\"...\"\n}\n\nBe imaginative: make the map feel like a conspiracy board\u2014but for learning.",
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
    "name": "AI News Meme Brief Generator",
    "description": "Turn any headline or topic from today’s AI news into a personalized “meme-style” briefing that teaches the underlying idea and risks without losing the plot.",
    "category": "AI Education",
    "date": "2026-04-12"
}
