#!/usr/bin/env python3
"""
AI Color Palette Generator - Combined API
Actions: from_mood, from_keyword, harmonious
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

def from_mood(mood: str, palette_size: int = 5):
    """Generate color palette from a mood/emotion"""
    prompt = f'''Create a color palette that evokes the mood "{mood}".

Generate {palette_size} colors as a palette.

Return ONLY valid JSON with these fields:
- palette: array of objects, each with:
  - name: string (descriptive color name)
  - hex: string (6-digit hex code)
  - rgb: string (rgb(r,g,b) format)
  - description: string (how this color contributes to mood)
- overall_mood: "{mood}"
- usage_tip: string (how to apply this palette)

Ensure colors are visually cohesive and accessible.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    palette_data = extract_json(text)

    if not palette_data or 'palette' not in palette_data or not isinstance(palette_data['palette'], list):
        defaults = {
            "calm": ["#87CEEB", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"],
            "energy": ["#FF6B6B", "#FFA502", "#FFD93D", "#6BCB77", "#4D96FF"],
            "luxury": ["#1A1A2E", "#16213E", "#0F3460", "#E94560", "#F8B500"]
        }
        colors = defaults.get(mood.lower(), defaults["calm"])
        palette_data = {
            "palette": [
                {"name": f"{mood.title()} Color 1", "hex": colors[0], "rgb": "135,206,235", "description": "Primary calming tone"},
                {"name": f"{mood.title()} Color 2", "hex": colors[1], "rgb": "152,216,200", "description": "Supporting accent"},
                {"name": f"{mood.title()} Color 3", "hex": colors[2], "rgb": "247,220,111", "description": "Highlight"},
                {"name": f"{mood.title()} Color 4", "hex": colors[3], "rgb": "187,143,206", "description": "Depth"},
                {"name": f"{mood.title()} Color 5", "hex": colors[4], "rgb": "133,193,233", "description": "Balance"}
            ][:palette_size],
            "overall_mood": mood,
            "usage_tip": f"Use these colors to create a {mood} atmosphere in your designs."
        }

    return {"palette": palette_data, "mood": mood, "size": palette_size}

def from_keyword(keyword: str, style: str = "modern"):
    """Generate palette from keyword"""
    prompt = f'''Generate a color palette inspired by the keyword "{keyword}" in a {style} style.

Return ONLY valid JSON with these fields:
- keyword: "{keyword}"
- style: "{style}"
- palette: array of 5 objects with:
  - name: string
  - hex: string (6-digit)
  - meaning: string (why this color fits the keyword)
- total_vibe: string (overall description)
- best_use_cases: array of 3 strings (what kind of projects this palette suits)

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    keyword_data = extract_json(text)

    if not keyword_data or 'palette' not in keyword_data:
        keyword_data = {
            "keyword": keyword,
            "style": style,
            "palette": [
                {"name": f"{keyword.title()} Primary", "hex": "#3498DB", "meaning": f"Primary color representing {keyword}"},
                {"name": f"{keyword.title()} Secondary", "hex": "#2ECC71", "meaning": f"Supporting color for {keyword}"},
                {"name": f"{keyword.title()} Accent", "hex": "#9B59B6", "meaning": f"Accent color highlighting {keyword}"},
                {"name": f"{keyword.title()} Neutral", "hex": "#ECF0F1", "meaning": "Neutral background"},
                {"name": f"{keyword.title()} Dark", "hex": "#2C3E50", "meaning": "Strong contrast"}
            ],
            "total_vibe": f"A {style} palette inspired by {keyword}",
            "best_use_cases": ["Web design", "Branding", "UI/UX"]
        }

    return {"palette_data": keyword_data, "keyword": keyword, "style": style}

def harmonious(base_color: str):
    """Generate harmonious colors from a base color"""
    prompt = f'''Given the base color {base_color}, generate 4 harmonious colors for a 5-color palette.

The harmonious colors should create a cohesive scheme (complementary, analogous, or triadic).

Return ONLY valid JSON with these fields:
- base_color: "{base_color}"
- scheme_type: string ("complementary", "analogous", "triadic", "tetradic")
- palette: array of 5 objects:
  - name: string
  - hex: string
  - role: string (base, complementary, accent1, accent2, neutral)
  - harmony_explanation: string (why these colors work together)
- contrast_ratio: string (WCAG accessibility level)

Ensure good contrast and accessibility.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    harmony = extract_json(text)

    if not harmony or 'palette' not in harmony:
        harmony = {
            "base_color": base_color,
            "scheme_type": "analogous",
            "palette": [
                {"name": "Base", "hex": base_color or "#3498DB", "role": "base", "harmony_explanation": "Your starting color"},
                {"name": "Harmony 1", "hex": "#5DADE2", "role": "complementary", "harmony_explanation": "Creates balanced contrast"},
                {"name": "Harmony 2", "hex": "#AED6F1", "role": "accent1", "harmony_explanation": "Lighter variation"},
                {"name": "Harmony 3", "hex": "#2E86C1", "role": "accent2", "harmony_explanation": "Deeper variation"},
                {"name": "Neutral", "hex": "#F8F9F9", "role": "neutral", "harmony_explanation": "Background/white space"}
            ],
            "contrast_ratio": "AA"
        }

    return {"harmony": harmony, "base": base_color}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'from_mood')

            if action == 'from_mood':
                result = from_mood(
                    data.get('mood', 'calm'),
                    data.get('palette_size', 5)
                )
            elif action == 'from_keyword':
                result = from_keyword(
                    data.get('keyword', ''),
                    data.get('style', 'modern')
                )
            elif action == 'harmonious':
                result = harmonious(
                    data.get('base_color', '#3498DB')
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
