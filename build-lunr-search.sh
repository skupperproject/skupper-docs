#!/bin/sh

DOCSEARCH_ENABLED=true DOCSEARCH_ENGINE=lunr NODE_PATH="$(npm -g root)" antora --generator antora-site-generator-lunr preview-playbook.yml
echo "Antora build completed successfully."

echo "Customizing output."
# find build -name '*.html' -exec sed -i 's/_images/assets-images/g' {} \;
echo "Done."
