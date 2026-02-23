#!/usr/bin/env python3
"""
AI Story Starter - Combined API
Actions: opening, prompt_writing, character_intro
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

def story_opening(genre: str = "fantasy", mood: str = "mysterious", protagonist_type: str = "any", hook_type: str = "action"):
    """Generate a story opening"""
    prompt = f'''Write a compelling first paragraph (opening) for a {genre} story.

Mood: {mood}
Protagonist type: {protagonist_type}
Preferred hook: {hook_type} (action, mystery, dialogue, question, statement)

Return ONLY valid JSON with these fields:
- opening: string (the story opening paragraph, 80-150 words)
- genre: "{genre}"
- hook_used: "{hook_type}"
- protagonist_hint: string (what we learn about protagonist)
- setting_established: string (time/place context)
- conflict_seeds: array of 2 strings (elements that might become conflict)
- continue_prompt: string (question to help writer continue)

Make it gripping, atmospheric, and full of potential.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    opening = extract_json(text)

    if not opening or 'opening' not in opening:
        opening = {
            "opening": "The storm came without warning, tearing through the village like an angry god. Elara clutched her cloak against the wind, her eyes fixed on the dark tower looming through the rain. Tonight, she would either save her brother or lose herself to the ancient magic that had cursed their bloodline.",
            "genre": genre,
            "hook_used": hook_type,
            "protagonist_hint": "Heroine named Elara with family troubles and a quest",
            "setting_established": "Fantasy village during supernatural storm, dark tower present",
            "conflict_seeds": ["Family curse/magic", "Rescue mission", "Ancient power vs mortal"],
            "continue_prompt": "What does Elara find when she enters the tower? Who or what is she really up against?"
        }

    return {"opening": opening, "genre": genre, "mood": mood}

def prompt_writing(theme: str = "", genre_mashup: str = "", writing_prompt: str = ""):
    """Generate a writing prompt or exercise"""
    if writing_prompt:
        prompt = f'''Analyze and improve this writing prompt, then generate a story starter from it:

Writing prompt: "{writing_prompt}"

Return ONLY valid JSON with these fields:
- refined_prompt: string (improved version of input)
- story_starters: array of 3 different opening paragraphs based on this prompt
- genre_blend: string (if multiple genres are suggested)
- key_elements: array of 3 strings (key themes/symbols to include)
- word_limit: string (suggested length for writer)
- exercise_type: string ("character focus", "plot focus", "worldbuilding", etc.)

No markdown, just JSON.'''
    elif theme and genre_mashup:
        prompt = f'''Generate a writing prompt blending {genre_mashup} around the theme: {theme}

Return ONLY valid JSON with these fields:
- prompt: string (the writing prompt)
- genre_mashup: "{genre_mashup}"
- theme: "{theme}"
- expected_tone: string (tone writers should aim for)
- constraints: array of 2 strings (interesting constraints to challenge writer)
- inspiration_sources: array of 2 strings (books/movies with similar vibe)

No markdown, just JSON.'''
    else:
        prompt = f'''Generate an interesting writing prompt about {theme if theme else "anything"}.

Return ONLY valid JSON with these fields:
- prompt: string (the writing prompt)
- category: string (plot, character, worldbuilding, etc.)
- difficulty: string ("beginner", "intermediate", "advanced")
- time_estimate: string (how long this might take to write)
- expected_genre: string (what genre this would produce)
- similar_prompts: array of 2 related prompt ideas

Make it inspiring and specific.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    prompt_data = extract_json(text)

    if not prompt_data:
        prompt_data = {
            "refined_prompt": writing_prompt if writing_prompt else f"Write a {genre_mashup or 'story'} about {theme or 'anything'}.",
            "story_starters": ["The rain hadn't stopped in three days..."],
            "genre_blend": genre_mashup or "unknown",
            "key_elements": ["Conflict", "Character growth"],
            "word_limit": "500-1000 words",
            "exercise_type": "general"
        }

    return {"prompt_data": prompt_data, "theme": theme, "genre_mashup": genre_mashup, "original_prompt": writing_prompt}

def character_intro(character_type: str = "", archetype: str = "", situation: str = ""):
    """Generate a character introduction"""
    prompt = f'''Write a character introduction paragraph for a {character_type if character_type else 'character'}.

Archetype: {archetype if archetype else 'any'}
Situation: {situation if situation else 'ordinary day'}

Return ONLY valid JSON with these fields:
- introduction: string (paragraph introducing the character)
- character_name: string (invent a name if needed)
- traits_revealed: array of 3 strings (personality/background elements shown)
- situation_context: string (where/when we meet them)
- narrator_pov: string (first person, third limited, etc.)
- hook_question: string (what makes reader curious about this character)
- casting_suggestion: string (which actor/celebrity fits this role)

Show, don't tell. Use action, dialogue, or observation.

No markdown, just JSON.'''

    text = call_pollinations(prompt)
    char_intro = extract_json(text)

    if not char_intro or 'introduction' not in char_intro:
        char_intro = {
            "introduction": "Marcus checked his watch for the seventh time in as many minutes, the anxiety visible in the way his fingers drummed against the cafe table. He'd chosen the corner seat, back to the wall, eyes scanning every newcomer. This wasn't his first clandestine meeting, and it wouldn't be his last.",
            "character_name": "Marcus",
            "traits_revealed": ["Anxious/nervous", "Experienced in secret meetings", "Observant/vigilant"],
            "situation_context": "Waiting for someone in a cafe, clearly a meetup with purpose",
            "narrator_pov": "third limited",
            "hook_question": "What secret is Marcus meeting about? Why is he so experienced at this?",
            "casting_suggestion": "Similar vibe to Michael Fassbender in thriller roles"
        }

    return {"character_intro": char_intro, "character_type": character_type, "archetype": archetype}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}

            action = data.get('action', 'opening')

            if action == 'opening':
                result = story_opening(
                    data.get('genre', 'fantasy'),
                    data.get('mood', 'mysterious'),
                    data.get('protagonist_type', 'any'),
                    data.get('hook_type', 'action')
                )
            elif action == 'prompt_writing':
                result = prompt_writing(
                    data.get('theme', ''),
                    data.get('genre_mashup', ''),
                    data.get('writing_prompt', '')
                )
            elif action == 'character_intro':
                result = character_intro(
                    data.get('character_type', ''),
                    data.get('archetype', ''),
                    data.get('situation', '')
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
