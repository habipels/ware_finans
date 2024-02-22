from django import template
from bilgideposu.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def get_otv_fiyati(stok_kart):
    
    satis_fiyati = stok_diger_kismi_otv.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.otv_orani if satis_fiyati else 0

@register.filter
def get_otv_fiyati_otv_tahsil_orani(stok_kart):
    
    satis_fiyati = stok_diger_kismi_otv.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.otv_tahsil_orani if satis_fiyati else 0
@register.filter
def get_otv_fiyati_mera_fonu_orani(stok_kart):
    
    satis_fiyati = stok_diger_kismi_otv.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.mera_fonu_orani if satis_fiyati else 0
@register.filter
def get_otv_fiyati_otv_tecil_orani(stok_kart):
    
    satis_fiyati = stok_diger_kismi_otv.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.otv_tecil_orani if satis_fiyati else 0
@register.filter
def get_otv_fiyati_birim(stok_kart):
    
    satis_fiyati = stok_diger_kismi_otv.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.otv_brim_fiyati if satis_fiyati else 0
@register.filter
def get_stok_detaylari_ozellik1(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik1 if satis_fiyati.ozellik1 else ""
@register.filter
def get_stok_detaylari_ozellik2(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik2 if satis_fiyati.ozellik2 else ""
@register.filter
def get_stok_detaylari_ozellik3(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik3 if satis_fiyati.ozellik3 else ""
@register.filter
def get_stok_detaylari_ozellik4(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik4 if satis_fiyati.ozellik4 else ""
@register.filter
def get_stok_detaylari_ozellik5(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik5 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_kodlari_ozel_kod_1(stok_kart):
    
    satis_fiyati = stok_kodlari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozel_kod_1 if satis_fiyati.ozel_kod_1 else ""
@register.filter()
def get_stok_kodlari_ozel_kod_2(stok_kart):
    satis_fiyati = stok_kodlari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozel_kod_2 if satis_fiyati else ""
@register.filter()
def get_stok_kodlari_kalitekodu(stok_kart):
    
    satis_fiyati = stok_kodlari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.kalitekodu if satis_fiyati.kalitekodu else ""
@register.filter()
def get_stokalisveris(stok_kart):
    
    satis_fiyati = stok_alis_satis.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    if satis_fiyati.aktif_satis_fiyati == "1":
        satis_fiyati = satis_fiyati.satis_fiyati_1_tl
    elif satis_fiyati.aktif_satis_fiyati == "2":
        satis_fiyati = satis_fiyati.satis_fiyati_2_tl
    elif satis_fiyati.aktif_satis_fiyati == "3":
        satis_fiyati = satis_fiyati.satis_fiyati_3_tl
    elif satis_fiyati.aktif_satis_fiyati == "4":
        satis_fiyati = satis_fiyati.satis_fiyati_4_tl
    elif satis_fiyati.aktif_satis_fiyati == "5":
        satis_fiyati = satis_fiyati.satis_fiyati_5_tl
    elif satis_fiyati.aktif_satis_fiyati == "6":
        satis_fiyati = satis_fiyati.satis_fiyati_6_tl
    elif satis_fiyati.aktif_satis_fiyati == "7":
        satis_fiyati = satis_fiyati.satis_fiyati_7_tl
    elif satis_fiyati.aktif_satis_fiyati == "8":
        satis_fiyati = satis_fiyati.satis_fiyati_8_tl
    elif satis_fiyati.aktif_satis_fiyati == "9":
        satis_fiyati = satis_fiyati.satis_fiyati_9_tl
    elif satis_fiyati.aktif_satis_fiyati == "10":
        satis_fiyati = satis_fiyati.satis_fiyati_10_tl
    return satis_fiyati if satis_fiyati else "0"
@register.filter(name="get_stok_kodlari_alternatifstokkodu")
def get_stok_kodlari_alternatifstokkodu(stok_kart):
    
    satis_fiyati = stok_kodlari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.alternatifstokkodu if satis_fiyati.alternatifstokkodu else ""
@register.filter()
def get_stok_kodlari_alternatifstokadi(stok_kart):
    
    satis_fiyati = stok_kodlari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.alternatifstokadi if satis_fiyati.alternatifstokadi else ""

@register.filter()
def get_stokalisverisalis(stok_kart):
    satis_fiyati = stok_alis_satis.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    if satis_fiyati.aktif_alis_fiyati == "1":
        satis_fiyati = satis_fiyati.alis_fiyati_1_tl
    elif satis_fiyati.aktif_alis_fiyati == "2":
        satis_fiyati = satis_fiyati.alis_fiyati_2_tl
    elif satis_fiyati.aktif_alis_fiyati == "3":
        satis_fiyati = satis_fiyati.alis_fiyati_3_tl
    elif satis_fiyati.aktif_alis_fiyati == "4":
        satis_fiyati = satis_fiyati.alis_fiyati_4_tl
    elif satis_fiyati.aktif_alis_fiyati == "5":
        satis_fiyati = satis_fiyati.alis_fiyati_5_tl
    return satis_fiyati if satis_fiyati else "0"


@register.filter()
def get_stok_diger_kismi_agirliklar(stok_kart):
    
    satis_fiyati = stok_diger_kismi_agirliklar.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.net if satis_fiyati.net else ""


@register.filter()
def get_stok_diger_kismi_agirliklar_burut(stok_kart):
    
    satis_fiyati = stok_diger_kismi_agirliklar.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.brut if satis_fiyati.brut else ""


@register.filter()
def get_stok_diger_kismi_agirliklar_pkaciklamasi(stok_kart):
    
    satis_fiyati = stok_diger_kismi_agirliklar.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.p_aciklamasi if satis_fiyati.p_aciklamasi else ""

@register.filter()
def get_stok_diger_kismi_agirliklar_pkmiktari(stok_kart):
    
    satis_fiyati = stok_diger_kismi_agirliklar.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.p_miktari if satis_fiyati.p_miktari else ""


@register.filter
def get_stok_detaylari_ozellik6(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik6 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik7(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik7 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik8(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik8 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik9(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik9 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik10(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik10 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik11(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik11 if satis_fiyati.ozellik5 else ""

@register.filter
def get_stok_detaylari_ozellik12(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik12 if satis_fiyati.ozellik5 else ""

@register.filter
def get_stok_detaylari_ozellik13(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik13 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik14(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik14 if satis_fiyati.ozellik5 else ""

@register.filter
def get_stok_detaylari_ozellik15(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik15 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik16(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik16 if satis_fiyati.ozellik5 else ""

@register.filter
def get_stok_detaylari_ozellik17(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik17 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik18(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik18 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik19(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik19 if satis_fiyati.ozellik5 else ""
@register.filter
def get_stok_detaylari_ozellik20(stok_kart):
    
    satis_fiyati = stok_detaylari.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.ozellik20 if satis_fiyati.ozellik5 else ""

@register.simple_tag
def bakiye_degeri(a,b):
    if round(float(a-b),2) > 0:
        return round(float(a-b),2)
    else:
        return (-1)*(round(float(a-b),2))


@register.simple_tag
def bakiye_degeri_i(a,b):
    if round(float(a-b),2) > 0:
        return "A"
    else:
        return "B"

@register.simple_tag
def mizan_fis_islemleri_kontrol(id):
    a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = id).count()
    
    return a

@register.simple_tag
def mizan_fis_islemleri_borc(id):
    a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = id)
    sonuc = 0
    for i in a:
        sonuc = sonuc + i.borc
    return sonuc

@register.simple_tag
def mizan_fis_islemleri_alacak(id):
    a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = id)
    sonuc = 0
    for i in a:
        sonuc = sonuc + i.alacak_bilgisi
    return sonuc

@register.simple_tag
def mizan_fis_islemleri_borc_yazdirma(id):
    a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = id)
    borc = 0
    alacak = 0
    for i in a:
        borc = borc + i.borc
    for i in a:
        alacak = alacak + i.alacak_bilgisi
    if borc > alacak:

        return borc-alacak
    return ""

@register.simple_tag
def mizan_fis_islemleri_alacak_yazdirma(id):
    a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = id)
    borc = 0
    alacak = 0
    for i in a:
        borc = borc + i.borc
    for i in a:
        alacak = alacak + i.alacak_bilgisi
    if borc < alacak:

        return alacak-borc
    return ""


@register.simple_tag
def mizan_fislerin_borc_toplam_hesaplanmasi(veri):
    borc = 0
    alacak = 0
    for i in veri :
        a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = i.id)
        
        for i in a:
            borc = borc + i.borc
        for i in a:
            alacak = alacak + i.alacak_bilgisi
    print(borc)
    return borc

@register.simple_tag
def mizan_fislerin_alacak_toplam_hesaplanmasi(veri):
    borc = 0
    alacak = 0
    for i in veri :
        a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = i.id)
        
        for i in a:
            borc = borc + i.borc
        for i in a:
            alacak = alacak + i.alacak_bilgisi
    return alacak

@register.simple_tag
def mizan_fislerin_borc_toplam_hesaplanmasi_bakiye(veri):
    borc = 0
    alacak = 0
    for i in veri :
        a = genel_muhasebe_fis.objects.filter(hesap_plani_secim__id = i.id)
        
        for i in a:
            borc = borc + i.borc
        for i in a:
            alacak = alacak + i.alacak_bilgisi
    
    return borc-alacak

@register.simple_tag
def borc_topam(id):
    borc_topam_ = 0
    a = musteri_cari_fis.objects.filter(bagli_oldugu_cari__id = id)
    for i in a:
        borc_topam_ = borc_topam_+ float(i.borc)
    return borc_topam_

@register.simple_tag
def alacak_topam(id):
    borc_topam_ = 0
    a = musteri_cari_fis.objects.filter(bagli_oldugu_cari__id = id)
    for i in a:
        borc_topam_ = borc_topam_+ float(i.alacak)
    return borc_topam_

@register.simple_tag
def bakiye_topam(id):
    borc_topam_ = 0
    alacak_topam_ = 0
    sonuc = 0
    a = musteri_cari_fis.objects.filter(bagli_oldugu_cari__id = id)
    for i in a:
        alacak_topam_ = alacak_topam_+ float(i.alacak)
    for i in a:
        borc_topam_ = borc_topam_+ float(i.borc)
    if borc_topam_ > alacak_topam_:
        sonuc =  borc_topam_ - alacak_topam_
    else:
        sonuc =  alacak_topam_ - borc_topam_ 
    return sonuc
@register.simple_tag
def alacak_vericek_topam(id):
    borc_topam_ = 0
    alacak_topam_ = 0
    a = musteri_cari_fis.objects.filter(bagli_oldugu_cari__id = id)
    for i in a:
        alacak_topam_ = alacak_topam_+ float(i.alacak)
    for i in a:
        borc_topam_ = borc_topam_+ float(i.borc)
    if borc_topam_ > alacak_topam_:
        return "B"
    else:
        return "A"
    
@register.simple_tag
def tum_toplam_olayi(id):
    a = musavir_stok_fisi.objects.filter(bagli_oldugu_stok = get_object_or_404(musavir_stok,id = id))
    giris = 0
    giris_tutar = 0
    cikis = 0
    cikis_tutar = 0
    for i in a:
        giris = giris+i.giris_miktari
        giris_tutar = giris_tutar+i.giris_fiyati
        cikis = cikis + i.cikis_miktari
        cikis_tutar = cikis_tutar + i.cikis_fiyati
    sonuc = giris - cikis
    veri= '<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>'.format(
        giris,giris_tutar,cikis,cikis_tutar,sonuc
    )
    return mark_safe ( veri)

@register.simple_tag
def tarih_yazdirma(a):
    b = str(a).split("-")
    durum = ""
    if b[1] == "01":
        durum = str(b[0])+": OCAK"
    if b[1] == "02":
        durum = str(b[0])+": ŞUBAT"
    if b[1] == "03":
        durum = str(b[0])+": MART"
    if b[1] == "04":
        durum = str(b[0])+": NİSAN"
    if b[1] == "05":
        durum = str(b[0])+": MAYIS"
    if b[1] == "06":
        durum = str(b[0])+": HAZİRAN"
    if b[1] == "07":
        durum = str(b[0])+": TEMMUZ"
    if b[1] == "08":
        durum = str(b[0])+": AĞUSTOS"
    if b[1] == "09":
        durum = str(b[0])+": EYLÜL"
    if b[1] == "10":
        durum = str(b[0])+": EKİM"
    if b[1] == "11":
        durum = str(b[0])+": KASIM"
    if b[1] == "12":
        durum = str(b[0])+": ARALIK"
    return durum

@register.simple_tag
def silinen_firmalar(bilgi):
    a = firma.objects.filter(firma_muhasabecisi = bilgi,silinme_bilgisi = True)
    return a
@register.simple_tag
def silinen_subeler(bilgi):
    a = sube.objects.filter(bagli_oldugu_firma__firma_muhasabecisi = bilgi,silinme_bilgisi = True)
    return a