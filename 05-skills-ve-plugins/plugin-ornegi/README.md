# @goatstarter/claude-code-plugin

Goatstarter ekibi için Claude Code skill, agent ve komut koleksiyonu.

## Kurulum

```bash
# Public npm (eğer yayınlandıysa)
claude plugins install @goatstarter/internal

# Yerel test
claude plugins install ./

# GitHub direct
claude plugins install gh:goatstarter/claude-code-plugin
```

## İçerik

### Skills (auto-trigger)
- `goat:commit-stili` — Conventional commits zorlayıcısı
- `goat:api-route-kurali` — Next.js API route pattern
- `goat:component-pattern` — React component konvansiyonları

### Agents (subagent)
- `goat:kod-incelemeci` — Senior code review (Opus 4.7)
- `goat:pr-ozetleyici` — PR açıklaması üretici

### Commands (slash)
- `/ship` — Test + build + commit + push + PR
- `/deploy [env]` — Vercel deploy (preview/prod)
- `/review [PR#]` — Multi-agent PR review

## Geliştirme

```bash
# Yerel kurulum (development mode)
claude plugins install --dev ./

# Skill'i test et
cd test-project && claude
# Skill'in tetiklendiğini gör

# Validate
claude plugins validate ./

# Yayınla (private)
npm publish --registry=https://npm.goatstarter.com
```

## Plugin Yapısı

```
plugin-ornegi/
├── plugin.json           # plugin manifest
├── package.json          # npm metadata
├── README.md             # bu dosya
├── skills/               # auto-trigger yetenekler
│   ├── commit-stili/
│   │   └── SKILL.md
│   └── api-route-kurali/
│       └── SKILL.md
├── agents/               # custom subagents
│   ├── kod-incelemeci.md
│   └── pr-ozetleyici.md
└── commands/             # slash commands
    ├── ship.md
    ├── deploy.md
    └── review.md
```

## Önemli

`SKILL.md`, `plugin.json`, `package.json` gibi dosya adları **standart konvansiyonlar**, değiştirilmemeli. Skill ve agent kimliği frontmatter'daki `name:` alanı ile belirlenir, dosya adından bağımsızdır.
