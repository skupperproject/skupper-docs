# Refdog Navigation Options for MkDocs

## Problem

Refdog has 43 command pages + 9 resource pages with its own hierarchical structure. Manually adding all these to `mkdocs.yml` nav would be tedious and hard to maintain.

## Solutions

### Option 1: Awesome Pages Plugin ✅ (Recommended)

**Install**:
```bash
pip install mkdocs-awesome-pages-plugin
```

**Configure in `mkdocs.yml`**:
```yaml
plugins:
  - search
  - awesome-pages
  # macros disabled or configured to skip refdog
```

**Create `.pages` files in refdog**:

#### `refdog/input/.pages`
```yaml
title: Reference
nav:
  - Commands: commands
  - Resources: resources
```

#### `refdog/input/commands/.pages`
```yaml
title: CLI Commands
nav:
  - Overview: index.md
  - site
  - connector
  - listener
  - link
  - token
  - debug
  - system
  - version.md
```

#### `refdog/input/commands/site/.pages`
```yaml
title: Site Commands
nav:
  - Overview: index.md
  - create.md
  - update.md
  - delete.md
  - status.md
  - generate.md
```

**Main `mkdocs.yml` stays simple**:
```yaml
nav:
  - Home: index.md
  - Overview: ...
  - Installation: ...
  # ... existing nav ...
  - Reference: refdog  # Just point to the directory!
```

**Pros**:
- ✅ Navigation defined within refdog directory
- ✅ Can commit `.pages` files to refdog repo
- ✅ Auto-discovery of new pages
- ✅ Flexible ordering and titles
- ✅ Refdog stays self-contained

**Cons**:
- ⚠️ Need to create `.pages` files
- ⚠️ Additional dependency

---

### Option 2: Literate Nav Plugin

**Install**:
```bash
pip install mkdocs-literate-nav
```

**Configure in `mkdocs.yml`**:
```yaml
plugins:
  - search
  - literate-nav:
      nav_file: SUMMARY.md
```

**Create `refdog/input/SUMMARY.md`**:
```markdown
# Reference Documentation

* [Commands](commands/index.md)
    * [Site](commands/site/index.md)
        * [create](commands/site/create.md)
        * [update](commands/site/update.md)
        * [delete](commands/site/delete.md)
        * [status](commands/site/status.md)
        * [generate](commands/site/generate.md)
    * [Connector](commands/connector/index.md)
        * [create](commands/connector/create.md)
        * [update](commands/connector/update.md)
        * [delete](commands/connector/delete.md)
        * [status](commands/connector/status.md)
        * [generate](commands/connector/generate.md)
    # ... etc
* [Resources](resources/index.md)
    * [Site](resources/site.md)
    * [Connector](resources/connector.md)
    # ... etc
```

**Main `mkdocs.yml`**:
```yaml
nav:
  - Home: index.md
  # ... existing nav ...
  - refdog/input/SUMMARY.md  # Points to literate nav file
```

**Pros**:
- ✅ Navigation as markdown (easy to edit)
- ✅ Single file to maintain
- ✅ Familiar GitBook-style

**Cons**:
- ⚠️ Must manually list all pages
- ⚠️ Still need to maintain SUMMARY.md

---

### Option 3: Section Plugin with Auto-discovery

**Install**:
```bash
pip install mkdocs-section-index
```

**Configure in `mkdocs.yml`**:
```yaml
plugins:
  - search
  - section-index

nav:
  - Home: index.md
  # ... existing nav ...
  - Reference:
    - refdog/input/index.md  # Section index
    # All sub-pages auto-discovered
```

**Pros**:
- ✅ Minimal configuration
- ✅ Auto-discovers pages

**Cons**:
- ⚠️ Less control over ordering
- ⚠️ Can't customize titles easily

---

### Option 4: Generate Navigation Programmatically

**Create script**: `refdog/generate-nav.py`

```python
#!/usr/bin/env python3
"""Generate MkDocs navigation from refdog structure"""

import os
import yaml
from pathlib import Path

def scan_commands():
    """Scan commands directory and generate nav structure"""
    nav = []
    commands_dir = Path('input/commands')
    
    # Get all command groups (subdirectories)
    for group_dir in sorted(commands_dir.iterdir()):
        if not group_dir.is_dir():
            continue
        
        group_name = group_dir.name.title()
        group_nav = {group_name: []}
        
        # Add index
        if (group_dir / 'index.md').exists():
            group_nav[group_name].append({
                'Overview': f'commands/{group_dir.name}/index.md'
            })
        
        # Add command pages
        for cmd_file in sorted(group_dir.glob('*.md')):
            if cmd_file.name == 'index.md':
                continue
            cmd_name = cmd_file.stem.title()
            group_nav[group_name].append({
                cmd_name: f'commands/{group_dir.name}/{cmd_file.name}'
            })
        
        nav.append(group_nav)
    
    return nav

def scan_resources():
    """Scan resources directory and generate nav structure"""
    nav = []
    resources_dir = Path('input/resources')
    
    for resource_file in sorted(resources_dir.glob('*.md')):
        if resource_file.name == 'index.md':
            continue
        resource_name = resource_file.stem.title()
        nav.append({
            resource_name: f'resources/{resource_file.name}'
        })
    
    return nav

def generate_nav():
    """Generate complete navigation structure"""
    nav = {
        'Reference': [
            {'Commands': 'refdog/input/commands/index.md'},
            *scan_commands(),
            {'Resources': 'refdog/input/resources/index.md'},
            *scan_resources()
        ]
    }
    
    print(yaml.dump(nav, default_flow_style=False))

if __name__ == '__main__':
    os.chdir('refdog')
    generate_nav()
```

