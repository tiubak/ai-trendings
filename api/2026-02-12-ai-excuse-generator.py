#!/usr/bin/env python3
"""
AI Excuse Generator - Combined API
Actions: generate, socially_acceptable, funny
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

def generate_excuse(situation: str, audience: str = "casual", credibility: str = "reasonable"):
    """Generate an excuse"""
    prompt = f'''Generate a {credibility} excuse for: {situation}

Audience: {audience} (affects how formal/specific the excuse should be)

Return ONLY valid JSON with these fields:
- excuse: string (the excuse itself, 1-2 sentences max)
- credibility_level: integer (1-10 how believable)
- social_risk: string ("low", "medium", "high")
- when_to_use: string (appropriate situations)
- backup_story: string (one additional detail to make it more believable)
- warning: string (caution about overusing this excuse)

The excuse should be plausible, brief, and appropriate for the audience.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    exc = extract_json(text)

    if not exc or 'excuse' not in exc:
        exc = {
            "excuse": "Something urgent came up and I need to reschedule.",
            "credibility_level": 7,
            "social_risk": "low",
            "when_to_use": "Canceling plans last minute",
            "backup_story": "Family emergency that can't be postponed.",
            "warning": "Don't overuse vague excuses - people catch on."
        }

    return {"excuse": exc, "situation": situation, "audience": audience}

def socially_acceptable_excuse(profession: str = "", reason_needed: str = ""):
    """Generate socially acceptable excuses (work-appropriate)"""
    prompt = f'''Generate a professional, socially acceptable excuse{f" for: {reason_needed}" if reason_needed else ""}.

{f"Profession context: {profession}" if profession else ""} (may tailor to workplace norms)

Return ONLY valid JSON with these fields:
- excuse: string
- professionalism_score: integer (1-10)
- appropriate_for_work: boolean
- delivery_tip: string (how to present it professionally)
- alternative_phrasings: array of 2-3 variations
- why_it_works: string

Make it sound legitimate without being dishonest.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    soc = extract_json(text)

    if not soc or 'excuse' not in soc:
        soc = {
            "excuse": "I have a prior commitment that cannot be changed.",
            "professionalism_score": 8,
            "appropriate_for_work": True,
            "delivery_tip": "Be vague but confident. Don't over-explain.",
            "alternative_phrasings": ["I'm unfortunately tied up with something else", "My schedule is unexpectedly blocked"],
            "why_it_works": "Unspecific but professional; people respect privacy"
        }

    return {"excuse": soc, "profession": profession, "reason": reason_needed}

def funny_excuse(absurdity_level: str = "moderate"):
    """Generate funny, absurd excuses (for friends/social)"""
    prompt = f'''Generate a {absurdity_level}-absurdity funny excuse.

Should be obviously humorous, not meant to be believed. Good for texting friends or breaking tension.

Return ONLY valid JSON with these fields:
- excuse: string (the funny excuse)
- laugh_factor: integer (1-10 how funny)
- absurdity_score: integer (1-10)
- best_for: string (who to use it with)
- straight_man_alternative: string (how to follow up if they joke back)
- emoji_suggestions: array of 2-3 emojis to accompany

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    funny = extract_json(text)

    if not funny or 'excuse' not in funny:
        funny = {
            "excuse": "My pet dragon ate my schedule.",
            "laugh_factor": 8,
            "absurdity_score": 9,
            "best_for": "Close friends who know you don't have a dragon",
            "straight_man_alternative": "Yeah, he's a messy eater.",
            "emoji_suggestions": ["🐉", "🔥", "😅"]
        }

    return {"excuse": funny, "absurdity_level": absurdity_level}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_excuse(
                    data.get('situation', ''),
                    data.get('audience', 'casual'),
                    data.get('credibility', 'reasonable')
                )
            elif action == 'socially_acceptable':
                result = socially_acceptable_excuse(
                    data.get('profession', ''),
                    data.get('reason_needed', '')
                )
            elif action == 'funny':
                result = funny_excuse(
                    data.get('absurdity_level', 'moderate')
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
