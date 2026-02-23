"""Project handlers registry."""

# Import project handlers here
from . import _2026_02_01  # New naming: YYYY_MM_DD (underscore prefix for valid Python identifier)
from . import _2026_02_02  # AI Attention Mechanism Explorer
from . import _2026_02_03  # AI Ethics Simulator - Feb 3, 2026
from . import _2026_02_04  # AI Safety & Alignment Explorer - Feb 4, 2026
from . import _2026_02_05  # AI Ethics Dilemma Simulator
from . import _2026_02_06  # AI Ethics Dilemma Simulator
from . import _2026_02_07  # AI Token Cost Calculator & Optimizer - Feb 7, 2026
# from . import 2026_02_03
# ...

# Map date string -> (handler, metadata)
# Key: "YYYY-MM-DD" (e.g., "2026-02-01")
# Value: (handler_function, META_dict)
PROJECTS = {
    "2026-02-01": (lambda a, d: _2026_02_01.handle(a, d), _2026_02_01.META),
    "2026-02-02": (lambda a, d: _2026_02_02.handle(a, d), _2026_02_02.META),
    "2026-02-03": (lambda a, d: _2026_02_03.handle(a, d), _2026_02_03.META),
    "2026-02-04": (lambda a, d: _2026_02_04.handle(a, d), _2026_02_04.META),
    "2026-02-05": (lambda a, d: _2026_02_05.handle(a, d), _2026_02_05.META),
    "2026-02-06": (lambda a, d: _2026_02_06.handle(a, d), _2026_02_06.META),
    "2026-02-07": (lambda a, d: _2026_02_07.handle(a, d), _2026_02_07.META),
}

def get_handler(date_str: str):
    """Get project handler for a given date string (YYYY-MM-DD)."""
    if date_str in PROJECTS and PROJECTS[date_str]:
        return PROJECTS[date_str][0]
    return None

def get_meta(date_str: str):
    """Get project metadata for a given date string (YYYY-MM-DD)."""
    if date_str in PROJECTS and PROJECTS[date_str]:
        return PROJECTS[date_str][1]
    return None

def register(date_str: str, handler, meta: dict):
    """Register a new project.
    
    Args:
        date_str: Date string "YYYY-MM-DD"
        handler: Function that handles (action, data) -> dict
        meta: Metadata dict with name, description, category
    """
    PROJECTS[date_str] = (handler, meta)
