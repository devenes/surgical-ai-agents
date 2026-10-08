# Workshop Hazırlık ve Depo Denetimi (Readiness & Repository Audit)

- **Belge Sürümü**: 1.0.0
- **Denetim Tarihi**: 2026-10-03
- **Denetim Hedefi**: Surgical AI Agents Workshop Proof-of-Concept (POC)
- **Durum**: Eksiksiz Depo Denetimi (Phase 6A)

---

## 1. Yönetici Özeti

Bu denetim; akademik cerrahlar, cerrahi asistanları ve klinik fellow'lar için tasarlanan 60 dakikalık interaktif eğitsel workshop için deponun hazır olma durumunu değerlendirir.

Birincil workshop sunum ortamı **Google Cloud Agent Studio (Agent Designer)** platformudur. **Google Agent Development Kit (ADK)** içindeki programatik uygulama, geliştirici/referans temeli ve değerlendirme aynası olarak hizmet eder.

Mimari kesin olarak şu şekilde tanımlanmıştır:
```
Coordinator Agent
    ├── Evidence Specialist (Yerel Subagent)
    └── Guideline Specialist (Yerel Subagent)
```

Multimodal görüntü anlama, Agent Studio Chat / Freeform içinde yürütülen **ayrı, tamamlayıcı bir mini-demo** olarak ele alınır ve multi-agent tuvaline **entegre edilmez**.

---

## 2. Depo Eserleri Sınıflandırması (Artifact Classification)

Doğrulanmış gerçekler ile tarihsel eserleri ayırmak ve bileşen sahipliğini netleştirmek için bir envanter çalışması yapılmıştır:

| Eser / Dosya Yolu | Rol / Kategori | Mevcut Sınıflandırma | Açıklama ve Otorite |
| :--- | :--- | :---: | :--- |
| `agents/coordinator/instructions.md` | Temel Agent Prompt'u | **Source of Truth** | Coordinator için kanonik PICOT ayrıştırma ve sentez mantığı. |
| `agents/evidence/instructions.md` | Temel Agent Prompt'u | **Source of Truth** | Evidence Agent için kanonik biyomedikal literatür getirme mantığı. |
| `agents/guideline/instructions.md` | Temel Agent Prompt'u | **Source of Truth** | Guideline Agent için kanonik klinik kılavuz kataloglama mantığı. |
| `agents/*/output-schema.json` | JSON Schema Draft-07 | **Source of Truth** | Coordinator ve uzman çıktıları için katı sözleşme. |
| `agents/agent-studio/*.md` | UI Prompt'ları & Kurulum | **Source of Truth (Agent Studio)** | Görsel tuval için sistem prompt'ları, iş akışı topolojisi ve kurulum kontrol listesi. |
| `adk/` (`config.py`, `schemas.py`, vb.) | Programatik Kod | **Source of Truth (ADK Reference)** | `google-adk 2.11.0` ve `google-genai 2.28.0` kullanan Python referans uygulaması. |
| `evaluations/evalset.json`, `test-cases.yaml` | Değerlendirme Katalogları | **Source of Truth (Evaluation)** | Standartlaştırılmış 16 vakalık benchmark (8 normal, 8 edge case). |
| `evaluations/results/gemini-3-8-migration.*` | Canlı Değerlendirme Günlükleri | **Doğrulanmış Tarihsel Kanıt** | `gemini-3.8-flash` üzerinde 6 canlı testte %100 geçiş doğrulaması. |
| `docs/adk-baseline.md` | Dokümantasyon | **Tarihsel Temel** | Phase 3 dondurmasını yansıtır; 3.8 Flash geçişi öncesi tablolarda `gemini-2.5-flash` referansları içerir. |
| `docs/model-baseline.md` | Dokümantasyon | **Güncel Model Temeli** | Çoklu bölge `us` ve `global` üzerinde `gemini-3.8-flash` resmi doğrulaması. |
| `docs/agent-studio-parity.md` | Dokümantasyon | **Tarihsel Değerlendirme** | ADK yapılarını Agent Studio ile eşler; manuel UI eylemlerini sınıflandırır. |
| `docs/architecture.md` | Sistem Mimarisi | **Doğrulanmış Mimari** | 4 operasyonel yüzeyi açıklar (Web UI, Agent Studio, Multimodal, ADK Reference). |
| `README.md` | Proje Genel Bakışı | **Doğrulanmış Proje Genel Bakışı** | 4 yüzey, workshop gündemi ve hızlı başlangıç rehberleri içeren kapsamlı belge. |
| `app/README.md` | Web UI Dokümantasyonu | **Source of Truth (Web UI)** | 16 benchmark vakası ve çevrimdışı sıfır-token provası ile çalışan operasyonel FastAPI + Streamlit web paneli. |

