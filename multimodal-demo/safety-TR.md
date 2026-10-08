# Multimodal Güvenlik Bariyerleri ve Yasakları (Multimodal Safety Guardrails)

- **Kapsam**: Tamamlayıcı Multimodal Demo (Agent Studio Chat / Freeform & Bağımsız Python Betiği)
- **Durum**: **KATI TAVİZSİZ POLİTİKA**

---

## 1. Kesin Yasaklar (Hard Prohibitions)

Cerrahi veya anatomik görüntüler işlenirken sistem ve sunucu aşağıdaki güvenlik sınırlarına kesinlikle uymalıdır:

### 1. Tıbbi veya Cerrahi Tanı Konulamaz
- Sistem bir görüntüden **asla** patolojik durum tanısı koymamalıdır (örn. lezyonu habis olarak sınıflandırmak, akut kolesistit teşhisi koymak, apandisiti tanımlamak).
- Klinik karar alma süreçleri için patoloji derecelendirmesi veya radyolojik evreleme çıktısı vermemelidir.

### 2. Hastaya Özgü Tedavi Önerisinde Bulunulamaz
- Sistem, görsel bulgulara dayanarak hangi tıbbi tedavinin, ilacın veya cerrahi prosedürün uygulanması gerektiği konusunda **asla** tavsiyede bulunmamalıdır.

### 3. Ameliyat İçi Cerrahi Karar Verilemez (Devam / Dur - Go / No-Go)
- Sistem **asla** ameliyat içi bir cerrahi eylem önermemelidir (örn. *"Bu yapıyı klipleyin"*, *"Buradan kesin"*, *"Açık cerrahiye geçin"*, *"Bu arteri kesmek güvenlidir"*).
- Sistem intraoperatif bir yönlendirme cihazı olarak görev yapamaz.

### 4. Klinik Risk Sınıflandırması Yapılamaz
- Sistem görüntü analizine dayanarak hastaya özgü komplikasyon olasılıkları, mortalite skorları veya risk kademeleri **asla** atamamalıdır.

### 5. Sıfır Gerçek Hasta Verisi ve Sıfır PHI
- Gerçek hasta hastane görüntüleri, kimliği belirlenebilir cerrahi video klipleri, DICOM hasta başlıkları içeren PACS dışa aktarımları veya dosya numaraları kesinlikle men edilmiştir.
- Tüm gösterim görselleri %100 sentetik diyagramlar, açık erişimli tıbbi eğitim çizimleri veya açık izin lisanslarına sahip anonim kıyaslama veri setleri olmalıdır.

---

## 2. İzin Verilen Eğitsel Davranışlar

Sistemin yalnızca **nötr görsel ve bilişimsel analiz** yapmasına izin verilir:
- **Gözlemlenebilir Görsel Özelliklerin Tanımlanması**: Geometrik şekillerin, renk varyasyonlarının, görünür cerrahi aletlerin (tutucular, klip uygulayıcılar), anatomik planların ve uzamsal işaretlerin tanımlanması.
- **Eğitsel Bilişim Tartışması**: Bilgisayarlı görü modellerinin (sınırlayıcı kutu tespiti, anlamsal segmentasyon, optik akış) akademik literatürde nasıl değerlendirildiğinin açıklanması (örn. IoU, DICE skorları, DECIDE-AI kılavuzları).
- **Kısıtlamaların Vurgulanması**: 2D kamera açılarının, ışık yansımalarının, duman engelinin ve kamera hareketinin sınırlılıklarının açıkça belirtilmesi.
