"""AI Funding Playground — Enter a one-line AI startup idea and get a playful, realistic simulated valuation, investor personas, and a mock term-sheet with negotiation playbook."""

from ..base import (call_openrouter, call_pollinations, extract_json, fetch_image,
    query_db, load_json_data, web_search, fetch_url, wikipedia_summary, fetch_rss,
    generate_qr, generate_wordcloud, tmp_sqlite, call_huggingface, call_gTTS,
    classify_text, embed_text, text_to_speech, CDN_LIBS, PUBLIC_APIS)
import json as _json

ACTIONS = {
    "start": {
        "prompt": "You are a witty, data-savvy startup sage who translates a one-line AI startup idea into a vivid funding scene. Take the user's input {topic} (a short description of an AI startup) and produce imaginative, concrete, and plausible output in JSON. Be playful (use metaphors like dragons, librarians, or neighborhood baristas) but precise with numbers and assumptions. Provide the following keys exactly:\n\n- title: short, clever scene title\n- one_liner: improved one-line elevator pitch\n- estimated_valuation: {min:int, mid:int, max:int, currency:string, pre_or_post:string} where values are in USD and assumptions are given\n- valuation_rationale: 2-4 sentences explaining the mid valuation and the main drivers/risks\n- key_metrics: list of 5 metric objects {name, value, why_it_matters}\n- investor_personas: array of 3 persona objects {name, archetype, one_line_quote, ideal_check_size_usd, ideal_terms_summary, top_concern}\n- mock_term_sheet: object {round: \"Series A\" or \"Seed\", raise_usd, pre_money_usd, equity_pct_offered, option_pool_after_round_pct, liquidation_pref, board_seats, vesting_months, anti_dilution:short, pro_rata:boolean, milestones_tranches: array of {milestone, tranche_amount_usd}}\n- dilution_preview: array showing founders' % ownership before and after (assume founders start with 100% before option pool expansion) as objects {stage_label, founders_pct, investors_pct, option_pool_pct}\n- negotiation_levers: list of 5 concrete levers (e.g., milestone tranches, ratchets, price-based vesting) with one-line examples\n- recommended_next_steps: 3 actionable next moves for the founder (e.g., metrics to hit, investor types to target, script to open conversation)\n\nKeep tone surprising and friendly; include at least one playful metaphor (e.g., \"this investor is like a librarian who quietly checks your references\") and call out the top 2 assumptions you used for the numbers. Return valid JSON only.",
        "parse": "json"
    },
    "explore": {
        "prompt": "Take the founder's selection {user_input} (either the name of an investor persona from the previous output or a scenario like \"accept mid valuation\" / \"push for higher valuation with milestones\") and run a step-by-step negotiation simulation. Return JSON with these keys:\n\n- scenario_title: short\n- starting_term_sheet: copy of the mock_term_sheet object used as the starting point\n- negotiation_rounds: array of rounds where each round is {round_number:int, actor:\"Founder\"|\"Investor\", action_summary:string, new_terms:object (same shape as mock_term_sheet but only fields that changed), founder_equity_after_round_pct:float, notes_for_founder:string}\n- cap_table_snapshots: array of {label, founders_pct, investors_pct, option_pool_pct, post_money_usd}\n- three_counteroffer_templates: array of 3 objects {tone:\"bridging\"|\"bold\"|\"conservative\", email_subject, email_body} that the founder can send to the investor\n- impact_analysis: list of 4 short items describing how the final terms affect control, fundraising runway, hiring ability, and exit scenarios\n- risk_mitigation_checklist: 5 checklist items (one-line) to protect founder upside\n\nUse lively metaphors and practical negotiation language (no legalese). Make each negotiation round realistic and show numeric changes to equity or amounts. Return valid JSON only.",
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
    "name": "AI Funding Playground",
    "description": "Enter a one-line AI startup idea and get a playful, realistic simulated valuation, investor personas, and a mock term-sheet with negotiation playbook.",
    "category": "AI Education",
    "date": "2026-03-14"
}
