#!/usr/bin/env python3
"""
Helper script to update index.html with a new project
Usage: python scripts/update_calendar.py <date> <name> <path>
"""

import sys
import re

def update_calendar(date: str, name: str, path: str):
    """Add a project to the calendar in index.html"""

    with open("index.html", "r") as f:
        lines = f.readlines()

    # Find the projects section and rebuild it
    in_projects = False
    projects = {}
    brace_level = 0
    projects_start = -1
    projects_end = -1

    for i, line in enumerate(lines):
        if "const projects = {" in line:
            in_projects = True
            projects_start = i
            brace_level = 1
            continue

        if in_projects:
            # Count braces to find the end of the object
            brace_level += line.count('{') - line.count('}')

            if brace_level == 0:
                projects_end = i
                break

            # Parse project entries (skip comments)
            stripped = line.strip()
            if stripped.startswith('"') and ':' in stripped:
                # Extract key and value
                try:
                    # Format: "2026-02-21": { name: "...", path: "..." },
                    match = re.match(r'"(\d{4}-\d{2}-\d{2})":\s*\{\s*name:\s*"([^"]*)",\s*path:\s*"([^"]*)"\s*\}', stripped)
                    if match:
                        p_date = match.group(1)
                        p_name = match.group(2)
                        p_path = match.group(3)
                        projects[p_date] = {"name": p_name, "path": p_path}
                except:
                    pass

    # Add new project
    projects[date] = {"name": name, "path": path}

    # Rebuild the projects section
    new_projects_lines = []
    new_projects_lines.append(lines[projects_start])  # Keep the opening line
    new_projects_lines.append("            // Format: \"YYYY-MM-DD\": { name: \"Project Name\", path: \"projects/2026-02-21-project-name\" }\n")

    # Add all projects sorted by date
    for d in sorted(projects.keys()):
        info = projects[d]
        # Escape any quotes in the name
        safe_name = info["name"].replace('"', '\\"')
        new_projects_lines.append(f'            "{d}": {{ "name": "{safe_name}", "path": "{info["path"]}" }},\n')

    # Add closing brace
    new_projects_lines.append("        };")

    # Replace old section with new one
    new_lines = lines[:projects_start] + new_projects_lines + lines[projects_end + 1:]

    with open("index.html", "w") as f:
        f.writelines(new_lines)

    print(f"✓ Calendar updated: {date} - {name}")
    print(f"  Total projects: {len(projects)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scripts/update_calendar.py <YYYY-MM-DD> <name> <path>")
        sys.exit(1)

    date, name, path = sys.argv[1], sys.argv[2], sys.argv[3]
    update_calendar(date, name, path)
