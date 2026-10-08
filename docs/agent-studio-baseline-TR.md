# Agent Studio Temel Yapılandırma Bildirgesi (Baseline Configuration Manifest)

- **Belge Sürümü**: 1.0.0
- **Temel Tarihi**: 2026-10-03
- **Temel Hedefi**: Google Cloud Gemini Enterprise Agent Platform (Vertex AI Agent Studio)
- **Durum**: **DONDURULMUŞ TEMEL (FROZEN BASELINE)** (Phase 6A)

---

## 1. Sınıflandırma Standardı

Bu temel manifestodaki her özellik üç katı kademeden birine göre sınıflandırılmıştır:

- **`VERIFIED BY MANUAL TEST` (Manuel Test ile Doğrulandı)**: Bu proje ortamında doğrudan yürütülmüş ve çalıştığı onaylanmış özellikler (Google Cloud Console'da canlı yürütme veya doğrulanmış programatik ayna aracılığıyla).
- **`DOCUMENTATION ASSUMPTION` (Dokümantasyon Varsayımı)**: Resmi Google Cloud / Vertex AI ürün belgelerinde veya şartnamelerinde belirtilen ancak bu çalışma alanında tüm sınır koşulları altında ayrı ayrı stres testine tabi tutulmamış özellikler.
- **`NOT YET VERIFIED` (Henüz Doğrulanmadı)**: Manuel test yürütmesi veya canlı inceleme ile henüz doğrulanmamış beklenen davranışlar.

---

## 2. Temel Agent Yapılandırması

| Nitelik | Değer / Özellik | Doğrulama Kademesi | Doğrulama Notları & Mekaniği |
| :--- | :--- | :---: | :--- |
| **GCP Project ID** | `GOOGLE_CLOUD_PROJECT` ile yapılandırılır | **VERIFIED BY MANUAL TEST** | ADC ile kimliği doğrulanmış aktif proje. |
| **Bölge (Region)** | `us` (US çoklu bölge) | **VERIFIED BY MANUAL TEST** | `gemini-3.8-flash` için çoklu bölge `us` test edildi ve aktif olduğu onaylandı (Not: `us-central1` 404 döndürür). |
| **Alternatif Bölge** | `global` | **DOCUMENTATION ASSUMPTION** | Google tarafından `gemini-3.8-flash` için desteklendiği belgelenmiştir. |
| **Model** | `gemini-3.8-flash` | **VERIFIED BY MANUAL TEST** | Vertex AI üzerinde onaylanmış GA model tanımlayıcısı; düşük gecikme, yüksek akıl yürütme sadakati. |
| **Thinking Düzeyi** | `MEDIUM` | **VERIFIED BY MANUAL TEST** | ADK ve GenAI SDK yapılandırmasında doğrulandı. Akıl yürütme derinliğini kontrol eder; eski örnekleme parametrelerinin yerini alır. |
| **Örnekleme Parametreleri** | Yok (çıkarıldı) | **VERIFIED BY MANUAL TEST** | `temperature`, `top_p`, `top_k` Gemini 3.8 Flash backend'inde kullanımdan kaldırılmış ve yok sayılmıştır. |
| **Dağıtım Durumu** | Kaydedildi & İnteraktif Preview | **VERIFIED BY MANUAL TEST** | Agent tuvali kaydedildi; yürütme yerleşik Preview paneli aracılığıyla test edildi. |
| **Cloud Run Üretim Endpoint'i** | Ertelendi | **DOCUMENTATION ASSUMPTION** | Agent Studio UI'da tek tıkla dağıtım mevcuttur ancak workshop kapsamı dışındadır. |

---

## 3. Agent Topolojisi ve Uzman Rolleri

### A. Root Coordinator Agent

- **Agent Name**: `surgical-evidence-coordinator` (`VERIFIED BY MANUAL TEST`)
- **Display Name**: `Surgical Evidence Coordinator` (`VERIFIED BY MANUAL TEST`)
- **Node Type**: Kök Agent / Tuval Giriş Noktası (`VERIFIED BY MANUAL TEST`)
- **Sistem Talimatları**: `agents/agent-studio/coordinator-instructions.md` dosyasındaki tam metin (`VERIFIED BY MANUAL TEST`)
- **Eklenen Araçlar**: **Yok** (`VERIFIED BY MANUAL TEST`)  
  *Gerekçe*: Google Search'ün doğrudan Coordinator'a eklenmesi, Vertex AI üzerinde yapılandırılmış JSON çıktı üretimi ile araç bildirim çakışmalarına yol açar.
- **Eklenen Subagent'lar**:  
  1. `evidence-specialist` (`VERIFIED BY MANUAL TEST`)  
  2. `guideline-specialist` (`VERIFIED BY MANUAL TEST`)
- **Çıktı Şeması**: `agents/coordinator/output-schema.json` standardına uyan prompt ile zorunlu kılınmış JSON (`VERIFIED BY MANUAL TEST`).

### B. Evidence Specialist (Yerel Subagent)

- **Agent Name**: `evidence-specialist` (`VERIFIED BY MANUAL TEST`)
- **Display Name**: `Evidence Research Agent` (`VERIFIED BY MANUAL TEST`)
- **Node Type**: Yerel Subagent (Coordinator'a bağlı alt düğüm) (`VERIFIED BY MANUAL TEST`)
- **Sistem Talimatları**: `agents/agent-studio/evidence-instructions.md` dosyasındaki tam metin (`VERIFIED BY MANUAL TEST`)
- **Model**: `gemini-3.8-flash` (`VERIFIED BY MANUAL TEST`)
- **Eklenen Araçlar**:
  - `Google Search` (Grounding with Google Search etkin) (`VERIFIED BY MANUAL TEST`)
  - `URL Context` (Web URL incelemesi) (`DOCUMENTATION ASSUMPTION` - araç çekmecesinde mevcuttur ancak ödeme duvarı takılmalarını önlemek için varsayılan olarak devre dışıdır)
- **Rolü**: PRISMA/RKÇ kademelerine, çalışma metodolojisine, örneklem büyüklüklerine ve birincil klinik sonlanım noktalarına odaklanan literatür getirme (`VERIFIED BY MANUAL TEST`).

### C. Guideline Specialist (Yerel Subagent)

- **Agent Name**: `guideline-specialist` (`VERIFIED BY MANUAL TEST`)
- **Display Name**: `Guideline Specialist Agent` (`VERIFIED BY MANUAL TEST`)
- **Node Type**: Yerel Subagent (Coordinator'a bağlı alt düğüm) (`VERIFIED BY MANUAL TEST`)
- **Sistem Talimatları**: `agents/agent-studio/guideline-instructions.md` dosyasındaki tam metin (`VERIFIED BY MANUAL TEST`)
- **Model**: `gemini-3.8-flash` (`VERIFIED BY MANUAL TEST`)
- **Eklenen Araçlar**:
  - `Google Search` (Grounding with Google Search etkin) (`VERIFIED BY MANUAL TEST`)
  - `URL Context` (Web URL incelemesi) (`DOCUMENTATION ASSUMPTION`)
- **Rolü**: Uzmanlık dernekleri kılavuzlarını kataloglama (ERAS Society, ASCRS, NICE, SAGES, EAES, ESCP, TSS), derecelendirilmiş tavsiyeleri ayıklama ve uluslararası görüş ayrılıklarını tespit etme (`VERIFIED BY MANUAL TEST`).

---

## 4. Orkestrasyon ve Çalışma Zamanı Davranışı

| Davranış Özelliği | Durum | Gözlemlenen Davranış & Detaylar |
| :--- | :---: | :--- |
| **Görev Ayrıştırma (Task Decomposition)** | **VERIFIED BY MANUAL TEST** | Coordinator, gelen doğal dil sorgularını epidemiyolojik PICOT alanlarına ayrıştırır (Population, Intervention, Comparator, Outcomes, Timeframe). |
| **Uzman Delegasyonu (Specialist Delegation)** | **VERIFIED BY MANUAL TEST** | Coordinator, hakemli çalışmalar için `evidence-specialist`'i, dernek kılavuzları için `guideline-specialist`'i çağırır. |
| **Yürütme Sıralaması** | **VERIFIED BY MANUAL TEST** | Eksiksiz bir sorgu sırasında her iki subagent da çağrılır. Sıra, LLM akıl yürütme planlayıcısı tarafından dinamik olarak belirlenir (genellikle önce Evidence, ancak deterministik olarak garanti edilmez). |
| **Paralel Yürütme** | **NOT YET VERIFIED** | Agent Studio'nun her iki subagent'ı her durumda eşzamanlı mı yoksa sıralı mı sevk ettiği backend motoru zamanlamasına bağlıdır. |
| **Bağlam Aktarımı (Aşağı Doğru)** | **VERIFIED BY MANUAL TEST** | Coordinator, normalize edilmiş PICOT parametrelerini paketler ve subagent çağrılarına iletir. |
| **Bağlam Aktarımı (Yukarı Doğru)** | **VERIFIED BY MANUAL TEST** | Uzman agent'lar doğrulanmış başlıklar ve URL'ler içeren markdown/metin bulguları döndürür; Coordinator bunları nihai brief içinde sentezler. |
| **Uzmanlar Arası Bağlam Aktarımı** | **DOCUMENTATION ASSUMPTION** | Subagent'lar bağımsız çalışır; Guideline uzmanı doğrudan Evidence uzmanının çıktısını okumaz, ancak tüm ilgili bağlamı Coordinator üzerinden alır. |
| **Kaynak Atfı (Citation Attribution)** | **VERIFIED BY MANUAL TEST** | Çıktı; Google Search grounding ile getirilen kaynak başlıklarını, yayın yıllarını, yayınlayan kurumları ve canlı URL'leri korur. |
| **Negatif Durum Tespiti (`not_found`)** | **VERIFIED BY MANUAL TEST** | Güvenilir klinik çalışmalar veya kılavuzlar mevcut olmadığında (örn. özofagus kanserinde HIFU), kaynak uydurmadan `not_found: true` doğru şekilde doldurulur. |
| **Güvenlik Reddi (Safety Refusal)** | **VERIFIED BY MANUAL TEST** | Hastaya özel klinik ikilemler (örn. 72 yaşındaki erkek sigmoid rezeksiyonu), bireyselleştirilmiş tıbbi tavsiyenin derhal reddedilmesini ve genelleştirilmiş eğitsel senteze yönlendirilmesini tetikler. |
| **Preview ve İz İncelemesi (Trace Inspection)** | **VERIFIED BY MANUAL TEST** | Agent Studio Preview paneli, subagent çağrılarını ve araç grounding yürütmelerini onaylayan interaktif bir **Events / Trace** çekmecesi içerir. |

---

## 5. Mimari Kararlılık ve Dondurma Beyanı (Freeze Statement)

Yukarıda ayrıntıları verilen yapılandırma, Surgical AI Agents workshop'u için **doğrulanmış temeli (verified baseline)** temsil eder. Açık güçlendirme kanıtı ve regresyon testi olmaksızın agent topolojisinde, araç tahsislerinde veya sistem talimatlarında hiçbir değişiklik yapılmamalıdır.
