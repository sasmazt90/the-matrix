"""
PARALEL AJAN İLE KONSENSÜS
Slayt 50 — Paralel Ajan Başlatma (asyncio.gather)
"""
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()


async def single_run(prompt: str, run_id: int) -> str:
    response = await client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        temperature=0.9,  # Yüksek çeşitlilik
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


async def consensus_run(prompt: str, n: int = 5) -> list:
    # N ajanı aynı anda başlat
    tasks = [single_run(prompt, i) for i in range(n)]
    results = await asyncio.gather(*tasks)
    return list(results)


# Kullanım: 5 paralel çalıştırma, ~2 saniye
if __name__ == "__main__":
    outputs = asyncio.run(
        consensus_run("Bu Python kodundaki en kritik güvenlik açığı nedir?", n=5)
    )
    for i, out in enumerate(outputs, 1):
        print(f"\n[Çalıştırma {i}]\n{out}")
