"""Project handlers registry."""

# Import project handlers here
from .feb_01 import handle as feb_01, META as META_01
# from .feb_02 import handle as feb_02, META as META_02
# ...

# Map day -> (handler, metadata)
PROJECTS = {
    1: (feb_01, META_01),
    # 2: (feb_02, META_02),
    # ...
}

def get_handler(day: int):
    """Get project handler for a given day."""
    if day in PROJECTS:
        return PROJECTS[day][0]
    return None

def get_meta(day: int):
    """Get project metadata for a given day."""
    if day in PROJECTS:
        return PROJECTS[day][1]
    return None

def register(day: int, handler, meta: dict):
    """Register a new project."""
    PROJECTS[day] = (handler, meta)
