#!/usr/bin/env bash
# Formats the file Claude just edited, so every member's Claude produces identical formatting.
# Never blocks Claude: always exits 0. Formatters that aren't installed are skipped.
input=$(cat)
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null \
  || printf '%s' "$input" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
[ -z "$file" ] || [ ! -f "$file" ] && exit 0

case "$file" in
  */ai-service/*.py)
    (cd "$CLAUDE_PROJECT_DIR/ai-service" && uv run ruff format "$file" && uv run ruff check --fix "$file") >/dev/null 2>&1 ;;
  *.java)
    # Enable once Spotless is added to build.gradle.kts by the tech lead:
    # (cd "$CLAUDE_PROJECT_DIR" && ./gradlew spotlessApply -q) >/dev/null 2>&1
    : ;;
esac
exit 0
