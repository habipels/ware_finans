from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("<str:slug>/", views.firma_sayfasi, name="firma_sayfasi"),
    #kasa işlemleri
    path("<str:slug>/kasa/", views.kasa_sayfasi, name="kasa_sayfasi"),
    path("<str:slug>/yenikasakarti/", views.yeni_kasa_karti_sayfasi, name="yeni_kasa_karti_sayfasi"),
    path("<str:slug>/kasakartiduzelt/<int:id>/", views.kasa_karti_duzeltme_sayfasi, name="kasa_karti_duzeltme_sayfasi"),
    path("<str:slug>/kasakartisil/<int:id>/", views.kasa_karti_silme_sayfasi, name="kasa_karti_silme_sayfasi"),
    #kasa işlemleri
    #gider işlemelri
    path("<str:slug>/gider/", views.gider_sayfasi, name="gider_sayfasi"),
    path("<str:slug>/yenigider/", views.yeni_gider_sayfasi, name="yeni_gider_sayfasi"),
    path("<str:slug>/giderduzelt/<int:id>/", views.gider_duzeltme_sayfasi, name="gider_duzeltme_sayfasi"),
    path("<str:slug>/gidersil/<int:id>/", views.gider_silme_sayfasi, name="gider_silme_sayfasi"),
    #gider işlemelri
    #gelir İşlemelri
    path("<str:slug>/gelir/", views.gelir_sayfasi, name="gelir_sayfasi"),
    path("<str:slug>/yenigelir/", views.yeni_gelir_sayfasi, name="yeni_gelir_sayfasi"),
    path("<str:slug>/gelirduzelt/<int:id>/", views.gelir_duzeltme_sayfasi, name="gelir_duzeltme_sayfasi"),
    path("<str:slug>/gelirsil/<int:id>/", views.gelir_silme_sayfasi, name="gelir_silme_sayfasi"),
    #cari işlemleri
    path("<str:slug>/cari/", views.cari_sayfasi, name="cari_sayfasi"),
    path("<str:slug>/yenicari/", views.yeni_cari_karti, name="yeni_cari_karti"),
    path("<str:slug>/carisil/<int:id>/", views.cari_silme_sayfasi, name="cari_silme_sayfasi"),
    #cari işlemleri
    #stok işlemelri
    path("<str:slug>/stok/", views.stok_sayfasi, name="stok_sayfasi"),
    path("<str:slug>/yenistok/", views.yeni_stok_karti, name="yeni_stok_karti"),
    #stok İşlemelri
    #stok işlemelri
    path("<str:slug>/fatura/", views.fatura_sayfasi, name="fatura_sayfasi"),
    #stok İşlemelri
    #siparis işlemleri 
    path("<str:slug>/siparis/", views.siparis_sayfasi, name="siparis_sayfasi"),
    #siparis işlemeleri
    #Banka işlemleri 
    path("<str:slug>/banka/", views.banka_sayfasi, name="banka_sayfasi"),
    path("<str:slug>/yenibankakarti/", views.yeni_banka_karti, name="yeni_banka_karti"),
    #Banka işlemeleri
]