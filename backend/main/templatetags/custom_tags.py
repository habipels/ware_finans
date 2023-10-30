from django import template
from bilgideposu.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
register = template.Library()

@register.filter
def get_otv_fiyati(stok_kart):
    
    satis_fiyati = stok_diger_kismi_otv.objects.filter(stok_karti_bilgisi=stok_kart.id).last()
    return satis_fiyati.otv_orani if satis_fiyati else 0

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
    print(satis_fiyati,"stok")
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
