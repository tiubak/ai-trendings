"""Chromatic Cue Lab — An interactive lab where users design, simulate, and visualize 'selective color' strategies to learn why video AI often works in grayscale and only needs color at key moments."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an eccentric film director fused with a pragmatic ML researcher. For the scenario described as \"{topic}\", invent a compact, memorable interactive experiment that teaches a newcomer why video AI often doesn't need full-color input and benefits from 'selective color cues'. Think in metaphors (e.g., 'color as stage lighting'), use a pinch of humor, and suggest experiments people can run without heavy infrastructure. Produce a single valid JSON object only, with these keys: \n- title: short catchy experiment title (string)\n- teaser: one-sentence hook (string)\n- hypotheses: array of 2-4 short hypotheses to test (array of strings)\n- experiment_steps: array of step objects {step_number:int, instructions:string, expected_result:string}\n- visualization_prototypes: array of 2-3 short descriptions of visualizations to build (e.g., toggles, before/after frames, confidence heatmaps)\n- sample_prompts: array of 2 model prompts users can run (strings)\n- playful_analogy: a single memorable metaphor linking color use to a real-world scenario (string)\n- estimated_time_minutes: integer\n- difficulty: one of [\"Beginner\",\"Intermediate\",\"Advanced\"]\n- materials: array of required materials or demo assets (strings)\n- code_snippet: a brief pseudocode or CLI pipeline example showing grayscale baseline + selective color toggle (string)\n- notes: one short tip or gotcha (string)\nKeep language concise, witty, and surprising. Output valid JSON only and nothing else.",
        "parse": "json"
    },
    "explore": {
        "prompt": "You are continuing from the interactive experiment JSON the user ran; the user supplies that JSON as {user_input}. Act as a playful lab assistant and produce a deeper JSON-formatted output that simulates running the experiment and explains next steps. Return a single valid JSON object only with these keys:\n- simulated_results: array of objects [{frame:int, color_on:bool, model_confidence:float (0-1), brief_observation:string}] showing at least 6 frames (mix color_on true/false).\n- surprise_moments: array of 1-3 short strings describing unexpected behaviors the simulated model showed.\n- narrative: a 3-4 sentence plain-language story describing what happened in the simulation and why (string).\n- next_experiments: array of 3 concrete follow-ups (strings) ranked by ease (easy->hard).\n- teaching_quiz: array of 3 Q/A objects {question:string, answer:string, distractors:array of 2 plausible wrong answers} to use in a classroom or lab.\n- visual_export_instructions: concise steps to create an interactive toggle visualization (3-5 short step strings) for a web demo.\nUse playful metaphors, avoid dry textbook tone, and output valid JSON only.",
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
    "name": "Chromatic Cue Lab",
    "description": "An interactive lab where users design, simulate, and visualize 'selective color' strategies to learn why video AI often works in grayscale and only needs color at key moments.",
    "category": "AI Education",
    "date": "2026-04-03"
}
