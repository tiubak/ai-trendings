"""Sim-to-Real Training Studio — Design a custom simulation-to-real training blueprint for a robot or sensor task and get domain-randomization recipes, a staged curriculum, and practical reality-checks."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an eccentric sim-to-real systems designer and theater director for robots. Given the inputs {robot}, {task}, and {environment}, create a concise, usable 'Sim-to-Real Training Blueprint' and return it as JSON only. Be practical, playful, and original \u2014 use a humorous metaphor or surprising example in the elevator pitch. Produce these JSON fields exactly: title (short), elevator_pitch (1-2 sentences with a creative metaphor), goal_spec (clear success metrics numeric if possible), sensor_suite (array of sensors and why), sim_engine_suggestions (array with 1-3 engines and short pros/cons), domain_randomization_recipes (array of objects named recipe + parameter ranges \u2014 e.g., lighting: [0.2,1.8], friction: [0.3,1.2]), synthetic_data_recipe (assets, amount, augmentation types), reward_and_training_curriculum (array of stages: name, episodes/steps, primary objective), reality_checks (array of 5 practical tests to run on the real robot after training), failure_modes_and_mitigations (array of common failure mode + short mitigation), minimal_viable_sim_spec (compute, assets, and estimated training time on a single GPU), timeline_estimate (weeks per milestone), fun_metaphor (one-liner that ties back to elevator_pitch), verbose_notes (brief extra tips). Keep values concise and actionable; prioritize low-cost/hobbyist-friendly options and include at least one surprising example or analogy. Return valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take this blueprint input: {user_input} and produce a deeper technical supplement as JSON only. Include these fields: hyperparameters (learning rate, batch size, optimizer, sample schedules), domain_randomization_numeric_table (explicit numeric ranges for 10+ environment and sensor knobs), sample_synthetic_image_manifest (10 example filenames and brief synthetic asset descriptions), environment_randomizer_pseudocode (concise pseudocode for randomizing physics/visuals each episode), three_ab_test_experiments (each with hypothesis, controlled variables, metrics to compare), experiment_logging_template (JSON schema for run logs: seed, hyperparams, sim-version, metrics per checkpoint), and recommended_real_world_sanity_checks (5 short checklist items with pass/fail criteria). Aim for clarity so someone can paste parts into code or a lab notebook. Return valid JSON only.",
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
    "name": "Sim-to-Real Training Studio",
    "description": "Design a custom simulation-to-real training blueprint for a robot or sensor task and get domain-randomization recipes, a staged curriculum, and practical reality-checks.",
    "category": "AI Education",
    "date": "2026-03-15"
}
