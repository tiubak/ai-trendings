"""Model Training Ops Lab — Enter a training scenario to get an educational simulated monitoring dashboard, failure analysis, and step-by-step debugging guidance."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an educational AI assistant. Create a concise beginner-to-intermediate guide about model training monitoring and debugging focused on the topic: {topic}. Return JSON only with these fields:\n- title: short string title\n- summary: 2-3 sentence overview of why monitoring and debugging matters for {topic}\n- key_concepts: array of objects {\"name\": string, \"description\": short string} covering at least 6 concepts (e.g., metrics, drift, alerts, logging, reproducibility, resource monitoring)\n- example_dashboard: object with two keys: \"metrics\" (object mapping metric name to one-line explanation) and \"alert_rules\" (array of objects {\"name\", \"condition\", \"severity\",\"recommended_action\"})\n- common_failure_modes: array of objects {\"name\",\"symptoms\",\"likely_causes\",\"first_steps_to_investigate\"}\n- debugging_checklist: array of short actionable steps (ordered) to triage model training problems\n- mini_exercises: array of objects {\"exercise\",\"goal\",\"steps\",\"expected_result\"} (3 exercises for hands-on practice)\n- recommended_tools_and_reading: array of short strings listing tools, docs, or articles (include monitoring/debugging tools and one mention of \"Neptune\" or similar)\nKeep entries concise, practical, and educational. Return valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "You are an educational diagnostics assistant. Using the training scenario details provided as {user_input}, simulate a single training run report and produce focused debugging guidance. Return JSON only with these fields:\n- scenario_brief: one-line summary of the scenario you are analyzing\n- assumptions: array of strings listing any assumed defaults (optimizer, batch size, dataset size if not provided)\n- epoch_summary: array of objects for 5-12 epochs with keys {\"epoch\": int, \"train_loss\": number, \"val_loss\": number, \"train_acc\": number|null, \"val_acc\": number|null, \"lr\": number, \"throughput_samples_per_sec\": number, \"notes\": short string}\n- alerts_triggered: array of objects {\"alert\": string, \"epoch\": int, \"description\": string, \"severity\": \"low|medium|high\"}\n- root_cause_hypotheses: array of objects {\"hypothesis\": string, \"evidence_support\": string, \"confidence_0_1\": number}\n- recommended_actions: array of objects {\"action\": string, \"estimated_time_hours\": number, \"impact_on_metrics\": string}\n- suggested_hyperparameter_changes: array of objects {\"param\": string, \"from\": string|number, \"to\": string|number, \"rationale\": string}\n- what_to_test_next: array of short test objects {\"test\": string, \"purpose\": string, \"expected_outcome\": string}\n- explain_like_im5: one-sentence plain-language explanation of the main issue and next step\nBase your simulation on the specifics in {user_input}, fill gaps with reasonable defaults, and keep outputs concise and actionable. Return valid JSON only.",
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
    "name": "Model Training Ops Lab",
    "description": "Enter a training scenario to get an educational simulated monitoring dashboard, failure analysis, and step-by-step debugging guidance.",
    "category": "AI Education",
    "date": "2026-02-24"
}
