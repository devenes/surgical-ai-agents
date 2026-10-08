# 60 Dakikalık Cerrahi Yapay Zeka (AI Agent) Workshop Planı

## Workshop Genel Bakışı

- **Başlık**: Cerrahi Araştırmalarda Multi-Agent AI Mimarileri: Klinik Sorulardan Yapılandırılmış Kanıtlara
- **Hedef Kitle**: Akademik cerrahlar, cerrahi asistanları, klinik fellow'lar ve klinik araştırmacılar.
- **Süre**: 60 Dakika.
- **Format**: İnteraktif ders, canlı sistem demonstrasyonu ve uygulamalı prompt çözümlemesi.
- **Temel Eğitim Hedefi**: Modern yapay zekanın sohbet robotlarının ötesine geçerek nasıl yapılandırılmış, doğrulanmış (grounded) multi-agent araştırma asistanlarına dönüştüğünü göstererek cerrahi uygulayıcılar için AI agent kavramını anlaşılır kılmak.

---

## Pedagojik Konsept: 6 Aşamalı Dönüşüm

Cerrahlar sıklıkla kaynak uyduran (hallucination), muğlak yanıtlar veren veya yapılandırılmamış metin blokları üreten jenerik AI sohbet robotlarıyla zorluk yaşarlar. Bu workshop ilkeli dönüşümü sergiler:

```
[Klinik Araştırma Problemi]
       │
       ▼ (1. Sorgu Normalizasyonu & PICOT Çerçeveleme)
[Görev Ayrıştırma (Task Decomposition)]
       │
       ▼ (2. Uzmanlaşmış Delegasyon)
[Uzman Araştırma Agent'ları (Evidence & Guidelines)]
       │
       ▼ (3. Araç Doğrulaması / Grounding & URL Doğrulama)
[Web Araştırması & URL Context]
       │
       ▼ (4. Şema Kısıtlamalı Uzlaştırma)
[Yapılandırılmış Kanıt Özeti (Structured Evidence Brief)]
       │
       ▼ (5. Eğitsel İnceleme)
[Çalışan Yapay Zeka Prototipi]
```

---

## 60 Dakikalık Workshop Gündemi ve Oturum Modülleri

Oturum, [`workshop/presenter-runbook-TR.md`](../workshop/presenter-runbook-TR.md) dosyasında detaylandırılan senaryolaştırılmış 7 bölümlük operasyonel akışı takip eder:

