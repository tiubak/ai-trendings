"""AI Love Letter Analyst - Explore how AI understands romantic language, generate personalized love letters, and learn about sentiment analysis and emotional AI"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        intro = """Welcome to the AI Love Letter Analyst! ❤️

**What is this?**
This project explores how AI language models understand and generate emotional, romantic language. It's not just about writing love letters—it's about understanding the AI's approach to sentiment, tone, personalization, and the ethics of artificial intimacy.

**What you'll learn:**
- How sentiment analysis identifies emotional tone
- How AI models maintain consistent voice and style
- The importance ofpersonalization in language generation
- Ethical considerations: Can AI truly understand love?
- Prompt engineering techniques for emotional writing

**Features:**
- Generate personalized love letters based on relationship details
- Analyze the emotional tone and sentiment of any text
- Compare different romantic writing styles
- Learn about the AI's reasoning process
- Explore the science behind emotional language processing

**Why this matters:**
As AI becomes more integrated into personal communication, understanding its capabilities and limitations in emotional contexts is crucial. This tool demystifies how machines process something as human as love."""

        return {
            "intro": intro,
            "date": "2026-02-12",
            "project": "AI Love Letter Analyst",
            "actions": ["generate", "analyze", "compare_styles", "explain_ai", "ethics"],
            "styles": ["romantic", "playful", "poetic", "modern", "vintage", "passionate", "sincere", "whimsical"]
        }

    elif action == 'generate':
        """Generate a personalized love letter."""
        recipient_name = data.get('recipient_name', '').strip()
        sender_name = data.get('sender_name', '').strip()
        relationship = data.get('relationship', 'partner').strip()
        special_memory = data.get('special_memory', '').strip()
        style = data.get('style', 'romantic')
        length = data.get('length', 'medium')  # short, medium, long

        if not recipient_name or not sender_name:
            return {"error": "Please provide both recipient and sender names"}

        # Build prompt based on parameters
        prompt = f"""Write a {style} love letter from {sender_name} to {recipient_name}.

Context:
- Relationship: {relationship}
- Special memory to include: {special_memory if special_memory else 'a sweet moment they shared'}
- Desired length: {length} (short: 3-4 sentences, medium: 1 paragraph, long: 2-3 paragraphs)
- Style guidance:
  * romantic: poetic, heartfelt, dreamy
  * playful: lighthearted, teasing, joyful
  * poetic: metaphorical, rhythmic, artistic
  * modern: casual, authentic, contemporary
  * vintage: elegant, formal, timeless
  * passionate: intense, fiery, deeply emotional
  * sincere: honest, grounded, genuine
  * whimsical: fanciful, imaginative, fun

Requirements:
- Start with a warm greeting using the recipient's name
- Include specific details (use the special memory if provided, or suggest a sweet moment)
- Express genuine affection and appreciation
- End with a loving closing
- Match the chosen style consistently throughout
- Keep tone intimate but not overly dramatic (unless passionate style)
- Make it sound natural and personal, not generic

Write the complete letter now. Only output the letter text itself, no commentary."""

        letter = call_openrouter(prompt)

        # Also generate an analysis of what makes this letter effective
        analysis_prompt = f"""Analyze this love letter for its emotional and rhetorical qualities:

"{letter}"

Provide analysis in JSON format:
{{
  "emotional_tone": "primary emotion conveyed",
  "sentiment_score": 0.0-1.0,
  "key_phrases": ["phrase1", "phrase2"],
  "personalization_level": "high/medium/low",
  "style_consistency": "good/fair/poor",
  "literary_devices": ["device1", "device2"],
  "effectiveness_notes": "brief assessment"
}}

Only return valid JSON."""

        analysis_result = call_openrouter(analysis_prompt)
        analysis = extract_json(analysis_result) or {"raw_analysis": analysis_result}

        # Generate an image for the letter (optional decorative element)
        # Create a prompt for a romantic-themed abstract image
        image_prompt = f"Abstract romantic watercolor art, soft colors, heart shapes blending, dreamy atmosphere, suitable for a love letter illustration"
        image_b64 = fetch_image(image_prompt, width=512, height=512)

        return {
            "letter": letter,
            "recipient": recipient_name,
            "sender": sender_name,
            "style": style,
            "analysis": analysis,
            "image": f"data:image/png;base64,{image_b64}" if image_b64 else None,
            "date": "2026-02-12"
        }

    elif action == 'analyze':
        """Analyze sentiment and emotional content of user-provided text."""
        text = data.get('text', '').strip()

        if not text:
            return {"error": "Please provide text to analyze"}

        prompt = f"""Perform a deep emotional and rhetorical analysis of this text:

"{text}"

Return analysis as JSON:
{{
  "overall_sentiment": "positive/negative/neutral/mixed",
  "sentiment_confidence": 0.0-1.0,
  "primary_emotions": ["love", "longing", "joy", ...],
  "emotional_intensity": 0.0-1.0,
  "tone": ["romantic", "playful", "serious", "flirty", "formal", "casual"],
  "formality_level": "formal/casual/semi-formal",
  "personalization": "high/medium/low",
  "key_words": [" adored", "cherish", ...],
  "literary_devices": ["metaphor", "simile", "alliteration", "hyperbole", "personification"],
  "readability": "simple/moderate/complex",
  "authenticity_feeling": "genuine/forced/neutral",
  "suggestions": ["improvement1", "improvement2"]
}}

