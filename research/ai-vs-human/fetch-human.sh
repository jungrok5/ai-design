#!/usr/bin/env bash
# Clone the five human-written Korean doc sources at the commits used in docs/measurement.md (sparse, docs only).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p human; cd human
clone() { local repo=$1 dir=$2 rev=$3; shift 3
  [ -d "$dir" ] || git clone -q --filter=blob:none --no-checkout "https://github.com/$repo" "$dir"
  if [ $# -gt 0 ]; then git -C "$dir" sparse-checkout set "$@"; else git -C "$dir" sparse-checkout disable; fi
  git -C "$dir" checkout -q "$rev"; }
clone reactjs/ko.react.dev ko.react.dev 89f79e9e971e9ad424ea5ebabdf8d5fa66c87375 src/content
clone toss/es-toolkit es-toolkit 19bd2cb1a22ca2e874f7febadbbb3064c3f5d595 docs/ko
clone naver/fe-news fe-news 82bad15134cf11647a1d032a9114da5d00787642
clone gyoogle/tech-interview-for-developer tech-interview-for-developer 41a7e91356adae7ee598d5ee3c27438449ce55d8
clone mdn/translated-content translated-content dac2621a8458b676dbbe0efca2a5b31150dcd623 \
  files/ko/web/javascript/guide files/ko/web/javascript/reference/global_objects/array files/ko/web/css/css_grid_layout \
  files/ko/web/http/guides files/ko/learn_web_development
echo "human sources ready in $(pwd)"
