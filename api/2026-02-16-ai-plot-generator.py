#!/usr/bin/env python3
"""
AI Plot Generator - Combined API
Actions: generate, twist, structure
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

def generate_plot(genre: str = "fantasy", length: str = "short", protagonist_type: str = ""):
    """Generate a complete plot outline"""
    prompt = f'''Generate a {length} plot outline for a {genre} story.

{f"Protagonist type: {protagonist_type}" if protagonist_type else ""}

Return ONLY valid JSON with these fields:
- title: string (catchy working title)
- hook: string (logline: 1-2 sentence pitch)
- structure: array of 3-5 acts with:
  - act_number: integer
  - title: string
  - summary: string (1-2 sentences)
- key_twists: array of 2-3 major plot twists
- climax: string (climax description, 1-2 sentences)
- resolution: string (how it ends)
- genre_conventions: array of 2-3 genre tropes used

Make it compelling, logically sound, and with emotional stakes.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    plot = extract_json(text)

    if not plot or 'title' not in plot:
        plot = {
            "title": f"The {genre.title()} Quest",
            "hook": f"A {protagonist_type or 'hero'} must undertake a dangerous journey to save their world from destruction.",
            "structure": [
                {"act_number": 1, "title": "The Call", "summary": "Protagonist receives call to adventure, initially refuses."},
                {"act_number": 2, "title": "The Journey", "summary": "Challenges and growth on the road."},
                {"act_number": 3, "title": "Confrontation", "summary": "Final battle/climax."}
            ],
            "key_twists": ["The mentor was the villain.", "The protagonist has a hidden power."],
            "climax": "Hero faces antagonist in final confrontation.",
            "resolution": "Order restored, protagonist transformed.",
            "genre_conventions": ["The chosen one", "Mentor figure", "Quest narrative"]
        }

    return {"plot": plot, "genre": genre, "length": length, "protagonist": protagonist_type}

def add_twist(plot_outline: dict, twist_type: str = "unexpected"):
    """Add a plot twist to an existing outline"""
    prompt = f'''Add a {twist_type} plot twist to this story structure:

{json.dumps(plot_outline, indent=2)}

Return ONLY valid JSON with these fields:
- original_title: string
- twist_added: string (description of new twist)
- affected_acts: array of integers (which acts will change)
- new_structure: array of modified acts (only act number and modified summary)
- twist_reasoning: string (why this twist works in this story)
- reader_reaction: string ("shock", "satisfying revelation", "gut-punch", etc.)

Focus on making the twist meaningful, not just random.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    twist_data = extract_json(text)

    if not twist_data or 'twist_added' not in twist_data:
        twist_data = {
            "original_title": plot_outline.get('title', 'Untitled'),
            "twist_added": "The true villain is someone the protagonist trusted.",
            "affected_acts": [2, 3],
            "new_structure": plot_outline.get('structure', []),
            "twist_reasoning": "Betrayal by a trusted figure creates emotional impact and raises stakes.",
            "reader_reaction": "Shock and betrayal felt deeply"
        }

    return {"twist": twist_data, "original": plot_outline, "twist_type": twist_type}

def three_act_structure(topic: str, genre: str = "drama"):
    """Generate a three-act structure for a story idea"""
    prompt = f'''Create a classic three-act structure for a {genre} story about: {topic}

Return ONLY valid JSON with these fields:
- logline: string (1-2 sentence pitch)
- act_i_setup: object with:
  - ordinary_world: string (life before disruption)
  - inciting_incident: string (what changes everything)
  - key_character: string (protagonist intro)
- act_i_confrontation: object with:
  - rising_action: string (series of challenges)
  - midpoint: string (major turning point)
  - darkest_moment: string (all hope lost)
- act_iii_resolution: object with:
  - climax: string (final confrontation)
  - denouement: string (aftermath)
  - theme_fulfilled: string (how theme is proven)
- central_conflict: string (protagonist vs. what/whom)
- thematic_statement: string (what story says about topic)

Make it classic, satisfying, and emotionally resonant.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    structure = extract_json(text)

    if not structure or 'logline' not in structure:
        structure = {
            "logline": f"A {genre.lower()} story about {topic}.",
            "act_i_setup": {"ordinary_world": "Life is normal but unfulfilling", "inciting_incident": "Something disrupts routine", "key_character": "An ordinary person with hidden potential"},
            "act_ii_confrontation": {"rising_action": "Challenges mount, allies and enemies revealed", "midpoint": "Major setback or revelation", "darkest_moment": "All is lost, impossible to continue"},
            "act_iii_resolution": {"climax": "Final confrontation using all learned", "denouement": "New equilibrium reached", "theme_fulfilled": "Justice served / growth achieved"},
            "central_conflict": "Protagonist vs. antagonist/internal struggle",
            "thematic_statement": f"About {topic}, the story shows that perseverance wins."
        }

    return {"structure": structure, "topic": topic, "genre": genre}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_plot(
                    data.get('genre', 'fantasy'),
                    data.get('length', 'short'),
                    data.get('protagonist_type', '')
                )
            elif action == 'twist':
                result = add_twist(
                    data.get('plot_outline', {}),
                    data.get('twist_type', 'unexpected')
                )
            elif action == 'structure':
                result = three_act_structure(
                    data.get('topic', ''),
                    data.get('genre', 'drama')
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
