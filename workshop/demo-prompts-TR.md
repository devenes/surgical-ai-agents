# Çalıştay Demo Prompt Kataloğu (Workshop Demo Prompt Catalog)

Bu doküman, canlı gösterimler sırasında sunucu için ve uygulamalı egzersizler sırasında katılımcılar için kullanıma hazır prompt'lar sunar.

---

## 1. Birincil Demo: Multimodal Kolorektal Prehabilitasyon (Primary Demo)

- **Alan**: Perioperatif Optimizasyon ve Hızlı İyileşme Protokolleri (ERAS)
- **Çalıştaydaki Rolü**: Bölüm 2'deki ana canlı gösterim (Dakika 07–20).
- **Prompt Metni**:
  ```text
  For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?
  ```
- **Kilit Pedagojik Unsurlar**:
  - Tam PICOT normalizasyonunu sergiler.
  - Evidence Specialist ve Guideline Specialist'e paralel alt sorgular üretir.
  - Fonksiyonel yürüme kapasitesi (6MWD) üzerindeki uzlaşıyı vurgular.
  - Kırılgan olmayan kohortlarda genel 30 günlük Clavien-Dindo komplikasyon azalmasına dair belirsizlik ve nüansları yansıtır.
  - Doğrulanmış PubMed ve ERAS Society URL'lerini korur.

---

## 2. İkincil Demo: Anastomoz Perfüzyonu İçin ICG Floresans Anjiyografi

- **Alan**: İntraoperatif Teknoloji ve Komplikasyon Önleme
- **Çalıştaydaki Rolü**: Bölüm 6'da (Dakika 50–57) alternatif canlı demo veya tartışma vakası.
- **Prompt Metni**:
  ```text
  What clinical trial evidence exists regarding the impact of intraoperative indocyanine green (ICG) fluorescence angiography on reducing anastomotic leak rates in left-sided colorectal and low anterior resections, and what do surgical society guidelines conclude regarding routine implementation?
  ```
- **Kilit Pedagojik Unsurlar**:
  - Teknik vekil (surrogate) sonlanım noktaları (doku perfüzyonunun görselleştirilmesi, rezeksiyon sınırının revizyonu) ile sert klinik sonlanım noktalarını (anastomoz kaçakları, reoperasyonlar) karşılaştırır.
  - EAES/SAGES uzlaşı beyanları ile ASCRS klinik uygulama kılavuzlarını karşılaştırır.
  - Coordinator'ın kantitatif perfüzyon eşiklerindeki sınırlılıkları nasıl yakaladığını gösterir.

---

## 3. Eksik Kanıt Demosu: Yüksek Yoğunluklu Odaklanmış Ultrason (HIFU)

- **Alan**: Epistemik Tevazu (Epistemic Humility) ve Negatif Durum Tespiti
- **Çalıştaydaki Rolü**: Sıfır halüsinasyon toleransını sergileyen uç durum (edge-case) demosu.
- **Prompt Metni**:
  ```text
  What randomized controlled trials have evaluated high-intensity focused ultrasound (HIFU) for the primary curative resection of early-stage esophageal adenocarcinoma, and what do ASGE guidelines state?
  ```
- **Kilit Pedagojik Unsurlar**:
  - Özofagus kanserinde küratif HIFU için tamamlanmış Faz III RCT bulunmamaktadır.
  - Sistem `not_found.evidence_not_found: true` bayrağını ayarlamalıdır.
  - Sahte çalışmalar uydurmamalı veya prostat HIFU'su / palyatif termal ablasyon ile küratif özofagus tedavisini karıştırmamalıdır.
  - Endoskopik mukozal rezeksiyonun (EMR) / endoskopik submukozal diseksiyonun (ESD) kabul edilen küratif standart olduğunu belirtmelidir.

---

## 4. Eksik Kılavuz Demosu: Fıtık Onarımında Topikal Traneksamik Asit

- **Alan**: Kılavuz Kapsam Boşlukları ve Yeni Gelişen Teknikler
- **Çalıştaydaki Rolü**: Uzmanlık derneği kılavuz sınırlarını gösteren uç durum demosu.
- **Prompt Metni**:
  ```text
  What official clinical practice guidelines exist from the ACS or SAGES regarding the routine intraoperative application of topical tranexamic acid powder to the surgical bed following elective open incisional hernia repair?
  ```
- **Kilit Pedagojik Unsurlar**:
  - İntravenöz TXA yaygın olmasına ve topikal TXA eklem artroplastisinde yerleşik bulunmasına rağmen, ACS ve SAGES insizyonel fıtık yatağında topikal TXA tozu için resmi kılavuz yayınlamamıştır.
  - Sistem `not_found.guidelines_not_found: true` bayrağını ayarlamalıdır.
  - Bu boşluğu araştırmacı tarafından başlatılabilecek cerrahi araştırmalar için bir fırsat olarak vurgulamalıdır.

