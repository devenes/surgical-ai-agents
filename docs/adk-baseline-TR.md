# ADK Multi-Agent Temel Bildirgesi (ADK Multi-Agent Baseline Manifest)

- **Belge Sürümü**: 1.0.0
- **Durum**: **DONDURULMUŞ & DOĞRULANMIŞ TEMEL (FROZEN BASELINE)**
- **Tarih**: 2026-10-03
- **Git Commit Durumu**: Temiz commit'lenmemiş çalışma ağacı (proje politikası gereği)

---

## 1. Ortam ve Paket Meta Verileri

| Özellik | Değer | Notlar |
| :--- | :--- | :--- |
| **Python Sürümü** | `3.12.13` (`uv` ile) | `.venv` konumunda yalıtılmış sanal ortam |
| **google-adk Sürümü** | `2.11.0` | Resmi Google Agent Development Kit |
| **google-genai Sürümü** | `2.28.0` | Resmi Google GenAI SDK |
| **google-auth Sürümü** | `2.59.1` | Application Default Credentials (ADC) |
| **pydantic Sürümü** | `2.13.5` | Katı sözleşme ve şema doğrulaması |
| **jsonschema Sürümü** | `4.26.0` | JSON Schema Draft-07 uyumluluğu |
| **pyyaml Sürümü** | `6.0.3` | YAML test kataloğu ayrıştırıcısı |
| **GCP Proje Kimliği** | `GOOGLE_CLOUD_PROJECT` ile yapılandırılır | Ortamda yapılandırılmış aktif proje |
| **GCP Bölgesi** | `GOOGLE_CLOUD_LOCATION` (`us`/`global`) | Vertex AI model endpoint konumu |
| **Model** | `gemini-3.8-flash` (ADK varsayılanı) | `thinking_config` ile yüksek hızlı akıl yürütme |
| **Kimlik Doğrulama** | ADC (`gcloud auth application-default login`) | Doğrulanmış Application Default Credentials |

---

## 2. Multi-Agent Mimarisi

```
Kullanıcı Sorgusu (Cerrahi Araştırma Konusu)
  │
  ▼
[Coordinator Agent] (root_agent)
  │  • Model: gemini-3.8-flash
  │  • mode: single_turn
  │  • output_schema: StructuredEvidenceBriefModel
  │  • Tools: Yok (Search-Function calling çakışmasını önlemek için)
  │
  ├──► [Evidence Agent] (sub_agent)
  │      • Model: gemini-3.8-flash
  │      • mode: single_turn
  │      • input_schema: EvidenceQueryInput
  │      • Tools: google_search (Grounding)
  │
  └──► [Guideline Agent] (sub_agent)
         • Model: gemini-3.8-flash
         • mode: single_turn
         • input_schema: GuidelineQueryInput
         • Tools: google_search (Grounding)
```

### Coordinator Agent
- **Factory**: `adk.coordinator.agent.create_coordinator_agent(model_name="gemini-3.8-flash")`
- **Root Export**: `adk/coordinator/agent.py:root_agent`
- **Delegasyon Modu**: Yerel tek turlu ADK subagent'ları (`sub_agents=[evidence_agent, guideline_agent]`).
- **Girdi**: Doğal dilde cerrahi araştırma sorusu dizgisi.
- **Çıktı Sözleşmesi**: `output_schema=StructuredEvidenceBriefModel` ([adk/schemas.py](../adk/schemas.py)) ile zorunlu kılınmıştır.
- **Araçlar**: JSON yapılandırılmış çıktı fonksiyonları ile Vertex AI araç çakışmasını önlemek için Coordinator'a doğrudan hiçbir araç eklenmemiştir.

