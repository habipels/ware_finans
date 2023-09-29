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