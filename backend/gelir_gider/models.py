from django.db import models
from users.models import firma
# Create your models here.
class gider(models.Model):
    detay_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır"),
    )
    doviz_cinsi_secim= (
        ("",""),
        ("TL","TL"),
        ("$","$"),
        ("£","£"),

    )
    ana_gider_kodu = models.CharField(max_length=100,verbose_name="Ana Gider Kodu",blank=True,null=True)
    gider_kodu = models.CharField(max_length=200,verbose_name="Gider Kodu",blank=True,null=True)
    birim = models.CharField(max_length=200,verbose_name="Birim",blank=True,null=True)
    detay = models.CharField(max_length=100,default="",choices=detay_secim,verbose_name="Detay",blank=True,null=True)
    borc_tutari = models.CharField(verbose_name="Borç Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    alacak_tutari = models.CharField(verbose_name="Alacak Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    bakiye_tutari = models.CharField(verbose_name="Bakiye Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi",blank=True,null=True,choices=doviz_cinsi_secim,default="")
    kdv_orani = models.CharField(max_length=100,verbose_name="KDV Oranı",blank=True,null=True)
    ozel_kod = models.CharField(verbose_name="Özel Kod",max_length=100,blank=True,null=True,default="")
    birim_fiyati = models.CharField(verbose_name="Birim Fiyatı",max_length=100,null=True,blank=True)
    birim_fiyati_doviz = models.CharField(verbose_name="Birim Fiyatı Döviz",max_length=100,null=True,blank=True)
    muh_kodu1 = models.CharField(verbose_name="Muh. Kodu 1",max_length=100,null=True,blank=True)
    muh_kodu2 = models.CharField(verbose_name="Muh. Kodu 2",max_length=100,null=True,blank=True)
    kdv_muh_kodu2 = models.CharField(verbose_name="KDV Muh. Kodu 2",max_length=100,null=True,blank=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)
class gelir(models.Model):
    detay_secim = (
        ("",""),
        ("Evet","Evet"),
        ("Hayır","Hayır"),
    )
    doviz_cinsi_secim= (
        ("",""),
        ("TL","TL"),
        ("$","$"),
        ("£","£"),

    )
    ana_gelir_kodu = models.CharField(max_length=100,verbose_name="Ana gelir Kodu",blank=True,null=True)
    gelir_kodu = models.CharField(max_length=200,verbose_name="gelir Kodu",blank=True,null=True)
    birim = models.CharField(max_length=200,verbose_name="Birim",blank=True,null=True)
    detay = models.CharField(max_length=100,default="",choices=detay_secim,verbose_name="Detay",blank=True,null=True)
    borc_tutari = models.CharField(verbose_name="Borç Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    alacak_tutari = models.CharField(verbose_name="Alacak Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    bakiye_tutari = models.CharField(verbose_name="Bakiye Tutarı (TL)",max_length=100,blank=True,null=True,default="0")
    doviz_cinsi = models.CharField(max_length=100,verbose_name="Döviz Cinsi",blank=True,null=True,choices=doviz_cinsi_secim,default="")
    kdv_orani = models.CharField(max_length=100,verbose_name="KDV Oranı",blank=True,null=True)
    ozel_kod = models.CharField(verbose_name="Özel Kod",max_length=100,blank=True,null=True,default="")
    birim_fiyati = models.CharField(verbose_name="Birim Fiyatı",max_length=100,null=True,blank=True)
    birim_fiyati_doviz = models.CharField(verbose_name="Birim Fiyatı Döviz",max_length=100,null=True,blank=True)
    muh_kodu1 = models.CharField(verbose_name="Muh. Kodu 1",max_length=100,null=True,blank=True)
    muh_kodu2 = models.CharField(verbose_name="Muh. Kodu 2",max_length=100,null=True,blank=True)
    kdv_muh_kodu2 = models.CharField(verbose_name="KDV Muh. Kodu 2",max_length=100,null=True,blank=True)
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True,null=True,on_delete=models.SET_NULL)