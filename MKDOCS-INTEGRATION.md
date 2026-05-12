# MkDocs Integration Fix: Refdog Template Syntax

## Problem

Refdog-generated markdown uses `{{site.prefix}}` Jinja2 syntax for Transom/Jekyll, which conflicts with MkDocs macros plugin.

## Solutions

### Option 1: Configure Macros to Ignore Reference Docs (Recommended)

Edit `mkdocs.yml`:

```yaml
plugins:
  - search
  - macros:
      module_name: config/mkdocs_macros
      # Don't process refdog files (they have {{site.prefix}} syntax)
      include_dir: doc-input
      exclude:
        - reference/commands/*
        - reference/resources/*
```

**Pros**: 
- ✅ Simple configuration change
- ✅ Rest of site can still use macros
- ✅ Refdog files work as-is

**Cons**:
- ⚠️ Refdog files can't use mkdocs macros (but they don't need to)
- ⚠️ `{{site.prefix}}` won't be substituted (links may be broken)

---

### Option 2: Fix Refdog Generator to Output MkDocs-Compatible Syntax

Modify refdog's Python generator to use different syntax.

#### In `docs-vale/refdog/python/common.py`:

Find where links are generated and change `{{site.prefix}}` to relative paths:

```python
# OLD (Transom/Jekyll syntax)
url = f"{{{{site.prefix}}}}/{path}"

# NEW (MkDocs compatible - relative paths)
url = f"../{path}"  # or just f"/{path}" for absolute
```

**Implementation**:

```bash
cd docs-vale/refdog/
# Find where {{site.prefix}} is generated
grep -r "site.prefix" python/

# Likely in python/common.py or python/commands.py
# Replace template generation with relative paths
```

**Pros**:
- ✅ Refdog output is MkDocs native
- ✅ No MkDocs config changes needed
- ✅ Works with macros plugin

**Cons**:
- ⚠️ Breaks standalone refdog site (needs site.prefix)
- ⚠️ Must modify refdog generator

---

### Option 3: Post-Process Refdog Output for MkDocs

Create a script that converts refdog output for MkDocs:

```bash
#!/bin/bash
# convert-refdog-for-mkdocs.sh

# Replace {{site.prefix}} with empty string (relative links)
find docs-vale/refdog/input -name "*.md" -type f -exec \
  sed -i 's/{{site.prefix}}//g' {} \;

# Or replace with a base path
find docs-vale/refdog/input -name "*.md" -type f -exec \
  sed -i 's/{{site.prefix}}/\/docs/g' {} \;
```

**Usage**:
```bash
cd docs-vale/refdog/
./plano generate
../convert-refdog-for-mkdocs.sh
cd ../../website-mkdocs/
mkdocs build
```

**Pros**:
- ✅ Refdog generator unchanged
- ✅ Can customize for MkDocs

**Cons**:
- ❌ Extra build step
- ❌ Modifies committed files (or need .gitignore)
- ❌ Easy to forget

---

### Option 4: Make Refdog Output Configurable

Add configuration to refdog to choose output format:

#### In `docs-vale/refdog/python/common.py`:

```python
import os

# Check environment variable or config file
OUTPUT_FORMAT = os.getenv('REFDOG_OUTPUT_FORMAT', 'transom')

def make_link(path):
    if OUTPUT_FORMAT == 'mkdocs':
        # MkDocs style - relative or absolute paths
        return f"../{path}"
    else:
        # Transom/Jekyll style
        return f"{{{{site.prefix}}}}/{path}"
```

**Usage**:
```bash
# For standalone refdog site
./plano generate

# For MkDocs integration
REFDOG_OUTPUT_FORMAT=mkdocs ./plano generate
```

**Pros**:
- ✅ Best of both worlds
- ✅ Single source, multiple outputs
- ✅ No post-processing needed

**Cons**:
- ⚠️ Requires refdog code changes
- ⚠️ More complex generator logic

---

## Recommended Approach

### Short Term: Option 1 (Exclude from Macros)

Update `mkdocs.yml`:

```yaml
plugins:
  - search
  - macros:
      module_name: config/mkdocs_macros
      exclude:
        - reference/commands/**
        - reference/resources/**
```

**But**: The `{{site.prefix}}` will appear literally in rendered HTML. Need to fix links.

### Better Short Term: Option 3 (Post-Process)

Since `{{site.prefix}}` is in hundreds of files, use sed:

```bash
# One-time fix for existing files
cd /home/paulwright/repos/sk/vale/docs-vale/refdog/input
find . -name "*.md" -type f -exec sed -i 's/{{site\.prefix}}//g' {} \;

# Or add to refdog/.plano.py as a post-generation step
```

### Long Term: Option 4 (Configurable Output)

Modify refdog generator to support multiple output formats. This is the cleanest solution.

---

## Immediate Action

1. **Test with macros disabled**: You should now be able to build
2. **Check if links work**: With macros disabled, does site build and navigation work?
3. **Fix {{site.prefix}}**: Choose one of the approaches above

Let me know which approach you prefer and I can help implement it!
