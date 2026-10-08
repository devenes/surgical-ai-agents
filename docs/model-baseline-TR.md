# Gemini 3.8 Model Temel Bildirgesi (Model Baseline Manifest)

- **Belge Sürümü**: 1.0.0
- **Durum**: **DOĞRULANMIŞ & TEST EDİLMİŞ MODEL TEMELİ**
- **Tarih**: 2026-10-03
- **GCP Projesi**: `GOOGLE_CLOUD_PROJECT` ile yapılandırılır
- **Hedef Model**: `gemini-3.8-flash`
- **Hedef Konum**: `us` (çoklu bölge endpoint'i)

---

## 1. Resmi Dokümantasyon ve Özellikler

| Boyut | Özellik | Doğrulama Notları & Resmi Referanslar |
| :--- | :--- | :--- |
| **Model Adı** | `gemini-3.8-flash` | Google GenAI SDK ve Vertex AI'daki resmi tanımlayıcı. |
| **Yayın Aşaması** | Genel Erişilebilirlik (GA) | Üretim düzeyinde "akıllı iş gücü" (workhorse) modeli. |
| **Çıkış Tarihi** | Erken 2026 | Yüksek verimli agent iş akışları için Gemini 2.5/3.7'nin yerini aldı. |
| **Emeklilik Durumu** | Aktif (Mevcut Temel) | Standart yaşam döngüsü boyunca desteklenir; 31 Aralık 2026'ya kadar tanıtım fiyatlandırması. |
| **Desteklenen Bölgeler** | `us` (çoklu bölge), `eu` (çoklu bölge), `global` | **Kritik Bulgu**: Tek bölge `us-central1` `404 NOT_FOUND` döndürür. Çoklu bölge `us` ve `global` endpoint'leri tam olarak desteklenir. |
| **Bağlam Penceresi (Context Window)** | 1.048.576 token (Girdi) / 65.536 token (Çıktı) | Tam 1M token bağlam penceresi. |
| **Search Grounding** | **Destekleniyor & Doğrulandı** | Canlı Google Search grounding aracı (`google.adk.tools.google_search`) işlevsel olarak doğrulandı. |
| **URL Context** | **Destekleniyor** | GenAI SDK / Agent Studio context araçları aracılığıyla desteklenir. |
| **Structured Output** | **Destekleniyor & Doğrulandı** | Yerel JSON Schema ve Pydantic model yanıt üretimi desteklenir. |
| **Agent Studio Erişilebilirliği** | **Destekleniyor & Doğrulandı** | `us` ve `global` konumlarında Agent Studio içinde seçilebilir model. |
| **ADK Uyumluluğu** | **Destekleniyor & Doğrulandı** | `google-adk 2.11.0` ve `google-genai 2.28.0` ile %100 uyumlu olduğu doğrulandı. |
| **Desteklenen Thinking Düzeyleri** | `LOW`, `MEDIUM`, `HIGH` | **Kritik Bulgu**: `thinking_budget` parametresinin yerini aldı. `MINIMAL` **desteklenmez** (API doğrulama hatasına neden olur). `MEDIUM` önerilen standart temeldir. |
| **Örnekleme Parametreleri** | **Kaldırıldı & Deprecated** | **Kritik Bulgu**: `temperature`, `top_p` ve `top_k` kullanımdan kaldırılmıştır ve Gemini 3.8 Flash backend'i tarafından yok sayılır. Akıl yürütme derinliği ve determinizm yalnızca `thinking_level` ile kontrol edilir. Tüm eski örnekleme parametreleri `GenerateContentConfig` içinden çıkarılmalıdır. |
| **Fiyatlandırma** | 1M girdi için $0.75, 1M çıktı için $3.75 | 31 Aralık 2026'ya kadar tanıtım kademesi (sonrasında $1.50 / $7.50). |

---

## 2. Resmi Dokümantasyon Referans Kaynakları

1. **Model Genel Bakışı ve Yetenekleri**:
   - https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models/gemini-3-8-flash
   - https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
2. **Konum ve Bölgesel Endpoint'ler**:
   - https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations
   - https://cloud.google.com/vertex-ai/docs/general/locations
3. **Thinking Yapılandırması ve Düzeyleri**:
   - https://cloud.google.com/vertex-ai/generative-ai/docs/thinking-config
4. **Search Grounding**:
   - https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-with-google-search

---

## 3. Konumlar Genelinde Fiili Model Erişim Doğrulaması

Google Cloud Application Default Credentials (ADC) kullanılarak, aday konumlar genelinde model erişim testleri doğrulandı:

```text
Location us-central1: BAŞARISIZ -> 404 NOT_FOUND
  (Publisher model `projects/<project-id>/locations/us-central1/publishers/google/models/gemini-3.8-flash` bulunamadı)

Location us: BAŞARILI -> PING_OK
  (Çoklu bölge US endpoint'i düşük gecikme ve geçerli çıkarım ile yanıt veriyor)

Location global: BAŞARILI -> PING_OK
  (Global endpoint geçerli çıkarım ile yanıt veriyor)
```

### Konum Kararı
- **Seçilen Konum**: `us`
- **Gerekçe**: `us-central1`, `gemini-3.8-flash` yayıncı endpoint'i ile doldurulmamıştır. Çoklu bölge `us`, `us-central1` bölgesini kapsar, ABD veri sınırı garantilerini korur, ABD veri merkezleri arasında yüksek erişilebilirlik sunar ve düşük gecikmeyle yanıt verir.
