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
    path("<str:slug>/bankasil/<int:id>/", views.banka_silme_sayfasi, name="banka_silme_sayfasi"),
    #stok İşlemelri
    #siparis işlemleri 
    path("<str:slug>/siparis/", views.siparis_sayfasi, name="siparis_sayfasi"),
    path("<str:slug>/siparissil/<int:id>/", views.siparis_silme_sayfasi, name="siparis_silme_sayfasi"),
    path("<str:slug>/siparisaktifpasif/<int:id>/", views.siparis_aktif_pasif_sayfasi, name="siparis_aktif_pasif_sayfasi"),
    path("<str:slug>/siparisonaylama/<int:id>/", views.siparis_onaylama_sayfasi, name="siparis_onaylama_sayfasi"),
    path("<str:slug>/siparisduzelt/<int:id>/", views.siparis_sayfasi_duzeltme, name="siparis_sayfasi_duzeltme"),
    #deneme
    #siparis işlemeleri
    #irsaliye işlemleri 
    path("<str:slug>/irsaliye/", views.irsaliye_sayfasi, name="irsaliye_sayfasi"),
    path("<str:slug>/irsaliyesil/<int:id>/", views.irsaliye_silme_sayfasi, name="irsaliye_silme_sayfasi"),
    path("<str:slug>/siparisaktarma/<int:id>/", views.siparisi_irsaliye_aktar, name="siparisi_irsaliye_aktar"),
    #
    #irsaliye işlemleri
    #Banka işlemleri 
    path("<str:slug>/banka/", views.banka_sayfasi, name="banka_sayfasi"),
    path("<str:slug>/yenibankakarti/", views.yeni_banka_karti, name="yeni_banka_karti"),
    path("<str:slug>/stoksil/<int:id>/", views.stok_sil, name="stok_sil"),
    #Banka işlemeleri
    #kasa Fiş İşlemeleri
    path("<str:slug>/kasatahsilfisi/", views.kasa_tahsilat_fisi, name="kasa_tahsilat_fisi"),
    path("<str:slug>/kasaodemefisi/", views.kasa_odeme_fisi, name="kasa_odeme_fisi"),
    path("<str:slug>/virmanfisi/", views.kasa_virman_fisi, name="kasa_virman_fisi"),
    path("<str:slug>/dovizfisi/", views.kasa_doviz_fisi, name="kasa_doviz_fisi"),
    path("<str:slug>/kasaacilisfisi/", views.kasa_acilis_fisi, name="kasa_acilis_fisi"),
    path("<str:slug>/kasatahsilatmakbuzu/", views.kasa_tahsilat_makbuzu, name="kasa_tahsilat_makbuzu"),
    path("<str:slug>/kasaodememakbuzu/", views.kasa_tahsilat_odeme, name="kasa_tahsilat_odeme"),
    path("<str:slug>/kasamaasodeme/", views.kasa_maas_odeme, name="kasa_maas_odeme"),
    #kasa Fiş İşlemeleri
    #kasa cari fişleri
    path("<str:slug>/kasacariodeme/", views.kasa_cari_odeme_fisi, name="kasa_cari_odeme_fisi"),
    path("<str:slug>/kasacaritahsilat/", views.kasa_cari_tahsilat_fisi, name="kasa_cari_tahsilat_fisi"),
    #kasa cari fişleri
    #kasa Banka fişleri
    path("<str:slug>/kasabankayayatirmafisi/", views.kasa_banka_yatirilan, name="kasa_banka_yatirilan"),
    path("<str:slug>/kasabankacekmefisi/", views.kasa_banka_cekilen, name="kasa_banka_cekilen"),
    #kasa Banka fişleri
    # Banka fişleri
    #banka fişi kasa
    path("<str:slug>/bankadankasayayatirma/", views.kasadan_bankaya_yatirilan, name="kasadan_bankaya_yatirilan"),
    path("<str:slug>/bankakasacekmefisi/", views.bankadan_kasaya_yatirilan, name="bankadan_kasaya_yatirilan"),
    #banka fişi kasa
    #banka fişleri
    path("<str:slug>/bankaacilisfisi/", views.banka_acilis_fisi, name="banka_acilis_fisi"),
    path("<str:slug>/bankavirmanfisi/", views.banka_virman_fisi, name="banka_virman_fisi"),
    path("<str:slug>/bankadovizfisi/", views.banka_doviz_fisi, name="banka_doviz_fisi"),
    path("<str:slug>/bankagelirfisi/", views.banka_gelir_fisi, name="banka_gelir_fisi"),
    path("<str:slug>/bankagiderfisi/", views.banka_gider_fisi, name="banka_gider_fisi"),
    path("<str:slug>/bankagelirmakbuzu/", views.banka_gelir_makbuzu, name="banka_gelir_makbuzu"),
    path("<str:slug>/bankagidermakbuzu/", views.banka_gider_makbuzu, name="banka_gider_makbuzu"),
    path("<str:slug>/bankagonderilenhavale/", views.banka_cari_gonderilen_havale, name="banka_cari_gonderilen_havale"),
    path("<str:slug>/bankagelenhavale/", views.banka_cari_gelen_havale, name="banka_cari_gelen_havale"),
    #
    #  Banka fişleri
    # Borç Dekontu
    path("<str:slug>/borcdekontu/", views.cari_borcdekontu, name="cari_borcdekontu"),
    path("<str:slug>/alacakdekontu/", views.cari_alacakdekontu, name="cari_alacakdekontu"),
    path("<str:slug>/carivirman/", views.cari_virman_fisi, name="cari_virman_fisi"),
    path("<str:slug>/cariacilis/", views.cari_acilis_fisi, name="cari_acilis_fisi"),
    path("<str:slug>/borcmakbuzu/", views.cari_borcmakbuzu, name="cari_borcmakbuzu"),
    path("<str:slug>/alacakmakbuzu/", views.cari_alacakmakbuzu, name="cari_alacakmakbuzu"),
    path("<str:slug>/cariodemefisi/", views.cari_odeme_fisi, name="cari_odeme_fisi"),
    path("<str:slug>/caritahsilatfisi/", views.cari_tahsilat_fisi, name="cari_tahsilat_fisi"),
    # Borç Dekontu
    #dilekçe
    path("<str:slug>/dilekce/", views.dilekcesayfasi, name="dilekcesayfasi"),
    #dilekçe
    #Genel Muhasebe
    path("<str:slug>/genelmuhasebe/", views.genel_muhasebe_sayfasi, name="genel_muhasebe_sayfasi"),
    #Genel Muhasebe
    #Hesap Planları
    path("<str:slug>/hesapplanlari/", views.hesap_planlari_ayarlari, name="hesap_planlari_ayarlari"),
    path("<str:slug>/hesapplaniekle/", views.hesap_planlari_ekle, name="hesap_planlari_ekle"),
    path("<str:slug>/hesapplanisil/<int:id>/", views.hesap_planlari_silme, name="hesap_planlari_silme"),
    path("<str:slug>/hesapplandetaydegistir/<int:id>/", views.hesap_planlari_detay_degistirme, name="hesap_planlari_detay_degistirme"),
    path("<str:slug>/hesapplaniduzenle/<int:id>/", views.hesap_planlari_duzenle, name="hesap_planlari_duzenle"),
    #Hesap Planları
    #muavin
    path("<str:slug>/muavin/", views.muavin, name="muavin"),
    path("<str:slug>/genelmuhasebefis/<int:id>/", views.genel_muhasebe_sayfasi_fis_duzenleme, name="genel_muhasebe_sayfasi_fis_duzenleme"),
    path("<str:slug>/genelmuhasebefisgoster/<int:id>/", views.genel_muhasebe_sayfasi_fis_goster, name="genel_muhasebe_sayfasi_fis_goster"),
    #
]#