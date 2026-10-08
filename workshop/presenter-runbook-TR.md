# Sunucu Kılavuzu: 60 Dakikalık Cerrahi AI Agent Çalıştayı (Presenter Runbook)

- **Oturum Başlığı**: Multi-Agent AI Architectures in Surgical Research: From Clinical Inquiries to Structured Evidence
- **Sunucu Rolü**: Lider Cerrahi AI Eğitmeni / Çalıştay Moderatörü
- **Birincil Canlı Yüzey**: Google Cloud Agent Studio (Agent Designer Canvas)
- **Tamamlayıcı Canlı Yüzey**: Agent Studio Chat / Freeform (Multimodal Mini-Demo)
- **Yedek Yüzey**: ADK CLI Terminali ve Önceden Hesaplanmış Evidence Brief'ler
- **Hedef Süre**: Tam 60 Dakika

---

## 🛡️ T-30 Dakika Çalıştay Öncesi Prova Protokolü (Kürsü Doğrulaması - Podium Verification)

Katılımcılar konferans salonuna girmeden otuz dakika önce, terminalinizde otomatikleştirilmiş prova (dry-run rehearsal) komutunu çalıştırın:
```bash
uv run python -m app.cli rehearse
```

### Bu komutun < 2 saniyede deterministik olarak doğruladıkları:
- **Sıfır Token Güvencesi (Zero-Token Assurance)**: Gerekli demo verilerinin %100'ünün sıfır API çağrısı ile yerel olarak önbelleğe alındığını doğrular.
- **Multimodal Studio**: Laparoskopik Critical View of Safety (CVS) şematiğinin yerel render edilmesini ve nötr eğitici vision çıktısını doğrular.
- **Tüm 16 Kıyaslama Vakası (Benchmark Cases)**: 8 Normal (`NORM-01` - `NORM-08`) ve 8 Uç Durum (`EDGE-01` - `EDGE-08`) genelinde PICOT ayrıştırmasını, Evidence Specialist çalışmalarını, Guideline Specialist beyanlarını ve Consensus Matrislerini test eder.
- **Epistemik Tevazu Tetikleyicileri (Epistemic Humility Triggers)**: `evidence_not_found: true` (`EDGE-01`, `EDGE-05`, `EDGE-08`) ve `guidelines_not_found: true` (`EDGE-02`) durumlarını doğrular.
- **Uyuşmazlık Matrisleri (Disagreement Matrices)**: Nüanslı klinik görüş ayrılıklarını doğrular (`EDGE-03`, `EDGE-04`, `NORM-06`).
- **Hasta Güvenliği Bariyerleri (Patient Safety Guardrails)**: Klinik tuzak sorguları için otomatik yakalama ve eğitsel reddetmeyi teyit eder (`EDGE-07`).
- **JSON Schema Doğrulaması**: `agents/coordinator/output-schema.json` standardına tam uyumu garanti eder.

### Kürsü Başlatma Kontrol Listesi (Podium Launch Checklist):
1. Terminal 1: Yerel Web UI'ı başlatın:
   ```bash
   uv run python -m app.cli all
   ```
2. Tarayıcıda `http://127.0.0.1:8501` adresini açın.
3. Salon Wi-Fi bağlantısı yavaşsa veya güvenlik duvarı/captive portal tarafından engelleniyorsa, **kenar çubuğundaki "⚡ Offline Mock Mode (Zero Tokens / No API)" seçeneğini işaretli tutun**.
4. Anlık sıfır token'lı CLI fallback'leri için Terminal 2'yi açık tutun:
   ```bash
   uv run python -m adk.run --offline
   uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up
   ```

---

## Zaman Çizelgesi Genel Bakışı (Timeline Overview)

| Zaman Aralığı | Bölüm | Odak | Yüzey |
| :---: | :--- | :--- | :--- |
| **00:00 – 07:00** (7dk) | Bölüm 1 | Giriş ve Agentic Paradigma Değişimi | Slayt Sunumu / Ekran Paylaşımı |
| **07:00 – 20:00** (13dk) | Bölüm 2 | Canlı Multi-Agent Demosu (Kolorektal Prehabilitasyon) | Agent Studio Canvas + Preview |
| **20:00 – 25:00** (5dk) | Bölüm 3 | Mimari Analiz ve Trace İncelemesi | Agent Studio Trace Çekmecesi |
| **25:00 – 30:00** (5dk) | Bölüm 4 | Tamamlayıcı Multimodal Mini-Demo | Agent Studio Chat / Freeform |
| **30:00 – 50:00** (20dk) | Bölüm 5 | Katılımcı Uygulamalı Proje Egzersizi | Katılımcı Kılavuzu ve Çalışma Sayfaları |
| **50:00 – 57:00** (7dk) | Bölüm 6 | Grup Tartışması ve Çıktı Değerlendirmesi | Paylaşılan Ekran / Tartışma |
| **57:00 – 60:00** (3dk) | Bölüm 7 | Kapanış, Klinik Güvenlik ve Sonraki Adımlar | Kapanış Slaytları |

