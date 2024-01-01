
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *
app_name = "company"
urlpatterns = [
    path("companysettings/",firma_ekleme,name="Firma_ekle"),
    path("show/<str:slug>",firma_gosterme,name="firmagosterme"),
    path("addsite/<str:slug>",firmaya_sube_ekleme,name="firmaya_sube_ekleme"),
    path("show/<str:slug>/<int:id>",firma_gosterme_subeli,name="firma_gosterme_subeli"),
    path("delete/<str:slug>/<int:id>",sube_sil,name="sube_sil"),
    path("deletecompany/<str:slug>",firma_sil,name="firma_sil"),
]
#