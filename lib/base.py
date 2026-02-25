"""Common functions for AI Trendings projects."""

import os
import json
import sqlite3
import subprocess
from http.server import BaseHTTPRequestHandler
from urllib.parse import quote

# ---------------------------------------------------------------------------
# SQLite helpers — pre-loaded AI data (models, timeline, glossary, GPUs, etc.)
# ---------------------------------------------------------------------------
_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "ai_data.db")

def query_db(sql: str, params: tuple = ()) -> list[dict]:
    """Run a read-only query on the bundled AI database.
    Returns list of dicts. Safe for use in Vercel (read-only).
    
    Tables: models, timeline, glossary, languages, gpus, datasets
    
    Example:
        query_db("SELECT * FROM models WHERE open_source = 1 ORDER BY mmlu_score DESC LIMIT 5")
        query_db("SELECT * FROM timeline WHERE year >= ? ORDER BY year", (2020,))
        query_db("SELECT * FROM glossary WHERE category = ?", ("architecture",))
        query_db("SELECT * FROM gpus ORDER BY fp16_tflops DESC")
    """
    try:
        conn = sqlite3.connect(f"file:{_DB_PATH}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        return [{"error": str(e)}]

def load_json_data(filename: str) -> dict:
    """Load a JSON file from lib/data/. 
    Available: ai_models.json, ai_timeline.json, ai_glossary.json"""
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

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

def call_gTTS(text: str) -> str:
    """Call gTTS (Google Text-to-Speech) - free, no API key required.
    Returns base64-encoded audio."""
    try:
        from gtts import gTTS
        import base64
        import io
        
        # Generate TTS
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_bytes = audio_buffer.getvalue()
        
        # Encode as base64
        return base64.b64encode(audio_bytes).decode('utf-8')
    except ImportError as e:
        return f"ERROR: gtts library not installed - {str(e)}"
    except Exception as e:
        return f"ERROR: TTS generation failed - {str(e)}"


def call_huggingface(prompt: str, model: str) -> str:
    """Call HuggingFace Inference API for specialized tasks.
    Returns text as string, or base64-encoded binary for audio/image outputs."""
    if not HUGGINGFACE_API_KEY:
        return "HUGGINGFACE_API_KEY_NOT_SET"

    # NOTE: HuggingFace Inference Providers does NOT support Text-to-Speech
    # Use call_gTTS() instead for TTS
    # This function remains for other supported tasks (images, etc.)

    # Correct HuggingFace router format for serverless inference
    # https://router.huggingface.co/hf-inference/models/{model}
    url = f"https://router.huggingface.co/hf-inference/models/{model}"

    result = subprocess.run([
        "curl", "-s", "-X", "POST", url,
        "-H", f"Authorization: Bearer {HUGGINGFACE_API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"inputs": prompt})
    ], capture_output=True, timeout=60)

    if result.returncode != 0:
        return f"Error: {result.stderr.decode('utf-8', errors='ignore')}"

    # Try to decode as UTF-8 text (e.g., JSON or plain text responses)
    try:
        decoded = result.stdout.decode('utf-8')
        # Check for error responses
        if "error" in decoded.lower() and decoded.startswith('{"error"'):
            return f"API Error: {decoded}"
        return decoded
    except UnicodeDecodeError:
        # Binary data (audio, image) -> return base64 string
        import base64
        return base64.b64encode(result.stdout).decode('utf-8')

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

# ---------------------------------------------------------------------------
# Web & Data tools — free, no API keys needed
# ---------------------------------------------------------------------------

def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web via DuckDuckGo (free, no API key).
    Returns: [{title, url, body}, ...]
    
    Example:
        web_search("latest AI breakthroughs 2026")
        web_search("transformer architecture explained", max_results=3)
    """
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [{"title": r.get("title",""), "url": r.get("href",""), "body": r.get("body","")} for r in results]
    except Exception as e:
        return [{"error": str(e)}]

def fetch_url(url: str, max_chars: int = 5000) -> str:
    """Fetch a URL and return text content (HTML stripped).
    Good for grabbing article text, API responses, etc.
    
    Example:
        fetch_url("https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)")
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        resp = requests.get(url, timeout=8, headers={"User-Agent": "AI-Trendings/1.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:max_chars]
    except Exception as e:
        return f"Error: {e}"

def wikipedia_summary(topic: str) -> dict:
    """Get Wikipedia summary for a topic (free, no API key).
    Returns: {title, summary, url} or {error}.
    
    Example:
        wikipedia_summary("Attention mechanism")
        wikipedia_summary("GPT-4")
    """
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia("AI-Trendings/1.0", "en")
        page = wiki.page(topic)
        if page.exists():
            return {"title": page.title, "summary": page.summary[:3000], "url": page.fullurl}
        return {"error": f"No Wikipedia page found for '{topic}'"}
    except Exception as e:
        return {"error": str(e)}

def fetch_rss(url: str, max_items: int = 10) -> list[dict]:
    """Parse an RSS/Atom feed (free, no API key).
    Returns: [{title, link, published, summary}, ...]
    
    Example:
        fetch_rss("https://arxiv.org/rss/cs.AI")            # Latest AI papers
        fetch_rss("https://news.ycombinator.com/rss")       # Hacker News
        fetch_rss("https://www.reddit.com/r/MachineLearning/.rss")
    """
    try:
        import feedparser
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:max_items]:
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")[:500],
            })
        return items
    except Exception as e:
        return [{"error": str(e)}]

