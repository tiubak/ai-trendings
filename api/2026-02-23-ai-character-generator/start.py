import os, json, logging
from http.server import BaseHTTPRequestHandler
import subprocess


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key from environment
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

def generate_character_persona(name, role, setting, theme, traits):
    """
    Generate a complete character persona using Pollinations.AI
    Returns structured character data with all fields
    """
    # Build the prompt
    prompt = f"""Create a detailed character profile for a {role} named {name}.

Setting: {setting}
Theme: {theme}
Desired traits: {traits}

Generate the following in JSON format:
{{
  "name": "{name}",
  "role": "{role}",
  "backstory": "3-4 sentences about their origin and past",
  "personality": "2-3 sentences describing their temperament and behavior",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "motivation": "What drives this character (1-2 sentences)",
  "relationships": {{
    "ally": "Description of an important ally",
    "rival": "Description of an important rival"
  }},
  "signature_quote": "A memorable line this character would say"
}}

Make it compelling and consistent with the {role} archetype."""

    try:
        # Call Pollinations.AI API using curl subprocess
        from urllib.parse import quote
        url = f"https://text.pollinations.ai/{quote(prompt)}"
        
        headers = []
        if POLLINATIONS_API_KEY:
            headers.extend(["-H", f"Authorization: Bearer {POLLINATIONS_API_KEY}"])
        
        result = subprocess.run(
            ["curl", "-s"] + headers + [url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            content = result.stdout.strip()
        else:
            raise Exception(f"curl failed: {result.stderr}")

        # Try to parse as JSON, fallback to structured extraction if needed
        try:
            persona = json.loads(content)
            return persona
        except json.JSONDecodeError:
            # Fallback: extract JSON from response
            import re
            json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
            if json_match:
                persona = json.loads(json_match.group(0))
                return persona
            else:
                # Final fallback: use the text as backstory
                return generate_fallback_persona(name, role, setting, content)

    except Exception as e:
        logger.error(f"Pollinations.AI request failed: {e}")
        return generate_fallback_persona(name, role, setting, theme)



def generate_fallback_persona(name, role, setting, context=""):
    """
    Generate a fallback persona if API fails
    Uses the context or generates a generic but coherent persona
    """
    # Role-specific personas
    role_personas = {
        "hero": {
            "backstory": f"{name} emerged from humble beginnings in {setting}, destined to protect the innocent and fight for justice against overwhelming odds.",
            "personality": "Brave, selfless, and driven by an unshakeable moral compass. Often struggles with the weight of responsibility.",
            "strengths": ["Unwavering courage", "Natural leadership", "Magnetic charisma"],
            "weaknesses": ["Self-sacrificing to a fault", "Trusts too easily", "Haunted by past failures"],
            "motivation": "To protect those who cannot protect themselves and restore balance to the world.",
            "relationships": {
                "ally": "A wise mentor who guides them through difficult choices.",
                "rival": "A dark reflection of themselves who tests their convictions."
            },
            "signature_quote": f"{'Hope' if 'light' in context.lower() else 'Justice'} is not given. It is forged in the fires of sacrifice."
        },
        "villain": {
            "backstory": f"{name} was once idealistic, but betrayal and loss in {setting} twisted their noble ambitions into something dark and vengeful.",
            "personality": "Charismatic, calculating, and utterly convinced of their own righteousness. Sees themselves as the hero of their story.",
            "strengths": ["Brilliant strategist", "Master manipulator", "Unmatched willpower"],
            "weaknesses": ["Obsessive", "Unable to trust", "Blind to their own cruelty"],
            "motivation": "To reshape the world according to their vision, no matter the cost.",
            "relationships": {
                "ally": "A loyal lieutenant who shares their vision.",
                "rival": "The hero who represents everything they despise."
            },
            "signature_quote": f"{'Chaos' if 'chaos' in context.lower() else 'Power'} is not an obstacle. It is a tool."
        },
        "mentor": {
            "backstory": f"{name} has walked the path of wisdom through decades of experience in {setting}, bearing scars and secrets that shaped their philosophy.",
            "personality": "Patient, enigmatic, and speaks in riddles. Values growth over comfort and lessons over victories.",
            "strengths": ["Deep wisdom", "Magical or spiritual mastery", "Unwavering patience"],
            "weaknesses": ["Cryptic communication", "Reluctant to intervene", "Haunted by past students"],
            "motivation": "To guide the next generation and pass on hard-earned wisdom before time runs out.",
            "relationships": {
                "ally": "A former student who now leads their own path.",
                "rival": "A peer who chose a different, darker philosophy."
            },
            "signature_quote": f"{'The sharpest blade is forged in the hottest flame. So too, are souls.' if 'wisdom' in context.lower() else 'Truth waits for those willing to seek it.'}"
        },
        "rogue": {
            "backstory": f"{name} learned to survive in the shadows of {setting}, where laws are suggestions and survival is the only currency that matters.",
            "personality": "Witty, cynical, and fiercely independent. Loyal to a fault to those who earn their trust, deadly to those who betray it.",
            "strengths": ["Master of stealth", "Silver-tongued manipulator", "Improvisational genius"],
            "weaknesses": ["Trust issues", "Reckless when cornered", "Troubled past haunts them"],
            "motivation": "Freedom from control and enough wealth to disappear forever.",
            "relationships": {
                "ally": "A fence who knows all the right people.",
                "rival": "A law enforcer who's always one step behind."
            },
            "signature_quote": f"{'Honor is a luxury I can\'t afford.' if 'survival' in context.lower() else 'Everyone has a price. Mine just happens to be higher.'}"
        }
    }

    # Get role-specific persona or default
    role_key = role.lower() if role.lower() in role_personas else "hero"
    base_persona = role_personas.get(role_key, role_personas["hero"])

    # Build complete persona
    persona = {
        "name": name,
        "role": role,
        "backstory": base_persona["backstory"],
        "personality": base_persona["personality"],
        "strengths": base_persona["strengths"],
        "weaknesses": base_persona["weaknesses"],
        "motivation": base_persona["motivation"],
        "relationships": base_persona["relationships"],
        "signature_quote": base_persona["signature_quote"],
        "setting": setting,
        "theme": theme,
        "generated_with": "fallback"
    }

    return persona


class Handler(BaseHTTPRequestHandler):
    """HTTP handler for character generation endpoint"""

    def send_json_response(self, status_code, data):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_json_response(200, {})

    def do_POST(self):
        """Handle character generation requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')

            # Parse JSON
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_json_response(400, {
                    "error": "Invalid JSON",
                    "message": "Request body must be valid JSON"
                })
                return

            # Validate required fields
            name = data.get('name', '').strip()
            role = data.get('role', 'hero').strip()
            setting = data.get('setting', 'Fantasy World').strip()
            theme = data.get('theme', 'Epic Adventure').strip()
            traits = data.get('traits', 'balanced').strip()

            if not name:
                self.send_json_response(400, {
                    "error": "Missing required field",
                    "message": "'name' is required"
                })
                return

            # Generate persona
            logger.info(f"Generating persona for {name} ({role})")
            persona = generate_character_persona(name, role, setting, theme, traits)

            # Return successful response
            self.send_json_response(200, {
                "success": True,
                "persona": persona
            })

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            self.send_json_response(500, {
                "error": "Internal server error",
                "message": str(e)
            })

# Vercel uses the Handler class directly - no separate handler() function needed!
