"""AI Superhero Forge - Create your own superhero with AI"""

from ..base import call_openrouter, fetch_image, extract_json

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        return {
            "message": "Welcome to the AI Superhero Forge! 🦸‍♂️",
            "description": "Generate a unique superhero with a name, powers, backstory, weakness, and visual appearance.",
            "actions": ["generate"],
            "date": "2026-02-04"
        }

    elif action == 'generate':
        name = data.get('name', '').strip()
        theme = data.get('theme', '').strip()

        # Build prompt for superhero profile in JSON format
        prompt = """Create a superhero character profile in JSON format with the following keys:
{
  "name": "Superhero name",
  "powers": ["power1", "power2", ...],
  "backstory": "A short backstory (2-3 sentences)",
  "weakness": "A weakness (one sentence)",
  "appearance": "A detailed visual description for image generation, including costume, colors, pose"
}
Make it fun, creative, and original.
"""
        if name:
            prompt += f"The superhero's name is {name}. "
        if theme:
            prompt += f"The theme/style is {theme}. "
        prompt += "Do not include any text outside the JSON object."

        # Generate text response
        response = call_openrouter(prompt)

        # Extract JSON
        profile = extract_json(response)
        if not profile:
            # Try to salvage by returning raw response
            return {
                "error": "Failed to generate a valid superhero profile. Please try again.",
                "raw_response": response,
                "date": "2026-02-04"
            }

        # Generate image based on appearance description
        appearance_desc = profile.get('appearance', f"A superhero named {profile.get('name', '')} with powers: {', '.join(profile.get('powers', []))}")
        image_b64 = fetch_image(appearance_desc, width=512, height=512)

        result = {
            "name": profile.get('name', 'Unknown'),
            "powers": profile.get('powers', []),
            "backstory": profile.get('backstory', ''),
            "weakness": profile.get('weakness', ''),
            "image": f"data:image/png;base64,{image_b64}" if image_b64 else None,
            "date": "2026-02-04"
        }
        return result

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Superhero Forge",
    "description": "Create your own superhero with AI: generate a name, powers, backstory, weakness, and avatar image",
    "category": "Fun",
    "date": "2026-02-04"
}
