#!/usr/bin/env python3
"""
Generate JTBD Job Mapping CSV for Service Interconnect from cqa/ content.

Walks the cqa/ include tree, maps each assembly/module to a JTBD category
(from RHSI Jobs CSV), and outputs a CSV matching the Job Mapping template.
"""

import argparse
import csv
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Explicit assembly → JTBD category mapping (derived from RHSI Jobs CSV)
# ---------------------------------------------------------------------------
ASSEMBLY_CATEGORY = {
    # Overview (Discover)
    "overview-assembly-skupper-overview": "Discover",
    "overview-assembly-overview-connectivity": "Discover",
    "overview-assembly-skupper-security": "Discover",
    "overview-assembly-skupper-routing": "Discover",
    "overview-assembly-overview-load-balancing": "Discover",
    # Reference
    "overview-assembly-kube-resources": "Reference",
    # Upgrade
    "overview-assembly-migrating": "Upgrade",
    # Deploy – Kubernetes CLI
    "kube-cli-assembly-kube-cli": "Deploy",
    "kube-cli-assembly-kube-creating-site-cli": "Deploy",
    # Configure – Kubernetes CLI
    "kube-cli-assembly-kube-linking-cli": "Configure",
    "kube-cli-assembly-kube-exposing-services-cli": "Configure",
    # Deploy – Kubernetes YAML
    "kube-yaml-assembly-kube-yaml": "Deploy",
    "kube-yaml-assembly-kube-creating-site-yaml": "Deploy",
    # Configure – Kubernetes YAML
    "kube-yaml-assembly-kube-yaml-site-linking": "Configure",
    "kube-yaml-assembly-kube-exposing-services-yaml": "Configure",
    # Secure – Kubernetes YAML
    "kube-yaml-assembly-kube-yaml-custom-certs": "Secure",
    # Deploy – System CLI
    "system-cli-assembly-system-cli": "Deploy",
    "system-cli-assembly-system-creating-site-cli": "Deploy",
    # Configure – System CLI
    "system-cli-assembly-system-linking-cli": "Configure",
    "system-cli-assembly-system-exposing-services-cli": "Configure",
    # Deploy – System YAML
    "system-yaml-assembly-system-yaml": "Deploy",
    "system-yaml-assembly-system-yaml-site-configuration": "Deploy",
    # Configure – System YAML
    "system-yaml-assembly-system-yaml-site-linking": "Configure",
    "system-yaml-assembly-system-yaml-service-exposure": "Configure",
    # Observe
    "console-assembly-observer-config": "Observe",
    # Troubleshoot
    "troubleshooting-assembly-troubleshooting": "Troubleshoot",
}

# Install guide modules that need category override
INSTALL_OVERRIDES = {
    "upgrading-operator-sites": "Upgrade",
    "upgrading-cli-sites": "Upgrade",
}

# ---------------------------------------------------------------------------
# Markdown file → JTBD category mapping (for monolithic md files in input/)
# ---------------------------------------------------------------------------
MD_CATEGORY = {
    "overview/index.md": "Discover",
    "overview/connectivity.md": "Discover",
    "overview/security.md": "Discover",
    "overview/routing.md": "Discover",
    "overview/load-balancing.md": "Discover",
    "overview/resources.md": "Reference",
    "overview/migrating.md": "Upgrade",
    "install/index.md": "Install",
    "kube-cli/index.md": "Deploy",
    "kube-cli/site-configuration.md": "Deploy",
    "kube-cli/site-linking.md": "Configure",
    "kube-cli/service-exposure.md": "Configure",
    "kube-yaml/index.md": "Deploy",
    "kube-yaml/site-configuration.md": "Deploy",
    "kube-yaml/site-linking.md": "Configure",
    "kube-yaml/custom-certs.md": "Secure",
    "kube-yaml/service-exposure.md": "Configure",
    "system-cli/index.md": "Deploy",
    "system-cli/site-configuration.md": "Deploy",
    "system-cli/site-linking.md": "Configure",
    "system-cli/service-exposure.md": "Configure",
    "system-yaml/index.md": "Deploy",
    "system-yaml/site-configuration.md": "Deploy",
    "system-yaml/site-linking.md": "Configure",
    "system-yaml/service-exposure.md": "Configure",
    "console/index.md": "Observe",
    "console/configuration.md": "Observe",
    "troubleshooting/index.md": "Troubleshoot",
}

