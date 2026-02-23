#!/usr/bin/env python3
"""
AI Playful Insult Generator - Combined API
Actions: generate, between_friends, roast_me
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

def generate_insult(target_type: str = "personality", intensity: str = "light", relationship: str = "friends"):
    """Generate a playful insult"""
    prompt = f'''Write a playful, {intensity} insult targeting {target_type}.

Relationship context: {relationship} (affects how harsh/soft the insult is)

IMPORTANT: Must be clearly joking, not genuinely hurtful. Include obvious humor signals.

Return ONLY valid JSON with these fields:
- insult: string (the playful insult)
- intensity: "{intensity}"
- target: "{target_type}"
- relationship: "{relationship}"
- humor_style: string (sarcasm, exaggeration, teasing, etc.)
- safe_for_relationship: boolean
- smiley_suggestion: string (emoji to soften it)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    insult = extract_json(text)

    if not insult or 'insult' not in insult:
        insult = {
            "insult": "You're so weird, it's kind of amazing.",
            "intensity": intensity,
            "target": target_type if target_type else "personality",
            "relationship": relationship,
            "humor_style": "teasing",
            "safe_for_relationship": True,
            "smiley_suggestion": "😄"
        }

    return {"insult": insult, "target_type": target_type, "intensity": intensity}

def between_friends(friend_quirk: str = ""):
    """Generate a friendly tease for a specific quirk"""
    prompt = f'''Create a friendly, affectionate tease{f" about {friend_quirk}" if friend_quirk else " about a typical friend quirk"}.

Should make the friend laugh, not feel bad. End with positive reinforcement.

Return ONLY valid JSON with these fields:
- tease: string (the playful insult/tease)
- quirk_targeted: string
- comeback_opportunity: string (how friend could fire back)
- affection_level: integer (1-10 how much you clearly like them)
- relationship_strength: string ("good friends", "besties", "childhood friends")
- follow_up_positive: string (something nice to say after)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    tease = extract_json(text)

    if not tease or 'tease' not in tease:
        tease = {
            "tease": "Only you would show up to a formal event wearing mismatched socks.",
            "quirk_targeted": "forgetfulness/fashion sense",
            "comeback_opportunity": "Says something about your weird laugh",
            "affection_level": 8,
            "relationship_strength": "besties",
            "follow_up_positive": "That's why I love you though!"
        }

    return {"tease": tease, "quirk": friend_quirk}

def roast_me(personality_trait: str = "", style: str = "light"):
    """Generate a self-deprecating roast (user insults themselves)"""
    style_map = {
        "light": "gentle self-deprecation",
        "moderate": "honest but funny self-critique",
        "brutal": "extreme but still playful self-roast"
    }

    prompt = f'''Write a {style_map[style]} self-roast.

{f"Target trait: {personality_trait}" if personality_trait else ""}

This should be the user insulting THEMSELVES in a funny way.

Return ONLY valid JSON with these fields:
- roast: string (the self-insult)
- style: "{style}"
- trait_targeted: string
- confidence_required: integer (1-10, how secure you need to be to say this)
- audience_reaction: string (what people would think/do)
- self_love_balance: string (how to balance laugh with self-acceptance)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    roast = extract_json(text)

    if not roast or 'roast' not in roast:
        roast = {
            "roast": "I'm not lazy, I'm on energy saving mode.",
            "style": style,
            "trait_targeted": personality_trait if personality_trait else "laziness joke",
            "confidence_required": 5,
            "audience_reaction": "Everyone nods, they've heard this one before",
            "self_love_balance": "Saying it with a smile shows you're secure"
        }

    return {"roast": roast, "style": style, "trait": personality_trait}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_insult(
                    data.get('target_type', 'personality'),
                    data.get('intensity', 'light'),
                    data.get('relationship', 'friends')
                )
            elif action == 'between_friends':
                result = between_friends(
                    data.get('friend_quirk', '')
                )
            elif action == 'roast_me':
                result = roast_me(
                    data.get('personality_trait', ''),
                    data.get('style', 'light')
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
