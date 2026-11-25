# Claude Code Ustalığı 2026 — Companion Files

YouTube videosunda gösterilen sunumun tüm kod örneklerini, şablonlarını ve yapılandırma dosyalarını bu klasörde bulabilirsiniz. Her dosya **kopyala-yapıştır kullanıma hazır**.

> Sunum dosyası: `../index.html` (tarayıcıda açın, T tuşu ile içindekiler).

## Bölüm Haritası

| Bölüm | Klasör | İçerik |
|---|---|---|
| 01 | `01-ajan-dongusu/` | Tamamlanma tanımı, ajan muhakeme log örneği |
| 02 | `02-kurulum/` | CLAUDE.md, settings.json, .gitignore, kurulum scriptleri |
| 03 | `03-prompt-teknikleri/` | Sistem promptu, ajan sözleşmesi, hata protokolü, çıktı şeması |
| 04 | `04-mcp/` | .mcp.json örnekleri, FastMCP ile özel sunucu, güvenlik kontrol listesi |
| 05 | `05-skills-ve-plugins/` | SKILL.md şablonu, örnek skill'ler, plugin yapısı |
| 06 | `06-alt-ajanlar-ve-komutlar/` | Custom agent şablonu, slash komut şablonları |
| 07 | `07-cok-ajanli-sistemler/` | Paralel ajanlar, meta-sentez, sohbet odası |
| 08 | `08-dogrulama-ve-debug/` | Doğrulayıcı, güvenlik tarayıcısı, hook'lar, debug reçeteleri |
| 09 | `09-baglam-yonetimi/` | .claudeignore, /compact stratejisi |
| 10 | `10-uretim/` | Görev yönlendirici, batch API, maliyet izleyici, tam pipeline |
| ⚡ | `bonus-video-pipeline/` | Bonus: YouTube videodan otomatik aksiyon çıkarma |

## Hızlı Başlangıç

```bash
# 1. Bağımlılıkları kur
pip install anthropic mcp fastmcp python-dotenv requests

# 2. .env dosyasını oluştur
cp 02-kurulum/.env.ornek .env
# → ANTHROPIC_API_KEY ekle

# 3. Bir örnek çalıştır
python 07-cok-ajanli-sistemler/paralel_ajanlar.py
```

## Model Sürümleri

Tüm örnekler **2026 itibarıyla güncel** modelleri kullanır:

- `claude-opus-4-7` — En güçlü, kritik kararlar (1M context mevcut)
- `claude-sonnet-4-6` — Dengeli, çoğu görev için ideal
- `claude-haiku-4-5` — Hızlı ve ucuz, basit görevler

## Kullanım Notları

- **Eğitim amaçlı.** Production'a almadan önce hata yönetimi ve güvenlik kontrollerini ekleyin.
- `.env`, `*.key` ve hassas dosyalar **asla** git'e commit edilmemeli.
- API anahtarları için her zaman `os.environ` veya `.env` kullanın.
- Permission rules için `02-kurulum/settings.local.json.ornek` dosyasını referans alın.

## Klasör Yapısı

