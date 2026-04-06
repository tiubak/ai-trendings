"""Diffusion Detective Lab — Type a concept and step through a playful, interactive reverse-diffusion walkthrough that produces analogies, a toy noise schedule, a ready-to-run prompt, and creative learning tasks."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an imaginative AI teacher for curious developers. Given the single-word or short-phrase topic {topic}, produce a single JSON object (no extra text) with the following fields: \n\n- \"hook\": one playful sentence that sparks curiosity about diffusion and ties to {topic} (use humor or a surprising twist). \n- \"analogy\": a fresh, original analogy (2-3 sentences) that compares the diffusion generation process to a tangible activity (e.g., sculpting, baking, fog-clearing) and references {topic}. Avoid textbook phrasing. \n- \"six_step_story\": an array of exactly 6 short strings; each string is a vivid 1-2 sentence step describing the reverse diffusion journey from random noise to a final sample of {topic}, using sensory language and a memorable metaphor. Number the steps in natural order. \n- \"visual_clue\": a small emoji or ASCII-art cue (max 3 lines) that helps the learner visualize the noise\u2192image progression for {topic}. \n- \"toy_noise_schedule\": an array of 6 numbers between 0.0 and 1.0 that represent a simple, plausible noise schedule (descending for denoising). \n- \"micro_challenge\": a 1-sentence playful task the user can try next (e.g., a prompt-edit, a tiny code tweak, or a hypothesis to test in 1\u20132 minutes). \n- \"seed_prompt\": a 1\u20132 sentence model-ready prompt optimized for creative output about {topic} (suitable for a text-to-image diffusion model). Keep it concrete and evocative. \n- \"quick_resources\": an array of up to 3 objects each with keys \"title\" and \"why\" giving a concise recommended next reading or tool and a one-line reason.\n\nBe imaginative and surprising \u2014 use humor, little metaphors, and sensory detail. Return only valid JSON.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Now dig deeper into user input {user_input}. Return a single JSON object (no extra text) with these keys: \n\n- \"refined_prompt\": an improved, detailed diffusion model prompt tuned from {user_input} with prompt-engineering tricks (token-weighting, vivid adjectives, negative prompts if applicable). \n- \"tweaks\": an object proposing exact numeric tweaks: {\"steps\":int, \"guidance_scale\":float, \"sampler\":string, \"batch_size\":int, \"noise_schedule\": [floats...] } tailored to produce clearer or more creative results from {user_input}. \n- \"pseudo_code\": a compact Python-style pseudo-code snippet (as a single string) for a 20-100 step sampling loop that shows where the noise_schedule and guidance_scale plug in (keep it short). \n- \"debug_tips\": an array of 3 concise troubleshooting tips for common problems (blurry output, mode collapse, too much noise). \n- \"personified_denoiser\": three short lines giving the denoiser an amusing internal monologue reacting to {user_input} (creative, first-person). \n- \"estimate_resource\": a one-line approximate runtime/VRAM estimate for generating a single 512x512 sample at the suggested steps on a consumer GPU (e.g., RTX 3060). \n\nBe practical but playful; produce only valid JSON.",
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
    "name": "Diffusion Detective Lab",
    "description": "Type a concept and step through a playful, interactive reverse-diffusion walkthrough that produces analogies, a toy noise schedule, a ready-to-run prompt, and creative learning tasks.",
    "category": "AI Education",
    "date": "2026-04-06"
}
