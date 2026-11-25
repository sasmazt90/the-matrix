# The Matrix
Yerel çalışan bir agent çalışma alanı. Kullanıcı Orchestrator ile konuşur. Hesapları kod yapar, uzmanlar gerektiğinde ayrı bağlamda kanıt inceler. Çalışan örnek, sentetik bir mobilite kampanyası için programmatic pacing ve bütçe testi taslağı üretir.

## Windows’ta ilk çalışma

Node.js 22 veya üstü ve PowerShell ile repo kökünde çalıştır. Paket kurulumu veya API anahtarı gerekmez.

```powershell
node tools/review.mjs examples/munich/input.json
node --test
```

Beklenen: 2.000 € plana karşı 2.200 € harcama. Retargeting +240 €, prospecting −40 €, toplam +%10. Kampanyanın medya sonrası katkısı 800 €. Mevcut deney kampanyada reklam açık/kapalı karşılaştırması. Retargeting’i %10 kısmanın kâra etkisi için çıktı `NEEDS_EVIDENCE` olur. Komut, JSON kanıt kaydı ve Markdown taslağının tam yollarını gösterir. Finance girdisini 3.000 €’dan 2.970 €’ya çekersen yeni kayıtta katkı 770 € olur.

## Claude Code ile uzman incelemesi

Projeyi Claude Code’da aç, önce yukarıdaki komutu çalıştır. Şöyle sor: **“Son komutun verdiği Journal dosyasını kullan. Measurement uzmanını çağır. Retargeting bütçesini %10 kısmak için yeterli kanıt var mı?”** Birden çok kayıt varsa kullanmak istediğin JSON yolunu belirt. Ayrı araç çağrısını incele. Yerel komut tek başına bir model çalıştırmaz. Claude oturumu ve erişimi ayrı gerekir.

| Nereden başlanır? | Ne içerir? |
|---|---|
| [Orchestrator](orchestrator/IDENTITY.md) ve [öncelikler](orchestrator/PRIORITIES.md) | Soru, kanıt gereksinimi, uzman seçimi, teslim ve devir |
| [Agent registry](AGENT_REGISTRY.md) ve [.claude/agents](.claude/agents) | Üç salt okunur uzman tanımı |
| [Knowledge](knowledge/METRICS.md) ve [ortak sözleşmeler](CONVENTIONS.md) | Onaylı tanımlar, Journal, kayıt kapsamı ve veri sahipliği |
| [İş akışı](.claude/skills/review-budget/SKILL.md) | Bütçe incelemesini tekrar etme prosedürü |
| [Yeni agent şablonu](agents/standard-agent/AGENT.md) ve [şablonlar](templates) | Agent tanımı, görev, Journal kaydı ve haftalık değerlendirme |
| [Kaynak yapıların değerlendirmesi](docs/architecture-review.md) | Hangi yapı neden alındı, ekip neyi devralır |
| [Testler](test/review.test.mjs) | Hesap, eksik veri, tekrar, eşzamanlı çalışma ve kaynak düzeltmesi |

Bu sürüm yerel bir referans uygulamadır. Üretim scheduler’ı, canlı reklam platformuna yazma, dağıtık işlem kuyruğu ve sağlayıcı maliyetlerinin otomatik toplanması sonraki entegrasyonlardır. Kaynak kurs malzemeleri [önceki Git sürümünde](https://github.com/sasmazt90/the-matrix/tree/7ea1745ce00509340f2eade862a33674749ebb9d) bulunur. Esad Kılıç’ın companion files içeriğinden üç kısa belge [kaynak notları](references/course) altında orijinal haliyle tutulur.
