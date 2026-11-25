"""
TASK_ROUTER.PY
Slayt 84 — Görev Yönlendirme: Doğru görevi doğru modele otomatik yönlendir
"""


def route_task(task: str) -> str:
    # Basit görev sinyalleri
    simple = ["sınıflandır", "özetle", "çıkar"]
    complex = ["tasarla", "mimari", "analiz et"]

    if any(s in task for s in simple):
        return "claude-haiku-4-5"
    elif any(c in task for c in complex):
        return "claude-opus-4-7"
    else:
        return "claude-sonnet-4-6"


# YÖNLENDİRME ETKİNLİĞİ
# %70 maliyet azalması
# %95 kalite korunması
# %80 Haiku'ya yönlendirilen
# %5  Opus gerektiren görev
