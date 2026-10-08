# Multimodal Gösterim Fallback ve Önceden Hesaplanmış Yanıtlar (Fallback Responses)

- **Kapsam**: 5 dakikalık tamamlayıcı multimodal mini-demo için acil durum prosedürleri.
- **Kural**: Canlı Agent Studio Freeform sekmesinde gecikme yaşanırsa veya yüklenmezse, bu önceden hesaplanmış gösterim metnini akıcı bir şekilde kullanın veya bağımsız Python betiğini çalıştırın.

---

## 1. Bağımsız Betik Fallback'i (Terminal)

Web konsolu yükleme butonu yanıt vermiyorsa veya yavaşsa:
1. Proje kök dizininde bir terminal penceresi açın.
2. Bağımsız referans betiğini çalıştırın (garantili sunum hızı için sıfır-token çevrimdışı mod):
   ```bash
   uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up
   ```
   *(Wi-Fi bağlantısı sağlandığında canlı Vertex AI çalıştırması için: `--offline` parametresini kaldırın)*
3. Terminalde doğrudan akan çıktıyı gösterin.

---

## 2. Önceden Hesaplanmış Doğrulanmış Gösterim Çıktısı

Tüm bulut yürütmesi kullanılamıyorsa veya Wi-Fi kesilmişse, aşağıdaki doğrulanmış çıktıyı doğrudan katılımcılara sunun:

### Aşama 1: Nötr Gözlem (Neutral Observation)
**Kullanıcı Girdisi**:
```text
Describe only the observable visual features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
```

**Doğrulanmış Model Yanıtı**:
> *Görsel, sağ üst kadrandaki laparoskopik bir ameliyat sahasını temsil eden şematik bir anatomik çizim sunmaktadır:*
> 
> 1. *İnfundibulum ve Safra Kesesi Hattı: Merkezde armut biçimli bir viseral yapı yer almakta olup, atravmatik bir laparoskopik tutucu alet ile sefalik ve lateral yönde ekarte edilmiştir.*
> 2. *Hepatosistik Üçgen (Calot Üçgeni): Karaciğerin alt kenarı, sistik kanal ve ana hepatik kanal arasında üçgen şeklinde bir anatomik alan ortaya konmuştur.*
> 3. *İki Belirgin Boru Biçimli Yapı: Safra kesesi boynunun alt kısmına giren iki izole boru yapısı tasvir edilmiştir; bu, sistik kanal ve sistik arterin tipik şematik görünümüyle uyumludur.*
> 4. *Diseksiyon Alanı (Sistik Taban): Safra kesesinin alt kısmı alttaki karaciğer yatağından ayrılmış ve fibröz sistik taban (cystic plate) açığa çıkarılmıştır.*
> 5. *Cerrahi Alet: Sağ üst kadranda doku gerginliğini koruyan bir laparoskopik tutucu forseps görünmektedir.*
> 
> *Not: Bu özet yalnızca görünür diyagramatik ve anatomik unsurları tanımlar. Tıbbi teşhis, klinik değerlendirme veya ameliyat kararları sağlamaz.*

---

## 3. Aşama 2: Eğitsel ve Bilişim Takibi

**Kullanıcı Girdisi**:
```text
Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
```

**Doğrulanmış Model Yanıtı**:
> *Cerrahi veri bilimi ve klinik yapay zeka araştırmalarında, ameliyat sahalarının görsel temsilleri klinik dışı kıyaslama ve eğitim görevleri için sıklıkla kullanılır:*
> 
> 1. *Critical View of Safety (CVS) Bilgisayarlı Görü Doğrulaması: Algoritmalar, kliplemeden önce üç Strasberg güvenlik kriterinin (hepatosistik üçgenin temizlenmesi, sistik tabanın açığa çıkarılması ve tam olarak iki yapının görülmesi) karşılanıp karşılanmadığını değerlendirmek üzere eğitilir.*
> 2. *Anlamsal Segmentasyon ve Anatomik Sınır Çizimi: Hedef organları (safra kesesi, karaciğer yatağı) yüksek riskli "kesilmeyecek" yapılardan (ana safra kanalı, sağ hepatik arter) ayırmak için evrişimli ağların (CNN) ve vision transformer modellerinin eğitilmesi.*
> 3. *Cerrahi Alet Tespiti ve Eylem Tanıma: Cerrahi iş akışı indekslemesini otomatikleştirmek için laparoskopik aletlerin (tutucular, elektrokoter kancaları, klip uygulayıcılar) uzamsal koordinatlarını ve operasyonel durumlarını tanımlama.*
> 4. *Raporlama Standartlarına Uyum: Bu modelleri değerlendiren akademik çalışmalar, modelin taşınabilirliğini ve farklı hastane görüntüleme veri setlerindeki sapma (bias) riskini değerlendirmek için DECIDE-AI ve TRIPOD-AI gibi özel raporlama kılavuzlarını kullanır.*
