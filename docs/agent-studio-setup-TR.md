# Agent Studio Yapılandırma Kılavuzu

- **Hedef Platform**: Google Cloud Gemini Enterprise Agent Platform (Vertex AI Agent Studio)
- **Mimari**: Hiyerarşik Multi-Agent Sistemi (Root Coordinator + 2 Yerel Subagent)
- **Gerçeklik Kaynağı (Source of Truth)**: 
  - Talimatlar: `agents/coordinator/instructions.md`, `agents/evidence/instructions.md`, `agents/guideline/instructions.md`
  - Şemalar: `agents/coordinator/output-schema.json`, `agents/evidence/output-schema.json`, `agents/guideline/output-schema.json`

---

## 1. Proje ve Konsol Gezintisi

1. [Google Cloud Console](https://console.cloud.google.com/) sayfasını açın.
2. Aktif workshop projenizi seçin (örn. `GOOGLE_CLOUD_PROJECT` ile yapılandırılan).
3. Gezinti menüsünden **Gemini Enterprise Agent Platform** (veya **Vertex AI** → **Agent Studio** / **Agents**) bölümüne gidin.
4. Konsol açılır menüsünden aktif bölgeyi doğrulayın: **`us`** (US çoklu bölge) veya **`global`**.
5. Kök agent tuvalini başlatmak için **Create Agent** (veya **+ New Agent**) düğmesine tıklayın.

---

## 2. Agent 1: Coordinator Agent (Kök Agent)

Coordinator; merkezi orkestratör, ayrıştırma motoru ve sentezleme otoritesi olarak görev yapar.

| Yapılandırma Alanı | Değer / Ayar |
| :--- | :--- |
| **Agent Name** | `surgical-evidence-coordinator` |
| **Display Name** | `Surgical Evidence Coordinator` |
| **Description** | `Chief orchestrator and synthesizer for educational surgical research inquiries. Decomposes research topics via PICOT, delegates to specialist subagents (Evidence & Guideline), and produces structured evidence briefs.` |
| **Model** | `gemini-3.8-flash` |
| **Reasoning / Thinking Level** | `MEDIUM` (standart akıl yürütme derinliği; temperature, top_p, top_k gibi eski örnekleme parametreleri Gemini 3.8 Flash için kullanımdan kaldırılmıştır) |
| **Instructions** | [agents/agent-studio/coordinator-instructions.md](../agents/agent-studio/coordinator-instructions.md) dosyasındaki tam metin |
| **Subagents** | 2 Yerel Subagent ekleyin:<br>1. `evidence-specialist` (Evidence Agent)<br>2. `guideline-specialist` (Guideline Agent) |
| **Tools** | **Yok / None** (Yapılandırılmış çıktı biçimlendirmesiyle araç çakışmalarını önlemek için Coordinator düğümüne doğrudan Google Search eklemeyin). |
| **Expected Output** | [agents/coordinator/output-schema.json](../agents/coordinator/output-schema.json) standardına tam uyan JSON nesnesi. PICOT kapsamı, bulgular, kaynaklar, uzlaşma/ayrışma ve güvenlik sorumluluk reddi içeren Yapılandırılmış Kanıt Özeti (Structured Evidence Brief). |

---

## 3. Agent 2: Evidence Agent (Yerel Subagent)

Hakemli cerrahi literatürü ve klinik çalışmaları sorgulamak, değerlendirmek ve kategorize etmekten sorumlu uzman subagent.

| Yapılandırma Alanı | Değer / Ayar |
| :--- | :--- |
| **Agent Name** | `evidence-specialist` |
| **Display Name** | `Evidence Research Agent` |
| **Description** | `Specialist agent for retrieving, evaluating, and summarizing peer-reviewed surgical literature, randomized controlled trials (RCTs), and systematic reviews using search grounding.` |
| **Model** | `gemini-3.8-flash` |
| **Reasoning / Thinking Level** | `MEDIUM` (örnekleme parametreleri Gemini 3.8 Flash'ta kaldırılmıştır) |
| **Instructions** | [agents/agent-studio/evidence-instructions.md](../agents/agent-studio/evidence-instructions.md) dosyasındaki tam metin |
| **Tools** | 1. **Google Search** (Grounding with Google Search etkin)<br>2. **URL Context** (Web URL getirme; isteğe bağlı/ikincil) |
| **Expected Output** | Çalışma başlığı, yazarlar/grup, yayın yılı, kanıt düzeyi (RKÇ, sistematik derleme, kohort), doğrulanmış URL, temel sonlanım bulguları ve metodolojik kısıtlılıkları içeren yapılandırılmış literatür değerlendirmesi. |

---

## 4. Agent 3: Guideline Agent (Yerel Subagent)

Tanınmış cerrahi derneklerin resmi klinik uygulama kılavuzlarını ve konsensüs bildirilerini sorgulamak, değerlendirmek ve kataloglamaktan sorumlu uzman subagent.

| Yapılandırma Alanı | Değer / Ayar |
| :--- | :--- |
| **Agent Name** | `guideline-specialist` |
| **Display Name** | `Guideline Specialist Agent` |
| **Description** | `Specialist agent for retrieving, evaluating, and cataloging official clinical practice guidelines, consensus statements, and practice parameters from recognized national and international surgical societies.` |
| **Model** | `gemini-3.8-flash` |
| **Reasoning / Thinking Level** | `MEDIUM` (örnekleme parametreleri Gemini 3.8 Flash'ta kaldırılmıştır) |
| **Instructions** | [agents/agent-studio/guideline-instructions.md](../agents/agent-studio/guideline-instructions.md) dosyasındaki tam metin |
| **Tools** | 1. **Google Search** (Grounding with Google Search etkin)<br>2. **URL Context** (Web URL getirme; isteğe bağlı/ikincil) |
| **Expected Output** | Yayınlayan kuruluş (NICE, ERAS, ACS, ASCRS, EAES, ESCP, SAGES, TSS), başlık, yıl, öneri özeti, öneri derecesi, doğrulanmış URL ve ayrışma notlarını içeren yapılandırılmış kılavuz analizi. |

---

## 5. Görsel Tuval Hiyerarşisi

```
                    ┌───────────────────────────────────┐
                    │  Surgical Evidence Coordinator    │
                    │      (Kök Yönlendirici Agent)     │
                    │      Model: gemini-3.8-flash      │
                    │      Tools: Yok (Yalnızca Sentez) │
                    └─────────────────┬─────────────────┘
                                      │
               ┌───────────────────────┴───────────────────────┐
               ▼                                               ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│     Evidence Specialist       │               │     Guideline Specialist      │
│       (Yerel Subagent)        │               │       (Yerel Subagent)        │
│    Model: gemini-3.8-flash    │               │    Model: gemini-3.8-flash    │
│    Tools: Google Search       │               │    Tools: Google Search       │
└───────────────────────────────┘               └───────────────────────────────┘
```

---

## 6. Agent Studio'da Yürütme Akışı

1. **Kullanıcı Gönderimi**: Kullanıcı, Agent Studio **Preview** sohbet paneli üzerinden cerrahi bir araştırma sorusu gönderir.
2. **Coordinator Ayrıştırması**: Coordinator sorguyu analiz eder, PICOT kapsamını çıkarır ve delegasyon gereksinimlerini belirler.
3. **Subagent Çağrısı**:
   - Coordinator literatür arama parametrelerini `evidence-specialist` agent'ına yönlendirir.
   - Coordinator dernek öneri parametrelerini `guideline-specialist` agent'ına yönlendirir.
4. **Araç Yürütme**:
   - Her iki subagent da doğrulanmış kaynakları, özetleri ve kılavuz depolarını getirmek için Google Search aracını çağırır.
5. **Sentez ve Biçimlendirme**:
   - Coordinator yapılandırılmış bulguları toplar.
   - Uzmanlar arası uzlaştırma gerçekleştirir (uzlaşma alanları, ayrışma alanları, belirsizlik, kısıtlılıklar).
   - Çıktıyı geçerli bir JSON Structured Evidence Brief olarak biçimlendirir.
6. **Preview İncelemesi**:
   - Subagent çağrı yörüngelerini ve grounding sorgularını doğrulamak için Preview panelindeki **Events** sekmesini inceleyin.
