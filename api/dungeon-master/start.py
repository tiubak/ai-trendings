#!/usr/bin/env python3
"""
AI Dungeon Master - Start Game Endpoint
POST /api/dungeon-master/start

Creates a new game and returns initial game state.

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import uuid
import logging
from http.server import BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# Game state storage (in-memory for demo)
games = {}

def generate_text_pollinations(prompt: str) -> str:
    """Generate text using Pollinations.AI"""
    try:
        from urllib.request import Request, urlopen
        from urllib.parse import quote
        
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
        raise

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
        choices = ["Explore the path", "Investigate the object", "Rest and recover"]
    
    return scene[:500], choices[:3]

def create_initial_prompt(theme: str, player_name: str) -> str:
    themes = {
        "fantasy": "a high fantasy dungeon with magical creatures",
        "sci-fi": "a futuristic spaceship or alien planet",
        "horror": "a haunted mansion or cursed forest",
        "mystery": "a mysterious crime scene"
    }
    setting = themes.get(theme, themes["fantasy"])
    return f"""You are a dungeon master. Player '{player_name}' starts a new adventure in {setting}.
Generate an opening scene (2-3 paragraphs). Then provide exactly 3 choices.

Format:
[Scene description]

Choices:
1. [First choice]
2. [Second choice]
3. [Third choice]

Scene:"""

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = self.headers.get('Content-Length')
            body = self.rfile.read(int(content_length)).decode('utf-8')
            data = json.loads(body)
            
            theme = data.get("theme", "fantasy")
            player_name = data.get("player_name", "Adventurer")
            game_id = str(uuid.uuid4())
            
            prompt = create_initial_prompt(theme, player_name)
            generated_text = generate_text_pollinations(prompt)
            scene, choices = parse_scene_and_choices(generated_text)
            
            games[game_id] = {
                "game_id": game_id,
                "theme": theme,
                "player_name": player_name,
                "scene": scene,
                "choices": choices
            }
            
            response = {
                "game_id": game_id,
                "scene": scene,
                "choices": choices,
                "theme": theme,
                "player_name": player_name,
                "message": "Game started!"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            logger.exception(f"Start game error: {e}")
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
    return Handler(event).handler(event)
