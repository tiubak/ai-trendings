"""Project handlers registry."""

# Import project handlers here
from . import day_2026_02_01
from . import day_2026_02_02
from . import day_2026_02_03
from . import day_2026_02_04
from . import day_2026_02_08
from . import day_2026_02_09
from . import day_2026_02_11
from . import day_2026_02_12

PROJECTS = {
    "2026-02-01": (day_2026_02_01.handle, day_2026_02_01.META),
    "2026-02-02": (day_2026_02_02.handle, day_2026_02_02.META),
    "2026-02-03": (day_2026_02_03.handle, day_2026_02_03.META),
    "2026-02-04": (day_2026_02_04.handle, day_2026_02_04.META),
    "2026-02-08": (day_2026_02_08.handle, day_2026_02_08.META),
    "2026-02-09": (day_2026_02_09.handle, day_2026_02_09.META),
    "2026-02-11": (day_2026_02_11.handle, day_2026_02_11.META),
    "2026-02-12": (day_2026_02_12.handle, day_2026_02_12.META),
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
