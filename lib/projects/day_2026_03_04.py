"""Parallel Research Engine Designer — Design and compare specialized AI research engines for a chosen domain and get tailored architectures, training plans, cost estimates, and safety guidance."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert AI systems architect and educator. The user will supply a research domain or topic in the placeholder {topic} (for example: 'drug discovery', 'real-time video analysis', 'financial forecasting', 'multimodal social research'). Produce a single JSON object and nothing else. Do not include explanatory text outside the JSON. The JSON must include the following fields:\n\n- title (string): a concise project title for the set of engines.\n- description (string): one-sentence description of the goal tailored to {topic}.\n- target_audience (string): who this learning project is for.\n- suggested_engines (array): 3 to 5 engine objects. Each engine object must contain: name (string), purpose (one sentence), architecture_overview (short paragraph), core_components (array of strings), compute_estimate (string; e.g., approximate GPU-hours and cost tiers), datasets (array of dataset descriptions or synthetic dataset ideas), evaluation_metrics (array of strings), safety_considerations (array of short items), tradeoffs (array of strings explaining design tradeoffs), learning_exercises (array of 2-4 short hands-on tasks with expected learning outcome).\n- recommended_learning_path (array): ordered steps learners should follow to build and study these engines.\n- interactive_experiments (array): 3 suggested experiments learners can run (each with name, objective, quick method, expected observations).\n- references (array): 3-6 URLs or citations for deeper reading.\n\nTailor all outputs to the domain {topic}. Keep descriptions concise and educational. Return only valid JSON that follows this schema.",
        "parse": "json"
    },
    "explore": {
        "prompt": "The user provides {user_input}. This could be the name of one suggested engine from the previous output, or a constraint such as 'low-cost prototype', 'safety-first', 'real-time <X> latency', or a request for expansion like 'detailed training plan'. Acting as an AI systems architect and instructor, return a single JSON object and nothing else. The JSON must include these fields:\n\n- engine_name (string): the selected engine or topic of expansion.\n- detailed_architecture (object) with fields: model_type (string), model_sizes (suggested parameter ranges), module_breakdown (array of module objects each with name and responsibilities), data_flow_description (short text explaining inputs/outputs), and dependencies (list of libraries/frameworks).\n- training_pipeline (array): ordered steps with each step as an object containing name, description, estimated_time, and required_resources.\n- infrastructure_and_ops (object): recommended infra components (compute, storage, network), deployment pattern, monitoring & logging checklist, and backup/replication notes.\n- cost_and_time_estimate (object): coarse estimates broken down by development, training, and serving costs and timelines (use ranges and assumptions).\n- safety_and_governance (array): explicit mitigations, tests, and policy checks to run (including data handling, adversarial tests, and prompt safeguards if applicable).\n- code_snippets (array): up to 4 short, language-agnostic pseudocode or CLI snippets illustrating key steps (data prep, training launch, eval command, or deploy command).\n- milestone_plan (array): 4-6 timeboxed milestones with success criteria.\n- educational_exercises (array): 3-5 lab-style exercises learners can complete to internalize the design decisions.\n- justification (string): concise rationale tying design choices to constraints in {user_input}.\n\nBe explicit about assumptions you make about scale, budget, and expertise; state them in the justification. Return only valid JSON that follows this schema.",
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
    "name": "Parallel Research Engine Designer",
    "description": "Design and compare specialized AI research engines for a chosen domain and get tailored architectures, training plans, cost estimates, and safety guidance.",
    "category": "AI Education",
    "date": "2026-03-04"
}
