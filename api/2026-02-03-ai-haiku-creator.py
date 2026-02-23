#!/usr/bin/env python3
"""
AI Haiku Creator - Combined API
Actions: create, customize, generate_from_theme
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

def create_haiku(theme: str = "", mood: str = "", style: str = "traditional"):
    """Generate a haiku with optional parameters"""
    style_desc = "traditional 5-7-5 syllable structure" if style == "traditional" else "free-form modern haiku"

    prompt = f'''Write a beautiful {f"about {theme} " if theme else ""}{f"with a {mood} mood " if mood else ""}in {style_desc}.

The haiku should capture a moment in nature, evoke emotion, and use vivid imagery.

Return ONLY valid JSON with these fields:
- haiku: string (line breaks with \\n for newlines)
- syllables: string (5-7-5 or "free form" if modern style)
- theme: string (theme if provided, or detected theme)
- mood: string (emotional tone)
- explanation: string (2-3 sentences explaining the imagery and feeling)

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    haiku_result = extract_json(text)

    if not haiku_result or 'haiku' not in haiku_result:
        haiku_result = {
            "haiku": "Autumn moonlight\nA worm digs silently\nInto the chestnut",
            "syllables": "5-7-5",
            "theme": theme if theme else "nature",
            "mood": mood if mood else "contemplative",
            "explanation": "A classic haiku capturing a quiet moment of observation, typical of traditional Japanese form."
        }

    return {"haiku": haiku_result, "theme": theme, "mood": mood, "style": style}

def customize_haiku(original_haiku: str, modification: str):
    """Modify an existing haiku"""
    prompt = f'''Modify this haiku according to the request:

Original haiku:
{original_haiku}

Modification request: {modification}

Return ONLY valid JSON with these fields:
- haiku: string (modified version with \\n for line breaks)
- modifications_made: array of 2-3 strings describing what changed
- why_it_fits: string (explanation of how modification improves the haiku)

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    customized = extract_json(text)

    if not customized or 'haiku' not in customized:
        customized = {
            "haiku": original_haiku,
            "modifications_made": ["No modification made - preserving original"],
            "why_it_fits": "The original haiku was maintained as no specific changes were provided."
        }

    return {"customized": customized, "original": original_haiku, "modification_request": modification}

def generate_from_theme(season: str = "", time_of_day: str = "", element: str = ""):
    """Generate haiku from specific natural themes"""
    prompt_parts = ["Write a haiku"]
    if season:
        prompt_parts.append(f"about {season}")
    if time_of_day:
        prompt_parts.append(f"set during {time_of_day}")
    if element:
        prompt_parts.append(f"featuring {element}")

    prompt = " ".join(prompt_parts) + "."

    prompt += '''

Return ONLY valid JSON with these fields:
- haiku: string (5-7-5 syllable structure with \\n)
- imagery: string (description of the visual scene)
- sensory_details: array of 3 strings (what you can see, hear, feel)
- seasonal_kigo: string (the seasonal reference used)
- emotional_essence: string (the feeling this haiku conveys)

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    themed = extract_json(text)

    if not themed or 'haiku' not in themed:
        themed = {
            "haiku": "Cherry blossoms fall\nPetals dance on gentle breeze\nSpring whispers hello",
            "imagery": "Pink cherry blossoms detaching from branches and floating on a soft wind",
            "sensory_details": ["Pink petals in vision", "Gentle breeze on skin", "Sweet floral scent"],
            "seasonal_kigo": "cherry blossoms (spring)",
            "emotional_essence": "Gentle renewal and fleeting beauty"
        }

    return {"haiku": themed, "season": season, "time": time_of_day, "element": element}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'create')

            if action == 'create':
                result = create_haiku(
                    data.get('theme', ''),
                    data.get('mood', ''),
                    data.get('style', 'traditional')
                )
            elif action == 'customize':
                result = customize_haiku(
                    data.get('original_haiku', ''),
                    data.get('modification', '')
                )
            elif action == 'generate_from_theme':
                result = generate_from_theme(
                    data.get('season', ''),
                    data.get('time_of_day', ''),
                    data.get('element', '')
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
