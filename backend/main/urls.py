from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("<str:slug>/", views.firma_sayfasi, name="firma_sayfasi"),
    path("<str:slug>/kasa/", views.kasa_sayfasi, name="kasa_sayfasi"),
    path("<str:slug>/yenikasakarti/", views.yeni_kasa_karti_sayfasi, name="yeni_kasa_karti_sayfasi"),
    path("<str:slug>/kasakartiduzelt/<int:id>/", views.kasa_karti_duzeltme_sayfasi, name="kasa_karti_duzeltme_sayfasi"),
    path("<str:slug>/kasakartisil/<int:id>/", views.kasa_karti_silme_sayfasi, name="kasa_karti_silme_sayfasi"),
]