Be thorough but concise. Only return valid JSON."""

        result = call_openrouter(prompt)
        analysis = extract_json(result)

        if analysis:
            return {
                "analysis": analysis,
                "text": text,
                "date": "2026-02-12"
            }
        else:
            return {
                "analysis": {"raw_response": result, "error": "Could not parse JSON"},
                "text": text,
                "date": "2026-02-12"
            }

    elif action == 'compare_styles':
        """Compare how different AI styles would write about the same topic."""
        topic = data.get('topic', 'love').strip()
        styles_to_compare = data.get('styles', ['romantic', 'playful', 'poetic'])

        if not topic:
            return {"error": "Please provide a topic"}

        prompt = f"""Compare how these {len(styles_to_compare)} writing styles would approach the topic of "{topic}":

{chr(10).join(f'- {s}' for s in styles_to_compare)}

For each style, provide:
1. A short example sentence or two (max 30 words each) showing that style
2. Key characteristics of that style (word choice, sentence structure, emotional register)
3. When that style is most appropriate

Present as a clear comparison. Total response ~300 words."""

        comparison = call_openrouter(prompt)

        return {
            "comparison": comparison,
            "topic": topic,
            "styles": styles_to_compare,
            "date": "2026-02-12"
        }

    elif action == 'explain_ai':
        """Educational explanation about how AI handles emotional language."""
        topic = data.get('topic', 'sentiment_analysis')

        explanations = {
            'sentiment_analysis': """**How AI Analyzes Sentiment**

Sentiment analysis (or opinion mining) is how AI determines the emotional tone behind text—positive, negative, or neutral.

**How it works:**
1. **Tokenization**: Text is broken into tokens (words, subwords)
2. **Embeddings**: Each token is converted to a vector representing its meaning
3. **Context understanding**: The model processes relationships between tokens
4. **Classification**: Patterns are compared to learned emotional associations

**What AI detects:**
- Word choice (e.g., "love" vs "hate")
- Modifiers ("very", "slightly")
- Negations ("not happy")
- Emojis and punctuation (exclamation marks, heart emojis)
- Context strings ("I love you" vs "I love my coffee")

**Limitations:**
- Sarcasm and irony can confuse AI
- Cultural differences in expression
- Subtle emotions (nostalgia, bittersweet) are harder
- AI doesn't *feel* emotions—it recognizes patterns

**Fun fact**: Modern LLMs like GPT-4 achieve ~90% accuracy on standard sentiment benchmarks, but human-level nuance remains challenging.""",

            'emotional_language': """**How AI Understands Emotional Language**

AI doesn't have emotions, but it can model how humans express them through language.

**Key concepts:**
- **Training data**: AI learns from millions of examples of emotional writing (books, letters, social media)
- **Pattern recognition**: It identifies which words/phrases correlate with which emotions
- **Style transfer**: AI can adopt different emotional tones by mimicking patterns
- **Personalization**: By using specific details, AI makes text feel more genuine

**What AI can do:**
- Generate text in various emotional registers
- Match tone to context (e.g., condolence vs celebration)
- Maintain emotional consistency across long text
- Adapt formality level

**What AI cannot do:**
- Actually experience emotions
- Have authentic emotional intent
- Replace genuine human connection
- Understand emotions without linguistic expression

**The takeaway**: AI is a tool for expression, not a substitute for human feeling.""",

            'prompt_engineering': """**Prompt Engineering for Emotional Writing**

Crafting effective prompts is key to getting good emotional output from AI.

**Principles:**
1. **Be specific**: "Write a heartfelt goodbye letter" beats "write something sad"
2. **Provide context**: Include relationship details, shared memories, personality traits
3. **Specify tone**: Use adjectives like "warm", "playful", "formal", "vulnerable"
4. **Give constraints**: Length, format, do's and don'ts
5. **Iterate**: Refine based on outputs

**Example progression:**
Weak: "Write a love letter"
Better: "Write a romantic love letter from Alex to Jamie, 2 years together, mentioning their trip to Paris"
Strong: "Write a 2-paragraph romantic love letter from Alex to Jamie (they've been together 2 years). Start with a memory of their trip to Paris where they got caught in the rain but danced anyway. Express gratitude for Jamie's patience and make it warm but not flowery. End with 'Yours always'."

**Why it matters**: Better prompts = more personal, meaningful output.""",

            'ethics': """**Ethics of AI in Personal Communication**

Using AI for intimate writing raises important questions.

**Benefits:**
- Helps people express difficult emotions
- Overcomes writer's block
- Makes communication more accessible
- Can inspire human creativity

**Concerns:**
- Authenticity: Is AI-written communication "real"?
- Consent: Should the recipient know AI was involved?
- Dependency: Reliance on AI for expression
- Privacy: Personal details shared with AI services
- Emotional manipulation potential

**Guidelines:**
- Be transparent if AI assistance was used (especially in important contexts)
- Use AI as a tool for expression, not a replacement for genuine feeling
- Never use AI to deceive or manipulate
- Keep personal data secure
- Remember: the relationship matters, not the perfection of words

**Bottom line**: AI can help us communicate, but human connection is about presence, not prose."""
        }

        topic_key = topic.lower().replace(' ', '_')
        explanation = explanations.get(topic_key, f"Topic '{topic}' not found. Try: sentiment_analysis, emotional_language, prompt_engineering, ethics")

        return {
            "explanation": explanation,
            "topic": topic,
            "date": "2026-02-12"
        }

    elif action == 'ethics':
        """Get ethical considerations about AI in romantic contexts."""
        # Reuse the ethics explanation
        return handle('explain_ai', {'topic': 'ethics'})

    return {"error": f"Unknown action: {action}"}

# Metadata for projects.json
META = {
    "name": "AI Love Letter Analyst",
    "description": "Explore how AI understands romantic language, generate personalized love letters, and learn about sentiment analysis and emotional AI",
    "category": "Fun",
    "date": "2026-02-12"
}
