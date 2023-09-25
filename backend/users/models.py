from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import json
import datetime
from django.utils import timezone
# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('muhasebeci', 'muhasebeci'),
        ('sirket', 'sirket'),
        ('admin1', 'admin1'),
        ('admin2', 'admin2'),
        ('admin3', 'admin3'),
    )
    abonelik_turu = (
        ("0","0"),
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
    )
    kullanicilar_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    hesap_turu = models.CharField(max_length=100, choices=STATUS, default='muhasebeci')
    abonelik_tur = models.CharField(max_length=100, choices=abonelik_turu, default='0')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    email_dogrulama = models.BooleanField(default= False)
    #hesap_kayit_tarihi = models.DateTimeField(default=datetime.datetime.now,null=True,blank=True)
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
    firma_muhasabecisi = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    tanitici_isim = models.CharField(max_length=100, verbose_name="Tanıtıcı Adı", blank=True, null=True)
    firma_unvani = models.CharField(max_length=100, verbose_name="Firma Unvanı (ADI)")
    Firma_unvani2 = models.CharField(max_length=100, verbose_name="Firma Unvanı (Soyadı)")
    silinme_bilgisi = models.BooleanField(default=False)
    firma_ozel_anahtar = models.CharField(max_length=200, verbose_name="Firma Özel Anahtar", null=True, blank=True)

    def save(self, *args, **kwargs):
        
            # Eğer nesne henüz kaydedilmediyse (yeni bir nesne), firma_ozel_anahtar oluşturun.
        self.yeni = random.randint(1, 9999999).__str__() + "ID" + random.randint(1, 9999999).__str__()
        self.firma_ozel_anahtar = self.yeni
        super(firma, self).save(*args, **kwargs)

class adresler(models.Model):
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
    il = models.CharField(blank = True,null = True,max_length = 50 ,verbose_name="İl")
    silinme_bilgisi = models.BooleanField(default=False)
class vergi_dairesi(models.Model):
    il = models.CharField(max_length=100,verbose_name="İL")
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
    bagkur_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Bağkur Numarası")
    bagkur_basamagi= models.CharField(max_length=100,null=True,blank=True,verbose_name="Bağkur Başamağı")
    ssk_no= models.CharField(max_length=100,null=True,blank=True,verbose_name="SSK NO")
    emekli_sandigi_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Emekli Sandığı No")
    diger_isyeri_tescil_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Diğer İşyeri Tescil No")
    vakif_no = models.CharField(max_length=100,verbose_name="Vakıf No",null=True,blank=True)
    dernek_no = models.CharField(max_length=100,verbose_name="Dernek No",null=True,blank=True)
    tutugu_defter_turu = models.CharField(max_length=100,verbose_name="Tutuğu Defter Türü",choices=tutugu_defter_turu_sec,default="")
    meslegi = models.CharField(max_length=100,verbose_name="Mesleği",null=True,blank=True)
    faliyet_kodu = models.CharField(max_length=100,verbose_name="Faliyet Kodu",null=True,blank=True)
    faliyet_suresi = models.CharField(max_length=100,verbose_name="Faliyet Süresi",null=True,blank=True)
    meslek_tesekkul_adi = models.CharField(max_length=100,verbose_name="Meslek Teşekkül Adı",null=True,blank=True)
    mesleki_tesekkulno = models.CharField(max_length=100,verbose_name="Meslek Teşekkül No",null=True,blank=True)
    arac_plaka_no1 = models.CharField(max_length=100,verbose_name="Araç Plaka No 1",null=True,blank=True)
    arac_plaka_no2 = models.CharField(max_length=100,verbose_name="Araç Plaka No 2",null=True,blank=True)
    arac_plaka_no3 = models.CharField(max_length=100,verbose_name="Araç Plaka No 3",null=True,blank=True)
    adress = models.ForeignKey(adresler,on_delete=models.SET_NULL,blank=True,null=True)
    isyeri_adrsi = models.CharField(max_length=200,verbose_name="İşyeri Adresi",null=True,blank=True)
    il_ilce = models.ForeignKey(İller_ve_ilceler,on_delete=models.SET_NULL,blank=True,null=True)
    isyeri_postakodu= models.CharField(max_length=200,verbose_name="İşyeri Posta Kodu",null=True,blank=True)
    istelefonu= models.CharField(max_length=20,verbose_name="İş Telefon Numarası",null=True,blank=True)
    istelefonu2= models.CharField(max_length=20,verbose_name="İş Telefon Numarası 2",null=True,blank=True)
    evtelefon= models.CharField(max_length=20,verbose_name="Ev Telefon Numarası ",null=True,blank=True)
    ceptelefon1 = models.CharField(max_length=20,verbose_name="Cep Telefon Numarası ",null=True,blank=True)
    ceptelefon2 = models.CharField(max_length=20,verbose_name="Cep Telefon Numarası 2",null=True,blank=True)
    fax =  models.CharField(max_length=100,verbose_name="Fax Adresi",null=True,blank=True)
    eposta = models.EmailField(max_length=100,verbose_name="Email Adresi",null=True,blank=True)
    web_adrsi = models.CharField(max_length=100,verbose_name="Web Adresi",null=True,blank=True)

