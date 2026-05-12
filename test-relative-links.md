# Alternative: Use Relative Links

The issue might be that absolute paths like `/docs/refdog/commands/site/create.html` don't resolve correctly.

## Try Relative Links Instead

MkDocs works well with relative links. Instead of:
```html
<a href="/docs/refdog/commands/site/create.html">
```

Use:
```html
<a href="site/create.html">  (from commands/index.html)
```

## Quick Test

Regenerate with empty prefix and see if relative links work:

```bash
cd /home/paulwright/repos/sk/vale/docs-vale
REFDOG_SITE_PREFIX="" ./regenerate-refdog.sh
```

This will generate links like:
- `/commands/site/create.html` (from root)

Which might work better depending on your MkDocs setup.

## Or Try Without Prefix At All

Actually, the best approach for MkDocs is usually to let it handle paths. Can you:

1. Check if you can manually navigate to: `http://127.0.0.1:8080/docs/refdog/commands/site/create.html`
   - If YES → prefix is wrong in generation
   - If NO → file isn't being built there

2. Try navigating to: `http://127.0.0.1:8080/refdog/commands/site/create.html`
   - Does this work?

This will tell me the exact prefix needed.
