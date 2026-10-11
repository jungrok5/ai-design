#!/usr/bin/env bash
# usage: gen_one_en.sh G ID -> G/ai/ID.md (skips if present). Same isolation as the Korean run: empty dir, neutral prompt, no tools.
G=$1; ID=$2; OUT="$G/ai/$ID.md"; [ -s "$OUT" ] && exit 0
MODEL=$(python3 -c "import json;print([x for x in json.load(open('$G/pairs.json')) if x['id']=='$ID'][0]['model'])")
PROMPT=$(python3 -c "import json;p=[x for x in json.load(open('$G/pairs.json')) if x['id']=='$ID'][0];print(f\"Write {p['kind']} in Markdown.\n\nTitle: {p['title']}\nLength: about {p['words']} words of body text\")")
mkdir -p "$G/empty" && cd "$G/empty" && for try in 1 2 3; do
  printf '%s' "$PROMPT" | timeout 600 claude -p --model "$MODEL" --system-prompt "You are a helpful assistant." \
    --disallowedTools Bash Edit Write Read Glob Grep WebFetch WebSearch Task NotebookEdit > "$OUT.tmp" 2>"$OUT.err" \
    && [ "$(wc -c < "$OUT.tmp")" -gt 300 ] && mv "$OUT.tmp" "$OUT" && rm -f "$OUT.err" && exit 0
  sleep 20
done; echo "FAILED $ID $(head -c 200 "$OUT.err" 2>/dev/null)" >&2; exit 1
