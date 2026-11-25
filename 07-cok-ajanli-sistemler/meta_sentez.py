"""
META_SYNTHESIS.PY
Slayt 51 — Sentez: Çıktıları Birleştirme (Meta-Sentez Stratejisi)
"""
from parallel_agents import single_run


async def synthesize(outputs: list[str]) -> str:
    # Tüm çıktıları formatla
    formatted = "\n\n".join(
        [f"[Ajan {i+1}]: {out}" for i, out in enumerate(outputs)]
    )

    # 4. ajan ile sentez yap
    synthesis_prompt = f"""
Aşağıdaki {len(outputs)} farklı ajan çıktısını analiz et.
Ortak noktaları, farklılıkları ve en güvenilir
sonucu belirleyerek tek bir nihai cevap üret:

{formatted}
"""
    result = await single_run(synthesis_prompt, "meta")
    return result
