"""One-Night Sleep Lab — Interactively explore how AI research can infer future disease risk from a single night of sleep through lessons, mini-projects, and a model-design assistant."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "Act as an educational AI module. Generate a single JSON object that teaches users about {topic} tailored to {audience_level} (options: 'beginner','intermediate','advanced'). Output only valid JSON with these exact fields:\n\n- title (string)\n- summary (string): one-paragraph overview\n- key_concepts (array of objects): each {name, explanation}\n- how_it_works (array of objects): each {step, detail}\n- data_requirements (object): {required_signals: array of strings, sample_size_guidelines: string, labeling_recommendations: string, privacy_considerations: array of strings}\n- model_design_outline (object): {input_features: array, suggested_models: array, training_pipeline: array of steps, evaluation_metrics: array}\n- ethics_and_bias (array of objects): each {issue, potential_impact, mitigation_suggestion}\n- limitations (array of strings)\n- hands_on_exercises (array of objects): each {name, goal, steps: array, expected_output}\n- further_reading (array of objects): each {title, url}\n- disclaimer (string): concise non-medical-advice disclaimer\n\nTailor language and depth to {audience_level}: use nontechnical language for 'beginner', include concrete code or equations for 'advanced'. Keep each field concise and actionable. Do not include anything outside this JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the user's input {user_input} \u2014 this can be a short description of a sleep dataset, an idea for a predictive model, or a focused research question \u2014 and produce only JSON with these fields:\n\n- assumptions (array of strings): assumptions inferred from {user_input}\n- analysis (string): concise feasibility assessment and main risks\n- features_to_engineer (array of objects): each {feature_name, rationale, priority}\n- model_recommendation (object): {architecture: string, why: string, complexity_level: 'low'|'medium'|'high'}\n- training_plan (array of steps): including data splits, augmentations, loss choices, and hyperparameter suggestions\n- evaluation_plan (array): metrics and validation strategies with brief justifications\n- privacy_and_consent_steps (array of actionable measures)\n- explainability_methods (array of strings): prioritized interpretability tools and how to apply them\n- simple_demo_code (string): a short illustrative Python snippet (scikit-learn or PyTorch) showing a minimal pipeline tailored to {user_input}\n- next_steps (array of actionable items with estimated time to complete)\n\nIf {user_input} includes a health claim or personal medical data, flag that in 'analysis' and include consultation with domain experts in 'next_steps'. Output only this JSON.",
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
    "name": "One-Night Sleep Lab",
    "description": "Interactively explore how AI research can infer future disease risk from a single night of sleep through lessons, mini-projects, and a model-design assistant.",
    "category": "AI Education",
    "date": "2026-02-26"
}
