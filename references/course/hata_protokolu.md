# HATA_PROTOKOLU.MD
## Slayt 25 — Hata Yönetimi Stratejileri

## HATA YÖNETİMİ PROTOKOLÜ

### KATMAN 1: YENİDEN DENEME
- Bir araç çağrısı başarısız olursa:
  1. Hata mesajını analiz et
  2. Farklı parametrelerle tekrar dene
  3. Maksimum 3 deneme

### KATMAN 2: ALTERNATİF YOL
- 3 denemeden sonra:
  → Daha basit bir yaklaşım dene
  → Kısmi çözüm üret ve belgele
  → Alternatif araç kullan

### KATMAN 3: TIRMANDIRMA
- Fallback da başarısız olursa:
  → DUR (devam etme)
  → Hata raporunu yaz
  → "İNSAN_GEREKLİ: [açıklama]" yaz

⚠ Asla tahmin etme — belirsizlikte dur ve sor.
