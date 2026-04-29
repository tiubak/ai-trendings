"""DeepSeek Resource Optimizer Lab — Enter your ML budget constraints and get a personalized “resource plan” that balances software efficiency, model choices, and deployment strategy—powered by an optimizer game inspired by DeepSeek’s software-first approach."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are designing an interactive \u201cAI Efficiency Heist\u201d that teaches resource optimization through decision-making.\n\nUser will provide: {topic}. Your job is to generate a playful, highly original content package that helps them plan a software-first strategy inspired by DeepSeek\u2019s resource optimization.\n\nDo NOT give a generic overview. Instead:\n1) Create a metaphor: liken optimization to stealing back minutes/battery/compute from a greedy system (choose one: vending machine, subway turnstiles, or movie theater line).\n2) Ask the user to act as the \u201coptimizer\u201d and draft a plan using 5 knobs (must be named creatively): {Knob1}, {Knob2}, {Knob3}, {Knob4}, {Knob5}\u2014each knob should correspond to a real technical lever (e.g., data pipeline efficiency, training schedule, quantization, routing/sparsity, caching/batching, distillation, eval-driven iteration).\n3) Include a \u201cconstraint trap\u201d mini-quiz: present 4 short scenarios and ask which choice is best under the user\u2019s constraints.\n4) Output a final \u201cResource Loot Manifest\u201d checklist with 8\u201312 bullet items that explicitly connect each bullet to one of the 5 knobs.\n5) Provide a \u201csuccess metric\u201d section with at least 3 metrics and how they would be measured.\n\nImportant: Output MUST be valid JSON with keys: title, metaphor, knob_guide (array of 5 objects: name, what_it_controls, why_it_matters, example_decision), constraint_trap (array of 4 objects: scenario, choices[3], correct_choice_explanation), loot_manifest (array of strings), success_metrics (array of objects: metric, what_to_measure, how_to_check_fast), and a short closing line.\n\nThink outside the box and make it memorable\u2014use humor, but keep technical mapping accurate to real optimization levers.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Continue the AI Efficiency Heist with deeper personalization.\n\nUser previously entered: {user_input}.\nGenerate an additional JSON output that refines the plan by asking targeted follow-up questions and generating an updated blueprint.\n\nRequirements:\n- Output MUST be valid JSON with keys: assumptions, follow_up_questions (array of 5 objects: question, why_it_matters), updated_blueprint (array of 6 objects: step, lever, tradeoff, expected_impact, risk), and a \u201c10-minute experiment\u201d (array of 3 objects: experiment_name, goal, exact_measurement_to_report).\n- The updated blueprint must explicitly reference at least 3 of the 5 optimization knobs by name (use consistent naming from the prior response if present; otherwise propose them and keep names stable inside this response).\n- Keep it concrete: mention batching/caching/quantization/distillation/evaluation cadence at least once across the steps.\n- Be specific about constraints: latency, cost per request, or memory/VRAM.\n\nReturn only the JSON object.",
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
    "name": "DeepSeek Resource Optimizer Lab",
    "description": "Enter your ML budget constraints and get a personalized “resource plan” that balances software efficiency, model choices, and deployment strategy—powered by an optimizer game inspired by DeepSeek’s software-first approach.",
    "category": "AI Education",
    "date": "2026-04-29"
}
