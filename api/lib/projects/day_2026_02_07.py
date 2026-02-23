"""AI Token Cost Calculator & Optimizer - February 7, 2026

Understand and optimize the costs of using AI APIs. Learn about tokens,
context windows, pricing models, and strategies to reduce AI usage costs.
"""

from ..base import call_openrouter, generate_image_url, extract_json
import json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.

    Args:
        action: 'start', 'calculate', 'optimize', 'compare', 'strategies'
        data: Request data from frontend

    Returns:
        dict: Response to send to frontend
    """

    if action == 'start':
        """Initialize with introduction to token economics."""
        prompt = """Explain AI token costs in simple, practical terms.

        Cover:
        - What is a token? (approx. 4 chars or 3/4 word)
        - Why tokens cost money (compute, training, infrastructure)
        - Different pricing models (per 1K tokens, per request)
        - Input vs output token costs (usually different)
        - Context windows and their impact on cost
        - Why understanding token economics matters for developers

        Make it engaging and include practical examples.
        ~250-300 words."""

        intro = call_openrouter(prompt)

        # Available models with pricing (example data - real prices change)
        models = [
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "provider": "OpenAI",
                "input_price": 0.01,  # per 1K tokens
                "output_price": 0.03,
                "context_window": 128000,
                "description": "High-capability generalist model"
            },
            {
                "id": "claude-3-opus",
                "name": "Claude 3 Opus",
                "provider": "Anthropic",
                "input_price": 0.015,
                "output_price": 0.075,
                "context_window": 200000,
                "description": "Most capable Claude model"
            },
            {
                "id": "claude-3-sonnet",
                "name": "Claude 3 Sonnet",
                "provider": "Anthropic",
                "input_price": 0.003,
                "output_price": 0.015,
                "context_window": 200000,
                "description": "Balanced Claude model"
            },
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "provider": "OpenAI",
                "input_price": 0.0005,
                "output_price": 0.0015,
                "context_window": 16385,
                "description": "Fast, cost-effective model"
            },
            {
                "id": "mistral-large",
                "name": "Mistral Large",
                "provider": "Mistral AI",
                "input_price": 0.004,
                "output_price": 0.012,
                "context_window": 32000,
                "description": "European multilingual model"
            },
            {
                "id": "openrouter/free",
                "name": "OpenRouter Free",
                "provider": "OpenRouter",
                "input_price": 0.0,
                "output_price": 0.0,
                "context_window": 16000,
                "description": "Free tier through OpenRouter aggregation"
            }
        ]

        return {
            "introduction": intro,
            "models": models
        }

    elif action == 'calculate':
        """Calculate cost for a given prompt/response."""
        model_id = data.get('model_id', 'gpt-4-turbo')
        input_text = data.get('input_text', '')
        expected_output_tokens = data.get('expected_output_tokens', 0)
        input_tokens = data.get('input_tokens', 0)

        # If no explicit token count, estimate (approx 4 chars per token)
        if input_tokens == 0 and input_text:
            input_tokens = len(input_text) // 4
        elif input_tokens == 0:
            input_tokens = 500  # default

        # Find model pricing
        models = [
            {"id": "gpt-4-turbo", "input_price": 0.01, "output_price": 0.03},
            {"id": "claude-3-opus", "input_price": 0.015, "output_price": 0.075},
            {"id": "claude-3-sonnet", "input_price": 0.003, "output_price": 0.015},
            {"id": "gpt-3.5-turbo", "input_price": 0.0005, "output_price": 0.0015},
            {"id": "mistral-large", "input_price": 0.004, "output_price": 0.012},
            {"id": "openrouter/free", "input_price": 0.0, "output_price": 0.0}
        ]

        model = next((m for m in models if m['id'] == model_id), models[0])

        input_cost = (input_tokens / 1000) * model['input_price']
        output_cost = (expected_output_tokens / 1000) * model['output_price']
        total_cost = input_cost + output_cost

        # Cost breakdown message
        if model_id == 'openrouter/free':
            cost_summary = "This model is free through OpenRouter's free tier!"
        else:
            cost_summary = f"Input: {input_tokens} tokens = ${input_cost:.4f}\nOutput: {expected_output_tokens} tokens = ${output_cost:.4f}\nTotal: ${total_cost:.4f}"

        return {
            "model": model_id,
            "input_tokens": input_tokens,
            "output_tokens": expected_output_tokens,
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total_cost": round(total_cost, 4),
            "cost_summary": cost_summary
        }

    elif action == 'optimize':
        """Provide optimization suggestions for a given use case."""
        use_case = data.get('use_case', '')
        current_tokens = data.get('current_tokens', 0)
        budget = data.get('budget', 1.0)  # daily budget in USD

        if not use_case:
            return {"error": "Please provide a use case description"}

        prompt = f"""As an AI cost optimization expert, provide practical strategies to reduce costs for this use case:

