#!/usr/bin/env bash
# Generate one page with Claude Code and no plugin, in an empty folder.
# usage: tools/gen.sh ID MODEL  -> out/ID-MODEL/  (ID is a row of prompts.tsv; MODEL is opus, sonnet or haiku)
set -u; ID=$1; M=$2; ROOT=$(cd "$(dirname "$0")/.." && pwd)
D="$ROOT/out/$ID-$M"; [ -n "$(ls -A "$D" 2>/dev/null)" ] && exit 0
mkdir -p "$D"; P=$(awk -F'\t' -v id="$ID" '$1==id{print $2}' "$ROOT/prompts.tsv")
cd "$D" && printf '%s' "$P" | timeout 900 claude -p --model "$M" --allowedTools Write Edit Read --permission-mode acceptEdits > "$D/.log" 2>&1
echo "done $ID $M $(ls "$D")"
