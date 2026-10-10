#!/usr/bin/env bash
# Build the GitHub Pages site into _site/: the page plus the design system files it loads (tokens, components,
# theme and copy scripts), copied from the plugin so the page always shows the current "Clear".
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf _site && mkdir -p _site/design
cp site/index.html _site/
cp plugins/ai-design/skills/polish-ui/design/{tokens.css,components.css,theme.js,copy.js} _site/design/
echo "wrote _site/"
