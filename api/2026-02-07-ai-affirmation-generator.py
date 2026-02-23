#!/usr/bin/env python3
"""
AI Affirmation Generator - Combined API
Actions: generate, personalize, daily_affirmations
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

def generate_affirmation(focus_area: str, intensity: str = "moderate", duration: str = "short"):
    """Generate a custom affirmation"""
    prompt = f'''Write a powerful {intensity}-intensity affirmation for {focus_area}.

Duration: {duration} (short = 1 sentence, medium = 2-3 sentences, long = 1 paragraph)

The affirmation should:
- Be in present tense, as if already true
- Be positive and empowering
- Be personally meaningful
- Include emotional and sensory language

Return ONLY valid JSON with these fields:
- affirmation: string (the full affirmation text)
- focus_area: "{focus_area}"
- intensity: "{intensity}"
- keywords: array of 3-5 power words from the affirmation
- suggested_usage: string (when/how to use it)
- belief_level: integer (1-10, how strongly to believe it while saying)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    aff = extract_json(text)

    if not aff or 'affirmation' not in aff:
        aff = {
            "affirmation": "I am worthy of love and capable of achieving my dreams.",
            "focus_area": focus_area if focus_area else "general well-being",
            "intensity": intensity,
            "keywords": ["worthy", "love", "capable", "dreams"],
            "suggested_usage": "Say each morning while looking in the mirror",
            "belief_level": 7
        }

    return {"affirmation": aff, "focus": focus_area, "intensity": intensity}

def personalize_affirmation(base_affirmation: str, name: str, personal_details: str = ""):
    """Personalize an existing affirmation"""
    prompt = f'''Personalize this affirmation for {name}:

Base affirmation: "{base_affirmation}"

Personal details: {personal_details if personal_details else "None provided"}

Return ONLY valid JSON with these fields:
- personalized: string (affirmation with name and personal touches)
- changes_made: array of strings (what was personalized)
- why_personal: string (why personalization helps)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    pers = extract_json(text)

    if not pers or 'personalized' not in pers:
        pers = {
            "personalized": f"Dear {name}, {base_affirmation}",
            "changes_made": ["Added name", "Added salutation"],
            "why_personal": "Using your name makes the affirmation feel directed and personal."
        }

    return {"personalized": pers, "base": base_affirmation, "name": name}

def daily_affirmations_set(areas: list = None):
    """Generate a daily set of affirmations for various life areas"""
    default_areas = ["self-love", "confidence", "gratitude", "success", "peace"]
    focus_areas = areas if areas else default_areas

    prompt = f'''Generate 5 morning affirmations for these life areas: {', '.join(focus_areas)}.

Each affirmation should be 1-2 sentences maximum.

Return ONLY valid JSON with these fields:
- affirmations: array of objects with:
  - area: string (life area)
  - affirmation: string
  - breath_count: integer (how many breaths to repeat)

No extra text.'''

    text = call_pollinations(prompt)
    daily_set = extract_json(text)

    if not daily_set or 'affirmations' not in daily_set or not isinstance(daily_set['affirmations'], list):
        daily_set = {
            "affirmations": [
                {"area": "self-love", "affirmation": "I love and accept myself completely.", "breath_count": 5},
                {"area": "confidence", "affirmation": "I am capable of handling any challenge.", "breath_count": 3},
                {"area": "gratitude", "affirmation": "I am grateful for all the good in my life.", "breath_count": 4},
                {"area": "success", "affirmation": "Success flows to me naturally and abundantly.", "breath_count": 3},
                {"area": "peace", "affirmation": "I am at peace with myself and the world.", "breath_count": 5}
            ]
        }

    return {"daily_set": daily_set["affirmations"], "date": "today"}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_affirmation(
                    data.get('focus_area', 'general well-being'),
                    data.get('intensity', 'moderate'),
                    data.get('duration', 'short')
                )
            elif action == 'personalize':
                result = personalize_affirmation(
                    data.get('base_affirmation', ''),
                    data.get('name', ''),
                    data.get('personal_details', '')
                )
            elif action == 'daily_affirmations':
                result = daily_affirmations_set(
                    data.get('areas')
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
