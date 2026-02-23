#!/usr/bin/env python3
"""
AI Riddle Generator - Combined API
Actions: generate, solve, create_custom
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

def generate_riddle(difficulty: str = "medium", category: str = "nature"):
    """Generate a riddle with answer"""
    difficulty_desc = {"easy": "simple and suitable for children", "medium": "moderately challenging", "hard": "very tricky and clever"}[difficulty]

    prompt = f'''Write a {difficulty_desc} riddle about {category}.

The riddle should be clever, engaging, and have a clear answer.

Return ONLY valid JSON with these fields:
- riddle: string (the riddle question)
- answer: string (the answer)
- hints: array of 2 progressive hints (getting easier)
- difficulty: "{difficulty}"
- category: "{category}"
- explanation: string (optional, explains the answer)

No markdown, no numbering, no extra text.'''

    text = call_pollinations(prompt)
    riddle_data = extract_json(text)

    if not riddle_data or 'riddle' not in riddle_data:
        default_riddles = {
            "nature": {
                "riddle": "I have roots as nobody sees,\nI am taller than trees,\nUp, up I go,\nAnd yet never grow.",
                "answer": "mountain",
                "hints": ["I am a natural landform", "I am very large and immovable"],
                "difficulty": "medium",
                "category": "nature"
            },
            "animals": {
                "riddle": "What has keys but can't open locks?",
                "answer": "piano",
                "hints": ["It's a musical instrument", "It has many black and white parts"],
                "difficulty": "easy",
                "category": "animals"
            }
        }
        riddle_data = default_riddles.get(category, default_riddles["nature"])

    return {"riddle": riddle_data, "difficulty": difficulty, "category": category}

def solve_riddle(user_answer: str, riddle_text: str, correct_answer: str):
    """Check if user's answer is correct"""
    prompt = f'''Check if this answer is correct for the riddle.

Riddle: {riddle_text}
User's answer: {user_answer}
Correct answer: {correct_answer}

Evaluate if the user's answer is semantically equivalent to the correct answer (allow for variations in phrasing).

Return ONLY valid JSON with these fields:
- is_correct: boolean (true if answer matches)
- feedback: string (encouraging feedback)
- if_wrong: string (the correct answer if they're wrong, empty if correct)
- alternative_phrasings: array of 2-3 other acceptable answers

No markdown, no explanation.'''

    text = call_pollinations(prompt)
    result = extract_json(text)

    if not result or 'is_correct' not in result:
        simple_match = user_answer.lower().strip() == correct_answer.lower().strip()
        result = {
            "is_correct": simple_match,
            "feedback": "The answer is correct!" if simple_match else f"Not quite! The answer is: {correct_answer}",
            "if_wrong": "" if simple_match else correct_answer,
            "alternative_phrasings": []
        }

    return {"evaluation": result, "user_answer": user_answer}

def create_custom_riddle(topic: str, creativity_level: str = "medium"):
    """Create a riddle on a custom topic"""
    creativity_desc = {"low": "straightforward and obvious", "medium": "creative with wordplay", "high": "highly creative and poetic"}[creativity_level]

    prompt = f'''Write a {creativity_desc} riddle about this topic: {topic}

The riddle should be clear, engaging, and appropriate for the topic.

Return ONLY valid JSON with these fields:
- riddle: string (the riddle)
- answer: string (the answer)
- difficulty_estimate: string ("easy", "medium", or "hard")
- topic_subcategory: string (what specific aspect of the topic)
- hint: string (one helpful hint)

No markdown, no extra text.'''

    text = call_pollinations(prompt)
    custom = extract_json(text)

    if not custom or 'riddle' not in custom:
        custom = {
            "riddle": f"What am I? (Topic: {topic})",
            "answer": topic,
            "difficulty_estimate": "medium",
            "topic_subcategory": "general",
            "hint": f"Think about what {topic} is or does."
        }

    return {"riddle": custom, "topic": topic, "creativity": creativity_level}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'generate')

            if action == 'generate':
                result = generate_riddle(
                    data.get('difficulty', 'medium'),
                    data.get('category', 'nature')
                )
            elif action == 'solve':
                result = solve_riddle(
                    data.get('user_answer', ''),
                    data.get('riddle', ''),
                    data.get('correct_answer', '')
                )
            elif action == 'create_custom':
                result = create_custom_riddle(
                    data.get('topic', ''),
                    data.get('creativity_level', 'medium')
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
