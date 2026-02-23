#!/usr/bin/env python3
"""
AI Name Generator - Combined API
Actions: baby_name, character_name, business_name
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

def baby_name(gender: str = "any", origin: str = "", meaning_pref: str = "", sibling_name: str = ""):
    """Generate baby name suggestions"""
    prompt = f'''Generate 5 baby name {f"suggestions for a {gender} baby" if gender != "any" else "suggestions"}.

Origin preference: {origin if origin else "any"}
Meaning preference: {meaning_pref if meaning_pref else "any"}
Sibling name: {sibling_name if sibling_name else "none"} (consider compatibility if provided)

Return ONLY valid JSON with these fields:
- names: array of objects with:
  - name: string
  - gender: string
  - origin: string
  - meaning: string (what the name means)
  - vibe: string (e.g., "classic", "modern", "nature-inspired")
- total_suggestions: 5

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    names_data = extract_json(text)

    if not names_data or 'names' not in names_data or not isinstance(names_data['names'], list):
        defaults = {
            "any": [{"name": "Avery", "gender": "unisex", "origin": "English", "meaning": "Elf counsel", "vibe": "modern"}],
            "boy": [{"name": "Liam", "gender": "boy", "origin": "Irish", "meaning": "Strong-willed warrior", "vibe": "classic"}],
            "girl": [{"name": "Emma", "gender": "girl", "origin": "German", "meaning": "Universal", "vibe": "timeless"}]
        }
        base = defaults.get(gender, defaults["any"])
        names_data = {
            "names": base * 5,
            "total_suggestions": 5
        }

    return {"names": names_data["names"][:5], "type": "baby", "gender": gender, "origin": origin}

def character_name(archetype: str, genre: str = "fantasy", gender: str = "any"):
    """Generate character names for stories/games"""
    prompt = f'''Generate 5 character names for a {archetype} character in a {genre} setting.

Gender: {gender}

Return ONLY valid JSON with these fields:
- names: array of objects with:
  - name: string
  - full_name: string (with optional surname/title)
  - archetype_match: string (how it fits the archetype)
  - cultural_inspiration: string (what culture the name evokes)
  - story_hook: string (1 sentence suggesting backstory)
- genre: "{genre}"

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    char_data = extract_json(text)

    if not char_data or 'names' not in char_data:
        char_data = {
            "names": [
                {"name": "Kaelen", "full_name": "Kaelen Shadowbane", "archetype_match": archetype, "cultural_inspiration": "Celtic fantasy", "story_hook": "Raised by wolves, learned magic from an ancient druid"}
            ],
            "genre": genre
        }

    return {"names": char_data["names"][:5], "type": "character", "archetype": archetype, "genre": genre}

def business_name(industry: str, style: str = "modern", keywords: list = None):
    """Generate business/company name ideas"""
    keywords_str = ", ".join(keywords) if keywords else "none"

    prompt = f'''Generate 5 creative business names for a {industry} company.

Style: {style}
Keywords to incorporate: {keywords_str}

Return ONLY valid JSON with these fields:
- names: array of objects with:
  - name: string (the business name)
  - tagline_suggestion: string (potential tagline)
  - memorability_score: integer (1-10)
  - domain_available: boolean (would .com likely be available?)
  - reasoning: string (why this name works for {industry})
- industry: "{industry}"

Make names memorable, brandable, and appropriate for the industry.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    biz_data = extract_json(text)

    if not biz_data or 'names' not in biz_data:
        biz_data = {
            "names": [
                {"name": f"{industry.title()}Flow", "tagline_suggestion": "Innovation that flows", "memorability_score": 8, "domain_available": True, "reasoning": f"Simple, memorable, suggests natural {industry} process"}
            ],
            "industry": industry
        }

    return {"names": biz_data["names"][:5], "type": "business", "industry": industry, "style": style}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'baby_name')

            if action == 'baby_name':
                result = baby_name(
                    data.get('gender', 'any'),
                    data.get('origin', ''),
                    data.get('meaning_pref', ''),
                    data.get('sibling_name', '')
                )
            elif action == 'character_name':
                result = character_name(
                    data.get('archetype', 'hero'),
                    data.get('genre', 'fantasy'),
                    data.get('gender', 'any')
                )
            elif action == 'business_name':
                result = business_name(
                    data.get('industry', 'tech'),
                    data.get('style', 'modern'),
                    data.get('keywords', [])
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
