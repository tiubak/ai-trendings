"""Project handlers registry — auto-discovers day_*.py modules."""

import importlib
import os
import re

PROJECTS = {}

def _discover():
    """Auto-discover and register all day_YYYY_MM_DD.py modules."""
    pkg_dir = os.path.dirname(__file__)
    pattern = re.compile(r'^day_(\d{4})_(\d{2})_(\d{2})\.py$')
    
    for filename in sorted(os.listdir(pkg_dir)):
        m = pattern.match(filename)
        if not m:
            continue
        date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        mod_name = filename[:-3]  # strip .py
        try:
            mod = importlib.import_module(f".{mod_name}", package=__name__)
            handler = getattr(mod, 'handle', None)
            meta = getattr(mod, 'META', {})
            if handler:
                PROJECTS[date_str] = (handler, meta)
        except Exception as e:
            # Don't crash the whole app if one project is broken
            import logging
            logging.getLogger(__name__).warning(f"Failed to load {mod_name}: {e}")

_discover()

def get_handler(date_str: str):
    entry = PROJECTS.get(date_str)
    return entry[0] if entry else None

def get_meta(date_str: str):
    entry = PROJECTS.get(date_str)
    return entry[1] if entry else None
