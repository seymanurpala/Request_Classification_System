import csv
import os
import random

random.seed(42)

SABLONLAR = {
    "Ulaşım": [
        "Otobüs sefer saatleri yetersiz.",
        "Toplu taşıma hattı mahallemize uğramıyor.",
        "Durakta çok uzun süre araç bekliyoruz.",
        "Hat güzergahı değiştirildi, durak çok uzakta kaldı.",
        "Otobüs içi kalabalık, yolcular binemıyor.",
        "Sefer sayısı azaltıldı, iş yerine yetişemiyorum.",
        "Minibüs hattı iptal edildi, ulaşım sorunu yaşıyoruz.",
        "Engelli bireylerin kullanabileceği araç bulunmuyor.",
        "Durak kaldırıldı, yaşlılar yürüyemiyor.",
        "Akşam seferleri çok erken bitiyor.",
        "Tramvay hattı hafta sonu çalışmıyor, alternatif yol yok.",
        "37 numaralı otobüs sabah 7'den sonra gelmiyor.",
        "Dolmuş güzergahı değişti, okula ulaşamıyoruz.",
        "Otobüs durağında oturma yeri yok, yaşlılar ayakta bekliyor.",
        "Metro istasyonu çıkışında toplu taşıma bağlantısı yok.",
        "Gece seferleri kaldırıldı, işten dönemiyoruz.",
        "Okul servisi güzergahını değiştirdi, çocuklar mağdur.",
        "Duraklar arası mesafe çok fazla, yürüyemiyoruz.",
        "Tatil günlerinde sefer düzenlenmesi gerekiyor.",
        "Araçlar zamanında gelmiyor, saatler tutmuyor.",
    ],
    "Çevre ve Temizlik": [
        "Mahallemizde çöpler zamanında toplanmıyor.",
        "Sokakta biriken atıklar kötü koku yapıyor.",
        "Çöp konteynerleri uzun süredir temizlenmedi.",
        "İnşaat molozları kaldırıma bırakılmış.",
        "Cadde üzerindeki çöp kutuları taşıyor.",
        "Sokak süpürme çalışması haftalar önce durdu.",
        "Komşu bina çöplerini dışarıya atıyor.",
        "Park içinde çöp birikintisi oluştu.",
        "Çevreye atılan izmaritler yangın tehlikesi yaratıyor.",
        "Dere kenarına dökülen atıklar temizlenmiyor.",
        "Boş arsaya moloz dökülüyor, kimse müdahale etmiyor.",
        "Apartman önüne bırakılan atıklar günlerce duruyor.",
        "Pazar yeri temizlenmeden bırakıldı, koku yayılıyor.",
        "Çöp toplama saatleri düzensiz, sabah erken geliyor.",
        "Geri dönüşüm kutuları aylar önce kaldırıldı.",
        "Sokak köpekleri çöpleri dağıtıyor, temizlenmiyor.",
        "Atık su oluğu tıkandı, kötü koku çıkıyor.",
        "Ormanlık alana çöp dökülüyor.",
        "Çöp kamyonu mahallemizi atlıyor.",
        "Bahçe atıkları kaldırıma bırakılmış, yürünemez oldu.",
    ],
    "Su ve Kanalizasyon": [
        "Suyumuz sarı renkte geliyor.",
        "Kanalizasyon taşması nedeniyle sokağı kötü koku sardı.",
        "Mahallede sık sık su kesintisi yaşanıyor.",
        "Su basıncı çok düşük, üst katlara su çıkmıyor.",
        "Boru patlaması nedeniyle yol su altında kaldı.",
        "İçme suyu şebeke hattı arızalı.",
        "Kanalizasyon rögarı açık ve tehlike oluşturuyor.",
        "Su sayacı arızalı, fatura çok yüksek geldi.",
        "Yağmur suyu tahliyesi yapılmıyor, sokak su altında kalıyor.",
        "Bodrumlara kanalizasyon suyu doldu.",
        "Musluktan akan suyun tadı değişti, içemiyoruz.",
        "Su borusu patladı, yol çamura döndü.",
        "Lağım kokusu evin içine kadar geliyor.",
        "Haftada birkaç kez su kesiliyor, bildirim yapılmıyor.",
        "Bina su deposu kirli, temizlenmesi gerekiyor.",
        "Rögar kapağı kırık, kaza riski var.",
        "Suyumuz bulanık geliyor, içmeye çekiniyoruz.",
        "Bahçemizde su borusu patladı, su fışkırıyor.",
        "Alt katlara kanalizasyon suyu geliyor.",
        "Su kesintisi 2 gündür devam ediyor, bilgi verilmiyor.",
    ],
    "Park ve Bahçe": [
        "Parkımızdaki oyun grubu bozulmuş.",
        "Mahalle parkındaki çimler bakımsız durumda.",
        "Ağaç budama çalışması uzun süredir yapılmıyor.",
        "Çocuk parkındaki kaydırak tehlikeli hale geldi.",
        "Park içindeki banklar kırık ve kullanılamıyor.",
        "Yeşil alan sulama sistemi çalışmıyor.",
        "Parkta aydınlatma yetersiz, geceleri karanlık.",
        "Ağaç dalları uzayarak yola sarktı.",
        "Spor aletleri bakımsız ve paslanmış durumda.",
        "Park girişine araç park ediliyor, yaya geçişi engelleniyor.",
        "Mahalledeki tek yeşil alan yapılaşmaya açıldı.",
        "Çocuk oyun alanı çamurlu, zemin döşenmesi gerekiyor.",
        "Parkta yabani otlar büyümüş, bakım yapılmıyor.",
        "Salıncak zinciri koptu, çocuk düştü.",
        "Park içindeki çeşme çalışmıyor.",
        "Ağaç fırtınada devrildi, yolu kapattı.",
        "Piknik alanı temizlenmiyor, çöp dolu.",
        "Bahçe duvarı yıkıldı, park güvensiz hale geldi.",
        "Çim biçme makinesi mahallemizdeki parkı atlıyor.",
        "Parkta içki içiliyor, aileler gelemiyor.",
    ],
    "İmar ve Yapı": [
        "Komşumun ek binası imar planına aykırı.",
        "İnşaat sahasında güvenlik önlemleri alınmıyor.",
        "Ruhsata aykırı yapılaşma olduğu düşünülüyor.",
        "Binanın cephesi izinsiz değiştirildi.",
        "İnşaat çalışmaları gece de devam ediyor, gürültü yapıyor.",
        "Kaçak kat inşaatı tespit edildi.",
        "İnşaat tozu çevreye yayılıyor.",
        "Yıkım izni olmadan bina yıkılıyor.",
        "Ruhsatsız tadilat yapılıyor.",
        "Yapı denetim eksikliği nedeniyle tehlikeli görünüyor.",
        "Binamızın bodrum katında izinsiz işyeri açıldı.",
        "Komşu bina balkonunu kapattı, izni var mı bilmiyoruz.",
        "İnşaat çitleri kaldırımı tamamen kapattı.",
        "Eski bina yıkılmadan yeni inşaata başlandı.",
        "Depreme dayanıksız bina için ne yapabiliriz.",
        "Komşu apartmana izinsiz asansör eklendi.",
        "İnşaat aracı yolu kapattı, geçiş yok.",
        "Kaçak depo inşaatı yapılıyor.",
        "Bina cephesindeki taşlar düşüyor, tehlikeli.",
        "Ruhsatsız çatı katı inşaatı yapılıyor.",
    ],
    "Elektrik ve Aydınlatma": [
        "Sokak lambaları geceleri yanmıyor.",
        "Park çevresindeki aydınlatmalar arızalı.",
        "Mahallede sürekli elektrik kesintisi yaşanıyor.",
        "Trafo arızası nedeniyle uzun süredir elektrik yok.",
        "Elektrik direği eğildi, tehlike oluşturuyor.",
        "Sokak lambası gündüz yanıyor, gece sönüyor.",
        "Bölgemizde voltaj dalgalanması cihazlara zarar veriyor.",
        "Yeraltı kablosu arızalı, kesintiler tekrarlanıyor.",
        "Ortak alan aydınlatması aylardır yanmıyor.",
        "Trafik ışıkları arızalı, kaza riski var.",
        "Akıllı sayaç takıldıktan sonra faturalarım iki katına çıktı.",
        "Cadde aydınlatması yetersiz, gece yürümek tehlikeli.",
        "Elektrik panosu açık duruyor, çocuklar için tehlikeli.",
        "Yıldırım düşmesi sonrası mahalle karanlıkta kaldı.",
        "Elektrik sayacım sürekli hata veriyor.",
        "Sokak lambası direği devrildi, yolu kapattı.",
        "Kesinti öncesi bildirim yapılmıyor.",
        "Pano arızası nedeniyle binada elektrik yok.",
        "Geceleri sadece bazı sokaklar aydınlatılıyor, eşitsizlik var.",
        "Yüksek gerilim hattı altında oturuyoruz, tehlikeli.",
    ],
    "Hayvan Kontrolü": [
        "Sokakta başıboş köpekler çocukları korkutuyor.",
        "Yaralı bir sokak hayvanı için ekip desteği gerekiyor.",
        "Mahallede sahipsiz hayvan sayısı arttı.",
        "Saldırgan köpek nedeniyle parkta yürüyemiyoruz.",
        "Kedilere mama bırakılan alan kirletiliyor.",
        "Sahipsiz hayvanlar çöp kutularını devirip dağıtıyor.",
        "Yaralı kedi yol ortasında bulundu, yardım gerekiyor.",
        "Köpek ısırması vakası yaşandı, önlem alınması gerekiyor.",
        "Güvercin popülasyonu çok arttı, hijyen sorunu var.",
        "Sahipsiz hayvanlar için barınak kapasitesi yetersiz.",
        "Balkonuma güvercin yuva kurdu, engelleyemiyorum.",
        "Sokak kedileri arabalara zarar veriyor.",
        "Köpek sürüsü okul önünde toplanıyor, çocuklar geçemiyor.",
        "Yaralı köpek kapı önünde yatıyor, toplanması gerekiyor.",
        "Komşu köpeği sürekli havlıyor, uyuyamıyoruz.",
        "Fare istilası var, ilaçlama yapılması gerekiyor.",
        "Sokak hayvanlarına eziyet eden biri var.",
        "Kedi maması bırakan vatandaşlar kaldırımı kirletiyor.",
        "Köpek saldırısı sonucu yaralandım, ekip gelsin.",
        "Mahallede çok sayıda başıboş hayvan dolaşıyor.",
    ],
    "Yol ve Kaldırım": [
        "Kaldırım taşları kırıldığı için yürümek zorlaştı.",
        "Yolda oluşan çukur araçlara zarar veriyor.",
        "Sokağımızdaki kaldırım işgali yayaları zorluyor.",
        "Asfalt çökmesi nedeniyle araçlar hasara uğruyor.",
        "Yağmur sonrası yol çok tehlikeli hale geliyor.",
        "Yaya geçidi silik, sürücüler fark etmiyor.",
        "Engelli rampası yapılmamış, tekerlekli sandalye geçemiyor.",
        "Kaldırıma araç park ediliyor, yürüyemiyoruz.",
        "Sokak taş döşemesi bozulmuş, takılma riski var.",
        "Köprü yüzeyinde çatlaklar oluştu.",
        "Yağmurda alt geçit su doldu, geçiş yapılamıyor.",
        "Ana caddemizde büyük bir çukur var, lastik patlattım.",
        "Yol kenarındaki bariyer yıkıldı, tehlike oluşturuyor.",
        "Kaldırım yüksekliği düzensiz, düşme riski var.",
        "Sokak tamirat çalışması yarım bırakıldı.",
        "Yol çizgileri silinmiş, trafik karışıyor.",
        "Tümsek çok yüksek, araçlar hasar görüyor.",
        "Kavşakta zemin kaygan, kaza çıktı.",
        "Yol kenarı çökmüş, araçlar düşüyor.",
        "Bisiklet yolu bozulmuş, kullanılamıyor.",
    ],
    "Sosyal Yardım": [
        "Ailem için gıda yardımı talebinde bulunuyorum.",
        "İhtiyaç sahibi komşumuz için sosyal destek istiyoruz.",
        "Eğitim yardımı başvurusu hakkında bilgi almak istiyorum.",
        "Engelli bireye yönelik destek programlarına başvurmak istiyorum.",
        "Yaşlı komşumuz bakıma muhtaç, yardım gerekiyor.",
        "Kış yardımı dağıtımı hakkında bilgi almak istiyorum.",
        "Barınma desteğine ihtiyacım var.",
        "Çocuğuma burs veya eğitim desteği almak istiyorum.",
        "Hasta yakınına evde bakım hizmeti talep ediyorum.",
        "Maddi sıkıntı içindeyiz, acil yardım talep ediyoruz.",
        "Yaşlı annem için evde sağlık hizmeti talep ediyorum.",
        "3 çocuklu aileyiz, kira yardımı almak istiyoruz.",
        "İşsiz kaldım, destek programları hakkında bilgi istiyorum.",
        "Engelli çocuğum için özel eğitim desteği lazım.",
        "Depremzede olarak yardım almak istiyorum.",
        "Yakacak yardımı başvurusu nasıl yapılır.",
        "Kronik hastayım, ilaç desteğine ihtiyacım var.",
        "Yaşlı bakım evine başvuru hakkında bilgi almak istiyorum.",
        "Yalnız yaşayan komşum için sosyal hizmet talep ediyorum.",
        "Okul kıyafeti yardımı almak istiyorum.",
    ],
    "Mezarlık Hizmetleri": [
        "Mezarlıkta bakım ve temizlik yetersiz kalıyor.",
        "Defin işlemleri hakkında destek almak istiyorum.",
        "Kabir ziyaret alanlarında düzenleme yapılması gerekiyor.",
        "Mezarlık yolları bozuk, araçlar giremiyor.",
        "Mezarlık aydınlatması yetersiz, gece ziyaret edilemiyor.",
        "Mezar taşı hasar gördü, onarım gerekiyor.",
        "Mezarlık çevre duvarı yıkılmış.",
        "Mezarlıkta su tesisatı çalışmıyor.",
        "Cenaze nakil hizmetiyle ilgili bilgi almak istiyorum.",
        "Mezarlıkta güvenlik yetersiz, vandalizm yaşanıyor.",
        "Mezarlık girişinde otopark yok, araçlar yolu kapatıyor.",
        "Babamın mezarı bulunduğu alanda çevre duvarı yıkılmış.",
        "Mezarlık kapısı kilitli, giriş yapılamıyor.",
        "Defin için yer tahsisi hakkında bilgi almak istiyorum.",
        "Mezarlık içindeki yollar çamurlu, yürünemiyor.",
        "Mezar yeri işaretleri silinmiş, bulmak zorlaştı.",
        "Mezarlıkta yabani otlar temizlenmiyor.",
        "Cenaze töreninde görevli gelmedi.",
        "Mezarlık ziyaret saatleri yetersiz.",
        "Kabristanda vandalizm yaşandı, mezarlar tahrip edildi.",
    ],
}

