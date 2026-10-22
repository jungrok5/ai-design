#!/usr/bin/env bash
# Generate one page with the plugin loaded (skills and the after-edit check).
# usage: tools/genp.sh TAG PLUGIN_DIR ID MODEL -> gen-TAG/ID-MODEL/
set -u; TAG=$1; PLUG=$2; ID=$3; M=$4; ROOT=$(cd "$(dirname "$0")/.." && pwd)
D="$ROOT/gen-$TAG/$ID-$M"; [ -f "$D/.done" ] && exit 0
rm -rf "$D"; mkdir -p "$D"; P=$(awk -F'\t' -v id="$ID" '$1==id{print $2}' "$ROOT/prompts.tsv")
cd "$D" && printf '%s' "$P 파일은 현재 폴더에 만들어." | timeout 1500 claude -p --model "$M" --plugin-dir "$PLUG" \
  --allowedTools Write Edit Read Skill --permission-mode acceptEdits > "$D/.log" 2>&1
touch "$D/.done"; echo "done $TAG $ID $M $(ls "$D")"
