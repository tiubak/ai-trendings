#!/usr/bin/env python3
"""Generate README.md files for existing projects that don't have one."""

import json
import os
from pathlib import Path

# Import from the main generator
from generate_project import build_readme, _call_ai

ROOT = Path(__file__).parent

def main():
    projects = json.loads((ROOT / "projects.json").read_text())
    
    generated = 0
    skipped = 0
    
    for date_str, project in sorted(projects.items()):
        path = ROOT / project["path"] / "README.md"
        
        if path.exists():
            print(f"  ⏭️  {date_str}: README exists, skipping")
            skipped += 1
            continue
        
        # Build a topic-like dict from project info
        topic = {
            "slug": project["path"].split("/")[-1].replace(f"{date_str}-", ""),
            "name": project["name"],
            "description": project.get("description", ""),
            "category": project.get("category", "AI Education"),
            "trending_source": project.get("trending_source", ""),
            "actions": {},
            "ui_config": {"input_fields": []},
        }
        
        # Try to read the handler to extract actions
        date_under = date_str.replace("-", "_")
        handler_path = ROOT / "lib" / "projects" / f"day_{date_under}.py"
        if handler_path.exists():
            try:
                code = handler_path.read_text()
                # Quick parse: find ACTIONS = {...} and META = {...}
                if "ACTIONS = " in code:
                    # Extract action names from the code
                    import re
                    actions_match = re.findall(r'"(\w+)":\s*\{', code)
                    for a in actions_match:
                        if a in ("name", "description", "category", "date", "prompt", "parse"):
                            continue
                        topic["actions"][a] = {"prompt": f"Action: {a}", "parse": "json"}
            except:
                pass
        
        readme = build_readme(topic, date_str)
        
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(readme)
        print(f"  ✅ {date_str}: {project['name']}")
        generated += 1
    
    print(f"\n📊 Done: {generated} generated, {skipped} skipped")

if __name__ == "__main__":
    main()
