from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import json
# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('muhasebeci', 'muhasebeci'),
        ('sirket', 'sirket'),
        ('admin1', 'admin1'),
        ('admin2', 'admin2'),
        ('admin3', 'admin3'),
    )
    kullanicilar_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    hesap_turu = models.CharField(max_length=100, choices=STATUS, default='muhasebeci')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    email_dogrulama = models.BooleanField(default= False)
    #hesap_kayit_tarihi = models.DateTimeField(auto_now_add=True,verbose_name= "Hesap Oluşturulma Tarihi")
    Referans_kodu =  models.CharField(max_length=100,null=True)
    referans_olan_kod = models.CharField(max_length=100,null=True,blank=True)
    smmmok  = models.FileField(upload_to='companylogo/',blank = True,null = True,verbose_name="Şirket Logosu")
    firma_adi = models.CharField(max_length=100 ,verbose_name= "Firma Adı")
    #random.randint(1, 9999999).__str__()+"ID"+ str(self.id)
    telefon_no = models.CharField(max_length=20,verbose_name="Telefon Numarası")
    kullanici_silme_bilgisi = models.BooleanField(default= False)
    lisans_bitis_tarih = models.DateField(null=True,verbose_name="Lisans Bitiş Tarihi",blank = True)
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if self.id:
            self.yeni = random.randint(1, 9999999).__str__() + "ID" + str(self.id)
            self.Referans_kodu = self.yeni
            super(CustomUser, self).save(*args, **kwargs)


class firma(models.Model):
    firma_muhasabecisi = models.ForeignKey(CustomUser,blank=True, null=True,on_delete=models.SET_NULL)
    tanitici_isim = models.CharField(max_length=100,verbose_name="Tanıtıcı Adı",blank=True,null=True)
    firma_unvani = models.CharField(max_length=100,verbose_name="Firma Unvanı (ADI)")
    Firma_unvani2 = models.CharField(max_length=100,verbose_name="Firma Unvanı (Soyadı)")
    silinme_bilgisi = models.BooleanField(default=False)



class adresler(models.Model):
    data = (
    ("istanbul","istanbul"),
    ('Van','Van'),
    ("Ankara","Ankara")
    ,("Batman","Batman"),
    ("Mersin","Mersin")
)
    adres = models.CharField(blank = True,null = True,max_length=200,verbose_name="Adres")
    mahhalle_koy = models.CharField(blank = True,null = True,max_length=100,verbose_name="Mahalle Köy")
    bulvar = models.CharField(blank = True,null = True,max_length=100,verbose_name="Bulvar")
    cadde = models.CharField(blank = True,null = True,max_length=100,verbose_name="Cadde")
    sokak = models.CharField(blank = True,null = True,max_length=100,verbose_name="Sokak")
    adaparselno = models.CharField(blank = True,null = True,max_length=100,verbose_name="ADA Parsel No")
    diskapino  = models.CharField(blank = True,null = True,max_length=10,verbose_name="Dış Kapı No")
    ickapino = models.CharField(blank = True,null = True,max_length=10,verbose_name="İç Kapı No")
    posta_kodu = models.CharField(blank = True,null = True,max_length=100,verbose_name="Posta Kodu")
    semt = models.CharField(blank = True,null = True,max_length=100,verbose_name="Semt")
    ilce = models.CharField(blank = True,null = True,max_length=100,verbose_name="İlçe")
    il = models.CharField(blank = True,null = True,max_length = 50 ,verbose_name="İl",default="Van",choices= data)
class vergi_dairesi(models.Model):
    vergi_dairesi_adi = models.CharField(max_length=200,verbose_name="Vewrigi Dairesi")
    vergi_dairesi_kodu = models.CharField(max_length=100,verbose_name="Vergi Dairesi Kodu")

class sube(models.Model):
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True, null=True,on_delete=models.SET_NULL)
    sube_adi = models.CharField(max_length=100,verbose_name="Şube Adı")
    sube_unvani = models.CharField(max_length=100,verbose_name="Şube Unvanı")
    adres_bilgisi = models.ForeignKey(adresler,blank=True, null=True,on_delete=models.SET_NULL)