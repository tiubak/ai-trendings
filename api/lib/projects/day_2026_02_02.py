"""AI Stand-up Comedian - Jokes, Roasts, and Stories with Voice"""

from ..base import call_openrouter, call_gTTS

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        return {
            "message": "Welcome to the AI Stand-up Comedian! 🤖😂",
            "description": "Generate jokes, roasts, and funny stories with AI-powered voice narration.",
            "actions": ["joke", "roast", "story", "tts_test"],
            "date": "2026-02-02"
        }

    elif action == 'joke':
        topic = data.get('topic', 'programming')
        prompt = f"Tell me a short, clean, and funny joke about {topic}. Keep it under 2 sentences."
        joke_text = call_openrouter(prompt)

        # Generate TTS for the joke using gTTS (Google TTS, free, no API key)
        audio_base64 = call_gTTS(joke_text)

        # Check if audio was generated successfully
        audio_url = None
        if audio_base64:
            # gTTS returns MP3
            audio_url = f"data:audio/mp3;base64,{audio_base64}"

        return {
            "joke": joke_text,
            "topic": topic,
            "audio": audio_url,
            "date": "2026-02-02"
        }

    elif action == 'roast':
        target = data.get('target', 'the audience')
        prompt = f"Give a playful, light-hearted roast of {target}. Keep it friendly and short."
        roast_text = call_openrouter(prompt)

        # Generate TTS using gTTS (Google TTS, free, no API key)
        audio_base64 = call_gTTS(roast_text)

        audio_url = None
        if audio_base64:
            audio_url = f"data:audio/mp3;base64,{audio_base64}"

        return {
            "roast": roast_text,
            "target": target,
            "audio": audio_url,
            "date": "2026-02-02"
        }

    elif action == 'story':
        characters = data.get('characters', 'a cat and a robot')
        prompt = f"Write a very short funny story (3-4 sentences) about {characters}. Include a punchline."
        story_text = call_openrouter(prompt)

        # Generate TTS using gTTS (Google TTS, free, no API key)
        audio_base64 = call_gTTS(story_text)

        audio_url = None
        if audio_base64:
            audio_url = f"data:audio/mp3;base64,{audio_base64}"

        return {
            "story": story_text,
            "characters": characters,
            "audio": audio_url,
            "date": "2026-02-02"
        }

    elif action == 'tts_test':
        # Direct test of gTTS
        test_text = data.get('text', 'Hello, this is a test of text-to-speech.')
        audio_base64 = call_gTTS(test_text)

        if not audio_base64:
            return {
                "success": False,
                "message": "TTS generation failed",
                "date": "2026-02-02"
            }
        else:
            return {
                "success": True,
                "message": "TTS generated successfully using gTTS (Google TTS, free, no API key required)!",
                "audio": f"data:audio/mp3;base64,{audio_base64}",
                "text": test_text,
                "date": "2026-02-02"
            }

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Stand-up Comedian",
    "description": "Generate jokes, roasts, and funny stories with AI-powered voice narration using Google TTS (gTTS - free, no API key required)",
    "category": "Fun",
    "date": "2026-02-02"
}
