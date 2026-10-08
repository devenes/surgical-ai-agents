# Multimodal Gösterim Varlıkları ve Lisans Kaydı (Assets Registry)

- **Dizin Kapsamı**: Tamamlayıcı multimodal çalıştay demosu için gösterim görselleri.
- **Güvenlik Kuralı**: **%100 Sıfır-PHI ve Sıfır Hasta Tanımlaması**.

---

## 1. Uyumluluk ve Lisans Standardı

Sağlık gizliliği yasaları (HIPAA, KVKK, GDPR) ve etik yapay zeka araştırma standartlarına tam uyum içinde:
- **Gerçek Hasta Görseli Yoktur**: Bu depoda hiçbir ameliyat içi hasta fotoğrafına, tanısal radyolojik taramaya (BT, MRG, Röntgen) veya kimliği belirlenebilir cerrahi videoya izin verilmez.
- **Telif Hakkı İhlali Yoktur**: Tüm gösterim görselleri şunlardan biri olmalıdır:
  1. Doğrudan kod içinde üretilmiş yöntemsel sentetik diyagramlar.
  2. Kamu Malı / Creative Commons Zero (CC0) anatomik diyagramlar.
  3. Açık izinli atıf lisanslarına (CC-BY 4.0) sahip açık erişimli tıbbi çizimler.

---

## 2. Varlık Kataloğu (Asset Catalog)

| Varlık Dosya Adı | Modalite / Konu | Kaynak / Köken | Lisans / Uyumluluk |
| :--- | :--- | :--- | :--- |
| `laparoscopic_cvs_schematic.png` | Laparoskopik kolesistektomide Strasberg Critical View of Safety'nin sentetik anatomik şematiği | Yerel Python prosedürel betiği aracılığıyla sentetik olarak üretilmiştir | **Kamu Malı / Apache-2.0** (Bu eğitsel çalıştay için özel olarak oluşturulmuştur; sıfır klinik veya hasta verisi içerir). |

---

## 3. Görsel Tanımı: `laparoscopic_cvs_schematic.png`

Sentetik görsel, laparoskopik sağ üst kadran ameliyat sahasının eğitici bir vektör şematiğini tasvir eder:
- **Anatomi**: Karaciğer konturu, safra kesesi fundus/infundibulumu, hepatosistik üçgen (Calot üçgeni), sistik kanal, sistik arter ve ana safra kanalını gösterir.
- **Diseksiyon Planları**: Temizlenmiş sistik tabanı (cystic plate) ve mobilize edilmiş safra kesesinin alt üçte birini vurgular.
- **Aletler**: Sefalik-lateral traksiyon uygulayan genel bir laparoskopik atravmatik tutucuyu tasvir eder.
- **Amaç**: Klinik veya gizlilik sorumluluğu oluşturmadan, vision-language modeli gözlemini ve uzamsal tanımayı test etmek için temiz, hastaya ait olmayan, telif haksız geometrik özellikler sağlar.
