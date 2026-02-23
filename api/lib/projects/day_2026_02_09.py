"""AI Model Selection Guide: Choose the Right AI for Your Task - February 9, 2026

A comprehensive guide to understanding AI models and selecting the best one
for your specific use case. Learn about model capabilities, strengths, and
practical applications across different domains.
"""

from ..base import call_openrouter, generate_image_url, extract_json
import json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.

    Args:
        action: 'start', 'compare', 'recommend', 'categories', 'capabilities', 'use_cases'
        data: Request data from frontend

    Returns:
        dict: Response to send to frontend
    """

    if action == 'start':
        """Initialize with introduction to AI model selection."""
        prompt = """Welcome to the AI Model Selection Guide!

AI models have different strengths and specializations. Choosing the right model
for your task can significantly impact both quality and cost.

Key factors to consider:
- Task type (text, code, reasoning, creative, analysis)
- Complexity level (simple to expert)
- Context length requirements
- Budget constraints
- Speed vs quality trade-offs
- Multilingual needs

Major model categories:
1. General-purpose chat models (GPT, Claude, etc.) - versatile assistants
2. Coding specialists (CodeLlama, DeepSeek Coder) - programming tasks
3. Reasoning models (o1, Claude Opus) - complex problem-solving
4. Fast/cheap models (GPT-3.5, Claude Sonnet) - simple tasks
5. Specialized models (math, medical, legal) - domain-specific
6. Multilingual models - non-English tasks

This guide helps you navigate these choices with interactive tools and
practical recommendations based on your specific needs.

