# Google Agent Development Kit (ADK) Kurulum ve Doğrulama Raporu

## Genel Bakış

Bu belge, bu depo içindeki Google Agent Development Kit (ADK) uygulaması için kesin paket adlarını, sürümlerini, doğrulama prosedürlerini ve API arayüzlerini kaydeder.

---

## 1. Doğrulanmış Paketler ve Sürümler

Tüm paketler, `uv` ile yönetilen yalıtılmış bir sanal ortamda (`.venv`) kuruludur:

| Paket | Kurulu Sürüm | Kaynak | Sistemdeki Rolü |
| :--- | :--- | :--- | :--- |
| **`google-adk`** | `2.11.0` | PyPI | Resmi Google Agent Development Kit: agent tanımları, `sub_agents`, orkestrasyon, `Runner`, `AgentEvaluator` |
| **`google-genai`** | `2.28.0` | PyPI | Model çağrılarını destekleyen birleşik Google GenAI SDK (Vertex AI backend) |
| **`google-auth`** | `2.59.1` | PyPI | Application Default Credentials (ADC) token üretimini yönetir |
| **`pydantic`** | `2.13.5` | PyPI | Yapılandırılmış veri modelleri, tip doğrulaması ve çıktı şeması üretimi |
| **`jsonschema`** | `4.26.0` | PyPI | Depo şemalarına karşı katı draft-07 JSON Schema doğrulaması |
| **`pyyaml`** | `6.0.3` | PyPI | Test senaryosu tanımlarının ayrıştırılması (`evaluations/test-cases.yaml`) |

---

## 2. Kurulum Komutları

Doğrulanmış ortamı sıfırdan oluşturmak için:

```bash
# 1. Python 3.12 ile özel sanal ortam oluşturun (Google GenAI SDK uyumluluğu için tercih edilir)
uv venv --python 3.12

# 2. Minimal gerekli bağımlılıkları yükleyin
uv pip install -e .
```

---

## 3. Kimlik Doğrulama Yöntemi

- **Birincil Kimlik Doğrulama**: Google Cloud **Application Default Credentials (ADC)**.
- **Doğrulama Durumu**: **DOĞRULANDI & ÇALIŞIYOR**.
- **Hesap**: ADC ile kimliği doğrulanmış geliştirici hesabı (`gcloud auth application-default login`)
- **Aktif GCP Projesi**: `GOOGLE_CLOUD_PROJECT` ile yapılandırılır (örn. `your-project-id`)
- **Hedef Vertex AI Konumu**: `us` (US çoklu bölge) / `global`
- **Doğrulanan Model Endpoint'leri**:
  - `gemini-3.8-flash` (`publishers/google/models/gemini-3.8-flash`) — Doğrulandı, erişilebilir & varsayılan (`us`, `global`)
  - `gemini-2.5-flash` (`publishers/google/models/gemini-2.5-flash`) — Doğrulandı, erişilebilir (`us-central1`)
- **Kimlik Bilgisi Depolama**: Doğrudan kullanıcı ana dizininde saklanır (`~/.config/gcloud/application_default_credentials.json`). **Bu depoda hiçbir gizli anahtar veya API anahtarı saklanmaz.**

---

## 4. Doğrulanmış ADK API'leri ve Yetenekleri

### Modernize Edilmiş Tek Turlu Uzman Subagent'lar (`sub_agents`)
`google-adk 2.11.0` sürümünde önerilen delegasyon kalıbı, açık tip korumalı `input_schema` ile `mode="single_turn"` kullanır:
```python
from google.adk import Agent
from google.adk.tools import google_search
from adk.schemas import EvidenceQueryInput, GuidelineQueryInput

evidence_agent = Agent(
    name="evidence_agent",
    description="Specialist biomedical literature researcher.",
    model=gemini_model,
    instruction=evidence_instruction,
    tools=[google_search],
    mode="single_turn",
    input_schema=EvidenceQueryInput,
)

guideline_agent = Agent(
    name="guideline_agent",
    description="Specialist surgical practice guidelines researcher.",
    model=gemini_model,
    instruction=guideline_instruction,
    tools=[google_search],
    mode="single_turn",
    input_schema=GuidelineQueryInput,
)
```

