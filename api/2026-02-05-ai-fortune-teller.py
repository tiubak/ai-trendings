#!/usr/bin/env python3
"""
AI Fortune Teller - Combined API
Actions: tell_fortune, daily_horoscope, destiny_reading
"""

import os
import json
import logging
import re
from datetime import datetime
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

def tell_fortune(user_name: str, question: str = "", focus_area: str = "general"):
    """Tell a personalized fortune"""
    today = datetime.now().strftime("%A, %B %d")
    prompt = f'''Create a mystical, encouraging fortune for {user_name} on {today}.

Question asked (if any): {question if question else "None"}
Focus area: {focus_area}

Return ONLY valid JSON with these fields:
- fortune: string (the main fortune message, 3-5 sentences)
- lucky_number: integer (1-100)
- lucky_color: string
- lucky_element: string (fire, water, earth, air, ether, etc.)
- omen: string ("favorable", "neutral", "challenging")
- guidance: string (specific actionable advice)
- planetary_influence: string (which planet/energy is strong today)

No markdown, no explanation, just the JSON.'''

    text = call_pollinations(prompt)
    fortune_data = extract_json(text)

    if not fortune_data or 'fortune' not in fortune_data:
        fortune_data = {
            "fortune": f"The stars align in your favor today, {user_name}. Trust your intuition as opportunities emerge. A surprise encounter may hold significance.",
            "lucky_number": 42,
            "lucky_color": "royal blue",
            "lucky_element": "air",
            "omen": "favorable",
            "guidance": "Take a different route today - serendipity awaits.",
            "planetary_influence": "Mercury in harmonious aspect"
        }

    return {"fortune": fortune_data, "name": user_name, "question": question, "focus": focus_area}

def daily_horoscope(zodiac_sign: str):
    """Generate daily horoscope"""
    prompt = f'''Write a daily horoscope for {zodiac_sign}.

Return ONLY valid JSON with these fields:
- sign: "{zodiac_sign}"
- date: string (today's date)
- overview: string (2-3 sentences)
- love: string (relationship advice)
- career: string (work/finance advice)
- health: string (wellbeing guidance)
- lucky_time: string (time of day)
- compatibility: string (which sign they'll harmonize with today)
- caution: string (what to watch out for)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    horoscope = extract_json(text)

    if not horoscope or 'overview' not in horoscope:
        today = datetime.now().strftime("%B %d, %Y")
        horoscope = {
            "sign": zodiac_sign,
            "date": today,
            "overview": f"The cosmic energies favor {zodiac_sign} today. Your natural qualities will shine through.",
            "love": "Open communication brings deeper connection.",
            "career": "A small adjustment yields significant results.",
            "health": "Listen to your body's needs today.",
            "lucky_time": "mid-afternoon",
            "compatibility": " Libra",
            "caution": "Avoid rushing important decisions."
        }

    return {"horoscope": horoscope, "sign": zodiac_sign}

def destiny_reading(birth_month: int, birth_year: int, life_question: str = ""):
    """Provide a destiny/life path reading"""
    elements = ["fire", "earth", "air", "water"]
    zodiac_animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

    prompt = f'''Create a destiny reading for someone born in {birth_month}/{birth_year}.

Life question: {life_question if life_question else "No specific question"}

Return ONLY valid JSON with these fields:
- life_path_number: integer (calculate from birth month/year)
- zodiac_animal: string (Chinese zodiac)
- element: string (one of: fire, earth, air, water)
- core_trait: string (defining characteristic)
- soul_purpose: string (2-3 sentences about life purpose)
- challenge: string (main life challenge to overcome)
- gift: string (natural gift/strength)
- decade_theme: string (what this 10-year period is about)
- advice: string (personalized guidance)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    reading = extract_json(text)

    if not reading or 'life_path_number' not in reading:
        reading = {
            "life_path_number": (birth_month + birth_year) % 9 + 1,
            "zodiac_animal": zodiac_animals[(birth_year - 1900) % 12],
            "element": elements[(birth_month + birth_year) % 4],
            "core_trait": "Resilient and intuitive",
            "soul_purpose": "To learn through experience and guide others with wisdom gained.",
            "challenge": "Balancing independence with connection",
            "gift": "Natural empathy and insight",
            "decade_theme": "Building foundations for lasting legacy",
            "advice": "Trust the journey, even when the path is unclear."
        }

    return {"reading": reading, "birth_month": birth_month, "birth_year": birth_year, "question": life_question}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'tell_fortune')

            if action == 'tell_fortune':
                result = tell_fortune(
                    data.get('user_name', 'Seeker'),
                    data.get('question', ''),
                    data.get('focus_area', 'general')
                )
            elif action == 'daily_horoscope':
                result = daily_horoscope(
                    data.get('zodiac_sign', 'Aries')
                )
            elif action == 'destiny_reading':
                result = destiny_reading(
                    data.get('birth_month', 1),
                    data.get('birth_year', 2000),
                    data.get('life_question', '')
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
