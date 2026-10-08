# Cerrahi AI Agent Çalıştay Paketi (Surgical AI Agents Workshop Package)

- **Oturum Başlığı**: Multi-Agent AI Architectures in Surgical Research: From Clinical Inquiries to Structured Evidence
- **Hedef Kitle**: Akademik cerrahlar, cerrahi asistanları, klinik fellow'lar ve sağlık bilişimi araştırmacıları
- **Oturum Süresi**: 60 Dakika
- **Birincil Sunum Platformu**: Google Cloud Agent Studio (Agent Designer)
- **Tamamlayıcı Platform**: Agent Studio Chat / Freeform (Multimodal Mini-Demo)
- **Geliştirici Referans Baseline**: Google Agent Development Kit (ADK `2.11.0` üzerinde `gemini-3.8-flash`)

---

## 1. Paket İçeriği (Package Contents)

Bu dizin, 60 dakikalık etkileşimli çalıştayı yürütmek için gerekli tüm operasyonel materyalleri içerir:

| Belge (EN) | Belge (TR) | Amaç ve Hedef Kitle |
| :--- | :--- | :--- |
| [`presenter-runbook.md`](presenter-runbook.md) | [`presenter-runbook-TR.md`](presenter-runbook-TR.md) | **Yalnızca Sunucu**: Dakika dakika akış planı (00–60dk), tam tıklama adımları, demo prompt'ları, konuşma metinleri ve fallback planları. |
| [`participant-guide.md`](participant-guide.md) | [`participant-guide-TR.md`](participant-guide-TR.md) | **Katılımcılar**: Katılımcıların klinik problemlerini bir yapay zeka projesine dönüştürmeleri için sadeleştirilmiş referans kılavuzu. |
| [`demo-prompts.md`](demo-prompts.md) | [`demo-prompts-TR.md`](demo-prompts-TR.md) | **Sunucu ve Katılımcılar**: Birincil, ikincil, uç durum ve dönüşüm örneklerini içeren derlenmiş prompt kataloğu. |
| [`storyboard.md`](storyboard.md) | [`storyboard-TR.md`](storyboard-TR.md) | **Eğitsel Anlatı**: Ham cerrahi ikilemden çalışan yapay zeka prototipine uzanan kavramsal pedagojik yolculuk. |
| [`troubleshooting.md`](troubleshooting.md) | [`troubleshooting-TR.md`](troubleshooting-TR.md) | **Canlı Operasyon**: Yaygın sınıf, ağ ve arayüz hataları için tanı ve hızlı kurtarma adımları. |
| [`fallback-demo.md`](fallback-demo.md) | [`fallback-demo-TR.md`](fallback-demo-TR.md) | **Acil Durum Planları**: Canlı bulut servislerinde sorun yaşanması durumunda 4 kademeli fallback iş akışı (Tier 0 / A / B / C / D). |
| [`cloud-deployment.md`](cloud-deployment.md) | [`cloud-deployment-TR.md`](cloud-deployment-TR.md) | **Ek Kulvar**: Cloud Buildpacks veya Dockerfile kullanarak en az yetkili IAM hesaplarıyla Cloud Run ve üretim konteyner dağıtımı. |

---

## 2. Temel Eğitsel Değer Önerisi (Core Educational Value Proposition)

Akademik cerrahlar sıklıkla jenerik sohbet botlarıyla çalışırken hayal kırıklığı yaşarlar:
1. **Atıf Uydurma (Hallucinated Citations)**: Sahte PMID'ler, var olmayan klinik çalışmalar ve makul görünen tıbbi yanlışlar.
2. **Yapılandırılmamış Düz Metin (Unstructured Prose)**: Titiz bilimsel değerlendirmeye uygun olmayan sohbet paragrafları.
3. **Kanıtların Birbirine Karışması (Evidence Conflation)**: Randomize kontrollü çalışmalar ile resmi uzmanlık derneği kılavuzlarının ayrıştırılamaması.
4. **Güvenlik Riskleri (Safety Risks)**: Bireyselleştirilmiş hasta vakalarına uygunsuz tavsiyelerde bulunma cüreti.

