#!/usr/bin/env python3
"""
AI Trendings — Bulletproof Daily Project Generator

Usage:
    python3 generate_project.py                    # today's date
    python3 generate_project.py 2026-02-15         # specific date
    python3 generate_project.py --backfill 2026-02-13 2026-02-23  # range

This script:
1. Picks a project from the curated topic pool (no AI needed for selection)
2. Generates the Python handler from a proven template
3. Generates the HTML frontend from a proven template
4. Updates projects.json
5. Validates everything compiles/parses
6. Commits and pushes

A dumb model only needs to run: python3 generate_project.py
"""

import json
import os
import sys
import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent

# ============================================================================
# TOPIC POOL — Curated, tested, ready to go. Add more anytime.
# Each topic has everything needed to generate a complete project.
# ============================================================================

TOPICS = [
    # --- Deep AI Topics ---
    {
        "slug": "ai-embedding-explorer",
        "name": "AI Embedding Explorer",
        "description": "Discover how AI converts words into numbers — explore word embeddings, see which words are similar, and understand the math behind semantic search",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain word embeddings in AI in simple terms. Cover: what they are, why they matter, how words become vectors, and give 3 surprising examples of word relationships (like king - man + woman = queen). Format as JSON with keys: explanation, examples (array of {words, relationship}), analogy.",
                "parse": "json"
            },
            "compare": {
                "prompt": "Compare these two words in embedding space: '{word1}' and '{word2}'. Explain how similar they are semantically, what dimensions they might share, and give a similarity score 0-100. Return JSON: {similarity_score, explanation, shared_concepts, fun_fact}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter two words to compare", "input_fields": ["word1", "word2"]}
    },
    {
        "slug": "ai-hallucination-detector",
        "name": "AI Hallucination Detector",
        "description": "Learn about AI hallucinations — why models make things up, how to spot them, and techniques researchers use to reduce confabulation",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain AI hallucinations in simple terms. Cover: what they are, why they happen (training data gaps, pattern completion, confidence calibration), 3 famous real-world examples, and 3 techniques to detect/prevent them. Format as JSON: {explanation, why_it_happens (array), famous_examples (array of {description, impact}), prevention_techniques (array of {name, how_it_works})}.",
                "parse": "json"
            },
            "test": {
                "prompt": "Generate a passage about '{topic}' that contains exactly 2 subtle factual errors (hallucinations) mixed with correct information. Then reveal what the errors are. Format as JSON: {passage, errors (array of {error_text, correction, why_ai_might_say_this}), correct_facts (array)}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter a topic to test", "input_fields": ["topic"]}
    },
    {
        "slug": "ai-prompt-engineering-lab",
        "name": "AI Prompt Engineering Lab",
        "description": "Master the art of prompt engineering — learn techniques like chain-of-thought, few-shot, and role prompting with interactive examples",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain prompt engineering in simple terms. Cover the top 5 techniques: 1) Zero-shot, 2) Few-shot, 3) Chain-of-thought, 4) Role prompting, 5) Self-consistency. For each give a concrete example. Format as JSON: {overview, techniques (array of {name, description, example_prompt, example_output, when_to_use})}.",
                "parse": "json"
            },
            "improve": {
                "prompt": "The user wrote this prompt: '{user_prompt}'. Analyze it and suggest 3 improved versions using different techniques. Explain why each is better. Format as JSON: {original_analysis, improvements (array of {technique, improved_prompt, why_better, expected_quality_boost})}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter a prompt to improve", "input_fields": ["user_prompt"]}
    },
    {
        "slug": "ai-temperature-playground",
        "name": "AI Temperature Playground",
        "description": "Understand how temperature and sampling parameters affect AI output — see the same prompt at different temperatures side by side",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain AI temperature/sampling parameters in simple terms. Cover: temperature (0.0-2.0), top-p (nucleus sampling), top-k, and frequency penalty. For each, explain what it does and when to use low vs high values. Format as JSON: {overview, parameters (array of {name, range, description, low_value_effect, high_value_effect, best_for})}.",
                "parse": "json"
            },
            "generate": {
                "prompt": "Generate 3 versions of a response to '{user_prompt}' as if using different temperature settings. Version 1: temperature=0.1 (precise, predictable). Version 2: temperature=0.7 (balanced, natural). Version 3: temperature=1.5 (creative, wild). Format as JSON: {versions (array of {temperature, response, characteristics})}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter a prompt to test at different temperatures", "input_fields": ["user_prompt"]}
    },
    {
        "slug": "ai-bias-explorer",
        "name": "AI Bias Explorer",
        "description": "Explore how bias enters AI systems — from training data to model outputs — and learn about fairness techniques researchers are developing",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain AI bias in simple terms. Cover: 5 types of bias (selection, confirmation, measurement, automation, historical), 3 real-world examples where AI bias caused harm, and 3 techniques to mitigate bias. Format as JSON: {overview, bias_types (array of {name, description, example}), real_world_cases (array of {case, impact, lesson}), mitigation (array of {technique, how_it_works})}.",
                "parse": "json"
            },
            "analyze": {
                "prompt": "Analyze this scenario for potential AI bias: '{scenario}'. Identify possible biases, affected groups, and suggest fairness improvements. Format as JSON: {scenario_analysis, potential_biases (array of {type, description, affected_groups}), recommendations (array), fairness_score (1-10)}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Describe an AI scenario to analyze for bias", "input_fields": ["scenario"]}
    },
    {
        "slug": "ai-training-cost-calculator",
        "name": "AI Training Cost Calculator",
        "description": "Estimate how much it costs to train AI models — from GPT-scale to small fine-tunes — covering GPU hours, electricity, and carbon footprint",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain AI training costs in simple terms. Include: cost breakdown for training a large model (GPUs, electricity, cooling, engineering), comparison of training costs for GPT-4 (~$100M), Llama 3 (~$30M), and a small fine-tune (~$100). Include carbon footprint data. Format as JSON: {overview, cost_breakdown (array of {component, percentage, description}), model_comparisons (array of {model, estimated_cost, gpu_hours, parameters, year}), carbon_impact, fun_facts (array)}.",
                "parse": "json"
            },
            "estimate": {
                "prompt": "Estimate the training cost for a model with these specs: {parameters} parameters, trained on {tokens} tokens, using {gpu_type} GPUs. Calculate approximate: GPU hours, electricity cost, total cost, and CO2 emissions. Format as JSON: {specs, estimated_gpu_hours, electricity_kwh, cost_usd, co2_kg, comparison (e.g. 'equivalent to X car trips'), tips_to_reduce_cost (array)}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Model specs", "input_fields": ["parameters", "tokens", "gpu_type"]}
    },
    {
        "slug": "ai-rag-explained",
        "name": "RAG Architecture Explained",
        "description": "Understand Retrieval-Augmented Generation — how AI combines search with generation to give accurate, sourced answers",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Explain RAG (Retrieval-Augmented Generation) in simple terms. Cover: what it is, the 3-step process (retrieve, augment, generate), why it reduces hallucinations, comparison with fine-tuning, and 4 real-world use cases. Format as JSON: {overview, steps (array of {step_number, name, description, analogy}), vs_fine_tuning (array of {aspect, rag, fine_tuning}), use_cases (array of {name, description}), limitations (array)}.",
                "parse": "json"
            },
            "simulate": {
                "prompt": "Simulate a RAG pipeline for the question: '{question}'. Show what would happen at each step: 1) What chunks would be retrieved, 2) How context is assembled, 3) How the final answer is generated. Format as JSON: {question, retrieved_chunks (array of {content, relevance_score}), assembled_context, generated_answer, without_rag_answer, comparison}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter a question to simulate RAG", "input_fields": ["question"]}
    },
    {
        "slug": "ai-benchmark-arena",
        "name": "AI Benchmark Arena",
        "description": "Compare AI models head-to-head on different tasks — see how GPT, Claude, Gemini, and open-source models stack up on reasoning, coding, and creativity",
        "category": "AI Education",
        "actions": {
            "start": {
                "prompt": "Create a comprehensive comparison of top AI models as of early 2026. Include: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3.1 405B, Mistral Large, and DeepSeek V3. Compare on: reasoning, coding, creative writing, math, multilingual, speed, cost. Format as JSON: {overview, models (array of {name, company, parameters, release_date, strengths, weaknesses}), benchmarks (array of {category, rankings (array of {model, score, notes})}), verdict}.",
                "parse": "json"
            },
            "challenge": {
                "prompt": "Create a '{task_type}' challenge and show how different AI models would likely approach it differently. Show expected outputs from 3 different models. Format as JSON: {challenge, task_type, model_responses (array of {model, approach, response_sample, strengths, weaknesses}), winner, analysis}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Choose a task type", "input_fields": ["task_type"]}
    },
    # --- Fun AI Applications ---
    {
        "slug": "ai-roast-master",
        "name": "AI Roast Master",
        "description": "Get lovingly roasted by AI — enter your bio or profession and receive clever, witty roasts that are funny but never mean",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "You are a comedy roast master. The audience member describes themselves as: '{bio}'. Write 5 clever, witty roasts that are funny but never cruel or offensive. Think Comedy Central Roast style — sharp but with love. Also include 1 genuine compliment at the end. Format as JSON: {roasts (array of strings), compliment, comedy_style}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Tell us about yourself (job, hobbies, etc.)", "input_fields": ["bio"]}
    },
    {
        "slug": "ai-startup-pitch-generator",
        "name": "AI Startup Pitch Generator",
        "description": "Generate hilariously absurd AI startup ideas with pitch decks, valuations, and investor buzzwords — satire of Silicon Valley culture",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "Generate a hilariously absurd AI startup idea. Include: ridiculous name, outrageous tagline, what it supposedly does, inflated valuation, buzzword-laden pitch, fake testimonials, and why VCs would fund it. Make it satirical but clever. Format as JSON: {name, tagline, description, valuation, pitch_paragraph, buzzwords (array), testimonials (array of {person, quote}), funding_round, red_flags_investors_ignore (array)}.",
                "parse": "json"
            },
            "pivot": {
                "prompt": "The AI startup '{startup_name}' needs to pivot! Generate an even more absurd pivot idea that somehow makes it worse but more fundable. Format as JSON: {original, pivot_name, pivot_description, why_its_worse, why_vcs_love_it, new_valuation, press_headline}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Industry to satirize (optional)", "input_fields": ["industry"]}
    },
    {
        "slug": "ai-conspiracy-debunker",
        "name": "AI Conspiracy Theory Debunker",
        "description": "Enter any conspiracy theory and watch AI break it down with logic, evidence, and humor — learn critical thinking along the way",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "Debunk this conspiracy theory with facts, logic, and humor: '{theory}'. Cover: the claim, its origin, why people believe it (psychological factors), the actual evidence against it, and a funny analogy. Format as JSON: {claim, origin, why_people_believe (array of {factor, explanation}), debunking_evidence (array of {point, source}), logical_fallacies (array), funny_analogy, critical_thinking_tip}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter a conspiracy theory to debunk", "input_fields": ["theory"]}
    },
    {
        "slug": "ai-time-traveler-advice",
        "name": "AI Time Traveler's Advice",
        "description": "Ask an AI pretending to be from different time periods for advice — get hilariously anachronistic responses from medieval, Victorian, or future perspectives",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "You are a person from {era}. Someone from 2026 asks you: '{question}'. Answer completely in character — use the knowledge, vocabulary, worldview, and concerns of your era. Be funny and creative. Format as JSON: {era, character_description, response, misunderstandings (array — things from 2026 you'd find confusing), advice, historical_context}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Your question + choose an era", "input_fields": ["question", "era"]}
    },
    {
        "slug": "ai-excuse-generator",
        "name": "AI Excuse Generator",
        "description": "Need an excuse? AI generates increasingly elaborate and creative excuses for any situation — from missing meetings to forgetting birthdays",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "Generate 5 creative excuses for this situation: '{situation}'. Make them escalating in absurdity: 1) Believable, 2) Somewhat plausible, 3) Stretching it, 4) Ridiculous, 5) Absolutely unhinged. Format as JSON: {situation, excuses (array of {level, excuse, believability_percent, potential_consequences}), pro_tip}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "What do you need an excuse for?", "input_fields": ["situation"]}
    },
    {
        "slug": "ai-movie-plot-mashup",
        "name": "AI Movie Plot Mashup",
        "description": "Combine two movies into one absurd plot — AI creates the mashup with cast, plot twists, and a Rotten Tomatoes score",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "Combine these two movies into one absurd mashup: '{movie1}' and '{movie2}'. Create a complete movie concept. Format as JSON: {title, tagline, genre, plot_summary, cast (array of {character, actor, description}), plot_twists (array), best_scene_description, rotten_tomatoes_score, critic_quote, sequel_hint}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter two movies to mash up", "input_fields": ["movie1", "movie2"]}
    },
    {
        "slug": "ai-alien-translator",
        "name": "AI Alien Language Translator",
        "description": "AI invents an alien language and translates your messages — complete with grammar rules, pronunciation guide, and cultural notes",
        "category": "Fun",
        "actions": {
            "start": {
                "prompt": "Create an alien language and translate this message into it: '{message}'. Include: language name, home planet, grammar rules (at least 3), the translation with pronunciation, and cultural context about how aliens would interpret this message. Format as JSON: {language_name, planet, species, grammar_rules (array of {rule, example}), original, translation, pronunciation, cultural_notes, fun_fact}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Enter a message to translate to alien", "input_fields": ["message"]}
    },
    # --- Practical AI Tools ---
    {
        "slug": "ai-code-explainer",
        "name": "AI Code Explainer",
        "description": "Paste any code snippet and get a clear, visual explanation of what it does — line by line, with complexity analysis and improvement suggestions",
        "category": "Practical",
        "actions": {
            "start": {
                "prompt": "Explain this code in simple terms: ```{code}```. Cover: what language it is, what it does overall, line-by-line explanation, time/space complexity, potential bugs, and one improvement suggestion. Format as JSON: {language, summary, line_by_line (array of {line_number, code, explanation}), complexity (time and space), potential_bugs (array), improvement}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Paste code to explain", "input_fields": ["code"]}
    },
    {
        "slug": "ai-regex-builder",
        "name": "AI Regex Builder",
        "description": "Describe what you want to match in plain English and get a regex pattern with explanation, test cases, and visual breakdown",
        "category": "Practical",
        "actions": {
            "start": {
                "prompt": "Create a regex pattern for: '{description}'. Provide the pattern, a visual breakdown of each part, 5 test strings (3 that match, 2 that don't), common pitfalls, and alternatives. Format as JSON: {description, pattern, breakdown (array of {part, meaning}), test_cases (array of {input, matches, reason}), pitfalls (array), language_notes (for JS, Python, etc)}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "Describe what you want to match", "input_fields": ["description"]}
    },
    {
        "slug": "ai-learning-path-generator",
        "name": "AI Learning Path Generator",
        "description": "Enter any skill you want to learn and get a personalized study plan with resources, milestones, and estimated time to competency",
        "category": "Practical",
        "actions": {
            "start": {
                "prompt": "Create a learning path for someone who wants to learn '{skill}' from {level} level. Include: overview, prerequisites, 5 phases with milestones, recommended resources (mix of free and paid), estimated total hours, and a weekly study schedule. Format as JSON: {skill, current_level, overview, prerequisites (array), phases (array of {name, duration_weeks, topics (array), milestone, resources (array of {name, type, url_or_description, cost})}), total_hours, weekly_schedule, motivation_tip}.",
                "parse": "json"
            }
        },
        "ui_type": "input_output",
        "ui_config": {"input_label": "What do you want to learn?", "input_fields": ["skill", "level"]}
    },
]

# ============================================================================
# TEMPLATES — Proven, tested templates for handler + frontend
# ============================================================================

HANDLER_TEMPLATE = '''"""__NAME__ — __DESCRIPTION__"""

from ..base import call_openrouter, extract_json, fetch_image

ACTIONS = __ACTIONS_JSON__

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
    "name": "__NAME__",
    "description": "__DESCRIPTION__",
    "category": "__CATEGORY__",
    "date": "__DATE__"
}
'''

FRONTEND_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__NAME__ | AI Trendings</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #e0e0e0;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .back-nav { margin-bottom: 30px; }
        .back-btn {
            display: inline-flex; align-items: center; gap: 8px;
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            color: #00f260; padding: 10px 20px; border-radius: 8px;
            text-decoration: none; font-size: 0.9rem; transition: all 0.3s;
        }
        .back-btn:hover { background: rgba(255,255,255,0.1); transform: translateY(-2px); }
        h1 {
            font-size: 2.2rem; margin-bottom: 10px;
            background: linear-gradient(90deg, #00f260 0%, #0575e6 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .subtitle { color: #888; margin-bottom: 30px; font-size: 1.1rem; }
        .card {
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 24px; margin-bottom: 20px;
        }
        .input-group { margin-bottom: 16px; }
        .input-group label { display: block; margin-bottom: 6px; color: #00f260; font-size: 0.9rem; }
        .input-group input, .input-group textarea, .input-group select {
            width: 100%; padding: 12px; border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.3);
            color: #e0e0e0; font-size: 1rem; font-family: inherit;
        }
        .input-group textarea { min-height: 100px; resize: vertical; }
        .btn {
            background: linear-gradient(90deg, #00f260, #0575e6); color: #fff;
            border: none; padding: 12px 32px; border-radius: 8px; font-size: 1rem;
            cursor: pointer; transition: all 0.3s; font-weight: 600;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,242,96,0.3); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .result { margin-top: 24px; }
        .result-section { margin-bottom: 16px; }
        .result-section h3 { color: #00f260; margin-bottom: 8px; font-size: 1rem; }
        .result-section p, .result-section li { line-height: 1.6; }
        .result-section ul { padding-left: 20px; }
        .result-section li { margin-bottom: 6px; }
        .loading { text-align: center; padding: 40px; }
        .loading .spinner {
            width: 40px; height: 40px; border: 3px solid rgba(255,255,255,0.1);
            border-top-color: #00f260; border-radius: 50%;
            animation: spin 0.8s linear infinite; margin: 0 auto 16px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .error { color: #ff6b6b; padding: 16px; background: rgba(255,0,0,0.1); border-radius: 8px; }
        .tag {
            display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;
            background: rgba(0,242,96,0.15); color: #00f260; margin: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="back-nav">
            <a href="/" class="back-btn">&larr; Back to Calendar</a>
        </nav>
        <h1>__NAME__</h1>
        <p class="subtitle">__DESCRIPTION__</p>

        <div class="card" id="input-card">
            __INPUT_FIELDS_HTML__
            <button class="btn" id="go-btn" onclick="run()">
                __BUTTON_TEXT__
            </button>
        </div>

        <div id="loading" class="loading" style="display:none">
            <div class="spinner"></div>
            <p>Thinking...</p>
        </div>

        <div id="result" class="result" style="display:none"></div>
        <div id="error" class="error" style="display:none"></div>
    </div>

    <script>
        const DATE = '__DATE__';
        const API_URL = '/api/index';

        async function apiCall(action, data = {}) {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ date: DATE, action, ...data })
            });
            if (!response.ok) throw new Error('API error: ' + response.status);
            return response.json();
        }

        async function run() {
            const btn = document.getElementById('go-btn');
            const loading = document.getElementById('loading');
            const resultDiv = document.getElementById('result');
            const errorDiv = document.getElementById('error');

            const data = {};
            document.querySelectorAll('[data-field]').forEach(el => {
                data[el.dataset.field] = el.value;
            });

            btn.disabled = true;
            loading.style.display = 'block';
            resultDiv.style.display = 'none';
            errorDiv.style.display = 'none';

            try {
                const resp = await apiCall('__DEFAULT_ACTION__', data);
                if (resp.error) throw new Error(resp.error);
                resultDiv.innerHTML = renderResult(resp.result || resp);
                resultDiv.style.display = 'block';
            } catch (e) {
                errorDiv.textContent = e.message;
                errorDiv.style.display = 'block';
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }

        function renderResult(data) {
            if (typeof data === 'string') return `<div class="card"><p>${data}</p></div>`;
            if (data.text) return `<div class="card"><p>${data.text}</p></div>`;

            let html = '';
            for (const [key, value] of Object.entries(data)) {
                if (key === 'date' || key === 'parse_note') continue;
                html += `<div class="card result-section">`;
                html += `<h3>${key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</h3>`;

                if (Array.isArray(value)) {
                    html += '<ul>';
                    value.forEach(item => {
                        if (typeof item === 'object') {
                            html += '<li>' + Object.entries(item)
                                .map(([k,v]) => `<strong>${k.replace(/_/g,' ')}:</strong> ${typeof v === 'object' ? JSON.stringify(v) : v}`)
                                .join(' &middot; ') + '</li>';
                        } else {
                            html += `<li>${item}</li>`;
                        }
                    });
                    html += '</ul>';
                } else if (typeof value === 'object' && value !== null) {
                    html += '<ul>';
                    Object.entries(value).forEach(([k, v]) => {
                        html += `<li><strong>${k.replace(/_/g,' ')}:</strong> ${v}</li>`;
                    });
                    html += '</ul>';
                } else {
                    html += `<p>${value}</p>`;
                }
                html += '</div>';
            }
            return html || '<div class="card"><p>No results</p></div>';
        }

        // Auto-run start action on load
        __AUTO_START_JS__
    </script>
</body>
</html>
'''


def build_input_fields_html(topic):
    """Generate HTML input fields from topic config."""
    config = topic.get("ui_config", {})
    fields = config.get("input_fields", [])
    
    if not fields:
        return ""
    
    html_parts = []
    for field in fields:
        label = field.replace("_", " ").title()
        if field in ("code", "bio", "description", "scenario", "theory", "message", "user_prompt"):
            html_parts.append(f'<div class="input-group"><label>{label}</label><textarea data-field="{field}" placeholder="Enter {label.lower()}..."></textarea></div>')
        elif field in ("era", "level", "gpu_type", "task_type"):
            options = get_select_options(field)
            opts_html = "".join(f'<option value="{o}">{o}</option>' for o in options)
            html_parts.append(f'<div class="input-group"><label>{label}</label><select data-field="{field}">{opts_html}</select></div>')
        else:
            html_parts.append(f'<div class="input-group"><label>{label}</label><input type="text" data-field="{field}" placeholder="Enter {label.lower()}..."></div>')
    
    return "\n            ".join(html_parts)


def get_select_options(field):
    options = {
        "era": ["Ancient Egypt (3000 BC)", "Medieval Europe (1200 AD)", "Renaissance Italy (1500)", "Victorian England (1880)", "Roaring Twenties (1920)", "Year 3000 (Future)"],
        "level": ["complete beginner", "beginner", "intermediate", "advanced"],
        "gpu_type": ["NVIDIA A100", "NVIDIA H100", "NVIDIA RTX 4090", "Google TPU v4", "AMD MI300X"],
        "task_type": ["creative writing", "coding", "math reasoning", "summarization", "translation", "debate"],
    }
    return options.get(field, ["option1", "option2", "option3"])


def get_default_action(topic):
    """Get the best action to run by default."""
    actions = topic.get("actions", {})
    # Prefer interactive actions over 'start'
    for a in actions:
        if a != "start":
            return a
    return "start"


def get_button_text(topic):
    actions = topic.get("actions", {})
    action_names = list(actions.keys())
    if len(action_names) <= 1 and "start" in action_names:
        return "🚀 Explore"
    for a in action_names:
        if a != "start":
            return f"🚀 {a.replace('_', ' ').title()}"
    return "🚀 Go"


def pick_topic(date_str, used_slugs):
    """Pick a topic for the date, avoiding recently used ones."""
    random.seed(date_str)  # Deterministic per date
    available = [t for t in TOPICS if t["slug"] not in used_slugs]
    if not available:
        available = TOPICS  # Reset if all used
    return random.choice(available)


def generate_project(date_str, topic=None):
    """Generate a complete project for the given date."""
    print(f"\n{'='*60}")
    print(f"  Generating project for {date_str}")
    print(f"{'='*60}")
    
    # Load existing projects
    projects_json_path = ROOT / "projects.json"
    projects = json.loads(projects_json_path.read_text()) if projects_json_path.exists() else {}
    
    if date_str in projects:
        print(f"  ⚠️  Project already exists for {date_str}, skipping")
        return False
    
    # Get used slugs from existing projects
    used_slugs = set()
    for d, p in projects.items():
        # Match by slug in path
        path = p.get("path", "")
        slug = path.split("/")[-1].replace(f"{d}-", "") if "/" in path else ""
        used_slugs.add(slug)
    
    # Pick topic
    if topic is None:
        topic = pick_topic(date_str, used_slugs)
    
    slug = topic["slug"]
    name = topic["name"]
    desc = topic["description"]
    category = topic["category"]
    
    print(f"  📦 Topic: {name} ({category})")
    print(f"  🔗 Slug: {slug}")
    
    # 1. Generate Python handler
    date_parts = date_str.split("-")
    module_name = f"day_{date_parts[0]}_{date_parts[1]}_{date_parts[2]}"
    handler_path = ROOT / "lib" / "projects" / f"{module_name}.py"
    
    actions_json = json.dumps(topic["actions"], indent=4)
    
    handler_code = (HANDLER_TEMPLATE
        .replace("__NAME__", name)
        .replace("__DESCRIPTION__", desc)
        .replace("__CATEGORY__", category)
        .replace("__DATE__", date_str)
        .replace("__ACTIONS_JSON__", actions_json)
    )
    
    handler_path.write_text(handler_code)
    print(f"  ✅ Handler: {handler_path.relative_to(ROOT)}")
    
    # 2. Generate frontend
    project_dir = ROOT / "projects" / f"{date_str}-{slug}"
    project_dir.mkdir(parents=True, exist_ok=True)
    
    input_fields_html = build_input_fields_html(topic)
    default_action = get_default_action(topic)
    button_text = get_button_text(topic)
    
    # Auto-start: load overview on page load if there's a 'start' action
    auto_start = ""
    if "start" in topic["actions"] and len(topic["actions"]) > 1:
        auto_start = "apiCall('start', {}).then(r => { if(r.result) { document.getElementById('result').innerHTML = renderResult(r.result); document.getElementById('result').style.display = 'block'; }}).catch(() => {});"
    
    frontend_code = (FRONTEND_TEMPLATE
        .replace("__NAME__", name)
        .replace("__DESCRIPTION__", desc)
        .replace("__DATE__", date_str)
        .replace("__INPUT_FIELDS_HTML__", input_fields_html)
        .replace("__DEFAULT_ACTION__", default_action)
        .replace("__BUTTON_TEXT__", button_text)
        .replace("__AUTO_START_JS__", auto_start)
    )
    
    (project_dir / "index.html").write_text(frontend_code)
    print(f"  ✅ Frontend: {project_dir.relative_to(ROOT)}/index.html")
    
    # 3. Update projects.json
    projects[date_str] = {
        "name": name,
        "path": f"projects/{date_str}-{slug}",
        "description": desc,
        "category": category,
        "created_at": date_str,
    }
    
    # Sort by date
    projects = dict(sorted(projects.items()))
    projects_json_path.write_text(json.dumps(projects, indent=4) + "\n")
    print(f"  ✅ projects.json updated")
    
    # 4. Validate
    print(f"  🔍 Validating...")
    
    # Check Python syntax
    try:
        compile(handler_path.read_text(), str(handler_path), 'exec')
        print(f"  ✅ Python syntax OK")
    except SyntaxError as e:
        print(f"  ❌ Python syntax error: {e}")
        return False
    
    # Check JSON
    try:
        json.loads(projects_json_path.read_text())
        print(f"  ✅ projects.json valid")
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON error: {e}")
        return False
    
    # Check HTML exists and has required elements
    html = (project_dir / "index.html").read_text()
    checks = [("Back to Calendar", "back button"), ("API_URL", "API integration"), (date_str, "date constant")]
    for check, label in checks:
        if check in html:
            print(f"  ✅ Frontend has {label}")
        else:
            print(f"  ⚠️  Frontend missing {label}")
    
    print(f"  🎉 Project generated successfully!")
    return True


def commit_and_push(dates_generated):
    """Git commit and push."""
    if not dates_generated:
        print("\nNothing to commit.")
        return
    
    os.chdir(ROOT)
    
    subprocess.run(["git", "add", "-A"], check=True)
    
    if len(dates_generated) == 1:
        d = dates_generated[0]
        # Get project name from projects.json
        projects = json.loads((ROOT / "projects.json").read_text())
        name = projects.get(d, {}).get("name", "new project")
        msg = f"Add {d}: {name}"
    else:
        msg = f"Add projects: {', '.join(dates_generated)}"
    
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"\n🚀 Pushed to GitHub!")


def main():
    args = sys.argv[1:]
    
    if not args:
        # Today's date
        today = datetime.now().strftime("%Y-%m-%d")
        generated = []
        if generate_project(today):
            generated.append(today)
        commit_and_push(generated)
    
    elif args[0] == "--backfill" and len(args) == 3:
        start = datetime.strptime(args[1], "%Y-%m-%d")
        end = datetime.strptime(args[2], "%Y-%m-%d")
        generated = []
        current = start
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            if generate_project(date_str):
                generated.append(date_str)
            current += timedelta(days=1)
        commit_and_push(generated)
    
    elif len(args) == 1:
        # Specific date
        generated = []
        if generate_project(args[0]):
            generated.append(args[0])
        commit_and_push(generated)
    
    else:
        print("Usage:")
        print("  python3 generate_project.py                          # today")
        print("  python3 generate_project.py 2026-02-15               # specific date")
        print("  python3 generate_project.py --backfill 2026-02-13 2026-02-23  # range")
        sys.exit(1)


if __name__ == "__main__":
    main()