class ortak_kimlik_bilgileri(models.Model):
    cinsiyet_secim = (
        ("",""),
        ("Erkek","Erkek"),
        ("Kadın","Kadın")
    )
    medeni_hali_secim =(
        ("",""),
        ("Evli","Evli"),
        ("Bekar","Bekar")
    )
    uyruk_secim=(
        ("",""),
        ("T.C","T.C"),
        ("Yabancı","Yabancı")
    )
    ortak_bilgileri = models.ForeignKey(ortak_bilgileri,on_delete=models.CASCADE)
    adi_soyadi = models.CharField(max_length=100,verbose_name="Adı Soyadı")
    tckimlik = models.CharField(max_length=12,verbose_name="T.C Kimlik No",blank=True,null=True)
    kimlik_seri= models.CharField(max_length=20,verbose_name="T.C Kimlik Seri No",blank=True,null=True)
    kimlik_no= models.CharField(max_length=100,verbose_name="Kimlik No",blank=True,null=True)
    baba_adi =  models.CharField(max_length=100,verbose_name="Baba Adı",null=True,blank=True)
    anne_adi =  models.CharField(max_length=100,verbose_name="Anne Adı",null=True,blank=True)
    dogum_yeri = models.CharField(max_length=100,verbose_name="Doğum Yeri",null=True,blank=True)
    dogum_tarihi = models.DateField(null=True,blank=True,verbose_name="Doğum Tarihi")
    cinsiyet = models.CharField(verbose_name="Cinsiyet",max_length=100,choices=cinsiyet_secim,default="")
    anne_kizlık_soyadi =models.CharField(max_length=100,verbose_name="Anne Kızlık Soyadı",null=True,blank=True)
    medeni_hali = models.CharField(verbose_name="Medeni Hali",max_length=100,choices=medeni_hali_secim,default="")
    evlilik_tarihi = models.DateField(verbose_name="Evlilik Tarihi",blank=True,null=True)
    onceki_soyadi = models.CharField(max_length=100,verbose_name="Önceki Soyadı",blank=True,null=True)
    uyruğu_yabanci_ise_ulkesi = models.CharField(max_length=100,verbose_name="Uyruğu Yabancı İse Ülkesi",null=True,blank=True)
    kan_grubu = models.CharField(max_length=5,verbose_name="Kan Grubu",blank=True,null=True)
    nufusa_kayitli_il_ilce = models.ForeignKey(İller_ve_ilceler,on_delete=models.SET_NULL,verbose_name="Nufusa KAyıtlı Olduğu İl İlçe",blank=True,null=True)
    nufusa_kayitli_koy_mahhalle = models.CharField(max_length=200,verbose_name="Nufusa Kayıtlı Olduğu Köy Mahalle",blank=True,null=True)
    cilt_no = models.CharField(max_length=50,verbose_name="Cilt NO",blank=True,null=True)
    aile_sira_no = models.CharField(max_length=50,verbose_name="Aile Sıra NO",blank=True,null=True)
    sira_no = models.CharField(max_length=50,verbose_name="Sıra NO",blank=True,null=True)
    sayfa_no = models.CharField(max_length=50,verbose_name="Sayfa NO",blank=True,null=True)
    cuzdanin_verildiği_yer= models.CharField(max_length=100,verbose_name="Cüzdanın Verildiği Yer",blank=True,null=True)
    verilis_nedeni = models.CharField(max_length=100,verbose_name="Nufus Cüzdanı Veriliş Nedeni",blank=True,null=True)
    cuzdan_kayit_no = models.CharField(max_length=50,verbose_name="Cüzdan Kayıt No",blank=True,null=True)
    cuzdan_verilis_tarihi = models.DateField(null=True,blank=True,verbose_name="Cüzdan Veriliş Tarihi")