---

## Bölüm 1: Giriş ve Agentic Değişim (00:00 – 07:00)

- **Hedef**: Akademik cerrahların monolitik chatbot'lar yerine neden multi-agent mimarilere ihtiyaç duyduğunu açıklamak; PICOT görev ayrıştırmasını ve epistemik tevazuyu tanıtmak.
- **Sunucunun Söyleyecekleri**:
  > *"Herkese merhaba. Cerrahlar olarak hepimiz ChatGPT veya Gemini gibi ticari yapay zeka chatbot'larını deneyimledik. Ve hepimiz aynı klinik duvara çarptık: sahte çalışma atıfları (hallucination) üretiyorlar, muğlak sohbet diliyle yazıyorlar, klinik araştırmalar ile kılavuzları birbirine karıştırıyorlar ve tehlikeli bir şekilde bireysel hasta tavsiyesi vermeye cüret edebiliyorlar.*
  > 
  > *Bugün, geleneksel chatbot'ların ötesine geçiyoruz. AI agent mimarilerini inceleyeceğiz. Bir agent sadece bir sonraki kelimeyi tahmin etmekle kalmaz; plan yapar, canlı Google Search gibi araçları kullanır, uzmanlaşmış görevleri alt agent'lara devreder ve doğrulanabilir, yapılandırılmış kanıt özetleri (evidence briefs) üretir. Önümüzdeki 60 dakika boyunca, kritik cerrahi araştırma sorularını nasıl güvenilir sistemlere dönüştürdüğümüzü göreceksiniz."*
- **Sunucunun Tıklayacakları**:
  - Slayt 1: Başlık ve Cerrahi Bilişim İkilemi.
  - Slayt 2: Chatbot vs. Agent Mimarisi karşılaştırma tablosu.
  - Ekranı Google Cloud Console üzerindeki Agent Studio canvas ekranına geçirin.
- **Tam Demo Prompt**: Yok (Açılış sunumu ve çerçeveleme).
- **Beklenen Görsel Durum**: Sunum slaytları; tarayıcıda `surgical-evidence-coordinator` canvas görünümüne geçiş.
- **Beklenen Çıktı**: Katılımcıların oturum amacını kavraması: klinik tanı değil, yapılandırılmış araştırma sentezi.
- **Fallback**: Projeksiyon/ekran çalışmazsa, basılı ajanda notlarından anlatıma devam edin.

---

## Bölüm 2: Canlı Multi-Agent Demosu (07:00 – 20:00)

- **Hedef**: Agent Studio Preview içinde birincil kolorektal prehabilitasyon sorgusunu yürütmek; otonom ayrıştırma, alt agent delegasyonu, gerçek zamanlı web grounding ve yapılandırılmış JSON sentezini göstermek.
- **Sunucunun Söyleyecekleri**:
  > *"Şimdi bunu canlı izleyelim. Ekranımda Google Cloud Agent Studio açık. Üç agent'lı bir sistem inşa ettik: merkezi bir Coordinator ve iki yerel alt agent — tıp literatürünü tarayan Evidence Specialist ve cerrahi uzmanlık derneklerini sorgulayan Guideline Specialist.*
  > 
  > *Elektif kolorektal prehabilitasyon ile ilgili gerçek bir klinik araştırma sorusu soruyorum. Preview panelinde ne olduğuna dikkat edin."*
