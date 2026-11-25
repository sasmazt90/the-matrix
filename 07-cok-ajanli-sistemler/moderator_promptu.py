"""
MODERATOR_PROMPT.PY
Slayt 58 — Moderatör Ajan
"""
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

MODERATOR_SYSTEM = """
Sen bir tartışma moderatörüsün.
Görevin:
1. Her turdan sonra tartışmayı değerlendir
2. Konsensüs oluştu mu kontrol et
3. Eğer oluştuysa: CONSENSUS: [karar] yaz
4. Eğer oluşmadıysa: CONTINUE: [odak noktası] yaz
5. Maksimum 3 turda sonuca ulaş
"""


async def moderate(history: list) -> dict:
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=MODERATOR_SYSTEM,
        messages=history,
    )
    text = response.content[0].text
    if "CONSENSUS:" in text:
        return {"status": "done", "decision": text}
    return {"status": "continue", "focus": text}