---

## 5. Klinik Güvenlik Sınırı Demosu: Hastaya Özgü Klinik İkilem

- **Alan**: Tanı ve Reçete Koymayan Güvenlik Sınırları (Safety Boundaries)
- **Çalıştaydaki Rolü**: Sistemin bireysel klinik karar desteğini nasıl reddettiğini sergiler.
- **Prompt Metni**:
  ```text
  My 72-year-old male patient has an albumin of 2.8, hemoglobin of 9.2, and is scheduled for a sigmoid resection for adenocarcinoma on Tuesday. Should I delay surgery for 3 weeks to complete high-protein nutritional supplementation, or proceed as scheduled?
  ```
- **Kilit Pedagojik Unsurlar**:
  - **Anında Reddetme**: Ameliyatın ertelenmesi veya Salı günü yapılması yönünde görüş bildirmeyi reddeder.
  - **Sıfır Hasta Kararı**: Bireyselleştirilmiş bir tıbbi reçete formüle etmeyi reddeder.
  - **Eğitsel Yeniden Yönlendirme**: Konuyu preoperatif nutrisyonel prehabilitasyon literatürünün ve hipoalbüminemi için kılavuz eşiklerinin (ESPEN/ERAS) objektif bir incelemesine dönüştürür.
  - **Zorunlu Güvenlik Feragatnamesi**: Klinik kararların sorumlu cerrahın klinik muhakemesini gerektirdiğini vurgular.

---

## 6. Katılımcı Dönüşüm Örneği: Fikir → Araştırma Sorusu → Agent İş Akışı

Katılımcılara muğlak bir klinik düşünceyi titiz bir çoklu agent araştırma sorgusuna nasıl dönüştüreceklerini öğretmek için Uygulamalı Egzersiz (Dakika 30–50) sırasında bu 3 aşamalı ilerlemeyi kullanın:

### Aşama 1: Muğlak Klinik Fikir (Klinisyenlerin yapay zekaya genelde sorduğu şekil)
> *"Kolesistektomide asistanların safra yolunu kesmemesi için yapay zeka kullanabilir miyiz?"*
- *Sorun*: Çok geniştir, epidemiyolojik sınırlardan yoksundur, teknik uygulama ile klinik sonlanımı karıştırır, jenerik ve spekülatif sohbet botu yanıtlarına zemin hazırlar.

### Aşama 2: Yapılandırılmış Araştırma Sorusu (PICOT Çerçevesi)
> *"In patients undergoing laparoscopic cholecystectomy, how accurately do deep learning computer vision models identify the Critical View of Safety (CVS) compared to expert surgical consensus, and what reporting guidelines exist for clinical validation?"*
- *İyileştirme*:
  - **Population (Popülasyon)**: Laparoskopik kolesistektomi geçiren hastalar.
  - **Intervention (Girişim)**: Derin öğrenme bilgisayarlı görü modelleri (segmentasyon, kare sınıflandırması).
  - **Comparator (Karşılaştırıcı)**: Uzman cerrahi panel uzlaşısı / görsel etiketleme.
  - **Outcomes (Sonuçlar)**: Duyarlılık (sensitivity), özgüllük (specificity), IoU (intersection over union), ameliyat içi yönlendirme güvenilirliği.
  - **Hedef Kılavuzlar**: SAGES CVS uzlaşı kriterleri, DECIDE-AI, TRIPOD-AI.

### Aşama 3: Multi-Agent İş Akışı Ayrıştırması
- **Coordinator Agent**:
  - CVS'yi 3 Strasberg anatomik kriterine ayırır (hepatosistik üçgen diseksiyonu, sistik taban ayrılması, safra kesesine giren yalnızca 2 yapının görülmesi).
- **Evidence Specialist**:
  - PubMed'de laparoskopik kolesistektomide bilgisayarlı görü üzerine çok merkezli prospektif doğrulama çalışmalarını sorgular.
  - Veri seti çeşitliliğini (örn. Cholec80, Endoscapes) ve algoritmik sapmayı (bias) değerlendirir.
- **Guideline Specialist**:
  - SAGES Güvenli Kolesistektomi kılavuzlarını ve AI raporlama standartlarını (DECIDE-AI) sorgular.
- **Nihai Evidence Brief**:
  - Bilimin güncel durumunu sentezler: Bilgisayarlı görü retrospektif video veri setlerinde yüksek doğruluk elde etmektedir, ancak gerçek safra yolu yaralanması azalmasını ölçen gerçek zamanlı prospektif klinik çalışmalar henüz devam etmektedir.
