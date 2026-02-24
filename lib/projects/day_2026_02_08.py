"""AI Mystic Oracle - Get mystical predictions and read your fortune"""

from ..base import call_openrouter, call_gTTS, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        return {
            "message": "🔮 Welcome to the AI Mystic Oracle",
            "description": "Ask questions about your future and receive mystical predictions from the AI oracle. Includes TTS narration!",
            "actions": ["fortune", "tarot", "crystal_ball", "horoscope"],
            "date": "2026-02-08"
        }

    elif action == 'fortune':
        question = data.get('question', 'What does my future hold?')
        prompt = f"""You are a mystical oracle speaking in a mysterious, poetic tone. 
The user asks: "{question}"
Provide a short, enigmatic fortune (3-5 sentences) that feels mystical and thought-provoking.
Use imagery of stars, fog, paths, or cosmic forces. End with a hint of both hope and caution."""
        fortune_text = call_openrouter(prompt)

        # Generate TTS using gTTS (slow, mysterious voice effect through text style)
        audio_base64 = call_gTTS(fortune_text)

        audio_url = None
        if audio_base64:
            audio_url = f"data:audio/mp3;base64,{audio_base64}"

        return {
            "fortune": fortune_text,
            "question": question,
            "audio": audio_url,
            "date": "2026-02-08"
        }

    elif action == 'tarot':
        spread = data.get('spread', 'single')  # single, three, five
        
        prompt = f"""Perform a {spread}-card tarot reading for the user.
For each card drawn, provide:
1. Card name (e.g., The Fool, The High Priestess, Knight of Wands)
2. Whether it's upright or reversed
3. A brief interpretation (1-2 sentences) of what it means for their situation
Keep it mystical and insightful but not frightening. Use traditional Rider-Waite-Smith deck."""
        reading = call_openrouter(prompt)

        # Generate a mystical visual: crystal ball with tarot cards
        image_prompt = "A mystical crystal ball floating on a velvet cloth, with tarot cards spread around it, soft candlelight, ethereal fog, magical atmosphere"
        image_b64 = fetch_image(image_prompt)

        return {
            "reading": reading,
            "spread": spread,
            "image": f"data:image/png;base64,{image_b64}" if image_b64 else None,
            "date": "2026-02-08"
        }

    elif action == 'crystal_ball':
        topic = data.get('topic', 'love')
        prompt = f"""Peer into the crystal ball and reveal what you see about the user's {topic}.
Write 3-4 short, poetic visions or symbols that appear in the mist.
Each should be cryptic but meaningful, like: 'I see a rose wilting yet blooming' or 'A river flows backward under a blood moon.'
Make it mysterious and visually evocative."""
        vision = call_openrouter(prompt)

        # Generate crystal ball image
        image_prompt = f"A glowing crystal ball showing visions of {topic}, mystical fog inside the ball, ethereal light, magical"
        image_b64 = fetch_image(image_prompt)

        return {
            "vision": vision,
            "topic": topic,
            "image": f"data:image/png;base64,{image_b64}" if image_b64 else None,
            "date": "2026-02-08"
        }

    elif action == 'horoscope':
        zodiac = data.get('zodiac', 'Aries')
        prompt = f"""Write a daily horoscope for {zodiac}.
Include: general outlook, love, career, and a lucky number/color.
Keep it concise, positive, and mystical. End with a short advice sentence."""
        horoscope = call_openrouter(prompt)

        # Generate TTS with horoscope
        audio_base64 = call_gTTS(horoscope)
        audio_url = f"data:audio/mp3;base64,{audio_base64}" if audio_base64 else None

        return {
            "horoscope": horoscope,
            "zodiac": zodiac,
            "audio": audio_url,
            "date": "2026-02-08"
        }

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Mystic Oracle",
    "description": "Ask questions about your future and receive mystical predictions, tarot readings, crystal ball visions, and daily horoscopes from the AI oracle",
    "category": "Fun",
    "date": "2026-02-08"
}