class faliyet_bilgisi(models.Model):
    tehlike_secimi = (
        ("",""),
        ("Tehlikeli","Tehlikeli"),
        ("Çok Tehlikeli","Çok Tehlikeli"),
        ("Az Tehlikeli","Az Tehlikeli")
    )
    faliyet_kodu = models.BigIntegerField(verbose_name="Faliyet Kodu")
    faliyet_adi = models.CharField(max_length=200,verbose_name="Faliyet Adı")
    tehlike = models.CharField(max_length=100,verbose_name="Tehlike Sınıfı",choices=tehlike_secimi,default="")
class calisma_sosyal_guvenlik_is_kollari(models.Model):
    kod_baslik = models.CharField(max_length=200,verbose_name="Çalışma ve Sosyal Güvenlik iş Kolu ve Kodu")
class sube_faliyet_bilgileri(models.Model):
    faliyet_niteligi_secimi = (
        ("",""),
        ("Devamlı","Devamlı"),
        ("Mevsimlik","Mevsimlik"),
        ("Geçici","Geçici"),
        ("Diğer","Diğer")
    )
    tabi_oldugu_sektor_secim = (
        ("",""),
        ("Şirket Türü","Şirket Türü"),
        ("Dernek","Dernek"),
        ("Vakıf","Vakıf"),
        ("Sendika","Sendika"),
        ("Apartman Yönetimi","Apartman Yönetimi"),
        ("Siyasi Parti","Siyasi Parti"),
        ("Spor Klüpleri","Spor Klüpleri"),
        ("Basın","Basın"),
        ("Diğer","Diğer")
    )

    isyeri_turu_secim = (
        ("",""),
        ("Merkez","Merkez"),
        ("Mükellefyetsiz Şube","Mükellefyetsiz Şube"),
        
    )
    isyeri_mulkiyet_secim = (
        ("",""),
        ("Kira","Kira"),
        ("Mal Sahibi","Mal Sahibi"),
        ("Diğer","Diğer")
    )
    sube_bilgisi = models.ForeignKey(sube,blank=True, null=True,on_delete=models.CASCADE)
    kurulus_tarihi = models.DateField(verbose_name="Kuruluş Tarihi")
    terk_tarihi = models.DateField(verbose_name="Terk Tarihi")
    faliyet_nace_kodu = models.ForeignKey(faliyet_bilgisi,blank=True, null=True,on_delete=models.SET_NULL)
    faliyet_niteligi = models.CharField(max_length=100,verbose_name="Faliyet Niteliği",choices=faliyet_niteligi_secimi,default="")
    tabi_oldugu_sektor = models.CharField(max_length=200,verbose_name="Tabi Olduğu Sektör",choices=tabi_oldugu_sektor_secim,default="")
    yapilan_is_niteligi = models.CharField(max_length=200,verbose_name="Yapılan İş Niteliği",blank=True, null=True)
    calisma_ve_sosyal_is_kolu = models.ForeignKey(calisma_sosyal_guvenlik_is_kollari,blank=True,null=True,verbose_name="Çalişma Ve Sosya Güvenlik İş Kolu",on_delete=models.SET_NULL)
    sahis_ise_ticaret_unvani = models.CharField(max_length=200,verbose_name="Şahıs İse Ticaret Ünvanı",blank=True,null=True)
    ticaret_sicil_gazete = models.DateField(verbose_name="Ticaret Sicil Gazetesi Tarihi")
    ticaret_sicil_gazete_sayfa_no = models.CharField(verbose_name="Ticaret Sicil Gazete Sayfa No",max_length=100,null=True,blank=True)
    ticaret_sicil_gazete_no = models.CharField(verbose_name="Ticaret Sicil Gazete No",max_length=100,null=True,blank=True)
    meslek_tesekkul_adi = models.CharField(verbose_name="Meslek Teşekkül Adı",max_length=100,null=True,blank=True)
    meslek_tesekkul_no = models.CharField(verbose_name="Meslek Teşekkül No",max_length=100,null=True,blank=True)
    adres_no = models.CharField(verbose_name="Adres No",max_length=100,null=True,blank=True)
    taahut_edilen_sermaye = models.CharField(verbose_name="Taahüt Edilen Sermaye",max_length=100,null=True,blank=True)
    odenen_sermaye = models.CharField(verbose_name="Ödenen Sermaye",max_length=100,null=True,blank=True)
    e_posta_adresi2 = models.EmailField(max_length=200,verbose_name="Email Adresi 2",null=True,blank=True)
    kayitli_oldugu_il = models.CharField(max_length=100,verbose_name="Kayıtlı Olduğu İl",blank=True,null=True)
    ticaret_sicil_no = models.CharField(verbose_name="Ticaret Sicil No",max_length=100,null=True,blank=True)
    mersis_no = models.CharField(verbose_name="Mersis No",max_length=100,null=True,blank=True)
    isyeri_turu = models.CharField(max_length=200,verbose_name="İşyeri Türü",choices=isyeri_turu_secim,default="")
    isyeri_kodu = models.CharField(max_length=200,verbose_name="İşyeri Kodu",blank=True,null=True)
    isyeri_mulkiyet = models.CharField(max_length=200,verbose_name="İşyeri Mülkiyet",choices=isyeri_mulkiyet_secim,default="")
    vergi_dairesi_adi = models.ForeignKey(vergi_dairesi,verbose_name="KDV1 KDV2 Beyanname Vergi Dairesi",blank=True, null=True,on_delete=models.SET_NULL)
    yetkili_adi_soyadi = models.CharField(max_length=200,null=True,blank=True,verbose_name="Yetkili Adı Soyadı")
    yetkili_tckimlikno = models.CharField(max_length=11,null=True,blank=True,verbose_name="Yetkili T.C. Kimlik No")
    vergi_kimlikno = models.CharField(max_length=100,null=True,blank=True,verbose_name="Vergi Kimlik No")
    oda_sicil_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Bağlı Olduğu Oda Sicil No")
    cevre_temizlik_vergi_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Çevre Temizlik Vergi No")
    beldye_ilan_reklam_vergi_no = models.CharField(max_length=100,null=True,blank=True,verbose_name="Beledye İlan Reklam Vergi No")


