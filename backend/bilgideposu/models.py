from django.db import models
from users.models import *
# Create your models here.

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
    iban_numarasi = models.CharField(max_length=20,verbose_name="İban Numarası",blank=True,null=True)
    kullanabilir_kredi_tutari = models.CharField(max_length=200,verbose_name="Kullanabilir kredi Tutarı",null=True,blank=True)
    ozel_kod = models.CharField(max_length=100,verbose_name="Özel Kod",blank=True,null=True)
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi", choices=doviz,default="",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    toplam_yatirilan = models.CharField(max_length=100,verbose_name="Toplam Yatırılan",blank=True,null=True)
    toplam_cekilen = models.CharField(max_length=100,verbose_name="Toplam Çekilen",blank=True,null=True)
    toplam_bakiye = models.CharField(max_length=100,verbose_name="Bakiye",blank=True,null=True)
    muh_kodu = models.CharField(max_length=100,verbose_name="Muh Kodu",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
class banka_yetkilisi(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    adi_soyadi = models.CharField(max_length=200,verbose_name="Banka Yetkilisi Adı Soyadı ",blank=True, null=True)
    gorevi = models.CharField(max_length=200,verbose_name="Görevi",blank=True,null=True)
    istelefonu = models.CharField(max_length=20,verbose_name="İş Telefonu",blank=True,null=True)
    dahili_numara = models.CharField(max_length=100,verbose_name="Dahili Numara",blank=True,null=True)
    gsm = models.CharField(max_length=100,verbose_name="GSM",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)
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
        ("turklirasi","TL"),
        ("euro","£"),
        ("dolar","$")
    )
    kasa_kodu = models.CharField(max_length=100,verbose_name="Kasa Kodu",blank=True,null=True)
    entkodu = models.CharField(max_length=10,choices=entkodu_secim,verbose_name="Ent Kodu",default="",blank=True,null=True)
    kasa_adi = models.CharField(max_length=200,verbose_name="kasa Adı",blank=True,null=True)
    ozel_kod = models.CharField(max_length=100,verbose_name="Özel Kod",blank=True,null=True)
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi", choices=doviz,default="",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
    toplam_tahsilat = models.CharField(max_length=100,verbose_name="Toplam Tahsilat",blank=True,null=True)
    toplam_odeme = models.CharField(max_length=100,verbose_name="Toplam Ödeme",blank=True,null=True)
    toplam_bakiye = models.CharField(max_length=100,verbose_name="Bakiye",blank=True,null=True)
    muh_kodu = models.CharField(max_length=100,verbose_name="Muh Kodu",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama",blank=True, null=True)