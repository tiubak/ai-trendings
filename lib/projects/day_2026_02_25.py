"""Token-Adaptive Quantization Playground — Explore and experiment with token-adaptive quantization strategies for elastic LLMs—get tailored explanations, code snippets, trade-off analysis, and a hands-on tuning plan."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert ML engineer teaching token-adaptive quantization. Generate a JSON document about {topic} that educates a practitioner who knows basic neural nets but is new to token-adaptive/mixture-of-bits quantization. Include the exact fields below and no extra top-level keys:\n\n- topic_title: short title\n- audience: one-line description of intended audience\n- difficulty_level: choose from [Beginner, Intermediate, Advanced]\n- estimated_read_time_min: integer\n- topic_summary: 3-5 sentence summary of the idea behind token-adaptive/mixture-of-bits quantization and why it matters for elastic LLMs\n- key_concepts: array of objects with {name, one_sentence_definition}\n- how_it_works_steps: ordered array of step objects {step_number, title, details} describing the mechanism at a technical but practical level\n- toy_example: object with {input_prompt, token_sequence_example, chosen_bitwidths_per_token, reasoning, pseudo_code_snippet} showing a minimal illustrative example\n- simple_python_snippet: a short ready-to-run Python pseudocode example demonstrating per-token bit assignment and a quantize()/dequantize() mock\n- recommended_settings: object mapping device_profiles (e.g., 'edge-low-memory','gpu-server') to recommended bitmix strategies and expected speed/size tradeoffs\n- tradeoffs: array of strings listing practical tradeoffs and common pitfalls\n- visuals: array of visualization suggestions (each {name, description, x_axis, y_axis}) that a beginner could implement to illustrate behavior\n- quick_quiz: array of up to 3 short Q/A pairs to test comprehension, each {question, answer}\n- further_reading: array of high-quality links or citations (title + URL)\n\nTailor explanations so someone can move from conceptual understanding to a small experiment. Keep JSON values concise but informative.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the user's input {user_input} and produce a JSON experimental plan that deepens exploration of token-adaptive quantization for that specific scenario. Return only the following fields:\n\n- scenario: echo of {user_input}\n- goal: one-sentence measurable objective (e.g., 'reduce memory by X% while keeping perplexity delta < Y')\n- baseline_setup: concise description of baseline model, dataset, and metrics to measure\n- proposed_quant_strategy: detailed specification of bit allocations or policy (per-token heuristics, attention-aware rules, gating network, or per-layer rules), with pseudo-parameters\n- experiment_steps: ordered array of steps {step_number, action, commands_or_pseudocode, expected_observation}\n- metrics_to_track: array of metric names and how to compute them (e.g., latency_p95, throughput_tokens_per_sec, memory_peak, validation_loss, downstream_accuracy)\n- synthetic_results_estimate: conservative expected ranges for key metrics after quantization (explain assumptions)\n- visualization_plan: 3 plots to produce (each {title, x, y, interpretation_guideline})\n- failure_modes_and_mitigation: array of likely problems and concise mitigations\n- next_actions: prioritized checklist for a developer to run in the next 48 hours\n\nMake the output actionable and specific to the scenario described in {user_input}. Provide concise pseudocode or shell commands where helpful. Return valid JSON only.",
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
    "name": "Token-Adaptive Quantization Playground",
    "description": "Explore and experiment with token-adaptive quantization strategies for elastic LLMs—get tailored explanations, code snippets, trade-off analysis, and a hands-on tuning plan.",
    "category": "AI Education",
    "date": "2026-02-25"
}
