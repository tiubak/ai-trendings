"""Post-Training Sandbox — Enter a task or application and get an educational, step-by-step post-training refinement plan for turning a base model into a production-ready specialist."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are an expert AI engineer and educator. Given the user-specified application or task {topic}, produce a single JSON object containing the following fields: \n\n- topic: echo the input string.\n- summary: one-sentence plain-language summary of the problem and the specialization goal.\n- why_post_training: 2-3 short bullet points explaining why a post-training specialization approach fits this use case.\n- post_training_strategy: an ordered array of 6\u201310 concise steps (each a short string) describing a viable post-training pipeline (data curation, adapter/LoRA or fine-tuning choice, curriculum, evaluation loop, deployment tweaks).\n- dataset_examples: an array of 3\u20136 dataset types or concrete data sources the practitioner could use, with one-line sourcing or generation tips for each.\n- labeling_guidelines: an array of 4\u20136 concise labeling rules or schema tips that maximize downstream performance and reduce noise.\n- evaluation_metrics: an array of metrics to measure (each item: metric name and one-line reason it's relevant).\n- compute_and_cost_estimate: an object with keys small, medium, large each giving approximate resources (GPU type or vCPU), typical wall-time, and a rough cost range in USD.\n- risks_and_mitigation: an array of 4\u20136 short risk statements paired with one-line mitigation actions.\n- prototype_pipeline: an ordered array of 6\u20138 concrete commands or pseudocode steps (short strings) showing how to run one iteration end-to-end (data -> post-train -> eval -> deploy).\n- milestones: an array of 3\u20135 milestone objects {name:string, target:string, success_criteria:string}.\n- further_reading: an array of 3 concise references (title and URL) for deeper study.\n\nKeep explanations concise and technical enough for an intermediate ML engineer. Use arrays and objects, avoid long paragraphs. Return only valid JSON (no surrounding commentary).",
        "parse": "json"
    },
    "explore": {
        "prompt": "The user provided additional input {user_input} (this could be constraints such as 'edge device only', 'privacy-first', 'limited budget', or 'robotics safety-critical'). Based on that, produce a JSON object with these fields:\n\n- user_input: echo the string.\n- refined_plan: an ordered array of 6\u201310 revised post_training_strategy steps tailored to the constraint.\n- reduced_resource_options: an array of 3 options (each with name, how it reduces compute, and impact on accuracy) for low-cost or edge-friendly deployment.\n- data_collection_plan: a short timeline object {week1:activities, week2:activities, week3:activities} with pragmatic tasks for 3 weeks.\n- evaluation_protocol: an array of 4\u20136 concrete tests (each with test name, how to run it, and pass/fail criteria) addressing performance and safety for this use case.\n- code_snippets: an array of 2\u20134 short code snippets or CLI commands (strings) illustrating critical steps (e.g., adapter training command, quantization command, quick eval loop). Keep them short and high-level.\n- tradeoffs: an array of 3 concise tradeoff statements comparing accuracy, latency, cost, and safety for the options above.\n- next_actions: an ordered array of 5 immediate actionable steps the user should take next.\n\nOutput only valid JSON. Keep entries concise and actionable.",
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
    "name": "Post-Training Sandbox",
    "description": "Enter a task or application and get an educational, step-by-step post-training refinement plan for turning a base model into a production-ready specialist.",
    "category": "AI Education",
    "date": "2026-02-17"
}
