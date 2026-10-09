# Multimodal Gösterim Varlıkları ve Lisans Kaydı (Assets Registry)

- **Dizin Kapsamı**: Multimodal görüntü ve video stüdyoları için anonimleştirilmiş gösterim radyoloji görselleri ve ekokardiyografi videosu.
- **Güvenlik Kuralı**: **%100 Sıfır-PHI ve Sıfır Hasta Tanımlaması**.

---

## 1. Uyumluluk ve Etik Standartlar

Sağlık gizliliği yasaları (HIPAA, KVKK, GDPR) ve etik yapay zeka araştırma standartlarına tam uyum içinde:
- **Sıfır Kişisel Sağlık Verisi (Zero PHI)**: Tüm görseller ve video klipleri tamamen anonimleştirilmiş, hasta kimliğinden arındırılmış, açık erişimli olup DICOM etiketleri, tarihler, hastane adları veya demografik bilgiler içermez.
- **İzin Verici / Açık Erişim**: Tüm varlıklar eğitim, algoritma karşılaştırması ve multimodal yapay zeka demoları için açık tıbbi kaynaklardan derlenmiştir.
- **Eğitsel / Tanısal Olmayan Kapsam**: Varlıklar yalnızca bilgisayarlı görü ve özellik çıkarma kıyaslamaları için değerlendirilir; hastaya özel klinik tanı veya tedavi kararı üretilmez.

---

## 2. Varlık Kataloğu (Asset Catalog)

| Varlık Dosya Adı | Modalite / Anatomi | Açıklama | Biçim |
| :--- | :--- | :--- | :--- |
| `miliary-tuberculosis-5.jpeg` | Düz Radyografi (Akciğer PA) | Klasik miliyer paternde bilateral yaygın mikronodüler akciğer opasiteleri | JPEG |
| `anterior-shoulder-dislocation-26.jpeg` | Düz Radyografi (Omuz) | Glenohumeral eklem hizalanması, anterior-inferior humerus başı dislokasyonu | JPEG |
| `phalanx-fracture-hand.png` | Düz Radyografi (El) | Falanks kortikal devamlılık bozukluğu ve eklem hizalanması | PNG |
| `osteochondroma-femur-7.png` | Düz Radyografi (Femur) | Ana kemik korteks ve medullası ile devamlı metafizer ekzostoz | PNG |
| `pulmonary-metastatic-calcification.jpeg` | Düz Radyografi (Akciğer PA) | Yüksek dansiteli konfluen parankimal opasiteler ve kalsifikasyonlar | JPEG |
| `apical_4_chamber_echo.mp4` | Transtorasik Ekokardiyografi (TTE) | Ventrikül/atriyum duvar hareketlerini gösteren gerçek zamanlı dinamik apikal 4-boşluk videosu | MP4 (H.264) |

---

## 3. Varlık Ayrıntıları ve Modalite Tanımları

### 1. `miliary-tuberculosis-5.jpeg`
- **Projeksiyon**: Posteroanterior (PA) akciğer grafisi.
- **Gözlemlenen Özellikler**: Her iki akciğer alanına simetrik dağılmış ince, homojen 1-2 mm mikronodüller. Korunmuş keskin kostofrenik sinüsler ve normal kardiyotorasik indeks.
- **Araştırma Kullanımı**: Yaygın nodüler segmentasyon ve akciğer alanı patern sınıflandırma modeli kıyaslaması.

### 2. `anterior-shoulder-dislocation-26.jpeg`
- **Projeksiyon**: Anteroposterior (AP) omuz grafisi.
- **Gözlemlenen Özellikler**: Humerus başının glenoid fossaya göre inferomediale yer değiştirmesi, korakoid çıkıntı altında konumlanması.
- **Araştırma Kullanımı**: Eklem hizalanması tanıma ve travma sınıflandırması.

### 3. `phalanx-fracture-hand.png`
- **Projeksiyon**: Düz el grafisi.
- **Gözlemlenen Özellikler**: Falanks cismi boyunca minimal açılanmalı belirgin kortikal kırık hattı.
- **Araştırma Kullanımı**: Kemik korteks sınırı çıkarma ve kırık tespiti modelleri.

### 4. `osteochondroma-femur-7.png`
- **Projeksiyon**: Femur grafisi (diz eklemi komşuluğu).
- **Gözlemlenen Özellikler**: Distal femur metafizinden eklemden uzağa yönelen, doğrudan kortikomedüller devamlılık gösteren kemik çıkıntısı.
- **Araştırma Kullanımı**: Kas-iskelet lezyon sınır segmentasyonu ve morfometrisi.

### 5. `pulmonary-metastatic-calcification.jpeg`
- **Projeksiyon**: Akciğer grafisi.
- **Gözlemlenen Özellikler**: Ön planda üst ve orta akciğer zonlarını etkileyen yoğun konfluen kalsifik parankim opasiteleri.
- **Araştırma Kullanımı**: Yüksek dansiteli atenüasyon profil çıkarma ve parankim segmentasyonu.

### 6. `apical_4_chamber_echo.mp4`
- **Modalite**: Transtorasik Ekokardiyografi (TTE), Apical 4-Chamber kesiti.
- **Gözlemlenen Özellikler**: Sol Ventrikül (LV), Sağ Ventrikül (RV), Sol Atriyum (LA) ve Sağ Atriyumun (RA) gerçek zamanlı kasılması ve ritmik duvar hareketi; diastolde açılan ve sistolde koapte olan mitral ve triküspit kapak yaprakçıkları; sol atriyum içinde gözlemlenen spontan eko kontrastı ("duman").
- **Araştırma Kullanımı**: Zamansal video transformer modelleri, otomatik ejeksiyon fraksiyonu (EF) tahmini ve kalp döngüsü boyunca çoklu boşluk segmentasyonu.
