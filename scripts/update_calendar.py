#!/usr/bin/env python3
"""
Helper script to update index.html with a new project
Usage: python scripts/update_calendar.py <date> <name> <path>
"""

import sys
import json
from datetime import datetime

def update_calendar(date: str, name: str, path: str):
    """Add a project to the calendar in index.html"""

    with open("index.html", "r") as f:
        content = f.read()

    # Find the projects object and add the new entry
    projects_pattern = r"const projects = \{([^}]+)\};"
    match = __import__('re').search(projects_pattern, content, __import__('re').DOTALL)

    if match:
        projects_dict_str = match.group(1).strip()
        # Parse existing projects
        try:
            projects = eval("{" + projects_dict_str + "}")
        except:
            projects = {}
    else:
        projects = {}

    # Add new project
    projects[date] = {
        "name": name,
        "path": path
    }

    # Convert back to string
    new_projects_str = "const projects = {\n"
    for d, info in sorted(projects.items()):
        new_projects_str += f'            "{d}": {{ "name": "{info["name"]}", "path": "{info["path"]}" }},\n'
    new_projects_str = new_projects_str.rstrip(",\n") + "\n        };"

    # Replace in content
    new_content = __import__('re').sub(
        r"const projects = \{[^}]+\};",
        new_projects_str,
        content,
        flags=__import__('re').DOTALL
    )

    with open("index.html", "w") as f:
        f.write(new_content)

    print(f"✓ Calendar updated: {date} - {name}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scripts/update_calendar.py <YYYY-MM-DD> <name> <path>")
        sys.exit(1)

    date, name, path = sys.argv[1], sys.argv[2], sys.argv[3]
    update_calendar(date, name, path)
