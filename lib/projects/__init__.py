"""Project handlers registry."""

# Import project handlers here
from . import day_2026_02_01
from . import day_2026_02_02
from . import day_2026_02_03
from . import day_2026_02_04
from . import day_2026_02_05
from . import day_2026_02_06
from . import day_2026_02_07
from . import day_2026_02_08
from . import day_2026_02_24

PROJECTS = {
    "2026-02-01": (day_2026_02_01.handle, day_2026_02_01.META),
    "2026-02-02": (day_2026_02_02.handle, day_2026_02_02.META),
    "2026-02-03": (day_2026_02_03.handle, day_2026_02_03.META),
    "2026-02-04": (day_2026_02_04.handle, day_2026_02_04.META),
    "2026-02-05": (day_2026_02_05.handle, day_2026_02_05.META),
    "2026-02-06": (day_2026_02_06.handle, day_2026_02_06.META),
    "2026-02-07": (day_2026_02_07.handle, day_2026_02_07.META),
    "2026-02-08": (day_2026_02_08.handle, day_2026_02_08.META),
    "2026-02-24": (day_2026_02_24.handle, day_2026_02_24.META),
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
