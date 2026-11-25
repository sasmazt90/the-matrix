---
description: "Vercel'e deploy et. Argüman: prod | preview (default: preview)"
---

# /deploy

Mevcut branch'i Vercel'e deploy eder. Preview varsayılan, `prod` argümanı ile production.

## Kullanım

```
/deploy             # preview
/deploy prod        # production
/deploy production  # production (alternatif)
```

`$1` = environment (preview / prod / production)

## Adımlar

### 1. Pre-flight check

Önce şunları kontrol et:

```bash
# Working tree temiz mi?
git status

# Hangi branch'teyiz?
git branch --show-current
```

Eğer:
- Working tree kirli ise: dur, "Önce commit et" de
- `prod` deploy isteniyor ama branch `main`/`master` değilse: kullanıcıya **özellikle** sor

### 2. Test ve build

```bash
pnpm test
pnpm tsc --noEmit
pnpm build
```

Herhangi biri başarısız: dur, deploy etme.

### 3. Deploy

#### Preview deploy
```bash
vercel
```

Çıktıdan preview URL'yi al ve göster.

#### Production deploy
```bash
# ÖNEMLİ: prod deploy için ekstra onay gerekir
vercel --prod
```

**Production deploy öncesi insan onayı zorunlu.**

### 4. Smoke test

Deploy bittikten sonra:
1. URL'ye `curl -I` at, 200 dönmeli
2. Health check endpoint varsa: `curl URL/api/health`
3. Sentry/Logflare'de yeni error var mı kontrol et (varsa MCP)

### 5. Rapor

```
✓ Deploy tamamlandı
  Environment: [preview | production]
  URL: https://...
  Commit: abc1234
  Build süresi: Xs
  Bundle size: X KB
```

Ekstra:
- Production ise: Slack #deploys kanalına bildirim gönder (varsa Slack MCP)
- Preview ise: PR yorumuna URL ekle (varsa GitHub MCP)

## Don't

- ❌ Test geçmeden deploy etme
- ❌ Working tree kirli iken prod deploy etme
- ❌ Production deploy'a açık onay olmadan başlama
- ❌ `--force` veya `--yes` kullanarak doğrulama atla
- ❌ Failed deploy'u görmezden gel (rollback öner)

## Rollback

Production deploy sonrası problem fark edilirse:
```bash
vercel rollback
```

veya Vercel dashboard'tan önceki deployment'ı promote et.
