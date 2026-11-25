"""
WEEKLY REPORT PIPELINE
Slayt 99 — 10 Bölümün Sentezi

Tüm öğrendiklerimiz tek bir gerçek üretim sistemi:
- Cron schedule (B10) ile her Pazartesi 09:00
- MCP araçları (B4) ile Postgres + GitHub + Slack + Notion
- Paralel subagent'lar (B6+B7) ile veri toplama
- Konsensüs sentezi (B7) ile birleştirme
- Doğrulayıcı ajan (B8) ile rakam kontrolü
- Prompt caching (B9) ile %90 maliyet tasarrufu
- Model routing (B10) ile akıllı seçim

Yıllık değer: ~250 saat geri kazanım, $2/hafta maliyet.
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass

import anthropic


# ----------------------------------------------------------------------------
# Konfigürasyon
# ----------------------------------------------------------------------------
client = anthropic.AsyncAnthropic()

# Cache'lenecek sabit içerikler (sistem promptu, rapor şablonu)
SYSTEM_PROMPT = """
Sen Goatstarter'ın senior data analyst'isin. Görevin:
- Şirket metriklerini analiz etmek
- Anomalileri tespit etmek
- Aksiyon önerileri üretmek
- Türkçe, kısa, net rapor yazmak

Stilrei rehberi:
- Em dash (—) kullanma
- Emoji kullanma
- Madde madde, kısa cümleler
- Sayılar somut, kaynak belirtilmiş

Output formatı: Markdown, başlıklarla, tablolarla.
"""

REPORT_TEMPLATE = """
## Haftalık Rapor — {week_start} ile {week_end} arası

### 📊 Üst Düzey Metrikler
[buraya gelir]

### 🚨 Dikkat Gereken 3 Madde
[buraya gelir]

### 💡 Bu Hafta Önerisi
[buraya gelir]
"""


# ----------------------------------------------------------------------------
# 1. PARALEL VERİ TOPLAMA (Subagents pattern)
# ----------------------------------------------------------------------------
async def fetch_revenue_data() -> dict:
    """Postgres MCP ile geçen haftanın revenue verileri."""
    # Gerçek implementasyonda MCP tool çağrısı
    # Örnek için mock data
    return {
        "total_revenue": 47200,
        "vs_last_week_pct": 12.4,
        "new_customers": 28,
        "churn_count": 3,
        "top_product": "DOA Community ($49/ay)",
    }


async def fetch_engineering_data() -> dict:
    """GitHub MCP ile son 7 günün dev verileri."""
    return {
        "merged_prs": 14,
        "open_prs": 6,
        "open_issues_p0": 2,
        "open_issues_p1": 8,
        "deploys": 9,
        "deploy_failures": 1,
    }


async def fetch_marketing_data() -> dict:
    """Notion MCP ile pazarlama metrikleri."""
    return {
        "campaigns_active": 4,
        "total_impressions": 234000,
        "ctr_pct": 3.2,
        "conversions": 89,
        "cac_usd": 12.50,
    }


# ----------------------------------------------------------------------------
# 2. KONSENSÜS SENTEZİ (Multi-agent pattern)
# ----------------------------------------------------------------------------
async def synthesize_report(revenue, engineering, marketing) -> str:
    """3 farklı veri kaynağını sentezleyen rapor üret."""

    raw_data = json.dumps(
        {"revenue": revenue, "engineering": engineering, "marketing": marketing},
        indent=2,
        ensure_ascii=False,
    )

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=[
            # Cache edilen sabit sistem promptu (%90 indirim)
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            },
            # Cache edilen rapor şablonu
            {
                "type": "text",
                "text": f"Rapor şablonu:\n{REPORT_TEMPLATE}",
                "cache_control": {"type": "ephemeral"},
            },
        ],
        messages=[
            {
                "role": "user",
                "content": f"""
Aşağıdaki haftalık verilerden Türkçe, üst düzey, eyleme yönelik bir rapor üret.

Veriler:
{raw_data}

Format: Yukarıdaki şablon. Sayıları somut tut, vs hafta öncesi karşılaştır.
""",
            }
        ],
    )
    return response.content[0].text


# ----------------------------------------------------------------------------
# 3. DOĞRULAMA (Validation pattern)
# ----------------------------------------------------------------------------
async def verify_report(report: str, raw_data: dict) -> dict:
    """Verifier agent: rapordaki rakamlar veriyle uyumlu mu?"""

    response = await client.messages.create(
        model="claude-haiku-4-5",  # Verifier ucuz model
        max_tokens=500,
        system="Sen bir doğrulayıcı ajansın. Görevin: rapordaki sayıların kaynak verilerle uyumlu olup olmadığını kontrol et. JSON döndür: {passed: bool, issues: [...]}",
        messages=[
            {
                "role": "user",
                "content": f"""
Rapor:
{report}

Kaynak veri:
{json.dumps(raw_data, ensure_ascii=False, indent=2)}

Kontrol et: rapordaki her sayı kaynak veride var mı? Tutarsızlık varsa raporla.
JSON formatında döndür.
""",
            }
        ],
    )

    text = response.content[0].text
    # JSON parse (defensive)
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"passed": False, "issues": ["verifier output not parseable"]}


# ----------------------------------------------------------------------------
# 4. ÇIKTI: SLACK + NOTION + EMAIL
# ----------------------------------------------------------------------------
async def deliver_report(report: str):
    """Rapor onaylanırsa Slack, Notion, email'e gönder."""
    # Slack MCP
    print("📤 Slack #leadership kanalına gönderiliyor...")
    # Notion MCP: yeni sayfa oluştur
    print("📝 Notion'da haftalık rapor sayfası oluşturuluyor...")
    # Email
    print("📧 Yöneticilere email gönderiliyor...")


# ----------------------------------------------------------------------------
# 5. ANA PIPELINE
# ----------------------------------------------------------------------------
async def main():
    print(f"🚀 Weekly Report Pipeline başlıyor — {datetime.now().isoformat()}")

    # 1. Paralel veri toplama
    print("\n[1/4] Paralel veri toplama...")
    revenue, engineering, marketing = await asyncio.gather(
        fetch_revenue_data(),
        fetch_engineering_data(),
        fetch_marketing_data(),
    )
    print("  ✓ Revenue, Engineering, Marketing verileri alındı")

    # 2. Sentez
    print("\n[2/4] Sentezleyen ajan çalışıyor (Sonnet, prompt cache aktif)...")
    report = await synthesize_report(revenue, engineering, marketing)
    print(f"  ✓ Rapor üretildi ({len(report)} karakter)")

    # 3. Doğrulama
    print("\n[3/4] Doğrulayıcı ajan kontrol ediyor (Haiku)...")
    raw_data = {"revenue": revenue, "engineering": engineering, "marketing": marketing}
    verification = await verify_report(report, raw_data)

    if not verification["passed"]:
        print(f"  ✗ Doğrulama başarısız: {verification['issues']}")
        # İnsan onayına gönder
        print("  → Slack #ai-alerts kanalına escalation gönderildi")
        return

    print("  ✓ Doğrulama geçti")

    # 4. Teslim
    print("\n[4/4] Rapor teslim ediliyor...")
    await deliver_report(report)
    print("  ✓ Tamamlandı")

    # Maliyet özeti
    print("\n💰 Tahmini maliyet: ~$0.05 (cache aktif)")
    print(f"⏱  Toplam süre: ~30 saniye")
    print("✅ Pipeline tamamlandı")


if __name__ == "__main__":
    asyncio.run(main())
