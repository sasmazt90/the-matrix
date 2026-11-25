# Kaynak yapıların değerlendirmesi

| Kaynakta görülen bölüm | Repoya taşınan sorumluluk | Uygulama kararı |
|---|---|---|
| Üst çalışma alanındaki orchestrator, registry ve proje kuralları | İş kabulü, öncelik, devir | Ana oturum yönlendirir. Üç uzman ayrı Claude Code tanımıdır. |
| agents/standard-agent ve örnek podcast agent’ı | Amaç, sınırlar, heartbeat, hafıza, skill | Standart agent şablonu korunur. İçerik üretimi örneğinin yerini ölçülebilir medya vakası alır. |
| knowledge, journal ve templates | Statik iş tanımı, ortak bulgu, görev ve haftalık değerlendirme | Referanslar sürümlenir. Yerel JSON bulgusu ve Markdown taslağı ayrı yazılır. |
| Ayrı operasyon projesinin kök kurulum ve otomasyon rehberi | Sahiplik, kurulum ve aktivasyon | README ilk çalışmayı tarif eder. Periyodik tetik üretimde ayrıca kurulur. |
| Operasyon projesindeki on kardeş iş akışı | Karar kaydı, lansman, yönetim raporu, ekip, hesap, olay, lokasyon, sözleşme, toplantı ve takip | Ortak desen: tetik → kapsamlı veri → doğrulama → sahibi belli taslak → insan kararı. Her fonksiyon için ayrı çalışan model gerekmez. |
| Ortak durum, normalizasyon, takip, log, taslak çıktıları | İş durumu, operasyon bulgusu ve onay kanıtının ayrı tutulması | Pacing demosunda tekrarlanabilir Journal ve taslak yazımı var. Canlıya geçişte kimlik, süre, onay sürümü ve geri alma doğrulanır. |
| Repodaki eğitim örnekleri | Bitiş ölçütü, hata protokolü, bağlam devri | Üç özgün referans ayrı klasörde. Kalan ders, kurulum ve video yayınlama örnekleri önceki commit üzerinden erişilebilir. |

Ekipte ortak motorun ve doğrulamanın bir sahibi vardır. Kanal uzmanı kendi rapor adaptörünü, iş akışını ve bilinen sonuçlu testini geliştirir. Üretim hesabı bağlamadan önce entegrasyon, yetkilendirme, hata geri kazanımı ve gerçekleşen model maliyetlerinin ölçümü ayrı doğrulanmalıdır. Bu çalışma alanında yalnız sentetik örnek ve genel rol tanımları yayımlanır.
