from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(banka)
admin.site.register(banka_yetkilisi)
admin.site.register(tevkifat_tur_kodu)
admin.site.register(HesapPlanlari)
admin.site.register(banka_kart_bilgileri)
admin.site.register(Kasa)
admin.site.register(Giderler)
admin.site.register(Gelirler)
admin.site.register(kasa_fisleri)
admin.site.register(cari_kartlar)
admin.site.register(ulke_ulke_kodlari)
admin.site.register(cari_kartislemleri_adresleri_kimlik)
admin.site.register(cari_kartislemleri_diger_bilgiler)
admin.site.register(cari_kartislemleri_notlar)
admin.site.register(cari_kartislemleri_firma_gorevilisi)
admin.site.register(banka_kodlari)
admin.site.register(banka_notlari)
admin.site.register(banka_kredikartibilgileri)