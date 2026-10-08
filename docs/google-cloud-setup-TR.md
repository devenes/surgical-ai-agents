# Google Cloud Kurulum ve Ön Koşullar Kılavuzu

## Genel Bakış

Bu kılavuz, multi-agent sistemini Google Cloud Vertex AI ve Gemini servislerine bağlamak için gereken ön koşulları ve yapılandırma adımlarını açıklamaktadır.

---

## 1. Doğrulanmış Google Cloud Proje Yapılandırması

| Yapılandırma Öğesi | Durum | Doğrulanmış Değer | Rehberlik |
| :--- | :--- | :--- | :--- |
| **GCP Project ID** | **DOĞRULANDI & ÇALIŞIYOR** | `GOOGLE_CLOUD_PROJECT` ile yapılandırılır | Aktif Vertex AI erişimine sahip hedef proje. |
| **Birincil Bölge (Region)** | **DOĞRULANDI & ÇALIŞIYOR** | `us` (US çoklu bölge) | Gemini 3.8 Flash model endpoint'leri için varsayılan konum (`global` da doğrulandı). |
| **Kimlik Doğrulama** | **DOĞRULANDI & ÇALIŞIYOR** | Application Default Credentials (ADC) | `gcloud auth application-default login` ile yapılandırılır. |
| **Doğrulanmış Modeller** | **DOĞRULANDI & ÇALIŞIYOR** | `gemini-3.8-flash` | Model endpoint'inin Vertex AI üzerinde erişilebilir olduğu doğrulandı (`us` ve `global`). |
| **Search Grounding** | **DOĞRULANDI & ÇALIŞIYOR** | Google Search Grounding | `google.adk.tools.google_search` aracılığıyla çalışır. |

---

## 2. Google Cloud API'leri

Aşağıdaki API'ler etkindir ve multi-agent sistemi tarafından kullanılır:

- **Vertex AI API** (`aiplatform.googleapis.com`): `google-genai` ve `google-adk` üzerinden Gemini model çıkarımı (inference) için gereklidir.
- **Search Grounding**: Vertex AI araç yürütmesi üzerinden yerel olarak kullanılır.

Bu API'leri yeni bir GCP projesinde etkinleştirmek için:
```bash
gcloud services enable \
    aiplatform.googleapis.com \
    discoveryengine.googleapis.com
```

---

## 3. Kimlik ve Erişim Yönetimi (IAM) Rolleri

Erişim, En Az Yetki İlkesini (Principle of Least Privilege) takip eder:

### Yerel Geliştirme / Workshop Kolaylaştırıcıları (Doğrulanmış Yol)
Geliştiriciler, Google Cloud Application Default Credentials (ADC) kullanarak geliştirici hesaplarıyla kimlik doğrulaması yapar:
```bash
gcloud auth application-default login
```
Bu işlem, kullanıcı kimlik bilgilerini bu deponun dışında, güvenli bir şekilde `~/.config/gcloud/application_default_credentials.json` konumunda saklar. Hiçbir API anahtarı veya servis hesabı anahtarı depolanmaz veya gerekmez.

### Otomatik Servis Hesabı Yürütmesi (CI/CD veya Konteyner İçin İsteğe Bağlı)
Gözetimsiz otomatik ardışık düzenlerde veya konteyner ortamlarında (örn. Cloud Run) çalışırken:
1. Özel bir servis hesabı oluşturun: `surgical-ai-agent-runner@[GCP-PROJECT-ID].iam.gserviceaccount.com`
2. En Az Yetki İlkesine sıkı sıkıya bağlı kalarak minimal roller atayın:
   - **Vertex AI User** (`roles/aiplatform.user`): Gemini model çıkarımı ve tahmin API çağrıları için gereklidir.
   - **Discovery Engine Viewer** (`roles/discoveryengine.viewer`, isteğe bağlı): Search grounding için kurumsal Discovery Engine veri depoları entegre ediliyorsa gereklidir.
   - **Cloud Run Invoker** (`roles/run.invoker`, isteğe bağlı): Cloud Run'a dağıtılan konteyner servislerini çağırmak için gereklidir.

> [!IMPORTANT]
> **Bölgesel Endpoint Kısıtlaması**:
> Temel model `gemini-3.8-flash`, çoklu bölge **`us`** ve **`global`** üzerinde mevcuttur. Tek bölge `us-central1` üzerinde dağıtım yapmak veya çalıştırmak, model yayıncı endpoint'i için `404 NOT_FOUND` hatası döndürür. Her zaman `GOOGLE_CLOUD_LOCATION=us` (veya `global`) olarak ayarlayın.

---

## 4. Model ve Grounding Aracı Yapılandırması

### Temel Modeller (Foundation Models)
- **Coordinator Agent**: Vertex AI üzerinde `gemini-3.8-flash` (`us` çoklu bölge).
- **Evidence Agent**: Google Search grounding ve URL context araçları eklenmiş `gemini-3.8-flash`.
- **Guideline Agent**: Google Search grounding ve URL context araçları eklenmiş `gemini-3.8-flash`.

### Grounding Araçları
- **`google_search`**: Hakemli literatürü ve klinik kılavuzları getirmek için gerçek zamanlı doğrulanmış sorgular yürüten yerleşik ADK aracı (`google.adk.tools.google_search`).
- **`url_context`**: Hedeflenen URL incelemesi için yerleşik ADK aracı (`google.adk.tools.url_context`).

---

## 5. Ortam Yapılandırması

Proje veya konum varsayılanlarını geçersiz kılmak için `.env.example` dosyasını `.env` (gitignored) olarak kopyalayın:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us
GEMINI_MODEL=gemini-3.8-flash
```
