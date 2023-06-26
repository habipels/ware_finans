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
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True, null=True,on_delete=models.SET_NULL)

class banka_yetkilisi(models.Model):
    banka_bilgisi = models.ForeignKey(banka,blank=True, null=True,on_delete=models.SET_NULL)
    adi_soyadi = models.CharField(max_length=200,verbose_name="Banka Yetkilisi Adı Soyadı ",blank=True, null=True)
    gorevi = models.CharField(max_length=200,verbose_name="Görevi",blank=True,null=True)
    istelefonu = models.CharField(max_length=20,verbose_name="İş Telefonu",blank=True,null=True)
    dahili_numara = models.CharField(max_length=100,verbose_name="Dahili Numara",blank=True,null=True)
    gsm = models.CharField(max_length=100,verbose_name="GSM",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Açıklama")