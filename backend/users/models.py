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
    silinme_bilgisi = models.BooleanField(default=False)
class vergi_dairesi(models.Model):
    vergi_dairesi_adi = models.CharField(max_length=200,verbose_name="Vewrigi Dairesi")
    vergi_dairesi_kodu = models.CharField(max_length=100,verbose_name="Vergi Dairesi Kodu")

class sube(models.Model):
    defter_turu = (
        ("Genel Muhasebe","Genel Muhasebe"),
        ("İşletme Defteri","İşletme Defteri")
    )
    aylik_tutma = (
        ("Aylık","Aylık"),
        ("Üç Aylık","Üç Aylık")
    )
    aylik_tutma_poset = (
        ("Aylık","Aylık"),
        ("Üç Aylık","Üç Aylık"),
        ("Altı Aylık","Altı Aylık")
    )
    firma_defter_turu_tutma = (
        ("İşletme","İşletme"),
        ("Serbest Meslek Defteri","Serbest Meslek Defteri")
    )
    defter_mukelefiyet_turu_secme =(
        ("Gerçek Kişi","Gerçek Kişi"),
        ("Adi Ortaklık","Adi Ortaklık"),
        ("Kollektif Şirket","Kollektif Şirket"),
        ("Adi Komandit Şirket","Adi Komandit Şirket"),
        ("Eshamlı Komandit Şirket","Eshamlı Komandit Şirket"),
        ("Limited Şirket","Limited Şirket"),
        ("Anonim Şirket","Anonim Şirket"),
        ("Kooperatif","Kooperatif"),
        ("Yabancı Kişi","Yabancı Kişi"),
        ("Diğer","Diğer"),
        ("Apartman Yönetimi","Apartman Yönetimi"),
        ("Avukatlık Ortaklığı","Avukatlık Ortaklığı"),
        ("Basın","Basın"),
        ("Birlik Ve Üst Birlik","Birlik Ve Üst Birlik"),
        ("Dernek","Dernek"),
        ("İş Ortaklığı","İş Ortaklığı"),
        ("Sendika","Sendika"),
        ("Site Yönetimi","Site Yönetimi"),
        ("Siyasi Parti","Siyasi Parti"),
        ("Spor Klübü","Spor Klübü"),
        ("Vakıf","Vakıf"),
        ("Kamu İktisadi Teşebbüsü","Kamu İktisadi Teşebbüsü"),
        ("Belediye İktisadi Teşebbüsü","Belediye İktisadi Teşebbüsü"),
    )
    stok_envanter_bilgileri_secme = (
        ("FİFO","FİFO"),
        ("LİFO","LİFO"),
        ("Agirlikli Ortalama","Ağırlıklı Ortalama"),
        ("Basit Ortalama","Basit Ortalama"),
        ("Hareketli Agirlikli Ortalama","Hareketli Ağırlıklı Ortalama"),
        ("Her Kartın Kendi Yöntemine Göre","Her Kartın Kendi Yöntemine Göre")
    )
    bagli_oldugu_firma = models.ForeignKey(firma,blank=True, null=True,on_delete=models.SET_NULL)
    sube_adi = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Adı")
    sube_unvani = models.CharField(max_length=100,verbose_name="Şube Unvanı")
    adres_bilgisi = models.ForeignKey(adresler,blank=True, null=True,on_delete=models.SET_NULL)
    vergi_dairesi_adi = models.ForeignKey(vergi_dairesi,blank=True, null=True,on_delete=models.SET_NULL)
    vergi_dairesi_kodu = models.CharField(max_length=100,blank=True, null=True,verbose_name="Vergi Dairesi Kodu")
    vergi_numarasi = models.CharField(max_length=100 ,blank=True, null=True,verbose_name="Vergi Numarası")
    sahis_ise_tc = models.CharField(max_length=20,blank=True, null=True,verbose_name="Şahis İse Tc Kimlik Numarası")
    email_adresi = models.EmailField(max_length=100,blank=True, null=True,verbose_name="Şube Email Adresi ")
    web_adresi = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Web Adresi ")
    telefon_numarasi = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Telefon Numarası ")
    sube_defter_turu = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Defter Türü ",choices=defter_turu,default="Genel Muhasebe")
    kdv1 = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube KDV1",choices=aylik_tutma,default="Aylık")
    kdv2 = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube KDV2",choices=aylik_tutma,default="Aylık")
    turizm = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Turizm",choices=aylik_tutma,default="Aylık")
    muhsgk = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube MuhSGK",choices=aylik_tutma,default="Aylık")
    poset = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Poşet",choices=aylik_tutma_poset,default="Aylık")
    firma_defter_turu = models.CharField(max_length=100,blank=True, null=True,verbose_name="Firma Defter Türü ",choices=firma_defter_turu_tutma,default="İşletme")
    mukellefiyet_turu = models.CharField(max_length=100,blank=True, null=True,verbose_name="Mükellefiyet Türü ",choices=defter_mukelefiyet_turu_secme,default="Gerçek Kişi")
    stok_bilgisi = models.CharField(max_length=100,blank=True, null=True,verbose_name="Stok Envanter Bilgileri",choices=stok_envanter_bilgileri_secme,default="FİFO")
    gecici_vergi_orani = models.BigIntegerField(blank=True, null=True,verbose_name="Geçici Vergi Oranı %")
    silinme_bilgisi = models.BooleanField(default=False)
