#!/usr/bin/env python3
"""
AI Compliment Generator - Combined API
Actions: generate, personalize, random
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

def generate_compliment(category: str = "general", recipient_gender: str = "any", tone: str = "warm"):
    """Generate a compliment"""
    prompt = f'''Write a genuine, uplifting compliment.

Category: {category if category != "general" else "any"}
Recipient gender: {recipient_gender}
Tone: {tone}

Return ONLY valid JSON with these fields:
- compliment: string (the compliment text)
- category: "{category}"
- tone: "{tone}"
- sincerity_level: integer (1-10)
- best_for: string (when to give this compliment)
- follow_up: string (optional way to continue conversation)

Make it feel personal and authentic, not generic.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    comp = extract_json(text)

    if not comp or 'compliment' not in comp:
        comp = {
            "compliment": "You have such a wonderful energy that brightens any room.",
            "category": "general",
            "tone": tone,
            "sincerity_level": 9,
            "best_for": "Casual compliments to friends or colleagues",
            "follow_up": "I really mean that by the way."
        }

    return {"compliment": comp, "category": category, "recipient_gender": recipient_gender}

def personalize_compliment(base_compliment: str, recipient_name: str, context: str = ""):
    """Personalize a compliment with name and context"""
    prompt = f'''Personalize this compliment for {recipient_name}:

Base compliment: "{base_compliment}"

Context: {context if context else "None provided"}

Return ONLY valid JSON with these fields:
- personalized: string (compliment with name and context woven in)
- personalization_level: string ("light", "moderate", "deep")
- why_personal: string (explanation of personalization choices)
- original: "{base_compliment}"

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    pers = extract_json(text)

    if not pers or 'personalized' not in pers:
        pers = {
            "personalized": f"{recipient_name}, {base_compliment}",
            "personalization_level": "light",
            "why_personal": "Added name for personal connection.",
            "original": base_compliment
        }

    return {"personalized": pers, "recipient_name": recipient_name, "context": context}

def random_compliment_batch(count: int = 5):
    """Generate a batch of random compliments"""
    categories = ["appearance", "personality", "skills", "effort", "character", "creativity"]
    import random
    selected_cats = random.sample(categories, min(count, len(categories)))

    prompt = f'''Generate {count} genuine, uplifting compliments for various situations.

Categories: {', '.join(selected_cats)}

Return ONLY valid JSON with these fields:
- compliments: array of objects with:
  - compliment: string
  - category: string (from the above)
  - tone: string (warm, playful, sincere, enthusiastic)
  - when_to_use: string (appropriate situation)
- total: {count}

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    batch = extract_json(text)

    if not batch or 'compliments' not in batch or not isinstance(batch['compliments'], list):
        batch = {
            "compliments": [
                {"compliment": "You make the people around you better.", "category": "personality", "tone": "sincere", "when_to_use": "Anytime"}
            ],
            "total": count
        }

    return {"compliments": batch["compliments"][:count], "batch_size": count}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_compliment(
                    data.get('category', 'general'),
                    data.get('recipient_gender', 'any'),
                    data.get('tone', 'warm')
                )
            elif action == 'personalize':
                result = personalize_compliment(
                    data.get('base_compliment', ''),
                    data.get('recipient_name', ''),
                    data.get('context', '')
                )
            elif action == 'random':
                result = random_compliment_batch(
                    data.get('count', 5)
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
