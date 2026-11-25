---
description: "PR için multi-agent review. Argüman: PR numarası"
---

# /review

Belirtilen PR için kapsamlı, çok ajanlı review yapar: kod kalitesi + güvenlik + test coverage.

## Kullanım

```
/review 123
```

`$1` = PR numarası (zorunlu)

## Adımlar

### 1. PR bilgisini al
```bash
gh pr view $1 --json title,body,files,author,baseRefName
```

PR yoksa veya kapalıysa: dur, raporla.

### 2. Diff'i incele
```bash
gh pr diff $1
```

### 3. Paralel subagent'ları başlat

**TEK MESAJDA, çoklu Agent tool çağrısı yap:**

```python
# Agent 1: Code review
Agent({
  description: "PR #$1 code review",
  subagent_type: "code-reviewer",
  prompt: """PR #$1 diff'ini incele:
    [diff buraya]

    Correctness, performance, maintainability açısından review yap.
    JSON formatında findings döndür."""
})

# Agent 2: Security audit
Agent({
  description: "PR #$1 security audit",
  subagent_type: "security-auditor",
  prompt: """PR #$1 diff'ini incele:
    [diff buraya]

    OWASP Top 10 ve secrets açısından tara.
    JSON formatında findings döndür."""
})
```

### 4. Sonuçları sentezle

İki agent'ın çıktılarını birleştir:
- Kritik bulgular ("critical" severity) en üstte
- High → Medium → Low sırasıyla
- Kategoriye göre grupla
- Tekrar eden bulguları birleştir

### 5. GitHub'a yorum yaz

```bash
gh pr comment $1 --body "$(cat <<'EOF'
## 🤖 Multi-Agent Review

[Genel özet]

### 🔴 Critical findings
- [Finding 1]

### 🟠 High
- [Finding 1]

### 🟡 Medium
- [Finding 1]

### 🟢 Highlights
- [İyi yönler]

---
*Review by code-reviewer + security-auditor agents*
EOF
)"
```

### 6. Review status

- Critical findings varsa: `gh pr review $1 --request-changes --body "..."`
- High findings varsa: `gh pr review $1 --comment --body "..."`
- Sadece low/info: `gh pr review $1 --approve --body "..."`

## Don't

- ❌ Subagent'ları ardışık çağırma (paralel olsun)
- ❌ Bulgular tekrarlanmışsa iki kez listele
- ❌ Sadece "looks good" yazıp geç (her bulgu somut olmalı)
- ❌ Otomatik approve etme — kullanıcıya sor
- ❌ Sensitive PR bilgisini başka kanala aktarma
