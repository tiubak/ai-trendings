"""AI Context Window Explorer - Understand AI model context limits"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""
    
    if action == 'start':
        topic = data.get('topic', 'context windows')
        prompt = f"""Explain what a context window is in AI language models in simple, clear terms. 
Include: definition, why it matters, how tokens work, and practical implications for users. 
Keep it concise but educational (about 150 words)."""
        explanation = call_openrouter(prompt)
        
        return {
            "explanation": explanation,
            "topic": topic,
            "date": "2026-02-01"
        }
    
    elif action == 'models':
        # Compare context window sizes across popular models
        prompt = """Create a comparison table of popular AI models' context window sizes.
Include: Model name, Context Window size (in tokens), Release year, and Key notes.
Focus on models from OpenAI, Anthropic, Google, Meta, and others.
Format as clean markdown table."""
        comparison = call_openrouter(prompt)
        
        return {
            "comparison": comparison,
            "date": "2026-02-01"
        }
    
    elif action == 'calculate':
        text = data.get('text', '')
        model = data.get('model', 'GPT-4')
        
        if not text:
            return {"error": "No text provided"}
        
        prompt = f"""Given this text: "{text[:500]}..."
Estimate the token count. Also, if the model '{model}' has a context window of X tokens,
calculate what percentage of the context window this text uses.
Provide: token_count, percentage, and a brief interpretation."""
        analysis = call_openrouter(prompt)
        
        return {
            "analysis": analysis,
            "model": model,
            "date": "2026-02-01"
        }
    
    elif action == 'visualize':
        concept = data.get('concept', 'context window')
        prompt = f"Create a simple diagram showing how {concept} works in AI models, showing tokens flowing into a window with a limit"
        image_b64 = fetch_image(prompt)
        
        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-01"
            }
        else:
            return {"error": "Failed to generate visualization"}
    
    return {"error": f"Unknown action: {action}"}

# Metadata for projects.json
META = {
    "name": "AI Context Window Explorer",
    "description": "Learn about context windows in AI models: what they are, why they matter, and how different models compare",
    "category": "AI Education",
    "date": "2026-02-01"
}
