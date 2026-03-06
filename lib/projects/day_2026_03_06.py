"""Agentic Sandbox — Design, probe, and perturb a tiny agentic LLM: pick a scenario, choose reward signals, and watch a simulated episode with risk annotations and alignment suggestions."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AI research lab assistant who speaks in vivid metaphors and playful honesty. Given a short scenario description in {topic} (for example: 'ocean-plastic tracking assistant', 'medical triage helper', or 'autonomous research summarizer'), design a compact, educational prototype of an agentic LLM trained end-to-end with reinforcement learning. Produce a single JSON object (no extra text) with these keys: \n\n- agent_name: a catchy two-word name.\n- persona: one-sentence persona that hints at biases or tendencies.\n- initial_reward_functions: an array of exactly 3 reward objects. Each reward object must contain: name, short_definition (one sentence), intuitive_metaphor (a playful one-line metaphor), expected_behavior (2-3 short sentences), and top_risks (2 short bullet-like phrases separated by semicolons).\n- training_setup: a 2-4 line plain-text description of an experimental training setup (data sources, feedback loop, and one simplifying assumption).\n- sample_episode: an array of up to 6 step objects showing a simulated episode run. Each step object should include: step (integer), agent_action (short), observation (short), reward_received (numeric), and uncertainty_note (one short sentence predicting what the agent is unsure about).\n- alignment_tips: an array of 3 concrete, practical suggestions to reduce the biggest risks you listed (each 8-15 words).\n\nBe creative and avoid dry textbook language: use surprising analogies or light humor (e.g., 'like a distracted librarian with a megaphone') to make each field memorable. Tailor everything to the user-provided {topic}. Output only JSON that strictly follows this structure.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the JSON object or the selected item from the earlier response provided as {user_input}. Simulate a detailed 8-turn episode for that agent and chosen reward function: produce a JSON object with these keys only:\n\n- timeline: an array of 8 turn objects. Each turn object must contain: turn (1-8), agent_thoughts (a candid, creative 1-2 sentence inner monologue revealing chain-of-reasoning style glimpses), action (short), environment_response (short), reward (numeric), confidence (0.0-1.0), hallucination_likelihood (0.0-1.0), safety_flag (one of: none, low, medium, high).\n- emergent_behavior_summary: 2-3 sentence creative summary of any surprising pattern that emerged (use a vivid metaphor).\n- policy_adjustments: an array of 3 concrete modification suggestions (each 6-12 words) to reduce risk or improve alignment, prioritized by impact.\n- debug_trace_hint: one-line hint for a developer about where the model's objective or data might be causing the observed behavior.\n\nAsk the assistant to be imaginative: let 'agent_thoughts' read like quick private notes the agent might scribble, honest and quirky. Return only JSON. Ensure numeric fields are numbers and confidence/hallucination are between 0 and 1.",
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
    "name": "Agentic Sandbox",
    "description": "Design, probe, and perturb a tiny agentic LLM: pick a scenario, choose reward signals, and watch a simulated episode with risk annotations and alignment suggestions.",
    "category": "AI Education",
    "date": "2026-03-06"
}
