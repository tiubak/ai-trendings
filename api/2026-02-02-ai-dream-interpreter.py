#!/usr/bin/env python3
"""
AI Dream Interpreter - Combined API
Actions: interpret, explore_symbols
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

def interpret_dream(dream_description: str, dreamer_details: str = ""):
    """Interpret a dream and provide meaning"""
    prompt = f'''Interpret this dream and provide psychological insight:

Dream: {dream_description}
Dreamer context: {dreamer_details if dreamer_details else "General interpretation"}

Return ONLY valid JSON with these fields:
- primary_theme: string (main theme like "transformation", "anxiety", "growth")
- key_symbols: array of objects with symbol (string) and meaning (string)
- emotional_tone: string (e.g., "fearful", "hopeful", "confusing")
- possible_meanings: array of 3 potential interpretations
- guidance: string (actionable advice based on dream, 60-100 words)
- related_tarot_card: string (tarot card that resonates with this dream)

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    interpretation = extract_json(text)

    if not interpretation:
        interpretation = {
            "primary_theme": "Transformation",
            "key_symbols": [
                {"symbol": "Water", "meaning": "Emotions, unconscious mind"},
                {"symbol": "Flying", "meaning": "Freedom, escaping constraints"},
                {"symbol": "Being chased", "meaning": "Avoiding something in waking life"}
            ],
            "emotional_tone": "Mysterious",
            "possible_meanings": [
                "Your subconscious is processing recent changes",
                "You may be avoiding an important decision",
                "A part of you seeks liberation from routine"
            ],
            "guidance": "Pay attention to what feels unresolved in your waking life. Dreams often highlight areas needing attention. Consider journaling about the symbols that stood out most to you.",
            "related_tarot_card": "The Moon - intuition, dreams, subconscious"
        }

    return {"interpretation": interpretation, "dream": dream_description, "dreamer_details": dreamer_details}

def explore_symbols(symbol: str):
    """Explore a specific dream symbol"""
    prompt = f'''Provide a comprehensive interpretation of this dream symbol:

Symbol: {symbol}

Return ONLY valid JSON with these fields:
- symbol: "{symbol}"
- general_meaning: string (core universal interpretation)
- positive_interpretation: string (when symbol appears in positive context)
- negative_interpretation: string (when symbol appears in challenging context)
- common_associations: array of 5 strings (related concepts, emotions, life areas)
- questions_for_dreamer: array of 3 reflective questions to ask about this symbol

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    symbol_exploration = extract_json(text)

    if not symbol_exploration:
        symbol_exploration = {
            "symbol": symbol,
            "general_meaning": "Symbols in dreams are highly personal. They often represent aspects of the dreamer's own psyche, experiences, and emotions.",
            "positive_interpretation": f"When {symbol} appears positively, it may indicate growth, opportunity, or a positive aspect of your inner world emerging.",
            "negative_interpretation": f"When {symbol} appears in a threatening way, it might represent fears, obstacles, or aspects of yourself you're resisting.",
            "common_associations": ["Transformation", "Self-discovery", "Emotional processing", "Unconscious messages", "Personal growth"],
            "questions_for_dreamer": [
                f"What does {symbol} personally remind you of?",
                "How did you feel when you encountered this symbol?",
                "What's happening in your life around the time of this dream?"
            ]
        }

    return {"exploration": symbol_exploration, "symbol": symbol}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'interpret')

            if action == 'interpret':
                result = interpret_dream(
                    data.get('dream_description', ''),
                    data.get('dreamer_details', '')
                )
            elif action == 'explore_symbols':
                result = explore_symbols(
                    data.get('symbol', '')
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
