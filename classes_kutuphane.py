import sys
import pymysql
import datetime

tarih = datetime.datetime.now()

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Esma.2021',
                             db='kutuphane',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


class Update(object):
    def __init__(self, kitap_id):
        self.kitap_id = kitap_id

    def kitap_ismi_update(self, kitapguncelleme_kitapadi):
        cursor.execute("UPDATE kitaplar SET kitap_adi = %s WHERE id = %s", (kitapguncelleme_kitapadi, self.kitap_id))
        connection.commit()
        print('Kayıt güncellendi')

    def yazar_ismi_update(self, yazar_guncelleme_yazaradi):
        cursor.execute("UPDATE kitaplar SET yazar_adi = %s WHERE id = %s", (yazar_guncelleme_yazaradi, self.kitap_id))
        connection.commit()
        print('Kayıt güncellendi')

    def yayinevi_update(self, yayinevi_guncelleme_adi):
        cursor.execute("UPDATE kitaplar SET yayinevi = %s WHERE id = %s", (yayinevi_guncelleme_adi, self.kitap_id))
        connection.commit()
        print('Kayıt güncellendi')

    def teslim_update(self, kullanici_id, tarih):
        cursor.execute("UPDATE kitaplar SET musaitlik=1 WHERE id=%s", self.kitap_id)
        connection.commit()
        cursor.execute(
            "UPDATE kullanicilar_kitaplar SET teslim_tarihi=%s WHERE kitap_id=%s and kullanici_id=%s and teslim_tarihi IS NULL",
            (tarih, self.kitap_id, kullanici_id))
        connection.commit()
        print("Kitabınız başarıyla teslim edildi!")


"""    
def kitap_ismi_update(kitapguncelleme_kitapadi,kitapguncelleme_id):
    cursor.execute("UPDATE kitaplar SET kitap_adi = %s WHERE id = %s", (kitapguncelleme_kitapadi,kitapguncelleme_id ))
    connection.commit()
    print('Kayıt güncellendi')

def yazar_ismi_update(yazar_guncelleme_yazaradi,yazar_guncelleme_id):
    cursor.execute("UPDATE kitaplar SET yazar_adi = %s WHERE id = %s", (yazar_guncelleme_yazaradi, yazar_guncelleme_id))
    connection.commit()
    print('Kayıt güncellendi')

def yayinevi_update(yayinevi_guncelleme_adi,yayinevi_guncelleme_id):
    cursor.execute("UPDATE kitaplar SET yayinevi = %s WHERE id = %s", (yayinevi_guncelleme_adi, yayinevi_guncelleme_id))
    connection.commit()
    print('Kayıt güncellendi')
"""


class Raporlama():
    def all_data(self):
        cursor.execute(
            "SELECT kl.kullanici_adi, kl.kullanici_soyadi, kt.kitap_adi, kk.alis_tarihi, kk.donus_tarihi, kk.teslim_tarihi FROM kullanicilar_kitaplar as kk INNER JOIN kullanicilar as kl ON kk.kullanici_id = kl.id INNER JOIN kitaplar as kt ON kk.kitap_id = kt.id")
        data = cursor.fetchall()
        for i in data:
            print(
                f"Kullanıcı Adı: {i['kullanici_adi']}, Soyadı: {i['kullanici_soyadi']}, Kitap Adı: {i['kitap_adi']}, Alış TArihi: {i['alis_tarihi']}, Dönüş Tarihi: {i['donus_tarihi']}, Teslim Tarihi: {i['teslim_tarihi']}")

    def gec_teslim_edilen_kitaplar(self):
        pass

    def erken_teslim_edilen_kitaplar(self):
        pass


