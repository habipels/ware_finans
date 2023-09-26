
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *
app_name = "company"
urlpatterns = [
    path("companysettings/",firma_ekleme,name="Firma_ekle"),
    path("show/<str:slug>",firma_gosterme,name="firmagosterme"),
]
