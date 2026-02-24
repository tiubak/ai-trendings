"""AI Tokenization Explorer - Understanding how AI models break down text into tokens"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        intro = """Tokenization is a fundamental concept in AI language models - it's the process of breaking down text into smaller units (tokens) that the model can understand and process.

Different AI models use different tokenization approaches, and understanding tokens helps you:

- Estimate costs (most APIs charge per token)
- Manage context window limits
- Optimize prompts for efficiency
- Understand why some words are handled differently across models

This explorer lets you:
- See how text gets tokenized
- Compare token counts across models
- Visualize the tokenization process
- Estimate processing costs

Enter some text and explore!"""
        
        return {
            "intro": intro,
            "date": "2026-02-09",
            "project": "AI Tokenization Explorer",
            "actions": ["tokenize", "compare", "visualize", "cost_estimator"],
            "example_texts": [
                "Hello world!",
                "The quick brown fox jumps over the lazy dog.",
                "Artificial intelligence is transforming how we interact with technology.",
                "🔬 This emoji and special chars: @#$%^&*()",
                "Supercalifragilisticexpialidocious"
            ]
        }

    elif action == 'tokenize':
        """Tokenize text and show the breakdown."""
        text = data.get('text', 'Hello world!')
        model = data.get('model', 'gpt-4')  # Could be gpt-4, claude, llama, etc.
        
        # Use OpenRouter to get tokenization info
        # For this demo, we'll estimate tokens using a simple algorithm
        # In production, you'd use tiktoken or the actual model's tokenizer
        
        prompt = f"""Analyze this text and break it down into tokens as if you were tokenizing it for a {model}-style transformer model.

Text: "{text}"

Provide:
1. A list of tokens (including special tokens like spaces, punctuation marked with symbols like 'Ġ' for GPT-style)
2. Token count
3. Notes about how this model's tokenizer works (BPE, WordPiece, SentencePiece, etc.)

Make it educational and show the reasoning."""
        
        tokenization = call_openrouter(prompt)
        
        # Simple token count estimation (rough)
        # Real implementation would use actual tokenizer
        estimated_count = len(text.split()) * 1.3  # Very rough estimate
        
        return {
            "text": text,
            "model": model,
            "tokenization_analysis": tokenization,
            "estimated_token_count": int(estimated_count),
            "character_count": len(text),
            "date": "2026-02-09"
        }

    elif action == 'compare':
        """Compare tokenization across different models."""
        text = data.get('text', 'The quick brown fox')
        models = data.get('models', ['GPT-4', 'Claude 3', 'LLaMA 2', 'Gemini'])
        
        models_list = ', '.join(models)
        prompt = f"""Compare how these different AI models would tokenize this text:

Text: "{text}"

Models: {models_list}

For each model, provide:
- Approximate token count
- Notable tokenization quirks (e.g., how GPT handles spaces, how BERT uses WordPiece)
- Whether it would split or keep certain words together

Present as a comparison table or structured list."""
        
        comparison = call_openrouter(prompt)
        
        return {
            "text": text,
            "models": models,
            "comparison": comparison,
            "date": "2026-02-09"
        }

    elif action == 'cost_estimator':
        """Estimate processing cost based on token counts."""
        text = data.get('text', '')
        model = data.get('model', 'gpt-4')
        operations = data.get('operations', ['input', 'output'])  # input tokens, output tokens
        
        # Get token count first
        token_result = handle('tokenize', {'text': text, 'model': model})
        token_count = token_result.get('estimated_token_count', 0)
        
        # Cost data per 1K tokens (these should be current but we'll use estimates)
        cost_rates = {
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
            'claude-3-opus': {'input': 0.015, 'output': 0.075},
            'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
            'llama-2-70b': {'input': 0.0007, 'output': 0.0007}
        }
        
        rates = cost_rates.get(model, {'input': 0.01, 'output': 0.01})
        
        estimated_cost = {}
        if 'input' in operations:
            estimated_cost['input'] = (token_count / 1000) * rates['input']
        if 'output' in operations:
            # Assume similar length output unless specified
            output_tokens = data.get('output_tokens', token_count)
            estimated_cost['output'] = (output_tokens / 1000) * rates['output']
        
        estimated_cost['total'] = estimated_cost.get('input', 0) + estimated_cost.get('output', 0)
        
        return {
            "text": text,
            "model": model,
            "token_count": token_count,
            "cost_breakdown_usd": estimated_cost,
            "rates_used": rates,
            "date": "2026-02-09"
        }

    elif action == 'visualize':
        """Generate a visualization of tokenization process."""
        text = data.get('text', 'AI is amazing')
        focus = data.get('focus', 'bpe')  # bpe, attention, embeddings
        
        if focus == 'bpe':
            viz_prompt = f"""Create an educational diagram showing Byte Pair Encoding (BPE) tokenization process.

Show step-by-step how the text "{text}" gets broken down into subword tokens.

Use a flow diagram style:
1. Original text as characters
2. Initial vocabulary
3. Merging pairs step by step
4. Final tokens

Style: clean, technical, educational, blue color scheme, with arrows showing merges."""
        else:
            viz_prompt = f"""Create an educational visualization of how transformers process tokens.

Show: "{text}" being converted to embeddings, then through attention layers.

Style: clean, technical diagram, layered architecture, neural network style."""
        
        image_b64 = fetch_image(viz_prompt, width=800, height=500)
        
        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "focus": focus,
                "date": "2026-02-09"
            }
        else:
            return {"error": "Failed to generate visualization"}

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Tokenization Explorer",
    "description": "Understand how AI models break down text into tokens: learn about tokenization algorithms, compare across models, estimate costs, and visualize the process",
    "category": "AI Education",
    "date": "2026-02-09"
}