# Action verbs that indicate a content item is a job (not a topic)
ACTION_VERBS = [
    "creating", "create", "install", "link ", "linking",
    "expose", "exposing", "check", "delete", "deleting",
    "configur", "deploy", "generate", "set up", "build",
    "upgrade", "upgrading", "migrat", "activate", "activating",
    "download", "register", "specify", "specifying",
    "provision", "troubleshoot", "access",
]

TOPIC_INDICATORS = [
    "overview", "about", "introduction", "what is",
    "application networks", "skupper routers", "skupper routing",
    "skupper security", "skupper connectivity", "load balancing",
    "custom resource definitions", "deployments", "configmaps",
    "secrets", "service accounts", "services",
    "network observer configuration reference",
]


def get_title(filepath):
    """Extract = Title from an adoc file."""
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                if line.startswith("= "):
                    return line[2:].strip()
    except (FileNotFoundError, IsADirectoryError):
        pass
    return filepath.stem


def get_includes(filepath):
    """Return list of resolved include paths from an adoc file."""
    includes = []
    parent = filepath.parent
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("//"):
                    continue
                m = re.match(r"include::(.+?)\[", stripped)
                if m:
                    inc = Path(os.path.normpath(parent / m.group(1)))
                    if inc.exists() and inc.suffix == ".adoc":
                        name = inc.name
                        if name in ("attributes.adoc", "revision-info.adoc",
                                    "tp-note.adoc", "master-docinfo.xml"):
                            continue
                        includes.append(inc)
    except FileNotFoundError:
        pass
    return includes


def is_job(title):
    """Heuristic: action-oriented titles are jobs, noun phrases are topics."""
    if not title:
        return False
    t = title.lower()
    for indicator in TOPIC_INDICATORS:
        if indicator in t:
            return False
    for verb in ACTION_VERBS:
        if verb in t:
            return True
    return False


def rel_path(filepath):
    """Return path relative to repo root."""
    try:
        return str(filepath.relative_to(BASE))
    except ValueError:
        return str(filepath)


def process_book(master_path, default_category, entries):
    """Process a master.adoc → assemblies → modules hierarchy."""
    includes = get_includes(master_path)
    for inc in includes:
        inc_stem = inc.stem
        inc_title = get_title(inc)

        # Determine category
        cat = ASSEMBLY_CATEGORY.get(inc_stem)
        if cat is None:
            cat = INSTALL_OVERRIDES.get(inc_stem, default_category)

        sub_includes = get_includes(inc)

        if sub_includes:
            # Assembly with modules
            entries.append({
                "category": cat,
                "level": 2,
                "title": inc_title,
                "path": rel_path(inc),
                "is_job": is_job(inc_title),
            })
            for mod in sub_includes:
                mod_title = get_title(mod)
                entries.append({
                    "category": cat,
                    "level": 3,
                    "title": mod_title,
                    "path": rel_path(mod),
                    "is_job": is_job(mod_title),
                })
        else:
            # Standalone module (no sub-includes)
            entries.append({
                "category": cat,
                "level": 2,
                "title": inc_title,
                "path": rel_path(inc),
                "is_job": is_job(inc_title),
            })


def build_entries():
    entries = []

    # 1. cqa/usage → vale/sk-vale/index.adoc → assemblies → modules
    usage_master = (BASE / "cqa" / "usage" / "master.adoc").resolve()
    if usage_master.exists():
        for inc in get_includes(usage_master):
            if "index" in inc.name:
                process_book(inc, "Discover", entries)

    # 2. cqa/install → docs/install/master.adoc
    install_master = (BASE / "cqa" / "install" / "master.adoc").resolve()
    if install_master.exists():
        process_book(install_master, "Install", entries)

    # 3. cqa/overview → docs/overview/master.adoc
    overview_master = (BASE / "cqa" / "overview" / "master.adoc").resolve()
    if overview_master.exists():
        process_book(overview_master, "Discover", entries)

    # 4. cqa/release-notes → docs/release-notes/master.adoc
    rn_master = (BASE / "cqa" / "release-notes" / "master.adoc").resolve()
    if rn_master.exists():
        process_book(rn_master, "What's New", entries)

    return entries


# ---------------------------------------------------------------------------
# Markdown (monolithic .md files in input/) support
# ---------------------------------------------------------------------------

