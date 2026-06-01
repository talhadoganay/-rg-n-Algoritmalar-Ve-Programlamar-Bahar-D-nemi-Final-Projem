import sqlite3

def veritabani_olustur():
    baglanti = sqlite3.connect("hastane_veritabani.sqlite")
    imlec = baglanti.cursor()
    imlec.execute("CREATE TABLE IF NOT EXISTS randevular (tc_no, hasta_adi, poliklinik, doktor, tarih)")
    baglanti.commit()
    baglanti.close()

def islem_kaydi_tut(mesaj):
    with open("sistem_loglari.txt", "a", encoding="utf-8") as dosya:
        dosya.write(mesaj + "\n")

def doktorlari_al(poliklinik_adi):
    hastane_sozlugu = {
        "Dahiliye": ["Ahmet Yılmaz", "Ayşe Kaya", "Veli Demir"],
        "Kardiyoloji": ["Mehmet Öz", "Fatma Çelik"],
        "Göz Hastalıkları": ["Selin Can", "Burak Yıldız"],
        "Ortopedi": ["Caner Şahin", "Zeynep Arslan"]
    }
    
    if poliklinik_adi in hastane_sozlugu:
        return hastane_sozlugu[poliklinik_adi]
    return []

def yeni_randevu():
    tc = input("TC Kimlik Numaranızı Giriniz: ")
    if len(tc) != 11 or not tc.isdigit():
        print("Hatalı giriş! TC Kimlik numarası 11 haneli sayılardan oluşmalıdır.")
        return
        
    ad_soyad = input("Adınız ve Soyadınız: ")
    
    bolumler = {"1": "Dahiliye", "2": "Kardiyoloji", "3": "Göz Hastalıkları", "4": "Ortopedi"}
    
    print("\nPoliklinikler:")
    for numara, isim in bolumler.items():
        print(numara + " - " + isim)
        
    secilen_bolum_no = input("Lütfen bölüm numarasını seçiniz: ")
    
    if secilen_bolum_no not in bolumler.keys():
        print("Yanlış bölüm seçimi yaptınız.")
        return
        
    poliklinik = bolumler[secilen_bolum_no]
    doktorlar_listesi = doktorlari_al(poliklinik)
    
    print("\n" + poliklinik + " Doktorları:")
    for sira, doktor in enumerate(doktorlar_listesi, 1):
        print(str(sira) + " - " + doktor)
        
    secilen_doktor_no = input("Doktor numarasını seçiniz: ")
    
    try:
        indis = int(secilen_doktor_no) - 1
        secilen_doktor = doktorlar_listesi[indis]
    except:
        print("Geçersiz bir doktor seçimi yaptınız.")
        return
        
    randevu_tarihi = input("Randevu Tarihi (Örn: 25.05.2026): ")
    
    baglanti = sqlite3.connect("hastane_veritabani.sqlite")
    imlec = baglanti.cursor()
    imlec.execute("INSERT INTO randevular VALUES (?, ?, ?, ?, ?)", (tc, ad_soyad, poliklinik, secilen_doktor, randevu_tarihi))
    baglanti.commit()
    baglanti.close()
    
    print("\nRandevunuz başarıyla oluşturulmuştur.")
    islem_kaydi_tut(tc + " TC numaralı hasta için " + poliklinik + " bölümüne randevu oluşturuldu.")

def randevulari_goster():
    tc = input("Sorgulamak istediğiniz TC Kimlik Numarası: ")
    
    baglanti = sqlite3.connect("hastane_veritabani.sqlite")
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM randevular WHERE tc_no=?", (tc,))
    bulunan_randevular = imlec.fetchall()
    baglanti.close()
    
    if len(bulunan_randevular) == 0:
        print("Sistemde bu TC kimlik numarasına ait kayıt bulunamadı.")
    else:
        print("\n--- KAYITLI RANDEVULARINIZ ---")
        for kayit in bulunan_randevular:
            print("TC: " + kayit[0] + " | Ad: " + kayit[1] + " | Poliklinik: " + kayit[2] + " | Doktor: " + kayit[3] + " | Tarih: " + kayit[4])

def sistemi_baslat():
    veritabani_olustur()
    
    while True:
        print("\n" + "*"*30)
        print("   HASTANE RANDEVU SİSTEMİ   ")
        print("*"*30)
        print("1 - Yeni Randevu Al")
        print("2 - Randevu Sorgula")
        print("3 - Sistemden Çıkış")
        print("*"*30)
        
        kullanici_secimi = input("Yapmak istediğiniz işlemi seçiniz: ")
        
        if kullanici_secimi == "1":
            yeni_randevu()
        elif kullanici_secimi == "2":
            randevulari_goster()
        elif kullanici_secimi == "3":
            print("Sağlıklı günler dileriz. Sistem kapatılıyor...")
            break
        else:
            print("Geçersiz giriş yaptınız, lütfen tekrar deneyin.")

if __name__ == "__main__":
    sistemi_baslat()