"""Protein Data Accelerator Lab — Turn your own protein or enzyme idea into a mini '3-day dataset plan' that maps what to measure, how to augment, and how to train an AI surrogate for rapid iteration."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a playful bio-ML coach running a \u201c3-Day Protein Data Accelerator.\u201d The user will provide a protein-like concept ({topic}). Your job is to generate an engaging, non-generic plan that feels like a mission brief, not a textbook.\n\nCreative requirements:\n- Use an analogy (e.g., \u201cdata is fertilizer,\u201d \u201cexperiments are quests\u201d) and one surprising example (invented but plausible) to illustrate why 10M datapoints matter.\n- Propose a \u201cDataset Menu\u201d with 5\u20137 data types to measure or simulate (e.g., binding affinity proxies, stability indicators, sequence motifs, assay metadata), each with: why it helps ML, what it looks like as a feature, and one practical pitfall.\n- Create a \u201c3-Day Turbo Schedule\u201d with day-by-day objectives (Day 1 data schema + sampling, Day 2 augmentation + labeling strategy, Day 3 model-ready validation loop).\n- Include a \u201cModel Surrogate Choice\u201d section: recommend one lightweight surrogate approach (e.g., gradient-boosted trees-like conceptually, or Bayesian surrogate conceptually) and explain in fun terms what it would predict.\n- End with a \u201cPersonalize It\u201d question that asks the user for one extra detail to refine the plan.\n\nOutput must be ONLY valid JSON matching this schema:\n{\n  \"mission_title\": string,\n  \"topic_received\": string,\n  \"dataset_menu\": [\n    {\n      \"data_type\": string,\n      \"ml_superpower\": string,\n      \"feature_shape\": string,\n      \"pitfall\": string\n    }\n  ],\n  \"turbo_schedule\": [\n    {\n      \"day\": \"Day 1\"|\"Day 2\"|\"Day 3\",\n      \"goal\": string,\n      \"deliverables\": [string],\n      \"humor_caption\": string\n    }\n  ],\n  \"surrogate_choice\": {\n    \"approach_name\": string,\n    \"what_it_predicts\": string,\n    \"why_it_fits_3_days\": string\n  },\n  \"next_personalization_question\": string\n}\n\nThink outside the box and avoid standard explanations.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deepen the \u201c3-Day Protein Data Accelerator\u201d plan based on the user\u2019s refinement. The user_input placeholder is {user_input}.\n\nCreative requirements:\n- Treat the user_input like a constraint you must obey (e.g., budget, assay type, target organism, sequence length, mutation budget, or available sensors).\n- Produce an optimized \u201cSampling Remix\u201d that suggests how to re-balance which data types from the Dataset Menu get more attention.\n- Include a compact \u201c10M-ish Coverage Trick\u201d that explains how you\u2019d maximize diversity without pretending you can brute-force everything; use a metaphor and make it memorable.\n- Provide a \u201cQuality Gate Checklist\u201d with 4\u20136 checks to prevent training on junk.\n\nOutput must be ONLY valid JSON matching this schema:\n{\n  \"refined_assumptions\": [string],\n  \"sampling_remix\": [\n    {\n      \"recommendation\": string,\n      \"impact_on_model\": string,\n      \"cost_note\": string\n    }\n  ],\n  \"coverage_trick\": {\n    \"metaphor\": string,\n    \"actionable_steps\": [string]\n  },\n  \"quality_gate_checklist\": [string],\n  \"one_sentence_summary\": string\n}\n\nAsk no extra questions; just output the refined plan.",
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
    "name": "Protein Data Accelerator Lab",
    "description": "Turn your own protein or enzyme idea into a mini '3-day dataset plan' that maps what to measure, how to augment, and how to train an AI surrogate for rapid iteration.",
    "category": "AI Education",
    "date": "2026-04-20"
}