def get_md_headings(filepath):
    """Extract headings with anchor IDs and content-type markers from a markdown file."""
    headings = []
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return headings

    pending_anchor = None
    in_fence = False
    for i, raw in enumerate(lines):
        line = raw.strip()

        if line.startswith("```") or line.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        m = re.match(r'<a\s+id="([^"]+)"', line)
        if m:
            pending_anchor = m.group(1)
            continue

        if line.startswith("## "):
            title = line[3:].strip()
            level = 2
        elif line.startswith("# "):
            title = line[2:].strip()
            level = 1
        else:
            if line and not line.startswith("<a "):
                pending_anchor = None
            continue

        content_type = ""
        if i + 1 < len(lines):
            ct = re.match(r'<!--(\w+)-->', lines[i + 1].strip())
            if ct:
                content_type = ct.group(1)

        headings.append({
            "level": level,
            "title": title,
            "anchor": pending_anchor or "",
            "content_type": content_type,
        })
        pending_anchor = None

    return headings


def build_entries_md():
    """Build entries from monolithic markdown files in input/."""
    entries = []
    input_dir = BASE / "input"
    if not input_dir.exists():
        return entries

    for md_rel, category in MD_CATEGORY.items():
        filepath = input_dir / md_rel
        if not filepath.exists():
            continue

        headings = get_md_headings(filepath)
        file_rel = f"input/{md_rel}"

        for h in headings:
            if h["level"] == 1:
                entries.append({
                    "category": category,
                    "level": 2,
                    "title": h["title"],
                    "path": file_rel,
                    "is_job": is_job(h["title"]),
                })
            elif h["level"] == 2:
                anchor = f"#{h['anchor']}" if h["anchor"] else ""
                entries.append({
                    "category": category,
                    "level": 3,
                    "title": h["title"],
                    "path": f"{file_rel}{anchor}",
                    "is_job": is_job(h["title"]),
                })

    return entries


# ---------------------------------------------------------------------------
# Sort by category in JTBD lifecycle order, then by level
# ---------------------------------------------------------------------------
CATEGORY_ORDER = [
    "What's New", "Discover", "Get started", "Plan",
    "Install", "Deploy", "Configure", "Secure",
    "Observe", "Troubleshoot", "Upgrade", "Reference", "Optimize",
]


def sort_key(entry):
    cat = entry["category"]
    try:
        cat_idx = CATEGORY_ORDER.index(cat)
    except ValueError:
        cat_idx = 999
    return (cat_idx, entry["level"])


def write_csv(entries, output_path):
    # Group entries: within each category keep original order (doc structure)
    from collections import OrderedDict
    groups = OrderedDict()
    for e in entries:
        groups.setdefault(e["category"], []).append(e)

    sorted_cats = sorted(groups.keys(), key=lambda c: CATEGORY_ORDER.index(c)
                         if c in CATEGORY_ORDER else 999)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Template header rows
        w.writerow(["", "JTBD - Service Interconnect Job Mapping", "", "",
                     "", "", "", "", ""])
        w.writerow(["", "", "", "", "", "", "", "", ""])
        w.writerow(["", "LEFT HAND NAVIGATION", "", "",
                     "RIGHT HAND NAVIGATION", "", "", "", ""])
        w.writerow([
            "Category (L!)", "Level 2 (Jobs)", "Level 3 (Jobs or Topics)",
            "Level 4 (Jobs or Topics)", "Topic (H2)", "H3",
            "Full filename path", "Is a job?", "Navtitle",
        ])

        for cat in sorted_cats:
            items = groups[cat]
            # Category header row
            w.writerow([cat, "", "", "", "", "", "", "FALSE", ""])

            for item in items:
                row = [""] * 9
                lvl = item["level"]
                row[lvl - 1] = item["title"]  # L2→col1, L3→col2, L4→col3
                row[6] = item["path"]
                row[7] = "TRUE" if item["is_job"] else "FALSE"
                w.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate JTBD Job Mapping CSV for Service Interconnect")
    parser.add_argument(
        "--source", choices=["adoc", "md", "auto"], default="auto",
        help="Content source: adoc (cqa/ tree), md (input/ markdown), "
             "or auto-detect (default)")
    args = parser.parse_args()

    source = args.source
    if source == "auto":
        source = "adoc" if (BASE / "cqa").exists() else "md"

    if source == "adoc":
        entries = build_entries()
    else:
        entries = build_entries_md()

    output = BASE / "skupper-job-mapping.csv"
    write_csv(entries, output)
    print(f"Wrote {len(entries)} entries to {output} (source: {source})")