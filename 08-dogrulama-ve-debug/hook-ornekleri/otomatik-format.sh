#!/bin/bash
# auto-format.sh
# PostToolUse hook: Edit sonrası dosya formatla.

set -euo pipefail

# Tool input'tan dosya yolunu çıkar
file=$(echo "${CLAUDE_TOOL_INPUT:-}" | jq -r '.file_path // .path // ""' 2>/dev/null)

if [ -z "$file" ] || [ ! -f "$file" ]; then
    exit 0
fi

# Uzantıya göre formatter seç
case "$file" in
    *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
        if command -v prettier &> /dev/null; then
            prettier --write "$file" 2>/dev/null && echo "✓ formatted: $file" >&2
        elif command -v biome &> /dev/null; then
            biome format --write "$file" 2>/dev/null && echo "✓ formatted: $file" >&2
        fi
        ;;
    *.py)
        if command -v ruff &> /dev/null; then
            ruff format "$file" 2>/dev/null && echo "✓ formatted: $file" >&2
        elif command -v black &> /dev/null; then
            black --quiet "$file" 2>/dev/null && echo "✓ formatted: $file" >&2
        fi
        ;;
    *.go)
        command -v gofmt &> /dev/null && gofmt -w "$file" 2>/dev/null
        ;;
    *.json)
        command -v jq &> /dev/null && jq '.' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        ;;
    *.md)
        command -v prettier &> /dev/null && prettier --write "$file" --parser markdown 2>/dev/null
        ;;
esac

exit 0