Bu çalıştay **agentik çözümü** sergilemektedir:
```
Klinik Araştırma Sorusu ──► PICOT Normalizasyonu ──► Uzman Delegasyonu ──► Grounded Search ──► Yapılandırılmış JSON Kanıt Özeti
```

---

## 3. Oturum Eğitim Adımları Yol Haritası (Session Tutorial Steps Roadmap)

Çalıştay sırasında bu senaryolaştırılmış adımları izleyin:

| Adım / Bölüm | Süre | Aşama / Konu | Uygulamalı Eylemler | Birincil Alt Belge Bağlantıları (EN / TR) |
| :---: | :---: | :--- | :--- | :--- |
| **Adım 0** | T-30dk | **Kürsü Doğrulaması** | Otomatik prova (dry-run rehearsal) komutunu çalıştırın | [EN](presenter-runbook.md#🛡️-t-30-minute-pre-workshop-rehearsal-protocol-podium-verification) \| [TR](presenter-runbook-TR.md#🛡️-t-30-dakika-çalıştay-öncesi-prova-protokolü-kürsü-doğrulaması---podium-verification) |
| **Adım 1** | 00–07dk | **Giriş ve Agentic Değişim** | Klinik ikilemi çerçeveleme; Monolitik vs Agentic | [EN](storyboard.md) \| [TR](storyboard-TR.md) • [EN](../docs/safety.md) \| [TR](../docs/safety-TR.md) |
| **Adım 2** | 07–20dk | **Canlı Multi-Agent Demosu** | Canvas/UI içinde Kolorektal Prehab sorgusunu yürütme | [EN](presenter-runbook.md#segment-2-live-multi-agent-demo-0700--2000) \| [TR](presenter-runbook-TR.md#bölüm-2-canlı-multi-agent-demosu-0700--2000) • [EN](demo-prompts.md#1-primary-demo-multimodal-colorectal-prehabilitation) \| [TR](demo-prompts-TR.md#1-birincil-demo-multimodal-kolorektal-prehabilitasyon-primary-demo) |
| **Adım 3** | 20–25dk | **Trace ve Grounding Denetimi** | Arama sorgularını, kaynak URL'leri, JSON şemasını inceleme | [Schema](../agents/coordinator/output-schema.json) • [EN](troubleshooting.md) \| [TR](troubleshooting-TR.md) |
| **Adım 4** | 25–30dk | **Multimodal Vision Demosu** | Strasberg CVS şemasının tanı koymayan gözlemi | [EN](../multimodal-demo/prompt.md) \| [TR](../multimodal-demo/prompt-TR.md) • [EN](../multimodal-demo/safety.md) \| [TR](../multimodal-demo/safety-TR.md) |
| **Adım 5** | 30–50dk | **Uygulamalı Proje Egzersizi** | Katılımcıların PICOT oluşturması ve uzman sorguları test etmesi | [EN](participant-guide.md) \| [TR](participant-guide-TR.md) • [EN](demo-prompts.md) \| [TR](demo-prompts-TR.md) |
| **Adım 6** | 50–57dk | **Değerlendirme ve Uç Durumlar** | Eksik kanıt (`EDGE-01`) ve güvenliği (`EDGE-07`) test etme | [Eval](../evaluations/expected-behavior.md) • [EN](fallback-demo.md) \| [TR](fallback-demo-TR.md) |
| **Adım 7** | 57–60dk | **Kapanış ve Kod Aynası** | Python ADK'ya aktarma; Cloud Run barındırmayı keşfetme | [EN](../docs/adk-setup.md) \| [TR](../docs/adk-setup-TR.md) • [EN](cloud-deployment.md) \| [TR](cloud-deployment-TR.md) |
