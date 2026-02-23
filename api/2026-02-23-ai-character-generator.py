#!/usr/bin/env python3
"""
AI Character Generator - Combined API
Actions: start (generate), develop
"""

import os
import json
import logging
import re
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
        return '{"error": "API unavailable"}'

def extract_json(text: str) -> dict:
    """Extract JSON from text that might have extra content"""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Find JSON object in text
    start = text.find('{')
    if start == -1:
        return None
    
    # Find matching closing brace
    depth = 0
    for i, char in enumerate(text[start:], start):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i+1])
                except json.JSONDecodeError:
                    continue
    
    return None

def generate_character(name: str, role: str, setting: str, theme: str):
    """Generate complete character profile"""
    prompt = f'''Create a JSON character profile for a {role} named {name}.

Setting: {setting}
Theme: {theme}

Return ONLY valid JSON with these fields:
- name: "{name}"
- role: "{role}"
- backstory: string
- personality: string  
- strengths: array of 3 strings
- weaknesses: array of 3 strings
- motivation: string
- relationships: object with ally and rival
- signature_quote: string

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    character = extract_json(text)
    
    if not character:
        character = {
            "name": name,
            "role": role,
            "backstory": f"A mysterious {role} from {setting}.",
            "personality": "Enigmatic and determined.",
            "strengths": ["Resourceful", "Determined", "Cunning"],
            "weaknesses": ["Secretive", "Stubborn", "Overconfident"],
            "motivation": "Driven by a hidden purpose.",
            "relationships": {"ally": "A trusted companion", "rival": "A shadow from the past"},
            "signature_quote": "The path forward is never clear."
        }
    
    return {"character": character, "setting": setting, "theme": theme}

def develop_character(character: dict, aspect: str):
    """Develop character further"""
    prompt = f'''Expand on this character's {aspect}:

{json.dumps(character, indent=2)}

Write 2 paragraphs developing their {aspect} further. Be specific and vivid.'''
    
    development = call_pollinations(prompt)
    return {"character": character, "aspect": aspect, "development": development}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            action = data.get('action', 'start')
            
            if action == 'start':
                result = generate_character(
                    data.get('name', 'Unknown'),
                    data.get('role', 'Hero'),
                    data.get('setting', 'Fantasy realm'),
                    data.get('theme', 'Adventure')
                )
            elif action == 'develop':
                result = develop_character(
                    data.get('character', {}),
                    data.get('aspect', 'backstory')
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
