#!/usr/bin/env bash
# usage: gen.sh DIR ID -> DIR/ai/ID.md. Same isolation as research/ai-vs-human: empty dir, neutral system prompt, no tools.
G=$1; ID=$2; OUT="$G/ai/$ID.md"; [ -s "$OUT" ] && exit 0
MODEL=$(python3 -c "import json;print([p for p in json.load(open('$G/prompts.json')) if p['id']=='$ID'][0]['model'])")
mkdir -p "$G/empty" && cd "$G/empty" && python3 -c "import json;print([p for p in json.load(open('$G/prompts.json')) if p['id']=='$ID'][0]['prompt'],end='')" \
 | timeout 600 claude -p --model "$MODEL" --system-prompt "You are a helpful assistant." --disallowedTools Bash Edit Write Read Glob Grep WebFetch WebSearch Task NotebookEdit > "$OUT.tmp" && mv "$OUT.tmp" "$OUT" || echo "FAILED $ID"
