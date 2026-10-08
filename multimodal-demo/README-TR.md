# Tamamlayıcı Multimodal Cerrahi AI Demosu (Supplemental Multimodal Demonstration)

- **Gösterim Kapsamı**: Tamamlayıcı 5 Dakikalık Görsel Demo (Bölüm 4, Dakika 25–30)
- **Birincil Canlı Yüzey**: Google Cloud Agent Studio Chat / Freeform (veya Vertex AI Studio Multimodal Interface)
- **Geliştirici Referansı**: Bağımsız Python betiği (`adk_multimodal_example.py`)
- **Temel İlke**: Birincil metin tabanlı Agent Designer araştırma tuvalinden tamamen ayrılmıştır.

---

## 1. Mimari Sınır Bildirimi (Architectural Boundary Notice)

> [!IMPORTANT]
> **Katı Tuval Ayrımı (Strict Canvas Separation)**:
> - Birincil çalıştay multi-agent sistemi (`surgical-evidence-coordinator`) **%100 metin tabanlıdır**.
> - Agent Designer tuvaline görüntü girdili bir alt agent veya multimodal algı aracı eklemeye **çalışmayın**.
> - Multimodal akıl yürütme, multi-agent orkestrasyon mimarisini karmaşıklaştırmadan temel modelin görme (vision) yeteneklerini göstermek amacıyla ayrı bir **Agent Studio Chat / Freeform** arayüzünde **tamamlayıcı bir mini-demo** olarak sergilenir.

---

## 2. Paket İçeriği (Package Contents)

| Belge / Varlık | Amaç |
| :--- | :--- |
| [`prompt.md`](prompt.md) \| [`prompt-TR.md`](prompt-TR.md) | Standartlaştırılmış iki aşamalı demo prompt'ları (Nötr Gözlem + Araştırma Takibi). |
| [`safety.md`](safety.md) \| [`safety-TR.md`](safety-TR.md) | Tanı ve reçete koymayan multimodal güvenlik bariyerleri ve yasakları. |
| [`test-cases.md`](test-cases.md) \| [`test-cases-TR.md`](test-cases-TR.md) | Önceden tanımlanmış multimodal test senaryoları ve değerlendirme kriterleri. |
| [`presenter-script.md`](presenter-script.md) \| [`presenter-script-TR.md`](presenter-script-TR.md) | 5 dakikalık demo için konuşma noktaları, tıklama adımları ve zamanlama. |
| [`fallback.md`](fallback.md) \| [`fallback-TR.md`](fallback-TR.md) | Canlı UI yavaşsa acil durum prosedürleri ve önceden hesaplanmış görsel açıklamalar. |
| [`assets/README.md`](assets/README.md) \| [`assets/README-TR.md`](assets/README-TR.md) | Test görsellerinin dokümantasyonu, telif/lisans doğrulaması ve sıfır-PHI uyumluluğu. |
| [`adk_multimodal_example.py`](adk_multimodal_example.py) | Resmi Google GenAI SDK'sını kullanan bağımsız, çalıştırılabilir Python referans betiği. |

---

## 3. İş Akışı Genel Bakışı (Workflow Overview)

```
Ameliyat İçi Görsel Varlık (Sentetik / Açık Şema)
                    │
                    ▼
          [Aşama 1: Gözlem Prompt'u]
"Yalnızca gözlemlenebilir görsel anatomik özellikleri tanımla..."
                    │
                    ▼
        Gemini Multimodal Anlama
           (`gemini-3.8-flash`)
                    │
                    ▼
      Nötr Anatomik Gözlem
    (İşaretler, aletler, uzamsal yönelim)
                    │
                    ▼
          [Aşama 2: Eğitsel Takip]
"Hangi bilgisayarlı görü araştırma görevleri bunu kullanır açıkla..."
                    │
                    ▼
   Akademik Bilişim Tartışması
(Critical View of Safety, alet segmentasyonu, DECIDE-AI)
```
