# EXTRACTION_PROMPT.MD
## Slayt 43 — Adım Çıkarma Teknikleri

Bu videoyu analiz et ve şu JSON'u üret:

```json
{
  "baslik": "string",
  "adimlar": [{
    "num":       "integer",
    "zaman":     "MM:SS",
    "aciklama":  "string",
    "kod":       "string | null",
    "bagimlilik": ["integer"],
    "kosul":     "string | null"
  }],
  "gereksinimler": ["string"],
  "sure_dakika": "integer"
}
```

**Kurallar:**
- Sadece videoda görülen bilgileri kullan
- Tahmin etme — emin değilsen `null` bırak

> "Zaman damgası + bağımlılık haritası = otomatik proje planı.
> Toplantı kaydından Gantt şeması."