Use Case: {use_case}
Current token usage: ~{current_tokens} tokens per request
Budget: ${budget:.2f}

Provide specific, actionable advice:
1. Prompt engineering to reduce token count
2. Model selection (which models to use for which parts)
3. Caching and reuse strategies
4. Chunking and processing approaches
5. Alternative architectures (if applicable)
6. Monitoring and alerting setup

Give concrete examples relevant to the use case. ~250 words."""

        advice = call_openrouter(prompt)

        # Generate a simple optimization checklist image concept
        image_prompt = f"Minimalist icon set showing AI cost optimization: token reduction, caching, model selection, budget monitoring, prompt engineering. Clean vector style, blue and green colors."
        image_url = generate_image_url(image_prompt)

        return {
            "use_case": use_case,
            "optimization_advice": advice,
            "visualization_url": image_url
        }

    elif action == 'compare':
        """Compare costs across multiple models for a given usage pattern."""
        usage_pattern = data.get('usage_pattern', {})
        # Expected: {"requests_per_day": 1000, "avg_input_tokens": 500, "avg_output_tokens": 300}

        requests = usage_pattern.get('requests_per_day', 1000)
        input_tokens = usage_pattern.get('avg_input_tokens', 500)
        output_tokens = usage_pattern.get('avg_output_tokens', 300)

        models = [
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "input_price": 0.01, "output_price": 0.03},
            {"id": "claude-3-opus", "name": "Claude 3 Opus", "input_price": 0.015, "output_price": 0.075},
            {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "input_price": 0.003, "output_price": 0.015},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "input_price": 0.0005, "output_price": 0.0015},
            {"id": "mistral-large", "name": "Mistral Large", "input_price": 0.004, "output_price": 0.012},
            {"id": "openrouter/free", "name": "OpenRouter Free", "input_price": 0.0, "output_price": 0.0}
        ]

        comparisons = []
        for model in models:
            cost_per_request = (input_tokens / 1000) * model['input_price'] + (output_tokens / 1000) * model['output_price']
            daily_cost = cost_per_request * requests
            monthly_cost = daily_cost * 30

            comparisons.append({
                "model": model['name'],
                "model_id": model['id'],
                "cost_per_1k_requests": round(cost_per_request * 1000, 4),
                "daily_cost": round(daily_cost, 4),
                "monthly_cost": round(monthly_cost, 4),
                "free_available": model['input_price'] == 0 and model['output_price'] == 0
            })

        # Find cheapest and best value
        paid_models = [c for c in comparisons if not c['free_available']]
        if paid_models:
            cheapest = min(paid_models, key=lambda x: x['monthly_cost'])
            best_value = cheapest  # Simple: cheapest among paid
        else:
            cheapest = comparisons[0]
            best_value = comparisons[0]

        return {
            "usage_pattern": usage_pattern,
            "comparisons": comparisons,
            "cheapest": cheapest,
            "recommendation": f"For {requests:,} requests/day with {input_tokens} input / {output_tokens} output tokens, {best_value['model']} offers the best value at ${best_value['monthly_cost']:.2f}/month."
        }

    elif action == 'strategies':
        """Get cost optimization strategies and best practices."""
        strategies = [
            {
                "category": "Prompt Engineering",
                "techniques": [
                    "Be specific and concise - avoid vague instructions",
                    "Use delimiters and structure to reduce ambiguity",
                    "Specify output format to avoid follow-ups",
                    "Include examples in the prompt to guide the model",
                    "Remove unnecessary context and small talk"
                ],
                "potential_savings": "20-50%"
            },
            {
                "category": "Model Selection",
                "techniques": [
                    "Use smaller, faster models for simple tasks",
                    "Reserve large models for complex reasoning only",
                    "Consider fine-tuning smaller models for specialized tasks",
                    "Use multiple models in a cascade (cheap first, expensive if needed)",
                    "Leverage free tiers (OpenRouter free, Claude Sonnet, etc.)"
                ],
                "potential_savings": "40-80%"
            },
            {
                "category": "Caching & Memory",
                "techniques": [
                    "Cache frequent queries and their responses",
                    "Implement semantic caching (similar queries hit cache)",
                    "Store conversation history and reuse context",
                    "Use embeddings to find similar past responses",
                    "Set appropriate cache TTLs based on content volatility"
                ],
                "potential_savings": "30-70% for repetitive workloads"
            },
            {
                "category": "Token Management",
                "techniques": [
                    "Trim context windows to only relevant history",
                    "Use vector databases for long-term memory instead of context",
                    "Compress or summarize old messages",
                    "Implement token counting and set alerts",
                    "Use token-efficient formats (JSON over verbose examples)"
                ],
                "potential_savings": "10-40%"
            },
            {
                "category": "Architecture Patterns",
                "techniques": [
                    "Split tasks: small model for simple parts, large model for hard parts",
                    "Preprocess with traditional algorithms before AI",
                    "Use AI only where truly needed, rules elsewhere",
                    "Batch process similar requests together",
                    "Implement request deduplication"
                ],
                "potential_savings": "25-60%"
            }
        ]

        # Generate a summary of the most important principles
        prompt = """Summarize the 5 most important principles of AI cost optimization.

        For each principle, provide:
        1. A clear principle name
        2. A one-sentence explanation
        3. A concrete example

        Make it memorable and actionable. JSON format with array of objects."""

        summary_text = call_openrouter(prompt)
        summary = extract_json(summary_text, default=[
            {
                "principle": "Right-Size Your Model",
                "explanation": "Match model capability to task complexity.",
                "example": "Use GPT-3.5 for simple Q&A, GPT-4 for complex reasoning."
            },
            {
                "principle": "Cache Aggressively",
                "explanation": "Reuse responses to identical or similar queries.",
                "example": "Cache product FAQ answers for 24 hours."
            },
            {
                "principle": "Trim Token Bloat",
                "explanation": "Only send necessary context to the API.",
                "example": "Keep only last 5 conversation turns, not 50."
            },
            {
                "principle": "Batch and Deduplicate",
                "explanation": "Group similar requests and eliminate duplicates.",
                "example": "Batch 100 similar classification requests into one API call."
            },
            {
                "principle": "Monitor and Alert",
                "explanation": "Track token usage and set budget alerts.",
                "example": "Alert when daily spending exceeds $10."
            }
        ])

        return {
            "strategies": strategies,
            "key_principles": summary
        }

    elif action == 'pricing_info':
        """Get current pricing information and trends."""
        prompt = """Provide an overview of current AI API pricing trends (as of early 2026).

        Cover:
        1. General pricing direction (increasing, decreasing, stable)
        2. Free tier availability across major providers
        3. Context window trends (getting larger)
        4. Emerging pricing models (e.g., per token, per session, per character)
        5. Cost vs quality trade-offs
        6. Tips for staying current with pricing changes

        Make it practical for developers. ~200 words."""

        pricing_info = call_openrouter(prompt)

        # Generate a pricing trends visualization concept
        image_prompt = "Line chart showing AI API costs decreasing over time while capabilities increase. Two lines: cost per 1K tokens and context window size. Clean, modern data visualization style."
        image_url = generate_image_url(image_prompt)

        return {
            "pricing_trends": pricing_info,
            "visualization_url": image_url
        }

    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Token Cost Calculator & Optimizer",
    "description": "Understand and optimize the costs of using AI APIs. Calculate token usage, compare model pricing, learn cost reduction strategies, and make informed decisions about AI budgeting.",
    "category": "AI Tools",
    "tags": ["cost-optimization", "tokens", "pricing", "budgeting", "api", "educational"],
    "difficulty": "Beginner to Intermediate"
}