class ihale_bilgileri(models.Model):
    bildirge_imzalayan = (
        ("",""),
        ("İşveren","İşveren"),
        ("İşveren Vekili","İşveren Vekili")
    )
    isverentip = (
        ("",""),
        ("Asıl İşveren","Asıl İşveren"),
        ("Alt Yüklenici","Alt Yüklenici")
    )
    sube_bilgisi = models.ForeignKey(sube,blank=True, null=True,on_delete=models.CASCADE)
    ihalekonusundaihaleyapanmakam = models.CharField(max_length=200,verbose_name="İhale Konusunda İhaleyi Yapan Makam",blank=True,null=True)
    isyeri_bildirgersi_imzalayan = models.CharField(max_length=100,verbose_name="İşyeri Bildirgesi İmzalayan",choices=bildirge_imzalayan,default="")
    ihalekonusundaihaleyapanmakamadresi = models.CharField(max_length=200,verbose_name="İhale Konusunda İhaleyi Yapan Makam Adresi",blank=True,null=True)
    isveren_tipi = models.CharField(max_length=100,verbose_name="İşveren Tipi",choices=bildirge_imzalayan,default="")

class taseronbilgileri(models.Model):
    sube_bilgisi = models.ForeignKey(sube,blank=True, null=True,on_delete=models.CASCADE)
    adres_bilgisi = models.ForeignKey(adresler,blank=True, null=True,on_delete=models.SET_NULL)
    taseronunvanbilgisi = models.CharField(max_length=100 ,blank=True, null=True,verbose_name="Taşeron Unvan Bilgisi")
    vergi_numarasi = models.CharField(max_length=100 ,blank=True, null=True,verbose_name="Vergi Numarası")
    sahis_tc = models.CharField(max_length=20,blank=True, null=True,verbose_name="Şahis Tc Kimlik Numarası")
    email_adresi = models.EmailField(max_length=100,blank=True, null=True,verbose_name="Şube Email Adresi ")
    telefon_numarasi = models.CharField(max_length=100,blank=True, null=True,verbose_name="Şube Telefon Numarası ")

