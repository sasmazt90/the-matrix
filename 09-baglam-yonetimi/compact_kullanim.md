# /compact KOMUTU
## Slayt 76

## Terminalde Kullanım

```bash
# Basit kullanım
/compact

# Özelleştirilmiş — neyin korunacağını belirt
/compact Şunları mutlaka koru:
1. Kullandığımız tech stack (Next.js + Supabase)
2. API endpoint yapısı
3. Tamamlanan özellikler listesi
4. Bekleyen görevler

# Otomatik compact — her 30 mesajda
claude --auto-compact 30
```

## /compact ne korur, ne kaybeder?

| ✓ KORUNAN | ✗ KAYBOLAN |
|---|---|
| Mimari kararlar | Detaylı tartışmalar |
| Mevcut proje durumu | Hata geçmişi |
| Önemli kısıtlamalar | Deneme yanılma süreci |
| Tamamlanan görevler | Ara adımlar |

## Önce / Sonra (token)

| Önce | Sonra |
|---|---|
| 85K token (50 mesaj geçmişi) | 8K token (sıkıştırılmış özet) → %90 tasarruf |
