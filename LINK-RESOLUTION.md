# Link Resolution Guide

## How Refdog Links Work

Refdog generates links between pages using the `SITE_PREFIX` variable. The correct prefix depends on **where refdog content is mounted** in your documentation site.

### Your Current Structure

```
docs-vale/
  input/
    refdog -> ../refdog/input  (symlink)
      ↓ points to ↓
  refdog/
    input/
      commands/
        index.md
        site/
          create.md
      resources/
        site.md
```

## Finding the Right Prefix

### Test 1: Check MkDocs Structure

When MkDocs builds, check the output path structure:

```bash
# After mkdocs build
find output/docs -name "index.html" -path "*/commands/*" | head -1
```

Example outputs:
- `output/docs/refdog/commands/index.html` → use `/refdog`
- `output/docs/commands/index.html` → use `` (empty)

### Test 2: Check Generated Links

```bash
# Regenerate with test prefix
cd docs-vale
REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh

# Check what was generated
head -50 refdog/input/commands/index.md | grep href
```

Sample link: `<a href="/refdog/commands/site/create.html">`

### Test 3: Verify in Browser

1. Run `mkdocs serve`
2. Navigate to commands index page
3. Click a command link
4. If it works → prefix is correct!
5. If 404 → try different prefix

## Common Scenarios

### Scenario 1: Refdog at /refdog/

**MkDocs sees**:
```
doc-input/
  refdog/          ← via symlink
    commands/
    resources/
```

**Generated URLs**:
```
/refdog/commands/site/create.html
/refdog/resources/site.html
```

**Regenerate command**:
```bash
REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh
```

---

### Scenario 2: Refdog at Root

**MkDocs sees**:
```
doc-input/
  commands/       ← via symlink flattening
  resources/
```

**Generated URLs**:
```
/commands/site/create.html
/resources/site.html
```

**Regenerate command**:
```bash
REFDOG_SITE_PREFIX="" ./regenerate-refdog.sh
```

---

### Scenario 3: Custom Path

**MkDocs sees**:
```
doc-input/
  reference/       ← via symlink
    commands/
    resources/
```

**Generated URLs**:
```
/reference/commands/site/create.html
/reference/resources/site.html
```

**Regenerate command**:
```bash
REFDOG_SITE_PREFIX="/reference" ./regenerate-refdog.sh
```

## How MkDocs Resolves Links

With `use_directory_urls: false` (which you have), MkDocs keeps `.html` extensions.

**Absolute paths** (starting with `/`):
- `/refdog/commands/site/create.html` → looks from docs root
- Works if file exists at `output/docs/refdog/commands/site/create.html`

**Relative paths** (no leading `/`):
- `./site/create.html` → relative to current page
- `../index.html` → up one level

Refdog uses **absolute paths** for simplicity and consistency.

## Testing Link Resolution

### Quick Test

```bash
cd docs-vale

# Test with /refdog prefix
REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh

# Check a generated link
grep -m 1 'href="/refdog' refdog/input/commands/index.md

# Test with empty prefix
REFDOG_SITE_PREFIX="" ./regenerate-refdog.sh

# Check a generated link
grep -m 1 'href="/' refdog/input/commands/index.md
```

### Full Test with MkDocs

```bash
# 1. Regenerate with chosen prefix
REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh

# 2. Build and serve
cd ../website-mkdocs  # or wherever your mkdocs site is
mkdocs serve

# 3. Open browser to http://localhost:8000
# 4. Navigate to refdog commands index
# 5. Click any command link
# 6. If it loads → ✅ prefix is correct!
# 7. If 404 → ❌ try different prefix
```

## Debugging 404s

If links don't work:

### Check 1: Verify File Exists

```bash
# If link is: /refdog/commands/site/create.html
# Check file exists:
ls -la output/docs/refdog/commands/site/create.html
```

### Check 2: Check Browser Network Tab

1. Open browser DevTools (F12)
2. Click Network tab
3. Click the broken link
4. See what path the browser requested
5. Compare to actual file location

### Check 3: Try Different Prefix

```bash
# If /refdog doesn't work, try empty:
REFDOG_SITE_PREFIX="" ./regenerate-refdog.sh
# Rebuild and test

# If empty doesn't work, try /refdog:
REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh
# Rebuild and test
```

## Setting Default Prefix

### Option 1: Environment Variable

Add to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
export REFDOG_SITE_PREFIX="/refdog"
```

Then just run:
```bash
./regenerate-refdog.sh  # Uses /refdog automatically
```

### Option 2: Edit Script

Edit `regenerate-refdog.sh` and change this line:

```bash
# Change from:
SITE_PREFIX="${REFDOG_SITE_PREFIX:-/refdog}"

# To your default:
SITE_PREFIX="${REFDOG_SITE_PREFIX:-}"  # Empty prefix
# Or:
SITE_PREFIX="${REFDOG_SITE_PREFIX:-/reference}"  # Custom path
```

### Option 3: Wrapper Script

Create `regen.sh`:
```bash
#!/bin/bash
REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh
```

## Link Types in Refdog Output

Refdog generates several types of links:

### 1. Between Commands

`commands/index.md` → `commands/site/create.md`

```html
<a href="/refdog/commands/site/create.html">Site create</a>
```

### 2. Between Resources

`resources/index.md` → `resources/site.md`

```html
<a href="/refdog/resources/site.html">Site</a>
```

### 3. Commands ↔ Resources

`commands/site/create.md` → `resources/site.md`

```html
<a href="/refdog/resources/site.html">Site resource</a>
```

### 4. To External Links

External links are unchanged:

```html
<a href="https://skupper.io">Skupper website</a>
```

All internal links use `SITE_PREFIX`, so one setting controls all links.

## Summary

1. **Determine where refdog appears in MkDocs** (check built output)
2. **Set REFDOG_SITE_PREFIX** to match that path
3. **Regenerate** with `./regenerate-refdog.sh`
4. **Test** in browser to verify links work
5. **Commit** once confirmed

Most common values:
- `/refdog` - if refdog is in subdirectory
- `` (empty) - if refdog is at root
- `/reference` - if using custom path

**Need help?** Run `mkdocs build` and check where the HTML files end up!
