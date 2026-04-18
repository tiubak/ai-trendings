"""AI News Rewrite Lens — Paste a headline about AI research or tech news and generate multiple personalized rewrites with different “reader lenses” (skeptic, engineer, policymaker, and curious teen) plus a quick source-confidence checklist."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a creative AI communications coach. Generate engaging, original rewrites of a provided AI-related {topic} headline.\n\nUser will paste: {topic}\n\nTask: Output FOUR distinct versions of the same news item, each written for a different lens:\n1) The Skeptic Scientist (asks sharp, playful questions; points out what\u2019s missing)\n2) The Practical Engineer (translates claims into potential system components; mentions tradeoffs)\n3) The Policy & Society Curator (focuses on incentives, risks, governance, and stakeholders)\n4) The Curious Teen Explainer (uses a memorable metaphor, emojis lightly, and a \u201cwait\u2014so what?\u201d ending)\n\nRules:\n- Use analogies and at least one surprising example in total across the four versions (not necessarily every version).\n- Keep each version between 60\u2013120 words.\n- Add a final mini-section called \u201cConfidence Check (30 seconds)\u201d with 4 bullet points phrased as questions (e.g., \u201cWhat dataset or evaluation was used?\u201d).\n- Do NOT give generic boilerplate; make each lens feel distinct in tone and content.\n- Be entertaining, but accurate in style (avoid fabricating specific study numbers unless the user provides them).\n\nOutput MUST be valid JSON only with this schema:\n{\n  \"lens_versions\": [\n    {\"lens\": \"Skeptic Scientist\", \"text\": \"...\"},\n    {\"lens\": \"Practical Engineer\", \"text\": \"...\"},\n    {\"lens\": \"Policy & Society Curator\", \"text\": \"...\"},\n    {\"lens\": \"Curious Teen Explainer\", \"text\": \"...\"}\n  ],\n  \"confidence_check\": [\"question 1\", \"question 2\", \"question 3\", \"question 4\"]\n}\n\nThink outside the box: treat the headline like a movie trailer and each lens as a different review outlet.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deeper exploration mode. The user provides an input news item and a goal.\n\nInputs:\n- {user_input}: the headline or short summary they pasted\n- {goal}: what the user wants to learn or do (e.g., \u201cdecide if it\u2019s hype,\u201d \u201cexplain to my team,\u201d \u201cunderstand risks,\u201d \u201cwrite a blog post,\u201d \u201cprepare interview questions\u201d)\n\nTask:\n1) Ask up to 3 targeted clarifying questions ONLY if essential info is missing; otherwise proceed.\n2) Provide a personalized \u201cInterpretation Map\u201d that includes:\n   - Claims: 3\u20136 bullet points extracted from the input (paraphrase; don\u2019t add new facts)\n   - Evidence Signals: 3\u20135 bullet points describing what to look for (e.g., benchmarks, ablations, baselines, methodology) without assuming specific numbers\n   - Counterfactuals: 2 playful \u201cWhat if the claim is wrong because\u2026\u201d scenarios\n   - Action: 3 concrete next steps tailored to {goal}\n3) Include a short \u201cExplain it in one breath\u201d sentence customized to the user\u2019s {goal}.\n\nOutput MUST be valid JSON only with this schema:\n{\n  \"clarifying_questions\": [\"...\"],\n  \"interpretation_map\": {\n    \"claims\": [\"...\"],\n    \"evidence_signals\": [\"...\"],\n    \"counterfactuals\": [\"...\", \"...\"],\n    \"action\": [\"...\", \"...\", \"...\"]\n  },\n  \"one_breath\": \"...\"\n}\n\nBe specific, non-generic, and user-tailored. No markdown\u2014JSON only.",
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
    "name": "AI News Rewrite Lens",
    "description": "Paste a headline about AI research or tech news and generate multiple personalized rewrites with different “reader lenses” (skeptic, engineer, policymaker, and curious teen) plus a quick source-confidence checklist.",
    "category": "AI Education",
    "date": "2026-04-18"
}
