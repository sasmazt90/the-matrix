"""
SECURITY_SCANNER.PY
Slayt 67 — Güvenlik Taraması (OWASP Top 10)
"""
import json
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

SECURITY_PROMPT = """
Bu kodu güvenlik açıkları için tara.
Kontrol et: SQL injection, XSS,
hardcoded secrets, auth bypass,
eski bağımlılıklar, hata sızması.
JSON formatında döndür.
"""


async def security_scan(code: str) -> dict:
    result = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SECURITY_PROMPT,
        messages=[{"role": "user", "content": code}],
    )
    return json.loads(result.content[0].text)


# TARAMA SONUCU
# [✗] CRITICAL: SQL injection — satır 23
# [✗] CRITICAL: Hardcoded API key — satır 7
# [✓] PASS:     XSS koruması mevcut
# [✓] PASS:     Auth kontrolleri yerinde
