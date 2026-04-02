import csv
import random
import os

random.seed(42)

SABLONLAR = {
    "Ulaşım":              "Otobüs sefer saatleri yetersiz.",
    "Çevre ve Temizlik":   "Mahallemizde çöpler zamanında toplanmıyor.",
    "Su ve Kanalizasyon":  "Suyumuz sarı renkte geliyor.",
    "Park ve Bahçe":       "Parkımızdaki oyun grubu bozulmuş.",
    "İmar ve Yapı":        "Komşumun ek binası imar planına aykırı.",
}

VATANDAS_ADLARI = ["Ahmet Yılmaz", "Fatma Demir", "Mehmet Kaya"]
ILCELER         = ["Kadıköy", "Beşiktaş", "Üsküdar"]
GELIS_KANALLARI = ["Çağrı", "Mobil"]
EKLER           = [" Acil çözüm bekliyorum.", " Lütfen ilgilenin.", ""]


def generate(kayitSayisi: int = 50):
    tipler = list(SABLONLAR.keys())

    result = []
    for _ in range(kayitSayisi):
        tip = random.choice(tipler)

        result.append({
            "talepMetni": SABLONLAR[tip] + random.choice(EKLER),
            "talepTipi": tip,
            "vatandasAdi": random.choice(VATANDAS_ADLARI),
            "ilce": random.choice(ILCELER),
            "gelisKanali": random.choice(GELIS_KANALLARI),
        })

    return result


def writeCsv(kayitlar, dosya):
    os.makedirs(os.path.dirname(os.path.abspath(dosya)), exist_ok=True)

    with open(dosya, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=kayitlar[0].keys())
        writer.writeheader()
        writer.writerows(kayitlar)


if __name__ == "__main__":
    cikti = os.path.join(os.path.dirname(__file__), "talep_ornek.csv")

    kayitlar = generate(50)
    writeCsv(kayitlar, cikti)

    print("✅ CSV oluşturuldu:", cikti)