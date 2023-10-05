from django.db import models
from users.models import *
# Create your models here.
from datetime import datetime
from PIL import Image
from io import BytesIO
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
        ("",""),
        ("turklirasi","TL"),
        ("euro","£"),
        ("dolar","$")
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
    iliskili_kdv_hesap_kodu = models.ForeignKey('self',related_name ="iliskili_kdv_hesap_kodular",blank=True,null=True,verbose_name="İlişkili KDV Hesap Kodu",on_delete=models.CASCADE)
    kamumu_ozelmi = models.CharField(max_length=100,verbose_name="Kamu Mu Özel Mi ? 120 veya 320 ler",blank=True,null=True,choices=secme,default="")
    hesap_aciklamasi = models.CharField(max_length=200,verbose_name="Hesap Açıklaması",blank=True,null=True)
    grup_kodu = models.CharField(max_length=200,verbose_name="Grup Kodu",blank=True,null=True)
    ba_bslerde_kullanilsinmi = models.CharField(max_length=100,verbose_name="Ba/Bs lerde Kullanılsın mı ?",blank=True,null=True,choices=secme,default="")
    kur_farkinida_kullan = models.CharField(max_length=100,verbose_name="Kur Farkınıda Kullan ?",blank=True,null=True,choices=secme,default="")
    stopaj_hesap_kodu = models.ForeignKey('self',related_name ="stopaj_hesap_kodular",blank=True,null=True,verbose_name="Stopaj Hesap Kodu",on_delete=models.CASCADE)
    stopaj_orani = models.BigIntegerField(verbose_name="Stopaj Oranı",default=0)
    stopaj_tur_kodu = models.CharField(max_length=200,verbose_name="Stopaj Tür Kodu",blank=True,null=True)
    stopaj_belge_turu = models.CharField(max_length=100,verbose_name="Stopaj Belge Türü",blank=True,null=True,choices=stopaj_belge_turu_secme,default="")
    tevkifat_hesap_kodu = models.ForeignKey('self',related_name ="tevkifat_hesap_kodular",blank=True,null=True,verbose_name="Tevkifat KDV Hesap Kodu",on_delete=models.CASCADE)
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
    borc_toplam = models.CharField(max_length=100, verbose_name="Borç Toplam", blank=True, null=True)
    alacak_toplam = models.CharField(max_length=100, verbose_name="Alacak Toplam", blank=True, null=True)
    bakiye_toplam = models.CharField(max_length=100, verbose_name="Bakiye Toplam", blank=True, null=True)
    bakiye_tipi = models.CharField(max_length=100, verbose_name="Bakiye Tipi", blank=True, null=True)
    borclu_alacakli = models.CharField(max_length=100, verbose_name="Borçlu Alacaklı", blank=True, null=True)
    miktarli = models.CharField(max_length=100, verbose_name="Miktarlı", blank=True, null=True, choices=secme, default="")
    stok_kodu = models.CharField(max_length=100, verbose_name="Stok Kodu", blank=True, null=True)
    kdv_orani = models.BigIntegerField(verbose_name="KDV Oranı", default=0)
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
        ("",""),
        ("TL","TL"),
        ("Euro","£"),
        ("Dolar","$")
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
        ("",""),
        ("TL","TL"),
        ("Euro","£"),
        ("Dolar","$")
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
        ("",""),
        ("TL","TL"),
        ("Euro","£"),
        ("Dolar","$")
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
        ("",""),
        ("TL","TL"),
        ("Euro","£"),
        ("Dolar","$")
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
        ("",""),
        ("TL","TL"),
        ("Euro","£"),
        ("Dolar","$")
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
        ("Ödeme Fişi","Ödeme Fişi"),
        ("Tahsilat Fişi","Tahsilat Fişi"),
        ("Maaş Ödemesi (Kasa)","Maaş Ödemesi (Kasa)"),
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
    cari_unvan = models.ForeignKey(cari_kartlar,blank=True,null=True,verbose_name="Cari Unvan Bilgisi",on_delete=models.SET_NULL)
    banka_bilgisi = models.ForeignKey(banka,blank=True,null=True,verbose_name="Banka Bilgisi",on_delete=models.SET_NULL)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False)


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