~200 words introduction."""

        intro = call_openrouter(prompt)

        # Generate an AI model ecosystem visualization
        image_prompt = "Tree diagram showing AI model ecosystem: trunk 'Foundation Models', branches for 'General Purpose', 'Coding', 'Reasoning', 'Creative', 'Analysis', 'Multilingual'. Each branch has model icons: GPT, Claude, Llama, Mistral, etc. Clean infographic style with connected nodes."
        image_url = generate_image_url(image_prompt)

        return {
            "introduction": intro,
            "ecosystem_image": image_url,
            "quick_stats": {
                "total_categories": 6,
                "featured_models": 15,
                "use_cases": "50+"
            }
        }

    elif action == 'categories':
        """Get overview of AI model categories."""
        categories = [
            {
                "id": "general",
                "name": "General Purpose",
                "description": "Versatile models for everyday tasks, conversation, and general assistance",
                "models": [
                    {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI", "strengths": ["conversation", "analysis", "creative"], "best_for": "Most general tasks"},
                    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "strengths": ["reasoning", "writing", "safety"], "best_for": "Complex analysis and writing"},
                    {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "Anthropic", "strengths": ["balanced", "efficient"], "best_for": "Good balance of cost and capability"},
                    {"id": "llama-3-70b", "name": "Llama 3 70B", "provider": "Meta", "strengths": ["open-source", "customizable"], "best_for": "Self-hosting and customization"}
                ]
            },
            {
                "id": "coding",
                "name": "Programming & Code",
                "description": "Specialized models for software development, debugging, and code generation",
                "models": [
                    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "OpenAI", "strengths": ["multi-language", "frameworks", "documentation"], "best_for": "Full-stack development"},
                    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "strengths": ["code quality", "best practices"], "best_for": "Production-grade code"},
                    {"id": "deepseek-coder", "name": "DeepSeek Coder", "provider": "DeepSeek", "strengths": ["algorithms", "competitive programming"], "best_for": "Algorithmic problems"},
                    {"id": "codellama-70b", "name": "CodeLlama 70B", "provider": "Meta", "strengths": ["open-source", "local"], "best_for": "Local development environments"}
                ]
            },
            {
                "id": "reasoning",
                "name": "Advanced Reasoning",
                "description": "Models optimized for complex reasoning, problem-solving, and analytical tasks",
                "models": [
                    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "strengths": ["nuanced reasoning", "complex analysis"], "best_for": "Strategic planning and deep analysis"},
                    {"id": "openai-o1", "name": "GPT-o1", "provider": "OpenAI", "strengths": ["step-by-step reasoning", "math"], "best_for": "Math and logic puzzles"},
                    {"id": "mistral-large", "name": "Mistral Large", "provider": "Mistral AI", "strengths": ["multilingual reasoning"], "best_for": "Cross-cultural analysis"},
                    {"id": "claude-3.5-sonnet", "name": "Claude 3.5 Sonnet", "provider": "Anthropic", "strengths": ["speed+reasoning"], "best_for": "Fast, high-quality reasoning"}
                ]
            },
            {
                "id": "creative",
                "name": "Creative & Content",
                "description": "Models excelling at creative writing, storytelling, and content creation",
                "models": [
                    {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI", "strengths": ["storytelling", "dialogue", "style"], "best_for": "Fiction and creative writing"},
                    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "strengths": ["long-form", "narrative"], "best_for": "Novels and long content"},
                    {"id": "midjourney-api", "name": "Midjourney", "provider": "Midjourney", "strengths": ["visual art", "imagery"], "best_for": "Image generation and visual concepts"},
                    {"id": "dall-e-3", "name": "DALL-E 3", "provider": "OpenAI", "strengths": ["text-to-image", "prompt-adherence"], "best_for": "Illustrations and diagrams"}
                ]
            },
            {
                "id": "analysis",
                "name": "Data Analysis & Research",
                "description": "Models specialized in analyzing data, research papers, and structured information",
                "models": [
                    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "strengths": ["paper analysis", "citations"], "best_for": "Academic research"},
                    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "OpenAI", "strengths": ["data interpretation", "charts"], "best_for": "Business intelligence"},
                    {"id": "perplexity-api", "name": "Perplexity", "provider": "Perplexity", "strengths": ["web search", "real-time"], "best_for": "Current information and fact-checking"},
                    {"id": "wolfram-alpha", "name": "Wolfram Alpha", "provider": "Wolfram", "strengths": ["computation", "verified facts"], "best_for": "Scientific and mathematical computing"}
                ]
            },
            {
                "id": "multilingual",
                "name": "Multilingual & Translation",
                "description": "Models with strong capabilities across multiple languages",
                "models": [
                    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "OpenAI", "strengths": ["100+ languages", "cultural nuance"], "best_for": "Global content localization"},
                    {"id": "mistral-large", "name": "Mistral Large", "provider": "Mistral AI", "strengths": ["European languages", "accuracy"], "best_for": "European market content"},
                    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "strengths": ["translation quality", "idioms"], "best_for": "High-stakes professional translation"},
                    {"id": "google-gemini", "name": "Gemini Pro", "provider": "Google", "strengths": ["Asian languages", "technical"], "best_for": "East Asian languages and tech content"}
                ]
            }
        ]

        return {"categories": categories}

    elif action == 'capabilities':
        """Get detailed capability matrix for models."""
        # Define capability matrix
        capabilities_matrix = {
            "dimensions": [
                "reasoning", "coding", "creative_writing", "math", "multilingual",
                "long_context", "speed", "cost_effectiveness", "instruction_following",
                "factual_accuracy", "safety", "customization"
            ],
            "models": [
                {
                    "id": "gpt-4-turbo",
                    "name": "GPT-4 Turbo",
                    "scores": [9, 9, 8, 8, 9, 9, 7, 6, 9, 8, 8, 7],
                    "price_tier": "high"
                },
                {
                    "id": "claude-3-opus",
                    "name": "Claude 3 Opus",
                    "scores": [10, 9, 9, 9, 8, 10, 6, 5, 9, 9, 10, 6],
                    "price_tier": "high"
                },
                {
                    "id": "claude-3.5-sonnet",
                    "name": "Claude 3.5 Sonnet",
                    "scores": [9, 8, 9, 8, 8, 8, 8, 7, 9, 8, 9, 6],
                    "price_tier": "mid"
                },
                {
                    "id": "gpt-3.5-turbo",
                    "name": "GPT-3.5 Turbo",
                    "scores": [6, 6, 6, 5, 7, 6, 9, 9, 7, 6, 7, 5],
                    "price_tier": "low"
                },
                {
                    "id": "mistral-large",
                    "name": "Mistral Large",
                    "scores": [8, 8, 7, 7, 9, 7, 8, 8, 8, 7, 8, 7],
                    "price_tier": "mid"
                },
                {
                    "id": "deepseek-coder",
                    "name": "DeepSeek Coder",
                    "scores": [7, 10, 5, 8, 6, 6, 8, 9, 8, 6, 7, 6],
                    "price_tier": "mid"
                },
                {
                    "id": "openrouter/free",
                    "name": "OpenRouter Free",
                    "scores": [5, 5, 5, 4, 5, 5, 8, 10, 6, 5, 6, 4],
                    "price_tier": "free"
                }
            ]
        }

        # Generate capability radar chart description
        image_prompt = "Radar chart comparing AI models across dimensions: reasoning, coding, creative, math, multilingual, context length. Three overlapping polygons for GPT-4, Claude Opus, and free models. Clean, modern data visualization with legend."
        image_url = generate_image_url(image_prompt)

        return {
            "matrix": capabilities_matrix,
            "visualization": image_url,
            "dimension_descriptions": {
                "reasoning": "Complex logical reasoning and problem-solving",
                "coding": "Programming tasks, debugging, code generation",
                "creative_writing": "Storytelling, creative content, original narratives",
                "math": "Mathematical computation and problem-solving",
                "multilingual": "Non-English language understanding and generation",
                "long_context": "Ability to process very long inputs (32K+ tokens)",
                "speed": "Response time and throughput",
                "cost_effectiveness": "Quality per dollar spent",
                "instruction_following": "Precision in following user instructions",
                "factual_accuracy": "Truthfulness and avoidance of hallucinations",
                "safety": "Alignment, refusal of harmful requests",
                "customization": "Fine-tuning and adaptation capabilities"
            }
        }

    elif action == 'recommend':
        """Get personalized model recommendation based on use case."""
        task_type = data.get('task_type', 'general')
        complexity = data.get('complexity', 'medium')  # simple, medium, complex
        budget = data.get('budget', 'mid')  # low, mid, high
        speed_priority = data.get('speed_priority', False)
        context_length = data.get('context_length', 'medium')  # short, medium, long
        language = data.get('language', 'english')

        # Recommendation logic based on inputs
        recommendations = []

        if task_type == 'coding':
            if complexity == 'complex' and budget in ['high', 'mid']:
                recommendations.append({
                    "model": "claude-3-opus",
                    "confidence": 0.9,
                    "reason": "Best code quality and best practices for complex projects"
                })
            elif budget == 'low':
                recommendations.append({
                    "model": "deepseek-coder",
                    "confidence": 0.85,
                    "reason": "Excellent coding capability at lower cost"
                })
            else:
                recommendations.append({
                    "model": "gpt-4-turbo",
                    "confidence": 0.8,
                    "reason": "Strong all-around coding ability with fast iteration"
                })

        elif task_type == 'reasoning':
            if complexity == 'complex':
                recommendations.append({
                    "model": "claude-3-opus",
                    "confidence": 0.95,
                    "reason": "Superior complex reasoning and nuanced understanding"
                })
            elif speed_priority:
                recommendations.append({
                    "model": "claude-3.5-sonnet",
                    "confidence": 0.85,
                    "reason": "Excellent reasoning with faster response times"
                })
            else:
                recommendations.append({
                    "model": "openai-o1",
                    "confidence": 0.8,
                    "reason": "Strong step-by-step reasoning for analytical tasks"
                })

        elif task_type == 'creative':
            if complexity == 'complex':
                recommendations.append({
                    "model": "gpt-4",
                    "confidence": 0.85,
                    "reason": "Excellent storytelling and creative writing"
                })
            else:
                recommendations.append({
                    "model": "claude-3.5-sonnet",
                    "confidence": 0.8,
                    "reason": "Good creative output with faster speed"
                })

        elif task_type == 'analysis':
            if context_length == 'long':
                recommendations.append({
                    "model": "claude-3-opus",
                    "confidence": 0.9,
                    "reason": "200K context window ideal for long documents"
                })
            else:
                recommendations.append({
                    "model": "gpt-4-turbo",
                    "confidence": 0.85,
                    "reason": "Strong analytical capabilities with good speed"
                })

        elif task_type == 'multilingual':
            if language in ['chinese', 'japanese', 'korean']:
                recommendations.append({
                    "model": "google-gemini",
                    "confidence": 0.85,
                    "reason": "Strong performance on East Asian languages"
                })
            elif language in ['french', 'german', 'spanish', 'italian']:
                recommendations.append({
                    "model": "mistral-large",
                    "confidence": 0.9,
                    "reason": "Excellent European language support"
                })
            else:
                recommendations.append({
                    "model": "gpt-4-turbo",
                    "confidence": 0.85,
                    "reason": "Broad language coverage and good quality"
                })

        else:  # general
            if budget == 'low' or (budget == 'mid' and speed_priority):
                recommendations.append({
                    "model": "claude-3.5-sonnet",
                    "confidence": 0.8,
                    "reason": "Best balance of cost, speed, and capability"
                })
            elif budget == 'high' and complexity == 'complex':
                recommendations.append({
                    "model": "claude-3-opus",
                    "confidence": 0.95,
                    "reason": "Top-tier capability for demanding tasks"
                })
            else:
                recommendations.append({
                    "model": "gpt-4-turbo",
                    "confidence": 0.85,
                    "reason": "Versatile and reliable for most general tasks"
                })

        # Add budget-friendly alternative
        if budget != 'low':
            budget_alternative = {
                "model": "claude-3.5-sonnet" if recommendations[0]['model'] != "claude-3.5-sonnet" else "gpt-3.5-turbo",
                "confidence": 0.7,
                "reason": "Budget-friendly alternative with reasonable performance"
            }
            recommendations.append(budget_alternative)

        # Generate model comparison visual
        top_model = recommendations[0]['model']
        prompt = f"Comparison card for {top_model}: highlight key features, strengths, best use cases, and pricing tier. Modern UI card design with icons and clean layout."
        image_url = generate_image_url(prompt)

        return {
            "recommendations": recommendations,
            "user_profile": {
                "task_type": task_type,
                "complexity": complexity,
                "budget": budget,
                "speed_priority": speed_priority,
                "context_length": context_length,
                "language": language
            },
            "top_pick_image": image_url
        }

    elif action == 'use_cases':
        """Get specific use case recommendations."""
        use_cases = [
            {
                "category": "Development",
                "cases": [
                    {"name": "Code Review", "recommendation": "claude-3-opus", "reason": "Detailed, thoughtful feedback on code quality"},
                    {"name": "Bug Debugging", "recommendation": "gpt-4-turbo", "reason": "Fast iteration and multiple solution approaches"},
                    {"name": "Test Generation", "recommendation": "deepseek-coder", "reason": "Strong algorithmic thinking"},
                    {"name": "Documentation", "recommendation": "gpt-3.5-turbo", "reason": "Good quality at low cost"}
                ]
            },
            {
                "category": "Content Creation",
                "cases": [
                    {"name": "Blog Posts", "recommendation": "claude-3.5-sonnet", "reason": "Excellent writing quality and SEO awareness"},
                    {"name": "Social Media", "recommendation": "gpt-3.5-turbo", "reason": "Fast and engaging"},
                    {"name": "Technical Writing", "recommendation": "claude-3-opus", "reason": "Deep technical understanding"},
                    {"name": "Creative Stories", "recommendation": "gpt-4", "reason": "Strong narrative capabilities"}
                ]
            },
            {
                "category": "Research & Analysis",
                "cases": [
                    {"name": "Paper Summarization", "recommendation": "claude-3-opus", "reason": "Long context, precise summarization"},
                    {"name": "Data Interpretation", "recommendation": "gpt-4-turbo", "reason": "Good balance of analysis and speed"},
                    {"name": "Market Research", "recommendation": "perplexity-api", "reason": "Real-time web search capabilities"},
                    {"name": "Statistical Analysis", "recommendation": "wolfram-alpha", "reason": "Verified computational accuracy"}
                ]
            },
            {
                "category": "Business & Productivity",
                "cases": [
                    {"name": "Email Drafting", "recommendation": "gpt-3.5-turbo", "reason": "Quick, professional responses"},
                    {"name": "Meeting Summaries", "recommendation": "claude-3.5-sonnet", "reason": "Excellent condensation and clarity"},
                    {"name": "Strategy Planning", "recommendation": "claude-3-opus", "reason": "Deep strategic thinking"},
                    {"name": "Customer Support", "recommendation": "gpt-3.5-turbo", "reason": "Fast, consistent responses"}
                ]
            },
            {
                "category": "Education & Learning",
                "cases": [
                    {"name": "Tutoring", "recommendation": "gpt-4-turbo", "reason": "Adaptable explanations and patience"},
                    {"name": "Problem Sets", "recommendation": "openai-o1", "reason": "Step-by-step reasoning visible"},
                    {"name": "Language Learning", "recommendation": "mistral-large", "reason": "Strong multilingual support"},
                    {"name": "Essay Feedback", "recommendation": "claude-3-opus", "reason": "Detailed, constructive criticism"}
                ]
            },
            {
                "category": "Multilingual Tasks",
                "cases": [
                    {"name": "Translation (European)", "recommendation": "mistral-large", "reason": "Specialized in European languages"},
                    {"name": "Translation (Asian)", "recommendation": "google-gemini", "reason": "Strong East Asian language support"},
                    {"name": "Localization", "recommendation": "gpt-4-turbo", "reason": "Cultural nuance understanding"},
                    {"name": "Cross-cultural Communication", "recommendation": "claude-3-opus", "reason": "Sensitive to cultural differences"}
                ]
            }
        ]

        return {"use_cases": use_cases}

    elif action == 'compare':
        """Compare specific models side by side."""
        model_ids = data.get('models', ['gpt-4-turbo', 'claude-3-opus', 'gpt-3.5-turbo'])

        model_details = {
            "gpt-4-turbo": {
                "name": "GPT-4 Turbo",
                "provider": "OpenAI",
                "context_window": 128000,
                "pricing": {"input": 0.01, "output": 0.03, "per_1k": True},
                "strengths": ["Versatile", "Strong coding", "Multilingual", "Good speed"],
                "weaknesses": ["Cost can add up", "Default behavior can be verbose"],
                "best_for": ["General tasks", "Development", "Analysis", "Creative work"],
                "release_date": "2023-11",
                "model_type": "General purpose"
            },
            "claude-3-opus": {
                "name": "Claude 3 Opus",
                "provider": "Anthropic",
                "context_window": 200000,
                "pricing": {"input": 0.015, "output": 0.075, "per_1k": True},
                "strengths": ["Best reasoning", "Long context", "Superior writing", "Safety"],
                "weaknesses": ["Slow", "Expensive", "Verbose outputs"],
                "best_for": ["Complex analysis", "Long-form writing", "Strategic tasks"],
                "release_date": "2024-03",
                "model_type": "Reasoning specialist"
            },
            "claude-3.5-sonnet": {
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "context_window": 200000,
                "pricing": {"input": 0.003, "output": 0.015, "per_1k": True},
                "strengths": ["Fast", "Cost-effective", "Excellent quality", "Long context"],
                "weaknesses": ["Slightly less capable than Opus on edge cases"],
                "best_for": ["Most workloads", "Production applications", "Balanced use"],
                "release_date": "2024-06",
                "model_type": "Balanced"
            },
            "gpt-3.5-turbo": {
                "name": "GPT-3.5 Turbo",
                "provider": "OpenAI",
                "context_window": 16385,
                "pricing": {"input": 0.0005, "output": 0.0015, "per_1k": True},
                "strengths": ["Very fast", "Very cheap", "Good for simple tasks"],
                "weaknesses": ["Limited reasoning", "Smaller context", "Lower quality"],
                "best_for": ["Simple Q&A", "Classification", "High-volume tasks"],
                "release_date": "2023-03",
                "model_type": "Fast/cheap"
            },
            "mistral-large": {
                "name": "Mistral Large",
                "provider": "Mistral AI",
                "context_window": 32000,
                "pricing": {"input": 0.004, "output": 0.012, "per_1k": True},
                "strengths": ["European languages", "Multilingual", "Good reasoning"],
                "weaknesses": ["Smaller context than top models", "Less US-centric"],
                "best_for": ["European markets", "Multilingual apps", "Cost-quality balance"],
                "release_date": "2024-02",
                "model_type": "Multilingual"
            },
            "deepseek-coder": {
                "name": "DeepSeek Coder",
                "provider": "DeepSeek",
                "context_window": 16000,
                "pricing": {"input": 0.00014, "output": 0.00028, "per_1k": True},
                "strengths": ["Excellent coding", "Algorithm problems", "Very cheap"],
                "weaknesses": ["English-only mostly", "Niche focus"],
                "best_for": ["Coding tasks", "Competitive programming", "Budget development"],
                "release_date": "2024-01",
                "model_type": "Coding specialist"
            },
            "openrouter/free": {
                "name": "OpenRouter Free",
                "provider": "OpenRouter",
                "context_window": 16000,
                "pricing": {"input": 0.0, "output": 0.0, "per_1k": True},
                "strengths": ["Free", "Multiple models", "Easy access"],
                "weaknesses": ["Rate limits", "Inconsistent quality", "Less reliable"],
                "best_for": ["Prototyping", "Testing", "Non-critical tasks"],
                "release_date": "2023-12",
                "model_type": "Free tier"
            }
        }

        comparison = []
        for model_id in model_ids:
            if model_id in model_details:
                comparison.append(model_details[model_id])

        if not comparison:
            # Return all if none match
            comparison = list(model_details.values())

        # Generate comparison table visualization
        prompt = "Comparison table of AI models showing: name, context window, input price, output price, and best use cases. Clean, readable table design with alternating row colors."
        image_url = generate_image_url(prompt)

        return {
            "models": comparison,
            "visualization": image_url,
            "total_models_available": len(model_details)
        }

    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Model Selection Guide",
    "description": "Choose the right AI model for your task. Compare capabilities, get personalized recommendations, and understand which models excel at coding, reasoning, creativity, analysis, and more.",
    "category": "AI Education",
    "tags": ["model-selection", "comparison", "recommendations", "guidance", "educational", "decision-making"],
    "difficulty": "Beginner",
    "date": "2026-02-09"
}