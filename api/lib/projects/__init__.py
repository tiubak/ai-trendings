"""Project handlers registry."""

# Import project handlers here
from . import day_2026_02_01

PROJECTS = {
    "2026-02-01": (day_2026_02_01.handle, day_2026_02_01.META),
}

def get_handler(date_str: str):
    if date_str in PROJECTS and PROJECTS[date_str]:
        return PROJECTS[date_str][0]
    return None

def get_meta(date_str: str):
    if date_str in PROJECTS and PROJECTS[date_str]:
        return PROJECTS[date_str][1]
    return None

def register(date_str: str, handler, meta: dict):
    PROJECTS[date_str] = (handler, meta)
