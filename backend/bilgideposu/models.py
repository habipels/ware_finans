from django.db import models
from users.models import *
# Create your models here.
from datetime import datetime
from PIL import Image
from io import BytesIO
from ckeditor.fields import RichTextField
class banka(models.Model):
    secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır")
    )
    entkodu_secim = (
        ("",""),
        ("1","1"),
        ("2","2")
    )
    hesap_tur = (
        ("",""),
        ("Ticari","Ticari"),
        ("Kredi","Kredi"),
        ("Kredi Kartı","Kredi Kartı")
        
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    banka_kodu = models.CharField(max_length=100,verbose_name="Banka Kodu",blank=True,null=True)
    entkodu = models.CharField(max_length=10,choices=entkodu_secim,verbose_name="Ent Kodu",default="",blank=True,null=True)
    banka_adi = models.CharField(max_length=200,verbose_name="Banka Adı",blank=True,null=True)
    sube_adi = models.CharField(max_length=200,verbose_name="Şube Adı",blank=True,null=True)
    sube_kodu = models.CharField(max_length=200,verbose_name="Şube Kodu",blank=True,null=True)
    hesap_turu = models.CharField(max_length=100,choices=hesap_tur,verbose_name="Hesap Turu",blank=True,null=True,default="")
    hesap_adi = models.CharField(max_length=200,verbose_name="Hesap Adı",blank=True,null=True)
    hesap_no = models.CharField(max_length=200,verbose_name="Hesap No",blank=True,null=True)
    iban_numarasi = models.CharField(max_length=30,verbose_name="İban Numarası",blank=True,null=True)
    kullanabilir_kredi_tutari = models.CharField(max_length=200,verbose_name="Kullanabilir kredi Tutarı",null=True,blank=True)
    ozel_kod = models.CharField(max_length=100,verbose_name="Özel Kod",blank=True,null=True)
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi", choices=doviz,default="",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    toplam_yatirilan = models.FloatField(verbose_name="Toplam Yatırılan",blank=True,null=True)
    toplam_cekilen = models.FloatField(verbose_name="Toplam Çekilen",blank=True,null=True)
    toplam_bakiye = models.FloatField(verbose_name="Bakiye",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
class banka_yetkilisi(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    adi_soyadi = models.CharField(max_length=200,verbose_name="Banka Yetkilisi Adı Soyadı ",blank=True, null=True)
    gorevi = models.CharField(max_length=200,verbose_name="Görevi",blank=True,null=True)
    istelefonu = models.CharField(max_length=20,verbose_name="İş Telefonu",blank=True,null=True)
    dahili_numara = models.CharField(max_length=100,verbose_name="Dahili Numara",blank=True,null=True)
    gsm = models.CharField(max_length=100,verbose_name="GSM",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
class banka_kodlari(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    banka_muhasebe_hesap_kodu = models.CharField(max_length=200,verbose_name="Banka Muhasebe Hesap Kodu ",blank=True, null=True)
    kredi_kartı_hesap_kodu = models.CharField(max_length=200,verbose_name="Kredi Kartı Hesap Kodu",blank=True,null=True)
    verilen_cekler_hesap_kodu = models.CharField(max_length=200,verbose_name="Verilen Çekler Hesap Kodu ",blank=True, null=True)
    tahsil_cekler_hesap_kodu = models.CharField(max_length=200,verbose_name="Tahsil Çekleri Hesap Kodu",blank=True,null=True)
    tahsil_senetleri_hesap_kodu = models.CharField(max_length=200,verbose_name="Tahsil Senetleri Hesap Kodu ",blank=True, null=True)
    teminat_cekler_hesap_kodu = models.CharField(max_length=200,verbose_name="Teminat Çekleri Hesap Kodu",blank=True,null=True)
    teminat_senetleri_hesap_kodu = models.CharField(max_length=200,verbose_name="Teminat Senetleri Hesap Kodu",blank=True,null=True)
    ilgilikisi= models.CharField(max_length=200,verbose_name="İlgili Kişi",blank=True,null=True)
    telefonbilgisi = models.CharField(max_length=200,verbose_name="Telefon Bilgisi",blank=True,null=True)
    adresbilgisi = models.CharField(max_length=200,verbose_name="Adres Bilgisi",blank=True,null=True)
class banka_notlari(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    banka_nottarihi = models.DateField(verbose_name="Not Tarihi",blank=True,null=True)
    banka_not = models.TextField(verbose_name="Not ",blank=True, null=True)
class banka_kredikartibilgileri(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    tahsilatkodu = models.CharField(max_length=200,verbose_name="Tahsilat Kodu",blank=True,null=True)
    tahsilatsekli = models.CharField(max_length=200,verbose_name="Tahsilat Şekli",blank=True,null=True)
    taksitadedi = models.CharField(max_length=200,verbose_name="Taksitli Çekim",blank=True,null=True)
    taksitaralikligun = models.CharField(max_length=200,verbose_name="Taksitli Çekim",blank=True,null=True)
    bankahesabinagecissekli = models.CharField(max_length=200,verbose_name="Banka Hesabına Geçiş Şekli",blank=True,null=True)
    hesabagecissuresigun =  models.CharField(max_length=200,verbose_name="Hesaba Geçiş Süresi Gün",blank=True,null=True)
    carihesapkayitsekli = models.CharField(max_length=200,verbose_name="Cari Hesap Geçiş Şekli",blank=True,null=True)
    komisyonorani= models.CharField(max_length=200,verbose_name="Komisyon Oranı",blank=True,null=True)
    komisyontutari =  models.CharField(max_length=200,verbose_name="Komisyon Tutarı",blank=True,null=True)
    komisyongiderkodu  = models.CharField(max_length=200,verbose_name="Komisyon gider Kodu",blank=True,null=True)
    promosyonorani =  models.CharField(max_length=200,verbose_name="Promosyon Oranı",blank=True,null=True)
    promosyontutari = models.CharField(max_length=200,verbose_name="Promosyon Tutarı",blank=True,null=True)
    promosyonkesintisekli = models.CharField(max_length=200,verbose_name="Promosyon Kesinti Şekli",blank=True,null=True)
    promosyongiderkodu = models.CharField(max_length=200,verbose_name="Promosyon Gider Kodu",blank=True,null=True)
    hizmetorani=  models.CharField(max_length=200,verbose_name="Hizmet Oranı",blank=True,null=True)
    hizmettutari = models.CharField(max_length=200,verbose_name="Hizmet Tutarı",blank=True,null=True)
    hizmetgiderkodu = models.CharField(max_length=200,verbose_name="Hizmet Gider Kodu",blank=True,null=True)
    hizmetkesintisekli  = models.CharField(max_length=200,verbose_name="Hizmet Kesinti Şekli",blank=True,null=True)
    kredikartaciklama = models.TextField(verbose_name="Açıklama",blank=True,null=True)
    taksitgunleri = models.CharField(max_length=20,verbose_name="Taksit Günleri Hafta Sonuna Denk Gelmesin",blank=True,null=True)

class tevkifat_tur_kodu (models.Model):
    hesap_turu = (
        ("1","Genel Planlar"),
        ("2","Özel Planlar"),
    )
    secme = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır"),
    )
    kamu_ozel = (
        ("",""),
        ("Kamu","Kamu"),
        ("Özel","Özel"),
    )
    stopaj_belge_turu_secme =(
        ("",""),
        ("Yok","Yok"),
        ("S.M. Makbuz","S.M. Makbuz"),
        ("M. Makbuz","M. Makbuz"),
        ("Gider Pusulası","Gider Pusulası"),
        ("Fatura","Fatura"),
        ("Diğer","Diğer"),
    )
    tevkifat_orani_secim = (
        ("",""),
        ("2/10","2/10"),
        ("3/10","3/10"),
        ("4/10","4/10"),
        ("5/10","5/10"),
        ("7/10","7/10"),
        ("9/10","9/10"),
        ("10/10","10/10")
    )
    ay = (
        ("",""),
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
        ("6","6"),
        ("7","7"),
        ("8","8"),
        ("9","9"),
        ("10","10"),
        ("11","11"),
        ("12","12"),
    )
    hesap_kodu = models.CharField(max_length=100,verbose_name="Hesap Kodu",blank=True,null=True)
    hesap_adi = models.CharField(max_length=100,verbose_name="Hesap Adı",blank=True,null=True)
    detay = models.CharField(max_length=100,verbose_name="Detay",blank=True,null=True,choices=secme,default="")
    vergi_tc_no = models.CharField(max_length=100,verbose_name="Vergi/TC No",blank=True,null=True)
    vergi_dairesi = models.CharField(max_length=100,verbose_name="Vergi Dairesi",blank=True,null=True)
    borc_toplam = models.CharField(max_length=100,verbose_name="Borç Toplam",blank=True,null=True)
    alacak_toplam = models.CharField(max_length=100,verbose_name="Alacak Toplam",blank=True,null=True)
    bakiye_toplam = models.CharField(max_length=100,verbose_name="Bakiye Toplam",blank=True,null=True)
    bakiye_tipi = models.CharField(max_length=100,verbose_name="Bakiye Tipi",blank=True,null=True)
    borclu_alacakli = models.CharField(max_length=100,verbose_name="Borçlu Alacaklı",blank=True,null=True)
    miktarli = models.CharField(max_length=100,verbose_name="Miktarlı",blank=True,null=True,choices=secme,default="")
    stok_kodu = models.CharField(max_length=100,verbose_name="Stok Kodu",blank=True,null=True)
    kdv_orani = models.BigIntegerField(verbose_name="KDV Oranı",default=0)
    iliskili_kdv_hesap_kodu = models.ForeignKey('self',related_name ="iliskili_kdv_hesap_kodular",blank=True,null=True,verbose_name="İlişkili KDV Hesap Kodu",on_delete=models.SET_NULL)
    kamumu_ozelmi = models.CharField(max_length=100,verbose_name="Kamu Mu Özel Mi ? 120 veya 320 ler",blank=True,null=True,choices=secme,default="")
    hesap_aciklamasi = models.CharField(max_length=200,verbose_name="Hesap Açıklaması",blank=True,null=True)
    grup_kodu = models.CharField(max_length=200,verbose_name="Grup Kodu",blank=True,null=True)
    ba_bslerde_kullanilsinmi = models.CharField(max_length=100,verbose_name="Ba/Bs lerde Kullanılsın mı ?",blank=True,null=True,choices=secme,default="")
    kur_farkinida_kullan = models.CharField(max_length=100,verbose_name="Kur Farkınıda Kullan ?",blank=True,null=True,choices=secme,default="")
    stopaj_hesap_kodu = models.ForeignKey('self',related_name ="stopaj_hesap_kodular",blank=True,null=True,verbose_name="Stopaj Hesap Kodu",on_delete=models.SET_NULL)
    stopaj_orani = models.BigIntegerField(verbose_name="Stopaj Oranı",default=0)
    stopaj_tur_kodu = models.CharField(max_length=200,verbose_name="Stopaj Tür Kodu",blank=True,null=True)
    stopaj_belge_turu = models.CharField(max_length=100,verbose_name="Stopaj Belge Türü",blank=True,null=True,choices=stopaj_belge_turu_secme,default="")
    tevkifat_hesap_kodu = models.ForeignKey('self',related_name ="tevkifat_hesap_kodular",blank=True,null=True,verbose_name="Tevkifat KDV Hesap Kodu",on_delete=models.SET_NULL)
    tevkifat_orani = models.CharField(max_length=100,verbose_name="Tevkifat Orani",blank=True,null=True,choices=tevkifat_orani_secim,default="")
    ilave_edilecek_kdv_mi = models.CharField(max_length=100,verbose_name="İlave Edilecek KDV mi?",blank=True,null=True,choices=secme,default="")
    iade_edilecek_kdv_mi = models.CharField(max_length=100,verbose_name="İade Edilecek KDV mi?",blank=True,null=True,choices=secme,default="")
    ozel_matrah_mi = models.CharField(max_length=100,verbose_name="Özel Matrah Mi? ",blank=True,null=True,choices=secme,default="")
    kredi_karti_satis_mi = models.CharField(max_length=100,verbose_name="Kredi Kartı Satış Mi?",blank=True,null=True,choices=secme,default="")
    yuklenilen_iadeli_konu_olan_kdv_mi = models.CharField(max_length=100,verbose_name="Yüklenilen İadeli Konu Olan KDV Mi?",blank=True,null=True,choices=secme,default="")
    ihrac_kayitli_satis_kdv_mi_85 = models.CharField(max_length=100,verbose_name="İhraç Kayıtlı Satış KDV Mi? (85)",blank=True,null=True,choices=secme,default="")
    ihrac_kayitli_satis_kdv_mi_87 = models.CharField(max_length=100,verbose_name="İhraç Kayıtlı Satış KDV Mi? (87)",blank=True,null=True,choices=secme,default="")
    mutabakat_ayi = models.CharField(max_length=100,verbose_name="Mutabakat Ayı",blank=True,null=True,choices=ay,default="")
    yurt_ici_satis_mi = models.CharField(max_length=100,verbose_name="Yurt İçi Satış Mi? (600,601,602 Hariç)",blank=True,null=True,choices=secme,default="")
    bagli_oldugu_firma = models.ForeignKey(firma, blank=True, null=True, on_delete=models.SET_NULL)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    degistiremez_bilgisi = models.BooleanField(default=False)
class HesapPlanlari(models.Model):
    hesap_turu = (
        ("1", "Genel Planlar"),
        ("2", "Özel Planlar"),
    )
    secme = (
        ("", ""),
        ("Evet", "Evet"),
        ("Hayır", "Hayır"),
    )
    kamu_ozel = (
        ("", ""),
        ("Kamu", "Kamu"),
        ("Özel", "Özel"),
    )
    stopaj_belge_turu_secme = (
        ("", ""),
        ("Yok", "Yok"),
        ("S.M. Makbuz", "S.M. Makbuz"),
        ("M. Makbuz", "M. Makbuz"),
        ("Gider Pusulası", "Gider Pusulası"),
        ("Fatura", "Fatura"),
        ("Diğer", "Diğer"),
    )
    tevkifat_orani_secim = (
        ("", ""),
        ("2/10", "2/10"),
        ("3/10", "3/10"),
        ("4/10", "4/10"),
        ("5/10", "5/10"),
        ("7/10", "7/10"),
        ("9/10", "9/10"),
    )
    ay = (
        ("", ""),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    )
    hesap_kodu = models.CharField(max_length=100, verbose_name="Hesap Kodu", blank=True, null=True)
    hesap_adi = models.CharField(max_length=100, verbose_name="Hesap Adı", blank=True, null=True)
    detay = models.CharField(max_length=100, verbose_name="Detay", blank=True, null=True, choices=secme, default="")
    vergi_tc_no = models.CharField(max_length=100, verbose_name="Vergi/TC No", blank=True, null=True)
    vergi_dairesi = models.CharField(max_length=100, verbose_name="Vergi Dairesi", blank=True, null=True)
    borc_toplam = models.FloatField(default=0 ,verbose_name="Borç Toplam", blank=True, null=True)
    alacak_toplam = models.FloatField(default=0 , verbose_name="Alacak Toplam", blank=True, null=True)
    bakiye_toplam = models.FloatField(default=0 , verbose_name="Bakiye Toplam", blank=True, null=True)
    bakiye_tipi = models.CharField(max_length=100, verbose_name="Bakiye Tipi", blank=True, null=True)
    borclu_alacakli = models.CharField(max_length=100, verbose_name="Borçlu Alacaklı", blank=True, null=True)
    miktarli = models.CharField(max_length=100, verbose_name="Miktarlı", blank=True, null=True, choices=secme, default="")
    stok_kodu = models.CharField(max_length=100, verbose_name="Stok Kodu", blank=True, null=True)
    kdv_orani = models.FloatField(verbose_name="KDV Oranı", default=0)
    iliskili_kdv_hesap_kodu2 = models.ForeignKey('self', related_name="iliskili_kdv_hesap_kodlari", blank=True,
                                                null=True, verbose_name="İlişkili KDV Hesap Kodu",
                                                on_delete=models.CASCADE)
    kamumu_ozelmi = models.CharField(max_length=100, verbose_name="Kamu Mu Özel Mi? 120 veya 320 ler", blank=True,
                                     null=True, choices=secme, default="")
    hesap_aciklamasi = models.CharField(max_length=200, verbose_name="Hesap Açıklaması", blank=True, null=True)
    grup_kodu = models.CharField(max_length=200, verbose_name="Grup Kodu", blank=True, null=True)
    ba_bslerde_kullanilsinmi = models.CharField(max_length=100, verbose_name="Ba/Bs lerde Kullanılsın mı?", blank=True,
                                                null=True, choices=secme, default="")
    kur_farkinida_kullan = models.CharField(max_length=100, verbose_name="Kur Farkını da Kullan?", blank=True,
                                            null=True, choices=secme, default="")
    stopaj_hesap_kodu2 = models.ForeignKey('self', related_name="stopaj_hesap_kodlari", blank=True, null=True,
                                           verbose_name="Stopaj Hesap Kodu", on_delete=models.CASCADE)
    stopaj_orani = models.BigIntegerField(verbose_name="Stopaj Oranı", default=0)
    stopaj_tur_kodu = models.CharField(max_length=200, verbose_name="Stopaj Tür Kodu", blank=True, null=True)
    stopaj_belge_turu = models.CharField(max_length=100, verbose_name="Stopaj Belge Türü", blank=True, null=True,
                                         choices=stopaj_belge_turu_secme, default="")
    tevkifat_hesap_kodu2 = models.ForeignKey('self', related_name="tevkifat_hesap_kodlari", blank=True, null=True,
                                             verbose_name="Tevkifat KDV Hesap Kodu", on_delete=models.CASCADE)
    kdv_islem_turu = models.ForeignKey('tevkifat_tur_kodu', related_name="kdv_islem_turleri", blank=True, null=True,
                                       verbose_name="KDV İşlem Türü", on_delete=models.CASCADE)
    tevkifat_orani = models.CharField(max_length=100, verbose_name="Tevkifat Oranı", blank=True, null=True,
                                      choices=tevkifat_orani_secim, default="")
    ilave_edilecek_kdv_mi = models.CharField(max_length=100, verbose_name="İlave Edilecek KDV mi?", blank=True,
                                             null=True, choices=secme, default="")
    iade_edilecek_kdv_mi = models.CharField(max_length=100, verbose_name="İade Edilecek KDV mi?", blank=True, null=True,
                                            choices=secme, default="")
    ozel_matrah_mi = models.CharField(max_length=100, verbose_name="Özel Matrah Mı?", blank=True, null=True,
                                      choices=secme, default="")
    kredi_karti_satis_mi = models.CharField(max_length=100, verbose_name="Kredi Kartı Satış Mı?", blank=True, null=True,
                                            choices=secme, default="")
    yuklenilen_iadeli_konu_olan_kdv_mi = models.CharField(max_length=100,
                                                          verbose_name="Yüklenilen İadeli Konu Olan KDV Mi?",
                                                          blank=True, null=True, choices=secme, default="")
    ihrac_kayitli_satis_kdv_mi_85 = models.CharField(max_length=100, verbose_name="İhraç Kayıtlı Satış KDV Mi? (85)",
                                                     blank=True, null=True, choices=secme, default="")
    ihrac_kayitli_satis_kdv_mi_87 = models.CharField(max_length=100, verbose_name="İhraç Kayıtlı Satış KDV Mi? (87)",
                                                     blank=True, null=True, choices=secme, default="")
    mutabakat_ayi = models.CharField(max_length=100, verbose_name="Mutabakat Ayı", blank=True, null=True, choices=ay,
                                     default="")
    yurt_ici_satis_mi = models.CharField(max_length=100, verbose_name="Yurt İçi Satış Mı? (600,601,602 Hariç)",
                                         blank=True, null=True, choices=secme, default="")
    bagli_oldugu_firma = models.ForeignKey(firma, blank=True, null=True, on_delete=models.SET_NULL)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    degistiremez_bilgisi = models.BooleanField(default=False)

class banka_kart_bilgileri(models.Model):
    hafta = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır"),
    )
    tahsilat_sekilleri_secim =(
        ("",""),
        ("Tek Çekim","Tek Çekim"),
        ("Tek Çekim Taksitli","Tek Çekim Taksitli"),
        ("Taksitli Çekim","Taksitli Çekim"),
    )
    gecis_sekli = (
        ("",""),
        ("Hemen","Hemen"),
        ("Gecikmeli","Gecikmeli"),
        ("Taksitli","Taksitli"),
    )
    komisyon_sekli = (
        ("",""),
        ("İlk Taksitle","İlk Taksitle"),
        ("Taksitlendirilmiş","Taksitlendirilmiş"),
    )
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    tahsilat_kodu = models.CharField( max_length=100,blank=True, null=True,verbose_name = "Tahsilat Kodu")
    tahsilat_sekli = models.CharField(choices=tahsilat_sekilleri_secim,blank=True, null=True,default= "",verbose_name="Tahsilat Şekilleri", max_length=100)
    taksit_adedi = models.CharField(max_length=100,verbose_name="Taksit Adedi",blank=True, null=True)
    taksit_araliklari_gun = models.CharField(max_length=100,verbose_name="Taksit Aralıkları (Gün)",blank=True, null=True)
    banka_hesap_gecis_sekli = models.CharField(choices=gecis_sekli,blank=True, null=True,default= "",verbose_name="Banka Hesap Geçiş Şekli", max_length=100)
    banka_hesap_gecis_gun = models.CharField(max_length=100,verbose_name="Banka Hesap Geçiş (Gün)",blank=True, null=True)
    cari_hesap_kayit_sekli = models.CharField(max_length=100,choices=gecis_sekli,default="" ,verbose_name="Cari Hesap Kayıt Şekli",blank=True, null=True)
    komisyon_orani = models.CharField(max_length=100,verbose_name="Komisyon Oranı (%)",blank=True, null=True)
    komisyon_tutari = models.CharField(max_length=100,verbose_name="Komisyon Tutarı",blank=True, null=True)
    komisyon_kesinti_sekli = models.CharField(max_length=100,choices=komisyon_sekli,default="",verbose_name="Komisyon Kesinti Şekli",blank=True, null=True)
    komisyon_gider_kodu = models.CharField(max_length=100,verbose_name="Komisyon Gider Kodu Tutarı",blank=True, null=True)
    promosyon_orani = models.CharField(max_length=100,verbose_name="promosyon Oranı (%)",blank=True, null=True)
    promosyon_tutari = models.CharField(max_length=100,verbose_name="promosyon Tutarı",blank=True, null=True)
    promosyon_kesinti_sekli = models.CharField(max_length=100,choices=komisyon_sekli,default="",verbose_name="promosyon Kesinti Şekli",blank=True, null=True)
    promosyon_gider_kodu = models.CharField(max_length=100,verbose_name="Promosyon Gider Kodu Tutarı",blank=True, null=True)
    hizmet_orani = models.CharField(max_length=100,verbose_name="Hizmet Oranı (%)",blank=True, null=True)
    hizmet_tutari = models.CharField(max_length=100,verbose_name="Hizmet Tutarı",blank=True, null=True)
    hizmet_kesinti_sekli = models.CharField(max_length=100,choices=komisyon_sekli,default="",verbose_name="Hizmet Kesinti Şekli",blank=True, null=True)
    hizmet_gider_kodu = models.CharField(max_length=100,verbose_name="Hizmet Gider Kodu Tutarı",blank=True, null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    hafta_sonuna_denk_gelmesin = models.CharField(max_length=100,choices=hafta,default="",verbose_name="Hafta Sonlarına Denk Gelmesin",blank=True, null=True)
class Kasa(models.Model):
    secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır")
    )
    entkodu_secim = (
        ("",""),
        ("1","1"),
        ("2","2")
    )
   
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    kasa_kodu = models.CharField(max_length=100,verbose_name="Kasa Kodu",blank=True,null=True)
    entkodu = models.CharField(max_length=10,choices=entkodu_secim,verbose_name="Ent Kodu",default="",blank=True,null=True)
    kasa_adi = models.CharField(max_length=200,verbose_name="kasa Adı",blank=True,null=True)
    ozel_kod = models.CharField(max_length=100,verbose_name="Özel Kod",blank=True,null=True)
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi", choices=doviz,default="",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    toplam_tahsilat = models.FloatField(verbose_name="Toplam Tahsilat",blank=True,null=True)
    toplam_odeme = models.FloatField(verbose_name="Toplam Ödeme",blank=True,null=True)
    toplam_bakiye = models.FloatField(verbose_name="Bakiye",blank=True,null=True)
    muh_kodu = models.CharField(max_length=100,verbose_name="Muh Kodu",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    silinme_bilgisi = models.BooleanField(default=False)


class cari_kartlar(models.Model):
    detay_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır",)
    )
    mukellefyet_turu_secim = (
        ("",""),
        ("Tüzel Kişi","Tüzel Kişi"),
        ("Gerçek Kişi","Gerçek Kişi"),
    )
    tip_secim = (
        ("",""),
        ("1","1"),
        ("2","2"),
    )
    doviz = (
        ("",""),
        ("TL","TL"),
        ("Euro","Euro"),
        ("Dolar","Dolar")
        
    )
    cari_kart_tipi_secim =(
        ("",""),
        ("Alıcı","Alıcı"),
        ("Satıcı","Satıcı"),
        ("Her İkisi","Her İkisi"),
        ("Ortak","Ortak"),
        ("Özel Cari","Özel Cari"),
        ("Personel","Personel"),
        ("Palsiyer","Palsiyer"),
        ("Gider","Gider"),
        ("Gelir","Gelir"),
        ("Diğer","Diğer"),
        ("Fason","Fason"),
        ("Üye","Üye"),
    )
    ana_cari_kodu = models.CharField(max_length=100,verbose_name="Ana Cari Kodu",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    detay = models.CharField(max_length=100,verbose_name="Detay",choices=detay_secim,default="",blank=True,null=True)
    listede_gorunsun = models.CharField(max_length=100,verbose_name="Listede Görünsün",choices=detay_secim,default="",blank=True,null=True)
    cari_kodu = models.CharField(max_length=100,verbose_name="Cari Kodu",blank=True,null=True)
    mukellefyet_turu = models.CharField(max_length=100,verbose_name="Mükelelefiyet Türü",choices=mukellefyet_turu_secim,default="",blank=True,null=True)
    tip = models.CharField(max_length=100,verbose_name="Tip",choices=tip_secim,default="",blank=True,null=True)
    cari_hesap_kilitli = models.CharField(max_length=100,verbose_name="Cari Hesap Kilitli",choices=detay_secim,default="",blank=True,null=True)
    takip_doviz_cinsi = models.CharField(max_length=100,verbose_name="Takip Döviz Cinsi",choices=doviz,default="",blank=True,null=True)
    cari_adi = models.CharField(max_length=200,verbose_name="Cari Adı",blank=True,null=True)
    yetkili_adi = models.CharField(max_length=100,verbose_name="Yetkili Adı",blank=True,null=True)
    gorevi = models.CharField(max_length=100,verbose_name="Görevi",blank=True,null=True)
    istihbarat = models.CharField(max_length=100,verbose_name="İstihbarat",blank=True,null=True)
    cari_kart_tipi = models.CharField(max_length=100,verbose_name="Cari Kart Tipi",choices=cari_kart_tipi_secim,default="",blank=True,null=True)
    borc_tutari = models.BigIntegerField(verbose_name="Borç Tutarı (TL)",blank=True,null=True,default="0")
    alacak_tutari = models.BigIntegerField(verbose_name="Alacak Tutarı (TL)",blank=True,null=True,default="0")
    bakiye_tutari = models.BigIntegerField(verbose_name="Bakiye Tutarı (TL)",blank=True,null=True,default="0")
    ozel_kod_1 = models.CharField(verbose_name="Özel Kod 1",max_length=100,blank=True,null=True)
    ozel_kod_2 = models.CharField(verbose_name="Özel Kod 2",max_length=100,blank=True,null=True)
    satici = models.CharField(verbose_name="Satıcı",max_length=100,blank=True,null=True)
    departman = models.CharField(verbose_name="Departman",max_length=100,blank=True,null=True)
    grup_kod_1 = models.CharField(verbose_name="Grup Kod 1",max_length=100,blank=True,null=True)
    grup_kod_2 = models.CharField(verbose_name="Grup Kod 2",max_length=100,blank=True,null=True)
    grup_kod_3 = models.CharField(verbose_name="Grup Kod 3",max_length=100,blank=True,null=True)
    muhkodu = models.CharField(max_length=100,verbose_name="Muh. Kodu",blank=True,null=True)
    tevkifatkodu = models.CharField(max_length=100,verbose_name="Tevkifat Kodu",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class Giderler(models.Model):
    detay_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır",)
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    ana_gider_kodu = models.CharField(max_length=100,verbose_name="Ana Gider Kodu",blank=True,null=True)
    gider_kodu = models.CharField(max_length=100,verbose_name="gider Kodu",blank=True,null=True)
    gider_adi =  models.CharField(max_length=200,verbose_name="Gİder Adı",blank=True,null=True)
    detay = models.CharField(max_length=100,verbose_name="Detay",choices=detay_secim,default="",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    birim = models.CharField(max_length=200,verbose_name="birim",blank=True,null=True)
    kdv = models.BigIntegerField(verbose_name="KDV (%)",blank=True,null=True)
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi", choices=doviz,default="",blank=True,null=True)
    birim_fiyat_tl = models.CharField(max_length=200,verbose_name="birim Fiyat TL",blank=True,null=True)
    birim_fiyat_doviz = models.CharField(max_length=200,verbose_name="birim Fiyat Döviz",blank=True,null=True)
    ozel_kod_1 = models.CharField(verbose_name="Özel Kod 1",max_length=100,blank=True,null=True)
    toplam_alacak = models.CharField(max_length=100,verbose_name="Toplam Tahsilat",blank=True,null=True)
    toplam_borc = models.CharField(max_length=100,verbose_name="Toplam Ödeme",blank=True,null=True)
    toplam_bakiye = models.CharField(max_length=100,verbose_name="Bakiye",blank=True,null=True)
    muh_kodu1 = models.CharField(max_length=100,verbose_name="Muh Kodu 1",blank=True,null=True)
    muh_kodu2 = models.CharField(max_length=100,verbose_name="Muh Kodu 2",blank=True,null=True)
    muh_kodukdv = models.CharField(max_length=100,verbose_name="Muh Kodu KDV",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
class Gelirler(models.Model):
    detay_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır",)
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    ana_gelir_kodu = models.CharField(max_length=100,verbose_name="Ana gelir Kodu",blank=True,null=True)
    gelir_kodu = models.CharField(max_length=100,verbose_name="gelir Kodu",blank=True,null=True)
    gelir_adi =  models.CharField(max_length=200,verbose_name="gelir Adı",blank=True,null=True)
    detay = models.CharField(max_length=100,verbose_name="Detay",choices=detay_secim,default="",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    birim = models.CharField(max_length=200,verbose_name="birim",blank=True,null=True)
    kdv = models.BigIntegerField(verbose_name="KDV (%)",blank=True,null=True)
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi", choices=doviz,default="",blank=True,null=True)
    birim_fiyat_tl = models.CharField(max_length=200,verbose_name="birim Fiyat TL",blank=True,null=True)
    birim_fiyat_doviz = models.CharField(max_length=200,verbose_name="birim Fiyat Döviz",blank=True,null=True)
    ozel_kod_1 = models.CharField(verbose_name="Özel Kod 1",max_length=100,blank=True,null=True)
    toplam_alacak = models.CharField(max_length=100,verbose_name="Toplam Tahsilat",blank=True,null=True)
    toplam_borc = models.CharField(max_length=100,verbose_name="Toplam Ödeme",blank=True,null=True)
    toplam_bakiye = models.CharField(max_length=100,verbose_name="Bakiye",blank=True,null=True)
    muh_kodu1 = models.CharField(max_length=100,verbose_name="Muh Kodu 1",blank=True,null=True)
    muh_kodu2 = models.CharField(max_length=100,verbose_name="Muh Kodu 2",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
class kasa_fisleri(models.Model):
    fis_islem_turu = (
        ("",""),
        ("Tahsilat Fişi","Tahsilat Fişi"),
        ("Ödeme Fişi","Ödeme Fişi"),
        ("Virman Fişi","Virman Fişi"),
        ("Döviz Fişi","Döviz Fişi"),
        ("Açılış Fişi","Açılış Fişi"),
        ("Kasa Tahsilat Makbuzu","Kasa Tahsilat Makbuzu"),
        ("Kasa Ödeme Makbuzu","Kasa Ödeme Makbuzu"),
        ("Maaş Ödeme (Kasa)","Maaş Ödeme (Kasa)"),
        ("Ödeme Fişi","Ödeme Fişi"),
        ("Tahsilat Fişi","Tahsilat Fişi"),
        ("Maaş Ödemesi (Kasa)","Maaş Ödemesi (Kasa)"),
        ("Bankaya Yatırılan","Bankaya Yatırılan"),
        ("Bankadan Çekilen","Bankadan Çekilen"),
        ("Çek/Senet Tahsili","Çek/Senet Tahsili"),
        ("Senet Ödemesi","Senet Ödemesi"),
    )
    entkodu_secim = (
        ("",""),
        ("1","1"),
        ("2","2")
    )
   
    kasa_bilgis = models.ForeignKey(Kasa,blank=True,null=True,verbose_name="Kasa Bilgisi",on_delete=models.CASCADE)
    fis_islemi = models.CharField(max_length=200,verbose_name="Kasa Fiş İşlem Türü",default="",choices=fis_islem_turu)
    tarih = models.DateField(verbose_name="İşlem Saati",blank=True,null=True,)
    saat = models.TimeField(verbose_name="İşlem Saati")
    evrak_no = models.CharField(max_length=200,verbose_name="Evrak No",blank=True,null=True)
    entkodu = models.CharField(max_length=10,choices=entkodu_secim,verbose_name="Ent Kodu",default="",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
    odeme_tutari = models.CharField(verbose_name="Borç Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    tahsilat_tutari = models.CharField(verbose_name="Alacak Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    banka_bilgisi = models.ForeignKey(banka,blank=True,null=True,verbose_name="Banka Bilgisi",on_delete=models.SET_NULL)
    gider_bilgisi = models.ForeignKey(Giderler,blank=True,null=True,verbose_name="Gider Bilgisi",on_delete=models.SET_NULL)
    gelri_bilgis = models.ForeignKey(Gelirler,blank=True,null=True,verbose_name="Gelir Bilgisi",on_delete=models.SET_NULL)
    m = models.CharField(max_length=10,verbose_name="M Bilgisi",blank=True,null=True)
    ozel_kod_1 = models.CharField(verbose_name="Özel Kod 1",max_length=100,blank=True,null=True)
    ozel_kod_2 = models.CharField(verbose_name="Özel Kod 2",max_length=100,blank=True,null=True)
    ent = models.CharField(max_length=10,verbose_name="ent? Bilgisi",blank=True,null=True)
    uygunkur = models.CharField(max_length=100,verbose_name="Uygun Kur",blank=True,null=True)
    sube_kodu = models.ForeignKey(sube,blank=True,null=True,verbose_name="Gelir Bilgisi",on_delete=models.SET_NULL)
    departman = models.CharField(max_length=100,verbose_name="Departman",blank=True,null=True)
    islemi_yapan = models.CharField(max_length=100,verbose_name="Tahsilatı / Ödemeyi Yapan",blank=True,null=True)
    islemi_kaydeden_kullanici =  models.CharField(max_length=100,verbose_name="İşlemi Kaydeden Kullanıcı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)

class ulke_ulke_kodlari(models.Model):
    ulke_kodu = models.CharField(max_length=10,verbose_name="Ülke Kodu")
    ulke_adi = models.CharField(max_length=200,verbose_name="Ülke Adı")

class cari_kartislemleri_adresleri_kimlik(models.Model):
    cari_bilgisi = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Bilgisi",on_delete=models.CASCADE)
    adres1 = models.CharField(max_length=200,verbose_name="Adres 1 Bilgisi",blank=True,null=True)
    ilce = models.CharField(max_length=200,verbose_name="İlçe Bilgisi",blank=True,null=True)
    il = models.CharField(max_length=200,verbose_name="il Bilgisi",blank=True,null=True)
    telefon = models.CharField(max_length=20,verbose_name="Telefon Bilgisi",blank=True,null=True)
    faks = models.CharField(max_length=20,verbose_name="Faks Bilgisi",blank=True,null=True)
    telefon2 = models.CharField(max_length=20,verbose_name="Telefon2 Bilgisi",blank=True,null=True)
    Telefon3 = models.CharField(max_length=20,verbose_name="Telefon 3 Bilgisi",blank=True,null=True)
    gsm1 = models.CharField(max_length=20,verbose_name="Gsm1 Bilgisi",blank=True,null=True)
    gsm2 = models.CharField(max_length=20,verbose_name="Gsm2 Bilgisi",blank=True,null=True)
    posta_kodu = models.CharField(max_length=200,verbose_name="Posta Kodu",blank=True,null=True)
    ulke =  models.ForeignKey(ulke_ulke_kodlari,blank=True,null=True,verbose_name="Cari Bilgisi",on_delete=models.SET_NULL)
    vergi_dairesi = models.ForeignKey(vergi_dairesi,blank=True, null=True,on_delete=models.SET_NULL)
    tc_veya_vergi_no = models.CharField(max_length=100,verbose_name="TC Veya Vergi No",blank=True,null=True)
    eposta_adresi = models.EmailField(max_length=200,verbose_name="Eposta Aderesi",blank=True,null=True)
    web_adresi = models.CharField(max_length=200,verbose_name="Web Adresi",blank=True,null=True)
    adres2 = models.CharField(max_length=200,verbose_name="Adres 2 Bilgisi",blank=True,null=True)
    ilce2 = models.CharField(max_length=200,verbose_name="İlçe Bilgisi",blank=True,null=True)
    il2 = models.CharField(max_length=200,verbose_name="il Bilgisi",blank=True,null=True)
    telefon4 = models.CharField(max_length=20,verbose_name="Telefon Bilgisi",blank=True,null=True)
    faks2 = models.CharField(max_length=20,verbose_name="Faks Bilgisi",blank=True,null=True)
    gsm3 = models.CharField(max_length=20,verbose_name="Gsm1 Bilgisi",blank=True,null=True)
    telefon5 = models.CharField(max_length=20,verbose_name="Gsm2 Bilgisi",blank=True,null=True)
    ulke2 = models.CharField(max_length=200,verbose_name="Ülke Bilgisi",blank=True,null=True)
    posta_kodu2 = models.CharField(max_length=200,verbose_name="Posta Kodu",blank=True,null=True)
    adi = models.CharField(max_length=200,verbose_name="ADI Bilgisi",blank=True,null=True)
    soyadi = models.CharField(max_length=200,verbose_name="SOYADI Bilgisi",blank=True,null=True)
    babaadi = models.CharField(max_length=200,verbose_name="BABA ADI Bilgisi",blank=True,null=True)
    anneadi = models.CharField(max_length=200,verbose_name="ANNE ADI Bilgisi",blank=True,null=True)
    dogum_yeri =  models.CharField(max_length=200,verbose_name="Doğum Bilgisi",blank=True,null=True)
    dogum_tarihi = models.DateField(verbose_name="Doğum Tarihi")
    cinsiyet = models.CharField(max_length=200,verbose_name="Cinsiyet Bilgisi",blank=True,null=True)
    seri_no = models.CharField(max_length=200,verbose_name="Seri No Bilgisi",blank=True,null=True)
    ssk_bagkur_no = models.CharField(max_length=200,verbose_name="SSK / Bağkur Bilgisi",blank=True,null=True)

class cari_kartislemleri_diger_bilgiler(models.Model):
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    cari_bilgisi = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Bilgisi",on_delete=models.CASCADE)
    risklimiti = models.FloatField(verbose_name="Risk Limiti",blank=True,null=True)
    digerdovizcinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi",choices=doviz,default="")
    faizvadefarki = models.CharField(max_length=100,verbose_name="Faiz Vade Farkı",blank=True,null=True)
    odemesuresigun = models.CharField(max_length=200,verbose_name="Ödeme Süresi Gün",blank=True,null=True)
    iskontoorani = models.FloatField(verbose_name="İskonto Oranı",blank=True,null=True)
    karorani =  models.FloatField(verbose_name="Kar Oranı",blank=True,null=True)
    taksitsayisi = models.BigIntegerField(verbose_name="Taksit Sayısı",blank=True,null=True)
    taksitodemegunuherayin = models.BigIntegerField(verbose_name="Taksit Her Ayın Şu Günü",blank=True,null=True)
    satisfiyati = models.CharField(max_length=100,verbose_name="Satış Fiyatı",blank=True,null=True)
    alisfiyati= models.CharField(max_length=100,verbose_name="Alış Fiyatı",blank=True,null=True)
    stokgrupkodu = models.CharField(max_length=100,verbose_name="Stok Grup Kodu",blank=True,null=True)
    iskontoorani2 = models.FloatField(verbose_name="İskonto Oranı",blank=True,null=True)
    indim1 = models.CharField(max_length=100,verbose_name="İndirim 1",blank=True,null=True)
    indim2 = models.CharField(max_length=100,verbose_name="İndirim 2",blank=True,null=True)
    indim3 = models.CharField(max_length=100,verbose_name="İndirim 3",blank=True,null=True)
    indim4 = models.CharField(max_length=100,verbose_name="İndirim 4",blank=True,null=True)
    indim5 = models.CharField(max_length=100,verbose_name="İndirim 5",blank=True,null=True)
    indim6 = models.CharField(max_length=100,verbose_name="İndirim 6",blank=True,null=True)
    uygunkursecenek = models.CharField(max_length=100,verbose_name="Uygun Kur ",blank=True,null=True)
    otvicin_kullan = models.BooleanField(verbose_name="ÖTV İçin Kullan",default=False)
    bankaadi = models.CharField(max_length=200,verbose_name="Banka Adı",blank=True,null=True)
    subesi =models.CharField(max_length=200,verbose_name="Şube Adı",blank=True,null=True)
    bankadovizcinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi",choices=doviz,default="")
    hesapno =models.CharField(max_length=200,verbose_name="Hesap No",blank=True,null=True)
    iban = models.CharField(max_length=200,verbose_name="IBAN",blank=True,null=True)

class cari_kartislemleri_sube_bilgiler(models.Model):
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    cari_bilgisi = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Bilgisi",on_delete=models.CASCADE)
    subebilgilerisubekodu = models.CharField(max_length=100,verbose_name="Şube Kodu",blank=True,null=True)
    subebilgilerisubeadi = models.CharField(max_length=200,verbose_name="Şube Adı",blank=True,null=True)
    subebilgileridovizcinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi",choices=doviz,default="")
    subebilgileriborctutari = models.FloatField(verbose_name="Borç Tutarı",blank=True,null=True)
    subebilgilerialacaktutari = models.FloatField(verbose_name="Alacak Tutarı",blank=True,null=True)
    subebilgileribakiyetutari = models.FloatField(verbose_name="Bakiye Tutarı",blank=True,null=True)
    subebilgileriba = models.CharField(max_length=10,verbose_name="Borçlu Alacaklı",blank=True,null=True)
    subebilgilerivadetarihi = models.DateField(verbose_name="Vade Tarihi",blank=True,null=True)
    subebilgileriadres = models.CharField(max_length=200,verbose_name="Şube Adresi",blank=True,null=True)
    subebilgilerisemt = models.CharField(max_length=200,verbose_name="ŞubeSemt Bilgisi",blank=True,null=True)
    subebilgilerisehir = models.CharField(max_length=200,verbose_name="Şube Şehir",blank=True,null=True)
    subebilgileritelefon = models.CharField(max_length=20,verbose_name="Telefon Numarası",blank=True,null=True)
    subebilgileriyetkili = models.CharField(max_length=200,verbose_name="Şube Yetkilisi",blank=True,null=True)
    subebilgileriodemesuresi = models.CharField(max_length=200,verbose_name="Şube Ödeme Süresi",blank=True,null=True)
    subebilgilerivadehesapyonetimi = models.CharField(max_length=200,verbose_name="Şube Yonetim HEsabı",blank=True,null=True)
    subebilgilerimuhkodu = models.CharField(max_length=200,verbose_name="Muhtasar Kodu",blank=True,null=True)
    subebilgileripostakodu = models.CharField(max_length=200,verbose_name="Şube POsta Kodu",blank=True,null=True)

class cari_kartislemleri_notlar(models.Model):
    cari_bilgisi = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Bilgisi",on_delete=models.CASCADE)
    notlartarihi = models.DateField(verbose_name="Notlar Tarihi",blank=True,null=True)
    notlarsatici = models.CharField(max_length=200,verbose_name="Satıcı",blank=True,null=True)
    notlarnot  = models.TextField(verbose_name="Not",blank=True,null=True)

class cari_kartislemleri_firma_gorevilisi(models.Model):
    cari_bilgisi = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Bilgisi",on_delete=models.CASCADE)
    firmagoreviadi = models.CharField(max_length=200,verbose_name="Firme Görevili ADı Soyadı",blank=True,null=True)
    firmagorevligorevi = models.CharField(max_length=200,verbose_name="Görevli Görevi",blank=True,null=True)
    firmagorevliistelefonu = models.CharField(max_length=20,verbose_name="Görevli Telefon Numarası",blank=True,null=True)
    firmagorevlidahilinumara = models.CharField(max_length=20,verbose_name="Firma FGörevil iTelefon Dahili Numara",blank=True,null=True)
    firmagorevligsm = models.CharField(max_length=20,verbose_name="Firma Görevili Gsm",blank=True,null=True)
    firmaaciklama = models.TextField(verbose_name="Firma Açıklama",blank=True,null=True)



class KasaFisIslemleri(models.Model):
    islem_turu_secim = (
        ("",""),
        ("Tahsilat Fişi","Tahsilat Fişi"),
        ("Ödeme Fişi","Ödeme Fişi"),
        ("Virman Fişi","Virman Fişi"),
        ("Döviz Fişi","Döviz Fişi"),
        ("Açılış Fişi","Açılış Fişi"),
        ("Kasa Tahsilat Makbuzu","Kasa Tahsilat Makbuzu"),
        ("Kasa Ödeme Makbuzu","Kasa Ödeme Makbuzu"),
        ("Maaş Ödeme (Kasa)","Maaş Ödeme (Kasa)"),
        ("Cari Ödeme Fişi","Cari Ödeme Fişi"),
        ("Cari Tahsilat Fişi","Cari Tahsilat Fişi"),
        ("Cari Maaş Ödemesi (Kasa)","Cari Maaş Ödemesi (Kasa)"),
        ("Bankaya Yatırılan","Bankaya Yatırılan"),
        ("Bankadan Çekilen","Bankadan Çekilen"),
        ("Çek/Senet Tahsili","Çek/Senet Tahsili"),
        ("Senet Ödemesi","Senet Ödemesi"),
    )
    entsecim = (
        ("", ""),
        ("1", "1"),
        ("2", "2"),
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "£"),
        ("Dolar", "$")
    )
    kendisi_secme =  models.ForeignKey('self',blank=True,null=True,verbose_name="makbuzlar için",related_name='children',on_delete=models.SET_NULL)
    islem_turu = models.CharField(max_length=200, verbose_name="İşlem Türü", default="", choices=islem_turu_secim)
    tarih = models.DateField(verbose_name="İşlem Tarihi", blank=True, null=True)
    saat = models.TimeField(verbose_name="İşlem Saati", blank=True, null=True)
    evrak_no = models.CharField(max_length=100, verbose_name="Evrak Tarihi", blank=True, null=True)
    ent_kodu = models.CharField(max_length=2, verbose_name="Ent Kodu", default="", choices=entsecim)
    birinciislem_sube_bilgisi = models.ForeignKey(sube, blank=True, null=True, verbose_name="Şube",
                                                   on_delete=models.SET_NULL,
                                                   related_name='birinciislem_kasa_fis_islemleri_set')
    ozelkod1 = models.CharField(max_length=200, verbose_name="Özel Kod", blank=True, null=True)
    ozelkod2 = models.CharField(max_length=200, verbose_name="Özel Kod 2", blank=True, null=True)
    birinci_departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    birinci_kasa_bilgisi = models.ForeignKey(Kasa, verbose_name="Birinci Kasa Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='birinci_kasa_fis_islemleri_set')
    birinci_kasa_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    gelir_bilgisi = models.ForeignKey(Gelirler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                      on_delete=models.SET_NULL, related_name='gelir_kasa_fis_islemleri_set')
    gider_bilgisi = models.ForeignKey(Giderler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                      on_delete=models.SET_NULL, related_name='gider_kasa_fis_islemleri_set')
    gelir_muh_kodu = models.CharField(max_length=200, verbose_name="Gelir Muhtasar Kodu", blank=True, null=True)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    aciklama = models.TextField(verbose_name="İşlem Açıklama ", blank=True, null=True)
    islemi_yapan = models.CharField(max_length=250, verbose_name="İşlemi Yapan", blank=True, null=True)
    tutar = models.FloatField(verbose_name="İşlem Tutarı", blank=True, null=True)
    tutar_tl = models.FloatField(verbose_name="İşlem Tutarı (TL)", blank=True, null=True)
    doviz_tutar = models.FloatField(verbose_name="İşlem Tutarı döviz", blank=True, null=True)
    ikinci_islem_sube_bilgisi = models.ForeignKey(sube, blank=True, null=True, verbose_name="Şube",
                                                  on_delete=models.SET_NULL,
                                                  related_name='ikinciislem_kasa_fis_islemleri_set')
    ikinci_gelir_bilgisi = models.ForeignKey(Gelirler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                             on_delete=models.SET_NULL,
                                             related_name='ikinci_gelir_kasa_fis_islemleri_set')
    ikinci_gider_bilgisi = models.ForeignKey(Giderler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                             on_delete=models.SET_NULL,
                                             related_name='ikinci_gider_kasa_fis_islemleri_set')
    gider_muh_kodu = models.CharField(max_length=200, verbose_name="Gİder Muhtasar Kodu", blank=True, null=True)
    ikinci_kasa_bilgisi = models.ForeignKey(Kasa, verbose_name="İkinci Kasa Bilgisi", blank=True, null=True,
                                            on_delete=models.SET_NULL, related_name='ikinci_kasa_fis_islemleri_set')
    ikinci_departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    ikinci_kasa_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    islem_durumu = models.BooleanField(default=False, verbose_name="İşlem Tamamlandıysa tikli olacak")
    satici = models.CharField(max_length=200, verbose_name="SAtıcı", blank=True, null=True)
    kampkodu = models.CharField(max_length=200, verbose_name="Kamp Kodu", blank=True, null=True)
    gunluk_kur = models.CharField(max_length=200, verbose_name="Günlük Kur", blank=True, null=True)
    uygun_kur = models.CharField(max_length=200, verbose_name="Uygun Kur", blank=True, null=True)
    alacakbilgisi = models.CharField(max_length=200, verbose_name="alacakbilgisi", blank=True, null=True)
    gider_durumu = models.CharField(max_length=100,verbose_name="Gider Durumu",blank=True,null=True)
    gideryuzdesi= models.FloatField(verbose_name="Gider yüzdesi",blank=True,null=True)
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    banka_bilgisi = models.ForeignKey(banka,blank=True,null=True,verbose_name="Banka Bilgisi",on_delete=models.SET_NULL)
    banka_kasa_muh_kodu = models.CharField(max_length=200, verbose_name="Banka Muhtasar Kodu", blank=True, null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False)
    islem_sonucu_bakiye_birinci_kasa = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_ikinci_kasa = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_cari = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_banka = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
class kdv_istisna_kodu(models.Model):
    kod = models.CharField(max_length=100,verbose_name="KDV İstisna Kodu",blank=True,null=True)
    kod_bilgi = models.CharField(max_length=100,verbose_name="KDV İstisna Kodu",blank=True,null=True)
    icerik = models.CharField(max_length=200,verbose_name="KDV İstisna Yazısı",blank=True,null=True)


class stok_kartlar(models.Model):
    detay_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır",)
    )
    mukellefyet_turu_secim = (
        ("",""),
        ("Hammadde","Hammadde"),
        ("Yarı Mamul","Yarı Mamul"),
        ("Mamul","Mamul"),
        ("Ticari Mal","Ticari Mal"),
        ("Demirbaş","Demirbaş"),
    )
    tip_secim = (
        ("",""),
        ("1","1"),
        ("2","2"),
    )
    ana_stok_kodu = models.CharField(max_length=100,verbose_name="Ana Stok Kodu",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    detay = models.CharField(max_length=100,verbose_name="Detay",choices=detay_secim,default="",blank=True,null=True)
    listede_gorunsun = models.CharField(max_length=100,verbose_name="Listede Görünsün",choices=detay_secim,default="",blank=True,null=True)
    stok_kodu = models.CharField(max_length=100,verbose_name="Stok Kodu",blank=True,null=True)
    stok_adi = models.CharField(max_length=200,verbose_name="Stok Adı",blank=True,null=True)
    stok_turu = models.CharField(max_length=100,verbose_name="Stok Türü",choices=mukellefyet_turu_secim,default="",blank=True,null=True)
    stok_hesap_kilitli = models.CharField(max_length=100,verbose_name="Stok Hesap Kilitli",choices=detay_secim,default="",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    image  = models.ImageField(upload_to='stokkartiimage/',blank=True,null=True,verbose_name="Stok kartı resmi")
    def save(self, *args, **kwargs):
        super(stok_kartlar, self).save(*args, **kwargs)
        if self.image:
            with Image.open(self.image.path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width > 800:
                    new_width = 800
                    new_height = int((new_width / width) * height)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=60)
                    self.image.save(self.image.name, content=buffer, save=False)
                    super(stok_kartlar, self).save(*args, **kwargs)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class stok_birim_alis_satis_birimi(models.Model):
    brim_islemleri = (
        ("",""),
        ("Adet","Adet")
    )
    lot_kullanim_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır")
    )
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_karti_bilgisi_set')
    birinci_birim = models.CharField(max_length=100,verbose_name="Birinci  Birim",choices=brim_islemleri,default="")
    ikinci_birim = models.CharField(max_length=100,verbose_name="İkinci  Birim",choices=brim_islemleri,default="")
    ucuncu_birim = models.CharField(max_length=100,verbose_name="Ücüncü  Birim",choices=brim_islemleri,default="")
    ikinci_birim_deger = models.CharField(max_length=100,verbose_name="İkinci  Birim",blank=True,null=True)
    ucuncu_birim_deger = models.CharField(max_length=100,verbose_name="Ücüncü  Birim",blank=True,null=True)
    ikinci_birim_islem = models.CharField(max_length=100,verbose_name="İkinci  İşlem",blank=True,null=True)
    ucuncu_birim_islem = models.CharField(max_length=100,verbose_name="Ücüncü  İşlem",blank=True,null=True)
    max_stok_miktari  = models.FloatField(verbose_name="Max Stok Miktarı",blank=True,null=True)
    min_stok_miktari  = models.FloatField(verbose_name="Min Stok Miktarı",blank=True,null=True)
    serbest_stok_birimi  = models.CharField(max_length=200,verbose_name="Serbest Stok Brimi",blank=True,null=True)
    temin_gun  = models.CharField(max_length=200,verbose_name="Temin Gün",blank=True,null=True)
    indirim1 = models.FloatField(verbose_name="İndirim 1",blank=True,null=True)
    indirim2 = models.FloatField(verbose_name="İndirim 2",blank=True,null=True)
    indirim3 = models.FloatField(verbose_name="İndirim 3",blank=True,null=True)
    satis_birimi = models.CharField(max_length=10,verbose_name="Satış Birimi Seç",blank=True,null=True)
    aliss_birimi = models.CharField(max_length=10,verbose_name="Alış Birimi Seç",blank=True,null=True)
    kdv_istisna_kodu_sec = models.ForeignKey(kdv_istisna_kodu,blank=True,null=True,
                                             verbose_name="KDV İstisna Kodu",on_delete=models.SET_NULL)
    kdv_orani = models.FloatField(verbose_name="KDV ORanı",blank=True,null=True)
    tevkifat_orani = models.CharField(max_length=20,verbose_name="Tev")
    lot_kullanimi = models.CharField(max_length=20,verbose_name="Lot Kullan",choices=lot_kullanim_secim,default="")
    serinokullan = models.CharField(max_length=20,verbose_name="Seri No Kullan",choices=lot_kullanim_secim,default="")
    stokmiktari = models.FloatField(verbose_name="Stok Miktarı",blank=True,null=True)
class bankaFisIslemleri(models.Model):
    islem_turu_secim = (
        ("",""),
        ("Virman Fişi","Virman Fişi"),
        ("Döviz Fişi","Döviz Fişi"),
        ("Açılış Fişi","Açılış Fişi"),
        ("Gelir Fişi","Gelir Fişi"),
        ("Gider Fişi","Gider Fişi"),
        ("Faiz Geliri Fişi","Faiz Geliri Fişi"),
        ("Banka Gelir Makbuzu","Banka Gelir Makbuzu"),
        ("Banka Gider Makbuzu","Banka Gider Makbuzu"),
        ("Gönderilen Havale","Gönderilen Havale"),
        ("Gelen Havale","Gelen Havale"),
        ("Cari Maaş Ödemesi (Banka)","Cari Maaş Ödemesi (Banka)"),
        ("Çek/Senet Tescili","Çek/Senet Tescili"),
        ("Çek Ödemesi","Çek Ödemesi"),
    )
    entsecim = (
        ("", ""),
        ("1", "1"),
        ("2", "2"),
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    kendisi_secme =  models.ForeignKey('self',blank=True,null=True,verbose_name="makbuzlar için",related_name='children',on_delete=models.SET_NULL)
    islem_turu = models.CharField(max_length=200, verbose_name="İşlem Türü", default="", choices=islem_turu_secim)
    tarih = models.DateField(verbose_name="İşlem Tarihi", blank=True, null=True)
    saat = models.TimeField(verbose_name="İşlem Saati", blank=True, null=True)
    evrak_no = models.CharField(max_length=100, verbose_name="Evrak Tarihi", blank=True, null=True)
    ent_kodu = models.CharField(max_length=2, verbose_name="Ent Kodu", default="", choices=entsecim)
    birinciislem_sube_bilgisi = models.ForeignKey(sube, blank=True, null=True, verbose_name="Şube",
                                                   on_delete=models.SET_NULL,
                                                   related_name='birinciislem_kasa_fis_islemleri_set_banka')
    ozelkod1 = models.CharField(max_length=200, verbose_name="Özel Kod", blank=True, null=True)
    ozelkod2 = models.CharField(max_length=200, verbose_name="Özel Kod 2", blank=True, null=True)
    birinci_departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    birinci_banka_bilgisi = models.ForeignKey(banka, verbose_name="Birinci Kasa Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='birinci_banka_fis_islemleri_set')
    birinci_banka_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    gelir_bilgisi = models.ForeignKey(Gelirler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                      on_delete=models.SET_NULL, related_name='gelir_banka_fis_islemleri_set')
    gider_bilgisi = models.ForeignKey(Giderler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                      on_delete=models.SET_NULL, related_name='gider_banka_fis_islemleri_set')
    gelir_muh_kodu = models.CharField(max_length=200, verbose_name="Gelir Muhtasar Kodu", blank=True, null=True)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    aciklama = models.TextField(verbose_name="İşlem Açıklama ", blank=True, null=True)
    islemi_yapan = models.CharField(max_length=250, verbose_name="İşlemi Yapan", blank=True, null=True)
    tutar = models.FloatField(verbose_name="İşlem Tutarı", blank=True, null=True)
    tutar_tl = models.FloatField(verbose_name="İşlem Tutarı (TL)", blank=True, null=True)
    doviz_tutar = models.FloatField(verbose_name="İşlem Tutarı döviz", blank=True, null=True)
    ikinci_islem_sube_bilgisi = models.ForeignKey(sube, blank=True, null=True, verbose_name="Şube",
                                                  on_delete=models.SET_NULL,
                                                  related_name='ikinciislem_banka_fis_islemleri_set')
    ikinci_gelir_bilgisi = models.ForeignKey(Gelirler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                             on_delete=models.SET_NULL,
                                             related_name='ikinci_gelir_banka_fis_islemleri_set')
    ikinci_gider_bilgisi = models.ForeignKey(Giderler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                             on_delete=models.SET_NULL,
                                             related_name='ikinci_gider_banka_fis_islemleri_set')
    gider_muh_kodu = models.CharField(max_length=200, verbose_name="Gİder Muhtasar Kodu", blank=True, null=True)
    ikinci_banka_bilgisi = models.ForeignKey(banka, verbose_name="İkinci Kasa Bilgisi", blank=True, null=True,
                                            on_delete=models.SET_NULL, related_name='ikinci_banka_fis_islemleri_set')
    ikinci_departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    ikinci_banka_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    islem_durumu = models.BooleanField(default=False, verbose_name="İşlem Tamamlandıysa tikli olacak")
    satici = models.CharField(max_length=200, verbose_name="SAtıcı", blank=True, null=True)
    kampkodu = models.CharField(max_length=200, verbose_name="Kamp Kodu", blank=True, null=True)
    gunluk_kur = models.CharField(max_length=200, verbose_name="Günlük Kur", blank=True, null=True)
    uygun_kur = models.CharField(max_length=200, verbose_name="Uygun Kur", blank=True, null=True)
    alacakbilgisi = models.CharField(max_length=200, verbose_name="alacakbilgisi", blank=True, null=True)
    gider_durumu = models.CharField(max_length=100,verbose_name="Gider Durumu",blank=True,null=True)
    gideryuzdesi= models.FloatField(verbose_name="Gider yüzdesi",blank=True,null=True)
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    banka_bilgisi = models.ForeignKey(Kasa,blank=True,null=True,verbose_name="Kasa Bilgisi",on_delete=models.SET_NULL)
    kasa_banka_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False)
    islem_sonucu_bakiye_birinci_banka = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_ikinci_banka = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_cari = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_kasa = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)



class cari_fisleri(models.Model):
    islem_turu_secim = (
        ("",""),
        ("Borç Dekontu","Borç Dekontu"),
        ("Alacak Dekontu","Alacak Dekontu"),
        ("Ödeme Fişi","Ödeme Fişi"),
        ("Tahsilat Fişi","Tahsilat Fişi"),
        ("Virman Fişi","Virman Fişi"),
        ("Açılış Fişi","Açılış Fişi"),
        ("Maaş Tahakkuku","Maaş Tahakkuku"),
        ("Maaş Ödemesi","Maaş Ödemesi"),
        ("Toplu Dekont","Toplu Dekont"),
        ("Cari Ödeme Makbuzu","Cari Ödeme Makbuzu"),
        ("Cari Tahsilat Makbuzu","Cari Tahsilat Makbuzu"),
        ("Borç Makbuzu","Borç Makbuzu"),
        ("Alacak Makbuzu","Alacak Makbuzu"),
        ("Tahsilat Makbuzu","Tahsilat Makbuzu"),
        ("Ödeme Planı Tahsilatı","Ödeme Planı Tahsilatı"),
        ("Bordrodan Puantaj Al","Bordrodan Puantaj Al")
    )
    entsecim = (
        ("", ""),
        ("1", "1"),
        ("2", "2"),
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "Euro"),
        ("Dolar", "Dolar")
    )
    kendisi_secme =  models.ForeignKey('self',blank=True,null=True,verbose_name="makbuzlar için",related_name='children',on_delete=models.SET_NULL)
    islem_turu = models.CharField(max_length=200, verbose_name="İşlem Türü", default="", choices=islem_turu_secim)
    tarih = models.DateField(verbose_name="İşlem Tarihi", blank=True, null=True)
    saat = models.TimeField(verbose_name="İşlem Saati", blank=True, null=True)
    evrak_no = models.CharField(max_length=100, verbose_name="Evrak Tarihi", blank=True, null=True)
    ent_kodu = models.CharField(max_length=2, verbose_name="Ent Kodu", default="", choices=entsecim)
    vade_tarih = models.DateField(verbose_name="Vade Tarihi", blank=True, null=True)
    vade_gunu =  models.CharField(max_length=100, verbose_name="Vade Günü", blank=True, null=True)
    birinciislem_sube_bilgisi = models.ForeignKey(sube, blank=True, null=True, verbose_name="Şube",
                                                   on_delete=models.SET_NULL,
                                                   related_name='birinciislem_cari_fis_islemleri_set_banka')
    ozelkod1 = models.CharField(max_length=200, verbose_name="Özel Kod", blank=True, null=True)
    ozelkod2 = models.CharField(max_length=200, verbose_name="Özel Kod 2", blank=True, null=True)
    birinci_departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    birinci_cari_bilgisi = models.ForeignKey(cari_kartlar, verbose_name="Birinci Cari Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='birinci_cari_fis_islemleri_set')
    birinci_cari_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    gelir_bilgisi = models.ForeignKey(Gelirler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                      on_delete=models.SET_NULL, related_name='gelir_cari_fis_islemleri_set')
    gider_bilgisi = models.ForeignKey(Giderler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                      on_delete=models.SET_NULL, related_name='gider_cari_fis_islemleri_set')
    gelir_muh_kodu = models.CharField(max_length=200, verbose_name="Gelir Muhtasar Kodu", blank=True, null=True)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    aciklama = models.TextField(verbose_name="İşlem Açıklama ", blank=True, null=True)
    islemi_yapan = models.CharField(max_length=250, verbose_name="İşlemi Yapan", blank=True, null=True)
    tutar = models.FloatField(verbose_name="İşlem Tutarı", blank=True, null=True)
    tutar_tl = models.FloatField(verbose_name="İşlem Tutarı (TL)", blank=True, null=True)
    doviz_tutar = models.FloatField(verbose_name="İşlem Tutarı döviz", blank=True, null=True)
    ikinci_islem_sube_bilgisi = models.ForeignKey(sube, blank=True, null=True, verbose_name="Şube",
                                                  on_delete=models.SET_NULL,
                                                  related_name='ikinciislem_cari_fis_islemleri_set')
    ikinci_gelir_bilgisi = models.ForeignKey(Gelirler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                             on_delete=models.SET_NULL,
                                             related_name='ikinci_gelir_cari_fis_islemleri_set')
    ikinci_gider_bilgisi = models.ForeignKey(Giderler, blank=True, null=True, verbose_name="Gelir Bilgisi",
                                             on_delete=models.SET_NULL,
                                             related_name='ikinci_gider_cari_fis_islemleri_set')
    gider_muh_kodu = models.CharField(max_length=200, verbose_name="Gİder Muhtasar Kodu", blank=True, null=True)
    ikinci_cari_bilgisi = models.ForeignKey(cari_kartlar, verbose_name="İkinci Kasa Bilgisi", blank=True, null=True,
                                            on_delete=models.SET_NULL, related_name='ikinci_cari_fis_islemleri_set')
    ikinci_departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    ikinci_cari_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    islem_durumu = models.BooleanField(default=False, verbose_name="İşlem Tamamlandıysa tikli olacak")
    satici = models.CharField(max_length=200, verbose_name="SAtıcı", blank=True, null=True)
    kampkodu = models.CharField(max_length=200, verbose_name="Kamp Kodu", blank=True, null=True)
    gunluk_kur = models.CharField(max_length=200, verbose_name="Günlük Kur", blank=True, null=True)
    uygun_kur = models.CharField(max_length=200, verbose_name="Uygun Kur", blank=True, null=True)
    alacakbilgisi = models.CharField(max_length=200, verbose_name="alacakbilgisi", blank=True, null=True)
    gider_durumu = models.CharField(max_length=100,verbose_name="Gider Durumu",blank=True,null=True)
    gideryuzdesi= models.FloatField(verbose_name="Gider yüzdesi",blank=True,null=True)
    bankasecme = models.ForeignKey(banka,blank=True,null=True,verbose_name="Banka Bilgisi",on_delete=models.SET_NULL)
    banka_bilgisi = models.ForeignKey(Kasa,blank=True,null=True,verbose_name="Kasa Bilgisi",on_delete=models.SET_NULL)
    kasa_banka_muh_kodu = models.CharField(max_length=200, verbose_name="Kasa Muhtasar Kodu", blank=True, null=True)
    
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False)
    islem_sonucu_bakiye_birinci_cari = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_ikinci_cari = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_banka = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)
    islem_sonucu_bakiye_kasa = models.FloatField(verbose_name="İşlem Sonucu Bakiye",blank=True,null=True)



class stok_alis_satis(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_karti_bilgisi_stokalis_satis_set')
    satis_fiyati_1_tl = models.FloatField(verbose_name="Satış fiyatı tl 1",blank=True,null=True)
    satis_fiyati_2_tl = models.FloatField(verbose_name="Satış fiyatı tl 2",blank=True,null=True)
    satis_fiyati_3_tl = models.FloatField(verbose_name="Satış fiyatı tl 3",blank=True,null=True)
    satis_fiyati_4_tl = models.FloatField(verbose_name="Satış fiyatı tl 4",blank=True,null=True)
    satis_fiyati_5_tl = models.FloatField(verbose_name="Satış fiyatı tl 5",blank=True,null=True)
    satis_fiyati_6_tl = models.FloatField(verbose_name="Satış fiyatı tl 6",blank=True,null=True)
    satis_fiyati_7_tl = models.FloatField(verbose_name="Satış fiyatı tl 7",blank=True,null=True)
    satis_fiyati_8_tl = models.FloatField(verbose_name="Satış fiyatı tl 8",blank=True,null=True)
    satis_fiyati_9_tl = models.FloatField(verbose_name="Satış fiyatı tl 9",blank=True,null=True)
    satis_fiyati_10_tl = models.FloatField(verbose_name="Satış fiyatı tl 10",blank=True,null=True)
    satis_fiyati_1_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 1",blank=True,null=True)
    satis_fiyati_2_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 2",blank=True,null=True)
    satis_fiyati_3_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 3",blank=True,null=True)
    satis_fiyati_4_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 4",blank=True,null=True)
    satis_fiyati_5_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 5",blank=True,null=True)
    satis_fiyati_6_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 6",blank=True,null=True)
    satis_fiyati_7_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 7",blank=True,null=True)
    satis_fiyati_8_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 8",blank=True,null=True)
    satis_fiyati_9_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 9",blank=True,null=True)
    satis_fiyati_10_dvz = models.FloatField(verbose_name="Satış fiyatı Döviz 10",blank=True,null=True)
    aktif_satis_fiyati = models.CharField(max_length=20,verbose_name="Aktif Satış Fiyatı",blank=True,null=True)
    satis_dovizcinsi = models.CharField(max_length=20,verbose_name="Secilen Döviz Seçeneği",blank=True,null=True)
    birim_secenegi = models.CharField(max_length=20,verbose_name="Secilen Birim Seçeneği",blank=True,null=True)
    alis_fiyati_1_tl = models.FloatField(verbose_name="Satış fiyatı tl 1",blank=True,null=True)
    alis_fiyati_2_tl = models.FloatField(verbose_name="Satış fiyatı tl 2",blank=True,null=True)
    alis_fiyati_3_tl = models.FloatField(verbose_name="Satış fiyatı tl 3",blank=True,null=True)
    alis_fiyati_4_tl = models.FloatField(verbose_name="Satış fiyatı tl 4",blank=True,null=True)
    alis_fiyati_5_tl = models.FloatField(verbose_name="Satış fiyatı tl 5",blank=True,null=True)
    alis_fiyati_1_dvz = models.FloatField(verbose_name="Satış fiyatı dvz 1",blank=True,null=True)
    alis_fiyati_2_dvz = models.FloatField(verbose_name="Satış fiyatı dvz 2",blank=True,null=True)
    alis_fiyati_3_dvz = models.FloatField(verbose_name="Satış fiyatı dvz 3",blank=True,null=True)
    alis_fiyati_4_dvz = models.FloatField(verbose_name="Satış fiyatı dvz 4",blank=True,null=True)
    alis_fiyati_5_dvz = models.FloatField(verbose_name="Satış fiyatı dvz 5",blank=True,null=True)
    aktif_alis_fiyati = models.CharField(max_length=20,verbose_name="Aktif Alış Fiyatı",blank=True,null=True)
    alis_dovizcinsi = models.CharField(max_length=20,verbose_name="Secilen Döviz Seçeneği",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True,null=True)
    maliyet_yontemi = models.CharField(max_length=200,verbose_name="Maliyet Yöntemi",blank=True,null=True)
    satis_kar_evrak = models.CharField(max_length=200,verbose_name="Satış Kar Evrağı",blank=True,null=True)
    satis_kar_yuzdesi = models.FloatField(verbose_name="Satış Kar Yüzdesi",blank=True,null=True)
class stok_kodlari(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_karti_bilgisi_kodlar_set')
    ozel_kod_1 = models.CharField(verbose_name="Özel Kod 1",max_length=100,blank=True,null=True)
    ozel_kod_2 = models.CharField(verbose_name="Özel Kod 2",max_length=100,blank=True,null=True)    
    grup_kod_1 = models.CharField(verbose_name="Grup Kod 1",max_length=100,blank=True,null=True)
    grup_kod_2 = models.CharField(verbose_name="Grup Kod 2",max_length=100,blank=True,null=True)
    grup_kod_3 = models.CharField(verbose_name="Grup Kod 3",max_length=100,blank=True,null=True)
    gtipno = models.CharField(verbose_name="Gtip No",max_length=100,blank=True,null=True)
    kalitekodu = models.CharField(verbose_name="Kalite Kodu",max_length=100,blank=True,null=True)
    barkod = models.CharField(verbose_name="Barkod",max_length=100,blank=True,null=True)
    brimno = models.CharField(verbose_name="Brim No",max_length=100,blank=True,null=True)
    alternatifstokkodu = models.CharField(verbose_name="alternatif stok kodu",max_length=100,blank=True,null=True)
    alternatifstokadi = models.CharField(verbose_name="alternatif stok adı",max_length=200,blank=True,null=True)
    alternatifstokkodu2 = models.CharField(verbose_name="alternatif stok kodu 2",max_length=100,blank=True,null=True)
    alternatifstokadi2 = models.CharField(verbose_name="alternatif stok adı 2",max_length=200,blank=True,null=True)
    alternatifstokkodu3 = models.CharField(verbose_name="alternatif stok kodu 3",max_length=100,blank=True,null=True)
    alternatifstokadi3 = models.CharField(verbose_name="alternatif stok adı 3",max_length=200,blank=True,null=True)
    yazarkasadepartman = models.CharField(verbose_name="yazarkasadepartmani",max_length=200,blank=True,null=True)
    tazeurunkodu = models.CharField(verbose_name="tazeurunkodu",max_length=200,blank=True,null=True)
    plukodu = models.CharField(verbose_name="plu kodu",max_length=100,blank=True,null=True)
    reyon = models.CharField(verbose_name="reyon",max_length=200,blank=True,null=True)
    raf1 = models.CharField(verbose_name="raf 1",max_length=100,blank=True,null=True)
    raf2 = models.CharField(verbose_name="raf 2 ",max_length=200,blank=True,null=True)
    raf3 = models.CharField(verbose_name="raf 3 ",max_length=200,blank=True,null=True)

class stok_detaylari(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_karti_bilgisi_detaylari_set')
    parametreadi1 = models.CharField(verbose_name="Paremetre Adı 1",max_length=100,blank=True,null=True)
    paremetredegeri1 = models.CharField(verbose_name="Parametre Değeri 1",max_length=200,blank=True,null=True)
    parametreadi2 = models.CharField(verbose_name="Paremetre Adı 2",max_length=100,blank=True,null=True)
    paremetredegeri2 = models.CharField(verbose_name="Parametre Değeri 2",max_length=200,blank=True,null=True)
    barkod = models.CharField(verbose_name="Barkod",max_length=200,blank=True,null=True)
    kalite = models.CharField(verbose_name="Kalite",max_length=200,blank=True,null=True)
    detayozellikadi = models.CharField(verbose_name="Detaylı özellik adi",max_length=200,blank=True,null=True)
    varyant = models.CharField(verbose_name="Varyant",max_length=200,blank=True,null=True)
    varyantkodu = models.CharField(verbose_name="Varyant Kodu",max_length=200,blank=True,null=True)
    secili = models.CharField(verbose_name="secili ? (E)",max_length=200,blank=True,null=True)
    varyantkodu2 = models.CharField(verbose_name="Varyant Kodu2",max_length=200,blank=True,null=True)
    ozellik1 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik2 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik3 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik4 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik5 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    ozellik6 = models.CharField(verbose_name="ozellil6",max_length=200,blank=True,null=True)
    ozellik7 = models.CharField(verbose_name="ozellil7",max_length=200,blank=True,null=True)
    ozellik8 = models.CharField(verbose_name="ozellil8",max_length=200,blank=True,null=True)
    ozellik9 = models.CharField(verbose_name="ozellil9",max_length=200,blank=True,null=True)
    ozellik10 = models.CharField(verbose_name="ozelli10",max_length=200,blank=True,null=True)
    ozellik11 = models.CharField(verbose_name="ozellil11",max_length=200,blank=True,null=True)
    ozellik12 = models.CharField(verbose_name="ozellil12",max_length=200,blank=True,null=True)
    ozellik13 = models.CharField(verbose_name="ozellil13",max_length=200,blank=True,null=True)
    ozellik14 = models.CharField(verbose_name="ozellil14",max_length=200,blank=True,null=True)
    ozellik15 = models.CharField(verbose_name="ozellil15",max_length=200,blank=True,null=True)
    ozellik16 = models.CharField(verbose_name="ozellil16",max_length=200,blank=True,null=True)
    ozellik17 = models.CharField(verbose_name="ozellil17",max_length=200,blank=True,null=True)
    ozellik18 = models.CharField(verbose_name="ozellil18",max_length=200,blank=True,null=True)
    ozellik19 = models.CharField(verbose_name="ozellil19",max_length=200,blank=True,null=True)
    ozellik20 = models.CharField(verbose_name="ozellil20",max_length=200,blank=True,null=True)
    ozellik21 = models.CharField(verbose_name="ozellil21",max_length=200,blank=True,null=True)
    ozellik22 = models.CharField(verbose_name="ozellil22",max_length=200,blank=True,null=True)
    ozellik23 = models.CharField(verbose_name="ozellil23",max_length=200,blank=True,null=True)
    ozellik24 = models.CharField(verbose_name="ozellil24",max_length=200,blank=True,null=True)
    ozellik25 = models.CharField(verbose_name="ozellil25",max_length=200,blank=True,null=True)
    ozellik26 = models.CharField(verbose_name="ozellil26",max_length=200,blank=True,null=True)
    ozellik27 = models.CharField(verbose_name="ozellil27",max_length=200,blank=True,null=True)
    ozellik28 = models.CharField(verbose_name="ozellil28",max_length=200,blank=True,null=True)
    ozellik29 = models.CharField(verbose_name="ozellil29",max_length=200,blank=True,null=True)
    ozellik30 = models.CharField(verbose_name="ozellil30",max_length=200,blank=True,null=True)

class stok_recetesi(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_recetesi_karti_set')
    brim_en = models.FloatField(verbose_name="Brim En",blank=True,null=True)
    brim_boy = models.FloatField(verbose_name="Brim Boy",blank=True,null=True)
    brim_kalinlik = models.FloatField(verbose_name="Brim Kalınlık",blank=True,null=True)
    brim_bolunme_katsayisi = models.FloatField(verbose_name="Brim Bölünme Katsayısı",blank=True,null=True)
    brim_cevrilecek_brim = models.CharField(max_length=100,verbose_name="Brim Çevrilecek Brim",blank=True,null=True)
    brim_islem_sonucu = models.FloatField(verbose_name="Brim İşlem Sonucu",blank=True,null=True)
    stok_brimi = models.CharField(verbose_name="Stok Brimi",max_length=200,blank=True,null=True)
    ozgul_agirlik = models.CharField(verbose_name="Özgül Ağırlık",max_length=200,blank=True,null=True)
    islem = models.CharField(verbose_name="İşlem",max_length=200,blank=True,null=True)
    recete_miktari = models.CharField(verbose_name="Reçete Miktarı",max_length=200,blank=True,null=True)
    recete_brim_maliyeti = models.CharField(verbose_name="Reçete Brim Maliyeti",max_length=200,blank=True,null=True)
    f_r = models.BooleanField(verbose_name="FR",default=False)
    stok_kodu = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_stok_kodu_set')
    brim_bilgisi = models.CharField(verbose_name="Brim Bilgisi",max_length=200,blank=True,null=True)
    tur = models.CharField(verbose_name="Tür",max_length=200,blank=True,null=True)
    miktar = models.FloatField(verbose_name="Miktarı",blank=True,null=True)
    doviz_cinsi = models.CharField(verbose_name="Döviz Cinsi",max_length=200,blank=True,null=True)
    brim_fiyati_tl = models.FloatField(verbose_name="Birim Fiyatı TL",blank=True,null=True)
    birim_fiyati_dvz = models.FloatField(verbose_name="Birim Fiyati Döviz",blank=True,null=True)
    fire_yuzdesi = models.FloatField(verbose_name="Fire Yüzdesi",blank=True,null=True)
    fire_miktari = models.FloatField(verbose_name="Fire Miktarı",blank=True,null=True)
    alternatif_stok_kodu = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_alternatif_stok_kodu_set')
    gider_yuzdesi = models.FloatField(verbose_name="Gider Yüzdesi",blank=True,null=True)
    son_guncelleme_tarihi = models.DateField(verbose_name="Son Güncelleme Tarihi",blank=True,null=True)
    satis_aninda_miktar_kadar_uretim_yap = models.BooleanField(default=False,verbose_name="Satış Anında Miktar Kadar Üretim Yap")
    uretimden_giriste_sarf_kaydi_yap = models.BooleanField(default=False,verbose_name="Satış Anında Miktar Kadar Üretim Yap")
    sarf_kaydi_hesaplama_yontemi = models.CharField(verbose_name="Sarf Kaydı Hesaplama Yöntemi",max_length=200,blank=True,null=True)

class stok_muhasabe_kodlari(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_muhasebekodlari_set')
    grup_muh_kodu = models.CharField(max_length=100,verbose_name="Grup Muh Kodu",blank=True,null=True)
    uretime_sevk_kodu= models.CharField(max_length=100,verbose_name="Üretime Sevk H. Kodu",blank=True,null=True)
    uretime_sarf_h_kodu= models.CharField(max_length=100,verbose_name="Üretim Sarf H. Kodu",blank=True,null=True)
    uretime_hesap_kodu= models.CharField(max_length=100,verbose_name="Üretim Hesap Kodu",blank=True,null=True)
    depo_s_fazlasi_h_kodu= models.CharField(max_length=100,verbose_name="Depo S. Fazlası H. Kodu",blank=True,null=True)
    depo_s_eksikligi_h_kodu= models.CharField(max_length=100,verbose_name="Depo S. Eksiği H. Kodu",blank=True,null=True)
    sarf_hesap_kodu= models.CharField(max_length=100,verbose_name="Sarf Hesap Kodu",blank=True,null=True)
    fire_hesap_kodu= models.CharField(max_length=100,verbose_name="Fire Hesap Kodu",blank=True,null=True)

class stok_muhasebe_kodlari_evraklar(models.Model):
    evrak_bagli_birim = models.ForeignKey(stok_muhasabe_kodlari, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='sevrak_bagli_birim_set')
    evrak_turu = models.CharField(max_length=200,verbose_name="Evrak Türü",blank=True,null=True)
    kdv_orani = models.CharField(max_length=20,verbose_name="KDV Oranı",blank=True,null=True)
    tevkifat_orani = models.CharField(max_length=20,verbose_name="Tevkifat Oranı",blank=True,null=True)
    stok_hesap_kodu = models.CharField(max_length=100,verbose_name="Stok Hesap Kodu",blank=True,null=True)
    kdv_hesap_kodu = models.CharField(max_length=100,verbose_name="KDV Hesap Kodu",blank=True,null=True)
    tevkifat_hesap_kodu1 = models.CharField(max_length=100,verbose_name="Tevkifat Hesap Kodu 1",blank=True,null=True)
    tevkifat_hesap_kodu2 = models.CharField(max_length=100,verbose_name="Tevkifat Hesap Kodu 2",blank=True,null=True)
    otv_hesap_kodu = models.CharField(max_length=100,verbose_name="ÖTV Hesap Kodu",blank=True,null=True)
    otv_tescilb_hesap_kodu = models.CharField(max_length=100,verbose_name="ÖTV (Tescil B) Hesap Kodu",blank=True,null=True)


class stok_iliskili_gider_gelir(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_iliskili_gider_gelir_set')
    gider = models.ForeignKey(Giderler,verbose_name="Gider",on_delete=models.SET_NULL,blank=True,null=True)
    o_ekle_gider = models.CharField(max_length=200,verbose_name="Gider Ekle",blank=True,null=True)
    gider_orani = models.FloatField(verbose_name="Gider Oranı",blank=True,null=True)
    gelir = models.ForeignKey(Gelirler,verbose_name="Gelir",on_delete=models.SET_NULL,blank=True,null=True)
    o_ekle_gelir = models.CharField(max_length=200,verbose_name="Gider Ekle",blank=True,null=True)
    gelir_orani = models.FloatField(verbose_name="Gider Oranı",blank=True,null=True)
    

class stok_diger_kismi_otv(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_diger_kismi_otv_set')
    otv_orani = models.FloatField(verbose_name="ÖTV Oranı",blank=True,null=True)
    otv_brim_fiyati = models.FloatField(verbose_name="ÖTV Brim Fiyatı",blank=True,null=True)
    otv_brim_no = models.FloatField(verbose_name="ÖTV Brim No",blank=True,null=True)
    otv_tahsil_orani = models.FloatField(verbose_name="ÖTV Tahsil Oranı",blank=True,null=True)
    otv_tecil_orani = models.FloatField(verbose_name="ÖTV Tecil Oranı",blank=True,null=True)
    mera_fonu_orani = models.FloatField(verbose_name="Mera Fonu Oranı",blank=True,null=True)
    fire_orani = models.FloatField(verbose_name="Fire Oranı",blank=True,null=True)

class stok_diger_kismi_agirliklar(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_diger_kismi_agirliklar_set')
    net = models.FloatField(verbose_name="NET",blank=True,null=True)
    brut = models.FloatField(verbose_name="Brüt",blank=True,null=True)
    dara = models.FloatField(verbose_name="Dara",blank=True,null=True)
    p_miktari = models.FloatField(verbose_name="P miktari",blank=True,null=True)
    p_aciklamasi = models.TextField(verbose_name="P Açıklması",blank=True,null=True)
    

class stok_diger_birim_durumu(models.Model):
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL, related_name='stok_diger_birim_durumu_set')
    birim = models.CharField(max_length=10,verbose_name="Birim No",blank=True,null=True)
    en = models.FloatField(verbose_name="En Ölçüsü",blank=True,null=True)
    en_birimi = models.CharField(max_length=20,verbose_name="En Birimi")
    boy = models.FloatField(verbose_name="Boy Ölçüsü",blank=True,null=True)
    boy_birimi = models.CharField(max_length=20,verbose_name="Boy Birimi")
    yukseklik = models.FloatField(verbose_name="Yükseklik Ölçüsü",blank=True,null=True)
    yukseklik_birimi = models.CharField(max_length=20,verbose_name="Boy Birimi")   
    ebat_birimi = models.CharField(max_length=20,verbose_name="Ebat Birimi")
    hacim = models.FloatField(verbose_name="Hacim Ölçüsü",blank=True,null=True)

class siparisislem_durumlari(models.Model):
    siparis_turu_secim = (
        ("",""),
        ("Alınan Sipariş","Alınan Sipariş"),
        ("Verilen Sipariş","Verilen Sipariş"),
        ("Alınan Teklif","Alınan Teklif"),
        ("Verilen Teklif","Verilen Teklif")
    )
    ent_kodu_secim = (
        ("1","1"),
        ("2","2")
    )
    kdv_durumu_secim = (
        ("Hariç","Hariç"),
        ("Dahil","Dahil")
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "£"),
        ("Dolar", "$")
    )
    siparis_tur = models.CharField(max_length=200,verbose_name="Sipariş Türü",choices=siparis_turu_secim,default="")
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    depo = models.CharField(max_length=200,verbose_name="Depo Adı",blank=True,null=True)
    ent_kodu = models.CharField(max_length=20,verbose_name="Entegrasyon Kodu",choices=ent_kodu_secim,default="1")
    kdv_durumu = models.CharField(max_length=200,verbose_name="KDV Durumu",choices=kdv_durumu_secim,default="Hariç")
    siparis_no = models.CharField(max_length=200,verbose_name="Sipariş No",blank=True,null=True)
    tarih = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    teslim_sekli = models.CharField(max_length=200, verbose_name="Teslim Şekli", blank=True, null=True)
    satici = models.CharField(max_length=200, verbose_name="SAtıcı", blank=True, null=True)
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    sube_kodu = models.ForeignKey(sube,blank=True,null=True,verbose_name="Şube Bilgisi",on_delete=models.SET_NULL)
    ozel_kod1 = models.CharField(verbose_name="Özel Kod",blank=True,null=True,max_length=200)
    ozel_kod2 = models.CharField(verbose_name="Özel Kod 2",blank=True,null=True,max_length=200)
    departman = models.CharField(verbose_name="departman",blank=True,null=True,max_length=200)
    onay = models.BooleanField(verbose_name="Sipariş Onaylandı",default=False)
    gunluk_kur = models.CharField(max_length=200, verbose_name="Günlük Kur", blank=True, null=True)
    uygun_kur = models.CharField(max_length=200, verbose_name="Uygun Kur", blank=True, null=True)
    irsaliyeye_aktar = models.BooleanField(verbose_name="irsaliyey Aktarıldı" , default=False)
    faturaya_aktar = models.BooleanField(verbose_name="Faturaya Aktarıldı" , default=False)
    tutar_doviz = models.FloatField(verbose_name="Tutar Döviz",blank=True,null=True)
    tutar_tl = models.FloatField(verbose_name="Tutar TL",blank=True,null=True)
    aktif_pasif = models.BooleanField(verbose_name="Aktif Pasif Olayı", default=False)
    otv_tutari = models.FloatField(verbose_name="Ötv Tutarı TL",blank=True,null=True)
    kdv_tutari = models.FloatField(verbose_name="KDV Tutarı TL",blank=True,null=True)
    indirim_tutari = models.FloatField(verbose_name="İndirim Tutarı TL",blank=True,null=True)
    genel_tutari = models.FloatField(verbose_name="Genel Tutarı TL",blank=True,null=True)
    iptaledildi = models.BooleanField(verbose_name="İptal Edildi" , default=False)
    silinme_bilgisi = models.BooleanField(verbose_name="Sİpariş Silme Durumu",default=False)
    irsaliye_durumu = models.CharField(max_length=200,verbose_name="İrsaliye Teslim Durumu",blank=True,null=True)
class siparis_olustur(models.Model):    
    grup_kodu = models.ForeignKey(siparisislem_durumlari,blank=True,null=True,on_delete=models.SET_NULL,verbose_name="Grup Kodu")
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    tip = models.CharField(max_length=200,verbose_name="tip",blank=True,null=True)
    teslim_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    teslim_sekli = models.CharField(max_length=200, verbose_name="Teslim Şekli", blank=True, null=True)
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL)
    miktar = models.FloatField(verbose_name="Miktar" ,blank=True,null=True,default=1)
    kalan_miktar = models.FloatField(verbose_name="Miktar" ,blank=True,null=True,default=1)
    birim = models.CharField(max_length=200,verbose_name="Birim",blank=True,null=True)
    birim_fiyat_tl = models.FloatField(verbose_name="Birim Fiyatı TL" ,blank=True,null=True,default=1)
    birim_fiyat_dvz = models.FloatField(verbose_name="Birim Fiyatı Döviz" ,blank=True,null=True,default=1)
    indirim_yuzdesi = models.FloatField(verbose_name="İndirim Yüzdesi" ,blank=True,null=True,default=0)
    indirim_tutari_tl = models.FloatField(verbose_name="İndirim Tutarı TL" ,blank=True,null=True,default=0)
    kdv_yuzdesi = models.FloatField(verbose_name="KDV Yüzdesi" ,blank=True,null=True,default=0)
    kdv_tutari_tl = models.FloatField(verbose_name="KDV Tutarı TL" ,blank=True,null=True,default=0)
    otv_yuzdesi = models.FloatField(verbose_name="ÖTV Yüzdesi" ,blank=True,null=True,default=0)
    otv_tutari_tl = models.FloatField(verbose_name="ÖTV Tutarı TL" ,blank=True,null=True,default=0)
    stoktutari = models.FloatField(verbose_name="Stok Tutarı TL" ,blank=True,null=True,default=0)
    durumu = models.CharField(max_length=200,verbose_name="Durum",blank=True,null=True)
    indirim1 = models.FloatField(verbose_name="İndirim 1",blank=True,null=True)
    indirim2 = models.FloatField(verbose_name="İndirim 2",blank=True,null=True)
    indirim3 = models.FloatField(verbose_name="İndirim 3",blank=True,null=True)
    ozelkod1 = models.CharField(max_length=200, verbose_name="Özel Kod", blank=True, null=True)
    ozelkod2 = models.CharField(max_length=200, verbose_name="Özel Kod 2", blank=True, null=True)
    departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    satir_aciklamasi = models.CharField(max_length=200, verbose_name="Satır Açıklaması", blank=True, null=True)
    serino = models.CharField(verbose_name="Seri No",max_length=100,blank=True,null=True)
    s_brim = models.CharField(verbose_name="Serbest Brim",max_length=100,blank=True,null=True)
    s_miktar = models.FloatField(verbose_name="Serbest Miktar" ,blank=True,null=True,default=1)
    alternatifstokkodu = models.CharField(verbose_name="alternatif stok kodu",max_length=100,blank=True,null=True)
    alternatifstokadi = models.CharField(verbose_name="alternatif stok adı",max_length=200,blank=True,null=True)
    kalite = models.CharField(verbose_name="Kalite",max_length=200,blank=True,null=True)
    ozellik1 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik2 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik3 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik4 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik5 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    ana_miktar = models.FloatField(verbose_name="Ana Miktar" ,blank=True,null=True,default=1)
    ana_birim_fiyat_tl = models.FloatField(verbose_name="Ana Birim Fiyatı TL" ,blank=True,null=True,default=1)
    ana_birim_fiyat_dvz = models.FloatField(verbose_name="Ana Birim Fiyatı Döviz" ,blank=True,null=True,default=1)
    parti_kodu = models.CharField(max_length=200,verbose_name="Parti Kodu",blank=True,null=True)
    son_kullanim_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)

#irsaliye
class irsaliyeislem_durumlari(models.Model):
    siparis_turu_secim = (
        ("",""),
        ("Satış İrsaliyesi","Satış İrsaliyesi"),
        ("Satış İade İrsaliyesi","Satış İade İrsaliyesi"),
        ("Alış İrsaliyesi","Alış İrsaliyesi"),
        ("Alış İade İrsaliyesi","Alış İade İrsaliyesi"),
        ("Konsinye Çıkış İrsaliyesi","Konsinye Çıkış İrsaliyesi"),
        ("Konsinye Çıkış İade İrsaliyesi","Konsinye Çıkış İade İrsaliyesi"),
        ("Konsinye Giriş İrsaliyesi","Konsinye Giriş İrsaliyesi"),
        ("Konsinye Giriş İade İrsaliyesi","Konsinye Giriş İade İrsaliyesi"),
        ("Depo Sayım Fazlası","Depo Sayım Fazlası"),
        ("Depo Sayım Eksikliği","Depo Sayım Eksikliği"),
        ("Depo Transfer Fişi","Depo Transfer Fişi"),
        ("Üretimden Giriş Fişi","Üretimden Giriş Fişi"),
        ("Üretim Sevk Fişi","Üretim Sevk Fişi"),
        ("Üretim Sevk iade Fişi","Üretim Sevk iade Fişi"),
        ("Fire Fişi","Fire Fişi"),
        ("Sarf Fişi","Sarf Fişi"),
        ("Açılış Fişi","Açılış Fişi"),
        ("Stok (Depo) Sayım Fişleri","Stok (Depo) Sayım Fişleri"),
    )
    ent_kodu_secim = (
        ("1","1"),
        ("2","2")
    )
    kdv_durumu_secim = (
        ("Hariç","Hariç"),
        ("Dahil","Dahil")
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "£"),
        ("Dolar", "$")
    )
    siparis_tur = models.CharField(max_length=200,verbose_name="Sipariş Türü",choices=siparis_turu_secim,default="")
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    depo = models.CharField(max_length=200,verbose_name="Depo Adı",blank=True,null=True)
    ent_kodu = models.CharField(max_length=20,verbose_name="Entegrasyon Kodu",choices=ent_kodu_secim,default="1")
    kdv_durumu = models.CharField(max_length=200,verbose_name="KDV Durumu",choices=kdv_durumu_secim,default="Hariç")
    siparis_no = models.CharField(max_length=200,verbose_name="Sipariş No",blank=True,null=True)
    tarih = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    satici = models.CharField(max_length=200, verbose_name="SAtıcı", blank=True, null=True)
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    sube_kodu = models.ForeignKey(sube,blank=True,null=True,verbose_name="Şube Bilgisi",on_delete=models.SET_NULL)
    ozel_kod1 = models.CharField(verbose_name="Özel Kod",blank=True,null=True,max_length=200)
    ozel_kod2 = models.CharField(verbose_name="Özel Kod 2",blank=True,null=True,max_length=200)
    departman = models.CharField(verbose_name="departman",blank=True,null=True,max_length=200)
    onay = models.BooleanField(verbose_name="Sipariş Onaylandı",default=False)
    gunluk_kur = models.CharField(max_length=200, verbose_name="Günlük Kur", blank=True, null=True)
    uygun_kur = models.CharField(max_length=200, verbose_name="Uygun Kur", blank=True, null=True)
    faturaya_aktar = models.BooleanField(verbose_name="Faturaya Aktarıldı" , default=False)
    tutar_doviz = models.FloatField(verbose_name="Tutar Döviz",blank=True,null=True)
    tutar_tl = models.FloatField(verbose_name="Tutar TL",blank=True,null=True)
    aktif_pasif = models.BooleanField(verbose_name="Aktif Pasif Olayı", default=False)
    otv_tutari = models.FloatField(verbose_name="Ötv Tutarı TL",blank=True,null=True)
    kdv_tutari = models.FloatField(verbose_name="KDV Tutarı TL",blank=True,null=True)
    indirim_tutari = models.FloatField(verbose_name="İndirim Tutarı TL",blank=True,null=True)
    genel_tutari = models.FloatField(verbose_name="Genel Tutarı TL",blank=True,null=True)
    iptaledildi = models.BooleanField(verbose_name="İptal Edildi" , default=False)
    silinme_bilgisi = models.BooleanField(verbose_name="Sİpariş Silme Durumu",default=False)

class irsaliye_olustur(models.Model):    
    grup_kodu = models.ForeignKey(irsaliyeislem_durumlari,blank=True,null=True,on_delete=models.SET_NULL,verbose_name="Grup Kodu")
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    tip = models.CharField(max_length=200,verbose_name="tip",blank=True,null=True)
    teslim_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    teslim_sekli = models.CharField(max_length=200, verbose_name="Teslim Şekli", blank=True, null=True)
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL)
    miktar = models.FloatField(verbose_name="Miktar" ,blank=True,null=True,default=1)
    kalan_miktar = models.FloatField(verbose_name="Miktar" ,blank=True,null=True,default=1)
    birim = models.CharField(max_length=200,verbose_name="Birim",blank=True,null=True)
    birim_fiyat_tl = models.FloatField(verbose_name="Birim Fiyatı TL" ,blank=True,null=True,default=1)
    birim_fiyat_dvz = models.FloatField(verbose_name="Birim Fiyatı Döviz" ,blank=True,null=True,default=1)
    indirim_yuzdesi = models.FloatField(verbose_name="İndirim Yüzdesi" ,blank=True,null=True,default=0)
    indirim_tutari_tl = models.FloatField(verbose_name="İndirim Tutarı TL" ,blank=True,null=True,default=0)
    kdv_yuzdesi = models.FloatField(verbose_name="KDV Yüzdesi" ,blank=True,null=True,default=0)
    kdv_tutari_tl = models.FloatField(verbose_name="KDV Tutarı TL" ,blank=True,null=True,default=0)
    otv_yuzdesi = models.FloatField(verbose_name="ÖTV Yüzdesi" ,blank=True,null=True,default=0)
    otv_tutari_tl = models.FloatField(verbose_name="ÖTV Tutarı TL" ,blank=True,null=True,default=0)
    stoktutari = models.FloatField(verbose_name="Stok Tutarı TL" ,blank=True,null=True,default=0)
    durumu = models.CharField(max_length=200,verbose_name="Durum",blank=True,null=True)
    indirim1 = models.FloatField(verbose_name="İndirim 1",blank=True,null=True)
    indirim2 = models.FloatField(verbose_name="İndirim 2",blank=True,null=True)
    indirim3 = models.FloatField(verbose_name="İndirim 3",blank=True,null=True)
    ozelkod1 = models.CharField(max_length=200, verbose_name="Özel Kod", blank=True, null=True)
    ozelkod2 = models.CharField(max_length=200, verbose_name="Özel Kod 2", blank=True, null=True)
    departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    satir_aciklamasi = models.CharField(max_length=200, verbose_name="Satır Açıklaması", blank=True, null=True)
    serino = models.CharField(verbose_name="Seri No",max_length=100,blank=True,null=True)
    s_brim = models.CharField(verbose_name="Serbest Brim",max_length=100,blank=True,null=True)
    s_miktar = models.FloatField(verbose_name="Serbest Miktar" ,blank=True,null=True,default=1)
    alternatifstokkodu = models.CharField(verbose_name="alternatif stok kodu",max_length=100,blank=True,null=True)
    alternatifstokadi = models.CharField(verbose_name="alternatif stok adı",max_length=200,blank=True,null=True)
    kalite = models.CharField(verbose_name="Kalite",max_length=200,blank=True,null=True)
    ozellik1 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik2 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik3 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik4 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik5 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    net_agirlik_kg = models.FloatField(verbose_name="Net Ağırlık KG" ,blank=True,null=True,default=1)
    Burut_agirlik_kg = models.FloatField(verbose_name="Bürüt Ağırlık KG" ,blank=True,null=True,default=1)
    pk_miktari = models.FloatField(verbose_name="Pk Miktarı" ,blank=True,null=True,default=1)
    pk_aciklamasi = models.CharField(max_length=200, verbose_name="PK Açıklaması", blank=True, null=True)
    parti_kodu = models.CharField(max_length=200,verbose_name="Parti Kodu",blank=True,null=True)
    son_kullanim_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)

#fatura
class fatura_durumlari(models.Model):
    siparis_turu_secim = (
        ("",""),
        ("Satış Faturası","Satış Faturası"),
        ("Satış İade Faturası","Satış İade Faturası"),
        ("Alış Faturası","Alış Faturası"),
        ("Alış İade Faturası","Alış İade Faturası"),
        ("Gider Faturası","Gider Faturası"),
        ("Parakende Satış Faturası","Parakende Satış Faturası"),
        ("Parakende Satış iadesi Faturası","Parakende Satış iadesi Faturası"),
        ("Müstahsil Makbuzu","Müstahsil Makbuzu"),
        ("Gider Pusulası","Gider Pusulası"),
        ("SMM Makbuzu","SMM Makbuzu"),
        ("İhraç Kayıtlı Satış Faturası","İhraç Kayıtlı Satış Faturası"),
        ("İhraç Kayıtlı Alış Faturası","İhraç Kayıtlı Alış Faturası"),
        ("Gider Pusulası (KDV'li)","Gider Pusulası (KDV'li)"),
        ("İhracat Faturası","İhracat Faturası"),
        ("Yolcu Beraber Fatura","Yolcu Beraber Fatura"),

    )
    ent_kodu_secim = (
        ("1","1"),
        ("2","2")
    )
    kdv_durumu_secim = (
        ("Hariç","Hariç"),
        ("Dahil","Dahil")
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "£"),
        ("Dolar", "$")
    )
    faturaislem_turu=(
        ("Yurt İçi","Yurt İçi"),
        ("Yurt Dışı","Yurt Dışı")

    )
    siparis_tur = models.CharField(max_length=200,verbose_name="Sipariş Türü",choices=siparis_turu_secim,default="")
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    depo = models.CharField(max_length=200,verbose_name="Depo Adı",blank=True,null=True)
    ent_kodu = models.CharField(max_length=20,verbose_name="Entegrasyon Kodu",choices=ent_kodu_secim,default="1")
    kdv_durumu = models.CharField(max_length=200,verbose_name="KDV Durumu",choices=kdv_durumu_secim,default="Hariç")
    fatura_no = models.CharField(max_length=200,verbose_name="Sipariş No",blank=True,null=True)
    tarih = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    satici = models.CharField(max_length=200, verbose_name="SAtıcı", blank=True, null=True)
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    sube_kodu = models.ForeignKey(sube,blank=True,null=True,verbose_name="Şube Bilgisi",on_delete=models.SET_NULL)
    ozel_kod1 = models.CharField(verbose_name="Özel Kod",blank=True,null=True,max_length=200)
    ozel_kod2 = models.CharField(verbose_name="Özel Kod 2",blank=True,null=True,max_length=200)
    departman = models.CharField(verbose_name="departman",blank=True,null=True,max_length=200)
    onay = models.BooleanField(verbose_name="Sipariş Onaylandı",default=False)
    gunluk_kur = models.CharField(max_length=200, verbose_name="Günlük Kur", blank=True, null=True)
    uygun_kur = models.CharField(max_length=200, verbose_name="Uygun Kur", blank=True, null=True)
    tutar_doviz = models.FloatField(verbose_name="Tutar Döviz",blank=True,null=True)
    tutar_tl = models.FloatField(verbose_name="Tutar TL",blank=True,null=True)
    aktif_pasif = models.BooleanField(verbose_name="Aktif Pasif Olayı", default=False)
    kdv_doviz = models.FloatField(verbose_name="Ötv Tutarı TL",blank=True,null=True)
    kdv_tutari = models.FloatField(verbose_name="KDV Tutarı TL",blank=True,null=True)
    indirim_tutari = models.FloatField(verbose_name="İndirim Tutarı TL",blank=True,null=True)
    genel_tutari = models.FloatField(verbose_name="Genel Tutarı TL",blank=True,null=True)
    iptaledildi = models.BooleanField(verbose_name="İptal Edildi" , default=False)
    silinme_bilgisi = models.BooleanField(verbose_name="Sİpariş Silme Durumu",default=False)
    kasa = models.ForeignKey(Kasa, verbose_name="Kasa Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL)
    banka = models.ForeignKey(banka, verbose_name="Banka Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL)
    deg_tarih = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    proje_adi = models.CharField(max_length=200,verbose_name="Proje Adı",blank=True,null=True)
    fatura_yeri = models.CharField(max_length=200,verbose_name="Yurt İçi / Dışı",choices=faturaislem_turu,default="Yurt İçi")
    fatura_tipi= models.CharField(max_length=200,verbose_name="Açık Kapalı",blank=True,null=True)
class fatura_olustur(models.Model):    
    grup_kodu = models.ForeignKey(fatura_durumlari,blank=True,null=True,on_delete=models.SET_NULL,verbose_name="Grup Kodu")
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    tip = models.CharField(max_length=200,verbose_name="tip",blank=True,null=True)
    teslim_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    teslim_sekli = models.CharField(max_length=200, verbose_name="Teslim Şekli", blank=True, null=True)
    stok_karti_bilgisi = models.ForeignKey(stok_kartlar, verbose_name="Stok Kartı Bilgisi", blank=True, null=True,
                                             on_delete=models.SET_NULL)
    miktar = models.FloatField(verbose_name="Miktar" ,blank=True,null=True,default=1)
    kalan_miktar = models.FloatField(verbose_name="Miktar" ,blank=True,null=True,default=1)
    birim = models.CharField(max_length=200,verbose_name="Birim",blank=True,null=True)
    birim_fiyat_tl = models.FloatField(verbose_name="Birim Fiyatı TL" ,blank=True,null=True,default=1)
    birim_fiyat_dvz = models.FloatField(verbose_name="Birim Fiyatı Döviz" ,blank=True,null=True,default=1)
    indirim_yuzdesi = models.FloatField(verbose_name="İndirim Yüzdesi" ,blank=True,null=True,default=0)
    indirim_tutari_tl = models.FloatField(verbose_name="İndirim Tutarı TL" ,blank=True,null=True,default=0)
    kdv_yuzdesi = models.FloatField(verbose_name="KDV Yüzdesi" ,blank=True,null=True,default=0)
    kdv_tutari_tl = models.FloatField(verbose_name="KDV Tutarı TL" ,blank=True,null=True,default=0)
    otv_yuzdesi = models.FloatField(verbose_name="ÖTV Yüzdesi" ,blank=True,null=True,default=0)
    otv_tutari_tl = models.FloatField(verbose_name="ÖTV Tutarı TL" ,blank=True,null=True,default=0)
    stoktutari = models.FloatField(verbose_name="Stok Tutarı TL" ,blank=True,null=True,default=0)
    durumu = models.CharField(max_length=200,verbose_name="Durum",blank=True,null=True)
    indirim1 = models.FloatField(verbose_name="İndirim 1",blank=True,null=True)
    indirim2 = models.FloatField(verbose_name="İndirim 2",blank=True,null=True)
    indirim3 = models.FloatField(verbose_name="İndirim 3",blank=True,null=True)
    ozelkod1 = models.CharField(max_length=200, verbose_name="Özel Kod", blank=True, null=True)
    ozelkod2 = models.CharField(max_length=200, verbose_name="Özel Kod 2", blank=True, null=True)
    departman = models.CharField(max_length=200, verbose_name="Departman", blank=True, null=True)
    satir_aciklamasi = models.CharField(max_length=200, verbose_name="Satır Açıklaması", blank=True, null=True)
    serino = models.CharField(verbose_name="Seri No",max_length=100,blank=True,null=True)
    s_brim = models.CharField(verbose_name="Serbest Brim",max_length=100,blank=True,null=True)
    s_miktar = models.FloatField(verbose_name="Serbest Miktar" ,blank=True,null=True,default=1)
    alternatifstokkodu = models.CharField(verbose_name="alternatif stok kodu",max_length=100,blank=True,null=True)
    alternatifstokadi = models.CharField(verbose_name="alternatif stok adı",max_length=200,blank=True,null=True)
    kalite = models.CharField(verbose_name="Kalite",max_length=200,blank=True,null=True)
    ozellik1 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik2 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik3 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik4 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik5 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    ozellik6 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik7 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik8 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik9 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik10 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    ozellik11 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik12 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik13 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik14 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik15 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    ozellik16 = models.CharField(verbose_name="ozellil1",max_length=200,blank=True,null=True)
    ozellik17 = models.CharField(verbose_name="ozellil2",max_length=200,blank=True,null=True)
    ozellik18 = models.CharField(verbose_name="ozellil3",max_length=200,blank=True,null=True)
    ozellik19 = models.CharField(verbose_name="ozellil4",max_length=200,blank=True,null=True)
    ozellik20 = models.CharField(verbose_name="ozellil5",max_length=200,blank=True,null=True)
    net_agirlik_kg = models.FloatField(verbose_name="Net Ağırlık KG" ,blank=True,null=True,default=1)
    Burut_agirlik_kg = models.FloatField(verbose_name="Bürüt Ağırlık KG" ,blank=True,null=True,default=1)
    pk_miktari = models.FloatField(verbose_name="Pk Miktarı" ,blank=True,null=True,default=1)
    pk_aciklamasi = models.CharField(max_length=200, verbose_name="PK Açıklaması", blank=True, null=True)
    parti_kodu = models.CharField(max_length=200,verbose_name="Parti Kodu",blank=True,null=True)
    son_kullanim_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    kdv_istisna_yuzdesi = models.FloatField(verbose_name="KDV İstisna Yüzdesi" ,blank=True,null=True,default=0)
    kdv_istisna_tl = models.FloatField(verbose_name="KDV İstisna Tl" ,blank=True,null=True,default=0)
    kdv_istisna_koduu = models.CharField(max_length=100,verbose_name="KDV İstisna Kodu",blank=True,null=True)
    kdv_istisna_aciklamasi = models.CharField(max_length=200,verbose_name="KDV İstisna Açıklaması",blank=True,null=True)
    tevkifat_kodu = models.CharField(max_length=200,verbose_name="Tevkifat Kodu",blank=True,null=True)
    tevkifat_yuzdesi = models.FloatField(verbose_name="Tevkifat Yüzdesi" ,blank=True,null=True,default=0)
    tevkifat_tl = models.FloatField(verbose_name="Tevkifat Tl" ,blank=True,null=True,default=0)
    otv_matrah_tl = models.FloatField(verbose_name="ÖTV Matrah Tl" ,blank=True,null=True,default=0)
    otv_birim_fiyat_tl = models.FloatField(verbose_name="ÖTV Birim Fİyat Tl" ,blank=True,null=True,default=0)
    otv_kodu = models.CharField(max_length=200,verbose_name="ÖTV Kodu",blank=True,null=True)
    otv_tahsil_yuzdesi = models.FloatField(verbose_name="ÖTV Tahsil Yuzdesi" ,blank=True,null=True,default=0)
    otv_tecil_yuzdesi = models.FloatField(verbose_name="ÖTV Tecil Yuzdesi" ,blank=True,null=True,default=0)
    otv_istisna_kodu = models.CharField(max_length=100,verbose_name="ÖTV İstisna Kodu",blank=True,null=True)
    otv_tevkifat_yuzdesi = models.FloatField(verbose_name="ÖTV Tecil Yuzdesi" ,blank=True,null=True,default=0)
    gv_stopaj_yuzdesi = models.FloatField(verbose_name="GV Stopaj Yuzdesi" ,blank=True,null=True,default=0)
    mera_fonu_tl = models.FloatField(verbose_name="Mera Fonu Tl" ,blank=True,null=True,default=0)
    mera_fonu_yuzdesi = models.FloatField(verbose_name="Mera Fonu Yüzdesi" ,blank=True,null=True,default=0)
    muh_kodu = models.CharField(max_length=200,verbose_name="Muh Kodu",blank=True,null=True)
    kdv_muh_kodu = models.CharField(max_length=200,verbose_name="KDV Muh Kodu",blank=True,null=True)
    gv_muh_kodu = models.CharField(max_length=200,verbose_name="GV Muh Kodu",blank=True,null=True)
    kampanya_kodu = models.CharField(max_length=200,verbose_name="Kampanya Kodu",blank=True,null=True)
    vade_tarihi = models.DateField(verbose_name="Vade Tarihi",blank=True,null=True)
    aciklama = models.CharField(max_length=200,verbose_name="Açıklama",blank=True,null=True)
    net_birim_fiyat_tl = models.FloatField(verbose_name="Birim Fiyatı TL" ,blank=True,null=True,default=1)
    net_birim_fiyat_dvz = models.FloatField(verbose_name="Birim Fiyatı Döviz" ,blank=True,null=True,default=1)
    irsaliye_tarihi = models.DateField(verbose_name="İrsaliye Tarihi",blank=True,null=True)
    irsaliye_no = models.CharField(max_length=200,verbose_name="İrsaliye No",blank=True,null=True)
    mal_kabul_no = models.CharField(max_length=200,verbose_name="İrsaliye No",blank=True,null=True)

class cek_senet_durumu(models.Model):
    ent_kodu_secim = (
        ("1","1"),
        ("2","2")
    )
    kdv_durumu_secim = (
        ("Hariç","Hariç"),
        ("Dahil","Dahil")
    )
    doviz = (
        ("", ""),
        ("TL", "TL"),
        ("Euro", "£"),
        ("Dolar", "$")
    )
    bodro_tarihi = models.DateField(verbose_name="Kayıt Tarihi",blank=True,null=True)
    bodro_no = models.CharField(max_length=200,verbose_name="Bodro No",blank=True,null=True)
    ent_kodu = models.CharField(max_length=20,verbose_name="Entegrasyon Kodu",choices=ent_kodu_secim,default="1")
    sube_kodu = models.ForeignKey(sube,blank=True,null=True,verbose_name="Şube Bilgisi",on_delete=models.SET_NULL)
    saat = models.TimeField(verbose_name="Saat",blank=True,null=True)
    devir_mi = models.BooleanField(verbose_name="Devir Mi ? ",default=False)
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    islem_doviz_cinsi = models.CharField(max_length=100, verbose_name="İşlem Döviz Cinsi", choices=doviz, default="")
    ozel_kod1 = models.CharField(verbose_name="Özel Kod",blank=True,null=True,max_length=200)
    ozel_kod2 = models.CharField(verbose_name="Özel Kod 2",blank=True,null=True,max_length=200)
    departman = models.CharField(verbose_name="departman",blank=True,null=True,max_length=200)
    kampkodu = models.CharField(verbose_name="Kamp Kod",blank=True,null=True,max_length=200)
    muh_kodu = models.CharField(verbose_name="muh. Kod 2",blank=True,null=True,max_length=200)
    aciklama = models.CharField(verbose_name="açıklama",blank=True,null=True,max_length=200)
    tahsilati_ismeli_yapan = models.CharField(verbose_name="Tahsilati İşlemi Yapan",blank=True,null=True,max_length=200)
    
#fatura
class dilekceler(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    dilekce_adi = models.CharField(max_length=200,verbose_name="Dilekçe Adı",blank=True,null=True)
    dilekce = RichTextField(verbose_name="Dilekçe Metni",blank=True,null=True)



#genel muhasebe 

class genel_muhasebe(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    fis_turu = models.CharField(max_length=200,verbose_name="yevmiye No",blank=True,null=True)
    fis_tarihi = models.DateField(verbose_name="Fiş Tarihi",blank=True,null=True)
    fis_no = models.CharField(max_length=200,verbose_name="Fiş No",blank=True,null=True)
    yevmiye_no = models.CharField(max_length=200,verbose_name="yevmiye No",blank=True,null=True)

class genel_muhasebe_fis( models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugufis = models.ForeignKey(genel_muhasebe,blank=True,null=True,on_delete=models.SET_NULL)
    hesap_plani_secim = models.ForeignKey(HesapPlanlari,blank=True,null=True,on_delete=models.SET_NULL)
    evrak_no = models.CharField(max_length=200,verbose_name="Fiş No",blank=True,null=True)
    evrak_tarihi = models.DateField(verbose_name="Evrak Tarihi",blank=True,null=True)
    bt_turu = models.CharField(max_length= 200,blank=True,null=True,verbose_name = "BT Türü")
    vergi_numarasi = models.CharField(max_length= 200,blank=True,null=True,verbose_name = "Vergi Nuımarası")
    aciklama = models.TextField(blank=True,null=True,verbose_name = "Açıklama")
    aciklama8belgesi = models.TextField(blank=True,null=True,verbose_name = "aciklama8belgesi")
    borc = models.FloatField(verbose_name="Borç Bilgisi",default = 0)
    alacak_bilgisi = models.FloatField(verbose_name="Borç Bilgisi",default = 0)


class musteri_cari(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    cari_adi = models.CharField(max_length = 200 ,verbose_name = "Cari Adı",blank = True,null = True)
    sininme_bilgisi = models.BooleanField(default = False)
class musteri_cari_fis(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_cari = models.ForeignKey(musteri_cari,blank=True,null=True,on_delete=models.SET_NULL)
    evrak_tarihi = models.DateField(verbose_name="evrak Tarihi",blank = True,null = True)
    aciklama = models.TextField(verbose_name="Açıklama",blank = True,null = True)
    alacak = models.FloatField(verbose_name="Alacak ",default = 0)
    borc = models.FloatField(verbose_name="Borc ",default = 0)


class musavir_stok(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    stok_kodu = models.CharField(max_length = 200 ,verbose_name = "Stok Kodu",blank = True,null = True)
    stok_adi = models.CharField(max_length = 200 ,verbose_name = "Stok Adı",blank = True,null = True)
    birim = models.CharField(max_length = 200 ,verbose_name = "Birim",blank = True,null = True)
    envanter_yonetimi = models.CharField(max_length = 200 ,verbose_name = "Envanter yönetimi",blank = True,null = True)
    ort_kar = models.FloatField(default = 0,verbose_name = "Ort Kar")
    ticari = models.CharField(max_length = 200 ,verbose_name = "Envanter yönetimi",blank = True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    sininme_bilgisi = models.BooleanField(default = False)

class musavir_stok_fisi(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_stok = models.ForeignKey(musavir_stok,blank=True,null=True,on_delete=models.SET_NULL)
    evrak_tarihi = models.DateField(verbose_name = "Evrak Tarihi",blank = True,null = True)
    donem = models.CharField(max_length = 200 ,verbose_name = "Dönem Başı Veya Dönem İçi",blank = True,null = True)
    iademi = models.CharField(max_length = 200 ,verbose_name = "İademi ? ",blank = True,null = True)
    evrak_no = models.CharField(max_length = 200 ,verbose_name = "evrak No",blank = True,null = True)
    evrak_aciklama = models.CharField(max_length = 200 ,verbose_name = "Evrak Açıklama",blank = True,null = True)
    giris_miktari = models.FloatField(default = 0,verbose_name = "Giriş Miktari")
    cikis_miktari = models.FloatField(default = 0,verbose_name = "Çıkış Miktari")
    giris_birim_fiyati = models.FloatField(default = 0,verbose_name = "Giriş Brm Fiyatı")
    giris_fiyati = models.FloatField(default = 0,verbose_name = "Giriş Fiyatı")
    cikis_birim_fiyati = models.FloatField(default = 0,verbose_name = "Çıkış Brm Fiyatı")
    cikis_fiyati = models.FloatField(default = 0,verbose_name = "Çıkış Fiyatı")


class amortisman_bilgileri(models.Model):
    N1 = models.CharField(max_length = 200,verbose_name="N3",blank = True,null = True)
    N2 = models.CharField(max_length = 200,verbose_name="N3",blank = True,null = True)
    N3 = models.CharField(max_length = 200,verbose_name="N3",blank = True,null = True)
    N4 = models.CharField(max_length = 200,verbose_name="N4",blank = True,null = True)
    amortismana_tabi_olan_ikstisidai_kiymet = models.CharField(max_length = 400,verbose_name="N4",blank = True,null = True)
    faydali_omur = models.BigIntegerField(default = 0,verbose_name="Faydalı Ömür")
    amortisman_orani = models.FloatField(default = 0,verbose_name = "Amortisman Oranı")
    defter_beyan_kodu = models.CharField(max_length = 200,verbose_name="Defter Beyan Kodu",blank = True,null = True)


#genel_muhasebe Cari Bilgileri

class Genel_Muhasebe_cari_bilgileri(models.Model):
    cari_adi = models.CharField(max_length = 400,verbose_name = "Cari Adı",blank = True,null = True)
    vergi_tc_kimlikno = models.CharField(max_length = 100,verbose_name = "Vergi Tc Kimlik No",blank = True,null = True)
    vergi_dairesi_bilgisi = models.CharField(max_length = 200,verbose_name = "Vergi Dairesi Bilgisi",blank = True,null = True)
    ulke_kodu = models.CharField(max_length = 20,verbose_name = "Ülke Kodu",blank = True,null = True)
    firma_unvani = models.CharField(max_length = 600,verbose_name = "Firma unvanı Adı",blank = True,null = True)
    telefon_1 = models.CharField(verbose_name = "Telefon 1 ",max_length = 20,blank = True,null = True)
    telefon_2 = models.CharField(verbose_name = "Telefon 1 ",max_length = 20,blank = True,null = True)
    telefon_3 = models.CharField(verbose_name = "Telefon 1 ",max_length = 20,blank = True,null = True)
    telefon_4 = models.CharField(verbose_name = "Telefon 1 ",max_length = 20,blank = True,null = True)
    adres_1 = models.CharField(verbose_name = "Adres ",max_length = 200,blank = True,null = True)
    adres_2 = models.CharField(verbose_name = "Adres 1 ",max_length = 200,blank = True,null = True)
    adres_3 = models.CharField(verbose_name = "Adres 1 ",max_length = 200,blank = True,null = True)
    adres_4 = models.CharField(verbose_name = "Adres 1 ",max_length = 200,blank = True,null = True)
    fax_1 = models.CharField(verbose_name = "Fax 1 ",max_length = 20,blank = True,null = True)
    fax_2 = models.CharField(verbose_name = "Fax 2 ",max_length = 20,blank = True,null = True)
    cep_1 = models.CharField(verbose_name = "Cep 1 ",max_length = 20,blank = True,null = True)
    cep_2 = models.CharField(verbose_name = "Cep 2 ",max_length = 20,blank = True,null = True)
    email_1 = models.EmailField(verbose_name = "Email ",max_length = 200,blank = True,null = True)
    email_2 = models.EmailField(verbose_name = "Email 1 ",max_length = 200,blank = True,null = True)
    web_adresi = models.CharField(verbose_name = "web 1 ",max_length = 400,blank = True,null = True)
    yetkili = models.CharField(verbose_name = "Yetkili ",max_length = 400,blank = True,null = True)
    gorevi = models.CharField(verbose_name = "Görevi ",max_length = 400,blank = True,null = True)
    bilgi_notu = models.CharField(verbose_name = "Bilgi Notu ",max_length = 400,blank = True,null = True)
    il = models.CharField(verbose_name = "il ",max_length = 400,blank = True,null = True)
    ilce = models.CharField(verbose_name = "İlçe ",max_length = 400,blank = True,null = True)
    posta_kodu = models.CharField(verbose_name = "Posta Kodu ",max_length = 400,blank = True,null = True)
    ulke = models.CharField(verbose_name = "Ülke ",max_length = 400,blank = True,null = True)
    satis_muh_kodu = models.ForeignKey(HesapPlanlari,blank = True,null = True,on_delete = models.SET_NULL,related_name ="satis_muhtasar_kodu")
    alis_muh_kodu = models.ForeignKey(HesapPlanlari,blank = True,null = True,on_delete = models.SET_NULL,related_name ="alis_muhtasar_kodu")

class firma_ayarlari_ayar_kisimi(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    damga_vergisi_5033sk = models.CharField(max_length = 200,verbose_name = "Damga Vergisi ,5033 Sk",blank = True,null = True)
    muhasabe_odemesi_gelir_vergisi_kesinti_orani = models.FloatField(default = 0,verbose_name="Gelir Ödemesi Vergi Kesintisi")
    kira_odemesi_gelir_vergisi_kesinti_orani = models.FloatField(default = 0,verbose_name="Kira Ödemesi Vergi Kesintisi")
    kdv_beyannamesi_damga_vergisi = models.FloatField(default = 0,verbose_name="KDV Beyannamesi Damga Vergisi")
    gecici_vergi_beyannamesi_damga_vergisi = models.FloatField(default = 0,verbose_name="Gecici Vergi Beyannamesi Damga Vergisi")
    gecici_vergi_orani_kurumlar = models.FloatField(default = 0,verbose_name="Gecici Vergi Orani Kurumlar")
    gecici_vergi_orani_gercek_kisiler= models.FloatField(default = 0,verbose_name="Gecici Vergi Orani Gerçek Kişiler")

class firma_ayarlari_smm_ymm_sm_bilgileri(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    ad = models.CharField(max_length = 400,verbose_name = "ad",blank = True,null = True)
    soyad = models.CharField(max_length = 400,verbose_name = "soyad",blank = True,null = True)
    musavir_turu = models.CharField(max_length = 400,verbose_name = "Müşavir Türü",blank = True,null = True)
    kayitliolduguoda = models.CharField(max_length = 400,verbose_name = "Kayıtlı oldugu Oda",blank = True,null = True)
    odasicilno = models.CharField(max_length = 400,verbose_name = "Oda Sicil No",blank = True,null = True)
    muhur_numarasi = models.CharField(max_length = 400,verbose_name = "Mühür Numarası",blank = True,null = True)
    baslama_tarihi = models.CharField(max_length = 400,verbose_name = "Başlama Tarihi",blank = True,null = True)
    ortakli_unvan = models.CharField(max_length = 400,verbose_name = "Ortak Unvanlı",blank = True,null = True)
    sirket_unvan = models.CharField(max_length = 400,verbose_name = "Şirket Unvanlı",blank = True,null = True)
    vergi_dairesi = models.CharField(max_length = 400,verbose_name = "Vergi Dairesi",blank = True,null = True)
    vergi_no = models.CharField(max_length = 400,verbose_name = "Vergi No",blank = True,null = True)
    ticari_sicil_no = models.CharField(max_length = 400,verbose_name = "Ticari Sicili No",blank = True,null = True)
    vergi_kimlik_no = models.CharField(max_length = 400,verbose_name = "Vergi Kimlik No",blank = True,null = True)
    tc_kimlik_no = models.CharField(max_length = 400,verbose_name = "Tc Kimlik No",blank = True,null = True)
    goreve_baslama_tarihi = models.CharField(max_length = 400,verbose_name = "Görev Başlama Tarihi",blank = True,null = True)
    isyeri_adresi = models.CharField(max_length = 400,verbose_name = "İşeri Adresi",blank = True,null = True)
    fax = models.CharField(max_length = 400,verbose_name = "fax",blank = True,null = True)
    eposta = models.CharField(max_length = 400,verbose_name = "E-Posta",blank = True,null = True)
    arac_plaka_no = models.CharField(max_length = 400,verbose_name = "Araç Plaka No",blank = True,null = True)
    cinsiyet = models.CharField(max_length = 400,verbose_name = "Cinsiyet",blank = True,null = True)
    uyrugu = models.CharField(max_length = 400,verbose_name = "Uyruğu",blank = True,null = True)
    baba_adi = models.CharField(max_length = 400,verbose_name = "Baba Adı",blank = True,null = True)
    anne_adi = models.CharField(max_length = 400,verbose_name = "Anne Adı",blank = True,null = True)
    dogum_yeri = models.CharField(max_length = 400,verbose_name = "Doğum Yeri",blank = True,null = True)
    dogum_tarihi = models.CharField(max_length = 400,verbose_name = "Doğum Tarihi",blank = True,null = True)
    nufusa_kayitli_oldugu_yer = models.CharField(max_length = 400,verbose_name = "Nüfusta Kayıtlı Olduğu Yer",blank = True,null = True)
    ikametgah_adresi = models.CharField(max_length = 400,verbose_name = "İkametgah Adresi",blank = True,null = True)
    ikametgah_bulvar = models.CharField(max_length = 400,verbose_name = "İkametgah bulvar",blank = True,null = True)
    ikametgah_cadde = models.CharField(max_length = 400,verbose_name = "İkametgah Cadde",blank = True,null = True)
    ikametgah_sokak = models.CharField(max_length = 400,verbose_name = "İkametgah Sokak",blank = True,null = True)
    ikametgah_ic_kapi = models.CharField(max_length = 400,verbose_name = "İkametgah İç Kapı",blank = True,null = True)
    ikametgah_dis_kapi = models.CharField(max_length = 400,verbose_name = "İkametgah Dış Kapı",blank = True,null = True)
    ikametgah_mahalle_koy = models.CharField(max_length = 400,verbose_name = "İkametgah Mahalle Köy",blank = True,null = True)
    ikametgah_ilce = models.CharField(max_length = 400,verbose_name = "İkametgah İlçe",blank = True,null = True)
    ikametgah_il = models.CharField(max_length = 400,verbose_name = "İkametgah İl",blank = True,null = True)
    ikametgah_posta_kodu = models.CharField(max_length = 400,verbose_name = "İkametgah Posta Kodu",blank = True,null = True)
    cep_telefonu = models.CharField(max_length = 400,verbose_name = "Cep Telefonu",blank = True,null = True)


#demirbaş 
"""class demirbaslar(models.Model):
    pass"""


#ürünler
class urunler(models.Model):
    urun_kodu = models.CharField(max_length = 20,verbose_name= "Ürün Kodu",blank = True,null = True)
    grup = models.CharField(max_length = 100,verbose_name = "Grup Kodu",blank = True,null = True)
    urun_adi = models.CharField(max_length = 200,verbose_name = "ürün Adları",blank = True,null  = True)
    tutar = models.FloatField(default = 0,verbose_name = "Tutarı")
    birimi = models.CharField(max_length  = 200 ,verbose_name = "Birimi",blank = True,null = True)

#GEKAP TAHSİL EDİLMEYECEK ÜRÜNLER
class dayanak(models.Model):
    aciklama = models.CharField(max_length = 200 ,verbose_name = "Açıklama")



#beyannameler
#KDV1
class kdv1_beyannamesi_bilgileri(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    ay = models.DateField(verbose_name = "Tarihi",blank = True,null=True)
#Matrah
#TEVKİFAT UYGULANMAYAN İŞLEMLER
class matrah_bildirimi_tevkifatuygulanmayanislemler(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    matrah = models.FloatField(verbose_name = "Matrah",default = 0)
    kdv = models.FloatField(verbose_name = "KDV",default = 0)
    vergi = models.FloatField(verbose_name = "Vergi",default = 0)
    matrah1 = models.FloatField(verbose_name = "Matrah",default = 0)
    kdv1 = models.FloatField(verbose_name = "KDV",default = 0)
    vergi1 = models.FloatField(verbose_name = "Vergi",default = 0)
    matrah2 = models.FloatField(verbose_name = "Matrah",default = 0)
    kdv2 = models.FloatField(verbose_name = "KDV",default = 0)
    vergi2 = models.FloatField(verbose_name = "Vergi",default = 0)
#KISMİ TEVKİFAT UYGULANAN İŞLEMLER
class matrah_bildirimi_kismi_tevkifatuygulanmayanislemler(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    # İlk İşlem
    islem_turu = models.ForeignKey(tevkifat_tur_kodu, blank=True, null=True, on_delete=models.SET_NULL,related_name='islem_turu')
    matrah = models.FloatField(verbose_name="Matrah", default=0)
    kdv = models.FloatField(verbose_name="KDV", default=0)
    vergi = models.FloatField(verbose_name="Vergi", default=0)
    tevkifatorani = models.CharField(max_length=20, verbose_name="tevkifatorani", blank=True, null=True)
    
    # İkinci İşlem
    islem_turu1 = models.ForeignKey(tevkifat_tur_kodu, blank=True, null=True, on_delete=models.SET_NULL,related_name='islem_turu1')
    matrah1 = models.FloatField(verbose_name="Matrah", default=0)
    kdv1 = models.FloatField(verbose_name="KDV", default=0)
    vergi1 = models.FloatField(verbose_name="Vergi", default=0)
    tevkifatorani1 = models.CharField(max_length=20, verbose_name="tevkifatorani", blank=True, null=True)
    
    # Üçüncü İşlem
    islem_turu2 = models.ForeignKey(tevkifat_tur_kodu, blank=True, null=True, on_delete=models.SET_NULL,related_name='islem_turu2')
    matrah2 = models.FloatField(verbose_name="Matrah", default=0)
    kdv2 = models.FloatField(verbose_name="KDV", default=0)
    vergi2 = models.FloatField(verbose_name="Vergi", default=0)
    tevkifatorani2 = models.CharField(max_length=20, verbose_name="tevkifatorani", blank=True, null=True)
    # Dördüncü İşlem
    islem_turu3 = models.ForeignKey(tevkifat_tur_kodu, blank=True, null=True, on_delete=models.SET_NULL,related_name='islem_turu3')
    matrah3 = models.FloatField(verbose_name="Matrah", default=0)
    kdv3 = models.FloatField(verbose_name="KDV", default=0)
    vergi3 = models.FloatField(verbose_name="Vergi", default=0)
    tevkifatorani3 = models.CharField(max_length=20, verbose_name="tevkifatorani", blank=True, null=True)
#DİĞER İŞLEMLER
    
class matrah_bildirimi_digerislemleri(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    #Türkiye'de İkamet Etmeyenlere KDV Hesaplanarak Yapılan Satışlar (Yolcu Beraberi Eşya)[KDVGUT - (II/A-5)]
    bilgi = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah1 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi1 = models.FloatField(verbose_name = "Vergi",default = 0)
    #Amortismana Tabi Sabt Kymet (Taşımaz, Taşıt Araçlan, Demirbaş, Makine ve Teçhizat vb.) Satışları
    bilgi2 = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah2 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi2 = models.FloatField(verbose_name = "Vergi",default = 0)
    #Amortismana Tabi Sabt Kymet (Taşımaz, Taşıt Araçlan, Demirbaş, Makine ve Teçhizat vb.) Satışları
    bilgi3 = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah3 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi3 = models.FloatField(verbose_name = "Vergi",default = 0)  
    #Amortismana Tabi Sabt Kymet (Taşımaz, Taşıt Araçlan, Demirbaş, Makine ve Teçhizat vb.) Satışları
    bilgi4 = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah4 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi4 = models.FloatField(verbose_name = "Vergi",default = 0)  
    #Alınan Malları İadesi, Gerçekleşmeyen İşlemler
    bilgi5 = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah5 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi5 = models.FloatField(verbose_name = "Vergi",default = 0)  
    #Diğerleri, maddesinden önce VUK 322 Kapsamna Gren Borçlara At KDV
    bilgi6 = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah6 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi6 = models.FloatField(verbose_name = "Vergi",default = 0)  
    #Diğerleri
    bilgi7 = models.CharField(max_length = 200 ,verbose_name = "Açıklama" ,blank = True,null = True)
    matrah7 = models.FloatField(verbose_name = "Matrah",default = 0)
    vergi7 = models.FloatField(verbose_name = "Vergi",default = 0)  

#İSTEĞE BAĞLI TAM TEVKİFAT UYGULANAN İŞLEMLER
class matrah_bildirimi_istegebaglitamtevkifat(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    islem_turu = models.ForeignKey(tevkifat_tur_kodu, blank=True, null=True, on_delete=models.SET_NULL)
    matrah = models.FloatField(verbose_name = "Matrah",default = 0)
    kdv = models.FloatField(verbose_name = "KDV",default = 0)
    vergi = models.FloatField(verbose_name = "Vergi",default = 0)
#Matrah

#indirimler

class indirimler(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    #Önceki Dönemden Devreden Indrilecek KDV
    bilgi = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar = models.FloatField(verbose_name = "Tutar",default = 0)
    #Satış İade Edlen, İşlemi Gerçekleşmeyen veya Işleminden Vazgeçlen Mal ve Hizmetler Nedeniyle İndrimesi Gereken KDV
    bilgi1 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar1 = models.FloatField(verbose_name = "Tutar",default = 0)
    #Türkiye'de İkamet Etmeyen Yolculara Bu Dönemde Ödenen KDV (43 No.lu G.T.)
    bilgi2 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar2 = models.FloatField(verbose_name = "Tutar",default = 0)
    #İndirimli Orana Tabi İşlemlerle İlgili Yıl İçerisinde Mahsuben İadesi Gerçekleşmeyen KDV
    bilgi3 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar3 = models.FloatField(verbose_name = "Tutar",default = 0)
    #Kanunun (11/1-c) ve Geçici 17. Maddelerinden Doğan İadelerin İndiirm Yoluyla Telafisi Nedeniyle Indrilecek KDV
    bilgi4 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar4 = models.FloatField(verbose_name = "Tutar",default = 0)
    #Yurtiçi Alımlara İlişkin KDV
    bilgi5 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar5 = models.FloatField(verbose_name = "Tutar",default = 0)
    #Sorumlu Sifatıyla Beyan Edien KDV
    bilgi6 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar6 = models.FloatField(verbose_name = "Tutar",default = 0)
    #İthalde Ödenen KDV
    bilgi7 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar7 = models.FloatField(verbose_name = "Tutar",default = 0)
    #Değersiz Hale Gelen Alacaklara İlişkin İndrilecek KDV
    bilgi8 = models.CharField(max_length = 200,verbose_name = "Bilgi 1",blank = True,null = True)
    tutar8 = models.FloatField(verbose_name = "Tutar",default = 0)

#BU DÖNEME AİT İNDİRİLECEK KDV TUTARININ ORANLARA GÖRE DAĞILIMI
class indirim_bildirimi(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    kdvorani1 = models.FloatField(verbose_name = "Matrah",default = 0)
    kdvtutari1 = models.FloatField(verbose_name = "Vergi",default = 0)
    kdvorani2 = models.FloatField(verbose_name = "Matrah",default = 0)
    kdvtutari2 = models.FloatField(verbose_name = "Vergi",default = 0)
    kdvorani3 = models.FloatField(verbose_name = "Matrah",default = 0)
    kdvtutari3 = models.FloatField(verbose_name = "Vergi",default = 0)  
#ÖNCEKİ DÖNEME AİT MİKTARDA DEĞİŞİKLİK VARSA BU TABLO DOLDURULACAKTIR
class indirim_oncekidonem(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    indirimoncekidonem1 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama1 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar1 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem2 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama2 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar2 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem3 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama3 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar3 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem4 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama4 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar4 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem5 =models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama5 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar5 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem6 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama6 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar6 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem7 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama7 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar7 = models.FloatField(verbose_name = "Miktar",default = 0)
    indirimoncekidonem8 = models.CharField(max_length = 200,verbose_name = "Başlığı",blank = True,null  =True)
    aciklama8 = models.CharField(max_length = 400,verbose_name = "Açıklama",blank = True,null  =True)
    miktar8 = models.FloatField(verbose_name = "Miktar",default = 0)

##SONUÇ HESAPLARI
class sonuc_hesaplari(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    bagli_oldugu_beyanname = models.ForeignKey(kdv1_beyannamesi_bilgileri,blank=True,null=True,on_delete=models.SET_NULL)
    sonucyazisi1 =  models.CharField(max_length = 200,verbose_name = "sonuç yazısı",blank = True,null  =True)
    sonuc1 = models.FloatField(verbose_name = "sonuctutarı",default = 0)
    sonuc2 = models.FloatField(verbose_name = "sonuctutarı",default = 0)
    sonucyazisi2 =  models.CharField(max_length = 200,verbose_name = "sonuç yazısı",blank = True,null  =True)
    sonuc3 = models.FloatField(verbose_name = "sonuctutarı",default = 0)
    sonucyazisi3 =  models.CharField(max_length = 200,verbose_name = "sonuç yazısı",blank = True,null  =True)
    sonuc4 = models.FloatField(verbose_name = "sonuctutarı",default = 0)
    sonucyazisi4 =  models.CharField(max_length = 200,verbose_name = "sonuç yazısı",blank = True,null  =True)
#KDV1
