# Çalıştay Fallback ve Acil Durum Planları (Workshop Fallback & Contingency Plans)

- **Doküman Sürümü**: 1.0.0
- **Amaç**: Bulut platformu, Wi-Fi veya API sorunlarından bağımsız olarak kesintisiz bir 60 dakikalık çalıştay garanti etmek için operasyonel acil durum prosedürleri.
- **Kural**: Asla sahte sonuçlar uydurmayın; fallback mekanizmasını katılımcılara her zaman şeffaf bir şekilde açıklayın.

---

## Acil Durum Matrisi (Contingency Matrix)

| Fallback Kademesi | Tetikleyici Koşul | Acil Durum İş Akışı | Fallback Varlığı / Komut |
| :---: | :--- | :--- | :--- |
| **Tier 0 (Birincil Savunma)** | **Salon Wi-Fi kesintisi, captive portal bağlantı kopması veya sıfır konferans interneti** | **Sıfır Token'lı Çevrimdışı Modda Yerel Web UI ve CLI'a Geçiş** | **`uv run python -m app.cli all` ('Offline Mock Mode' işaretli) veya `uv run python -m adk.run --offline`** |
| **Fallback A** | Multi-agent orkestrasyonu başarısız olursa veya alt agent döngüye girerse | Agent Studio'da tek agent'lı kaynaklı sorguya geçiş | Google Search grounding aracı içeren tek agent prompt'u |
| **Fallback B** | Google Search grounding kotası biterse veya hata verirse | Önceden doğrulanmış literatür kaynaklarını ve dernek bağlantılarını sunma | `examples/research-questions/` içindeki önbelleğe alınmış alıntılar |
| **Fallback C** | Agent Studio UI yanıt vermezse, yavaşsa veya 500 hatası verirse | Programatik ADK CLI baseline çalıştırma veya doğrulanmış JSON gösterme | Terminal: `uv run python -m adk.run --offline` veya önceden hesaplanmış JSON |
| **Fallback D** | Katılımcı egzersizi aksarsa veya mekan ağı çökerse | Sunucu liderliğinde etkileşimli tahta / slayt egzersizi | Proje Dönüşüm Çalışma Sayfası (Katılımcı Kılavuzu) |

---

## ⚡ 10 Saniyelik Wi-Fi Acil Durum Geçiş Protokolü

Canlı gösterim sırasında kürsüde konferans Wi-Fi bağlantısı koparsa:
1. **Sakin kalın ve geçişi anlatın** (0-3sn):
   > *"Gerçek dünyadaki hastane sistemlerinin, WAN bağlantıları koptuğunda yerel edge fallback mekanizmalarına ihtiyaç duyduğuna dikkat edin. Tam da bu sıfır token'lı yerel simülasyon katmanını çalıştay yapımıza dahil ettik."*
2. **UI Seçeneğini veya Terminal Bayrağını Değiştirin** (3-6sn):
   - **Web UI (`http://127.0.0.1:8501`)**: Kenar çubuğundaki **"⚡ Offline Mock Mode (Zero Tokens / No API)"** kutusunu işaretleyin.
   - **Terminal**: `uv run python -m adk.run --offline` veya `uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up` komutunu çalıştırın.
3. **Kıyaslama Senaryosunu Yürütün** (6-10sn):
   - 16 önceden tanımlanmış kıyaslama senaryosundan birini seçin (örn. `NORM-01 Colorectal Prehab`, `EDGE-01 Missing Evidence` veya `EDGE-07 Patient Safety Refusal`).
   - Sistem doğrulanmış literatür sentezi, PICOT ayrıştırması, konsensüs matrisleri ve %100 JSON schema uyumu ile <100ms içinde deterministik olarak yanıt verir.

---

## Tier 0: Sıfır Token Çevrimdışı Modda Yerel Web UI

### Ne Zaman Kullanılır?
Konferans Wi-Fi ağı kararsız olduğunda, gecikme 5 saniyeyi aştığında veya internet erişimi tamamen koptuğunda.

