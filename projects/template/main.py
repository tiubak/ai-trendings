#!/usr/bin/env python3
"""
{PROJECT_NAME}
{ONE-LINE DESCRIPTION}

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables (set on Vercel)
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

app = FastAPI(
    title="{PROJECT_NAME}",
    description="{ONE-LINE DESCRIPTION}",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend"""
    with open("index.html", "r") as f:
        return f.read()


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "{PROJECT_NAME}",
        "env_vars": {
            "pollinations": bool(POLLINATIONS_API_KEY),
            "huggingface": bool(HUGGINGFACE_API_KEY),
            "openrouter": bool(OPENROUTER_API_KEY)
        }
    }


# Example: Using environment variables in your code
# import requests
#
# @app.post("/api/generate")
# async def generate_endpoint(request: Request):
#     data = await request.json()
#     
#     # Option 1: Pollinations.AI (no key needed, but supports key)
#     if POLLINATIONS_API_KEY:
#         # Use with key if available
#         pass
#     
#     # Option 2: Hugging Face (requires API key)
#     if not HUGGINGFACE_API_KEY:
#         raise HTTPException(status_code=500, detail="HUGGINGFACE_API_KEY not configured")
#     
#     headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
#     # Make API call with headers
#     
#     # Option 3: OpenRouter (requires API key)
#     if not OPENROUTER_API_KEY:
#         raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not configured")
#     
#     headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
#     # Make API call with headers
#
#     return {"result": "success"}


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Log env var status on startup
    logger.info(f"Starting {PROJECT_NAME}...")
    logger.info(f"Env vars configured:")
    logger.info(f"  - POLLINATIONS_API_KEY: {bool(POLLINATIONS_API_KEY)}")
    logger.info(f"  - HUGGINGFACE_API_KEY: {bool(HUGGINGFACE_API_KEY)}")
    logger.info(f"  - OPENROUTER_API_KEY: {bool(OPENROUTER_API_KEY)}")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
