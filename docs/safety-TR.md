# Güvenlik ve Klinik Sınırlar

## Projenin Niteliği ve Misyonu

**Surgical AI Agents** sistemi, cerrahlara yönelik 60 dakikalık interaktif bir workshop için özel olarak geliştirilmiş bir **eğitim ve araştırma proof-of-concept (POC)** çalışmasıdır.

Sistem; multi-agent mimarilerinin (Coordinator, Evidence Agent, Guideline Agent) karmaşık cerrahi araştırma sorularını nasıl ayrıştırabildiğini (decompose), yanıtları hakemli bilimsel literatür ve klinik kılavuzlarla nasıl doğruladığını (grounding) ve yapılandırılmış kanıt özetleri (evidence briefs) ürettiğini göstermektedir.

---

## Kesin Yasaklar ve Katı Sınırlar

Bu depo ve sistemde çalışan tüm agent'lar aşağıdaki tavizsiz güvenlik kurallarına tabidir:

### 1. Gerçek Hasta Verisi ve Sıfır PHI (Zero PHI)
- Sistem hiçbir zaman Korumalı Sağlık Bilgisi (Protected Health Information - PHI) veya Kişisel Olarak Tanımlanabilir Bilgi (Personally Identifiable Information - PII) almamalı, işlememeli, saklamamalı veya çıktı olarak üretmemelidir.
- Gerçek hasta hastane kayıtları, ameliyat notları, laboratuvar çıktıları, radyoloji/görüntüleme dosyaları, patoloji raporları veya hastayı tanımlayıcı detaylar kesinlikle yasaktır.
- Tüm test, benchmark ve demonstrasyon materyalleri **%100 sentetik, kamuya açık veya genelleştirilmiş araştırma soruları** kullanmalıdır.

### 2. Hastaya Özel Klinik Tavsiye veya Karar Verilmemesi
- Sistem hiçbir zaman bireysel bir hastanın yönetimi hakkında tavsiyede bulunmamalıdır (örn. *"Hasta X'i bugün ameliyat etmeli miyim?"* veya *"Bu hastaya hangi dozda antibiyotik uygulamalıyım?"* gibi sorulara yanıt verilmez).
- Bir kullanıcı hastaya özgü parametreler içeren bir klinik vaka sunduğunda, sistem otomatik bir güvenlik sınırı reddi (safety boundary refusal) tetiklemelidir:
  - Bireyselleştirilmiş klinik tavsiye vermeyi reddetmek.
  - Klinik bakımın lisanslı insan hekim kararı gerektirdiğini hatırlatmak.
  - Konuyu genelleştirilmiş bir cerrahi araştırma sorusu olarak yeniden çerçevelemek (reframe).

### 3. Teşhis Koyulmaması ve Klinik Karar Destek İddiasında Bulunulmaması
- Sistem hastalık veya durum teşhisi koymaz.
- Sistem bir Klinik Karar Destek Sistemi (**Clinical Decision Support System - CDSS**) **DEĞİLDİR** ve FDA, AB MDR veya uluslararası tıbbi yazılım regülasyonları kapsamında tıbbi cihaz olma iddiası taşımaz.

### 4. Halüsinasyon Kanıt veya Kaynakçaya Sıfır Tolerans
- Cerrahi uygulama kanıt bütünlüğüne dayanır. Agent'lar asla makale başlıkları, yazar isimleri, dergi adları, DOI numaraları, yayın yılları veya URL uydurmamalıdır (fabricate).
- Google Search ve URL context üzerinden grounding, atıf yapılmadan önce doğrulanmalıdır.
- Grounding mevcut değilse veya yetersizse, agent inandırıcı bir halüsinasyon üretmek yerine atıfta bulunmayı reddetmelidir.

### 5. Zorunlu Epistemik Alçakgönüllülük (Belirsizlik ve "Not Found" Durumu)
- Bilimsel konsensüs eksik olduğunda veya klinik çalışma sonuçları çeliştiğinde, sistem bu çelişkiyi `areas_of_disagreement` ve `uncertainty` alanları altında açıkça belgelendirmelidir.
- Güvenilir hakemli literatür veya resmi uzmanlık derneği kılavuzları tespit edilemediğinde, sistem tahmin yürütmek veya spekülasyon yapmak yerine açıkça `not_found: true` bildirmelidir.
- Belirsizlik hiçbir zaman bir klinik öneriye dönüştürülmemelidir.

---

## Zorunlu Güvenlik Sorumluluk Reddi (Safety Disclaimer)

Üretilen her evidence brief ve kullanıcıya dönük yanıt, standart güvenlik sorumluluk reddi beyanı ile sonlandırılmalıdır:

> **Eğitim ve Araştırma Güvenliği Sorumluluk Reddi (Educational & Research Safety Disclaimer)**:  
> *Bu kanıt özeti (evidence brief), yalnızca eğitim ve akademik inceleme amacıyla deneysel bir yapay zeka araştırma prototipi tarafından üretilmiştir. Klinik teşhis, hastaya özel tedavi önerisi veya klinik karar destek sistemi olarak kullanılmak üzere tasarlanmamıştır. Hasta yönetimine ilişkin tüm kararlar, bireysel klinik değerlendirmeye dayanarak lisanslı sağlık profesyonelleri tarafından bağımsız olarak verilmelidir.*

---

## Gelecek Geliştirmeler İçin Güvenlik Kontrol Listesi

Güncellemeleri yayınlamadan veya yeni aşamalara geçmeden önce bu denetim kontrol listesini tamamlayın:

- [ ] **Prompt Guardrails**: System prompt'ları hastaya özel yönetim sorgularının reddedilmesini zorunlu kılıyor mu?
- [ ] **Veri Hijyeni (Data Hygiene)**: Depo, kazara eklenmiş PHI, test hasta kayıtları veya API kimlik bilgileri açısından tarandı mı?
- [ ] **Schema Zorunluluğu**: Output schema, `not_found` bayraklarını ve `safety_disclaimer` alanını kesin olarak zorunlu kılıyor mu?
- [ ] **Grounding Doğrulaması**: Tüm uzman (specialist) agent'lar doğrulanmış kaynakça sunmaya sınırlandırılmış mı?
- [ ] **Sentetik Senaryolar**: Tüm workshop test senaryolarının sentetik arketipler olduğu doğrulandı mı?
- [ ] **Sınır Denetimi**: Test paketi `EDGE-07-PATIENT-SPECIFIC-SAFETY` senaryosunda sıfır hata ile çalıştı mı?
