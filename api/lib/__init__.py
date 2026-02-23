"""AI Trendings Library"""

from .base import (
    call_openrouter,
    call_pollinations,
    fetch_image,
    call_huggingface,
    extract_json,
    Handler
)
from .projects import get_handler, get_meta, PROJECTS

__all__ = [
    'call_openrouter',
    'call_pollinations', 
    'fetch_image',
    'call_huggingface',
    'extract_json',
    'Handler',
    'get_handler',
    'get_meta',
    'PROJECTS'
]