### Çevrimdışı Olarak Tam Korunan Yetenekler:
1. **Multimodal Studio**: 3 Strasberg anatomik kriteri, Calot üçgeni diseksiyonu ve araştırma takibi ile Critical View of Safety (CVS) şematik görsel incelemesi.
2. **2 Alt Agent Konsensüs Hattı (2-Subagent Consensus Pipeline)**: Tüm 16 değerlendirme kıyaslama vakasında tam PICOT ayrıştırması, Evidence Specialist çalışma sentezi, Guideline Specialist önerileri ve Konsensüs Matrisi (Uzlaşı ve Ayrışmalar).
3. **5 Boyutlu Karşılaştırmalı Puan Kartı**: Halüsinasyon riskini, epistemik tevazuyu (`not_found: true`) ve klinik güvenlik sınırlarını sergileyen monolitik kaynaksız baseline ile kafa kafaya karşılaştırma.
4. **Güvenlik Sınırlarının Uygulanması**: Hastaya özgü klinik sorgular için katı reddetme ve eğitsel yeniden çerçeveleme (örn. 72 yaş albümin 2.8 sorgusu).
5. **JSON Schema Uyumluluğu**: `agents/coordinator/output-schema.json` standardına karşı %100 katı doğrulama.

---

## Fallback A: Tek Agent'lı Kaynaklı Demo (Single-Agent Grounded Demo)

### Ne Zaman Kullanılır?
Coordinator alt agent'ları çağıramazsa, bir araç özyineleme hatasına girerse veya Agent Studio Preview içinde çoklu agent delegasyonu durursa.

### Sunucu Eylemi ve Anlatımı:
1. Panik yapmadan akıcı bir geçiş yapın:
   > *"Multi-agent sistemlerde orkestrasyon birden fazla dağıtık akıl yürütme adımı içerir. Çok adımlı delegasyon olmadan kaynak kullanımını (grounding) doğrudan incelemek istersek, tek bir kaynaklı araştırma agent'ını doğrudan sorgulayabiliriz."*
2. Agent Studio içinde tek bir kaynaklı agent açın (veya Preview içinde doğrudan `evidence-specialist` düğümünü seçin).
3. Aşağıdaki birleşik prompt'u yapıştırın:
   ```text
   For adults undergoing elective colorectal surgery, summarize what recent randomized trials and ERAS Society guidelines report regarding multimodal prehabilitation. Ground your answer using Google Search and cite verified titles and URLs. Conclude with a safety disclaimer.
   ```
4. Tek bir adımda doğrudan arama aracı çağrısını ve kaynaklı sentezi gözlemleyin.

---

## Fallback B: Önceden Hesaplanmış Doğrulanmış Alıntılar

### Ne Zaman Kullanılır?
Canlı gösterim sırasında Google Search grounding hız sınırına (HTTP 429) veya ağ zaman aşımına uğrarsa veya boş parçacıklar döndürürse.

### Sunucu Eylemi ve Anlatımı:
1. Grounding bağımlılığını dürüstçe açıklayın:
   > *"Gerçek zamanlı arama grounding'i web indekslerine yapılan canlı sorgulara dayanır. Yüksek trafikli ortamlarda arama API'leri kısıtlamaya (throttling) uğrayabilir. Bu sorgu için önceden doğrulanmış alıntı kaydımızı inceleyelim."*
