#!/usr/bin/env bash
# Clone the three human-written English doc sources at the commits used in docs/measurement.md (sparse, docs only).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p human; cd human
clone() { local repo=$1 dir=$2 rev=$3; shift 3
  [ -d "$dir" ] || git clone -q --filter=blob:none --no-checkout "https://github.com/$repo" "$dir"
  git -C "$dir" sparse-checkout set "$@"; git -C "$dir" checkout -q "$rev"; }
clone reactjs/react.dev react.dev 046f17d04295ba047bb5739026b4ac3110f17028 src/content
clone toss/es-toolkit es-toolkit 19bd2cb1a22ca2e874f7febadbbb3064c3f5d595 docs/reference
clone mdn/content mdn-content aa95ccc2ee32f99c8fe2d7f370121a0fd4c6aaf4 \
  files/en-us/learn_web_development files/en-us/web/css/css_grid_layout files/en-us/web/css/guides/grid_layout \
  files/en-us/web/http/guides files/en-us/web/javascript/guide files/en-us/web/javascript/reference/global_objects/array
echo "human sources ready in $(pwd)"
