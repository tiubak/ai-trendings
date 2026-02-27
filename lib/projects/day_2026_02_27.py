"""AI Language Accessibility Lab — Try sample prompts at different English proficiency and formality levels to see how LLMs may perform, get rewrites, explanations and teaching exercises."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are building an interactive educational module about {topic}. Produce a JSON object only, no extra text, with these fields: \n- title: short title string\n- learning_objectives: array of 3-6 concise objectives (each a string)\n- summary: one-paragraph plain-language summary explaining the issue and why it matters for users and developers\n- evidence_summary: 3 bullet strings summarizing key findings from research (cite 'MIT Center for Constructive Communication' where relevant)\n- example_user_inputs: array of three objects showing simulated user prompts at different English proficiency levels; each object must have {\"id\",\"proficiency_label\",\"text\"}\n- expected_model_behavior: array of three objects matching example_user_inputs by id with {\"id\",\"likely_issues\":[strings],\"expected_quality_rating\":number} where rating is 0-10\n- classroom_exercises: array of 3 short interactive exercises teachers/developers can run with learners (strings)\n- demo_instructions: an object with {\"setup_steps\": [strings], \"how_to_run\": [strings], \"what_to_observe\": [strings]}\n- ui_payload: an object with {\"sample_scoring_function\": string describing a simple algorithm to estimate model robustness to nonstandard English, \"example_output_schema\": object that the web UI can expect when evaluating user input}\nReturn only valid JSON. Tailor content to be practical for an educator or developer introducing model fairness and robustness with live demos.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Analyze this user text: {user_input}. Return only JSON with the following fields: \n- original: the raw input string\n- proficiency_estimate: one of {\"low\",\"intermediate\",\"high\"} with a short justification string\n- common_challenges: array of strings describing linguistic issues (e.g., grammar, ambiguity, brevity, idioms)\n- suggested_rewrites: array of three objects for levels {\"clarified_simple\",\"neutral\",\"precise_formal\"}; each object must include {\"label\",\"rewritten_text\",\"goals\"}\n- predicted_model_responses: array with one object per rewrite containing {\"label\",\"simulated_response_snippet\":string (approx 1-2 sentences),\"confidence_estimate\":0-100}\n- robustness_score: number 0-100 estimating how robust a typical large language model might be to the original input, with a brief numeric rationale field\n- pedagogical_tips: array of 3 short actionable teaching tips for improving model-user interaction or collecting better datasets\n- citations: array with at least one string mentioning 'MIT Center for Constructive Communication' and the general finding about performance variation by English proficiency\nReturn only JSON. Do not include any commentary or extra text.",
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
    "name": "AI Language Accessibility Lab",
    "description": "Try sample prompts at different English proficiency and formality levels to see how LLMs may perform, get rewrites, explanations and teaching exercises.",
    "category": "AI Education",
    "date": "2026-02-27"
}
