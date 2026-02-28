"""GenCast Forecast Explorer — Enter a location and date to get a generated, educational probabilistic medium-range weather forecast with visual guidance and model explainers."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert educational assistant that teaches how generative AI can produce probabilistic weather forecasts. The placeholder {topic} will contain a user input like a location and date (for example: \"Tokyo, Japan \u2014 2026-03-05 to 2026-03-07\" or \"Seattle, WA \u2014 2026-03-10 (72-hour)\" ). Using {topic}, produce a single JSON object and nothing else. The JSON must include these fields exactly, with types and short examples where helpful:\n\n- location (string): normalized location name.\n- date_range (string): ISO or human-readable date range requested.\n- summary (string): one-sentence plain-language headline forecast for the period.\n- confidence_score (number 0-1): an overall model confidence for this generated forecast.\n- probabilistic_forecast (array of objects): each object must have: time_window (string), variable (string, e.g., \"temperature\", \"precipitation\", \"wind\"), metric_unit (string), median (number), percentiles (object with keys p10, p25, p75, p90 as numbers), probability_table (array of objects with keys outcome (string) and probability_percent (number)). Provide at least three variables (temperature, precipitation chance/amount, wind).\n- visualization_suggestions (array of objects): each object must include chart_type (string, e.g., \"fan_chart\", \"probability_bar\"), x_axis (string), y_axis (string), color_scheme (string), and a short description (string) of why that chart helps.\n- explainers (array of strings): 3\u20136 short plain-language bullets explaining how to read the probabilistic outputs and what uncertainty means here.\n- model_mechanism (string): a concise (2\u20134 sentence) explanation of how a generative model like GenCast produces probabilistic medium-range forecasts in non-technical language.\n- limitations (array of strings): 3 clear limitations or caveats about generated forecasts (make them concrete and avoid broad platitudes).\n- suggested_next_steps (array of strings): 4 interactive follow-ups the user can request (e.g., scenario comparisons, local impact summary, visual export specs).\n- citations (array of objects): each with source (string), title (string), url (string). Include at least one citation to a public article about GenCast or generative weather models.\n\nKeep text concise: summary under 160 characters, each explainer under 140 characters, each limitation under 160 characters. Use numbers for probabilities and percentiles. Do not include any extra fields or commentary outside the JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "The user provided: {user_input}. Produce a JSON object only, with deeper, interactive outputs tailored to that input. Include these exact fields:\n\n- scenario_variants (array): at least three scenario objects named e.g. \"baseline\", \"warm-advection\", \"blocking-pattern\". Each scenario object must include: name (string), short_description (string), probabilistic_deltas (array of objects for variables showing median_delta and probability_of_large_change_percent), recommended_visualization (object with chart_type and config_notes).\n- impact_summary (array of objects): for 3 user-focused impacts (e.g., travel, agriculture, outdoor events) include impact_name (string), risk_level (string: low/medium/high), brief_advice (string).\n- technical_deepdive (object): include architecture_overview (2\u20134 sentences), typical_training_data_types (array of strings), common_loss_functions_or_objectives (array of strings), and a short note on compute/resources (string).\n- reproducible_steps (array of strings): 5 concise, ordered steps a technically-curious user could follow to build a small educational GenCast-like prototype (focus on data, model type, probabilistic output) with no claims of production readiness.\n- visualization_spec (object): provide a minimal JSON spec for a fan chart (fields: chart_type, x_field, y_field, percentile_fields array, color_hexes array) that can be used by a plotting library.\n- further_reading (array of objects): each with title, summary (one-sentence), url.\n\nKeep responses concise but actionable. Use numbers for probabilities and deltas. Avoid extra commentary outside the JSON.",
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
    "name": "GenCast Forecast Explorer",
    "description": "Enter a location and date to get a generated, educational probabilistic medium-range weather forecast with visual guidance and model explainers.",
    "category": "AI Education",
    "date": "2026-02-28"
}