- **Sunucunun Tıklayacakları**:
  1. Agent Studio canvas'ın sağ üst köşesindeki **Preview** butonuna tıklayın.
  2. Birincil demo prompt'unu giriş kutusuna yapıştırın.
  3. **Send** butonuna tıklayın (veya Enter'a basın).
  4. Agent çalışırken (yaklaşık 45–90 saniye), canvas topolojisine dikkat çekin ve arka planda gerçekleşen PICOT ayrıştırmasını anlatın.
- **Tam Demo Prompt**:
  ```text
  For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?
  ```
- **Beklenen Görsel Durum**:
  - Preview panelinde ilerleme göstergeleri belirir.
  - Adım olayları Coordinator'ın `evidence-specialist` ve `guideline-specialist` agent'larını çağırdığını gösterir.
  - Nihai yanıt temiz, yapılandırılmış bir JSON evidence brief olarak render edilir.
- **Beklenen Çıktı**:
  - `research_scope`: Doldurulmuş PICOT ayrıştırması (Yetişkinler, Elektif kolorektal cerrahi, Multimodal prehab, Standart bakım, 6MWD/komplikasyonlar).
  - `evidence_findings`: PREHAB çalışması (Molenaar 2023), BJS meta-analizleri ve canlı URL bağlantıları.
  - `guideline_findings`: ERAS Society (2023) ve ASCRS önerileri ile URL bağlantıları.
  - `areas_of_agreement`: Fonksiyonel kapasite artışı üzerindeki uzlaşı.
  - `areas_of_disagreement`: Seçilmemiş kohortlarda majör cerrahi komplikasyonların azalmasına dair çelişkili bulgular.
  - `safety_disclaimer`: Zorunlu klinik dışı feragatname metni.
- **Fallback**:
  - *Üretim > 90 saniye sürer veya zaman aşımına uğrarsa*: `workshop/fallback-demo.md` kılavuzuna geçin veya önceden kaydedilmiş [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) dosyasını tarayıcıda veya terminalde açın (`.venv/bin/python -m adk.run`).

---

## Bölüm 3: Mimari Analiz ve Trace İncelemesi (20:00 – 25:00)

- **Hedef**: Katılımcılara araç çağrılarının, arama sorgularının ve prompt sözleşmelerinin tam mekaniğini göstermek için Trace / Events çekmecesini açarak "kara kutu" algısını kırmak.
- **Sunucunun Söyleyecekleri**:
  > *"Bir cerrah bu çıktıya neden güvenmeli? Çünkü agent'ın muhakeme adımlarının her birini denetleyebiliyoruz. Sağ taraftaki bu Trace çekmecesine bakın.*
  > 
  > *İşte Coordinator'ın Evidence Specialist'e gönderdiği net PICOT sorgusu. İşte gerçek zamanlı yürütülen Google Search sorgusu. PubMed ve ERAS Society'den dönen kaynak URL'lerine dikkat edin. Ve Coordinator agent'ın kendisinin DOĞRUDAN arama aracına SAHİP OLMADIĞINI görün — o yalnızca bir akıl yürütme ve sentez motorudur. Bu ayrım araç çakışmalarını önler ve bilimsel hesap verebilirliği sağlar."*
- **Sunucunun Tıklayacakları**:
  1. Preview çekmecesindeki **Events** (veya **Trace**) sekmesine tıklayın.
  2. Coordinator delegasyon olayını genişletin.
  3. `google_search` sorgu dizesini görmek için `evidence-specialist` alt agent olayını genişletin.
  4. Alınan dernek bağlantılarını görmek için `guideline-specialist` alt agent olayını genişletin.
  5. Nihai JSON çıktı biçimlendirme adımını vurgulayın.
- **Tam Demo Prompt**: Yok (Daha önce çalıştırılan oturumun denetimi).
- **Beklenen Görsel Durum**: Coordinator -> Subagent -> Tool Call -> Synthesis adımlarını gösteren hiyerarşik izleme ağacı.
- **Beklenen Çıktı**: Katılımcıların sürecin bir sihir değil; deterministik, kaynaklı (grounded) ve denetlenebilir olduğunu görmesi.
- **Fallback**: Tarayıcıda trace çekmecesi açılmazsa, [`docs/agent-studio-baseline.md`](../docs/agent-studio-baseline.md) dosyasındaki eşdeğer trace yapısını veya `adk.run` terminal telemetrisini gösterin.

---

## Bölüm 4: Tamamlayıcı Multimodal Mini-Demo (25:00 – 30:00)

- **Hedef**: Modern yapay zeka modellerinin görsel cerrahi bilgileri (laparoskopik görüntüler, ameliyat sahaları) işleyebildiğini ve aynı zamanda tanı koymayan, reçete yazmayan katı güvenlik sınırlarına nasıl uyduğunu göstermek.
- **Sunucunun Söyleyecekleri**:
  > *"Uygulamalı egzersizimize geçmeden önce ek bir yetenek göstermek istiyorum. Cerrahi doğası gereği görsel bir uzmanlıktır. Yapay zeka cerrahi görüntüleri anlayabilir mi?*
  > 
  > *Önemli bir not: Çoklu agent araştırma tuvalimiz bilinçli olarak metin tabanlıdır. Ancak Gemini ayrı bir yüzeyde multimodal muhakemeyi de destekler. Şimdi Agent Studio Chat / Freeform penceresine geçelim ve ameliyat içi bir çizim yükleyelim.*
  > 
  > *Katı prompt sınırımıza dikkat edin: modelden yalnızca gözlemlenebilir anatomik özellikleri tanımlamasını istiyoruz; bireysel hasta tanısı koymasını veya cerrahi devam/dur kararı vermesini açıkça yasaklıyoruz."*
- **Sunucunun Tıklayacakları**:
  1. **Agent Studio Chat / Freeform** (veya Vertex AI Studio Multimodal Prompt) ile yeni bir sekme açın.
  2. **Attach Image** butonuna tıklayın.
  3. `multimodal-demo/assets/` dizininden hazırlanan demo görselini yükleyin.
  4. `multimodal-demo/prompt.md` içindeki Prompt 1'i yapıştırın.
  5. **Run** butonuna tıklayın.
- **Tam Demo Prompt**:
  ```text
  Describe only the observable visual anatomical and operative features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
  ```
- **Takip Prompt'u (Zaman kalırsa)**:
  ```text
  Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
  ```
- **Beklenen Görsel Durum**:
  - Prompt metniyle birlikte görüntülenen resim önizlemesi.
  - Üretilen çıktının gözlemlenebilir anatomiyi (örn. safra kesesi infundibulumu, sistik kanal bölgesi, anatomik işaretler) tarafsız biçimde açıklaması.
  - Sıfır tanısal iddia; sıfır tedavi önerisi.
- **Beklenen Çıktı**: Objektif anatomik tanımlama; bilgisayarlı görü doğrulaması üzerine eğitsel tartışma (örn. Critical View of Safety).
- **Fallback**:
  - *Freeform sekmesi yavaşsa*: Terminalde `python multimodal-demo/adk_multimodal_example.py` betiğini çalıştırın veya `multimodal-demo/fallback.md` içindeki önceden kaydedilmiş çıktıyı gösterin.

---

## Bölüm 5: Katılımcı Uygulamalı Egzersizi (30:00 – 50:00)

- **Hedef**: Katılımcıların PICOT çerçevesini ve uzman delegasyonu tasarımını kullanarak kendi cerrahi araştırma sorularını agentik bir projeye dönüştürmelerine rehberlik etmek.
- **Sunucunun Söyleyecekleri**:
  > *"Şimdi sıra sizde. Katılımcı Kılavuzunuzu açın. Buradaki her cerrahın bu hafta ameliyathanede veya poliklinikte karşılaştığı bir klinik soru vardır.*
  > 
  > *Önümüzdeki 20 dakika boyunca göreviniz kod yazmak değil; bir AI Sistem Mimarı olarak hareket etmektir:*
  > *1. Cerrahi ikileminizi belirleyin.*
  > *2. Bunu PICOT çerçevesine ayrıştırın.*
  > *3. Evidence Specialist'in ne araması gerektiğini tanımlayın.*
  > *4. Guideline Specialist'in hangi kılavuzları sorgulaması gerektiğini belirleyin.*
  > *5. Çalışmalar ile kılavuzların nerede çelişebileceğini öngörün.*
  > 
  > *Çok önemli güvenlik hatırlatması: Kesinlikle gerçek hasta verisi KULLANMAYIN. Dosya numarası, tarih veya kimlik bilgisi girmeyin. Tüm sorular genel cerrahi araştırması olarak formüle edilmelidir."*
- **Sunucunun Tıklayacakları**:
  - Projeksiyonda **Egzersiz Çalışma Sayfası Şablonunu** gösterin (`workshop/participant-guide.md`).
  - Salonda dolaşarak katılımcıların sorularını formüle etmelerine yardımcı olun.
- **Tam Demo Prompt**: Katılımcılar [`workshop/participant-guide.md`](participant-guide.md) içindeki şablonları kullanır.
- **Beklenen Görsel Durum**: Katılımcıların dizüstü bilgisayarlarında veya basılı çalışma sayfalarında bireysel veya ikili gruplar halinde çalışması.
- **Beklenen Çıktı**: Katılımcıların tamamlanmış 5 maddelik PICOT ayrıştırması ve 2 uzman delegasyon prompt'u üretmesi.
- **Fallback**: Bir katılımcı takılırsa veya aklına fikir gelmezse, `workshop/demo-prompts.md` içindeki hazır başlıklara yönlendirin (örn. ICG ile anastomoz kaçak önleme, hafif safra taşı pankreatitinde indeks kolesistektomi, stoma açılmasında profilaktik meş).

---

## Bölüm 6: Sonuçları Paylaşma ve Çıktı Değerlendirmesi (50:00 – 57:00)

- **Hedef**: 2–3 katılımcının formüle ettiği soruyu paylaşmasını sağlamak; zaman elverirse Agent Studio Preview'da canlı test etmek; çıktı kalitesini ve epistemik tevazuyu değerlendirmek.
- **Sunucunun Söyleyecekleri**:
  > *"İki gönüllümüzü dinleyelim. Kim sorusunu paylaşmak ister?*
  > 
  > *[Gönüllü 1 konusunu paylaşır, örn. uç kolostomi açılışında profilaktik meş kullanımı].*
  > 
  > *Meslektaşımızın literatür görevini (parastomal herni insidansı üzerine RKÇ'ler) kılavuz görevinden (Avrupa Herni Derneği ve ASCRS görüşleri) ne kadar temiz ayırdığına bakın. Şimdi agent'ın bunu nasıl sentezlediğine bakalım: 'areas_of_disagreement' bölümüne bakın — gerçek klinik nüans tam olarak burada yatar."*
- **Sunucunun Tıklayacakları**:
  - İsteğe bağlı olarak seçilen bir katılımcı sorusunu Agent Studio Preview'a yapıştırın.
  - Alternatif olarak `workshop/demo-prompts.md` içindeki **ICG floresans** veya **Mekanik bağırsak hazırlığı** için önceden hesaplanmış çıktıyı sergileyin.
- **Tam Demo Prompt**: Gönüllü sorusu veya `workshop/demo-prompts.md` içindeki Demo Soru 3 (ICG Floresans).
- **Beklenen Görsel Durum**: Ana ekranda canlı veya hazır kanıt özeti gösterimi.
- **Beklenen Çıktı**: Kanıt kalitesi, atıf geçerliliği ve uzlaşı/ayrışma analizinin etkileşimli eleştirisi.
- **Fallback**: `prompts/demo-questions.md` içindeki hazır Demo Soru 5'i (akut pankreatitte kolesistektomi zamanlaması) kullanın.

---

## Bölüm 7: Kapanış, Güvenlik ve Sonraki Adımlar (57:00 – 60:00)

- **Hedef**: Güvenlik sınırlarını yinelemek (CDSS yok, hasta tavsiyesi yok); low-code Agent Studio ile high-code ADK arasındaki köprüyü açıklamak; kaynakları paylaşmak.
- **Sunucunun Söyleyecekleri**:
  > *"Bugünkü oturumumuzu tamamlarken şu üç temel ilkeyi unutmayalım:*
  > *Birincisi: Agent'lar sohbet botu değildir. Görevleri PICOT ile ayrıştırarak ve uzman alt agent'lara devrederek atıf uydurmalarını (hallucination) önler, yapılandırılmış ve doğrulanabilir araştırma özetleri elde ederiz.*
  > *İkincisi: Epistemik tevazu (Epistemic humility). Yetkin bir yapay zeka sistemi kanıt bulunamadığında bunu bilmeli ve makul görünen yalanlar uydurmak yerine 'bulunamadı' demelidir.*
  > *Üçüncüsü: Güvenlik tavizsizdir. Bu araçlar eğitsel araştırma asistanlarıdır; asla bireysel hasta için klinik karar destek sistemi (CDSS) değildir.*
  > 
  > *Bugün gördüğünüz her şey — prompt'lar, şemalar ve geliştirici ADK kod tabanı — açık kaynak depomuzda mevcuttur. Katılımınız için teşekkür ederim!"*
- **Sunucunun Tıklayacakları**:
  - Depo bağlantısı / QR kod içeren kapanış slaytı.
  - Kapanış Soru-Cevap.
- **Beklenen Görsel Durum**: Kapanış slaytı.
- **Beklenen Çıktı**: Oturumun tam 60:00'da tamamlanması.
