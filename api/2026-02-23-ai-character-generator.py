#!/usr/bin/env python3
"""
AI Character Generator - Combined API
Handles all character generation actions via POST with action parameter

Actions:
- start: Generate new character
- develop: Develop character further

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
        return "A mysterious character emerges..."

def generate_character(name: str, role: str, setting: str, theme: str):
    """Generate complete character profile"""
    prompt = f"""Create a detailed character profile for a {role} named {name}.

Setting: {setting}
Theme: {theme}

Generate JSON format:
{{
  "name": "{name}",
  "role": "{role}",
  "backstory": "3-4 sentences about their origin and past",
  "personality": "2-3 sentences describing temperament and behavior",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "motivation": "What drives this character",
  "relationships": {{
    "ally": "Description of an important ally",
    "rival": "Description of an important rival"
  }},
  "signature_quote": "A memorable line this character would say"
}}

Make it compelling and consistent with the {role} archetype."""

    text = call_pollinations(prompt)
    try:
        # Try to parse JSON directly
        character = json.loads(text)
    except json.JSONDecodeError:
        # Extract JSON from response
        import re
        json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
        if json_match:
            character = json.loads(json_match.group(0))
        else:
            character = {
                "name": name, "role": role, "backstory": text,
                "personality": "Complex and nuanced", "strengths": ["Determined"],
                "weaknesses": ["Stubborn"], "motivation": "Unknown",
                "relationships": {"ally": "None", "rival": "None"},
                "signature_quote": "..."
            }
    
    return {"character": character, "setting": setting, "theme": theme}

def develop_character(character: dict, aspect: str):
    """Develop character further in specific aspect"""
    prompt = f"""Develop this character's {aspect} further:

Character: {json.dumps(character)}

Write 2-3 paragraphs expanding on their {aspect}.
Include specific examples, memories, or scenarios.
Make it deeper and more nuanced."""

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
