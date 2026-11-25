# MCP GÜVENLİK KONTROL LİSTESİ
## Slayt 34

## ✗ GÜVENSİZ

```
GITHUB_TOKEN="ghp_abc123"   # hardcoded
scope: ["*"]                # tam erişim
Production DB'ye direkt bağlantı
Araç çağrıları loglanmıyor
```

## ✓ GÜVENLİ

```
GITHUB_TOKEN="${env:GITHUB_TOKEN}"
scope: ["repo:read", "issues:write"]
Read-only replica kullan
Her araç çağrısı audit log'a yazılır
```

## Deploy Öncesi Kontrol Listesi

- [ ] API anahtarları ortam değişkenlerinde mi?
- [ ] Scope'lar minimum gerekli izinlerle mi sınırlı?
- [ ] Araç çağrıları loglanıyor ve izleniyor mu?
- [ ] Staging ortamında test edildi mi?
- [ ] Hata senaryoları test edildi mi?
