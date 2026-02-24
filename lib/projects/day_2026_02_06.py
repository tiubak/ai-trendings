"""AI Mystic Fortune Teller - Discover what the future holds!"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        return {
            "message": "🔮 Welcome to the AI Mystic Fortune Teller!",
            "description": "Ask the AI oracle for a personalized fortune. Discover what the future holds!",
            "actions": ["tell_fortune", "visualize", "categories"],
            "date": "2026-02-06",
            "categories": ["general", "love", "career", "health", "wealth", "adventure"]
        }

    elif action == 'categories':
        # List available fortune categories
        return {
            "categories": ["general", "love", "career", "health", "wealth", "adventure"],
            "date": "2026-02-06"
        }

    elif action == 'tell_fortune':
        category = data.get('category', 'general').lower()
        name = data.get('name', '')
        question = data.get('question', '')

        # Build prompt based on category and optional personalization
        if name:
            prompt_intro = f"The mystic oracle gazes into the stars for {name}"
        else:
            prompt_intro = "The mystic oracle gazes into the stars"

        category_descriptions = {
            'general': 'a general fortune about what the future holds',
            'love': 'a romantic fortune about love and relationships',
            'career': 'a fortune about work, career path, and professional success',
            'health': 'a fortune about well-being, vitality, and health journey',
            'wealth': 'a fortune about prosperity, financial opportunities, and abundance',
            'adventure': 'a fortune about exciting journeys, new experiences, and daring quests'
        }

        topic = category_descriptions.get(category, category_descriptions['general'])

        if question:
            prompt = f"""{prompt_intro} and reveals an answer to the question: "{question}"
 Speak as a mystical fortune teller, using poetic, prophetic language.
 Include a mysterious element (crystals, stars, tea leaves, etc.).
 Keep it concise (2-3 sentences) but evocative.
 End with a cryptic warning or blessing."""
        else:
            prompt = f"""{prompt_intro} and reveals {topic}.
 Speak as a mystical fortune teller, using poetic, prophetic language.
 Include a mysterious element (crystals, stars, tea leaves, etc.).
 Keep it concise (2-3 sentences) but evocative.
 End with a cryptic warning or blessing."""

        fortune = call_openrouter(prompt)

        return {
            "fortune": fortune,
            "category": category,
            "name": name,
            "date": "2026-02-06"
        }

    elif action == 'visualize':
        # Generate a mystical image related to fortune telling
        concept = data.get('concept', 'mystical crystal ball showing the future')
        style = data.get('style', 'dreamy, ethereal, glowing, magical')

        prompt = f"A mystical, magical illustration: {concept}. Style: {style}. Soft glowing lights, stars, cosmic elements. High quality, enchanting."

        image_b64 = fetch_image(prompt, width=512, height=512)

        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-06"
            }
        else:
            return {"error": "Failed to generate visualization"}

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Mystic Fortune Teller",
    "description": "Discover what the future holds! Get personalized AI-generated fortunes with mystical visuals and categories like love, career, wealth, and adventure",
    "category": "Fun",
    "date": "2026-02-06"
}
