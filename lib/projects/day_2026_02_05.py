"""Emerging AI Architectures Explorer - Discover what's beyond transformers"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        prompt = """Provide an engaging introduction to emerging AI architectures beyond the transformer.
Cover why researchers are looking beyond transformers, what limitations they address (e.g., computational efficiency, long context, interpretability), and mention a few key alternatives like State Space Models (SSMs), neuro-symbolic systems, and others.
Keep it around 150-200 words for a general audience."""
        intro = call_openrouter(prompt)

        return {
            "intro": intro,
            "date": "2026-02-05",
            "project": "Emerging AI Architectures Explorer",
            "actions": ["explain", "compare", "visualize", "example"]
        }

    elif action == 'explain':
        architecture = data.get('architecture', 'State Space Models')
        level = data.get('level', 'intermediate')  # basic, intermediate, advanced

        if level == 'basic':
            prompt = f"""Explain {architecture} in the simplest possible terms. Use everyday analogies. No technical jargon. 100 words max."""
        elif level == 'intermediate':
            prompt = f"""Explain {architecture} with some technical detail but still accessible. Cover the key ideas and how it differs from transformers. About 200 words."""
        else:  # advanced
            prompt = f"""Provide a technical explanation of {architecture}, including mathematical foundations if relevant. Discuss its advantages, trade-offs, and current research directions. 300 words."""

        explanation = call_openrouter(prompt)

        return {
            "explanation": explanation,
            "architecture": architecture,
            "level": level,
            "date": "2026-02-05"
        }

    elif action == 'compare':
        prompt = """Compare the following emerging AI architectures: State Space Models (SSMs), neuro-symbolic AI, and any others you think are relevant.
For each, discuss: key principles, advantages over transformers, current research status, and potential applications.
Keep it concise, about 200 words. Use a structured format with headings."""
        comparison = call_openrouter(prompt)

        return {
            "comparison": comparison,
            "date": "2026-02-05"
        }

    elif action == 'visualize':
        concept = data.get('concept', 'emerging AI architecture')
        prompt = f"Create a clean, educational diagram showing the architecture of {concept}. Use labeled components, flow arrows, and a modern technical illustration style."
        image_b64 = fetch_image(prompt)

        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-05"
            }
        else:
            return {"error": "Failed to generate visualization"}

    elif action == 'example':
        architecture = data.get('architecture', 'State Space Models')
        prompt = f"""Provide a concrete example of how {architecture} works in practice.
Describe a specific task or application where this architecture shines, and walk through the steps or mechanisms.
Keep it clear and educational, about 150 words."""
        example = call_openrouter(prompt)

        return {
            "example": example,
            "architecture": architecture,
            "date": "2026-02-05"
        }

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "Emerging AI Architectures Explorer",
    "description": "Explore AI architectures beyond transformers: state-space models, neuro-symbolic systems, and the future of AI design",
    "category": "AI Education",
    "date": "2026-02-05"
}
