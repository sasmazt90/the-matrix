"""
PROMPT_CACHE_EXAMPLE.PY
Slayt 86 — Prompt Önbellekleme: %90 maliyet azalması (cache hit)
"""
import anthropic

client = anthropic.Anthropic()

system_prompt = "Çok uzun, sabit sistem promptunuz buraya..."
messages = [{"role": "user", "content": "Sorunuz"}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    system=[
        {
            "type": "text",
            "text": system_prompt,
            # Cache kontrolü ekle
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=messages,
)

# GÜNLÜK MALİYET KARŞILAŞTIRMASI
# [CACHE YOK] $3.00/gün — 100 çağrı × 10K token sistem prompt
# [CACHE VAR] $0.30/gün — ilk çağrı tam fiyat, geri kalan %90 indirim
