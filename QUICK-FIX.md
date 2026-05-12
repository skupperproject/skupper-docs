# Quick Fix: Link Resolution

## Problem

Links were 404-ing because they used `/refdog/...` but content is actually at `/docs/refdog/...`

## Solution

Set the correct prefix to match your MkDocs `site_dir`:

```bash
REFDOG_SITE_PREFIX="/docs/refdog" ./regenerate-refdog.sh
```

## How to Find the Correct Prefix

### Method 1: Check Your URL Structure

When you browse to a refdog page, look at the URL:
```
http://127.0.0.1:8080/docs/refdog/concepts/index.html
                      ^^^^^^^^^^^^^ this is your prefix
```

### Method 2: Check mkdocs.yml

```yaml
site_dir: output/docs  # ← The "/docs" part
```

If `site_dir` ends with `/docs`, your prefix should include `/docs`.

### Method 3: Test and Verify

1. Regenerate with a prefix:
   ```bash
   REFDOG_SITE_PREFIX="/docs/refdog" ./regenerate-refdog.sh
   ```

2. Rebuild MkDocs and test a link

3. If it works ✅ → prefix is correct!

4. If 404 ❌ → try without `/docs`:
   ```bash
   REFDOG_SITE_PREFIX="/refdog" ./regenerate-refdog.sh
   ```

## Common Prefixes

| Your Setup | Prefix to Use |
|------------|---------------|
| MkDocs serves at `/docs/` | `/docs/refdog` |
| MkDocs serves at root `/` | `/refdog` |
| Refdog in subdirectory `/reference/` | `/reference` |
| Refdog at root | `` (empty) |

## Default Updated

The `regenerate-refdog.sh` script now defaults to `/docs/refdog` to match your setup.

## Verification

After regenerating, check a generated file:

```bash
grep -m 3 'href=' refdog/input/concepts/index.md
```

Should show links like:
```html
href="/docs/refdog/concepts/site.html"
```

Not:
```html
href="/refdog/concepts/site.html"  ← Wrong, would 404
```

## Testing Checklist

- [ ] Regenerated with correct prefix
- [ ] MkDocs rebuilds without errors
- [ ] Navigate to any refdog page
- [ ] Click links - they should work!
- [ ] Cross-section links work (concepts → commands, etc.)

## If Links Still 404

1. **Check browser DevTools Network tab** - What URL is being requested?
2. **Check actual file location** - Does that file exist at that path?
3. **Try different prefix** - Experiment with `/docs/refdog`, `/refdog`, or empty
4. **Check MkDocs output** - Where are files actually being built?

   ```bash
   find output -name "site.html" | head -5
   ```

The file locations should match the link paths!
