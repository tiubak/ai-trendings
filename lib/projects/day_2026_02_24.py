"""AI Adventure Game Master - Embark on an AI-generated interactive adventure!"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        # Initialize a new adventure
        genre = data.get('genre', 'fantasy').lower()
        character = data.get('character', 'adventurer')

        # Generate opening scene
        prompt = f"""You are a game master for an interactive {genre} adventure.
Write the opening scene of an adventure where the protagonist is a {character}.
Set the scene with vivid sensory details (sights, sounds, smells).
Introduce a clear situation or challenge.
End with exactly 3 distinct choices for what to do next.
Format: Scene description, then choices numbered 1, 2, 3 on separate lines."""

        scene = call_openrouter(prompt)

        # Parse choices (simple extraction)
        lines = scene.strip().split('\n')
        choices = []
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.')):
                choices.append(line.strip()[2:].strip())

        return {
            "scene": scene,
            "genre": genre,
            "character": character,
            "choices": choices[:3],  # Ensure exactly 3
            "history": [],  # Track story progression
            "date": "2026-02-24"
        }

    elif action == 'choose':
        # Continue the story based on user's choice
        choice_index = data.get('choice', 0)
        history = data.get('history', [])
        genre = data.get('genre', 'fantasy')
        character = data.get('character', 'adventurer')
        previous_scene = data.get('previous_scene', '')

        # Build context from history (last few entries)
        context = f"Genre: {genre}. Character: {character}.\n"
        if history:
            context += "Recent story:\n"
            for i, entry in enumerate(history[-3:], 1):  # Last 3 scenes
                context += f"{i}. {entry['summary']}\n"

        prompt = f"""You are a game master for an interactive {genre} adventure.
Previous scene: {previous_scene}
The player chose option {choice_index + 1}.

Write the next scene of the adventure.
Continue the story naturally based on the choice.
Keep the same tone and style.
After the scene description, provide exactly 3 new distinct choices.
Format: Scene description, then choices numbered 1, 2, 3 on separate lines.
Be creative but consistent with the story so far."""

        new_scene = call_openrouter(prompt)

        # Parse new choices
        lines = new_scene.strip().split('\n')
        new_choices = []
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.')):
                new_choices.append(line.strip()[2:].strip())

        # Create summary for history (first sentence or first 100 chars)
        summary = new_scene.split('.')[0][:100] + "..."

        history.append({
            "summary": summary,
            "full": new_scene,
            "choice": choice_index
        })

        return {
            "scene": new_scene,
            "choices": new_choices[:3],
            "history": history,
            "date": "2026-02-24"
        }

    elif action == 'visualize':
        # Generate an image of the current scene
        scene = data.get('scene', 'an adventure scene')
        genre = data.get('genre', 'fantasy')

        # Extract key visual elements from scene
        prompt = f"Create a vibrant {genre} illustration: {scene[:200]}. Rich colors, dynamic composition, high quality digital art."

        image_b64 = fetch_image(prompt, width=512, height=512)

        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-24"
            }
        else:
            return {"error": "Failed to generate visualization"}

    elif action == 'genres':
        # List available adventure genres
        return {
            "genres": ["fantasy", "sci-fi", "mystery", "horror", "adventure", "steampunk", "cyberpunk"],
            "date": "2026-02-24"
        }

    return {"error": f"Unknown action: {action}"}

META = {
    "name": "AI Adventure Game Master",
    "description": "Embark on an AI-generated interactive adventure! Make choices that shape your journey through fantastical worlds, all narrated with AI-generated text and visuals",
    "category": "Fun",
    "date": "2026-02-24"
}
