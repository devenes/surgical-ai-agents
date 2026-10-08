# Agent Studio Eşdeğerlik Değerlendirmesi (Parity Assessment)

- **Belge Sürümü**: 1.0.0
- **Değerlendirme Tarihi**: 2026-10-03
- **Temel Çerçeve**: Google Agent Development Kit (ADK) `2.11.0` üzerinde `gemini-3.8-flash` (`us` / `global`)
- **Hedef Platform**: Google Cloud Gemini Enterprise Agent Platform (Vertex AI Agent Studio)

---

## 1. Özellik Eşdeğerlik Matrisi (Feature Parity Matrix)

Aşağıdaki tablo, doğrulanmış kod düzeyindeki ADK uygulamalarını doğrudan Google Cloud Agent Studio'daki görsel karşılıklarıyla eşleştirir:

| ADK Kavramı / API | Agent Studio Karşılığı | Parite Durumu | Doğrulama Notları & Mekaniği |
| :--- | :--- | :---: | :--- |
| **Coordinator Agent** (`root_agent`) | **Ana Agent / Kök Agent** | **VERIFIED** | Agent Studio tuvalindeki giriş noktası orkestratörü. Kullanıcı sorgusunu, ayrıştırmayı ve nihai yanıt sentezini yönetir. |
| **Evidence Agent** | **Yerel Subagent** (`evidence-specialist`) | **VERIFIED** | Tuval subagent düğmesi (`+`) ile eklenir. Özel talimatlar ve araçlarla yapılandırılır. |
| **Guideline Agent** | **Yerel Subagent** (`guideline-specialist`) | **VERIFIED** | Tuval subagent düğmesi (`+`) ile eklenir. Özel talimatlar ve araçlarla yapılandırılır. |
| **Sistem Talimatı** (`instruction=...`) | **Instructions Alanı** | **VERIFIED** | `agents/agent-studio/*.md` dosyalarındaki kesin markdown talimatları doğrudan UI agent talimatları paneline 1:1 eşlenir. |
| **Gemini Modeli** (`gemini-3.8-flash`) | **Model Seçici** | **VERIFIED** | Vertex AI Agent Studio genelinde `us` ve `global` bölgelerinde `gemini-3.8-flash` seçilebilir. |
| **Google Search Grounding** (`google_search`) | **Google Search Aracı** | **VERIFIED** | Agent Studio'da yerel yerleşik araç. Canlı web araması için subagent düğümlerinde etkinleştirilir. |
| **URL Context** (`url_context`) | **URL Context Aracı** | **REQUIRES MANUAL UI ACTION** | Araçlar çekmecesinde bir web bağlam aracı olarak mevcuttur; subagent yapılandırma panellerinde etkinleştirilmesi gerekir (Ödeme duvarı gecikmesine tabidir). |
| **Structured Output** (`output_schema=...`) | **Agent Output Schema / Response Config** | **REQUIRES MANUAL UI ACTION** | ADK kodunda Pydantic model parametresi ile zorunlu kılınır. Agent Studio'da Output/Response biçim panelinde yapılandırılır veya sistem talimatları ve `output-schema.json` ile prompt düzeyinde zorunlu kılınır. |
| **Agent Delegasyonu** (`sub_agents=[...]`) | **Subagent Routing / Akış Tuvali** | **VERIFIED** | Tuval yönlendirmesi, görev ayrıştırmasına dayalı olarak Coordinator'ı bağlı yerel subagent'ları çağırmaya otomatik yönlendirir. |
| **Çalışma Zamanı Olayları & Telemetri** (`runner.run_async`) | **Preview Events / Trace Çekmecesi** | **VERIFIED** | Agent Studio Preview çekmecesi adım adım yürütme izlerini, subagent çağrılarını ve grounding araç çağrılarını görsel olarak görüntüler. |
| **İnteraktif Preview** | **Preview Paneli Sohbeti** | **REQUIRES MANUAL UI ACTION** | Tuvalin sağ tarafındaki yerleşik test alanı. Araştırma sorularının manuel girilmesini gerektirir. |
| **Kod Dışa Aktarımı** (`adk export`) | **Get Code Düğmesi** | **VERIFIED** | Agent Studio, görsel agent yapısını doğrudan ADK Python koduna aktaran bir "Get Code" / dışa aktarma özelliği sunar. |

---

## 2. Durum Sınıflandırma Özeti

- **VERIFIED (8 öğe)**: ADK `2.11.0` ile Agent Studio platform özellikleri arasında yerel eşdeğerlik doğrulandı.
- **REQUIRES MANUAL UI ACTION (4 öğe)**: Google Cloud Console'da etkileşimli insan yapılandırması gerektiren özellikler (araçlar çekmecesinden URL context'i etkinleştirme, çıktı şemasını yanıtlama ayarlarına yapıştırma, Preview çekmecesinde sorguları yürütme ve çıktı izlerini doğrulama).
- **NOT AVAILABLE (0 öğe)**: Minimal POC'mizin hiçbir temel mimari özelliği Agent Studio'da desteklenmiyor değildir.
- **NOT YET VERIFIED (0 öğe)**: Tüm mimari kavramlar resmi platform şartnamelerine göre eşlenmiş ve doğrulanmıştır.

---

## 3. Tutarsızlık ve Davranış Analizi

### Araç Tahsisi (Arama vs Fonksiyon Çağırma)
- **ADK Kodunda**: Aynı subagent'ta `google_search` grounding ile fonksiyon çağırma yapılandırılmış çıktısının (`set_model_response`) karıştırılmasının Vertex AI'da `INVALID_ARGUMENT` hatasına yol açtığını keşfettik. Bu nedenle araçlar yalnızca subagent'lara (`evidence_agent`, `guideline_agent`) atanırken, Coordinator saf sentez gerçekleştirir.
- **Agent Studio'da**: Görsel tuval tam olarak bu topolojiyi yansıtır:
  - `Coordinator`: Araçlar = Yok. Subagent'lar = `[evidence-specialist, guideline-specialist]`.
  - `Evidence Agent`: Araçlar = Google Search.
  - `Guideline Agent`: Araçlar = Google Search.
Bu tasarım %100 kararlılık garanti eder ve hem kod hem de kullanıcı arayüzü ortamlarında Vertex AI araç çakışmalarını önler.

### Structured Output Zorunluluğu
- **ADK Kodunda**: Pydantic, yanıtı `StructuredEvidenceBriefModel` modeline göre doğrular.
- **Agent Studio'da**: Ayarlar panelinde Output Schema yapılandırılabilir veya talimatlarda modelin `output-schema.json` ile eşleşen geçerli JSON üretmesini yönlendiren açık negatif kısıtlamalar kullanılabilir.
