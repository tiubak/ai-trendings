#!/usr/bin/env python3
"""
Generate projects.json by scanning the projects/ directory.
This makes the calendar on index.html dynamic.

Usage: python scripts/generate_projects.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

def scan_projects():
    """Scan projects directory and extract project info"""

    projects_dir = Path("projects")
    if not projects_dir.exists():
        print("⚠ Projects directory not found")
        return {}

    projects = {}

    # Scan all subdirectories in projects/
    for project_path in projects_dir.iterdir():
        if not project_path.is_dir():
            continue

        # Skip template directory
        if project_path.name == "template":
            continue

        # Parse directory name: YYYY-MM-DD-project-name
        dir_name = project_path.name
        parts = dir_name.split("-", 3)

        if len(parts) < 4:
            # Invalid format, skip
            print(f"  ⚠ Skipping invalid format: {dir_name}")
            continue

        date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
        project_name = parts[3].replace("-", " ").title()

        # Extract README for description if available
        description = ""
        readme_path = project_path / "README.md"
        if readme_path.exists():
            with open(readme_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        description = line
                        break

        projects[date_str] = {
            "name": project_name,
            "path": f"projects/{dir_name}",
            "description": description,
            "created_at": date_str
        }

    return projects

def generate_projects_json(projects):
    """Generate projects.json file"""

    # Sort by date
    sorted_projects = dict(sorted(projects.items()))

    # Write to projects.json
    with open("projects.json", "w") as f:
        json.dump(sorted_projects, f, indent=2)

    print(f"✓ Generated projects.json with {len(projects)} projects")
    for date, info in sorted_projects.items():
        print(f"  {date}: {info['name']}")
    
    return sorted_projects

def update_readme_stats(projects):
    """Update README.md with project count"""

    readme_path = Path("README.md")
    if not readme_path.exists():
        return

    with open(readme_path, "r") as f:
        content = f.read()

    # Update project count if exists
    import re
    content = re.sub(
        r'<!-- PROJECT-COUNT -->\d+<!-- /PROJECT-COUNT -->',
        f'<!-- PROJECT-COUNT -->{len(projects)}<!-- /PROJECT-COUNT -->',
        content
    )

    with open(readme_path, "w") as f:
        f.write(content)

def main():
    print("🔍 Scanning projects directory...")
    
    projects = scan_projects()
    
    if not projects:
        print("⚠ No projects found")
        return
    
    generate_projects_json(projects)
    update_readme_stats(projects)
    
    print("\n✅ Done! projects.json is ready for index.html")

if __name__ == "__main__":
    main()
