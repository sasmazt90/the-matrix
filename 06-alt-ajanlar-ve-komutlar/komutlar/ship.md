---
description: "Bir feature'ı production-ready yap: test, build, commit, push, PR aç"
---

# /ship

Tamamlanmış bir feature'ı production'a hazır hale getirir: kalite kontrol, commit, push, PR.

## Adımlar

Şu adımları **sırasıyla** yap:

### 1. Mevcut durumu gör
```bash
git status
```

Eğer hiç değişiklik yoksa: dur, "Hiç değişiklik yok, ship edilecek bir şey yok" de.

### 2. Test'leri çalıştır
```bash
pnpm test
```

Başarısız test varsa: dur, çıktıyı göster, kullanıcıdan ne yapacağını sor.

### 3. Type check
```bash
pnpm tsc --noEmit
```

Hata varsa: dur, listele, düzeltme öner ama otomatik düzeltme.

### 4. Lint
```bash
pnpm lint
```

Hata varsa: `pnpm lint --fix` dene, kalan hataları kullanıcıya raporla.

### 5. Build
```bash
pnpm build
```

Build başarısız: dur ve raporla.

### 6. Hepsi temizse: commit
- `git diff --staged` ile değişiklikleri özetle
- Conventional Commits formatında (commit-style skill aktive olur) commit mesajı yaz
- Kullanıcıya göster, onay iste
- Onaylanırsa: `git commit -m "..."`

### 7. Push
```bash
git push -u origin HEAD
```

### 8. PR aç
```bash
gh pr create --title "..." --body "..." --label "ready-for-review"
```

PR body şu yapıda olmalı:
```markdown
## Summary
[1-3 cümle değişiklik özeti]

## Changes
- [Madde 1]
- [Madde 2]

## Test plan
- [ ] Manuel test 1
- [ ] Manuel test 2
- [ ] Edge case test
```

### 9. Tamamla
- PR URL'sini göster
- Sonraki adım: kim review edecek?

## Don't

- ❌ Test başarısızken push etme
- ❌ `--no-verify` ile commit hooks bypass etme
- ❌ `--force` push etme
- ❌ Sensitive bilgi içeren commit mesajı yazma
- ❌ "WIP", "fix stuff" gibi belirsiz commit mesajları

## Hata durumunda

Herhangi bir adımda başarısız olursa:
1. **DUR** (sonraki adımlara geçme)
2. Hata çıktısını göster
3. Olası çözümü öner
4. Kullanıcının kararını bekle (otomatik düzeltme yapma)
