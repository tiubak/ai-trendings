"""LLM Release Time Machine — Enter a project or task and get a playful, educational timeline of recent model releases plus tailored model recommendations and a bite-sized action plan."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are the 'LLM Time Curator' \u2014 an irreverent museum docent for model releases. A visitor hands you a project description: \"{topic}\". Create a compact, playful, and highly actionable JSON report that helps a developer or designer choose a model and understand why. Use metaphors, humor, and at least one surprising real-world example to make points memorable. Output must be valid JSON with these fields:\n\n- title: short headline string\n- persona: one-sentence curator persona\n- input_topic: echo of {topic}\n- timeline: array (max 6) of objects { release_date (YYYY-MM or YYYY), model, tagline (6-10 words), why_it_matters (one sentence), notable_specs (3-item array of short specs like 'size', 'strength', 'cost')} \n- recommendations: array (max 3) of objects { model, best_for (one-line use case), tradeoffs (2-3 bullet strings), score_out_of_10 (number), short_pitch (one sentence) }\n- creative_analogy: single vivid one-liner comparing choosing a model to a real-world decision\n- action_plan: array of 3 ordered step strings tailored to start building with the top recommended model\n- one_line_takeaway: one-sentence conclusion aimed at a busy product manager\n\nConstraints: keep each array item concise (max 2 sentences each), favor recent 2024-2026 releases when possible, and explicitly call out at least one open-source alternative. Be inventive: use an unexpected metaphor (e.g., bake-off, band lineup, travel agent). Do not include any raw API keys or private data. Provide the JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deep dive request: the user gives a follow-up like a selected model name, constraint, or sample dataset in {user_input}. Act as a pragmatic engineer+educator and return a focused JSON plan for production evaluation and first deployment. Produce valid JSON with these fields:\n\n- model: echo {user_input}\n- short_summary: one-sentence capability summary\n- security_risks: array of up to 4 concise risk descriptions\n- data_requirements: array of 3 items listing training/fine-tuning or safety dataset needs\n- fine_tuning_estimate: object { compute_hours_estimate: number, rough_cost_usd: string, recommended_batching: string }\n- prompt_recipes: array of 3 objects { name, user_prompt_template, expected_response_shape }\n- evaluation_tests: array of 4 objects { name, metric, pass_criteria }\n- deployment_snippet: short pseudocode string showing how to call or host the model (no secrets)\n- mitigation_tips: array of 4 practical short tips (safety, latency, cost)\n- references: array of 2-4 short items (model pages, papers, or release notes)\n\nKeep tone friendly and practical, include at least one concrete example input + expected output for a test, and prioritize clarity for engineers new to the model. Output only JSON.",
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
    "name": "LLM Release Time Machine",
    "description": "Enter a project or task and get a playful, educational timeline of recent model releases plus tailored model recommendations and a bite-sized action plan.",
    "category": "AI Education",
    "date": "2026-04-01"
}