---

## 3. Güncel Doğrulanmış Yetenekler

### A. Programatik ADK Temeli (Geliştirici Referansı)
- **Orkestrasyon**: `Coordinator` agent, `sub_agents=[evidence_agent, guideline_agent]` ile hiyerarşik bir delegasyon ağacı oluşturur.
- **Araç Tahsisi**: Arama desteği (`google.adk.tools.google_search`), kesinlikle uzman subagent'lara (`evidence_agent`, `guideline_agent`) bağlanmıştır. Coordinator'a doğrudan hiçbir araç bağlanmaz; bu da Vertex AI araç çakışmalarını önler.
- **Model Temeli**: Vertex AI çoklu bölge `us` (`https://us-aiplatform.googleapis.com`) ve `global` kullanılarak `gemini-3.8-flash` üzerinde doğrulandı.
- **Thinking Yapılandırması**: `thinking_level="MEDIUM"` ile doğrulandı; eski örnekleme parametreleri (`temperature`, `top_p`, `top_k`) Gemini 3.8 gereğince çıkarıldı.
- **Çevrimdışı Doğrulama**: 61/61 çevrimdışı birim testi geçti (%100 şema uyumu, agent yapısı, FastAPI rotaları ve prova kontrolleri).
- **Canlı Entegrasyon**: Vertex AI üzerinde 6/6 canlı entegrasyon test senaryosu geçti (kolorektal prehabilitasyon, ICG floresans, HIFU eksik kanıt, topikal TXA eksik kılavuz, bağırsak hazırlığı çelişkisi ve hastaya özel güvenlik reddi).
- **Değerlendirme Çerçevesi**: Yerel ADK değerlendirme çalıştırıcısı (`adk/eval.py`), 6 cerrahi bilişim boyutunun tamamında %100 puan aldı.

### B. Agent Studio Manuel Doğrulaması
- **Görsel Tuval Topolojisi**: İki yerel subagent'a bağlı Kök Coordinator (`evidence-specialist`, `guideline-specialist`).
- **Araç Ataması**: Subagent'lara yerel Google Search aracı eklendi; Coordinator saf akıl yürütme ve sentez orkestratörü olarak çalışır.
- **Ayrıştırma**: Coordinator, doğal dil sorgularını PICOT boyutlarına başarıyla normalize eder.
- **Kaynak Alıntıları**: Subagent'lar PubMed ve cerrahi derneklerinden canlı, tıklanabilir URL'ler getirir.
- **Preview & Trace**: Agent Studio Preview çekmecesi, adım adım yürütme izlerini, subagent çağrılarını ve search grounding araç çağrılarını görüntüler.

---

## 4. Güncel Agent Studio Davranışı vs. ADK Temeli

| Boyut | Programatik ADK Temeli | Agent Studio UI Uygulaması |
| :--- | :--- | :--- |
| **Model** | Vertex AI istemcisi üzerinden `gemini-3.8-flash` | Model açılır menüsünde seçilen `gemini-3.8-flash` |
| **Konum / Bölge** | `us` çoklu bölge (`adk/config.py` içinde belirtilir) | `us` veya `global` konsol seçicisi |
| **Agent Hiyerarşisi** | `sub_agents=[ev, gd]` ile `root_agent` | 2 yerel subagent'lı görsel kök düğüm (`+` düğmesi) |
| **Araç Yürütme** | `google_search` araç çağrı olayı | Subagent'larda etkinleştirilmiş Grounding with Google Search anahtarı |
| **Structured Output** | `output_schema=StructuredEvidenceBriefModel` ile zorunlu kılınmıştır | Sistem talimatları ile prompt düzeyinde JSON şema zorunluluğu |
| **İz İncelemesi** | Telemetri sözlüğü / log ayrıştırma (`adk.run`) | Konsolda interaktif **Preview Events / Trace** çekmecesi |
| **Yürütme Sırası** | Gemini tarafından otonom dinamik çağrı | Gemini tarafından otonom dinamik çağrı (Preview izi) |
| **Güvenlik Yönetimi** | Red tespiti & eğitsel yeniden çerçeveleme | Talimatlar üzerinden red tespiti & eğitsel yeniden çerçeveleme |

---

## 5. ADK ve Agent Studio Arasındaki Bilinen Farklar

