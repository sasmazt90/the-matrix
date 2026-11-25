#!/bin/bash
# check-no-secrets.sh
# PreToolUse hook: Edit/Write öncesinde içerikte secret var mı kontrol eder.
# Bulursa exit 1 → tool çağrısı bloklanır.

set -euo pipefail

# Tool input'tan içeriği çıkar
content=$(echo "${CLAUDE_TOOL_INPUT:-}" | jq -r '.content // .new_string // ""' 2>/dev/null)

if [ -z "$content" ]; then
    exit 0
fi

# Anahtar pattern'lar
PATTERNS=(
    'sk-[A-Za-z0-9]{20,}'                    # OpenAI / Anthropic
    'sk-ant-[A-Za-z0-9_-]{30,}'              # Anthropic specific
    'ghp_[A-Za-z0-9]{36}'                    # GitHub PAT
    'github_pat_[A-Za-z0-9_]{82}'            # GitHub fine-grained
    'AKIA[0-9A-Z]{16}'                       # AWS access key
    'AIza[A-Za-z0-9_-]{35}'                  # Google API
    'xox[baprs]-[A-Za-z0-9-]{10,}'           # Slack
    'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'  # JWT
    '-----BEGIN [A-Z ]+PRIVATE KEY-----'     # PEM keys
    'mongodb(\+srv)?:\/\/[^:]+:[^@]+@'       # MongoDB connection string with creds
    'postgres:\/\/[^:]+:[^@]+@'              # Postgres connection string with creds
)

for pattern in "${PATTERNS[@]}"; do
    if echo "$content" | grep -qE "$pattern"; then
        echo "❌ BLOCKED: Potansiyel secret tespit edildi (pattern: $pattern)" >&2
        echo "   Edit/Write iptal edildi. .env dosyası kullanın veya kasıtlıysa hook'u geçici devre dışı bırakın." >&2
        exit 1
    fi
done

# Common .env value patterns (assignment-style)
if echo "$content" | grep -qE '^(API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY)\s*=\s*["\x27]?[A-Za-z0-9+/=_-]{16,}'; then
    echo "❌ BLOCKED: Hardcoded credential assignment tespit edildi" >&2
    exit 1
fi

exit 0
