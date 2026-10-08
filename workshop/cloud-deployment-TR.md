# Cloud Run ve Konteyner Dağıtım Kılavuzu (Ek Kulvar)

> **Mimari Bildirim**:
> Bu dağıtım kulvarı, üretim ortamında barındırma, hastane içi kurumsal paylaşım veya Google Cloud üzerinde sürekli hazırlık (staging) için tasarlanmış **ek / ileri düzey bir seçenektir**.
> **60 dakikalık çalıştayın birincil yolu, low-code Agent Studio görsel tasarımcısı ve yerel ADK geliştirme ortamı olmaya devam etmektedir.**

---

## Genel Bakış (Overview)

Eksiksiz Cerrahi AI Web Studio'yu (Streamlit UI + FastAPI arka uç + 16 kıyaslama vakası) **Google Cloud Run** üzerine şu iki yöntemden biriyle dağıtabilirsiniz:
1. **Cloud Buildpacks ile Doğrudan Kaynaktan Dağıtım (Source-based deployment)** (en hızlı yöntem, Dockerfile gerektirmez)
2. **Google Artifact Registry Üzerinden Özel Üretim Dockerfile** (maksimum güvenlik, non-root kullanıcı, açık katmanlar)

Her iki dağıtım yolu da, yalnızca `roles/aiplatform.user` rolü ile sınırlandırılmış özel bir Custom Service Account (`surgical-agent-sa`) kullanarak **En Az Yetki İlkesi**ne (Principle of Least Privilege) tam olarak uyar.

---

## Yöntem 1: Doğrudan Kaynaktan Dağıtım (Cloud Buildpacks)

Doğrudan kaynaktan dağıtım yapmak, yerel Docker arka plan süreçlerini (daemon) yönetmek istemeyen katılımcılar için hızlı geliştirmeler ve çalıştay gösterimleri açısından idealdir.

### Adım 1: Özel Service Account Oluşturma (En Az Yetki - Least Privilege)

```bash
# Etkin projenizi ve bölgelerinizi ayarlayın
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"      # Cloud Run işlem bölgesi
export VERTEX_LOCATION="us"     # gemini-3.8-flash için Vertex AI multi-region konumu (us-central1 404 döner)

# Özel, ayrıcalıksız bir service account oluşturun
gcloud iam service-accounts create surgical-agent-sa \
  --description="Dedicated service account for Surgical AI ADK Agent on Cloud Run" \
  --display-name="Surgical Agent Service Account"
```

### Adım 2: En Az Yetkili IAM Rollerini Tanımlama

Yalnızca Gemini Enterprise Agent Platform kullanıcı rolünü (`roles/aiplatform.user`) tanımlayın:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Adım 3: Kaynaktan Cloud Run'a Dağıtma

Cloud Run deponuzu otomatik olarak analiz eder, `requirements.txt` dosyasını tespit eder ve güvenli bir çalışma zamanı konteyneri derlemek için Google Cloud Buildpacks kullanır:

```bash
gcloud run deploy surgical-ai-studio \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --labels workshop=cerrahi-kongresi \
  --command "/cnb/lifecycle/launcher" \
  --args "sh,-c,python3 -m streamlit run app/frontend/main.py --server.port=\$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false --server.headless=true" \
  --service-account "surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --set-env-vars GOOGLE_GENAI_USE_ENTERPRISE=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$VERTEX_LOCATION
```

> **Not**: Derlenen konteynerleri depolamak için bir Artifact Registry Docker deposu oluşturulması istenirse (örn. *Do you want to continue (Y/n)?*), `Y` tuşuna basın. Buildpack derlemesi yaklaşık 3–4 dakika sürer.

---

## Yöntem 2: Özel Üretim Dockerfile ve Artifact Registry

Kurumsal hastane uyumluluğu, internete kapalı (air-gapped) klinik intranetler veya katı konteyner güvenlik açığı taramaları için depodaki üretim [`Dockerfile`](../Dockerfile) dosyasını kullanın.