**Usage**:
```bash
cd docs-vale/refdog
python generate-nav.py > nav-refdog.yml

# Then include in mkdocs.yml or merge manually
```

**Pros**:
- ✅ Full control over generation
- ✅ Can customize as needed
- ✅ Automatic from directory structure

**Cons**:
- ⚠️ Extra build step
- ⚠️ Custom code to maintain

---

### Option 5: Minimal Manual Nav (Simple)

Just add top-level entries and let users browse from index pages:

**`mkdocs.yml`**:
```yaml
nav:
  - Home: index.md
  # ... existing nav ...
  - Reference:
    - refdog/input/commands/index.md  # Commands index has links to all
    - refdog/input/resources/index.md  # Resources index has links to all
```

**Pros**:
- ✅ Minimal configuration
- ✅ No extra plugins
- ✅ Index pages already have all links

**Cons**:
- ⚠️ Only top-level in sidebar
- ⚠️ Users must click through to see all pages

---

## Recommended: Awesome Pages Plugin

**Why**: Best balance of flexibility and maintainability.

### Implementation Steps

#### 1. Install Plugin

```bash
cd website-mkdocs
pip install mkdocs-awesome-pages-plugin
echo "mkdocs-awesome-pages-plugin" >> requirements.txt
```

#### 2. Update mkdocs.yml

```yaml
plugins:
  - search
  - awesome-pages
```

#### 3. Create Navigation Files in Refdog

Create these files in `docs-vale/refdog/input/`:

**`.pages`**:
```yaml
title: Reference
arrange:
  - commands
  - resources
```

**`commands/.pages`**:
```yaml
title: CLI Commands
arrange:
  - index.md
  - site
  - connector
  - listener
  - link
  - token
  - debug
  - system
  - version.md
```

**`commands/site/.pages`**:
```yaml
title: Site
arrange:
  - index.md
  - create.md
  - update.md
  - delete.md
  - status.md
  - generate.md
```

**`resources/.pages`**:
```yaml
title: Custom Resources
arrange:
  - index.md
  - site.md
  - connector.md
  - listener.md
  - link.md
  - access-grant.md
  - access-token.md
  - router-access.md
  - attached-connector.md
  - attached-connector-binding.md
```

#### 4. Update Main Nav

In `website-mkdocs/mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Overview: ...
  - Installation: ...
  # ... existing nav ...
  - ... | refdog/**  # Auto-discover from refdog with .pages
```

Or explicitly:

```yaml
nav:
  - Home: index.md
  # ... existing nav ...
  - Reference: refdog
```

#### 5. Generate .pages Files Automatically

Create `refdog/generate-pages-files.sh`:

```bash
#!/bin/bash
# Generate .pages files for awesome-pages plugin

cd input

# Commands
cat > commands/.pages <<EOF
title: CLI Commands
arrange:
  - index.md
EOF

# Auto-add all command groups
for dir in commands/*/; do
    group=$(basename "$dir")
    echo "  - $group" >> commands/.pages
done

echo "  - version.md" >> commands/.pages

# Resources
cat > resources/.pages <<EOF
title: Custom Resources
arrange:
  - index.md
EOF

# Auto-add all resources
for file in resources/*.md; do
    if [ "$(basename "$file")" != "index.md" ]; then
        echo "  - $(basename "$file")" >> resources/.pages
    fi
done

echo "✓ Generated .pages files"
```

Run after each refdog generation:
```bash
cd refdog
./plano generate
./generate-pages-files.sh
```

---

## Integration with Build Process

Update `fix-refdog-for-mkdocs.sh`:

```bash
#!/bin/bash
# fix-refdog-for-mkdocs.sh
set -e

REFDOG_INPUT="refdog/input"

echo "Fixing refdog markdown for MkDocs compatibility..."

# Remove {{site.prefix}} template syntax
find "$REFDOG_INPUT" -name "*.md" -type f -exec \
  sed -i 's/{{site\.prefix}}//g' {} \;

echo "✓ Fixed {{site.prefix}} template syntax"

# Generate .pages files if awesome-pages plugin is used
if [ -f "refdog/generate-pages-files.sh" ]; then
    echo "Generating .pages navigation files..."
    cd refdog && ./generate-pages-files.sh && cd ..
    echo "✓ Generated .pages files"
fi

echo "✓ Refdog output is now MkDocs compatible"
```

---

## Quick Start: Minimal Approach

If you want to get started quickly without plugins:

**`website-mkdocs/mkdocs.yml`**:
```yaml
nav:
  - Home: index.md
  - Overview: ...
  - Installation: ...
  # ... existing sections ...
  
  - CLI Reference:
    - Overview: refdog/commands/index.md
    
  - Resource Reference:
    - Overview: refdog/resources/index.md
```

Users navigate from the index pages (which already have links to all commands/resources).

**Then later** add awesome-pages plugin for full navigation.

---

## Recommendation

**Start simple** (Option 5):
- Add just the index pages to nav
- Users can browse from there

**Then upgrade** to awesome-pages (Option 1):
- Install plugin
- Add `.pages` files to refdog
- Get full navigation automatically

This gives you a working integration immediately, with easy upgrade path to full navigation later.
