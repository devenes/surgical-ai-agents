# Multimodal Gösterim Prompt'ları (Multimodal Demonstration Prompts)

Bu prompt'lar, **Agent Studio Chat / Freeform** arayüzünde (veya Vertex AI Studio Multimodal Prompt ekranında) Gemini 3.8 Flash ile kullanılmak üzere tasarlanmıştır. Nötr gözlemi zorunlu kılar ve yetkisiz klinik karar verilmesini engeller.

---

## 1. Birincil Gözlem Prompt'u (Aşama 1 - Primary Observation Prompt)

`multimodal-demo/assets/` dizininden görseli yükleyin ve aşağıdaki prompt'u gönderin:

```text
Describe only the observable visual features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
```

### Beklenen Çıktı Özellikleri:
- **Objektif Görsel Envanter**: Görselde görünen anatomik yapıları, cerrahi aletleri, doku hatlarını ve uzamsal yönelimleri tanımlar.
- **Epistemik Tevazu**: Tanımlayıcı bir dil kullanır (örn. *"Alanı enine geçen boru şeklinde bir yapı görülmektedir"*, *"Sağ üst kadranda konumlandırılmış bir tutucu alet yer almaktadır"*).
- **Yasaklanmış İçerik**: Sıfır tanısal ifade (örn. *"Bu hastada akut gangrenöz kolesistektomi vardır"* DEMEZ); sıfır tedavi önerisi; sıfır cerrahi devam/dur tavsiyesi.

---

## 2. Eğitsel ve Araştırma Takip Prompt'u (Aşama 2)

Modelin Aşama 1 yanıtının hemen ardından, aynı sohbet oturumunda şu takip sorgusunu iletin:

```text
Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
```

### Beklenen Çıktı Özellikleri:
- **Bilgisayarlı Görü Görevleri**: Anatomik planların anlamsal segmentasyonu (semantic segmentation), cerrahi alet tespiti ve takibi, ameliyat aşaması tanıma ve Critical View of Safety (CVS) kriterlerinin doğrulanması.
- **Bilişim Standartları**: Klinik yapay zeka için raporlama standartlarından (DECIDE-AI ve TRIPOD-AI gibi) bahseder.
- **Sıfır Hasta Kararı**: Otomatik bilgisayarlı görü modellerinin, klinik uygulamadan önce titiz prospektif çalışma doğrulaması gerektiren araştırma araçları olduğunu vurgular.
