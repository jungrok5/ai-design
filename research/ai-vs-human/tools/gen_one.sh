#!/usr/bin/env bash
# usage: gen_one.sh G ID  -> G/ai/ID.md  (skips if present)
G=$1; ID=$2; OUT="$G/ai/$ID.md"; [ -s "$OUT" ] && exit 0
read -r MODEL PROMPT < <(python3 -c "
import json,sys;p=[x for x in json.load(open('$G/pairs.json')) if x['id']=='$ID'][0]
print(p['model'], json.dumps(f\"다음 제목으로 {p['kind']}을(를) 한국어 마크다운으로 작성해 주세요.\n\n제목: {p['title']}\n분량: 본문 약 {p['chars']}자\"))")
PROMPT=$(python3 -c "import json,sys;print(json.loads(sys.argv[1]))" "$PROMPT")
mkdir -p "$G/empty" && cd "$G/empty" && for try in 1 2 3; do
  printf '%s' "$PROMPT" | timeout 600 claude -p --model "$MODEL" --system-prompt "You are a helpful assistant." \
    --disallowedTools Bash Edit Write Read Glob Grep WebFetch WebSearch Task NotebookEdit > "$OUT.tmp" 2>"$OUT.err" \
    && [ "$(wc -c < "$OUT.tmp")" -gt 300 ] && mv "$OUT.tmp" "$OUT" && rm -f "$OUT.err" && exit 0
  sleep 5
done; echo "FAILED $ID" >&2; exit 1
