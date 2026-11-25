"""
AUTO_FIX_LOOP.PY
Slayt 69 — Otomatik Düzeltme Döngüsü (max 3 deneme, %87 başarı oranı)
"""


async def auto_fix_loop(task, max_retries: int = 3):
    attempt = 0
    last_error = None

    while attempt < max_retries:
        # 1. Üret
        output = await generate(task, last_error)

        # 2. Doğrula
        result = await verify(output)
        if result["passed"]:
            return output  # ✓ Başarılı

        # 3. Hata geri besleme
        last_error = result["issues"]
        attempt += 1

    # 4. Max deneme aşıldı → escalation
    return escalate_to_human(task, last_error)


# --- Yer tutucular ---


async def generate(task, last_error):
    """Üretici ajanı çağırın (anthropic / openai / vs.)."""
    raise NotImplementedError


async def verify(output):
    """Doğrulayıcı ajan — verifier_prompt.py'deki verify() ile değiştirilebilir."""
    raise NotImplementedError


def escalate_to_human(task, last_error):
    return {"status": "human_review_required", "task": task, "error": last_error}
