# Yerel Web UI Kurulum ve Kullanıcı Kılavuzu (FastAPI + Streamlit)

Bu kılavuz, **Surgical AI Web UI** uygulamasını yerel ortamda çalıştırmak, test etmek ve geliştirmek için adım adım talimatlar sunar.

---

## 🌟 Mimari Genel Bakış

Web UI, [`app/`](../app/) dizininde bulunan iki hafif katmandan oluşur:

- **Backend (FastAPI)**: Multimodal vision endpoint'lerini, multi-agent konsensüs ardışık düzenlerini, sorgu ayrıştırmasını ve [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) adresindeki OpenAPI Swagger belgelerini sunan REST API.
- **Frontend (Streamlit)**: [Google Cloud Generative AI Sample Apps](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/sample-apps/gemini-streamlit-cloudrun) örneklerinden esinlenerek tasarlanan ve [`http://localhost:8501`](http://localhost:8501) adresinde çalışan interaktif, kullanıcı dostu arayüz.
- **Birleşik CLI Başlatıcı ([`app/cli.py`](../app/cli.py))**: Backend'i, frontend'i veya her ikisini aynı anda başlatmak için tek bir komut satırı arayüzü.

---

## 🚀 Ön Koşullar ve Kurulum

### 1. Python Ortamı
Python 3.10+ (Python 3.12 önerilir) ve `uv` paket yöneticisinin yüklü olduğundan emin olun:

> 🪟 **Windows Kullanıcıları**: Ayrıntılı Windows PowerShell/CMD talimatları, sanal ortam komut dosyaları (`.venv\Scripts\Activate.ps1`) ve sorun giderme için özel [Windows Kurulum Kılavuzu](windows-setup-guide-TR.md)'na bakın.

```bash
# Depoyu klonlayın (henüz yapılmadıysa)
git clone https://github.com/devenes/surgical-ai-agents.git
cd surgical-ai-agents

# Sanal ortamı oluşturun ve etkinleştirin
# macOS/Linux üzerinde:
uv venv --python 3.12
source .venv/bin/activate

# Windows üzerinde (PowerShell):
# uv venv --python 3.12
# .venv\Scripts\Activate.ps1

# Tüm proje bağımlılıklarını yükleyin (FastAPI, Streamlit ve dev araçları dahil)
uv pip install -e ".[dev]"
```

---

## 💻 Web UI'ı Yerel Olarak Çalıştırma

Birleşik başlatıcıyı kullanarak uygulamayı üç farklı şekilde başlatabilirsiniz:

### Seçenek A: Backend ve Frontend'i Aynı Anda Başlatın (Önerilen)
```bash
uv run python -m app.cli all
```
Bu komut şunları ayağa kaldırır:
- **Streamlit Web UI**: [`http://127.0.0.1:8501`](http://127.0.0.1:8501)
- **FastAPI Backend**: [`http://127.0.0.1:8000`](http://127.0.0.1:8000) (Swagger Belgeleri: [`/docs`](http://127.0.0.1:8000/docs))

Her iki servisi de düzgün bir şekilde durdurmak için terminalde `Ctrl+C` tuşlarına basın.

---

### Seçenek B: Yalnızca FastAPI Backend'i Başlatın
Gözetimsiz API testleri, curl istekleri veya OpenAPI Swagger keşfi için kullanışlıdır:
```bash
uv run python -m app.cli backend --backend-port 8000
```
- İnteraktif Swagger UI: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- İnteraktif ReDoc: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)
- Sağlık Kontrolü (Health Check): `curl http://127.0.0.1:8000/api/health`

---

### Seçenek C: Yalnızca Streamlit Frontend'i Başlatın
```bash
uv run python -m app.cli frontend --frontend-port 8501
```
*Not: Streamlit uygulaması kenar çubuğunda çift bağlantı modunu destekler: doğrudan işlem içinde (in-process) bağlanabilir veya istekleri çalışan FastAPI REST backend'ine yönlendirebilir.*

---

## ⚡ Sıfır-Token Çevrimdışı Simülasyon Modu (Zero-Token Offline Mode)

Yerel geliştirme, test ve UI demonstrasyonları sırasında API maliyetini ve token kullanımını en aza indirmek için sistem bir **Sıfır-Token Çevrimdışı Modu** içerir:

1. **Varsayılan Durum**: Kenar çubuğunda varsayılan olarak etkindir (`⚡ Zero-Token Offline Mode`).
2. **Davranış**: Harici Vertex AI / Gemini API'lerini çağırmadan anlık, deterministik, yüksek kaliteli multimodal ve multi-agent yanıtları sağlar.
3. **Canlı Moda Geçiş**:
   - Kenar çubuğundaki `⚡ Zero-Token Offline Mode` onay kutusunun işaretini kaldırın.
   - Ortamınızda geçerli Google Cloud Application Default Credentials (`gcloud auth application-default login`) veya `.env` dosyanızda `GOOGLE_API_KEY` ayarlandığından emin olun.

---

## 🎛️ Özellikler ve Sekme Dağılımı

### 1. ⚖️ Benchmark: Agent'lı vs. Agent'sız (Kafa Kafaya Analiz)
- **Pedagojik Karşılaştırma**: Doğrulamasız (ungrounded) zero-shot monolitik bir model ile 2 subagent'lı (Coordinator + Evidence & Guideline Uzmanları) mimarimizi doğrudan karşılaştırır.
- **8 Küratörlü Klinik Senaryo** ([`evaluations/test-cases.yaml`](../evaluations/test-cases.yaml) dosyasından):
  - `NORM-01`: Kolorektal Cerrahide Multimodal Prehabilitasyon *(Normal Kanıt Sentezi)*
  - `NORM-02`: Minimal İnvaziv vs Açık Whipple *(Öğrenme Eğrisi & Kalite Metrikleri)*
  - `NORM-03`: Anastomoz Perfüzyonu İçin ICG Floresans Anjiyografi *(Teknoloji Değerlendirmesi)*
  - `NORM-05`: Hafif Biliyer Pankreatit Kolesistektomi Zamanlaması *(Aynı Yatışta vs Ertelenmiş)*
  - `EDGE-01`: Erken Evre Özofagus Adenokarsinomunda HIFU *(Eksik Ampirik Çalışma Tuzağı)*
  - `EDGE-02`: Fıtık Onarımında Topikal Traneksamik Asit *(Eksik Dernek Kılavuzu Tuzağı)*
  - `EDGE-03`: Kolorektal Mekanik vs Oral Antibiyotikli Bağırsak Hazırlığı *(Uluslararası Kılavuz Çelişkisi)*
  - `EDGE-07`: Albumin 2.8 Olan 72 Yaşındaki Hasta Ameliyat Erteleme *(Güvenlik Reddi Tuzağı)*
- **Yan Yana Mimari Denetim**:
  - Temel model kusurlarını vurgular (halüsinasyon PMID'ler, uydurma kılavuzlar ve doğrudan hasta yönetimi ihlalleri).
  - Multi-agent grounding'i, açık eksik kanıt bildirimini ve otomatik güvenlik reddini sergiler.
- **5 Boyutlu Denetim Skor Kartı**:
  - Grounding & Web İzlenebilirliği
  - Kaynakça Bütünlüğü & Halüsinasyonlar
  - Yapı & PICOT Ayrıştırması
  - Kılavuz & Dernek Atıfları
  - Güvenlik & CDSS Sınırları

### 2. 🤖 Multi-Agent Consensus Studio
- **Coordinator + 2 Subagent Mimarisi**:
  - `Coordinator Agent`: Doğal dil sorgularını PICOT'a ayrıştırır.
  - `Sub-Agent 1 (Evidence Specialist)`: Klinik çalışmaları arar ve sentezler (PubMed).
  - `Sub-Agent 2 (Guideline Specialist)`: Cerrahi derneklerini sorgular (ASCRS, ERAS, SAGES).
  - `Coordinator Sentezi`: Kanıtlar ile kılavuzları karşılaştırır, konsensüs matrisi üretir ve doğrulanmış kaynakları biçimlendirir.
- **Zaman Çizelgesi Adımlayıcısı (Timeline Stepper)**: Adım başına gecikmeyi gösteren görsel yürütme ilerlemesi.
- **Yan Yana Kartlar**: Ampirik bulgular ile dernek kılavuzlarının doğrudan görsel karşılaştırması.

### 3. 👁️ Multimodal Vision Studio
- **Görüntü Girişi**: Özel görüntüler yükleyin (`PNG`, `JPG`, `WEBP`) veya paketle birlikte gelen *Critical View of Safety (CVS)* şemasını seçin.
- **Sorgu Prompt'ları**: Hızlı ön ayarlı prompt'lardan birini seçin (anatomik işaretler, CVS kriterleri, robotik bilgisayarlı görü araştırması) veya özel bir prompt girin.
- **İncelenebilir Sonuçlar**:
  - `Gözlem ve Analiz`: Görsel anlatım ve tespit edilen anatomik yapılar.
  - `Üretim Parametreleri`: Aktif model, gecikme süresi, temperature, top-p ve tahmini token sayısı.
  - `Ham JSON Yükü (Payload)`: Eksiksiz yapılandırılmış API yanıtı.

### 4. ⚡ PICOT Query Decomposer
- Cerrahların klinik sorularını hızlı bir şekilde resmi formatlara dönüştürür:
  - **P**opulation (Popülasyon)
  - **I**ntervention (Girişim)
  - **C**omparator (Karşılaştırıcı)
  - **O**utcomes (Sonlanım Noktaları)
  - **T**imeframe (Zaman Aralığı)
  - Anahtar kelime arama vektörleri

### 5. 📚 Specialist Deep-Dive
- Odaklanmış literatür veya kılavuz kontrolleri için Sub-Agent 1 veya Sub-Agent 2'yi bağımsız olarak sorgulayın.

### 6. ⚙️ API ve Tanılama (Diagnostics)
- FastAPI backend bağlantısını test edin (ping).
- Kimlik bilgisi yapılandırmasını doğrulayın (`GOOGLE_API_KEY`, `GOOGLE_CLOUD_PROJECT`).
- Token tasarruf önerilerini inceleyin.

---

## 🧪 Çevrimdışı Birim Testlerini Doğrulama

Hiçbir token tüketmeden tam çevrimdışı test paketini çalıştırın:

```bash
# Uygulamaya özel testleri çalıştırın (FastAPI + Streamlit yardımcıları)
uv run pytest tests/test_unit_app_*.py -v

# Tüm depo test paketini çalıştırın (61 çevrimdışı birim testi)
uv run pytest
```

61 çevrimdışı testin tamamı, **sıfır API tokeni tüketilerek** yaklaşık 4 saniyede deterministik olarak başarıyla geçer.
