# Cerrahi AI Agent Çalıştayı: Katılımcı Kılavuzu (Participant Guide)

**Cerrahi AI Agent Çalıştayı**na hoş geldiniz. Bu kılavuz, bugünkü uygulamalı egzersiz sırasında cerrahi bir klinik problemi ayrıştırmanıza ve agentik bir yapay zeka araştırma iş akışı tasarlamanıza yardımcı olacaktır.

---

## 1. Ne İnşa Ediyoruz?

Biz tıbbi tavsiye veren bir sohbet botu (chatbot) **inşa etmiyoruz**.

Biz bir **Multi-Agent Kanıt Araştırma Asistanı (Multi-Agent Evidence Research Assistant)** tasarlıyoruz:
- Cerrahi bir araştırma sorusunu alan ve onu bileşenlerine ayıran bir **Coordinator Agent**.
- Hakemli literatürde klinik araştırmaları (RCT'ler) ve sistematik derlemeleri tarayan bir **Evidence Specialist**.
- Resmi cerrahi uzmanlık derneklerinde (örn. ASCRS, ERAS Society, SAGES, EAES, NICE) klinik uygulama kılavuzlarını tarayan bir **Guideline Specialist**.
- Bulguları düzenleyen, klinik araştırmalar ile kılavuzların nerede uzlaştığını veya çeliştiğini vurgulayan ve doğrulanmış kaynak URL'leri sunan bir **Yapılandırılmış Kanıt Özeti (Structured Brief)**.

---

## 2. Ne Tür Bir Cerrahi Problem Seçilmeli?

Şunları içeren bir cerrahi problem seçin:
- **Klinik belirsizlik veya tartışma** (örn. iki kabul görmüş cerrahi teknik).
- **Yeni cerrahi teknoloji** (örn. floresans görüntüleme, robotik cerrahi, yapay zeka desteği).
- **Perioperatif bakım paketleri** (örn. prehabilitasyon, beslenme, bağırsak hazırlığı, glisemik kontrol).
- **Zamanlama ikilemleri** (örn. erken indeks kolesistektomi ile ertelenmiş elektif cerrahi karşılaştırması).

---

## 3. İyi Bir Agent Problemini Ne Belirler?

İyi bir agent problemi, **PICOT** modeli kullanılarak çerçevelenebilen net epidemiyolojik sınırlara sahiptir:

| Eleman | Sorulacak Soru | Örnek |
| :--- | :--- | :--- |
| **P** — Population (Popülasyon) | Hangi hasta grubu? | Elektif kolorektal cerrahi geçiren yetişkinler |
| **I** — Intervention (Girişim) | Hangi prosedür, protokol veya cihaz? | Multimodal prehabilitasyon (egzersiz + beslenme) |
| **C** — Comparator (Karşılaştırıcı) | Hangi alternatife kıyasla? | Standart perioperatif bakım / desteksiz bakım |
| **O** — Outcomes (Sonuçlar) | Hangi klinik sonlanım noktaları önemli? | 30 günlük komplikasyonlar, fonksiyonel kapasite (6MWD), yatış süresi |
| **T** — Timeframe (Zaman Aralığı) | Hangi yayın aralığı? | Son 5–10 yıl |

---

## 4. Neler Kesinlikle Girilmemelidir? (Katı Güvenlik Kuralları)

> [!CAUTION]
> **KATI GÜVENLİK SINIRLARI**:
> - **GERÇEK HASTA VERİSİ KULLANMAYIN**: Asla dosya numarası, hasta baş harfleri, poliklinik notları veya ameliyat tarihleri girmeyin.
> - **PHI GİRMEYİN**: Korunan Sağlık Bilgisi (Protected Health Information - PHI) tüm yapay zeka prompt'larından kesinlikle men edilmiştir.
> - **HASTAYA ÖZGÜ KARARLAR TALEP ETMEYİN**: Asla *"Salı günü hasta X'i ameliyat etmeli miyim?"* veya *"Bu 72 yaşındaki erkeğe hangi antibiyotik dozunu vermeliyim?"* gibi sorular sormayın.
> 
> *Yapay zeka sistemimiz, eğitim ve literatür taraması amaçlı akademik bir araştırma asistanıdır. Asla bir klinik karar destek sistemi (CDSS) değildir.*

---

## 5. Örnek Nasıl Uyarlanır? (Egzersiz Çalışma Sayfası)

20 dakikalık egzersiz boyunca bu basit adım adım şablonu kullanın:

### Adım 1: Ham Fikir / Klinik İkilem
*Klinik probleminizi bir veya iki cümleyle yazın:*
> *Örnek: "Alçak anterior rezeksiyonda stapler ateşlenmeden önce perfüzyonu kontrol etmek için ICG floresans gerçekten gerekli mi?"*

### Adım 2: PICOT Ayrıştırması
- **Population (Popülasyon)**: 
- **Intervention (Girişim)**: 
- **Comparator (Karşılaştırıcı)**: 
- **Outcomes (Sonuçlar)**: 
- **Timeframe (Zaman Aralığı)**: 

### Adım 3: Uzman Görevlerine Ayrıştırma
- **Evidence Görevi**: *"[Population] grubunda [Intervention] ile [Comparator]'ı [Outcomes] açısından değerlendiren güncel çok merkezli RCT'leri ve meta-analizleri ara."*
- **Guideline Görevi**: *"[Intervention] konusunda [Hedef Dernekler, örn. SAGES, ASCRS, EAES] resmi kılavuzlarını ara."*

### Adım 4: Ana Prompt'u Oluşturma
PICOT ve uzman taleplerinizi tek bir yapılandırılmış soru altında birleştirin:
> *"For [Population], what clinical trial evidence evaluates [Intervention] compared to [Comparator] regarding [Outcomes], and what do major professional surgical society guidelines recommend regarding routine implementation?"*

---

## 6. Çıktı Nasıl Yorumlanır?

Multi-agent sistemi tarafından üretilen bir kanıt özetini (evidence brief) incelerken şu kilit bölümlere dikkat edin:

1. **`research_scope`**: Coordinator popülasyonunuzu, girişiminizi ve sonlanım noktalarınızı doğru yakaladı mı?
2. **`evidence_findings`**: Atıf yapılan çalışmalar gerçek randomize kontrollü araştırmalar (RCT) veya meta-analizler mi? Örneklem boyutlarına ve birincil sonlanım noktalarına bakın.
3. **`guideline_findings`**: Hangi uzmanlık dernekleri görüş bildirmiş? Öneri güçlü mü, koşullu mu, yoksa kılavuz yok mu?
4. **`areas_of_agreement`**: Klinik araştırmalar ile dernek kılavuzları nerede uzlaşıyor?
5. **`areas_of_disagreement`**: Klinik tartışma, uluslararası uygulama farkı veya çelişkili çalışma sonuçları nerede bulunuyor?
6. **`not_found`**: Agent sahte çalışmalar uydurmak yerine eksik verileri dürüstçe bayrakla işaretledi mi?
7. **`sources`**: URL adresleri doğrulanmış ve tıklanabilir bağlantılar mı?

---

## 7. Fikrinizi Bir Sonraki Adıma Nasıl Taşırsınız?

Çalıştay sonrasında yapılandırılmış AI agent tasarımınızı daha ileri seviyelere taşıyabilirsiniz:
- **Literatür Taraması / Meta-Analiz**: PICOT ayrıştırmasını ve arama parametrelerini resmi bir PRISMA sistematik derleme protokolünün temeli olarak kullanın.
- **Hibe Başvurusu / Araştırma Protokolü**: Araştırmacı tarafından başlatılan bir klinik çalışma hipotezi formüle etmek için tespit edilen `areas_of_disagreement` ve `uncertainty` alanlarını kullanın.
- **Kurumsal Kalite İyileştirme (QI)**: Hastanenizin cerrahi klinik yollarını (clinical pathways) dernek kılavuzları kataloğuyla karşılaştırın ve uygulama açıklarını belirleyin.
- **Kod Uygulaması**: Bu çoklu agent sistemini otomatik Python betiklerinde veya yerel veri hatlarında nasıl çalıştıracağınızı görmek için bu depodaki geliştirici ADK uygulamasını inceleyin.
- **Cloud ve Konteyner Dağıtımı (Ek Kulvar)**: Etkileşimli Web Studio'yu hastane intranetlerinde veya Google Cloud Run üzerinde Cloud Buildpacks veya Docker kullanarak barındırmak için [`cloud-deployment.md`](cloud-deployment.md) belgesine bakın.