class Listeleme():

    def tablo_select(self, tablo_ismi):
        cursor.execute(f"SELECT * FROM {tablo_ismi}")
        sonuc_listesi = cursor.fetchall()
        for i in sonuc_listesi:
            print(i)

    def filtreli_kullanici_listele(self, tc_kimlik_no):
        cursor.execute("SELECT * FROM kullanicilar WHERE tckimlikno=%s", (tc_kimlik_no))
        kullanicilar = cursor.fetchall()
        return kullanicilar

    def filtreli_kitap_listele(self):
        while True:
            kitap_adi = input("Hangi kitabı istiyorsunuz?")
            cursor.execute(f"SELECT * FROM kitaplar WHERE musaitlik=1 AND kitap_adi LIKE '%{kitap_adi}%'")
            kitaplar = cursor.fetchall()
            if len(kitaplar) >= 1:
                for i in kitaplar:
                    print(f"Kitap ID: {i['id']}, Kitap Adı: {i['kitap_adi']}, Müsaitlik: {i['musaitlik']}")
                break
            else:
                secim = int(input(
                    "Aradığınız kitap bulunmamaktadır ya da başka birine verilmiştir.Çıkış için 1'e Başka kitap ile devam etmek için 2'ye basınız."))
                if secim == 1:
                    sys.exit()
                else:
                    continue

    def kullanicilarin_aldigi_kitaplari_listele(self, kullanici_id):
        cursor.execute(
            "SELECT kitap_id, kitap_adi FROM kullanicilar_kitaplar as k_k INNER JOIN kitaplar as kitap on kitap.id=k_k.kitap_id WHERE k_k.kullanici_id=%s and teslim_tarihi IS NULL ",
            kullanici_id)
        kullanici_kitaplari = cursor.fetchall()
        print(kullanici_kitaplari)
        print("Elinizde bulunan kitaplar yukarıdaki gibidir.")


def kitap_inputs(adet):
    for x in range(adet):
        kitap_adi = input('Kitap adı: ')
        yazar_adi = input('Yazar adı: ')
        yayinevi = input('yayınevi: ')
        basim_yili = int(input('Basım yılı: '))
        raf_adresi = input('Raf adresi: ')
        musaitlik = int(input('müsaitlik :'))

        # Kitap tipine göre listeleme
        list_object = Listeleme()
        print("Kitap tipini aşağıdaki listeye göre seçebilirsiniz.")
        list_object.tablo_select('kitaplar_tip')
        kitap_tipi = int(input('kitap tipi: '))

        print('Kitap tipini aşağıdaki listeye göre seçebilirsiniz.')
        list_object.tablo_select('kitaplar_tur')
        kitap_turu = int(input('kitap turu: '))

        kitap_ekleme(kitap_adi, yazar_adi, yayinevi, basim_yili, raf_adresi, musaitlik, kitap_tipi, kitap_turu)
        # return kitap_adi, yazar_adi, yayinevi, basim_yili, raf_adresi, musaitlik, kitap_tipi, kitap_turu


def kitap_ekleme(kitap_adi, yazar_adi, yayinevi, basim_yili, raf_adresi, musaitlik, kitap_tipi, kitap_turu):
    cursor.execute(
        'INSERT INTO kitaplar (kitap_adi, yazar_adi, yayinevi, basim_yili, raf_adresi, musaitlik, kitap_tipi, kitap_turu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )',
        (kitap_adi, yazar_adi, yayinevi, basim_yili, raf_adresi, musaitlik, kitap_tipi, kitap_turu))
    connection.commit()
    print('Kayıt eklendi.')


def kitap_silme(kitap_silinecek_id):
    cursor.execute("DELETE FROM kitaplar WHERE id=%s", (kitap_silinecek_id))
    connection.commit()
    print('Kayıt silindi.')


def kullanici_ekleme():
    kullanici_adi = input("Kullanıcı adınız nedir? ")
    kullanici_soyadi = input("Kullanıcı soyadınız nedir? ")
    tc = input("TC kimlik no nedir? ")
    print("Aşağıdaki kullanıcı tipinden birini seçiniz: ")
    list_object = Listeleme()
    list_object.tablo_select('kitaplar_tip')
    kullanici_tipi = input("Kullanıcı tipi seçiniz: ")
    email = input("Email giriniz: ")
    telefon = input("Telefon giriniz: ")
    cursor.execute(
        "INSERT INTO kullanicilar (kullanici_adi, kullanici_soyadi, tckimlikno, uye_olma_tarihi, kullanici_tipi, email, telefon) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (kullanici_adi, kullanici_soyadi, tc, tarih, kullanici_tipi, email, telefon))
    connection.commit()
    cursor.execute("SELECT max(id) as id FROM kullanicilar")
    secilen_kisiler = cursor.fetchall()
    for i in secilen_kisiler:
        secilen_kisi = i['id']
    return secilen_kisi


def kitap_kiraya_verme(secilen_kisi, secilen_kitap, tarih):
    cursor.execute(
        "INSERT INTO kullanicilar_kitaplar (kullanici_id,kitap_id,alis_tarihi,donus_tarihi) VALUES (%s, %s, %s, DATE_ADD(%s, INTERVAL 5 DAY))",
        (secilen_kisi, secilen_kitap, tarih, tarih))
    connection.commit()
    cursor.execute("UPDATE kitaplar SET musaitlik=0 WHERE id= %s", secilen_kitap)
    connection.commit()
    print("Kitap kiraya verildi.")