```
companion-files/
├── README.md                                  # bu dosya
├── 01-ajan-dongusu/
│   ├── ajan_muhakeme_log.txt                  # gerçek bir oturum log'u
│   └── tamamlanma_tanimi.md                   # Definition of Done şablonu
├── 02-kurulum/
│   ├── .env.ornek                             # env değişken şablonu
│   ├── .gitignore                             # zorunlu .gitignore eklemeleri
│   ├── CLAUDE.md.sablon                       # proje anayasası şablonu
│   ├── kurulum.sh                             # Claude Code kurulum scripti
│   ├── ortam_yukleme_ornegi.py                # .env yükleme örneği
│   ├── ilk_gorev.md                           # ilk ajan görevi şablonu
│   └── settings.local.json.ornek              # güvenli permission örneği
├── 03-prompt-teknikleri/
│   ├── ajan_sozlesmesi.md
│   ├── cikti_semasi.json
│   ├── hata_protokolu.md
│   ├── kendini_guncelleyen.py
│   ├── sistem_promptu.md
│   └── ters_prompting_dialog.md
├── 04-mcp/
│   ├── benim_mcp_sunucum.py                   # FastMCP ile özel sunucu
│   ├── guvenlik_kontrol_listesi.md
│   ├── mcp_json_ornegi.json                   # 5 popüler sunucu örneği
│   └── ozel_mcp_sunucusu.py
├── 05-skills-ve-plugins/
│   ├── SKILL.md.sablon
│   ├── ornek-skills/
│   │   ├── commit-stili/                      # Conventional commits zorlayıcısı
│   │   └── api-route-kurali/                  # Next.js API route pattern
│   └── plugin-ornegi/                         # Tam plugin yapısı
├── 06-alt-ajanlar-ve-komutlar/
│   ├── ajanlar/
│   │   ├── ajan.md.sablon
│   │   ├── kod-incelemeci.md
│   │   └── guvenlik-denetcisi.md
│   └── komutlar/
│       ├── komut.md.sablon
│       ├── ship.md
│       ├── review.md
│       └── deploy.md
├── 07-cok-ajanli-sistemler/
│   ├── paralel_ajanlar.py
│   ├── meta_sentez.py
│   ├── sohbet_odasi.py
│   ├── ajan_rolleri.py
│   └── moderator_promptu.py
├── 08-dogrulama-ve-debug/
│   ├── otomatik_duzeltme_dongusu.py
│   ├── escalation_bildirici.py
│   ├── halusinasyon_ornegi.py
│   ├── guvenlik_tarayicisi.py
│   ├── dogrulayici_promptu.py
│   ├── hook-ornekleri/
│   │   ├── settings.json.ornek                # 3 hook konfigürasyonu
│   │   ├── secret-kontrol.sh
│   │   ├── durduginda-bildir.sh
│   │   └── otomatik-format.sh
│   └── debug_recetleri.md                     # Yaygın bug → reçete tablosu
├── 09-baglam-yonetimi/
│   ├── .claudeignore                          # production-ready ignore
│   ├── clear_oncesi_akis.md
│   └── compact_kullanim.md
├── 10-uretim/
│   ├── batch_isleyici.py
│   ├── maliyet_izleyici.py
│   ├── prompt_cache_ornegi.py
│   ├── gorev_yonlendirici.py
│   └── haftalik_rapor_pipeline.py             # 10 bölümün sentezi
└── bonus-video-pipeline/                      # YouTube → eylem otomasyonu
    ├── kareli_analiz.py
    ├── cikarma_promptu.md
    ├── toplanti_jira_otomasyonu.py
    ├── transkript_indir.sh
    └── video_analizci.py
```

## Önemli Notlar — Korunan İngilizce İsimler

Aşağıdaki dosya/klasör adları **Claude Code'un kendisi tarafından okunan teknik dosyalar**dır, isimleri değiştirilmemeli:

- `CLAUDE.md` (proje anayasası, Claude Code otomatik okur)
- `.mcp.json` (MCP sunucu konfigürasyonu)
- `.claudeignore` (gitignore benzeri ignore listesi)
- `.gitignore` (Git ignore)
- `.env`, `.env.local` (environment standardı)
- `settings.json`, `settings.local.json` (Claude Code settings)
- `SKILL.md` (skill manifesto)
- `plugin.json`, `package.json` (npm/plugin standardı)
- `README.md` (genel konvansiyon)

Slash command isimleri (`/ship`, `/review`, `/deploy`) ve subagent isimleri (örn. `kod-incelemeci`, `guvenlik-denetcisi`) ise **frontmatter'daki `name:` alanı** ile tanımlanır, dosya adından bağımsızdır.

## Lisans

Eğitim materyali. Kişisel ve ticari kullanımda serbest. Atıf güzel olur ama zorunlu değil.

— Esad Kılıç · Goatstarter Ventures · 2026
