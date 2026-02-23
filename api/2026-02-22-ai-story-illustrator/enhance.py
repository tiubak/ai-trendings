#!/usr/bin/env python3
"""
AI Story Illustrator - Enhance Story Endpoint
POST /api/2026-02-22-ai-story-illustrator/enhance

Enhances user's story prompt into a more engaging narrative.

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import logging
from http.server import BaseHTTPRequestHandler
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

def generate_text_pollinations(prompt: str) -> str:
    """Generate text using Pollinations.AI via curl subprocess

    CRITICAL: Python urllib is BLOCKED by Cloudflare (403 Forbidden)!
    Must use curl subprocess to bypass Cloudflare.
    """
    try:
        # URL encode the prompt
        from urllib.parse import quote
        url = f"https://text.pollinations.ai/{quote(prompt)}"

        headers = []
        if POLLINATIONS_API_KEY:
            headers.extend(["-H", f"Authorization: Bearer {POLLINATIONS_API_KEY}"])

        # Use curl subprocess instead of urllib
        result = subprocess.run(
            ["curl", "-s"] + headers + [url],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return result.stdout.strip()
        raise Exception(f"curl failed with status {result.returncode}: {result.stderr}")

    except Exception as e:
        logging.error(f"Text generation error: {e}")
        # Return fallback
        return "The story continues... A new challenge awaits.

Choices:
1. Press forward
2. Take a different path
3. Rest and reconsider"
def create_enhance_prompt(story_idea: str, style: str = "engaging") -> str:
    """Create prompt for story enhancement"""
    style_prompts = {
        "engaging": "Make it captivating and immersive",
        "fantasy": "Add magical elements and wonder",
        "sci-fi": "Add futuristic technology and discovery",
        "mystery": "Add suspense and intrigue",
        "humorous": "Make it funny and lighthearted",
        "dramatic": "Make it intense and emotional"
    }
    
    style_instruction = style_prompts.get(style, "Make it engaging")
    
    return f"""You are a creative writer. Expand this story idea into a short, engaging story (200-300 words).

Story idea: {story_idea}

Style: {style_instruction}

Write the story now:"""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            story_idea = data.get("story_idea", "")
            style = data.get("style", "engaging")
            
            if not story_idea:
                raise ValueError("story_idea is required")
            
            prompt = create_enhance_prompt(story_idea, style)
            enhanced_story = generate_text_pollinations(prompt)
            
            # Return enhanced story to client (client will store and pass back)
            response = {
                "original_idea": story_idea,
                "enhanced_story": enhanced_story,
                "style": style,
                "word_count": len(enhanced_story.split()),
                "message": "Story enhanced!"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            logger.info(f"Story enhanced: {len(enhanced_story)} characters")
            
        except Exception as e:
            logger.exception(f"Enhance story error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
