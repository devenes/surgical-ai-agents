# Çalıştay Görsel Taslağı: Katılımcı Yolculuğu (Workshop Storyboard)

- **Doküman Sürümü**: 1.0.0
- **Hedef Kitle**: Çalıştay Tasarımcıları, Eğitmenler ve Moderatörler
- **Amaç**: 60 dakikalık çalıştay deneyimi boyunca bir katılımcının bilişsel yolculuğunu haritalamak.

---

## 1. Temel Anlatı Akışı (The Core Narrative Arc)

Çalıştay, klinik ikilemden çalışan bir yapay zeka sistem mimarisine uzanan yapılandırılmış pedagojik bir ilerlemeyi takip eder:

```
"Cerrahi bir problem getiriyorum."
              │
              ▼
"Coordinator bunu görevlere dönüştürüyor."
              │
              ▼
"Uzman agent'lar araştırıyor."
              │
              ▼
"Kaynaklar ortaya çıkıyor."
              │
              ▼
"Agent'ların nasıl çalıştığını anlıyorum."
              │
              ▼
"İş akışını kendi problemim için yeniden tasarlıyorum."
              │
              ▼
"Bir AI projesinin ilk versiyonuna sahip oluyorum."
```

---

## 2. Adım Adım Katılımcı Bilişsel Dönüm Noktaları

### 1. Vuruş: "Cerrahi bir problem getiriyorum." (Dakika 00–07)
- **Zihinsel Durum**: Jenerik yanıtlar veren veya atıf uyduran (hallucination) yapay zeka chatbot'larına karşı mesafeli veya hayal kırıklığına uğramış.
- **Tetikleyici**: Sunucu cerrahların yaşadığı gerçek sürtünmeyi dile getirir: *"ChatGPT bana bir çalışmanın var olduğunu söylerken PMID neden sahte çıkıyor?"*
- **Aydınlanma (Aha!) Anı**: Chatbot'lar kelimeleri tahmin eder; agent'lar iş akışlarını yürütür.

### 2. Vuruş: "Coordinator bunu görevlere dönüştürüyor." (Dakika 07–15)
- **Zihinsel Durum**: Yapay zekanın karmaşık, çok yönlü soruları nasıl ele aldığını merak ediyor.
- **Görsel Olay**: Birincil kolorektal prehabilitasyon prompt'u Agent Studio Preview paneline gönderilir.
- **Aydınlanma (Aha!) Anı**: Coordinator sadece tahmin yürütmez; sorguyu epidemiyolojik bir PICOT çerçevesine (Population, Intervention, Comparator, Outcomes, Timeframe) ayırır.

### 3. Vuruş: "Uzman agent'lar araştırıyor." (Dakika 15–20)
- **Zihinsel Durum**: Klinik iş bölümünden etkilenmiş.
- **Görsel Olay**: Trace paneli, Coordinator'ın literatür sorgularını Evidence Specialist'e ve kılavuz sorgularını Guideline Specialist'e devrettiğini gösterir.
- **Aydınlanma (Aha!) Anı**: Hakemli dergi araştırmalarını dernek kılavuzlarından ayırmak, gerçek dünyadaki akademik cerrahi kanıt değerlendirmesini birebir yansıtır.

### 4. Vuruş: "Kaynaklar ortaya çıkıyor." (Dakika 20–25)
- **Zihinsel Durum**: Bilimsel titizlik ve doğrulanabilirlik ile güven duymuş.
- **Görsel Olay**: Çıktıda PubMed, *JAMA Surgery* ve ERAS Society kaynaklı canlı, tıklanabilir URL'ler belirir. Negatif durumlar (`not_found: true`) epistemik tevazuyu sergiler.
- **Aydınlanma (Aha!) Anı**: Grounding modeli gerçek dünyaya bağlar; sistem neyi bilmediğini dürüstçe kabul eder.

### 5. Vuruş: "Agent'ların nasıl çalıştığını anlıyorum." (Dakika 20–25)
- **Zihinsel Durum**: Mimari kavrayışla güçlenmiş.
- **Görsel Olay**: Sunucu Trace çekmecesini açarak prompt sözleşmelerini, araç çağrılarını ve yapılandırılmış JSON çıktısını gösterir.
- **Aydınlanma (Aha!) Anı**: Bir agent; planlama, araç çağırma ve sentezden oluşan yapılandırılmış bir döngüdür.

---

## 3. Tamamlayıcı Multimodal Mini-Demo Nereye Oturur? (Dakika 25–30)

```
                       [Ana Metin Tabanlı Araştırma Akışı]
                                         │
                                         ▼ (Dakika 25: Görsel Boyut)
                        ┌───────────────────────────────┐
                        │   Tamamlayıcı Mini-Demo       │
                        │ "AI metin dışını da işleyebilir" │
                        │  • Ayrı Freeform yüzeyi       │
                        │  • Nötr görsel özellikler     │
                        │  • Tanı koymayan güvenlik sınırı │
                        └───────────────┬───────────────┘
                                         │
                                         ▼ (Ana Yola Dönüş)
                     [Katılımcı Uygulamalı Tasarım Egzersizi]
```

### Multimodal Gösterimin Destekleyici Rolü:
- **Nedir?**: Temeldeki Gemini temel modelinin metinle birlikte ameliyat içi görüntüleri ve anatomik işaretleri işleyebildiğini gösteren kısa bir 5 dakikalık sergilemedir.
- **Ne Değildir?**: Agent Designer araştırma tuvali içinde görüntü alan bir alt agent **değildir**. Patoloji tanısı koymaz veya ameliyat içi cerrahi adımlar önermez.
- **Pedagojik Fonksiyonu**: Katı tanı koymayan güvenlik sınırlarını pekiştirirken cerrahın gelecekteki uygulamalara (örn. bilgisayarlı görü araştırmaları, Critical View of Safety doğrulaması) yönelik vizyonunu genişletir.

---

## 4. Aktif Üretici Yoluna Dönüş

### 6. Vuruş: "İş akışını kendi problemim için yeniden tasarlıyorum." (Dakika 30–50)
- **Zihinsel Durum**: Yaratıcı, aktif geliştirici.
- **Aktivite**: Katılımcılar Katılımcı Kılavuzunu açar ve PICOT dekonstrüksiyonunu kendi klinik uzmanlık alanlarına (fıtık onarımı, pankreatektomi, ICG perfüzyonu, travma resüsitasyonu) uygular.
- **Aydınlanma (Aha!) Anı**: *"Bu çoklu agent modelini kliniğimin araştırma sorularına birebir uygulayabilirim."*

### 7. Vuruş: "Bir AI projesinin ilk versiyonuna sahip oluyorum." (Dakika 50–60)
- **Zihinsel Durum**: Başarmış; atılabilecek somut bir sonraki adıma sahip.
- **Çıktı**: Tamamlanmış bir PICOT ayrıştırması, iki uzman prompt'u ve kavramın nasıl uygulanacağına veya yayınlanacağına dair net bir kavrayış.
