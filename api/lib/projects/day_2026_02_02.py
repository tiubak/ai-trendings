"""AI Attention Mechanism Explorer - February 2, 2026

An interactive educational tool that explains how attention mechanisms work
in transformer architectures. Users can visualize attention weights, understand
the self-attention computation, and explore how queries, keys, and values interact
to produce contextual representations.
"""

from ..base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'start', 'explain_concept', 'visualize_attention', 'compute_attention', 'analogy'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    
    if action == 'start':
        """Initialize with overview of attention mechanism."""
        prompt = """Provide a clear, comprehensive introduction to the attention mechanism in transformer architectures.
        
        Cover these key points:
        1. Why attention was needed (limitations of RNNs and fixed context)
        2. The core idea: allowing the model to focus on different parts of the input
        3. The three key components: Query (Q), Key (K), and Value (V)
        4. How self-attention works with a simple example
        5. The scaled dot-product attention formula
        6. Multi-head attention and why it's useful
        7. Real-world impact: how attention enabled GPT, BERT, and modern LLMs
        
        Make it accessible to developers with basic ML knowledge but not deep expertise.
        Use analogies where helpful. Keep it around 600-800 words for an educational tool."""
        
        overview = call_openrouter(prompt)
        
        return {
            "overview": overview,
            "key_concepts": [
                {"term": "Query", "symbol": "Q", "description": "What we're looking for"},
                {"term": "Key", "symbol": "K", "description": "What we're matching against"},
                {"term": "Value", "symbol": "V", "description": "What we actually retrieve"},
                {"term": "Attention Score", "symbol": "Attention(Q,K,V)", "description": "Weighted sum of values based on query-key similarity"}
            ]
        }
    
    elif action == 'explain_concept':
        """Explain a specific attention concept in detail."""
        concept = data.get('concept', 'self-attention')
        
        concept_prompts = {
            'self-attention': "Explain self-attention in transformers: how each token attends to all other tokens in the same sequence to build contextual understanding. Include the computational steps and a simple numeric example.",
            'scaled-dot-product': "Explain scaled dot-product attention: the formula sqrt(d_k), why scaling is necessary, and how it prevents gradient vanishing. Include the softmax step.",
            'multi-head': "Explain multi-head attention: why multiple attention heads are used, how they capture different relationship types, and how their outputs are combined.",
            'cross-attention': "Explain cross-attention in encoder-decoder architectures: how the decoder attends to encoder outputs. Contrast with self-attention.",
            'masked-attention': "Explain masked attention (causal attention) in decoder-only models like GPT: how it prevents attending to future tokens during training."
        }
        
        prompt = concept_prompts.get(concept, concept_prompts['self-attention'])
        explanation = call_openrouter(prompt)
        
        return {
            "explanation": explanation,
            "concept": concept
        }
    
    elif action == 'visualize_attention':
        """Generate a visual representation of attention weights."""
        viz_type = data.get('type', 'heatmap')
        context = data.get('context', 'The cat sat on the mat')
        
        viz_prompts = {
            'heatmap': f"Create an attention heatmap visualization for the sentence: '{context}'. Show a matrix where rows and columns are tokens, and colors represent attention weights. Include token labels on both axes. Make it look like a professional AI research diagram, clean and colorful.",
            'architecture': "Draw a schematic diagram of the transformer attention mechanism. Show Q, K, V vectors flowing into an attention block, with attention weights connecting tokens. Include the scaling factor and softmax step. Technical illustration style, clear labels.",
            'multi-head': "Illustrate multi-head attention with 8 parallel attention heads. Show how each head creates different representation subspaces, then show the concatenation and final linear projection. Infographic style with colors distinguishing heads.",
            'flow': "Create a step-by-step flow diagram of attention computation: from input embeddings → Q/K/V projections → scaled dot-product → softmax → weighted sum. Show shapes at each stage. Educational diagram style."
        }
        
        prompt = viz_prompts.get(viz_type, viz_prompts['heatmap'])
        image_url = generate_image_url(prompt, width=1200, height=800)
        
        return {
            "image_url": image_url,
            "type": viz_type,
            "prompt": prompt,
            "context": context
        }
    
    elif action == 'compute_attention':
        """Compute attention scores for a simple example (toy calculation)."""
        # This could do actual computation for demo purposes
        example = data.get('example', 'simple')
        
        if example == 'simple':
            prompt = """Provide a step-by-step numerical example of attention computation with small matrices (3 tokens, 4-dimensional).
            
            Show:
            - Initial token embeddings (3x4 matrix)
            - Random Q, K, V projections
            - Q*K^T computation
            - Scaling by sqrt(d_k)
            - Softmax to get attention weights
            - Final weighted sum of values
            
            Use simple integer-like numbers (1, 2, -1, 0.5, etc.) for clarity.
            Format with clear math notation and intermediate results so a user can follow the computation."""
        else:
            prompt = "Explain how attention probabilities are computed in detail, with the mathematical formulas and a clear explanation of each step."
        
        computation = call_openrouter(prompt)
        
        return {
            "computation": computation,
            "example": example
        }
    
    elif action == 'analogy':
        """Provide an intuitive analogy for attention."""
        prompt = "Provide a clear, relatable analogy for how attention mechanisms work. Compare it to something everyday (like reading a book and focusing on certain words, or a spotlight on a stage, or filtering noise to hear a conversation). Explain the analogy thoroughly, mapping each element (query, key, value, attention) to parts of the analogy."
        
        analogy = call_openrouter(prompt)
        
        return {
            "analogy": analogy
        }
    
    elif action == 'quiz':
        """Generate a quiz about attention mechanisms."""
        prompt = """Generate 5 multiple-choice quiz questions about attention mechanisms in transformers.
        
        Topics:
        - Purpose and motivation for attention
        - Q, K, V definitions and roles
        - Mathematical formula and scaling
        - Multi-head attention
        - Applications in encoder/decoder models
        
        Format as JSON array:
        [
          {
            "question": "string",
            "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "correct": 0-3,
            "explanation": "Brief explanation"
          }
        ]
        
        Difficulty: medium, for someone learning about transformers."""
        
        result = call_openrouter(prompt)
        quiz_data = extract_json(result)
        
        if not quiz_data:
            quiz_data = []
        
        return {"quiz": quiz_data}
    
    else:
        return {"error": f"Unknown action: {action}"}


META = {
    "name": "AI Attention Mechanism Explorer",
    "description": "An interactive educational tool that explains how attention mechanisms work in transformer architectures. Visualize attention weights, understand self-attention computation, and explore Q/K/V dynamics.",
    "category": "AI Education",
    "tags": ["transformers", "attention", "neural-networks", "educational", "visualization"],
    "difficulty": "intermediate"
}
