#!/usr/bin/env python3
"""
AI Dungeon Master - Make Choice Endpoint  
POST /api/2026-02-21-ai-dungeon-master/choice

Makes a choice and advances the story.
Client must pass current game state since serverless functions are stateless.

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import logging
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

def generate_text_pollinations(prompt: str) -> str:
    """Generate text using Pollinations.AI"""
    try:
        url = f"https://text.pollinations.ai/{quote(prompt)}"
        headers = {}
        if POLLINATIONS_API_KEY:
            headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
        
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            if response.status == 200:
                return response.read().decode('utf-8').strip()
        raise Exception("Text generation failed")
    except Exception as e:
        logger.exception(f"Text generation error: {e}")
        return """The story continues... A new challenge awaits.

Choices:
1. Press forward
2. Take a different path
3. Rest and reconsider"""

def parse_scene_and_choices(text: str):
    """Parse generated text into scene and choices"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    scene_lines = []
    choices = []
    in_choices = False
    
    for line in lines:
        if line.lower().startswith(("choices:", "options:")):
            in_choices = True
            continue
        if in_choices:
            if line and line[0].isdigit() and ". " in line:
                choices.append(line.split(". ", 1)[-1])
        else:
            scene_lines.append(line)
    
    scene = "\n".join(scene_lines)
    if not choices:
        choices = ["Continue", "Try something else", "Wait"]
    
    return scene[:500], choices[:3]

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            current_scene = data.get("scene", "")
            choices = data.get("choices", [])
            choice_index = data.get("choice_index", 0)
            history = data.get("history", [])
            
            if choice_index >= len(choices):
                choice_index = 0
            
            selected_choice = choices[choice_index] if choices else "Continue"
            
            # Generate next scene based on choice
            prompt = f"""Previous scene: {current_scene}
Player chose: {selected_choice}

Generate the next scene (2-3 paragraphs) showing consequences. Then provide exactly 3 new choices.

Format:
[Scene description]

Choices:
1. [First choice]
2. [Second choice]
3. [Third choice]

Scene:"""
            
            generated_text = generate_text_pollinations(prompt)
            new_scene, new_choices = parse_scene_and_choices(generated_text)
            
            # Update history
            history.append({"scene": new_scene, "choices": new_choices, "selected": selected_choice})
            
            response = {
                "scene": new_scene,
                "choices": new_choices,
                "selected_choice": selected_choice,
                "history": history
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            logger.info(f"Choice made: {selected_choice}")
            
        except Exception as e:
            logger.exception(f"Choice error: {e}")
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

def handler(event):
    """Vercel serverless entry point"""
    return Handler(event).handler(event)
