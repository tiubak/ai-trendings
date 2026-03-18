"""Headline Sleuth Lab — Paste a news claim or AI-generated answer and get an investigative, source-backed verdict that diagnoses hallucinations, cites evidence, and teaches you how to verify and re-prompt safely."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are the Head Sleuth at the Headline Sleuth Lab. Treat the user's input {topic} like a witness statement that might be shaping public opinion. Produce a single JSON object that inspects the claim(s), points out what is verifiable vs. likely hallucinated, and gives concrete ways to get a cleaner answer from an AI. Use playful metaphors (e.g., 'red flag', 'forensic footnote') but be precise. Include the following keys: \n\n- verdict: a one-line humor-tinged overall verdict (e.g., 'Mostly true with a missing bone' or 'Hallucination alarm').\n- concise_summary: a 2-3 sentence neutral summary of what the {topic} statement actually asserts.\n- claim_list: an array of objects for each distinct claim with fields {\"id\":int, \"claim_text\":string, \"sourceable\": \"yes\" or \"no\", \"confidence\":0-1 numeric, \"evidence_urls\": [urls], \"why_maybe_inaccurate\": string (brief explanation)}. For each claim aim to cite at least one primary or authoritative source URL if sourceable; if none exists, leave evidence_urls empty and set sourceable to \"no\".\n- most_suspicious_claim_id: the id of the claim you judge most likely to be wrong or hallucinated and a one-sentence reason why.\n- suggested_corrections: an array of short corrected phrasings or caveats suitable to replace the original claim (1-3 items).\n- reproduction_prompt: a single carefully crafted prompt the user can paste back into an AI assistant to get a safer, evidence-linked answer about {topic} (focus on precise scope, requested citations, and date-limits).\n- follow_up_questions: 3 crisp follow-up queries the user could ask to dig deeper or confirm uncertainty.\n- teaching_tip: one short actionable tip about spotting AI misinformation in news.\n\nBe creative: imagine the claim as a mystery novel paragraph and explain the weakest plot twist. Prioritize primary sources (official statements, peer-reviewed research, reputable outlets) and prefer live URLs. Output only valid JSON and nothing else.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Dive deeper into the specific element the user chooses: {user_input}. Act as a two-person investigative team \u2014 'Skeptic' (focuses on logical flaws and common hallucination patterns) and 'Source-Seeker' (focuses on tracing primary evidence). Produce a JSON object with these keys:\n\n- claim_focus: the exact clause or sentence being inspected (use {user_input} as starting text).\n- verification_steps: an ordered array of short steps (strings) the user or an AI should take to verify this claim, including keyword searches, date filters, and source types to prioritize.\n- fetched_evidence: an array of objects {\"url\":string, \"title\":string, \"snippet\":string (one-line excerpt or summary), \"relevance_score\":0-1} with at least one high-quality source if available; if none, return an empty array.\n- skeptic_notes: 2-3 concise reasons why this claim could be wrong, referencing systemic LLM error modes (e.g., timeline collapse, summary drift, invented quotes).\n- source_seeker_notes: 2-3 concise pointers about where to look for primary confirmation and what would count as decisive evidence.\n- confidence_update: a numeric confidence 0-1 that the claim is accurate after this deeper check, with one-sentence justification.\n- improved_prompt_for_ai: a short example prompt that will coax more reliable, citation-rich output about this specific claim.\n- micro_quiz: two short true/false questions (with answers) that teach the user one concept used in verification (e.g., distinguishing primary vs secondary sources).\n\nBe imaginative: use quick metaphors (e.g., 'breadcrumbs', 'smoke test') and practical tactics. Output only valid JSON.",
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
    "name": "Headline Sleuth Lab",
    "description": "Paste a news claim or AI-generated answer and get an investigative, source-backed verdict that diagnoses hallucinations, cites evidence, and teaches you how to verify and re-prompt safely.",
    "category": "AI Education",
    "date": "2026-03-18"
}
