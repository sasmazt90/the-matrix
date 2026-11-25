"""
Slayt 66 — Hallucination Tespiti
ÖNCE / SONRA örneği — model isimleri ve API yapıları doğrulanmalıdır.
"""

# ============================================================
# [✗] HALLUCINATION (ajanın uydurduğu)
# ============================================================
# import anthropic
# client = anthropic.Client()
# response = client.chat(
#     model="claude-3",
#     message="Merhaba"
# )
# ✗ .chat() metodu yok
# ✗ "claude-3" model adı yanlış (artık 4.7 var)
# ✗ message= parametresi yanlış

# ============================================================
# [✓] DOĞRULANMIŞ (gerçek API)
# ============================================================
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    messages=[{"role": "user", "content": "Merhaba"}],
)
# ✓ Gerçek API referansı
# ✓ Doğru model adı
# ✓ Doğru parametre yapısı
