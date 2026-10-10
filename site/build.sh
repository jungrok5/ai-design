#!/usr/bin/env bash
# Build the GitHub Pages site into _site/ (see site/build.py for what is generated).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 site/build.py
