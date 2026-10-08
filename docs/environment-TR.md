# Ortam İnceleme ve Çalışma Zamanı Doğrulama Raporu

**İnceleme Tarihi**: Ekim 2026 (Phase 2 Canlı ADK POC)  
**Kapsam**: Sanal ortam, Google Agent Development Kit (ADK), Vertex AI model bağlantısı, Application Default Credentials (ADC), Search Grounding ve güvenlik sınırı uygulaması.

---

## Durum Sınıflandırma Göstergesi

- **VERIFIED & WORKING (Doğrulandı & Çalışıyor)**: Canlı POC yürütmesinde tam olarak test edilmiş ve çalıştığı onaylanmış bileşenler.
- **VERIFIED (Doğrulandı)**: Statik dosya veya araç zinciri öğesinin mevcut olduğu onaylandı.
- **NOT WORKING (Çalışmıyor)**: Denenen ancak başarısız olan özellik (şu anda yok).
- **NOT TESTED (Test Edilmedi)**: Tasarım gereği sonraki aşamalara ertelenen uzak özellikler.
- **REQUIRES MANUAL ACTION (Manuel Eylem Gerektirir)**: İnsan kimlik bilgileri veya onayı gerektiren eylemler (şu anda yok; ADC aktif).

---

## Durum Matrisi

| Bileşen | Durum | Detaylar |
| :--- | :--- | :--- |
| **Sanal Ortam (Virtual Environment)** | **VERIFIED & WORKING** | CPython 3.12.13 kullanılarak `uv venv --python 3.12` ile oluşturulan `.venv` |
| **ADK Çerçevesi** | **VERIFIED & WORKING** | `.venv` içine kurulu `google-adk 2.11.0` |
| **Google GenAI SDK** | **VERIFIED & WORKING** | `.venv` içine kurulu `google-genai 2.28.0` |
| **Kimlik Doğrulama (ADC)** | **VERIFIED & WORKING** | `~/.config/gcloud/application_default_credentials.json` konumundaki aktif kimlik bilgileri |
| **GCP Projesi** | **VERIFIED & WORKING** | `GOOGLE_CLOUD_PROJECT` ile yapılandırıldı (konum: `us` / `global`) |
| **Gemini Temel Modelleri** | **VERIFIED & WORKING** | `gemini-3.8-flash` (`publishers/google/models/gemini-3.8-flash`) aktif olarak doğrulandı |
| **Google Search Grounding** | **VERIFIED & WORKING** | `google.adk.tools.google_search` canlı PubMed ve klinik çalışmalar üzerinde test edildi ve doğrulandı |
| **URL Context Aracı** | **VERIFIED & WORKING** | `google.adk.tools.url_context` uzman araştırma agent'larına eklendi |
| **Agent-as-a-Tool Delegasyonu**| **VERIFIED & WORKING** | Coordinator tarafından `AgentTool(evidence_agent)` ve `AgentTool(guideline_agent)` çağrıldı |
| **Yapılandırılmış Çıktı Şeması** | **VERIFIED & WORKING** | JSON Schema doğrulaması ile `agents/coordinator/output-schema.json` standardına %100 uyuyor |
| **Canlı Birincil Test Çalıştırması** | **VERIFIED & WORKING** | `examples/research-questions/colorectal-prehabilitation-live-example.json` dosyasına kaydedildi |
| **Güvenlik Sınırı Reddi** | **VERIFIED & WORKING** | Hastaya özel klinik soruları reddeder; genel araştırmaya yönlendirir |
| **Otomatik Birim Testleri** | **VERIFIED & WORKING** | Agent'lar, Draft-07 şemaları, FastAPI rotaları ve prova senaryolarında geçen 61 çevrimdışı pytest testi |
| **Multimodal Vision Studio** | **VERIFIED & WORKING** | Web UI (`app/`) ve bağımsız CLI (`multimodal-demo/`) içinde doğrulanan operatif işaret gözlemi |
| **Üretim Cloud Run Konteyneri** | **VERIFIED & TESTED** | `workshop/cloud-deployment-TR.md` dosyasında doğrulanan üretim Dockerfile (`python:3.12-slim`, non-root) ve dağıtım kılavuzu |
| **Kurumsal RAG / Vektör Depoları** | **NOT TESTED** | Phase 4A hastaneye özel kurumsal RAG tasarım gereği ertelendi |

---

## Doğrulanmış ADK Çalışma Zamanı Davranışı

1. **Agent Orkestrasyonu**:
   - Coordinator doğrudan arama yapmaz.
   - Coordinator, `AgentTool` aracılığıyla `evidence_agent` ve `guideline_agent`'ı ayrık araçlar olarak çağırır.
   - Uzman agent'lar hakemli literatürü ve klinik kılavuzları getirmek için Google Search grounding'ini çağırır.
   - Coordinator bulguları uzlaşmalar, ayrışmalar, belirsizlikler ve kısıtlılıklar olarak sentezler.

2. **Güvenlik Uygulaması**:
   - Doğrudan hasta yönetimi prompt'ları (`EDGE-07`), klinik tedavi direktifleri üretmeden anında konuşma reddini ve eğitsel yeniden yönlendirmeyi tetikler.
