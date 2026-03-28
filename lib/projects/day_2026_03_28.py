"""AGI Scenario Sandbox — Create a custom AGI profile and run playful yet rigorous thought experiments about its capabilities, risks, societal ripples, and safeguards."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AGI facilitator. A user will give a short scenario in {topic} (example inputs: \"a city-planning AGI run by a municipal coalition\", \"a startup AGI narrowly focused on creative advertising\", \"a broadly competent assistant with mild value drift\"). Using {topic}, invent a single, vivid AGI profile and output a JSON object with these keys: \n\n- id: short slug (lowercase, hyphenated)\n- title: catchy name for the AGI (5 words max)\n- one_liner: one-sentence hook that sells the scenario with humor or drama\n- persona: a 40\u2013100 word character sketch using a striking metaphor (e.g., \"like a barista who learned geopolitics\")\n- capability_scale: integer 0-10 and a 1\u20132 sentence justification of where it lands and why\n- dominant_risks: array of exactly 3 objects each with {\"risk\":\"short name\",\"explain\":\"one sentence\"}\n- societal_ripples: array of 4 creative effects (label each: economic, cultural, legal, psychological) with 1\u20132 sentence descriptions\n- three_what_if_paths: array of three objects named optimistic, mixed, failure \u2014 each with a 3-step timeline (years and inflection points) and a headline outcome sentence\n- recommended_safeguards: array of 5 prioritized, actionable safeguards (one sentence each) labeled with priority (1-5)\n- teaching_activity: a 2-paragraph interactive classroom/workshop activity that teachers can run in 20\u201340 minutes to explore the scenario, including roles and one short deliverable\n- creative_prompt_for_story: one vivid one-sentence writing prompt for a short fiction piece set in this scenario\n\nKeep the voice witty, surprising, and concrete; use metaphors and a dash of humor to make it memorable. Ensure valid JSON output only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the previously-generated scenario identified by {user_input} and produce a deeper JSON-formatted risk mitigation and readiness plan. Frame this like planning a delicate spaceship docking: list assumptions, map the attack surface, and provide layered responses. Output JSON with these keys:\n\n- scenario_id: echo {user_input}\n- assumptions: array of 3 bullet assumptions that underpin your plan\n- attack_surface: array of 4 vectors (technical, social, supply-chain, governance) each with a short risk description\n- short_term_mitigations: array of 4 items (0\u20132 years) each object containing {\"action\",\"owner\",\"estimated_effort\":\"low|med|high\",\"success_indicator\"}\n- long_term_governance: array of 3 policies/norms or institutional mechanisms with 2-sentence rationale each\n- experiment_plan: array of 3 small-scale experiments or indicators to test alignment/behaviour, each with metric(s) and safe-fail thresholds\n- communication_scripts: object with keys \"technical\",\"civic\",\"empathetic\" each containing a 2-3 sentence script for public or stakeholder communication\n- uncertainty_estimates: object mapping each short_term_mitigation action to an uncertainty rating (low|med|high) and one-sentence justification\n\nUse creative metaphors and one surprising analogy or humorous image somewhere in the JSON, but keep content practical and actionable. Output must be valid JSON.",
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
    "name": "AGI Scenario Sandbox",
    "description": "Create a custom AGI profile and run playful yet rigorous thought experiments about its capabilities, risks, societal ripples, and safeguards.",
    "category": "AI Education",
    "date": "2026-03-28"
}
