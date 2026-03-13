"""OctoSkin Studio — Give a mood or use-case and receive a playful, teachable design package for an octopus-inspired adaptive 'skin' — colors, patterns, and AI-driven actuation choreography."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative design assistant for bio-inspired materials. A user will provide a short {topic} (a mood, a function, or a scene). Produce a single JSON object called \"skin_design\" that is both practical for classroom explanation and delightfully whimsical. Think like an octopus poet meets a computational designer: use metaphors, surprises, and a touch of humor. For the provided {topic}, generate the following keys and content:\n\n- title: short evocative name (string)\n- blurb: one-sentence elevator pitch for this skin (string)\n- palette: array of 3 hex color strings that convey the mood (array)\n- pattern_description: short, vivid description of the surface pattern and how it changes (string, use at least one metaphor)\n- actuation_sequence: ordered array of steps; each step is an object with keys {time_ms, primary_visual_change, texture_or_shape_change} describing the choreography (array of objects)\n- control_signals: a high-level, non-hazardous description of the abstract control signals or inputs an AI controller would use (object with keys: sensor_inputs, control_strategy)\n- simulation_hint: a simple parametric formula or pseudo-code snippet (string) suitable for driving a front-end animation (no lab steps or hazardous details)\n- fabrication_notes: brief, non-actionable notes linking concept to smart hydrogel behavior and safe material considerations (2-3 sentences, explicitly avoid giving chemical protocols)\n- educational_explainer: 2-3 sentences connecting octopus biology, the hydrogel trend, and why AI is useful here (clear for learners)\n- octopus_whisperer_tip: a playful one-liner tip for designers (string)\n\nUse creative analogies (e.g., 'like a shy neon sign', 'papillae like popcorn') and avoid dry textbook language. Do NOT include step-by-step lab protocols, exact chemical recipes, or voltage/current values. Output ONLY valid JSON for the object \"skin_design\".",
        "parse": "json"
    },
    "explore": {
        "prompt": "Deeper dive: using the user's input {user_input}, produce a JSON object named \"explore_package\" that expands the initial design into actionable learning and simulation assets for a web demo. Include these keys:\n\n- variations: array of 3 alternative theme variations (each with name and one-line twist)\n- sim_parameters: object giving parametric animation parameters suitable for a browser (keys might include frequency, amplitude, phase_shift, color_cycle_time; provide example numeric ranges, not lab settings)\n- sample_data_stream: a short array of timestamped normalized sensor-like values (e.g., [{t:0, val:0.1}, ...]) that an AI controller could use to trigger pattern shifts\n- visualization_pseudocode: concise pseudo-code that maps sim_parameters and sample_data_stream to on-screen pattern updates (string)\n- classroom_exercises: array of 3 scaffolded activities (title and 1-2 sentence instructions) that teach concepts like bio-inspiration, control loops, and ethical considerations\n- further_reading: array of 3 short references or search phrases for learners to explore (strings)\n\nKeep the tone exploratory and playful but educational. Ensure outputs are safe and focused on simulation, design, and pedagogy (no wet-lab instructions). Return ONLY the JSON object \"explore_package\".",
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
    "name": "OctoSkin Studio",
    "description": "Give a mood or use-case and receive a playful, teachable design package for an octopus-inspired adaptive 'skin' — colors, patterns, and AI-driven actuation choreography.",
    "category": "AI Education",
    "date": "2026-03-13"
}
