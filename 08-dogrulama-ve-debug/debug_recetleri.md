# Debugging Recipes — Yaygın Bug → Reçete

Ajan beklenmedik davrandığında **sistematik debugging**. Bu tabloyu yer imi yapın.

## Belirti → Olası Neden → Reçete

| Belirti | Olası Neden | Reçete |
|---|---|---|
| 🔴 Sonsuz döngü, aynı işi 5+ kez yaptı | DoD belirsiz veya hata mesajını yanlış yorumluyor | `/clear` + DoD'a explicit "STOP after 3 attempts" ekle |
| 🔴 Yanlış dosyayı düzenliyor | Path resolution, benzer isimli dosyalar | Prompt'ta tam path: `app/api/users/route.ts` (tam belirt) |
| 🔴 "İyileştirdim" diyor ama hiçbir şey değişmemiş | Edit tool old_string yanlış, eşleşme yok, sessiz fail | Hooks: PostToolUse'a `git diff` log ekle |
| 🔴 Tek görev $3+ tüketti | Context şişti, .claudeignore yok, gereksiz dosya okuyor | `.claudeignore` ekle, `/compact`, model routing |
| 🔴 Plan Mode'da bile kararsız | CLAUDE.md çelişkili kurallar içeriyor | CLAUDE.md'yi review et, "yapma" listeleri arasında çelişki var mı? |
| 🔴 Halüsinasyon: var olmayan fonksiyon çağırıyor | Eski model bilgisi, kütüphane sürümü değişmiş | "Önce `node_modules`'da gerçek API'yi oku" diye prompt'a ekle |
| 🔴 Erken duruyor, "tamam" diyor | DoD test çalıştırmayı içermiyor | DoD'a "`pnpm test` output ekran çıktısı paylaş" ekle |
| 🔴 Hooks tetiklenmiyor | matcher pattern yanlış, JSON syntax hatası | `claude --debug` ile başlat, hook log'larını izle |
| 🔴 MCP tool çağrısında 401/403 | Token expired, scope yetersiz | `/mcp [server] reauthenticate`, scope'ları kontrol et |
| 🔴 Subagent ana ajandan veri görmüyor | Subagent'lar context paylaşmaz | Prompt'u self-contained yap, gerekli bilgiyi prompt içine koy |
| 🔴 Edit "old_string not found" hatası veriyor | Whitespace, tab vs space farkı | Daha küçük, unique bir bölgeye odaklan; replace_all kullan dikkatli |
| 🔴 Git commit hook tarafından bloklandı | Pre-commit hook fail | Hook çıktısını oku, ELLE düzelt (`--no-verify` kullanma) |
| 🔴 Ajan bash komutu için "permission denied" diyor | settings.json `deny` kuralı eşleşti | `settings.local.json`'a explicit allow ekle (gerçekten güvenliyse) |
| 🔴 Aynı prompt farklı sonuç veriyor | Temperature yüksek + bağlam değişiyor | Deterministik istiyorsan `temperature=0`, prompt cache kullan |

## Debug Komutları

### Token kullanımı
```
/cost
```
Bu konuşmaya kadar kaç token harcandı, hangi modele.

### Conversation log
```
/save debug-session.md
```
Tüm konuşma geçmişini markdown dosyasına yaz, ne sırada ne yapıldı oku.

### Plan Mode'a geç
```
Shift+Tab
```
Edit/Write/Bash bloklanır, model planı yazar, sen onayla.

### Verbose mode
```bash
claude --debug
```
Tool çağrıları, hook'lar, MCP iletişimi loglanır. Ne tetiklendi ne tetiklenmedi.

### Subagent ile izole
```
Agent({
  subagent_type: "general-purpose",
  prompt: "Buradaki sorunu izole şekilde analiz et: [self-contained context]"
})
```
Ana ajan kafayı yedi mi? Subagent'a fresh context ile sor.

## Sıfırlama Protokolü

Çıkmaz sokakta isen:

1. **Mevcut durumu kaydet**: "Şu ana kadar ne yapıldı, ne çalışmadı, neden? CLAUDE.md'ye 'Lessons' başlığı altında yaz."
2. **Geçici değişiklikleri geri al**: `git stash` veya `git checkout .`
3. **Bağlamı temizle**: `/clear`
4. **CLAUDE.md'yi review et**: Az önce eklediğin "Lessons"ı oku
5. **Plan Mode + Daha küçük scope**: Görevi parçala, ilk parçayı ver

> **Sunk cost tuzağı:** 30 dakika kaybettin diye 2 saat daha kaybetme. Sıfırla, daha temiz başla.

## Debug Oturumu Şablonu

```
[Adım 1] Token tüketimini kontrol et → /cost
[Adım 2] Conversation log → /save debug.md
[Adım 3] Root cause ara — log'ta tekrar eden patterns var mı?
[Adım 4] CLAUDE.md'ye "Lessons" ekle (gelecek için)
[Adım 5] git stash + /clear
[Adım 6] Plan Mode (Shift+Tab) ile yeniden başlat
[Adım 7] Görevi 2-3 alt göreve böl, ilkini ver
```

## Hata Mesajı Yorumlama

### "Tool call rejected"
Ajan kullanmaya çalıştığı tool denied veya ask edildi. settings'de allow listesini kontrol et.

### "Context window exceeded"
Bağlam doldu. `/compact` veya `/clear` + CLAUDE.md ile yeniden başla.

### "Rate limit exceeded"
API rate limit'ine ulaşıldı. 1-2 dakika bekle, sonra devam et. Sürekli oluyorsa: tier upgrade.

### "Model overloaded"
Anthropic tarafında geçici yoğunluk. 30 sn bekle, retry.

### "Hook returned non-zero"
PreToolUse hook tool'u blokladı. Hook çıktısını oku, kuralı anla. Gerçekten gereksizse hook'u geçici devre dışı bırak (hook dosyasında).
