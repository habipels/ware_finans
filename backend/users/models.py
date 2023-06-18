from django.contrib.auth.models import AbstractUser
from django.db import models
import random
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