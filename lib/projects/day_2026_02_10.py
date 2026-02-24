"""AI Ice Cream Flavor Generator - Create delicious and creative ice cream flavors with AI"""

from ..base import call_openrouter, fetch_image, extract_json

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        return {
            "message": "Welcome to the AI Ice Cream Flavor Generator! 🍦",
            "description": "Generate unique and delicious ice cream flavor ideas, including a creative name, description, ingredients, and a visual of the ice cream.",
            "actions": ["generate"],
            "date": "2026-02-10"
        }

    elif action == 'generate':
        # Optional inputs: flavor_hint, dietary, season
        flavor_hint = data.get('flavor_hint', '').strip()
        dietary = data.get('dietary', '').strip()
        season = data.get('season', '').strip()

        prompt = """Create an ice cream flavor profile in JSON format with these keys:
{
  "name": "Creative flavor name",
  "description": "A tasty description of the flavor, texture, and experience (2-3 sentences)",
  "ingredients": ["ingredient1", "ingredient2", ...],
  "fun_fact": "A fun fact about the flavor or its inspiration (optional)",
  "image_prompt": "A detailed visual description for generating an appetizing image of this ice cream in a cone or bowl, with toppings, lighting, style"
}
Make it delicious, creative, and fun.
"""
        extra = []
        if flavor_hint:
            extra.append(f"Flavor hint or base: {flavor_hint}")
        if dietary:
            extra.append(f"Dietary consideration: {dietary} (e.g., vegan, dairy-free, low-sugar)")
        if season:
            extra.append(f"Season: {season}")
        if extra:
            prompt += "Take into account: " + "; ".join(extra) + ". "
        prompt += "Do not include any text outside the JSON object."

        response = call_openrouter(prompt)
        profile = extract_json(response)
        if not profile:
            return {
                "error": "Failed to generate a valid flavor profile. Please try again.",
                "raw_response": response,
                "date": "2026-02-10"
            }

        # Generate image using image_prompt
        image_prompt = profile.get('image_prompt', f"Ice cream flavor: {profile.get('name')}")
        image_b64 = fetch_image(image_prompt, width=512, height=512)

        result = {
            "name": profile.get('name', 'Mystery Flavor'),
            "description": profile.get('description', ''),
            "ingredients": profile.get('ingredients', []),
            "fun_fact": profile.get('fun_fact', ''),
            "image": f"data:image/png;base64,{image_b64}" if image_b64 else None,
            "date": "2026-02-10"
        }
        return result

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Ice Cream Flavor Generator",
    "description": "Generate creative and delicious ice cream flavor ideas with AI, including name, description, ingredients, and visual representation",
    "category": "Fun",
    "date": "2026-02-10"
}
