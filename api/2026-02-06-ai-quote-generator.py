#!/usr/bin/env python3
"""
AI Quote Generator - Combined API
Actions: generate, by_theme, random_daily
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

def generate_quote(author_hint: str = "", topic: str = "", style: str = "inspirational"):
    """Generate an AI quote"""
    prompt = f'''Write an original, memorable quote{f" about {topic}" if topic else ""}{f" in the style of {author_hint}" if author_hint else ""}.

The quote should be:
- {style} in tone
- 10-25 words
- Thought-provoking and shareable
- Original, not a famous existing quote

Return ONLY valid JSON with these fields:
- quote: string (the quote itself)
- author: string (invented or "Anonymous" if not attributed)
- context: string (1-2 sentence explanation of the quote's meaning)
- tags: array of 3-5 relevant tags/themes
- style: "{style}"

No markdown, no explanation.'''

    text = call_pollinations(prompt)
    quote_data = extract_json(text)

    if not quote_data or 'quote' not in quote_data:
        quote_data = {
            "quote": "The only way to do great work is to love what you do.",
            "author": "AI Sage",
            "context": "Passion fuels excellence and sustains you through challenges.",
            "tags": ["passion", "work", "excellence"],
            "style": style
        }

    return {"quote": quote_data, "author_hint": author_hint, "topic": topic, "style": style}

def quotes_by_theme(theme: str, count: int = 5):
    """Generate multiple quotes on a specific theme"""
    prompt = f'''Generate {count} original quotes about {theme}.

Each quote should be unique and insightful.

Return ONLY valid JSON with these fields:
- quotes: array of objects, each with:
  - quote: string
  - author: string (invented name or "Anonymous")
  - tone: string (e.g., "wise", "playful", "reflective")

No extra text.'''

    text = call_pollinations(prompt)
    theme_data = extract_json(text)

    if not theme_data or 'quotes' not in theme_data or not isinstance(theme_data['quotes'], list):
        theme_data = {
            "quotes": [
                {"quote": f"Everything about {theme} teaches us about ourselves.", "author": "Philosophical AI", "tone": "wise"},
                {"quote": f"In {theme}, we find our truest selves.", "author": "Poetic Mind", "tone": "reflective"}
            ]
        }

    return {"quotes": theme_data["quotes"][:count], "theme": theme, "count": count}

def random_daily_quote():
    """Generate a random daily quote for inspiration"""
    topics = ["wisdom", "courage", "growth", "peace", "creativity", "resilience", "hope", "mindfulness", "success", "love"]
    import random
    random_topic = random.choice(topics)

    prompt = f'''Generate one profound, inspirational quote about {random_topic}.

Return ONLY valid JSON with these fields:
- quote: string
- author: string
- topic: "{random_topic}"
- day_of_year: string (e.g., "Day 36" - for tracking)
- reflection_prompt: string (a question to ponder about this quote)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    daily = extract_json(text)

    if not daily or 'quote' not in daily:
        daily = {
            "quote": f"Every moment of {random_topic} is a gift.",
            "author": "Universal Wisdom",
            "topic": random_topic,
            "day_of_year": "Day of Inspiration",
            "reflection_prompt": f"How can you invite more {random_topic} into your life today?"
        }

    return {"daily_quote": daily, "topic": random_topic}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_quote(
                    data.get('author_hint', ''),
                    data.get('topic', ''),
                    data.get('style', 'inspirational')
                )
            elif action == 'by_theme':
                result = quotes_by_theme(
                    data.get('theme', 'wisdom'),
                    data.get('count', 5)
                )
            elif action == 'random_daily':
                result = random_daily_quote()
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
