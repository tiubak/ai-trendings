"""AI Attention Explorer - Understand how transformers focus on relevant information"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        prompt = """Provide a friendly, beginner-friendly introduction to attention mechanisms in transformers.
Explain why attention was revolutionary, the basic idea (like focusing on relevant words), and its importance.
Keep it under 200 words, engaging, and accessible."""
        intro = call_openrouter(prompt)

        return {
            "intro": intro,
            "date": "2026-02-03",
            "project": "AI Attention Explorer",
            "actions": ["explain", "compare", "visualize", "example"]
        }

    elif action == 'explain':
        detail_level = data.get('level', 'intermediate')  # basic, intermediate, advanced

        if detail_level == 'basic':
            prompt = """Explain attention mechanisms in the simplest possible terms. Use an analogy (like reading a sentence and highlighting key words). No math equations, just intuition. 100 words max."""
        elif detail_level == 'intermediate':
            prompt = """Explain attention mechanisms with some technical detail but still accessible. Include:
- The concept of queries, keys, and values (Q, K, V)
- How attention scores are computed (dot product)
- How the model learns to focus
Avoid complex math notation but explain the process. 200 words."""
        else:  # advanced
            prompt = """Explain attention mechanisms with mathematical precision. Include:
- The scaled dot-product attention formula: Attention(Q,K,V) = softmax(QK^T/√d_k)V
- Why scaling is needed
- Multi-head attention and why it's used
- Position encodings and how attention is applied in transformers
Be technical but clear. 300 words."""

        explanation = call_openrouter(prompt)

        return {
            "explanation": explanation,
            "level": detail_level,
            "date": "2026-02-03"
        }

    elif action == 'compare':
        prompt = """Compare different types of attention mechanisms used in transformers:
1. Self-Attention (intra-attention)
2. Cross-Attention (encoder-decoder attention)
3. Multi-Head Attention
For each, explain:
- What it does
- Where it's used in a transformer model
- Why it's useful
Keep it concise (150 words total)."""
        comparison = call_openrouter(prompt)

        return {
            "comparison": comparison,
            "date": "2026-02-03"
        }

    elif action == 'visualize':
        concept = data.get('concept', 'attention mechanism')
        prompt = f"A clear, educational diagram showing how {concept} works in a transformer. Use labeled arrows, boxes for 'Query', 'Key', 'Value', and show the attention weights matrix. Clean, modern, technical illustration style."
        image_b64 = fetch_image(prompt)

        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-03"
            }
        else:
            return {"error": "Failed to generate visualization"}

    elif action == 'example':
        # Provide a concrete example of attention in action
        sentence = data.get('sentence', 'The cat sat on the mat')
        prompt = f"""Given the sentence: "{sentence}"
Explain how a transformer's attention mechanism would process this sentence.
Show which words attend to which others and why (based on meaning/grammar).
Provide a simple attention matrix visualization description.
Be concrete and show the connections."""
        example = call_openrouter(prompt)

        return {
            "example": example,
            "sentence": sentence,
            "date": "2026-02-03"
        }

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Attention Explorer",
    "description": "Explore how attention mechanisms work in transformers: the math, intuition, and how AI focuses on relevant information",
    "category": "AI Education",
    "date": "2026-02-03"
}
