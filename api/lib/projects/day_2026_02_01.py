"""AI Model Comparator & Evolution Explorer - February 1, 2026

Compare major AI language models, explore their evolution, and understand
the key differences in architecture, capabilities, and training approaches.
"""

from ..base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'start', 'compare', 'timeline', 'visualize', 'quiz'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    
    if action == 'start':
        """Initialize the project with overview and available models."""
        prompt = """Provide a comprehensive overview of major AI language models as of 2026.
        
        Include these models: GPT-4, Claude 3.5 Sonnet, Gemini 2.0, Llama 3.3, Mistral Large, 
        Command R+, and any significant 2026 releases.
        
        For each model, briefly cover:
        - Release date and developer
        - Key strengths and specialties
        - Context window size
        - Parameter count (if known)
        - Primary use cases
        
        Format as a clear, educational overview suitable for developers and AI enthusiasts.
        Keep it informative but not too lengthy (around 500 words)."""
        
        overview = call_openrouter(prompt)
        
        return {
            "overview": overview,
            "models": [
                {"id": "gpt4", "name": "GPT-4", "developer": "OpenAI"},
                {"id": "claude", "name": "Claude 3.5 Sonnet", "developer": "Anthropic"},
                {"id": "gemini", "name": "Gemini 2.0", "developer": "Google DeepMind"},
                {"id": "llama", "name": "Llama 3.3", "developer": "Meta"},
                {"id": "mistral", "name": "Mistral Large", "developer": "Mistral AI"},
                {"id": "command", "name": "Command R+", "developer": "Cohere"}
            ]
        }
    
    elif action == 'compare':
        """Compare two specific models in detail."""
        model1 = data.get('model1', 'gpt4')
        model2 = data.get('model2', 'claude')
        
        prompt = f"""Compare {model1} and {model2} in detail across these dimensions:
        
        1. Reasoning & problem-solving capabilities
        2. Code generation quality and language support
        3. Multilingual performance
        4. Creative writing and content creation
        5. Mathematical and analytical tasks
        6. Context window and memory management
        7. Safety and alignment approaches
        8. API pricing and accessibility
        9. Known limitations or weaknesses
        10. Best use cases and recommendations
        
        Provide specific examples where one model excels over the other.
        Be objective and based on known benchmarks and user experiences as of early 2026."""
        
        comparison = call_openrouter(prompt)
        
        return {
            "comparison": comparison,
            "model1": model1,
            "model2": model2
        }
    
    elif action == 'timeline':
        """Get historical evolution of AI language models."""
        year = data.get('year', 'all')
        
        if year == 'all':
            prompt = """Create a chronological timeline of major AI language model breakthroughs from 2018-2026:
            
            Include:
            - GPT-2 (2019)
            - GPT-3 (2020)
            - GPT-3.5/ChatGPT (2022)
            - GPT-4 (2023)
            - Claude 1-3 series (2023-2025)
            - Llama 1-3 series (2023-2025)
            - Gemini 1-2 series (2023-2026)
            - Mistral 7B, Mixtral, Large (2023-2025)
            - Command R+ (2024)
            - Any 2026 releases so far
            
            For each, note:
            - Release date
            - Key innovation or breakthrough
            - Parameter count or size milestone
            - Impact on the field
            
            Format as a clear timeline with brief explanations for each milestone."""
        else:
            prompt = f"Focus on AI model developments in {year}. What major models were released and what were their significance?"
        
        timeline = call_openrouter(prompt)
        
        return {"timeline": timeline, "year": year}
    
    elif action == 'visualize':
        """Generate a visual diagram of model architecture or comparison."""
        viz_type = data.get('type', 'architecture')
        model = data.get('model', 'transformer')
        
        prompts = {
            'architecture': f"Technical diagram showing the architecture of {model} language model, with labeled components like attention heads, feed-forward layers, embedding layers, clean vector illustration style",
            'comparison': "Information visualization comparing AI models across dimensions like parameters, context window, release date, capabilities, using bar charts and metric graphs, infographic style",
            'timeline': "Chronological timeline visualization of AI language model evolution from 2018 to 2026, showing major releases and breakthroughs, clean timeline infographic",
            'attention': "Educational diagram showing how attention mechanism works in transformers, with flow arrows and highlighted token relationships, clear and simple"
        }
        
        prompt = prompts.get(viz_type, prompts['architecture'])
        image_url = generate_image_url(prompt, width=1024, height=768)
        
        return {
            "image_url": image_url,
            "type": viz_type,
            "prompt": prompt
        }
    
    elif action == 'quiz':
        """Generate an interactive quiz about AI models."""
        prompt = """Generate 5 multiple-choice quiz questions testing knowledge about AI language models.
        
        Topics should include:
        - Model release dates and chronology
        - Model capabilities and specialties
        - Technical specifications
        - Developer companies and research labs
        - Notable benchmarks and achievements
        
        Format as JSON array with this structure:
        [
          {
            "question": "string",
            "options": ["A)", "B)", "C)", "D)"],
            "correct": 0-3 (index of correct answer),
            "explanation": "Brief explanation of the answer"
          }
        ]
        
        Make questions challenging but fair for someone who's read the overview."""
        
        result = call_openrouter(prompt)
        quiz_data = extract_json(result)
        
        if not quiz_data:
            # Fallback if JSON extraction fails
            quiz_data = []
        
        return {"quiz": quiz_data}
    
    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Model Comparator",
    "description": "Compare major AI language models, explore their evolution, and understand key differences in capabilities and architecture.",
    "category": "AI Education",
    "tags": ["comparison", "models", "benchmark", "timeline", "educational"]
}
