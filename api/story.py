#!/usr/bin/env python3
"""
AI Story Illustrator - Combined API
Handles all story illustration actions via POST with action parameter

Actions:
- start: Create new story project
- enhance: Enhance story text
- illustrate: Generate image prompt

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import logging
from http.server import BaseHTTPRequestHandler
import subprocess
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

def call_pollinations(prompt: str) -> str:
    """Call Pollinations.AI via curl subprocess (urllib blocked by Cloudflare)"""
    try:
        url = f"https://text.pollinations.ai/{quote(prompt)}"
        headers = []
        if POLLINATIONS_API_KEY:
            headers.extend(["-H", f"Authorization: Bearer {POLLINATIONS_API_KEY}"])
        result = subprocess.run(
            ["curl", "-s"] + headers + [url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        raise Exception(f"curl failed: {result.stderr}")
    except Exception as e:
        logger.error(f"Pollinations error: {e}")
        return "The story continues..."

def start_story(genre: str, theme: str):
    """Create new story project"""
    prompt = f"""Create a {genre} story opening with theme: {theme}

Write 2-3 paragraphs that:
- Establish the setting with vivid imagery
- Introduce the main character
- Present an inciting incident or mystery

Make it engaging and leave room for development."""
    
    story = call_pollinations(prompt)
    return {
        "story_id": "story-001",
        "genre": genre,
        "theme": theme,
        "text": story,
        "images": []
    }

def enhance_story(text: str, style: str):
    """Enhance story text with more detail"""
    prompt = f"""Enhance this story text in a {style} style:

"{text}"

Add:
- More sensory details
- Deeper character emotions
- Vivid descriptions

Keep the same plot but make it more immersive."""
    
    enhanced = call_pollinations(prompt)
    return {"original": text, "enhanced": enhanced, "style": style}

def illustrate_scene(text: str):
    """Generate image prompt for story scene"""
    prompt = f"""Create a detailed image prompt for this story scene:

"{text}"

Describe:
- Visual composition
- Color palette
- Mood and lighting
- Key elements to include

Output only the image prompt, concise and vivid."""
    
    image_prompt = call_pollinations(prompt)
    return {"scene": text, "image_prompt": image_prompt}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            action = data.get('action', 'start')
            
            if action == 'start':
                result = start_story(
                    data.get('genre', 'fantasy'),
                    data.get('theme', 'adventure')
                )
            elif action == 'enhance':
                result = enhance_story(
                    data.get('text', ''),
                    data.get('style', 'descriptive')
                )
            elif action == 'illustrate':
                result = illustrate_scene(data.get('text', ''))
            else:
                result = {"error": f"Unknown action: {action}"}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)
