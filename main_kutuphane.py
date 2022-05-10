import sys
import pymysql
import datetime
import classes_kutuphane

tarih = datetime.datetime.now()

#from classes_kutuphane import *

#import classes_kutuphane
#classes_obj=classes_kutuphane()


connection=pymysql.connect(host='localhost',
                     user ='root',
                     password = ' ',
                     db = 'kutuphane',
                     charset = 'utf8mb4',
                     cursorclass = pymysql.cursors.DictCursor)
cursor=connection.cursor()

# M A I N
if __name__ == '__name__':
    while True:  # Sonsuz döngü
        list_object = classes_kutuphane.Listeleme()
        print('Hoşgeldiniz.\nKütüphaneye kitap eklemek için 1e\nSilmek için 2ye\nKitap listelemek için 3e\nGüncellemek için 4e basın\nKitap kiralamak için 5e\nGelen kitapları kütüphaneye almak için 6ya basın\nRaporlama işlemleri için 7\nÇıkış için 0a basın.')
        secim = int(input('Lütfen seçiminizi girin: '))
        if secim == 1:
            # kitap ekleme
            adet = int(input('Kaç tane kitap eklemek istiyorsunuz: '))
            classes_kutuphane.kitap_inputs(adet)

        elif secim == 2:
            print('Aşağıdaki kayıtlardan hangisini silmek istiyorsunuz: ')
            list_object.tablo_select('kitaplar')
            kitap_silinecek_id = int(input('Hangi IDli kitabı silmek istiyorsunuz? '))
            classes_kutuphane.kitap_silme(kitap_silinecek_id)

        elif secim == 3:
            # kitap listeleme
            print('Kütüphanemdeki kitaplar aşağıdaki gibidir.')
            list_object.tablo_select('kitaplar')

        elif secim == 4:
            secim = int(input(
                'Hangi kolonu güncellemek istersiniz:\nKitap adı için 1e\nKitap Yazarı için 2ye\nYayınevi için 3e basın.'))
            print('Aşağıdaki kayıtlardan hangisini güncellemek istersin?')
            list_object.tablo_select('kitaplar')
            kitap_id = int(input('Hangi IDli kitabı güncellemek istiyorsunuz? '))
            update_obj = classes_kutuphane.Update(kitap_id)
            if secim == 1:
                kitapguncelleme_kitapadi = input('Güncellenecek kitap ismini giriniz: ')
                # kitap_ismi_update(kitapguncelleme_kitapadi,kitapguncelleme_id)
                update_obj.kitap_ismi_update(kitapguncelleme_kitapadi)

            elif secim == 2:
                yazar_guncelleme_yazaradi = input('Güncellenecek yazar ismini giriniz: ')
                # yazar_ismi_update(yazar_guncelleme_yazaradi,yazar_guncelleme_id)
                update_obj.yazar_ismi_update(yazar_guncelleme_yazaradi)
            elif secim == 3:
                yayinevi_guncelleme_adi = input('Güncellenecek yayinevi ismini giriniz: ')
                # yayinevi_update(yayinevi_guncelleme_adi, yayinevi_guncelleme_id)
                update_obj.yayinevi_update(yayinevi_guncelleme_adi)


            else:
                print('Lütfen doğru bir değer giriniz.')

        elif secim == 5:
            #####KIRAYA VERILECEK KITAP VE KIME VERILECEGI SECILDI
            list_object.filtreli_kitap_listele()
            secilen_kitap = int(input("Yukarıdaki listenilen kitaplardan hangisini almak istersiniz? ID giriniz."))
            tc_kimlik_no = input("Kim kitap almak istiyor? TCKN girin: ")
            kullanicilar = list_object.filtreli_kullanici_listele(tc_kimlik_no)
            if len(kullanicilar) >= 1:
                for i in kullanicilar:
                    print(f"Kullanıcı Adı: {i['kullanici_adi']}, Soyadı: {i['kullanici_soyadi']}, TC: {i['tckimlikno']}")
                    secilen_kisi = i['id']

            else:
                secim = int(input(("Kullanıcı mevcut değil eklemek için 1e basınız.")))
                if secim == 1:
                    secilen_kisi = classes_kutuphane.kullanici_ekleme()
                else:
                    print("Çıkış")
            #####KITAP KIRAYA VERME
            classes_kutuphane.kitap_kiraya_verme(secilen_kisi, secilen_kitap, tarih)

        elif secim == 6:  ##Kitap teslimi

            tc_kimlik_no = input("İşlem yapmak için lütfen tckn giriniz:")
            kullanici = list_object.filtreli_kullanici_listele(tc_kimlik_no)

            for i in kullanici:
                kullanici_id = int(i['id'])
            list_object.kullanicilarin_aldigi_kitaplari_listele(kullanici_id)
            kitap_id = int(input("Teslim etmek istediğiniz kitabın id'sini girin: "))
            update_obj = classes_kutuphane.Update(kitap_id)
            update_obj.teslim_update(kullanici_id, tarih)

        elif secim == 7:
            raporlama_obj = classes_kutuphane.Raporlama()
            secim = int(input("Tüm kiraya verilen kitap listesini ve kullanıcı listesi görmek için 1e basınız. "))
            if secim == 1:
                raporlama_obj.all_data()
            else:
                print("Yanlış bir seçim yaptınız lütfen tekrar deneyiniz.")

        elif secim == 0:
            connection.close()
            break

        else:
            print('Lütfen doğru bir değer giriniz.')