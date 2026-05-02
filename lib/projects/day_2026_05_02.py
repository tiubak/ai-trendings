"""AI Water Usage Dial: Make the Invisible Metric Visible — Users enter an AI workflow and see a playful, explainable estimate of potential water impact—then iterate with “green” alternatives to minimize it."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Imagine you\u2019re building a mini \u2018water budget\u2019 game for AI: Given a user\u2019s described workload {topic}, generate a personalized, creative response that estimates potential water impact and explains it with an analogy people remember. Use a framework called \u201cTHE SPOON TEST\u201d: how many \u2018spoons of water\u2019 the workload might consume depending on (1) model size/endpoint type, (2) how often prompts run, (3) output length, (4) whether results are cached, (5) batch vs real-time, and (6) retry behavior. \n\nRequirements:\n- First ask 3 quick clarifying questions the user can optionally answer, but still produce a best-effort estimate using defaults if they don\u2019t. Keep the tone witty and non-preachy.\n- Provide outputs in JSON only, with fields: {\"estimate_waterspoons\": number, \"range\": \"low|mid|high\", \"assumptions\": [strings], \"knobs\": [{\"name\": string, \"effect\": \"reduce|neutral|increase\", \"reason\": string}], \"green_alternatives\": [strings], \"one_line_metaphor\": string, \"explain_like_im_12\": string}.\n- Make the explanation feel like: \u2018AI is a factory that sometimes runs its cooling systems through rivers.\u2019 Include a surprising example (e.g., \u2018a chatbot on autopilot\u2019 vs \u2018a chatbot that only calls the model when needed\u2019).\n- Use the placeholder {topic} in the text so the user input is reflected.\n- Think outside the box: include at least one \u2018ethical\u2019 lens without getting political\u2014focus on informed tradeoffs and transparency.\n- Return ONLY valid JSON and nothing else.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now deepen the simulation for user {user_input}. Output JSON only with: {\"scenario\": string, \"water_dials\": [{\"dial\": string, \"current_setting\": string, \"suggested_setting\": string, \"expected_shift\": string}], \"strategy_plan\": [{\"step\": number, \"action\": string, \"why_it_matters\": string}], \"tradeoffs\": [{\"tradeoff\": string, \"impact\": string}], \"questions_for_user\": [string], \"final_summary\": string}. \n\nConstraints:\n- Use a \u2018choose-your-own-cost\u2019 narrative: present 2 distinct paths (e.g., \u201cSpeedy Stream\u201d vs \u201cBatch & Cache\u201d), each with a different water-performance profile.\n- Keep all numbers qualitative except one water estimate bucket label: {\"low\",\"mid\",\"high\"}.\n- Must incorporate at least one knob related to caching/retries and one related to output length or frequency.\n- Be creative and specific to {user_input} (e.g., if they say customer support bot, tailor dials to tickets; if they say research summarizer, tailor to batch runs).",
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
    "name": "AI Water Usage Dial: Make the Invisible Metric Visible",
    "description": "Users enter an AI workflow and see a playful, explainable estimate of potential water impact—then iterate with “green” alternatives to minimize it.",
    "category": "AI Education",
    "date": "2026-05-02"
}
