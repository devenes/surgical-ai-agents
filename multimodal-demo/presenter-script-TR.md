# Sunucu Metni: 5 Dakikalık Multimodal Gösterim (Presenter Script)

- **Bölüm**: Çalıştay Bölüm 4 (Dakika 25:00 – 30:00)
- **Sunucu Amacı**: Gemini 3.8 Flash modelinin temel görme-dil yeteneklerini katı tanı koymayan güvenlik sınırları içinde sergilemek.
- **Yüzey**: Agent Studio Chat / Freeform (veya Vertex AI Studio Multimodal Prompt)

---

## Senaryolaştırılmış Akış

### Dakika 25:00 – 26:00: Bağlamsal Kurulum
- **Sunucu Eylemleri**:
  1. Agent Studio Agent Designer tuvalini Tarayıcı Sekmesi 1'de açık bırakın.
  2. Tarayıcı Sekmesi 2'ye geçin: **Agent Studio Chat / Freeform**.
  3. Model seçicisinin **`gemini-3.8-flash`** olarak ayarlandığından emin olun.
- **Sunucu Konuşması**:
  > *"Bugün şu ana kadar çoklu agent araştırma koordinatörümüz tamamen metin tabanlı çalıştı. Bu bilinçli bir mimari tercihti: Metin ve yapılandırılmış JSON bize deterministik ve denetlenebilir kanıt özetleri sağlar.*
  > 
  > *Bununla birlikte cerrahi temelde görsel bir uzmanlıktır. Laparoskopik videoları, floroskopiyi ve BT taramalarını inceleriz. Gemini 3.8 Flash gibi modern multimodal temel modellere cerrahi görüntüler sunduğumuzda ne olur?*
  > 
  > *Şimdi görelim. Bu ayrı Freeform penceresinde, laparoskopik bir ameliyat sahasının şematik bir çizimini yükleyeceğim."*

---

### Dakika 26:00 – 27:30: Aşama 1 — Nötr Görsel Gözlem
- **Sunucu Eylemleri**:
  1. **Attach Image** simgesine (+ veya ataç) tıklayın.
  2. `multimodal-demo/assets/miliary-tuberculosis-5.jpeg` dosyasını seçin.
  3. `multimodal-demo/prompt.md` içindeki Prompt 1'i yapıştırın:
     ```text
     Describe only the observable visual features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
     ```
  4. **Run** / Send butonuna tıklayın.
- **Sunucu Konuşması**:
  > *"Prompt'umdaki güvenlik bariyerine dikkat edin: Tanı koymayı veya klinik karar vermeyi açıkça yasaklıyorum. Modelden yalnızca nötr bir görsel envanter istiyoruz.*
  > 
  > *Yanıta bakın: Gemini temel görsel varlıkları tanımlıyor — organ hatları, kanala benzer boru yapılar, tutucu alet ve diseke edilmiş anatomik plan. Safra kesesinin iltihaplı olup olmadığına veya kesmenin güvenli olup olmadığına dair aceleci sonuçlara varmadan bunları objektif bir şekilde tanımlıyor."*

---

### Dakika 27:30 – 29:00: Aşama 2 — Akademik Bilişim Takibi
- **Sunucu Eylemleri**:
  1. Aynı sohbet oturumunda, `multimodal-demo/prompt.md` içindeki Prompt 2'yi yapıştırın:
     ```text
     Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
     ```
  2. **Run** / Send butonuna tıklayın.
- **Sunucu Konuşması**:
  > *"Şimdi bu görsel gözlemi akademik bir araştırma sorusuna dönüştürüyoruz. Gemini'ın bu görsel özellikleri doğrudan gerçek cerrahi veri bilimi zorluklarına nasıl eşlediğine bakın:*
  > *1. Anlamsal segmentasyon: Algoritmaları anatomik sınırları çizecek şekilde eğitmek.*
  > *2. Laparoskopik kolesistektomide Critical View of Safety (CVS) kriterlerinin doğrulanması.*
  > *3. Alet takibi ve ameliyat aşaması tespiti.*
  > 
  > *Gemini'ın bu bilgisayarlı görü sistemlerinin bir ameliyathanede değerlendirilebilmesi için öncelikle DECIDE-AI gibi standartlar altında doğrulanması gerektiğini hatırlattığına da dikkat edin."*

---

### Dakika 29:00 – 30:00: Katılımcı Egzersizine Geçiş
- **Sunucu Eylemleri**:
  1. Tekrar Tarayıcı Sekmesi 1'e geçin veya projeksiyonda **Katılımcı Kılavuzu**nu gösterin.
- **Sunucu Konuşması**:
  > *"Bu multimodal önizleme cerrahi yapay zekanın nereye doğru gittiğini gösteriyor. Ancak bugünkü çalıştayımız için her cerrahın şu anda ihtiyaç duyduğu temel beceriye dönüyoruz: Bir klinik problemi nasıl ele alacağımız, ayrıştıracağımız ve agentik bir araştırma mimarisini nasıl kuracağımız.*
  > 
  > *Lütfen Katılımcı Kılavuzlarınızı açın. 20 dakikalık tasarım egzersizimize başlayalım."*