class kategory_link_ayari(models.CharField):
    def __init__(self, *args, **kwargs):
        super(kategory_link_ayari, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).lower().replace(" ","_")

class user_adi(models.CharField):
    def __init__(self, *args, **kwargs):
        super(user_adi, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).upper()
class İller_ve_ilceler(models.Model):
    kategory_tr = user_adi(verbose_name="İl veya İlçe ",max_length=100)
    ust_kategory = models.ForeignKey('self',blank=True,null=True,verbose_name="İlçe İse İli Şecin",related_name='children',on_delete=models.CASCADE)
    link = kategory_link_ayari(max_length=200)
    keywords = models.CharField(max_length=255)
    def __str__(self):
        full_path = [self.kategory_tr]                  # post.  use __unicode__ in place of
        k = self.ust_kategory
        while k is not None:
            full_path.append(k.kategory_tr)
            k = k.ust_kategory
        return ' --> '.join(full_path[::-1])
        
class ortak_bilgileri(models.Model):
    unvan_secim = (
        ("işveren","işveren"),
        ("Yönetici","Yönetici"),
        ("Ortak","Ortak"),
        ("İşveren Vekil","İşveren Vekil")

    )
    vekil_ortak_secim = (
        ("Ortak","Ortak"),
        ("İşveren Vekil","İşveren Vekil")
    )
    
    firma_bilgisi = models.ForeignKey(firma,on_delete=models.SET_NULL,blank=True,null=True,verbose_name="Firma Bilgisi")
    unvan = models.CharField(max_length=100,null=True,blank=True,choices=unvan_secim,default="işveren",verbose_name="Unvan Bilgisi")
    vekil_ortak= models.CharField(max_length=100,null=True,blank=True,choices=vekil_ortak_secim,default="Ortak",verbose_name="vekil Ortaklık Bilgisi")
    ortaklik_giris_tarihi = models.DateField(null=True,blank=True,verbose_name="Ortaklık Giriş Tarihi")
    ortakliktan_cikis_tarihi = models.DateField(null=True,blank=True,verbose_name="Ortaklıktan Çıkış Tarihi")
    goreve_baslama_tarihi = models.DateField(null=True,blank=True,verbose_name="Göreve Başlama Tarihi")
    gorevi_bitirme_tarihi = models.DateField(null=True,blank=True,verbose_name="Görevi Bitirme Tarihi")
    hisse_orani = models.BigIntegerField(null=True,blank=True,verbose_name="Hisse Oranı")
    hisse_tutari = models.BigIntegerField(null=True,blank=True,verbose_name="Hisse Tutarı")
    ticaret_sicil_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Ticaret Sicil No")
    ticaret_sicil_gazetesi_tarihi = models.DateField(null=True,blank=True,verbose_name="Ticaret Sicil Gazetesi Tarihi")
    ticaret_sicil_gazetesi_sayfa_n = models.BigIntegerField(null=True,blank=True,verbose_name="Ticaret Sicil Gazetesi Sayfa No")
    vergi_dairesi_adi = models.ForeignKey(vergi_dairesi,blank=True, null=True,on_delete=models.SET_NULL)
    vergi_dairesi_kodu = models.CharField(max_length=100,blank=True, null=True,verbose_name="Vergi Dairesi Kodu")
    vergi_numarasi = models.CharField(max_length=100 ,blank=True, null=True,verbose_name="Vergi Numarası")
    vergi_dairesi_ili_ilcesi = models.ForeignKey(İller_ve_ilceler,on_delete=models.SET_NULL,blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
class ortak_is_bilgileri(models.Model):
    tutugu_defter_turu_sec =(
        ("",""),
        ("Bilanço","Bilanço"),
        ("Diğer Defter","Diğer Defter"),
        ("Deftere Tabi Değil","Deftere Tabi Değil")
    )
    ortak_bilgileri = models.ForeignKey(ortak_bilgileri,on_delete=models.CASCADE)
    bagkur_no = models.CharField(max_length=100,verbose_name="Bağkur Numarası")
    bagkur_basamagi= models.CharField(max_length=100,verbose_name="Bağkur Başamağı")
    ssk_no= models.CharField(max_length=100,verbose_name="SSK NO")
    emekli_sandigi_no = models.CharField(max_length=100,verbose_name="Emekli Sandığı No")
    diger_isyeri_tescil_no = models.CharField(max_length=100,verbose_name="Diğer İşyeri Tescil No")
    vakif_no = models.CharField(max_length=100,verbose_name="Vakıf No")
    dernek_no = models.CharField(max_length=100,verbose_name="Dernek No")
    tutugu_defter_turu = models.CharField(max_length=100,verbose_name="Tutuğu Defter Türü",choices=tutugu_defter_turu_sec,default="")