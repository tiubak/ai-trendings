#!/usr/bin/env python3
"""
AI Dungeon Master - Make Choice Endpoint
POST /api/dungeon-master/choice

Makes a choice and advances the story.

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import logging
from http.server import BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

# Import shared game state
from api.dungeon_master.start import games, generate_text_pollinations, parse_scene_and_choices

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = self.headers.get('Content-Length')
            body = self.rfile.read(int(content_length)).decode('utf-8')
            data = json.loads(body)
            
            game_id = data.get("game_id")
            choice_index = data.get("choice_index", 0)
            
            if game_id not in games:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Game not found"}).encode('utf-8'))
                return
            
            game = games[game_id]
            selected_choice = game["choices"][choice_index]
            
            prompt = f"""Previous scene: {game['scene']}
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
            
            game["scene"] = new_scene
            game["choices"] = new_choices
            
            response = {
                "game_id": game_id,
                "scene": new_scene,
                "choices": new_choices,
                "selected_choice": selected_choice
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            logger.exception(f"Choice error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
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