VATANDAS_ADLARI = [
    "Ahmet Yılmaz",
    "Fatma Demir",
    "Mehmet Kaya",
    "Ayşe Çelik",
    "Mustafa Şahin",
    "Zeynep Arslan",
    "Ali Koç",
    "Hatice Öztürk",
]
ILCELER = [
    "Kadıköy",
    "Beşiktaş",
    "Üsküdar",
    "Ataşehir",
    "Maltepe",
    "Pendik",
    "Kartal",
    "Şişli",
]
GELIS_KANALLARI = ["Çağrı", "Mobil", "Web"]
EKLER = [
    " Acil çözüm bekliyorum.",
    " Lütfen ilgilenin.",
    " Konunun incelenmesini rica ederim.",
    " İlgili birim bilgilendirilsin.",
    " En kısa sürede müdahale bekliyoruz.",
    "",
]


def generate(kayitSayisi: int = 500):
    tipler = list(SABLONLAR.keys())
    secilen_tipler = [tipler[i % len(tipler)] for i in range(kayitSayisi)]
    random.shuffle(secilen_tipler)

    kayitlar = []
    for tip in secilen_tipler:
        kayitlar.append(
            {
                "talepMetni": random.choice(SABLONLAR[tip]) + random.choice(EKLER),
                "talepTipi": tip,
                "vatandasAdi": random.choice(VATANDAS_ADLARI),
                "ilce": random.choice(ILCELER),
                "gelisKanali": random.choice(GELIS_KANALLARI),
            }
        )

    return kayitlar


def writeCsv(kayitlar, dosya):
    os.makedirs(os.path.dirname(os.path.abspath(dosya)), exist_ok=True)

    with open(dosya, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=kayitlar[0].keys())
        writer.writeheader()
        writer.writerows(kayitlar)


if __name__ == "__main__":
    cikti = os.path.join(os.path.dirname(__file__), "talep_ornek.csv")

    kayitlar = generate(500)
    writeCsv(kayitlar, cikti)

    print("CSV oluşturuldu:", cikti)
    print("Toplam kayıt:", len(kayitlar))