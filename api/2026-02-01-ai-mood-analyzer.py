#!/usr/bin/env python3
"""
AI Mood Analyzer - Combined API
Actions: analyze, boost
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

def analyze_mood(feeling: str, context: str = ""):
    """Analyze mood and provide insights"""
    prompt = f'''Analyze this emotional state and provide a supportive response:

Primary feeling: {feeling}
Additional context: {context if context else "None provided"}

Return ONLY valid JSON with these fields:
- mood_label: string (one or two word label)
- intensity: integer 1-10
- possible_causes: array of 3 strings
- coping_suggestions: array of 3 strings
- uplifting_message: string (50-80 words, supportive and empathetic)
- related_quote: string (short inspirational quote)

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    analysis = extract_json(text)
    
    if not analysis:
        analysis = {
            "mood_label": "Complex",
            "intensity": 5,
            "possible_causes": ["Many factors influence emotions", "Life transitions", "Hormonal changes"],
            "coping_suggestions": ["Practice mindfulness", "Reach out to a friend", "Get some fresh air"],
            "uplifting_message": "Your feelings are valid. Remember that emotions are temporary visitors, not permanent residents. Be gentle with yourself today.",
            "related_quote": "Vulnerability is not weakness. It's the birthplace of connection and belonging. - Brené Brown"
        }
    
    return {"analysis": analysis, "feeling": feeling, "context": context}

def boost_mood(analysis: dict, preferred_activity: str = ""):
    """Generate personalized mood boost plan"""
    prompt = f'''Based on this mood analysis, create a personalized 3-step plan to lift their spirits:

{json.dumps(analysis, indent=2)}

Preferred activity if any: {preferred_activity if preferred_activity else "None specified"}

Return ONLY valid JSON with these fields:
- mood_goal: string (what emotional state to aim for)
- step_1_immediate: object with action (string) and reason (string)
- step_2_short_term: object with action (string) and reason (string)
- step_3_long_term: object with action (string) and reason (string)
- quick_win: string (something they can do in <5 minutes)
- encouragement: string (30-50 words of motivation)

No markdown, no explanation, just the JSON object.'''

    text = call_pollinations(prompt)
    boost_plan = extract_json(text)
    
    if not boost_plan:
        boost_plan = {
            "mood_goal": "Improved emotional well-being",
            "step_1_immediate": {"action": "Take 5 deep breaths", "reason": "Activates parasympathetic nervous system"},
            "step_2_short_term": {"action": "Go for a 10-minute walk", "reason": "Movement releases endorphins"},
            "step_3_long_term": {"action": "Practice daily gratitude journaling", "reason": "Retrains brain to focus on positives"},
            "quick_win": "Watch a funny video or look at cute animal pictures",
            "encouragement": "Small steps lead to big changes. You have the strength to shift your mood, one moment at a time."
        }
    
    return {"boost_plan": boost_plan, "original_analysis": analysis}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            action = data.get('action', 'analyze')
            
            if action == 'analyze':
                result = analyze_mood(
                    data.get('feeling', ''),
                    data.get('context', '')
                )
            elif action == 'boost':
                result = boost_mood(
                    data.get('analysis', {}),
                    data.get('preferred_activity', '')
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
