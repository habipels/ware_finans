from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(firma)
admin.site.register(adresler)
admin.site.register(vergi_dairesi)
admin.site.register(sube)
admin.site.register(İller_ve_ilceler)
admin.site.register(ortak_bilgileri)
admin.site.register(ortak_is_bilgileri)
admin.site.register(faliyet_bilgisi)
admin.site.register(calisma_sosyal_guvenlik_is_kollari)
admin.site.register(sube_faliyet_bilgileri)
admin.site.register(ihale_bilgileri)
admin.site.register(taseronbilgileri)
admin.site.register(kurumlar_dar_mukkelef_kimlik_ve_adres_bilgisi)
admin.site.register(beyanname_bilgileri)