2. [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) veya [`examples/research-questions/colorectal-prehabilitation.md`](../examples/research-questions/colorectal-prehabilitation.md) içindeki doğrulanmış alıntı kaydını açın.
3. Katılımcılara doğrulanmış alıntıları inceletin:
   - **PREHAB Çalışması**: Molenaar et al., *JAMA Surgery* 2023. [https://jamanetwork.com/journals/jamasurgery/fullarticle/2804564](https://jamanetwork.com/journals/jamasurgery/fullarticle/2804564)
   - **BJS Meta-analizi**: Waterland et al., *BJS* 2021. [https://academic.oup.com/bjs/article/108/8/900/6298514](https://academic.oup.com/bjs/article/108/8/900/6298514)
   - **ERAS Society Kılavuzları**: Gustafsson et al., *World J Surg* / ERAS Society 2023. [https://erassociety.org/guidelines/colorectal/](https://erassociety.org/guidelines/colorectal/)
   - **ASCRS Uygulama Parametreleri**: You et al., *Dis Colon Rectum* 2023. [https://fascrs.org/healthcare-providers/practice-parameters](https://fascrs.org/healthcare-providers/practice-parameters)

---

## Fallback C: Programatik ADK CLI Referansı

### Ne Zaman Kullanılır?
Google Cloud Console web uygulamasına erişilemiyorsa, yavaşsa veya bölgesel bir UI kesintisi yaşanıyorsa.

### Sunucu Eylemi ve Anlatımı:
1. Terminal ekranına geçin:
   > *"Bu mimarinin en güçlü yönlerinden biri, Agent Studio'da görsel olarak inşa edilen her şeyin Google Agent Development Kit (ADK) içinde birebir 1:1 kod karşılığına sahip olmasıdır. Web konsolu erişilemez hale gelirse, tüm çoklu agent sistemini doğrudan terminalimizden çalıştırabiliriz."*
2. Depo kök dizininde terminali açın ve çalıştırın:
   ```bash
   .venv/bin/python -m adk.run
   ```
3. PICOT çıkarımını, alt agent delegasyonunu ve ortaya çıkan JSON çıktısını canlı konsol akışında gösterin.
4. Alternatif olarak biçimlendirilmiş JSON dosyasını doğrudan görüntüleyin:
   ```bash
   cat examples/research-questions/colorectal-prehabilitation-gemini-3-8.json
   ```

---

## Fallback D: Sunucu Liderliğinde Etkileşimli Tahta Egzersizi

### Ne Zaman Kullanılır?
Uygulamalı egzersiz bölümünde (Dakika 30–50) salon Wi-Fi bağlantısı tamamen çökerse ve katılımcıların çevrimiçi araçları kullanması engellenirse.

### Sunucu Eylemi ve Anlatımı:
1. Etkileşimli bir masterclass formatına geçiş yapın:
   > *"Bir AI Sistem Mimarı gibi düşünmek için internet bağlantısına gerek yoktur. Bunu yazı tahtasında hep birlikte yapalım. Bu hafta klinik çalışmasında cerrahi bir ikilemle karşılaşan kim var?"*
2. Bir katılımcıdan klinik ikilemini önermesini isteyin (örn. *"Akut pankreatitte erken ve aralıklı kolesistektomi karşılaştırması"*).
3. Yazı tahtasında veya sunum ekranında 5 parçalı PICOT çerçevesini birlikte oluşturun:
   - **P**: Hafif akut biliyer pankreatit ilk atağı geçiren yetişkin hastalar.
   - **I**: İlk yatışta (index admission) 72 saat içinde laparoskopik kolesistektomi.
   - **C**: Taburculuktan 4–6 hafta sonra gecikmiş elektif kolesistektomi.
   - **O**: Tekrarlayan biliyer olaylar, yeniden yatış, açığa geçme oranı, toplam hastanede kalış süresi.
   - **T**: Son 5 yıl.
4. Evidence Specialist (IAP/APA çalışmaları, PONCHO çalışması) ve Guideline Specialist (WSES, Tokyo Kılavuzları, IAP/APA) için tam alt agent sorgu talimatlarını ana hatlarıyla belirleyin.
5. Sentezi tahmin etme konusunda katılımcılara rehberlik edin: İndeks cerrahinin yeniden yatışları azalttığı konusunda uzlaşı; iltihaplı safra keselerindeki teknik zorluk konusunda görüş ayrılıkları.
