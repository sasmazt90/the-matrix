"""
VERIFIER_PROMPT.PY
Slayt 65 — Doğrulayıcı Ajan Tasarımı
"""
import json
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

VERIFIER_SYSTEM = """
Sen bir kod doğrulayıcısısın.
Verilen kodu analiz et ve JSON döndür:
- passed: true/false
- issues: [bulunan sorunlar listesi]
- severity: "critical" | "warning" | "info"
- fix_suggestion: kısa düzeltme önerisi
Şüpheli her şeyi raporla. Varsayım yapma.
"""


async def verify(code: str) -> dict:
    result = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=VERIFIER_SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
    return json.loads(result.content[0].text)


# ÖRNEK ÇIKTI:
# {
#   "passed": false,
#   "issues": [
#     "SQL injection riski: satır 42",
#     "Hardcoded API key: satır 7"
#   ],
#   "severity": "critical",
#   "fix_suggestion": "Parametreli sorgu kullan"
# }
