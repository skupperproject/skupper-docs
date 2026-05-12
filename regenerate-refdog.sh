#!/bin/bash
# regenerate-refdog.sh
# Regenerate refdog documentation for MkDocs

set -e

cd refdog

echo "Regenerating refdog for /docs/refdog"

./plano generate

echo ""
echo "✓ Refdog regenerated successfully"
echo ""
echo "Sample links generated:"
grep -m 3 'href=' input/commands/index.md | sed 's/.*href="\([^"]*\)".*/  \1/'
echo ""
echo "Verify these links resolve correctly in your MkDocs site"
