#!/bin/bash
# find-correct-prefix.sh
# Help determine the correct REFDOG_SITE_PREFIX for your MkDocs setup

echo "=== Refdog Link Prefix Diagnostic ==="
echo ""
echo "Answer these questions:"
echo ""
echo "1. Can you load this page?"
echo "   http://127.0.0.1:8080/docs/refdog/commands/index.html"
echo "   Answer (yes/no): "
read page_loads
echo ""

if [ "$page_loads" = "yes" ]; then
    echo "2. When you click 'Site create' link, what URL appears in browser?"
    echo "   (Copy the full URL from address bar)"
    echo "   URL: "
    read clicked_url
    echo ""

    echo "3. Can you manually navigate to this URL and it works?"
    echo "   http://127.0.0.1:8080/docs/refdog/commands/site/create.html"
    echo "   Answer (yes/no): "
    read manual_works
    echo ""

    if [ "$manual_works" = "yes" ]; then
        echo "✓ DIAGNOSIS: Links are being generated INCORRECTLY"
        echo ""
        echo "The file exists at: /docs/refdog/commands/site/create.html"
        echo "But the generated link is different."
        echo ""
        echo "Generated link was: $clicked_url"
        echo ""
        echo "FIX: The prefix is correct (/docs/refdog), but something else is wrong."
        echo "     Check the generated HTML in refdog/input/commands/index.md"
        echo "     Look at lines 19-25 for the actual href values."

    else
        echo "4. Try these URLs manually and tell me which one WORKS:"
        echo "   A) http://127.0.0.1:8080/refdog/commands/site/create.html"
        echo "   B) http://127.0.0.1:8080/commands/site/create.html"
        echo "   C) http://127.0.0.1:8080/docs/commands/site/create.html"
        echo "   D) None work"
        echo ""
        echo "   Answer (A/B/C/D): "
        read works
        echo ""

        case $works in
            A)
                echo "✓ DIAGNOSIS: Use prefix '/refdog'"
                echo ""
                echo "FIX: Regenerate with:"
                echo "     REFDOG_SITE_PREFIX='/refdog' ./regenerate-refdog.sh"
                ;;
            B)
                echo "✓ DIAGNOSIS: Use empty prefix"
                echo ""
                echo "FIX: Regenerate with:"
                echo "     REFDOG_SITE_PREFIX='' ./regenerate-refdog.sh"
                ;;
            C)
                echo "✓ DIAGNOSIS: Use prefix '/docs'"
                echo ""
                echo "FIX: Regenerate with:"
                echo "     REFDOG_SITE_PREFIX='/docs' ./regenerate-refdog.sh"
                ;;
            D)
                echo "✗ PROBLEM: Files not being built by MkDocs"
                echo ""
                echo "The refdog markdown files aren't being processed."
                echo "Check your MkDocs configuration and symlink setup."
                ;;
        esac
    fi
else
    echo "✗ PROBLEM: Can't access refdog pages at all"
    echo ""
    echo "This means MkDocs isn't finding the refdog files."
    echo "Check your symlink setup and MkDocs navigation config."
fi

echo ""
echo "=== End Diagnostic ==="
