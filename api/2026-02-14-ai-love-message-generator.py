#!/usr/bin/env python3
"""
AI Love Message Generator - Combined API
Actions: romantic, flirty, anniversary
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

def romantic_message(recipient_name: str = "", relationship_stage: str = "established", length: str = "medium"):
    """Generate a romantic love message"""
    prompt = f'''Write a {length} romantic love message{f" for {recipient_name}" if recipient_name else ""}.

Relationship stage: {relationship_stage} (affects tone and depth)

Return ONLY valid JSON with these fields:
- message: string (the love message, 1-4 sentences depending on length)
- recipient: "{recipient_name if recipient_name else 'love'}"
- relationship_stage: "{relationship_stage}"
- sentiment_level: integer (1-10 how deeply romantic)
- use_case: string (text, card, spoken, etc.)
- poetic_elements: array of 2-3 strings (metaphors, imagery used)
- delivery_tip: string (how to make it extra special)

Make it heartfelt, genuine, and appropriate for the relationship stage.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    msg = extract_json(text)

    if not msg or 'message' not in msg:
        msg = {
            "message": f"You are my favorite hello and hardest goodbye. I love you more each day.",
            "recipient": recipient_name if recipient_name else "my love",
            "relationship_stage": relationship_stage,
            "sentiment_level": 8,
            "use_case": "Any romantic moment",
            "poetic_elements": ["Favorite hello/hardest goodbye cliché", "Growing love metaphor"],
            "delivery_tip": "Say it while looking into their eyes."
        }

    return {"message": msg, "recipient": recipient_name, "stage": relationship_stage}

def flirty_message(style: str = "witty", target: str = "crush"):
    """Generate a flirty message"""
    prompt = f'''Write a {style} flirty message for a {target}.

Flirty should be:
- Playful and fun
- Not overly forward
- Leaves room for reciprocation
- Has a spark of romantic interest

Return ONLY valid JSON with these fields:
- message: string
- style: "{style}"
- target: "{target}"
- flirt_level: integer (1-10 how bold)
- pickup_line_vibes: boolean (if it feels like a pickup line)
- ideal_setting: string (where to send/deliver)
- response_hint: string (what kind of reply it might elicit)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    flirty = extract_json(text)

    if not flirty or 'message' not in flirty:
        flirty = {
            "message": "Is it hot in here or is it just the chemistry between us?",
            "style": style,
            "target": target,
            "flirt_level": 6,
            "pickup_line_vibes": True,
            "ideal_setting": "text or casual hangout",
            "response_hint": "They'll likely laugh or play back"
        }

    return {"flirty": flirty, "style": style, "target": target}

def anniversary_message(years: int = 1, partner_name: str = "", memory_shared: str = ""):
    """Generate anniversary message"""
    prompt = f'''Write a heartfelt anniversary message{f" for {partner_name}" if partner_name else ""}.

Number of years together: {years}
{f"Special memory to reference: {memory_shared}" if memory_shared else ""}

Return ONLY valid JSON with these fields:
- message: string
- years: {years}
- partner: "{partner_name}"
- nostalgia_level: integer (1-10 how much it references the past)
- future_promise: string (reference to continuing journey)
- memory_mentioned: string (the shared memory if provided)
- romantic_gesture_suggestion: string (what to pair this with)

Should celebrate love, commitment, and shared history.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    anniversary = extract_json(text)

    if not anniversary or 'message' not in anniversary:
        anniversary = {
            "message": f"Every year with you feels like the first. Happy {years} year{'s' if years > 1 else ''}!",
            "years": years,
            "partner": partner_name if partner_name else "my love",
            "nostalgia_level": 7,
            "future_promise": "Here's to many more years of us.",
            "memory_mentioned": memory_shared or "When we first met",
            "romantic_gesture_suggestion": "Pair with a photo album or special dinner"
        }

    return {"anniversary": anniversary, "years": years, "partner": partner_name}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'romantic')

            if action == 'romantic':
                result = romantic_message(
                    data.get('recipient_name', ''),
                    data.get('relationship_stage', 'established'),
                    data.get('length', 'medium')
                )
            elif action == 'flirty':
                result = flirty_message(
                    data.get('style', 'witty'),
                    data.get('target', 'crush')
                )
            elif action == 'anniversary':
                result = anniversary_message(
                    data.get('years', 1),
                    data.get('partner_name', ''),
                    data.get('memory_shared', '')
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
