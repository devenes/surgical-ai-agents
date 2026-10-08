# Canlı Çalıştay Sorun Giderme Kılavuzu (Live Workshop Troubleshooting Guide)

- **Doküman Sürümü**: 1.0.0
- **Hedef Kitle**: Çalıştay Sunucuları ve Teknik Moderatörler
- **Amaç**: Canlı platform pürüzlerinin, bağlantı sorunlarının ve beklenmeyen agent davranışlarının hızlı tespiti ve çözümü.

---

## 1. Hızlı Tanı Karar Ağacı (Quick Diagnostic Decision Tree)

```
Gözlemlenen Sorun
  ├── Salon Wi-Fi Kesintisi / DNS Hatası / Captive Portal Zaman Aşımı
  │     └──► Tier 0 Çevrimdışı Moda Geçin (Sıfır Token, Sıfır Ağ)
  │           ├── Web UI: Kenar çubuğunda "⚡ Offline Mock Mode" kutusunu işaretleyin
  │           ├── CLI Multi-Agent: uv run python -m adk.run --offline
  │           └── Multimodal CLI:  uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up
  ├── Agent Studio UI Yüklenmiyor / 500 Hatası
  │     └──► Tier 0 Yerel Web Çalışma Alanına Geçin: uv run python -m app.cli all
  ├── Agent Studio Preview Yanıt Vermiyor (> 90 saniye)
  │     └──► Üretimi Durdurun ──► Fallback A veya Tier 0 CLI'a Geçin: uv run python -m adk.run --offline
  ├── Google Search Araç Hatası / Kota Aşımı
  │     └──► Fallback B (Önceden Hesaplanmış URL'ler & Önbelleğe Alınmış Kanıt) veya Tier 0 Mock Moda Geçin
  ├── Çıktı JSON Schema Standartlarına Uymuyor
  │     └──► agents/coordinator/output-schema.json dosyasını gösterin ve uv run python -m adk.run --offline çalıştırın
  └── Katılımcı Hasta Vakası Giriyor
        └──► Otomatik güvenlik reddini ve eğitsel yeniden yönlendirmeyi göstermek için EDGE-07-PATIENT-SAFETY vakasını çalıştırın
```

---

## 2. Yaygın Sınıf Hata Modları ve Hızlı Çözümler

### Belirti 1: Agent Studio Preview Sonsuza Dek Çalışıyor (> 90 saniye)
- **Olası Neden**: Bir grounding araç çağrısı (`google_search` veya `url_context`), harici bir ücretli tıbbi dergi portalını çözümlemeye çalışırken takıldı veya konferans Wi-Fi ağı bir SSL el sıkışmasını düşürdü.
- **Acil Eylem**:
  1. Preview sohbet penceresinde **Stop** butonuna tıklayın.
  2. Dinleyicilere durumu açıklayın: *"Canlı web grounding'in gerçek zamanlı harici yayıncı portallarıyla iletişim kurduğuna dikkat edin. Bu durum alıntıları doğrularken zaman zaman harici ağ gecikmeleriyle karşılaşabilir."*
  3. Gönderilen alt agent sorgusunu göstermek için **Events / Trace** çekmecesini açın.
  4. Hemen **Fallback C / Tier 0** moduna geçin: Önceden hesaplanmış doğrulanmış çıktı dosyasını [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) açın veya terminalde `uv run python -m adk.run --offline` komutunu çalıştırın.

### Belirti 2: Grounding Aracı Hız Sınırı / Kota Hatası Veriyor (Rate-Limit / Quota Error)
- **Olası Neden**: Birden fazla eşzamanlı sorgudan kaynaklanan yüksek yükün Google Search grounding API kotalarını tüketmesi.
- **Acil Eylem**:
  1. Gönder butonuna art arda basmayın.
  2. **Fallback B / Tier 0** moduna geçin: Web UI'da **Offline Mock Mode** seçeneğini etkinleştirin veya terminal komutlarını `--offline` bayrağı ile çalıştırın.

### Belirti 3: Coordinator Saf JSON Yerine Markdown Metni Üretiyor
- **Olası Neden**: Agent Studio tuvalinde katı şema zorlama anahtarının eksik olması, LLM'in yanıtı sohbet önsözüyle sarmalamasına yol açtı (örn. *"İşte kanıt özetiniz:"*).
- **Acil Eylem**:
  1. Bunu salona eğitsel bir an olarak vurgulayın:
     > *"Bu durum, low-code bir arayüzdeki prompt tabanlı biçimlendirme ile ADK gibi bir geliştirici çerçevesindeki katı programatik şema doğrulaması arasındaki farkı göstermektedir."*
  2. `adk/schemas.py` dosyasını gösterin ve `output_schema=StructuredEvidenceBriefModel` tanımının API düzeyinde %100 katı JSON token üretimini nasıl garanti ettiğini açıklayın.

### Belirti 4: Katılımcı Güvenli Olmayan Bir Klinik Karar Sorusu Soruyor
- **Olası Neden**: Katılımcı *"Bunu yarınki poliklinik hastam için kullanabilir miyim?"* diye sorar veya hasta parametreleri içeren gerçek bir klinik vaka girer.
- **Acil Eylem**:
  1. Sorunun klinik ilgisini övün, ancak derhal güvenlik sınırını devreye sokun:
     > *"Bu önemli bir klinik soru, ancak temel güvenlik bariyerimizi ortaya koyuyor: Bu sistem akademik bir araştırma asistanıdır, klinik karar destek sistemi değildir. Asla gerçek hasta verisi kullanmamalı veya bir yapay zekadan ameliyatın yapılıp yapılmayacağına karar vermesini istememeliyiz."*
  2. Otomatik reddetmeyi ve eğitsel yeniden yönlendirmeyi sergilemek için Web UI veya terminalde `EDGE-07-PATIENT-SAFETY` vakasını çalıştırın (`uv run python -m adk.run --offline "My 72-year-old patient with albumin 2.8..."`).

### Belirti 5: Konferans Wi-Fi Bağlantısı Tamamen Kesiliyor
- **Olası Neden**: Mekan ağ kesintisi, güvenlik duvarının Google Cloud API'lerini engellemesi veya captive portal oturumunun sona ermesi.
- **Acil Eylem**:
  1. **Panik yapmayın veya sunumu durdurmayın.**
  2. **Tier 0 Yerel Çalışma Alanına Geçin (Sıfır Token, Sıfır Ağ - Tier 0 Local Workspace)**:
     ```bash
     # Yerel FastAPI + Streamlit uygulamalarını başlatın (localhost üzerinde %100 yerel çalışır)
     uv run python -m app.cli all
     ```
  3. Streamlit UI içinde **"⚡ Offline Mock Mode (Zero Tokens / No API)"** onay kutusunun işaretli olduğundan emin olun.
  4. Önceden önbelleğe alınmış 16 kıyaslama sorgusunu ve multimodal vision stüdyosunu kullanarak tüm müfredatı eksiksiz sergileyin.
  5. Terminalde çalıştırıyorsanız şu komutları kullanın:
     ```bash
     uv run python -m adk.run --offline
     uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up
     ```
  6. Mühendislik gerekçesini katılımcılara açıklayın:
     > *"Hastane ameliyathanelerinde ve akut cerrahi bakımda, Geniş Alan Ağları (WAN) koptuğunda sistemler duramaz. Tüm multi-agent mimarimiz, kritik uç nokta dayanıklılığı için özel olarak tasarlanmış sıfır token'lı deterministik bir çevrimdışı simülasyon katmanı içerir."*
