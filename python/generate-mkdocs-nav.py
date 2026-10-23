#!/usr/bin/env python3
"""
Generate mkdocs.yml from mkdocs.template.yml and skupper-job-mapping.csv.

Reads the JTBD job-mapping CSV to build a nav section organized by JTBD
lifecycle categories (Discover, Install, Deploy, Configure, etc.), then
inserts it into the template to produce mkdocs.yml.
"""

import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TEMPLATE = BASE / "mkdocs.template.yml"
CSV_PATH = BASE / "skupper-job-mapping.csv"
OUTPUT = BASE / "mkdocs.yml"

CATEGORY_ORDER = [
    "What's New", "Discover", "Get started", "Plan",
    "Install", "Deploy", "Configure", "Secure",
    "Observe", "Troubleshoot", "Upgrade", "Reference", "Optimize",
]

HEADER_ROWS = 4


def read_csv_nav_entries(csv_path):
    """Read the job-mapping CSV and return L2 entries grouped by category."""
    groups = {}
    current_category = None

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader):
            if row_num < HEADER_ROWS:
                continue
            if len(row) < 7:
                continue

            cat_col = row[0].strip()
            l2_col = row[1].strip()
            path_col = row[6].strip()

            if cat_col and not l2_col:
                current_category = cat_col
                continue

            if l2_col and current_category:
                title = resolve_variables(l2_col)
                path = strip_input_prefix(path_col)
                if path:
                    groups.setdefault(current_category, []).append({
                        "title": title,
                        "path": path,
                    })

    return groups


def resolve_variables(title):
    """Replace template variables with literal values for nav labels."""
    title = title.replace("{{skupper_name}}", "Skupper")
    title = title.replace("{skupper_name}", "Skupper")
    return title


def strip_input_prefix(path):
    """Strip input/ prefix since mkdocs paths are relative to docs_dir."""
    if path.startswith("input/"):
        return path[6:]
    return path


def generate_nav_yaml(groups):
    """Generate the nav: YAML block from grouped entries."""
    lines = ["nav:"]
    lines.append("  - Home: index.md")

    sorted_cats = sorted(
        groups.keys(),
        key=lambda c: CATEGORY_ORDER.index(c) if c in CATEGORY_ORDER else 999,
    )

    for cat in sorted_cats:
        entries = groups[cat]
        lines.append(f"  - {cat}:")
        for entry in entries:
            lines.append(f"    - {entry['title']}: {entry['path']}")

    lines.append("  - ...")
    return "\n".join(lines)


def main():
    if not TEMPLATE.exists():
        print(f"Error: template not found at {TEMPLATE}")
        return 1
    if not CSV_PATH.exists():
        print(f"Error: CSV not found at {CSV_PATH}")
        return 1

    template = TEMPLATE.read_text(encoding="utf-8")
    groups = read_csv_nav_entries(CSV_PATH)
    nav_yaml = generate_nav_yaml(groups)

    output = re.sub(r"^# \{\{NAV\}\}$", nav_yaml, template, flags=re.MULTILINE)

    OUTPUT.write_text(output, encoding="utf-8")
    total = sum(len(v) for v in groups.values())
    print(f"Wrote {OUTPUT} with {len(groups)} categories, {total} nav entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
