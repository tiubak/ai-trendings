"""Visual Asset Localizer Lab — Generate an AI-driven, step-by-step plan to adapt a visual asset for a specific platform and regional market, including models, prompts, workflow and checks."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert AI product designer. The user will supply {topic}, a short description that combines a visual asset and a target platform/market (for example: \"lipstick hero image for Instagram India\" or \"30s product video for US TikTok\"). Using {topic}, generate a single JSON object with the exact fields below. Tailor all recommendations to the asset and target market in {topic}. Return only valid JSON.\n\nRequired fields and formats:\n- title: short string (project title)\n- one_sentence: one-line summary of what to do\n- market_description: 2-3 sentences describing audience, platform constraints, and cultural/format considerations\n- key_challenges: array of short strings (3-6) describing the main technical and creative challenges\n- adaptation_strategies: array of objects; each object must have: {\"strategy_name\":string, \"description\":string, \"when_to_use\":string, \"pros\":string, \"cons\":string}\n- recommended_models_and_tools: array of objects; each object must have: {\"name\":string, \"type\":string (e.g., 'style-transfer','text-to-image','video-edit','super-resolution'), \"why\":string, \"example_usage\":string}\n- sample_prompts_or_config: array of strings with concrete prompt templates or config snippets (include at least one for text-to-image/stylization and one for video reformatting or captioning)\n- end_to_end_workflow: array of step objects in order; each step must have: {\"step_number\":int, \"action\":string, \"tools\":string, \"expected_output\":string}\n- data_and_annotation_requirements: object with keys {\"data_types\":array of strings, \"min_examples\":int, \"labels_needed\":array of strings}\n- estimate_compute_and_cost: object with keys {\"low\":string, \"medium\":string, \"high\":string} describing approximate compute profile and rough cost guidance for small/medium/large scopes\n- quality_checks_and_metrics: array of strings listing practical checks and KPIs to validate localizations\n- ethical_and_regulatory_considerations: array of strings (privacy, cultural sensitivity, copyright, consent items)\n- example_transformed_asset_description: one paragraph describing the final localized asset the user would get\n- references: array of strings (URLs or paper titles)\n\nBe practical, educational and actionable in each field; keep each field concise but concrete. Use the {topic} placeholder values to customize explanations and examples.",
        "parse": "json"
    },
    "explore": {
        "prompt": "This is a deeper exploration step for the user's chosen scenario {user_input} (user_input is the same kind of input as {topic}). Produce a JSON object with these specific fields. Tailor everything to {user_input} and provide actionable artifacts that a small team could use to prototype or evaluate an adaptation system. Return only valid JSON.\n\nRequired fields and formats:\n- fine_tuning_plan: array of ordered step objects {\"step_number\":int, \"goal\":string, \"actions\":array of strings, \"expected_result\":string}\n- dataset_schema: object describing fields and types (e.g., {\"image_url\":\"string\",\"caption\":\"string\",\"region\":\"string\",\"platform\":\"string\",\"label_quality\":\"int\"}) and include a sample of 3 example rows as an array\n- augmentation_recipes: array of objects {\"name\":string, \"purpose\":string, \"parameters\":object} (include at least style-preserve color-shift and layout-cropping recipes)\n- training_hyperparams: object with keys {\"batch_size\":int, \"lr\":float, \"epochs\":int, \"optimizer\":string, \"notes\":string}\n- inference_pipeline: string containing concise pseudo-code or shell/CLI commands showing how to apply models to an input asset and produce outputs for the target platform\n- evaluation_and_ab_testing: object with {\"metrics\":array, \"A/B_design\":string, \"sample_size_guidance\":string}\n- deployment_considerations: array of strings covering latency, format conversions, CDN and regional caching, fallback strategies\n- monitoring_and_feedback_loop: array of objects {\"metric\":string, \"threshold\":string, \"alert_action\":string}\n- sample_prompts_and_negative_examples: object with {\"positive_prompts\":array of strings, \"negative_prompts_or_constraints\":array of strings}\n- estimated_timeline: object with {\"research_prototype_weeks\":int, \"pilot_weeks\":int, \"full_rollout_weeks\":int}\n- resource_estimates: object with {\"gpu_hours\":int, \"storage_gb\":int, \"team_roles\":array}\n- open_source_code_snippets: array of short code strings (max 6) such as a curl command, a small Python snippet for applying a model, or a shell command for FFmpeg reformatting\n\nKeep responses concrete and oriented to implementation, including sample sizes, commands, and measurable thresholds where possible.",
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
    "name": "Visual Asset Localizer Lab",
    "description": "Generate an AI-driven, step-by-step plan to adapt a visual asset for a specific platform and regional market, including models, prompts, workflow and checks.",
    "category": "AI Education",
    "date": "2026-03-01"
}
