"""LLM Model Comparator - Compare and understand different language models"""

def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'get_models', 'compare', 'explain_concept'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    from lib.base import call_openrouter, generate_image_url
    
    if action == 'get_models':
        """Return list of popular LLMs with their key characteristics."""
        models = [
            {
                "name": "GPT-4",
                "developer": "OpenAI",
                "release_date": "2023-03-14",
                "context_window": "128K tokens",
                "strengths": ["Strong reasoning", "Code generation", "Creative writing"],
                "best_for": ["Complex problem-solving", "Programming", "Content creation"],
                "limitations": ["Costly API", "Less transparent training data"],
                "open_source": False
            },
            {
                "name": "Claude 3.5 Sonnet",
                "developer": "Anthropic",
                "release_date": "2024-06-20",
                "context_window": "200K tokens",
                "strengths": ["Safety-focused", "Long document analysis", "Nuanced reasoning"],
                "best_for": ["Safety-critical applications", "Legal/technical docs", "Detailed analysis"],
                "limitations": ["Less creative than GPT-4", "Anthropic's guardrails"],
                "open_source": False
            },
            {
                "name": "Gemini 1.5 Pro",
                "developer": "Google DeepMind",
                "release_date": "2024-02-15",
                "context_window": "1M tokens",
                "strengths": ["Massive context", "Multimodal (text+image+audio)", "Fast processing"],
                "best_for": ["Long document processing", "Multimodal tasks", "Video understanding"],
                "limitations": ["Less nuanced in creative writing", "Integration complexity"],
                "open_source": False
            },
            {
                "name": "Llama 3.1",
                "developer": "Meta AI",
                "release_date": "2024-07-18",
                "context_window": "128K tokens",
                "strengths": ["Open source", "Customizable", "Strong performance", "Free to use"],
                "best_for": ["Research", "Custom deployments", "Privacy-sensitive apps", "Cost optimization"],
                "limitations": ["Requires infrastructure", "Less polished than commercial"],
                "open_source": True
            },
            {
                "name": "Mistral Large",
                "developer": "Mistral AI",
                "release_date": "2024-02-26",
                "context_window": "32K tokens",
                "strengths": ["Efficient", "Strong multilingual", "European data privacy"],
                "best_for": ["Multilingual applications", "EU compliance", "Resource-efficient deployment"],
                "limitations": ["Smaller context", "Less ecosystem than competitors"],
                "open_source": False
            },
            {
                "name": "Command R+",
                "developer": "Cohere",
                "release_date": "2024-03-04",
                "context_window": "128K tokens",
                "strengths": ["Enterprise-ready", "RAG optimization", "Tool use"],
                "best_for": ["Enterprise search", "RAG applications", "Tool-augmented AI"],
                "limitations": ["Less creative", "Commercial focus"],
                "open_source": False
            }
        ]
        return {"models": models}
    
    elif action == 'explain_concept':
        """Explain an AI/LLM concept in simple terms."""
        concept = data.get('concept', 'language models')
        prompt = f"""Explain the AI/LLM concept of "{concept}" in simple, beginner-friendly terms.

Provide:
1. A clear, jargon-free definition (2-3 sentences)
2. An analogy that makes it easy to understand
3. Why it matters for AI and everyday use

Keep the explanation accessible to someone without a technical background."""
        
        explanation = call_openrouter(prompt)
        return {
            "concept": concept,
            "explanation": explanation
        }
    
    elif action == 'generate_architecture':
        """Generate a simple diagram of an LLM architecture."""
        model_name = data.get('model', 'transformer architecture')
        prompt = f"Simple clean diagram showing {model_name} architecture, labeled parts, technical illustration style"
        image_url = generate_image_url(prompt, width=800, height=600)
        return {
            "model": model_name,
            "image_url": image_url
        }
    
    else:
        return {"error": f"Unknown action: {action}"}

# Metadata for projects.json
META = {
    "name": "LLM Model Comparator",
    "description": "Compare popular language models (GPT-4, Claude, Gemini, Llama) and learn about AI concepts",
    "category": "AI Education",
    "date": "2026-02-01"
}
