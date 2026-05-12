# Changes Summary: Configurable Link Prefix for MkDocs Integration

## Problem Solved

Refdog generated links with `{{site.prefix}}` template syntax that worked for Transom/Jekyll but broke MkDocs macros plugin, causing `'site' is undefined` errors.

## Solution Implemented

Made link prefix configurable via environment variable, allowing refdog to generate output for different deployment targets.

## Files Changed

### 1. `python/common.py`
**Lines added**: 7 (after line 3)
```python
import os as _os

# Link prefix - configurable via environment variable
SITE_PREFIX = _os.getenv('REFDOG_SITE_PREFIX', '{{site.prefix}}')
```

**Lines changed**: 2
- Line 120: `url = SITE_PREFIX + url` (was `url = "{{site.prefix}}" + url`)
- Line 261: `return f"{SITE_PREFIX}/{plural(type)}/{self.id}.html"` (was hardcoded template)

### 2. `python/commands.py`
**Lines changed**: 1
- Line 473: `return f"{SITE_PREFIX}/commands/{self.id}/index.html"` (was hardcoded template)

### 3. `python/resources.py`
**Lines changed**: 3
- Lines 64-66: Replace `{{site.prefix}}` in descriptions before output

**Total code changes**: 13 lines across 3 files

## Usage

### For MkDocs (default)
```bash
./regenerate-refdog.sh
# Uses REFDOG_SITE_PREFIX="/refdog" by default
```

### For Transom/Jekyll
```bash
REFDOG_SITE_PREFIX="{{site.prefix}}" ./plano generate
```

### For Custom Path
```bash
REFDOG_SITE_PREFIX="/reference" ./regenerate-refdog.sh
```

### For Root-Level Deployment
```bash
REFDOG_SITE_PREFIX="" ./regenerate-refdog.sh
```

## Generated Link Examples

### With Default (/refdog)
```html
<a href="/refdog/commands/site/create.html">Site create</a>
<a href="/refdog/resources/site.html">Site resource</a>
```

### With Empty Prefix
```html
<a href="/commands/site/create.html">Site create</a>
<a href="/resources/site.html">Site resource</a>
```

### With Custom Prefix (/reference)
```html
<a href="/reference/commands/site/create.html">Site create</a>
<a href="/reference/resources/site.html">Site resource</a>
```

## Verification

```bash
# Verify no template syntax remains
grep -r "{{site.prefix}}" refdog/input/
# Should return 0 matches

# Check generated links
grep -m 5 'href=' refdog/input/commands/index.md
# Should show links with configured prefix
```

## New/Updated Files

### Scripts
- **`regenerate-refdog.sh`** (new) - Regeneration script with prefix configuration
- ~~`fix-refdog-for-mkdocs.sh`~~ (removed) - No longer needed!

### Documentation
- **`LINK-RESOLUTION.md`** (new) - Complete guide to link resolution
- **`LINK-PREFIX-SOLUTION.md`** (new) - Technical details and implementation options  
- **`REFDOG-NAVIGATION.md`** (new) - MkDocs navigation options
- **`MKDOCS-INTEGRATION.md`** (new) - MkDocs integration guide
- **`README.md`** (updated) - New workflow without sed post-processing
- **`PLAN.md`** (updated) - Integration approach updated

## Benefits

✅ **No post-processing needed** - Links generated correctly by default
✅ **Flexible deployment** - Works for any base path
✅ **Backward compatible** - Default preserves Transom template syntax
✅ **Simple configuration** - Single environment variable
✅ **Clean code** - Minimal changes (13 lines)
✅ **MkDocs compatible** - No more macros plugin conflicts

## Testing

```bash
# Test default (MkDocs /refdog path)
./regenerate-refdog.sh
grep '/refdog/commands' refdog/input/commands/index.md

# Test empty (root deployment)
REFDOG_SITE_PREFIX="" ./regenerate-refdog.sh
grep -v '/refdog' refdog/input/commands/index.md | grep '/commands'

# Test custom path
REFDOG_SITE_PREFIX="/api-reference" ./regenerate-refdog.sh
grep '/api-reference/commands' refdog/input/commands/index.md
```

## Migration for Existing Users

### Old Workflow (with sed)
```bash
cd refdog
./plano generate
cd ..
./fix-refdog-for-mkdocs.sh  # sed post-processing
```

### New Workflow (clean)
```bash
./regenerate-refdog.sh  # One command, properly configured
```

## Backward Compatibility

Default behavior unchanged for Transom/Jekyll users:
```bash
# Without env var, uses {{site.prefix}} template syntax
./plano generate  # Still works for Transom!
```

MkDocs users explicitly set the prefix:
```bash
# With env var, uses actual path
REFDOG_SITE_PREFIX="/refdog" ./plano generate
```

## Next Steps

1. Test in your MkDocs build
2. Verify links resolve correctly
3. Adjust `REFDOG_SITE_PREFIX` if needed (see LINK-RESOLUTION.md)
4. Commit changes

## Questions?

- **Link resolution**: See `LINK-RESOLUTION.md`
- **Navigation setup**: See `REFDOG-NAVIGATION.md`
- **MkDocs integration**: See `MKDOCS-INTEGRATION.md`
- **Technical details**: See `LINK-PREFIX-SOLUTION.md`
