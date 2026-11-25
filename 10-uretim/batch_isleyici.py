"""
BATCH_PROCESSOR.PY
Slayt 85 — Batch API: %50 maliyet indirimi, asenkron işleme
"""
import anthropic

client = anthropic.Anthropic()

# Batch isteği oluştur
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "task_001",
            "params": {
                "model": "claude-haiku-4-5",
                "messages": [{"role": "user", "content": "Özetle: ..."}],
            },
        }
    ]
)

# NE ZAMAN KULLANILMALI?
# BATCH: Gece çalışan veri işleme ve analiz görevleri
# BATCH: Toplu belge özetleme ve sınıflandırma
# CANLI: Kullanıcıya anlık yanıt gerektiren sohbet
# CANLI: Gerçek zamanlı kod üretimi ve hata ayıklama
