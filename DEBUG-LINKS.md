# Debug: Why Links Lose /docs Prefix

## Current Situation

- **Markdown source**: `href="/docs/refdog/commands/site/create.html"`
- **Manual navigation works**: `http://127.0.0.1:8080/docs/refdog/commands/site/create.html` ✅
- **Clicking link goes to**: `http://127.0.0.1:8080/refdog/commands/site/create.html` ❌

The `/docs` prefix is being stripped somewhere!

## Possible Causes

### 1. MkDocs `use_directory_urls: false` Processing

Your mkdocs.yml has `use_directory_urls: false`. This tells MkDocs to process links.

**Test**: View page source in browser
- Right-click on the commands index page
- "View Page Source"
- Search for "Site create"
- Check what the actual HTML href is in the rendered page

If it shows `/refdog/...` (without /docs), MkDocs is stripping it during build.

### 2. Base URL Tag

Check if MkDocs added a `<base>` tag in the HTML head that's changing link resolution.

**In browser**: View page source, look for `<base href=...>` tag

### 3. Site URL Configuration

Check your mkdocs.yml:
```yaml
site_url: https://skupper.io/docs/
```

If `site_url` ends with `/docs/`, MkDocs might be stripping `/docs` from absolute links thinking it's the base path.

## Quick Fix: Use Relative Links

Instead of absolute paths, we could use relative links:

From `commands/index.html` to `commands/site/create.html`:
```html
<a href="site/create.html">  <!-- relative -->
```

Not:
```html
<a href="/docs/refdog/commands/site/create.html">  <!-- absolute -->
```

**To test this approach, I'd need to modify the refdog generator to output relative links instead of absolute.**

## Next Steps

1. **Check rendered HTML**: View source in browser, find the actual href value
2. **Check for <base> tag**: See if there's URL rewriting
3. **Try relative links**: If absolute links are problematic

What does the href show in the rendered HTML (not the markdown source)?