### Dockerfile Güvenlik Mimarisi
- **Temel İmaj (Base Image)**: Minimum CVE riski ve küçük imaj boyutu için `python:3.12-slim`.
- **En Az Yetkili Kullanıcı**: `appgroup` (GID 10001) içinde non-root `appuser` (UID 10001) olarak çalışır.
- **Ortam Bayrakları**: `PYTHONUNBUFFERED=1` ve `PYTHONDONTWRITEBYTECODE=1`.
- **Sağlık Kontrolü (Healthcheck)**: Periyodik olarak `http://localhost:${PORT}/_stcore/health` adresini yoklar.
- **Esnek Giriş Noktası (Entrypoint)**: [`docker-entrypoint.sh`](../docker-entrypoint.sh) şunları destekler:
  - `streamlit` (varsayılan: `$PORT` üzerinde Streamlit çalıştırır)
  - `backend` (`$PORT` üzerinde uvicorn ile FastAPI çalıştırır)
  - `all` (dahili 8000 portunda FastAPI ve `$PORT` üzerinde Streamlit çalıştırır)
  - `rehearse` (sıfır token'lı simülasyon provasını yürütür)

### Adım 1: Yerel Olarak Derleme ve Doğrulama

```bash
# 1. Yerel konteyner imajını derleyin
docker build -t surgical-ai-agents:latest .

# 2. Konteyner içinde otomatik sıfır token simülasyon provasını çalıştırın
docker run --rm surgical-ai-agents:latest rehearse

# 3. Etkileşimli web uygulamasını yerel olarak test edin
docker run -d --name surgical-ai-app -p 8080:8080 -e PORT=8080 surgical-ai-agents:latest

# 4. Sağlık kontrolünü doğrulayın
curl -I http://localhost:8080/_stcore/health

# 5. Yerel test konteynerini temizleyin
docker stop surgical-ai-app && docker rm surgical-ai-app
```

### Adım 2: Google Artifact Registry'ye Push Etme

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"      # Cloud Run işlem bölgesi
export VERTEX_LOCATION="us"     # gemini-3.8-flash için Vertex AI multi-region konumu (us-central1 404 döner)
export REPO="surgical-ai-repo"

# 1. Artifact Registry içinde Docker deposu oluşturun
gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION \
  --description="Docker repository for Surgical AI multi-agent workshop"

# 2. Docker kimlik doğrulamasını yapılandırın
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

# 3. Konteyner imajını etiketleyin ve push edin
docker tag surgical-ai-agents:latest $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/surgical-ai-studio:latest
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/surgical-ai-studio:latest
```

### Adım 3: Önceden Derlenmiş İmajı Cloud Run'a Dağıtma

```bash
gcloud run deploy surgical-ai-studio \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/surgical-ai-studio:latest \
  --region $REGION \
  --allow-unauthenticated \
  --service-account "surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --set-env-vars GOOGLE_GENAI_USE_ENTERPRISE=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$VERTEX_LOCATION
```

---

## 💬 Tartışma: Konteyner Dağıtımı vs. Kaynak Dağıtımı ve IAM Güvenliği

### 1. Cloud Run uygulamamızı Dockerfile olmadan nasıl derledi?
`gcloud run deploy --source .` komutu kullanıldığında, Cloud Run arka planda **CNCF Buildpacks** altyapısından yararlanır. Buildpacks kök dizini inceler: `requirements.txt` ve Python kaynak dosyalarını tespit ettiğinde, buildpack motoru otomatik olarak güvenli bir Python çalışma zamanı seçer, çok katmanlı bir konteyner oluşturur, bağımlılıkları yükler ve başlatıcıyı hazırlar.

- **Kaynaktan Dağıtım (`--source .`)**: Hızlı prototipleme ve sınıf içi kod laboratuvarları için idealdir. Yerel Docker daemon kurulumu gerektirmez.
- **Özel `Dockerfile`**: Kurumsal uyumluluk, özel C/sistem kütüphaneleri, deterministik çok aşamalı önbellekleme ve non-root kullanıcı zorunluluğu için şarttır.

### 2. Varsayılan Compute Engine hesabı yerine neden özel bir Service Account?
**Öncelik güvenlik ve klinik veri korumasıdır.**
- Varsayılan Compute Engine service account (`{PROJECT_NUMBER}-compute@developer.gserviceaccount.com`), varsayılan olarak geniş kapsamlı **Editor (`roles/editor`)** rolüne sahiptir.
- Bu hesap altında çalışan bir uygulama bir yazılım bağımlılığı açığı veya prompt enjeksiyonu zafiyeti içeriyorsa, bir saldırgan Google Cloud projeniz genelindeki tüm bulut depolama kovalarını (buckets), veritabanlarını veya sanal makineleri okuyabilir, değiştirebilir veya silebilir.
- Özel bir service account (`surgical-agent-sa`) tanımlayarak ve **yalnızca** `roles/aiplatform.user` rolünü bağlayarak **En Az Yetki İlkesi**ni uygularız: Konteyner, Vertex AI üzerindeki Gemini temel modellerini çağırmak için gereken tam izinlere sahiptir ve başka hiçbir kaynağa erişemez.

---

## 🧹 Maliyet Yönetimi ve GCP Temizlik Protokolü

Çalıştay veya test oturumunuz tamamlandıktan sonra Google Cloud üzerinde devam eden depolama veya barındırma ücretlerinden kaçınmak için aşağıdaki temizleme komutlarını çalıştırın:

```bash
# 1. Cloud Run servisini silin (işlem örneklerini sonlandırır)
gcloud run services delete surgical-ai-studio \
  --region $REGION \
  --quiet

# 2. Artifact Registry deposunu silin (saklanan konteyner imajlarını kaldırır)
gcloud artifacts repositories delete $REPO \
  --location=$REGION \
  --quiet

# 3. Özel service account'u silin
gcloud iam service-accounts delete surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --quiet
```
