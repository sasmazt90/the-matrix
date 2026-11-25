#!/bin/bash
# notify-stop.sh
# Stop hook: Ajan durduğunda bildirim gönder.

set -euo pipefail

# Stop nedenini al
reason=$(echo "${CLAUDE_HOOK_INPUT:-}" | jq -r '.reason // "completed"' 2>/dev/null)
session_id="${CLAUDE_SESSION_ID:-unknown}"
duration="${CLAUDE_SESSION_DURATION:-unknown}"

message="🤖 Claude Code session ended
Reason: $reason
Session: $session_id
Duration: $duration"

# Mac native notification
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e "display notification \"$reason\" with title \"Claude Code Done\" sound name \"Glass\""
fi

# Linux native notification
if command -v notify-send &> /dev/null; then
    notify-send "Claude Code Done" "$reason"
fi

# Slack webhook (env var'dan al)
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
    curl -s -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"$message\"}" \
        "$SLACK_WEBHOOK_URL" > /dev/null
fi

# Audit log
echo "[$(date -Iseconds)] STOP $session_id $reason" >> ~/.claude/sessions.log

exit 0
