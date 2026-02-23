#!/usr/bin/env python3
"""
AI Dungeon Master - Combined API
Handles all game actions via POST with action parameter

Actions:
- start: Create new game
- choice: Make a choice in existing game

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import uuid
import logging
from http.server import BaseHTTPRequestHandler
import subprocess
from urllib.parse import quote, parse_qs

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
        return "The adventure continues... Choose your path wisely."

def parse_scene_and_choices(text: str):
    """Parse generated text into scene and choices"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    scene_lines, choices, in_choices = [], [], False
    for line in lines:
        if line.lower().startswith(("choices:", "options:")):
            in_choices = True
            continue
        if in_choices:
            if line and line[0].isdigit() and ". " in line:
                choices.append(line.split(". ", 1)[-1])
        else:
            scene_lines.append(line)
    return "\n".join(scene_lines), choices if choices else ["Explore ahead", "Investigate nearby", "Rest"]

def start_game(theme: str, setting: str):
    """Create new game"""
    prompt = f"""Create an immersive {theme} adventure opening in {setting}.

First paragraph: Set the atmospheric scene with sensory details.
Second paragraph: Introduce tension or mystery.
Then list exactly 3 choices.

Format:
[Scene description]

Choices:
1. [First choice]
2. [Second choice]
3. [Third choice]"""
    
    text = call_pollinations(prompt)
    scene, choices = parse_scene_and_choices(text)
    return {
        "game_id": str(uuid.uuid4()),
        "theme": theme,
        "setting": setting,
        "scene": scene,
        "choices": choices,
        "history": [{"role": "narrator", "text": scene}]
    }

def make_choice(game_id: str, choice: str, history: list):
    """Process player choice"""
    prompt = f"""Continue the adventure. Player chose: "{choice}"

Previous context: {history[-1]['text'] if history else 'Beginning'}

Write 2-3 paragraphs advancing the story based on this choice.
Include consequences, new developments, or discoveries.
End with exactly 3 new choices.

Format:
[Story continuation]

Choices:
1. [First choice]
2. [Second choice]
3. [Third choice]"""
    
    text = call_pollinations(prompt)
    scene, choices = parse_scene_and_choices(text)
    new_history = history + [{"role": "player", "text": choice}, {"role": "narrator", "text": scene}]
    return {"game_id": game_id, "scene": scene, "choices": choices, "history": new_history}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            action = data.get('action', 'start')
            
            if action == 'start':
                result = start_game(
                    data.get('theme', 'fantasy'),
                    data.get('setting', 'mysterious dungeon')
                )
            elif action == 'choice':
                result = make_choice(
                    data.get('game_id', ''),
                    data.get('choice', ''),
                    data.get('history', [])
                )
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