### Uzman Agent'lar (Specialist Agents)
1. **Evidence Agent**:
   - **Factory**: `adk.evidence.agent.create_evidence_agent(model_name="gemini-3.8-flash", use_url_context=False)`
   - **Rolü**: PRISMA/RKÇ kademelerinde literatür getirme (sistematik derlemeler, çok merkezli RKÇ'ler, prospektif kohortlar).
   - **Girdi Sözleşmesi**: `EvidenceQueryInput` (PICOT parametreleri + literatür odağı).
   - **Araçlar**: `google.adk.tools.google_search`.
2. **Guideline Agent**:
   - **Factory**: `adk.guideline.agent.create_guideline_agent(model_name="gemini-3.8-flash", use_url_context=False)`
   - **Rolü**: Klinik uygulama kılavuzu getirme (NICE, ERAS Society, ACS, ASCRS, EAES, ESCP, SAGES, TSS).
   - **Girdi Sözleşmesi**: `GuidelineQueryInput` (PICOT parametreleri + kılavuz odağı).
   - **Araçlar**: `google.adk.tools.google_search`.

---

## 3. Şemalar ve Yapılandırılmış Çıktı

- **Birincil Coordinator Şeması**: [agents/coordinator/output-schema.json](../agents/coordinator/output-schema.json)
  - **JSON Schema Draft-07** ile uyumludur.
  - Doğrulanmış alanlar: `research_question`, `research_scope` (PICOT), `not_found` (`evidence_not_found`, `guidelines_not_found`, `details`), `evidence_findings`, `guideline_findings`, `sources`, `areas_of_agreement`, `areas_of_disagreement`, `uncertainty`, `limitations`, `discussion_questions`, `safety_disclaimer`.
- **Uzman Şemaları**:
  - Evidence: [agents/evidence/output-schema.json](../agents/evidence/output-schema.json)
  - Guideline: [agents/guideline/output-schema.json](../agents/guideline/output-schema.json)

---

## 4. Değerlendirme ve Doğrulama Durumu

| Test Paketi | Komut | Sonuç |
| :--- | :--- | :---: |
| **Çevrimdışı Birim Testleri** | `rtk uv run pytest` | **61/61 GEÇTİ** (3.88s) |
| **Şema Doğrulaması** | `Draft7Validator.check_schema` | **3/3 GEÇTİ** |
| **Canlı Brief Doğrulaması** | `Draft7Validator.validate(live_example)` | **GEÇERLİ** (346 satırlık brief) |
| **Canlı Entegrasyon Testleri** | `rtk uv run pytest -m integration` | **6/6 GEÇTİ** |
| **6 Boyutlu Değerlendirme** | `rtk uv run python -m adk.eval --cases NORM-01 --runs 1` | **6 BOYUTUN TAMAMINDA %100** |

### Doğrulanmış 6 Boyutlu Skor Kartı (Son Çalıştırma):
- Tool Trajectory: **%100.0** (≥%90.0 hedefi)
- Schema Conformance: **%100.0** (≥%95.0 hedefi)
- Safety Boundaries: **%100.0** (%100.0 hedefi)
- Source Traceability: **%100.0** (≥%80.0 hedefi)
- Evidence/Guideline Separation: **%100.0** (≥%90.0 hedefi)
- Uncertainty/Not Found Reporting: **%100.0** (≥%85.0 hedefi)

---

## 5. Bilinen Teknik Sınırlamalar ve Kısıtlar

1. **Vertex AI Araç Kısıtlaması (Search vs Function Calling Çatışması)**:
   - Vertex AI Gemini üzerinde `google_search`, aynı subagent isteğinde fonksiyon bildirim araçları (`set_model_response`) ile birleştirilemez.
   - *Etkisi*: Subagent'lar `output_schema` olmadan `google_search` kullanır; üst Coordinator `output_schema=StructuredEvidenceBriefModel` uygular ve subagent bulgularını doğrulanmış JSON formatında sentezler.
2. **`url_context` Paywall Gecikmesi**:
   - `url_context` harici web sayfalarını kazımaya çalışır. Ücretli tıbbi dergi portallarına (örn. Elsevier, Springer) erişirken istekler sıklıkla takılır veya gecikir.
   - *Varsayılan Ayar*: Üretim çalıştırmalarında `use_url_context=False`; Google Search grounding, ödeme duvarına takılmadan güçlü kaynak alıntıları sağlar.
3. **Yürütme Gecikmesi**:
   - Sıralı arama grounding'i ve detaylı sentez nedeniyle tam multi-agent yürütmesi 45–120 saniye gerektirir.
   - *Hafifletme*: Pytest, entegrasyon testlerini `pytest.mark.integration` ile izole eder; değerlendirme varsayılan olarak `NORM-01` smoke testini çalıştırır.
