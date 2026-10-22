#!/usr/bin/env bash
# Ask Claude Code (Opus, plugin loaded) to polish one page from out/.
# usage: tools/polish.sh TAG PLUGIN_DIR out/ID-MODEL -> polish-TAG/ID-MODEL/
set -u; TAG=$1; PLUG=$2; SRC=$3; ROOT=$(cd "$(dirname "$0")/.." && pwd); N=$(basename "$SRC")
D="$ROOT/polish-$TAG/$N"; [ -f "$D/.done" ] && exit 0
rm -rf "$D"; mkdir -p "$D"; cp "$ROOT/$SRC"/*.html "$ROOT/$SRC"/*.md "$D"/ 2>/dev/null
F=$(cd "$D" && ls *.html *.md 2>/dev/null | head -1)
cd "$D" && printf '%s' "$F 문구에서 AI가 쓴 티 나는 표현을 다듬어줘. 디자인과 구조는 그대로 두고 글만 고쳐." | \
  timeout 1200 claude -p --model opus --plugin-dir "$PLUG" --allowedTools Read Edit Write Skill --permission-mode acceptEdits > "$D/.log" 2>&1
touch "$D/.done"; echo "polished $TAG $N"
