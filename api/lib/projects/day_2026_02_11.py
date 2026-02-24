"""AI Tokenization Visualizer - Understand how text is broken into tokens for AI models"""

from ..base import call_openrouter, fetch_image

def handle(action: str, data: dict) -> dict:
    """Handle project actions."""

    if action == 'start':
        intro = """Tokenization is the crucial first step in how AI language models process text. Before understanding meaning, models must break input into tokens - the basic units they work with.

**What is a token?**
- Tokens can be whole words, parts of words, punctuation, or even single characters
- Different models use different tokenizers (BPE, WordPiece, SentencePiece)
- The same word can be split differently depending on the tokenizer

**Why it matters:**
- Context windows are measured in tokens (not characters or words)
- Token count affects API costs and processing speed
- Understanding tokenization helps you write efficient prompts

**In this visualizer:**
- Enter any text to see how it's tokenized
- Compare tokenization across different model types
- Learn token counts and efficiency tips"""

        return {
            "intro": intro,
            "date": "2026-02-11",
            "project": "AI Tokenization Visualizer",
            "actions": ["tokenize", "compare", "explain", "efficiency"],
            "supported_models": ["GPT-style (BPE)", "BERT-style (WordPiece)", "SentencePiece"]
        }

    elif action == 'tokenize':
        """Tokenize input text and show details."""
        text = data.get('text', '').strip()
        model_type = data.get('model', 'GPT-style (BPE)')

        if not text:
            return {"error": "Please provide text to tokenize"}

        prompt = f"""Analyze this text for tokenization:

"{text}"

For a {model_type} tokenizer, provide:
1. List each token (show them clearly, separated by commas)
2. Count total tokens
3. Count total characters
4. Calculate tokens per word ratio (tokens/words)
5. Brief notes on how this model type typically tokenizes

Format as JSON:
{{
  "tokens": ["token1", "token2", ...],
  "token_count": N,
  "character_count": N,
  "word_count": N,
  "tokens_per_word": X.XX,
  "notes": "brief explanation"
}}

Only respond with valid JSON, nothing else."""

        result = call_openrouter(prompt)

        # Try to extract JSON from response
        analysis = extract_json(result)
        if analysis:
            return {
                "analysis": analysis,
                "input_text": text,
                "model_type": model_type,
                "date": "2026-02-11"
            }
        else:
            # Fallback: return raw response
            return {
                "analysis": {"raw_response": result, "error": "Could not parse as JSON"},
                "input_text": text,
                "model_type": model_type,
                "date": "2026-02-11"
            }

    elif action == 'compare':
        """Compare tokenization across different model types."""
        text = data.get('text', '').strip()

        if not text:
            return {"error": "Please provide text to compare"}

        prompt = f"""Compare how different tokenizers would handle this text:

"{text}"

For each tokenizer type, describe:
- GPT-style (BPE): How would Byte-Pair Encoding split this?
- BERT-style (WordPiece): What subwords would it create?
- SentencePiece: How would it unigram or BPE approach this?

For each, provide:
- Estimated token count (give specific numbers)
- Examples of likely splits (show 2-3 actual token examples)
- Notes on special handling (spaces, punctuation, capitalization)

Present as a clear comparison table or structured comparison.
Keep it concise but informative."""

        comparison = call_openrouter(prompt)

        return {
            "comparison": comparison,
            "input_text": text,
            "date": "2026-02-11"
        }

    elif action == 'explain':
        """Provide educational explanation about tokenization."""
        topic = data.get('topic', 'overview')

        if topic == 'overview':
            prompt = """Explain tokenization in simple terms:
- What are tokens?
- Why do AI models need tokenization?
- How is it different from splitting by words?
- Visual analogy (like breaking a sentence into Lego blocks)
Keep it under 200 words, very beginner-friendly."""
        elif topic == 'bpe':
            prompt = """Explain Byte-Pair Encoding (BPE) tokenization:
- The algorithm: start with characters, merge frequent pairs
- Why it's good for handling rare words
- How it creates subword units
- Example showing merging steps
Keep it under 250 words, intermediate level."""
        elif topic == 'costs':
            prompt = """Explain how tokenization affects AI usage costs:
- API pricing is per token
- Why some texts cost more (Unicode, rare words)
- Tips to reduce token count (shorter prompts, efficient phrasing)
- Context window limits and token counting
Practical advice, ~200 words."""
        else:
            prompt = f"""Explain tokenization focusing on: {topic}
Provide clear, educational explanation about this aspect of tokenization.
Keep it concise (150-250 words)."""

        explanation = call_openrouter(prompt)

        return {
            "explanation": explanation,
            "topic": topic,
            "date": "2026-02-11"
        }

    elif action == 'efficiency':
        """Calculate token efficiency metrics."""
        text = data.get('text', '').strip()

        if not text:
            return {"error": "Please provide text to analyze"}

        prompt = f"""Analyze the tokenization efficiency of this text:

"{text}"

Provide efficiency analysis including:
1. Word count and token count
2. Tokens per word ratio (typical is ~1.3 for English)
3. Identify potential inefficiencies (emoji, special chars, spaces)
4. Suggest optimizations to reduce token count
5. Estimate cost if processed through OpenRouter ($0.001 per 1K tokens for input)

Return as JSON:
{{
  "word_count": N,
  "token_count": N,
  "tokens_per_word": X.XX,
  "inefficiencies": ["issue1", "issue2"],
  "optimization_suggestions": ["suggestion1", ...],
  "estimated_cost": "$0.00"
}}

Only return valid JSON."""

        result = call_openrouter(prompt)
        analysis = extract_json(result)

        if analysis:
            return {
                "efficiency_analysis": analysis,
                "input_text": text,
                "date": "2026-02-11"
            }
        else:
            return {
                "efficiency_analysis": {"raw_response": result},
                "input_text": text,
                "date": "2026-02-11"
            }

    elif action == 'visualize':
        """Generate educational diagram about tokenization."""
        concept = data.get('concept', 'tokenization process')

        prompt = f"""Create a clean, educational diagram explaining how tokenization works in AI language models.

Show:
1. Input text: "Hello world!" at the top
2. Tokenizer box in the middle, splitting into: ["Hello", " world", "!"]
3. Tokens flowing to model embedding layer
4. Label each token with its token ID (example numbers)
5. Show that 3 tokens != 2 words (" world" includes space)

Style: Technical illustration, clean lines, modern colors (blue/green), minimal, readable labels.
Aspect ratio: 16:9 or 4:3 landscape."""

        image_b64 = fetch_image(prompt, width=800, height=600)

        if image_b64:
            return {
                "image": f"data:image/png;base64,{image_b64}",
                "date": "2026-02-11",
                "concept": concept
            }
        else:
            return {"error": "Failed to generate visualization"}

    return {"error": f"Unknown action: {action}"}

# Metadata for projects.json
META = {
    "name": "AI Tokenization Visualizer",
    "description": "Explore how text is broken into tokens for AI models: visualize token splits, compare tokenizers, and learn efficiency tips",
    "category": "AI Education",
    "date": "2026-02-11"
}