def generate_qr(data: str) -> str:
    """Generate QR code as base64 PNG.
    Returns base64 string for <img src="data:image/png;base64,{result}">
    
    Example:
        generate_qr("https://ai-trendings.vercel.app")
    """
    try:
        import qrcode
        import io
        import base64
        img = qrcode.make(data)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        return None

def generate_wordcloud(text: str, width: int = 800, height: int = 400) -> str:
    """Generate word cloud as base64 PNG from text.
    Returns base64 string for <img src="data:image/png;base64,{result}">
    
    Example:
        generate_wordcloud("machine learning deep neural network transformer attention ...")
    """
    try:
        from wordcloud import WordCloud
        import io
        import base64
        wc = WordCloud(width=width, height=height, background_color="#1a1a2e",
                       colormap="cool", max_words=100).generate(text)
        buf = io.BytesIO()
        wc.to_image().save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        return None

def tmp_sqlite(name: str = "project") -> tuple:
    """Create an ephemeral SQLite database in /tmp for runtime data processing.
    Returns (connection, cursor). Data lives only during this function invocation.
    
    Example:
        conn, c = tmp_sqlite("quiz")
        c.execute("CREATE TABLE scores (name TEXT, score INT)")
        c.execute("INSERT INTO scores VALUES (?, ?)", ("Alice", 95))
        results = c.execute("SELECT * FROM scores").fetchall()
        conn.close()
    """
    import tempfile
    db_path = os.path.join(tempfile.gettempdir(), f"ai_trendings_{name}.db")
    conn = sqlite3.connect(db_path)
    return conn, conn.cursor()

def classify_text(text: str) -> dict:
    """Classify text sentiment/topic using HuggingFace (free tier).
    Returns classification labels and scores.
    """
    if not HUGGINGFACE_API_KEY:
        return {"error": "HUGGINGFACE_API_KEY not set"}
    result = call_huggingface(text, "distilbert-base-uncased-finetuned-sst-2-english")
    try:
        return json.loads(result) if isinstance(result, str) else result
    except:
        return {"raw": result}

def embed_text(text: str) -> list:
    """Get text embeddings from HuggingFace (free tier).
    Returns vector (list of floats) for similarity calculations.
    """
    if not HUGGINGFACE_API_KEY:
        return []
    result = call_huggingface(text, "sentence-transformers/all-MiniLM-L6-v2")
    try:
        return json.loads(result) if isinstance(result, str) else result
    except:
        return []

def text_to_speech(text: str, lang: str = "en") -> str:
    """Convert text to speech (gTTS — free, no API key).
    Returns base64 audio. Use: <audio src="data:audio/mp3;base64,{result}" controls>
    """
    return call_gTTS(text)


# ---------------------------------------------------------------------------
# Client-side library CDN links — for HTML templates
# ---------------------------------------------------------------------------
CDN_LIBS = {
    "chart.js": "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js",
    "d3": "https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js",
    "three.js": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js",
    "marked": "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
    "highlight.js": "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js",
    "highlight.css": "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css",
    "katex.js": "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js",
    "katex.css": "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css",
    "mermaid": "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js",
    "confetti": "https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.0/dist/confetti.browser.min.js",
    "anime.js": "https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js",
    "tone.js": "https://cdn.jsdelivr.net/npm/tone@14/build/Tone.js",
    "prism.js": "https://cdn.jsdelivr.net/npm/prismjs@1/prism.min.js",
    "prism.css": "https://cdn.jsdelivr.net/npm/prismjs@1/themes/prism-tomorrow.min.css",
}

# ---------------------------------------------------------------------------
# Public APIs — free, no keys needed
# ---------------------------------------------------------------------------
PUBLIC_APIS = {
    "arxiv": "http://export.arxiv.org/api/query?search_query={query}&max_results=5",
    "open_trivia": "https://opentdb.com/api.php?amount={amount}&category={category}&type=multiple",
    "github_trending": "https://api.github.com/search/repositories?q={query}&sort=stars&order=desc",
    "random_quote": "https://api.quotable.io/random",
    "dad_joke": "https://icanhazdadjoke.com/",
    "news_hn": "https://hacker-news.firebaseio.com/v0/topstories.json",
    "country_info": "https://restcountries.com/v3.1/name/{name}",
    "weather": "https://wttr.in/{city}?format=j1",
}


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
