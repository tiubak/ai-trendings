#!/usr/bin/env python3
"""
AI Cosmic Whisperer - Combined API
Actions: start, daily
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
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    start = text.find('{')
    if start == -1:
        return None
    
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

def generate_cosmic_message(name: str, theme: str, tone: str) -> dict:
    """Generate a cosmic message/reading"""
    theme_descriptions = {
        "general": "general life guidance",
        "love": "matters of the heart and relationships",
        "career": "your professional path and purpose",
        "health": "wellness and vitality",
        "spiritual": "your inner journey and awakening"
    }
    
    theme_desc = theme_descriptions.get(theme, "your life's journey")
    
    prompt = f'''You are a cosmic Oracle channeling messages from the stars and galaxies.

Speak to {name or 'a seeker'} about {theme_desc}.

Tone: {tone} (mystical/ethereal, direct/clear, or comforting/soothing)

Write a 2-3 paragraph cosmic message that feels like it's coming from the universe itself. Use space and celestial imagery (stars, galaxies, nebulae, constellations, cosmic energy, starlight, etc.). Make it feel magical and profound.

Structure:
- Opening: A cosmic invocation or visual
- Middle: The actual guidance/wisdom
- Closing: A blessing or encouragement

Return a JSON object with these fields:
{{
  "message": "the full cosmic message as a string",
  "theme": "{theme}",
  "tone": "{tone}",
  "key_words": ["array", "of", "3", "celestial", "keywords"],
  " affirmation ":"a short powerful affirmation related to the message"
}}

No markdown, no extra text, just the JSON.'''

    text = call_pollinations(prompt)
    result = extract_json(text)
    
    if not result or 'message' not in result:
        # Fallback message
        result = {
            "message": f"The stars align for {name or 'you'} today. In the vast cosmic dance, remember that you are both stardust and the universe experiencing itself. Trust the journey unfolding through {theme}. The celestial energies whisper: patience and courage will guide your way.",
            "theme": theme,
            "tone": tone,
            "key_words": ["stardust", "cosmic", "alignment"],
            "affirmation": "I am in harmony with the universe."
        }
    
    return result

def get_daily_cosmic_reading() -> dict:
    """Get a general cosmic message for the day"""
    import datetime
    today = datetime.datetime.now().strftime("%A, %B %d")
    
    prompt = f'''Today is {today}. Channel a general cosmic message for all beings on this day.

Write a 2-3 paragraph message that feels like it's coming from the universe. Use beautiful space imagery. Make it universally relevant and inspiring.

Return JSON:
{{
  "message": "the full cosmic message",
  "theme": "general",
  "date": "{today}",
  "key_words": ["array", "of", "3", "cosmic", "keywords"],
  "daily_focus": "a theme for today"
}}

No extra text, just JSON.'''

    text = call_pollinations(prompt)
    result = extract_json(text)
    
    if not result or 'message' not in result:
        result = {
            "message": f"The cosmos breathes with possibility on this {today}. Remember that you are a unique expression of the universe, capable of magnificent things. Today, embrace your inner light and let it guide your path. The stars support your journey.",
            "theme": "general",
            "date": today,
            "key_words": ["cosmos", "possibility", "light"],
            "daily_focus": "Self-discovery and growth"
        }
    
    return result

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            action = data.get('action', 'start')
            
            if action == 'start':
                result = generate_cosmic_message(
                    name=data.get('name', ''),
                    theme=data.get('theme', 'general'),
                    tone=data.get('tone', 'mystical')
                )
            elif action == 'daily':
                result = get_daily_cosmic_reading()
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
