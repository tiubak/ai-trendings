"""BrainScan AI Lab — Interactively explore how AI models infer biological sex from brain scans—learn methods, spot dataset confounds, run interpretability exercises, and design ethical experiments."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert educator in machine learning and neuroscience. Produce an educational, interactive briefing about the research topic or claim provided as: \"{topic}\" (for example: \"AI determines sex from brain scans\"). Return only a single JSON object with exactly the fields listed below and no extra commentary. Field list and expected types: \n\n- title (string): a concise headline for this briefing.\n- plain_summary (string): a 2-4 sentence non-technical summary of the claim and why it matters.\n- how_models_work (string): an accessible explanation of typical ML approaches used for this claim (models, inputs, preprocessing, common architectures), written as short paragraphs or numbered steps.\n- typical_datasets (array of objects): each object {\"name\":string, \"description\":string, \"size_examples\":string} describing common dataset types used.\n- common_confounders (array of strings): concise list of likely confounds or biases that can cause spurious results.\n- demo_exercise (object): {\"goal\":string, \"required_packages\": [strings], \"steps\": [strings], \"sample_code\": string} describing a short hands-on experiment a learner can run locally or in a notebook to reproduce a simplified test.\n- interpretability_exercises (array of objects): each {\"name\":string, \"steps\": [strings], \"expected_insight\":string} describing specific interpretability analyses (e.g., saliency, feature-ablation, demographic-conditioned analysis).\n- ethical_risks (array of objects): each {\"risk\":string, \"mitigation\":string} pairing an identified harm with practical mitigations or controls.\n- classroom_quiz (array of objects): each {\"question\":string, \"options\":[strings], \"correct_index\":integer, \"explanation\":string} with three short multiple-choice questions.\n- further_reading (array of objects): each {\"title\":string, \"url\":string} with 3 suggested readings or resources.\n- estimated_time_minutes (integer): approximate time to work through the briefing and demo.\n\nKeep answers concise but concrete. Use code in the sample_code field that is runnable pseudocode or minimal Python (numpy/torch/sklearn style) and under 25 lines. Do not include any other fields or prose outside the JSON object.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take this follow-up input from the user: \"{user_input}\". Provide a focused JSON reply with only the fields below and no additional text. Tailor recommendations and steps to the user's input. Required output fields and expected types:\n\n- refined_question (string): a one-sentence restatement of the user's goal or research question.\n- detailed_analysis (string): a concise, technical analysis of the key issues or mechanisms relevant to the input (3-6 short paragraphs or bullet-like text).\n- experimental_plan (object): {\"objective\":string, \"data_needed\": [strings], \"controls\": [strings], \"model_choices\": [strings], \"metrics\": [strings], \"step_by_step\": [strings]} giving a reproducible plan.\n- code_snippets (array of objects): each {\"name\":string, \"language\":string, \"code\":string} with short runnable examples or templates (max 40 lines each).\n- visualization_plan (array of objects): each {\"plot_type\":string, \"purpose\":string, \"data_required\":string} describing specific plots to run and what they reveal.\n- risk_mitigation (array of objects): each {\"risk\":string, \"practical_controls\": [strings]} focused on ethical, privacy, and misuse risks tied to the experiment.\n- expected_outcomes (array of strings): plausible results and how to interpret them, including what would indicate a confound vs a real signal.\n- references (array of objects): each {\"title\":string, \"url\":string} with 3-6 citations or links for deeper reading.\n- estimated_time_minutes (integer): time estimate for executing the experimental plan.\n\nDo not output additional fields. Keep code short and clearly labeled by language. Ensure all advice is actionable and specific to the user's input.",
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
    "name": "BrainScan AI Lab",
    "description": "Interactively explore how AI models infer biological sex from brain scans—learn methods, spot dataset confounds, run interpretability exercises, and design ethical experiments.",
    "category": "AI Education",
    "date": "2026-03-03"
}