| Zaman Aralığı | Bölüm | Odak & Katılımcı Aktiviteleri | Birincil Yüzey & Araçlar | Alt Belge Bağlantısı (TR / EN) |
| :---: | :--- | :--- | :--- | :--- |
| **T-30m** | **Uçuş Öncesi** | **Podyum Doğrulaması**: 16 benchmark senaryosunun tamamında otomatik sıfır-token prova komutu (`uv run python -m app.cli rehearse`). | Terminal / Web UI | [TR](../workshop/presenter-runbook-TR.md#🛡️-t-30-dakika-çalıştay-öncesi-prova-protokolü-kürsü-doğrulaması---podium-verification) \| [EN](../workshop/presenter-runbook.md#🛡️-t-30-minute-pre-workshop-rehearsal-protocol-podium-verification) |
| **00:00 – 07:00** (7m) | **Bölüm 1** | **Giriş ve Agentic Paradigma Değişimi**: Cerrahide monolitik sohbet robotlarının kısıtları; PICOT normalizasyonu; klinik güvenlik sınırları. | Slayt Sunumu / Ekran Paylaşımı | [TR](../workshop/storyboard-TR.md) \| [EN](../workshop/storyboard.md)<br>[TR](safety-TR.md) \| [EN](safety.md) |
| **07:00 – 20:00** (13m) | **Bölüm 2** | **Canlı Multi-Agent Demosu**: Birincil Kolorektal Prehabilitasyon sorgusu; Coordinator ayrıştırması; paralel Evidence & Guideline uzmanı search grounding. | Agent Studio Canvas / Web UI | [TR](../workshop/presenter-runbook-TR.md#bölüm-2-canlı-multi-agent-demosu-0700--2000) \| [EN](../workshop/presenter-runbook.md#segment-2-live-multi-agent-demo-0700--2000)<br>[TR](../workshop/demo-prompts-TR.md#1-birincil-demo-multimodal-kolorektal-prehabilitasyon-primary-demo) \| [EN](../workshop/demo-prompts.md#1-primary-demo-multimodal-colorectal-prehabilitation) |
| **20:00 – 25:00** (5m) | **Bölüm 3** | **İz İncelemesi ve Yapısal Ayrıştırma**: Araç çağrılarının, Google Search sorgularının, doğrulanmış kaynak URL'lerinin ve şema sözleşmelerinin denetimi. | Agent Studio Trace / Swagger | [Schema](../agents/coordinator/output-schema.json)<br>[TR](model-baseline-TR.md) \| [EN](model-baseline.md) |
| **25:00 – 30:00** (5m) | **Bölüm 4** | **Tamamlayıcı Multimodal Mini-Demo**: Operatif anatomik işaret gözlemi (Critical View of Safety şeması); tanısal olmayan güvenlik sınırları. | Vision Studio / Terminal | [TR](../multimodal-demo/README-TR.md) \| [EN](../multimodal-demo/README.md)<br>[TR](../multimodal-demo/prompt-TR.md) \| [EN](../multimodal-demo/prompt.md) |
| **30:00 – 50:00** (20m) | **Bölüm 5** | **Uygulamalı Katılımcı Egzersizi**: Katılımcılar kendi klinik ikilemlerini PICOT ile ayrıştırır ve Web UI veya Agent Studio'da çalıştırır. | Katılımcı Kılavuzu / Web UI | [TR](../workshop/participant-guide-TR.md) \| [EN](../workshop/participant-guide.md)<br>[TR](../workshop/demo-prompts-TR.md) \| [EN](../workshop/demo-prompts.md) |
| **50:00 – 57:00** (7m) | **Bölüm 6** | **Grup Değerlendirmesi ve Çıktı Analizi**: Kanıt özetlerinin eleştirel analizi; uzlaşma/ayrışma ve epistemik alçakgönüllülüğün (`not_found: true`) değerlendirilmesi. | Ortak Ekran / Tartışma | [Eval](../evaluations/expected-behavior.md)<br>[Prompts](../prompts/edge-cases.md) |
| **57:00 – 60:00** (3m) | **Bölüm 7** | **Kapanış, Kod Aynası ve Sonraki Adımlar**: Agent Studio'dan Python ADK koduna aktarım; PRISMA derleme süreçleri; kurumsal RAG yol haritası. | Sunum / Terminal | [TR](adk-setup-TR.md) \| [EN](adk-setup.md)<br>[TR](../workshop/cloud-deployment-TR.md) \| [EN](../workshop/cloud-deployment.md) |

---

## Katılımcılar İçin Uygulamalı Egzersiz Kılavuzu

Katılımcılar, [`workshop/participant-guide-TR.md`](../workshop/participant-guide-TR.md) dosyasındaki adım adım çalışma sayfasını takip eder:

1. **Egzersiz 1: Bir Klinik Soruyu Ayrıştırın (PICOT)**
   - Katılımcılar [`workshop/demo-prompts-TR.md`](../workshop/demo-prompts-TR.md) içinden bir soru seçer veya kendi klinik ikilemlerini yazar.
   - Açık PICOT kırılımını oluşturma pratiği yaparlar:
     - **Population**: Belirli hasta grubu (örn. elektif kolorektal rezeksiyon geçiren yetişkinler).
     - **Context**: Ortam (elektif vs acil).
     - **Intervention**: Cerrahi işlem, protokol veya cihaz.
     - **Comparator**: Standart bakım / geleneksel tedavi.
     - **Outcomes**: Birincil ve ikincil cerrahi sonlanım noktaları (örn. 30 günlük morbidite, kaçak oranı, yatış süresi).
     - **Timeframe**: Değerlendirilen literatür penceresi (örn. son 5–10 yıl).
2. **Egzersiz 2: Görüş Ayrılıklarını ve Epistemik Alçakgönüllülüğü Tespit Edin**
   - Multi-agent sistem tarafından üretilen kanıt özetini inceleyin.
   - Yapay zekanın klinik çalışma kanıtlarını uzmanlık derneği kılavuzlarından doğru şekilde ayırıp ayırmadığını değerlendirin.
   - Kanıt bulunmadığında negatif durum tespitini (`not_found: true`) doğrulayın (örn. özofagus kanserinde HIFU, `EDGE-01`).
3. **Egzersiz 3: Klinik Güvenlik Korkuluklarını Test Edin**
   - Gerçek dünya hasta senaryosu girin (`EDGE-07`).
   - Coordinator agent'ın güvenlik reddini nasıl uyguladığını, eğitsel sorumluluk reddi beyanı verdiğini ve genel akademik literatüre nasıl yeniden yönlendirdiğini gözlemleyin.

---

## Workshop Operasyonel Paket Bağlantıları

- **Sunucu Talimatları (Presenter Runbook)**: [TR](../workshop/presenter-runbook-TR.md) | [EN](../workshop/presenter-runbook.md)
- **Katılımcı Çalışma Sayfası (Participant Guide)**: [TR](../workshop/participant-guide-TR.md) | [EN](../workshop/participant-guide.md)
- **Küratörlü Prompt Kataloğu (16 Senaryo)**: [TR](../workshop/demo-prompts-TR.md) | [EN](../workshop/demo-prompts.md)
- **Canlı Sorun Giderme Kılavuzu (Troubleshooting)**: [TR](../workshop/troubleshooting-TR.md) | [EN](../workshop/troubleshooting.md)
- **4 Kademeli Acil Durum Planı (Fallback Demo)**: [TR](../workshop/fallback-demo-TR.md) | [EN](../workshop/fallback-demo.md)
- **Cloud Run Dağıtım Kılavuzu**: [TR](../workshop/cloud-deployment-TR.md) | [EN](../workshop/cloud-deployment.md)
- **İnteraktif Web UI Kılavuzu**: [TR](local-ui-setup-TR.md) | [EN](local-ui-setup.md)
- **Windows Kurulum Kılavuzu**: [TR](windows-setup-guide-TR.md) | [EN](windows-setup-guide.md)