class kurumlar_dar_mukkelef_kimlik_ve_adres_bilgisi(models.Model):
    sube_bilgisi = models.ForeignKey(sube,blank=True, null=True,on_delete=models.CASCADE)
    kurumlarvergiveyatckimlikno = models.CharField(max_length=100,verbose_name="Kurumlar Vergi , Tc Kimlikl NO",blank=True,null=True)
    kurumlarvergikimlikno = models.CharField(max_length=100,verbose_name="Kurumlar Vergi Nosu",blank=True,null=True)
    kurumlarsoyadiunvan = models.CharField(max_length=200,verbose_name="Kurumlar Soyadı Unvan",blank=True,null=True)
    kurumlaradiunvan = models.CharField(max_length=200,verbose_name="Kurumlar ADı Unvan",blank=True,null=True)
    kurumlarticaretsicilno = models.CharField(max_length=200,verbose_name="Kurumlar Ticaret Sicil No",blank=True,null=True)
    Kurumlarepostaadresi = models.EmailField(max_length=200,verbose_name="eposta Adresi",blank=True,null=True)
    kurumlarirtibatnumarasi = models.CharField(max_length=11,verbose_name="Kurumlar İrtibart Numarası",blank=True,null=True)
    kurumlarsube = models.CharField(max_length=200,verbose_name="Kurumlar Bağlı Şube",blank=True,null=True)
    cikisyeri =  models.CharField(max_length=200,verbose_name="Kurumlar Çıkış Yeri",blank=True,null=True)
    kurumlarajanlik = models.CharField(max_length=200,verbose_name="Kurumlar Ajanlık",blank=True,null=True)
    kurmlarimalatyeri = models.CharField(max_length=200,verbose_name="Kurumlar İmalat Yeri",blank=True,null=True)
    kurumlarsatisyeri = models.CharField(max_length=200,verbose_name="Kurumlar Satış Yeri",blank=True,null=True)
    kurumlarsair = models.CharField(max_length=200,verbose_name="Kurumlar Sair",blank=True,null=True)
    kurumlartoplam = models.CharField(max_length=200,verbose_name="Kurumlar Toplam",blank=True,null=True)
class beyanname_bilgileri(models.Model):
    beyannamehangisifatlaverildi_secim =(
        ("",""),
        ("mukellef","Mükellef"),
        ("mirascı","Miradscı"),
        ("kanunitemsilci","Kanuni Temsilci")
    )
    sube_bilgisi = models.ForeignKey(sube,blank=True, null=True,on_delete=models.CASCADE)
    beyannamehangisifatlaverildi  = models.CharField(max_length=100,choices=beyannamehangisifatlaverildi_secim,default="",verbose_name="Beyanname Hangi Sıfatla Verildiği",blank=True,null=True)
    mirascibilgisitc = models.CharField(max_length=100,verbose_name="Mirasci Tc Kimlik No",blank=True,null=True)
    mirascivergino  = models.CharField(max_length=100,verbose_name="Mirascı Vergi No",blank=True,null=True)
    beyannamesoyadiunvan = models.CharField(max_length=100,verbose_name="Soyadı Unvan",blank=True,null=True)
    beyannameadiunvandevami = models.CharField(max_length=100,verbose_name="Adı Unvan (devamı)",blank=True,null=True)
    beyannameyeaitticaretsicilno = models.CharField(max_length=100,verbose_name="Ticaret Sicil No",blank=True,null=True)
    beyannameemailadresi = models.EmailField(max_length=100,verbose_name="Email Adresi",blank=True,null=True)
    beyannametelefonumarasi = models.CharField(max_length=100,verbose_name="Telefon Numarası",blank=True,null=True)
class beyanname_kanuni_temsilcisi(models.Model):
    beyanname_bilgisi = models.ForeignKey(beyanname_bilgileri,blank=True, null=True,on_delete=models.CASCADE)
    beyannamekanunitemsicitc = models.CharField(max_length=15,verbose_name="Kanuni Temsilci Tc",blank=True,null=True)
    beyannamekanunitemsicivergino = models.CharField(max_length=20,verbose_name="Kanuni Temsilci Vergi No",blank=True,null=True)
    beyannamekanunitemsicisoyadi = models.CharField(max_length=200,verbose_name="")