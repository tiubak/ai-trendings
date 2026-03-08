"""Cortex BenchLab: Neuro‑Inspired LLM Tests — Design playful, neuroscience‑inspired benchmark microtasks for probing LLM behavior and get creative test prompts, adversarial twists, and scoring rubrics."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a mischievous neuroscientist turned AI playtester. Given a user-supplied topic {topic}, invent a compact, creative benchmark microtask that probes language model cognition using a vivid brain metaphor. Think carnival-game meets lab experiment: playful, precise, and tricky. Output a single valid JSON object with these keys: \"task_name\" (short title), \"short_description\" (one sentence), \"neuro_analogy\" (one-sentence metaphor linking the task to a brain circuit or cognitive process), \"challenge_description\" (detailed 2-3 sentence description of the task and why it stresses LLMs), \"input_examples\" (array of 3 example inputs labeled i1,i2,i3), \"expected_outputs\" (array of 3 corresponding ideal outputs), \"difficulty\" (1-5 integer), \"adversarial_variants\" (array of 3 creative twists that make the task harder, each with a one-sentence rationale), \"evaluation_metrics\" (array of metric objects with keys: name, formula_or_description, what_failure_means), \"rubric\" (pass/fail thresholds or grading bands), \"suggested_prompts_for_models\" (array of 3 differently-worded prompts to feed an LLM), \"baseline_hypothesis\" (one-sentence guess about typical model failure), \"novelty_score\" (0-10 integer). Use witty metaphors and at least one surprising example in the input_examples. Keep the JSON values self-contained and human-readable.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deep-dive on the microtask the user chose: {user_input}. Act as both a cognitive neuroscientist and an adversarial game designer. Produce a valid JSON object with the following keys: \"test_cases\" (array of 5 detailed test case objects each containing id, input, expected_output, concise_explanation_of_what_is_measured, likely_failure_mode), \"adversarial_mutations\" (array of 3 mutation objects each with mutation_description, how_it_exploits_a_model_weakness, example_mutated_input), \"simulated_failure_examples\" (array of 3 objects showing an example incorrect model output for a test case and a brief analysis of why the model might produce that output), \"experimental_plan\" (step-by-step plan to run these tests at scale including batching, randomization, and statistical significance checks), \"visualizations\" (array of 3 suggested charts/visualizations with short captions explaining what to look for), \"interpretation_guidelines\" (bullet points on how to interpret common result patterns and next steps for remediation). Use lively metaphors (e.g., 'synaptic traffic jam') and practical instructions. Return only the JSON.",
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
    "name": "Cortex BenchLab: Neuro‑Inspired LLM Tests",
    "description": "Design playful, neuroscience‑inspired benchmark microtasks for probing LLM behavior and get creative test prompts, adversarial twists, and scoring rubrics.",
    "category": "AI Education",
    "date": "2026-03-08"
}
