"""Project handlers registry."""

from . import day_2026_02_01  # AI Model Comparator
from . import day_2026_02_02  # AI Attention Mechanism Explorer
from . import day_2026_02_03  # AI Ethics Simulator
from . import day_2026_02_04  # AI Safety & Alignment Explorer
from . import day_2026_02_05  # AI Ethics Dilemma Simulator
from . import day_2026_02_07  # AI Token Cost Calculator
from . import day_2026_02_08  # AI Embeddings Explorer
from . import day_2026_02_09  # AI Model Selection Guide
from . import day_2026_02_10  # AI Fundamentals Explorer
from . import day_2026_02_11  # AI Trends & Insights
from . import day_2026_02_12  # AI Frontier Tracker
from . import day_2026_02_22  # AI Fundamentals: About AI
from . import day_2026_02_23  # AI Fundamentals & Insights

PROJECTS = {
    "2026-02-01": (lambda a, d: day_2026_02_01.handle(a, d), day_2026_02_01.META),
    "2026-02-02": (lambda a, d: day_2026_02_02.handle(a, d), day_2026_02_02.META),
    "2026-02-03": (lambda a, d: day_2026_02_03.handle(a, d), day_2026_02_03.META),
    "2026-02-04": (lambda a, d: day_2026_02_04.handle(a, d), day_2026_02_04.META),
    "2026-02-05": (lambda a, d: day_2026_02_05.handle(a, d), day_2026_02_05.META),
    "2026-02-07": (lambda a, d: day_2026_02_07.handle(a, d), day_2026_02_07.META),
    "2026-02-08": (lambda a, d: day_2026_02_08.handle(a, d), day_2026_02_08.META),
    "2026-02-09": (lambda a, d: day_2026_02_09.handle(a, d), day_2026_02_09.META),
    "2026-02-10": (lambda a, d: day_2026_02_10.handle(a, d), day_2026_02_10.META),
    "2026-02-11": (lambda a, d: day_2026_02_11.handle(a, d), day_2026_02_11.META),
    "2026-02-12": (lambda a, d: day_2026_02_12.handle(a, d), day_2026_02_12.META),
    "2026-02-22": (lambda a, d: day_2026_02_22.handle(a, d), day_2026_02_22.META),
    "2026-02-23": (lambda a, d: day_2026_02_23.handle(a, d), day_2026_02_23.META),
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
