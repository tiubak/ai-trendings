"""Common functions for AI Trendings projects."""

import os
import json
import subprocess
from http.server import BaseHTTPRequestHandler
from urllib.parse import quote

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

def call_openrouter(prompt: str) -> str:
    """Call OpenRouter for text generation."""
    if not OPENROUTER_API_KEY:
        return call_pollinations(prompt)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    data = {"model": "openrouter/free", "messages": [{"role": "user", "content": prompt}]}
    
    result = subprocess.run([
        "curl", "-s", "-X", "POST", url,
        "-H", f"Authorization: Bearer {OPENROUTER_API_KEY}",
        "-H", "Content-Type: application/json",
        "-H", "HTTP-Referer: https://ai-trendings.vercel.app",
        "-d", json.dumps(data)
    ], capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        try:
            return json.loads(result.stdout).get("choices", [{}])[0].get("message", {}).get("content", "")
        except:
            return call_pollinations(prompt)
    return call_pollinations(prompt)

def call_pollinations(prompt: str) -> str:
    """Fallback text generation via Pollinations.AI.
    
    Official API: gen.pollinations.ai/v1/chat/completions
    """
    url = "https://gen.pollinations.ai/v1/chat/completions"
    data = {"model": "openai", "messages": [{"role": "user", "content": prompt}]}
    
    cmd = [
        "curl", "-s", "-X", "POST", url,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(data)
    ]
    
    if POLLINATIONS_API_KEY:
        cmd.insert(3, "-H")
        cmd.insert(4, f"Authorization: Bearer {POLLINATIONS_API_KEY}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        try:
            return json.loads(result.stdout).get("choices", [{}])[0].get("message", {}).get("content", "")
        except:
            pass
    
    return "Response unavailable"

def fetch_image(prompt: str, width: int = 512, height: int = 512) -> str:
    """Fetch image as base64 from Pollinations.AI.
    
    Official API: gen.pollinations.ai/image/{prompt}?model=flux
    Returns base64 for frontend: <img src="data:image/png;base64,{result}">
    """
    url = f"https://gen.pollinations.ai/image/{quote(prompt)}?model=flux&width={width}&height={height}"
    
    cmd = ["curl", "-s", url]
    if POLLINATIONS_API_KEY:
        cmd.extend(["-H", f"Authorization: Bearer {POLLINATIONS_API_KEY}"])
    
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode == 0 and result.stdout:
            # Check if it's PNG or JPEG
            if result.stdout[:4] == b'\x89PNG' or result.stdout[:2] == b'\xff\xd8':
                import base64
                return base64.b64encode(result.stdout).decode('utf-8')
    except:
        pass
    
    return None

def call_huggingface(prompt: str, model: str) -> str:
    """Call HuggingFace Inference API for specialized tasks."""
    if not HUGGINGFACE_API_KEY:
        return "HuggingFace API key not available"
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    
    result = subprocess.run([
        "curl", "-s", "-X", "POST", url,
        "-H", f"Authorization: Bearer {HUGGINGFACE_API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"inputs": prompt})
    ], capture_output=True, text=True, timeout=60)
    
    return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"

def extract_json(text: str) -> dict:
    """Extract JSON from text with error handling."""
    try:
        return json.loads(text)
    except:
        start = text.find('{')
        if start == -1:
            return None
        depth = 0
        for i, c in enumerate(text[start:], start):
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i+1])
                    except:
                        continue
        return None

class Handler(BaseHTTPRequestHandler):
    """Base handler with common methods."""
    
    def parse_request(self):
        """Parse JSON request body."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            return json.loads(body)
        except:
            return {}
    
    def send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
