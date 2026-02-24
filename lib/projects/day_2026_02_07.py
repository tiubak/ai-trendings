"""AI Model Collapse Simulator - Demonstrate how training on AI-generated data leads to degradation"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        intro = """Model collapse is a phenomenon where AI models degrade in quality when trained on their own synthetic outputs over multiple generations.

This simulator lets you explore how an AI's responses become less diverse and accurate when it repeatedly trains on its own data.

**How it works:**
1. We start with a "clean" AI model (OpenRouter's free model)
2. Generate an initial response to a prompt
3. Feed that response back as training data (simulated)
4. Repeat for multiple generations
5. Track diversity and quality degradation

Try it yourself!"""
        
        return {
            "intro": intro,
            "date": "2026-02-07",
            "project": "AI Model Collapse Simulator",
            "actions": ["simulate", "compare", "visualize", "explain"],
            "generations": data.get('generations', 5)
        }

    elif action == 'simulate':
        """Run a model collapse simulation."""
        prompt = data.get('prompt', 'Explain quantum computing in simple terms')
        generations = min(data.get('generations', 5), 10)  # Max 10 for demo
        
        results = []
        current_prompt = prompt
        
        for gen in range(generations):
            # Simulate "training on previous output" by adding context
            if gen > 0:
                # Add previous output to prompt to simulate contamination
                prev_output = results[-1]['output']
                current_prompt = f"""Based on this previous explanation: "{prev_output}"

Now explain this topic again, but try to improve upon it:

{prompt}"""
            
            # Generate response using OpenRouter
            output = call_openrouter(current_prompt)
            
            # Calculate a simple "quality score" based on length and complexity
            # In reality, this would require human eval or multiple metrics
            words = len(output.split())
            diversity_hint = "varied" if words > 50 else "limited"
            
            results.append({
                "generation": gen + 1,
                "prompt_used": current_prompt[:100] + "..." if len(current_prompt) > 100 else current_prompt,
                "output": output,
                "word_count": words,
                "diversity_hint": diversity_hint
            })
        
        return {
            "simulation_results": results,
            "summary": f"Completed {generations} generations. Observe how responses may become repetitive or simplified over time.",
            "date": "2026-02-07"
        }

    elif action == 'explain':
        """Explain model collapse in detail."""
        detail_level = data.get('level', 'intermediate')
        
        if detail_level == 'basic':
            prompt = """Explain AI model collapse in the simplest terms:
- What happens when AI is trained on its own outputs?
- Why does quality get worse over time?
- Use an analogy (like copying a photocopy of a photocopy)
Keep it very simple, under 150 words."""
        elif detail_level == 'intermediate':
            prompt = """Explain AI model collapse with moderate technical detail:
- The mechanism: distribution shift, mode collapse, error accumulation
- Why synthetic data lacks diversity
- Real-world examples (GPT trained on GPT output, etc.)
- Mitigation strategies (curated data, human feedback)
Keep it under 250 words."""
        else:  # advanced
            prompt = """Provide a technical deep-dive on model collapse:
- Mathematical formulation: distribution P_data vs P_model divergence
- The theoretical inevitability under certain conditions
- Empirical studies and benchmarks
- Advanced mitigation techniques (data mixing, entropy regularization)
- Connection to natural language drift
Be precise but accessible, ~300-400 words."""
        
        explanation = call_openrouter(prompt)
        
        return {
            "explanation": explanation,
            "level": detail_level,
            "date": "2026-02-07"
        }

    elif action == 'visualize':
        """Generate a diagram of model collapse."""
        concept = data.get('concept', 'model collapse process')
        prompt = f"""Create a clear educational diagram showing the process of AI model collapse.
Show three stages side by side:
1. Initial training on diverse real data → diverse outputs
2. Mixing real + synthetic → some repetition
3. Training only on synthetic → collapsed, repetitive outputs
Use arrows, labels, and show how variety decreases.
Style: clean, modern, technical illustration, blue/red gradient to show degradation."""
        
        image_b64 = fetch_image(prompt, width=800, height=600)
        
        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-07",
                "concept": concept
            }
        else:
            return {"error": "Failed to generate visualization"}

    elif action == 'compare':
        """Compare with other AI problems."""
        prompt = """Compare and contrast these related AI training issues:
1. Model Collapse
2. Catastrophic Forgetting
3. Mode Collapse (in GANs)
4. Distribution Shift
For each, explain:
- What it is
- When it happens
- How to detect it
- How to mitigate it
Create a concise comparison table in text format."""
        
        comparison = call_openrouter(prompt)
        
        return {
            "comparison": comparison,
            "date": "2026-02-07"
        }

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Model Collapse Simulator",
    "description": "Explore the phenomenon where AI models degrade when trained on their own synthetic outputs through interactive simulations",
    "category": "AI Education",
    "date": "2026-02-07"
}
