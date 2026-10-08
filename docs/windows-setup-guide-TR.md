# Windows Kurulum ve Yürütme Kılavuzu

Bu kılavuz, Windows 10 ve Windows 11 üzerinde **Surgical AI Agents** sistemini ve **FastAPI + Streamlit Web UI** uygulamasını yüklemek, yapılandırmak ve çalıştırmak için adım adım talimatlar sağlar.

---

## 📋 İçindekiler
1. [Windows Ön Koşulları](#1-windows-ön-koşulları)
2. [Adım Adım Kurulum (PowerShell / CMD)](#2-adım-adım-kurulum-powershell--cmd)
3. [Windows'ta Sanal Ortam Etkinleştirme](#3-windowsta-sanal-ortam-etkinleştirme)
4. [Windows'ta Bağımlılıkları Yükleme](#4-windows-bağımlılıkları-yükleme)
5. [Windows'ta Web UI'ı Çalıştırma](#5-windowsta-web-uıı-çalıştırma)
6. [Windows'ta Google Cloud Kimlik Bilgilerini Yapılandırma](#6-windowsta-google-cloud-kimlik-bilgilerini-yapılandırma)
7. [Windows'ta Sıfır-Token Çevrimdışı Test](#7-windowsta-sıfır-token-çevrimdışı-test)
8. [Windows Sorun Giderme ve SSS](#8-windows-sorun-giderme-ve-sss)

---

## 1. Windows Ön Koşulları

Başlamadan önce aşağıdakilere sahip olduğunuzdan emin olun:

### A. Python 3.10+ (Python 3.12 Önerilir)
- [python.org/downloads/windows](https://www.python.org/downloads/windows/) adresinden indirin.
- ⚠️ **Kurulum sırasında önemli**: Yükleyicinin alt kısmında bulunan **"Add python.exe to PATH"** onay kutusunu işaretleyin!
- **Uygulama Yürütme Diğer Adlarını (App Execution Aliases) Kapatın** (eğer terminalde `python` yazınca Microsoft Store açılıyorsa):
  1. Windows **Ayarlar** (`Win + I`) menüsünü açın.
  2. **Uygulamalar** > **Gelişmiş uygulama ayarları** > **Uygulama yürütme diğer adları** yoluna gidin.
  3. `python.exe` ve `python3.exe` (Uygulama Yükleyicisi) için olan iki anahtarı da **KAPALI** konuma getirin.

### B. Git for Windows
- [git-scm.com/download/win](https://git-scm.com/download/win) adresinden indirin ve varsayılan ayarlarla yükleyin.

### C. uv Paket Yöneticisi (Şiddetle Önerilir)
PowerShell'de tek komutla yükleyin:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 2. Adım Adım Kurulum (PowerShell / CMD)

```powershell
# 1. Depoyu klonlayın
git clone https://github.com/devenes/surgical-ai-agents.git
cd surgical-ai-agents

# 2. Sanal ortamı oluşturun
# uv kullanarak (Önerilen):
uv venv --python 3.12

# VEYA standart Python venv kullanarak:
python -m venv .venv
```

---

## 3. Windows'ta Sanal Ortam Etkinleştirme

Windows'taki etkinleştirme komut dosyaları `.venv\Scripts\` dizininde bulunur (Linux/macOS'taki `.venv/bin/` yerine):

### PowerShell İçinde:
```powershell
.venv\Scripts\Activate.ps1
```

> [!TIP]
> **Eğer `execution of scripts is disabled on this system` hatası alırsanız**:
> PowerShell'i açın ve yerel komut dosyalarına izin vermek için şu tek seferlik komutu çalıştırın:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Ardından `.venv\Scripts\Activate.ps1` komutunu tekrar çalıştırın.

### Komut İstemi (CMD) İçinde:
```cmd
.venv\Scripts\activate.bat
```

### Git Bash İçinde:
```bash
source .venv/Scripts/activate
```

---

## 4. Windows Bağımlılıkları Yükleme

Sanal ortamınız etkinleştirildikten sonra (veya doğrudan `uv` kullanarak):

```powershell
# uv kullanarak (en hızlısı, sanal ortamı otomatik yönetir):
uv pip install -e ".[dev]"

# VEYA standart pip kullanarak:
pip install -e ".[dev]"
```

---

## 5. Windows'ta Web UI'ı Çalıştırma

Web UI, hem **FastAPI REST backend**'ini hem de **Streamlit interaktif frontend**'ini koordine eden birleşik bir başlatıcı (`app/cli.py`) ile birlikte gelir.

### Seçenek A: Her İki Servisi Aynı Anda Başlatın (Önerilen)

```powershell
# uv kullanarak:
uv run python -m app.cli all

# VEYA etkin sanal ortam ile:
python -m app.cli all
```

Başlatıldıktan sonra:
- **Streamlit Web UI**: [http://127.0.0.1:8501](http://127.0.0.1:8501)
- **FastAPI OpenAPI Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Her iki servisi durdurmak için: terminal penceresinde `Ctrl + C` tuşlarına basın.

---

### Seçenek B: Yalnızca FastAPI Backend'i Başlatın

```powershell
uv run python -m app.cli backend --backend-port 8000
```
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresinden interaktif Swagger belgelerine erişin.
- Sağlık endpoint'ini test edin:
  ```powershell
  curl http://127.0.0.1:8000/api/health
  ```

---

### Seçenek C: Yalnızca Streamlit Frontend'i Başlatın

```powershell
uv run python -m app.cli frontend --frontend-port 8501
```

---

## 6. Windows'ta Google Cloud Kimlik Bilgilerini Yapılandırma

### Sıfır-Token Çevrimdışı Modu (Google Cloud Hesabı Gerekmez)
Varsayılan olarak Web UI, kenar çubuğunda **Zero-Token Offline Mode** etkinleştirilmiş olarak çalışır. Tüm multimodal vision özelliklerini, 2 subagent'lı konsensüs ardışık düzenlerini ve PICOT sorgu ayrıştırmasını **0 token tüketimiyle** ve **hiçbir bulut kimlik bilgisi gerekmeden** inceleyebilirsiniz!

### Canlı Mod (Vertex AI / Gemini API)

Google Cloud üzerinde Vertex AI'a karşı canlı sorgular çalıştırmak isterseniz:

1. [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) adresinden Windows için Google Cloud SDK'yı yükleyin.
2. Application Default Credentials (ADC) ile kimlik doğrulaması yapın:
   ```powershell
   gcloud auth application-default login
   ```
   *Bu işlem kimlik bilgilerinizi `%APPDATA%\gcloud\application_default_credentials.json` konumuna kaydeder.*

3. `.env` dosyanızı yapılandırın:
   ```powershell
   Copy-Item .env.example .env
   ```
   Notepad veya VS Code kullanarak `.env` dosyasını düzenleyin:
   ```env
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   GOOGLE_CLOUD_LOCATION=us
   GEMINI_MODEL=gemini-3.8-flash
   ```

4. Veya PowerShell'de geçici ortam değişkenleri ayarlayın:
   ```powershell
   $env:GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   $env:GOOGLE_CLOUD_LOCATION="us"
   ```

---

## 7. Windows'ta Sıfır-Token Çevrimdışı Test

Windows üzerinde hiçbir API tokeni tüketmeden çevrimdışı birim test paketini çalıştırmak için:

```powershell
# Tüm çevrimdışı test paketini çalıştırın (61 birim testi)
uv run pytest

# Yalnızca Web UI & Karşılaştırmalı Benchmark birim testlerini çalıştırın
uv run pytest tests/test_unit_app_*.py -v
```

61 çevrimdışı testin tümü, **0 API tokeni tüketilerek** yaklaşık 4 saniyede deterministik olarak başarıyla geçer. Bu testler şunları doğrular:
- Multimodal görüntü özellik çıkarma simülasyonu
- 2-Subagent konsensüs orkestrasyon ardışık düzeni
- PICOT ayrıştırma mantığı
- 16 klinik benchmark senaryosunun tamamında (8 normal, 8 edge) kafa kafaya karşılaştırmalı analiz (`/api/agents/compare`)
- Klinik güvenlik korkulukları (hastaya özel tavsiyelerin tanısal olmayan reddi)
- Tam podyum provası doğrulaması (`tests/test_unit_offline_rehearsal.py`)

---

## 8. Windows Sorun Giderme ve SSS

### S1: PowerShell'de sanal ortam etkinleştirilirken `Set-ExecutionPolicy` hatası
**Belirti**: `cannot be loaded because running scripts is disabled on this system.`  
**Çözüm**: Çalıştırın:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### S2: `Address already in use` hatası (Port 8000 veya 8501)
**Belirti**: `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`  
**Çözüm**: Başka bir uygulama veya önceki bir terminal işlemi portu kullanıyor.
1. Port 8000'i neyin kullandığını kontrol edin:
   ```cmd
   netstat -ano | findstr :8000
   ```
2. Veya uygulamayı farklı bir portta çalıştırın:
   ```powershell
   uv run python -m app.cli all --backend-port 8080 --frontend-port 8502
   ```

---

### S3: Windows Defender Güvenlik Duvarı İstemi
**Belirti**: Windows Güvenlik Duvarı penceresi *"Windows Defender Güvenlik Duvarı bu uygulamanın bazı özelliklerini engelledi"* uyarısı verir.  
**Çözüm**: **"Özel ağlar (Private networks)"** kutusunu işaretleyin ve **"Erişime izin ver (Allow access)"** seçeneğine tıklayın. Uygulama yalnızca yerel makinede (`127.0.0.1`) iletişim kurar.

---

### S4: Terminal kodlaması / Türkçe karakter veya emoji görüntüleme
**Belirti**: Windows Komut İsteminde garip semboller veya `UnicodeEncodeError`.  
**Çözüm**: Windows konsolunuzun UTF-8 için yapılandırıldığından emin olun:
- CMD içinde:
  ```cmd
  chcp 65001
  ```
- PowerShell içinde:
  ```powershell
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  ```
- Tam emoji ve UTF-8 desteği için modern [Windows Terminal](https://aka.ms/terminal) (Windows 11'de yerleşiktir) kullanın.

---

### S5: Windows MAX_PATH Sınırlaması (260 karakter)
**Belirti**: Derin iç içe geçmiş dizinlerde paket yüklerken hatalar oluşması.  
**Çözüm**: PowerShell'de uzun dosya yollarını etkinleştirin (Yönetici olarak çalıştırın):
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