### Üst Coordinator Orkestrasyonu
Üst Coordinator, subagent'ları `sub_agents=[...]` aracılığıyla alır. ADK bunları otomatik olarak üst agent üzerinde tip korumalı `_SingleTurnAgentTool` araçlarına dönüştürür:
```python
coordinator = Agent(
    name="coordinator",
    description="Master surgical evidence synthesis coordinator.",
    model=gemini_model,
    instruction=coordinator_instruction,
    sub_agents=[
        evidence_agent,
        guideline_agent,
    ],
    output_schema=StructuredEvidenceBriefModel,
)
```

### Yürütme Çalışma Zamanı (`google.adk.Runner`)
```python
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

runner = Runner(
    app_name="surgical_ai",
    agent=coordinator,
    session_service=InMemorySessionService(),
    auto_create_session=True,
)

async for event in runner.run_async(
    user_id="surgeon",
    session_id="session-1",
    new_message=types.Content(
        role="user",
        parts=[types.Part.from_text(text=research_question)],
    ),
):
    # Resmi ADK doğrulanmış eylem yanıtını kontrol edin
    if hasattr(event, "actions") and event.actions and event.actions.set_model_response:
        structured_brief = event.actions.set_model_response
```

---

## 5. Kritik Sürüme Özgü Davranışlar ve Kurallar

1. **Vertex AI Araç Kısıtlaması (Search vs Function Calling Çatışması)**:
   Vertex AI Gemini API'de, `google_search` ile fonksiyon bildirim araçları (`set_model_response`) aynı istekte birleştirilemez. Eğer `google_search` kullanan bir subagent üzerine doğrudan `output_schema` eklenirse, ADK `set_model_response` enjekte eder ve bu durum Vertex AI'ın `400 INVALID_ARGUMENT: Multiple tools are supported only when they are all search tools` hatası vermesine yol açar.
   *Çözüm*: Subagent'lar `output_schema` olmadan `tools=[google_search]` ve `input_schema=...` barındırır ve kanıt bulgularını coordinator'a döndürür. Doğrudan arama aracı olmayan Coordinator ise `output_schema=StructuredEvidenceBriefModel` taşır ve nihai JSON brief'i sentezler.
2. **`Runner` İçinde `app_name` Zorunluluğu**:
   `google-adk 2.11.0` sürümünde, `Runner` şu hatayı verir: `ValueError: app_name is required when agent is provided without app`. Her zaman açık bir uygulama adı (`app_name="surgical_ai"`) geçilmelidir.
3. **`event.actions` Üzerinden Yapılandırılmış Yanıt Çıkarımı**:
   Subagent'lar ile `output_schema` kullanıldığında, ADK doğrulanmış Pydantic sözlüğünü `event.actions.set_model_response` içinde saklar.
4. **Yerel ADK Değerlendirmesi (`google.adk.evaluation`)**:
   `AgentEvaluator.evaluate_eval_set`, modül `root_agent` veya `get_agent_async()` sunduğunda agent'ları otomatik keşfeder. `adk/coordinator/agent.py` içinde `root_agent = create_coordinator_agent()` dışa aktarılmıştır.
5. **Gemini 3.8 Flash Üretim Parametreleri**:
   `gemini-3.8-flash` için örnekleme parametreleri (`temperature`, `top_p`, `top_k`) kullanımdan kaldırılmıştır (deprecated) ve backend tarafından yok sayılır. Akıl yürütme derinliği yalnızca `thinking_config=types.ThinkingConfig(thinking_level="MEDIUM")` ile yapılandırılır. Tam API uyumluluğu için tüm eski örnekleme parametreleri `GenerateContentConfig` içinden çıkarılmıştır.