1. **Şema Zorunluluk Mekanizması**:
   - ADK'da şema doğrulaması model düzeyinde programatik olarak zorunlu kılınır (`response_schema` / `output_schema` parametresi).
   - Agent Studio'da, görsel tuvalde en güvenilir ve doğrulanmış mekanizma negatif biçimlendirme kısıtlamalarına sahip **prompt düzeyinde şema belirtimidir**.
2. **Yürütme Telemetrisi Görünürlüğü**:
   - ADK'da olaylar yapılandırılmış Python nesneleri olarak yakalanır ve programatik olarak puanlanır.
   - Agent Studio'da yürütme adımları tuvalin sağ tarafındaki daraltılabilir **Trace / Events** çekmecesinde görsel olarak görünür.
3. **Yürütme Gecikmesi**:
   - Her iki ortamda da canlı search grounding ve multi-agent sentezi sorgu başına **45 ila 120 saniye** sürer. Sunucular üretim beklenirken izleyicileri aktif tutmalıdır.

---

## 6. Doğrulanmamış Varsayımlar

1. **Deterministik Yürütme Sırası**: `evidence-specialist`'in her zaman `guideline-specialist`'ten önce çalışacağı varsayılamaz.
2. **Sıfır Gecikmeli Arama**: Web grounding canlı Google Search indekslemesine dayanır; aralıklı ağ gecikmesi hız üzerinde etkili olabilir.
3. **Projeler Arasında Özdeş Görsel Tuval**: Google Cloud Agent Studio arayüz kontrolleri periyodik olarak güncellenebilir.

---

## 7. Workshop Riskleri ve Hata Modları

| Risk ID | Risk Açıklaması | Şiddet | Olasılık | Azaltma Stratejisi |
| :--- | :--- | :---: | :---: | :--- |
| **RSK-01** | Canlı sorgu üretim gecikmesi (60–120s) sunucuyu sessiz bırakır. | Orta | Yüksek | Üretim sırasında sunucunun senaryolu konuşma noktaları, mimari anlatımı ve PICOT açıklaması. |
| **RSK-02** | Bulut bağlantısı nedeniyle Agent Studio tuvali kullanılamaz veya yavaş. | Yüksek | Düşük | Hazırlanmış yedek ekran görüntüleri, önceden hesaplanmış JSON brief'leri ve yerel ADK CLI terminal yedeği. |
| **RSK-03** | Google Search grounding ödeme duvarlı bağlantılar veya boş alıntılar döndürür. | Orta | Orta | Subagent'lara açık erişimli PubMed özetlerine ve dernek portallarına öncelik verme talimatı verilmesi; doğrulanmış slaytlar. |
| **RSK-04** | Katılımcı teşhis planı bekleyerek gerçek hasta klinik vakası girer. | Yüksek | Orta | Katı güvenlik korkulukları bireysel tavsiyeyi reddeder; sunucu sınırları en baştan açıklar. |
| **RSK-05** | Agent Studio Preview'da çıktı JSON biçimlendirmesi hafifçe sapar. | Düşük | Düşük | Talimatlar açık negatif kısıtlamalar ve few-shot JSON şema yapısı içerir. |

---

## 8. Önerilen Düzeltmeler ve Güçlendirme Yol Haritası (Phase 6A)

1. **Agent Studio Temelini Dondurma**: Doğrulanmış yapılandırmayı belgeleyen `docs/agent-studio-baseline.md` dosyasını oluşturun.
2. **Güvenlik Politikası Dokümantasyonu**: Tanısal olmayan, reçete içermeyen, sıfır-PHI sınırlarını kodlayan `agents/agent-studio/safety-policy.md` belgesini resmileştirin.
3. **Güçlendirme Test Matrisi**: `evaluations/agent-studio-hardening.md` içinde H1–H6 testleri için beklentileri belgeleyin.
4. **Structured Output & Yönlendirme İncelemeleri**: `evaluations/agent-studio-structured-output.md`, `evaluations/agent-studio-routing.md` ve `evaluations/agent-studio-context-transfer.md` belgelerini oluşturun.
5. **Workshop Paketi**: Eksiksiz workshop paketini yazın (`workshop/presenter-runbook.md`, `participant-guide.md`, `demo-prompts.md`, `troubleshooting.md`, `fallback-demo.md`, `storyboard.md`).
6. **Ayrı Multimodal Demo**: Klinik olmayan cerrahi görsel prompt, sentetik varlık belgeleri, güvenlik sınırları ve çalıştırılabilir bağımsız ADK komut dosyası ile yalıtılmış `multimodal-demo/` dizini oluşturun.
7. **Ürün Sınırlarını Belgeleme**: 4 operasyonel sınırı açıkça tanımlamak için `README.md` ve `docs/architecture.md` dosyalarını güncelleyin.
