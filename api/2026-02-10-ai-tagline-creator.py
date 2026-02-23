#!/usr/bin/env python3
"""
AI Tagline Creator - Combined API
Actions: create, refine, from_keywords
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

def create_tagline(product_name: str, industry: str = "", brand_personality: str = "", target_audience: str = ""):
    """Create taglines for a product/brand"""
    prompt = f'''Generate 5 catchy, memorable taglines for{f" {product_name}" if product_name else " a product"}.

Industry: {industry if industry else "general"}
Brand personality: {brand_personality if brand_personality else "friendly and approachable"}
Target audience: {target_audience if target_audience else "general consumers"}

Return ONLY valid JSON with these fields:
- taglines: array of objects with:
  - tagline: string
  - word_count: integer
  - tone: string (e.g., "bold", "playful", "emotional", "benefit-driven")
  - uniqueness_score: integer (1-10)
  - memorability_hook: string (what makes it stick)
- total_generated: 5

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    tagline_data = extract_json(text)

    if not tagline_data or 'taglines' not in tagline_data or not isinstance(tagline_data['taglines'], list):
        tagline_data = {
            "taglines": [
                {"tagline": f"Simply {product_name or 'Amazing'}", "word_count": 2, "tone": "simple", "uniqueness_score": 7, "memorability_hook": "Repetition of brand name"},
                {"tagline": f"{product_name or 'Innovation'} that works for you", "word_count": 4, "tone": "benefit-driven", "uniqueness_score": 6, "memorability_hook": "User benefit focus"}
            ],
            "total_generated": 5
        }

    return {"taglines": tagline_data["taglines"][:5], "product": product_name, "industry": industry}

def refine_tagline(original_tagline: str, refinement_goal: str = ""):
    """Improve an existing tagline"""
    prompt = f'''Refine this tagline to make it better:

Original: "{original_tagline}"

Refinement goal: {refinement_goal if refinement_goal else "Make it more memorable and impactful"}

Generate 3 refined versions.

Return ONLY valid JSON with these fields:
- original: "{original_tagline}"
- refinements: array of objects with:
  - tagline: string
  - improvement: string (what was improved)
  - word_count: integer
  - catchiness: integer (1-10)
- refinement_goal: "{refinement_goal}"

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    refined = extract_json(text)

    if not refined or 'refinements' not in refined:
        refined = {
            "original": original_tagline,
            "refinements": [
                {"tagline": original_tagline, "improvement": "No refinement", "word_count": len(original_tagline.split()), "catchiness": 5}
            ],
            "refinement_goal": refinement_goal
        }

    return {"refined": refined, "original": original_tagline}

def from_keywords(keywords: list, industry: str = ""):
    """Generate taglines from a set of keywords"""
    keywords_str = ", ".join(keywords)
    prompt = f'''Create 5 tagline ideas using these keywords: {keywords_str}.

Industry: {industry if industry else "general"}

Get creative! Taglines should incorporate keywords naturally or conceptually.

Return ONLY valid JSON with these fields:
- taglines: array of objects with:
  - tagline: string
  - keywords_used: array of strings (which keywords appear)
  - creative_interpretation: string (how keywords were used)
  - fit_for_industry: boolean
- total: 5

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    keyword_data = extract_json(text)

    if not keyword_data or 'taglines' not in keyword_data:
        keyword_data = {
            "taglines": [
                {"tagline": " ".join(keywords[:2]) + " for all", "keywords_used": keywords[:2], "creative_interpretation": "Direct keyword use", "fit_for_industry": True}
            ],
            "total": 5
        }

    return {"taglines": keyword_data["taglines"][:5], "keywords": keywords, "industry": industry}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'create')

            if action == 'create':
                result = create_tagline(
                    data.get('product_name', ''),
                    data.get('industry', ''),
                    data.get('brand_personality', ''),
                    data.get('target_audience', '')
                )
            elif action == 'refine':
                result = refine_tagline(
                    data.get('original_tagline', ''),
                    data.get('refinement_goal', '')
                )
            elif action == 'from_keywords':
                result = from_keywords(
                    data.get('keywords', []),
                    data.get('industry', '')
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
