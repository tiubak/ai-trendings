#!/usr/bin/env python3
"""
AI Trendings - Single API Router

Routes requests by date parameter to project handlers.
Vercel Hobby plan limits to 12 functions, so we use ONE.
"""

import json
import logging
from http.server import BaseHTTPRequestHandler
from lib.projects import get_handler, get_meta
from lib.base import call_openrouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    """Main router for all AI Trendings projects."""
    
    def do_POST(self):
        try:
            # Parse request
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error("Empty request")
                return
            
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Get date and action
            date_str = data.get('date', '')
            action = data.get('action', 'start')
            
            if not date_str:
                self._send_error("Missing 'date' parameter")
                return
            
            # Parse day from date (2026-02-01 -> 1)
            try:
                day = int(date_str.split('-')[2])
            except:
                self._send_error(f"Invalid date format: {date_str}")
                return
            
            # Get project handler
            handler = get_handler(day)
            
            if handler:
                # Call project-specific handler
                result = handler(action, data)
            else:
                # Fallback: generate response with OpenRouter
                result = self._fallback_handler(action, data, day)
            
            # Send response
            self._send_json(result)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            self._send_error(str(e), 500)
    
    def _fallback_handler(self, action: str, data: dict, day: int):
        """Fallback handler for unregistered projects."""
        topic = data.get('topic', 'artificial intelligence')
        prompt = f"Explain {topic} in simple terms for a general audience."
        result = call_openrouter(prompt)
        return {
            "explanation": result,
            "topic": topic,
            "day": day,
            "note": "Project not yet implemented"
        }
    
    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, message: str, status: int = 400):
        """Send error response."""
        self._send_json({"error": message}, status)
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Log requests."""
        logger.info("%s", format % args)
