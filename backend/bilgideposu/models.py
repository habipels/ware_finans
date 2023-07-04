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
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi",blank=True,null=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)

class banka_yetkilisi(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    adi_soyadi = models.CharField(max_length=200,verbose_name="Banka Yetkilisi Adı Soyadı ",blank=True, null=True)
    gorevi = models.CharField(max_length=200,verbose_name="Görevi",blank=True,null=True)
    istelefonu = models.CharField(max_length=20,verbose_name="İş Telefonu",blank=True,null=True)
    dahili_numara = models.CharField(max_length=100,verbose_name="Dahili Numara",blank=True,null=True)
    gsm = models.CharField(max_length=100,verbose_name="GSM",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama")
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
    silinme_bilgisi = models.BooleanField(default=False)
