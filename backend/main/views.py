from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.http import HttpResponse
from users.models import *
from bilgideposu.models import *
from django.db.models import Q
from site_ayarlari.models import *
from datetime import datetime
def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except :
        return None
def site_ayarlari():
    sozluk = {}
    sozluk["logomuz"] = sayfa_logosu.objects.all().last()
    sozluk["iconumuz"] = sayfa_iconu.objects.all().last()
    sozluk["ismimiz"] = site_adi.objects.all().last()
    sozluk["numaramiz"] = numara.objects.all().last()
    sozluk["adresimiz"] = adres.objects.all().last()
    sozluk["emailimiz"] = email_adres.objects.all().last()
    sozluk["instamiz"] = sosyalmedyaInsgr.objects.all().last()
    sozluk["linkedinmiz"] = sosyalmedyalinkd.objects.all().last()
    sozluk["facemiz"] = sosyalmedyaFace.objects.all().last()
    sozluk["youtubemiz"] = sosyalmedyayoutube.objects.all().last()
    sozluk["twmiz"] = sosyalmedyatw.objects.all().last()
    sozluk["seoayarimiz"] = seo_ayarlari.objects.all().last()
    return sozluk
# Create your views here.
def homepage(request):
    content = site_ayarlari()
    if request.user.is_authenticated:
        content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    else:
        return redirect("/users/loginandregister/")
    return render(request,"index.html",content)

def firma_sayfasi(request,slug):
    content = site_ayarlari()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"firma_index.html",content)
#Kasa İşlemeleri 
def kasa_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["kasakartlarim"] = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kasafisleri"] = KasaFisIslemleri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"kasa/kasa.html",content)

def yeni_kasa_karti_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    if request.POST:
        kasakodu = request.POST.get("kasakodu")
        kasaadi = request.POST.get("kasaadi")
        kasaaciklamasi = request.POST.get("kasaaciklamasi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        entkodu = request.POST.get("entkodu")
        dovizcinsi = request.POST.get("dovizcinsi")
        ozelkod = request.POST.get("ozelkod")
        Kasa.objects.create(
            kasa_kodu = kasakodu,entkodu = entkodu,
            kasa_adi = kasaadi,ozel_kod = ozelkod,
            doviz_cinsi = dovizcinsi,bagli_oldugu_firma = get_object_or_404(firma,firma_ozel_anahtar = slug),
            toplam_tahsilat = "0",toplam_odeme = "0",toplam_bakiye = "0",
            muh_kodu = muhtasarkodu,aciklama = kasaaciklamasi,
            silinme_bilgisi = False
        )
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/yenikasa.html",content)
def kasa_karti_duzeltme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    kart = get_object_or_404(Kasa,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    if request.POST:
        kasakodu = request.POST.get("kasakodu")
        kasaadi = request.POST.get("kasaadi")
        kasaaciklamasi = request.POST.get("kasaaciklamasi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        entkodu = request.POST.get("entkodu")
        dovizcinsi = request.POST.get("dovizcinsi")
        ozelkod = request.POST.get("ozelkod")
        Kasa.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            kasa_kodu = kasakodu,entkodu = entkodu,
            kasa_adi = kasaadi,ozel_kod = ozelkod,
            doviz_cinsi = dovizcinsi,bagli_oldugu_firma = get_object_or_404(firma,firma_ozel_anahtar = slug),
            muh_kodu = muhtasarkodu,aciklama = kasaaciklamasi,
            silinme_bilgisi = False
        )
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/kasakartiduzelt.html",content)
def kasa_karti_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    kart = get_object_or_404(Kasa,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
  

    Kasa.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/kasa/"
    return redirect(link)
#Kasa İşlemeleri
#Gider İşlemelri 
def gider_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["giderler"] = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"gider_gelir/gider.html",content)


def yeni_gider_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    gider = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    content["gider"] = gider
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    if request.POST:
        anagiderkodu = request.POST.get("anagiderkodu")
        giderbilgisi = Giderler.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
        for i in giderbilgisi:
            if i.gider_kodu == anagiderkodu:
                anagiderkodu = i.gider_kodu
                break
            else:
                anagiderkodu = ""

        giderdetay = request.POST.get("giderdetay")
        giderkodu = request.POST.get("giderkodu")
        gideradi = request.POST.get("gideradi")
        giderbirim = request.POST.get("giderbirim")
        kdv = float(request.POST.get("kdv"))
        ozelkod = request.POST.get("ozelkod")
        dovizcinsi = request.POST.get("dovizcinsi")
        birimfiyati = request.POST.get("birimfiyati")
        birimfiyatidoviz = request.POST.get("birimfiyatidoviz")
        muhkodu1 = request.POST.get("muhkodu1")
        muhkodu2 = request.POST.get("muhkodu2")
        muhkodukdv = request.POST.get("muhkodukdv")
        Giderler.objects.create(
            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            ana_gider_kodu = anagiderkodu,gider_kodu = giderkodu,
            gider_adi = gideradi,detay = giderdetay,
            birim= giderbirim,kdv = kdv,doviz_cinsi = dovizcinsi,birim_fiyat_tl = birimfiyati,
            birim_fiyat_doviz = birimfiyatidoviz,ozel_kod_1 = ozelkod,toplam_alacak = "0",
            toplam_borc = "0",toplam_bakiye = "0",muh_kodu1 = muhkodu1,
            muh_kodu2 = muhkodu2,muh_kodukdv = muhkodukdv,silinme_bilgisi = False
        )
        link = "/"+slug+"/gider/"
        return redirect(link)
    return render(request,"gider_gelir/yeni_gider.html",content)


def gider_duzeltme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    gider = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    content["giderr"] = get_object_or_404(Giderler,silinme_bilgisi = False,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    if request.POST:
        anagiderkodu = request.POST.get("anagiderkodu")
        giderbilgisi = Giderler.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
        for i in giderbilgisi:
            if i.gider_kodu == anagiderkodu:
                anagiderkodu = i.gider_kodu
                break
            else:
                anagiderkodu = ""

        giderdetay = request.POST.get("giderdetay")
        giderkodu = request.POST.get("giderkodu")
        gideradi = request.POST.get("gideradi")
        giderbirim = request.POST.get("giderbirim")
        kdv = float(request.POST.get("kdv"))
        ozelkod = request.POST.get("ozelkod")
        dovizcinsi = request.POST.get("dovizcinsi")
        birimfiyati = request.POST.get("birimfiyati")
        birimfiyatidoviz = request.POST.get("birimfiyatidoviz")
        muhkodu1 = request.POST.get("muhkodu1")
        muhkodu2 = request.POST.get("muhkodu2")
        muhkodukdv = request.POST.get("muhkodukdv")
        Giderler.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            ana_gider_kodu = anagiderkodu,gider_kodu = giderkodu,
            gider_adi = gideradi,detay = giderdetay,
            birim= giderbirim,kdv = kdv,doviz_cinsi = dovizcinsi,birim_fiyat_tl = birimfiyati,
            birim_fiyat_doviz = birimfiyatidoviz,ozel_kod_1 = ozelkod,toplam_alacak = "0",
            toplam_borc = "0",toplam_bakiye = "0",muh_kodu1 = muhkodu1,
            muh_kodu2 = muhkodu2,muh_kodukdv = muhkodukdv,silinme_bilgisi = False
        )
        link = "/"+slug+"/gider/"
        return redirect(link)
    return render(request,"gider_gelir/gider_duzelt.html",content)


def gider_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    kart = get_object_or_404(Giderler,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
  

    Giderler.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/gider/"
    return redirect(link)
#Gider İşlemleri
#Gelir İşlemelri
def gelir_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["gelirler"] = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"gider_gelir/gelir.html",content)


def yeni_gelir_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    gider = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    content["gider"] = gider
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    if request.POST:
        anagiderkodu = request.POST.get("anagiderkodu")
        giderbilgisi = Giderler.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
        for i in giderbilgisi:
            if i.gider_kodu == anagiderkodu:
                anagiderkodu = i.gider_kodu
                break
            else:
                anagiderkodu = ""

        giderdetay = request.POST.get("giderdetay")
        giderkodu = request.POST.get("giderkodu")
        gideradi = request.POST.get("gideradi")
        giderbirim = request.POST.get("giderbirim")
        kdv = float(request.POST.get("kdv"))
        ozelkod = request.POST.get("ozelkod")
        dovizcinsi = request.POST.get("dovizcinsi")
        birimfiyati = request.POST.get("birimfiyati")
        birimfiyatidoviz = request.POST.get("birimfiyatidoviz")
        muhkodu1 = request.POST.get("muhkodu1")
        muhkodu2 = request.POST.get("muhkodu2")
        Gelirler.objects.create(
            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            ana_gelir_kodu = anagiderkodu,gelir_kodu = giderkodu,
            gelir_adi = gideradi,detay = giderdetay,
            birim= giderbirim,kdv = kdv,doviz_cinsi = dovizcinsi,birim_fiyat_tl = birimfiyati,
            birim_fiyat_doviz = birimfiyatidoviz,ozel_kod_1 = ozelkod,toplam_alacak = "0",
            toplam_borc = "0",toplam_bakiye = "0",muh_kodu1 = muhkodu1,
            muh_kodu2 = muhkodu2,silinme_bilgisi = False
        )
        link = "/"+slug+"/gelir/"
        return redirect(link)
    return render(request,"gider_gelir/yeni_gelir.html",content)


def gelir_duzeltme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    gider = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    content["giderr"] = get_object_or_404(Gelirler,silinme_bilgisi = False,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gider = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    content["gider"] = gider
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    if request.POST:
        anagiderkodu = request.POST.get("anagiderkodu")
        giderbilgisi = Gelirler.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
        for i in giderbilgisi:
            if i.gider_kodu == anagiderkodu:
                anagiderkodu = i.gider_kodu
                break
            else:
                anagiderkodu = ""

        giderdetay = request.POST.get("giderdetay")
        giderkodu = request.POST.get("giderkodu")
        gideradi = request.POST.get("gideradi")
        giderbirim = request.POST.get("giderbirim")
        kdv = float(request.POST.get("kdv"))
        ozelkod = request.POST.get("ozelkod")
        dovizcinsi = request.POST.get("dovizcinsi")
        birimfiyati = request.POST.get("birimfiyati")
        birimfiyatidoviz = request.POST.get("birimfiyatidoviz")
        muhkodu1 = request.POST.get("muhkodu1")
        muhkodu2 = request.POST.get("muhkodu2")
        muhkodukdv = request.POST.get("muhkodukdv")
        Gelirler.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            ana_gelir_kodu = anagiderkodu,gelir_kodu = giderkodu,
            gelir_adi = gideradi,detay = giderdetay,
            birim= giderbirim,kdv = kdv,doviz_cinsi = dovizcinsi,birim_fiyat_tl = birimfiyati,
            birim_fiyat_doviz = birimfiyatidoviz,ozel_kod_1 = ozelkod,toplam_alacak = "0",
            toplam_borc = "0",toplam_bakiye = "0",muh_kodu1 = muhkodu1,
            muh_kodu2 = muhkodu2,silinme_bilgisi = False
        )
        link = "/"+slug+"/gider/"
        return redirect(link)
    return render(request,"gider_gelir/gelir_duzelt.html",content)


def gelir_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    kart = get_object_or_404(Gelirler,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
  

    Gelirler.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/gelir/"
    return redirect(link)

#Gelir İşlemeleri
#Cari işlemeler
def cari_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["carikartlari"] = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carifisleri"] = cari_fisleri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"cari/cari.html",content)
def yeni_cari_karti(request,slug):
    content = site_ayarlari()
    v = vergi_dairesi.objects.all()
    content["firma"] =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["cariler"] = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["vergidaireleri"] = v
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    if request.POST:
        anacarikodu = request.POST.get("anacarikodu")
        caridetay = request.POST.get("caridetay")
        listedegorunme = request.POST.get("listedegorunme")
        carihesapkilidi = request.POST.get("carihesapkilidi")
        carikodu = request.POST.get("carikodu")
        mukellefturu = request.POST.get("mukellefturu")
        cariadi  = request.POST.get("cariadi")
        caritip = request.POST.get("caritip")
        dovizcinsi = request.POST.get("dovizcinsisec")
        carikarttipi = request.POST.get("carikarttipi")
        yetkiliadisoyadi = request.POST.get("yetkiliadisoyadi")
        gorevi = request.POST.get("gorevi")
        istihbarat = request.POST.get("istihbarat")
        muhkodu = request.POST.get("muhkodu")
        tevkifatkodu = request.POST.get("tevkifatkodu") 
        ozelkod1 = request.POST.get("ozelkod1") 
        ozelkod2 = request.POST.get("ozelkod2")
        satici = request.POST.get("satici")
        departman = request.POST.get("departman")
        grupkodu1 = request.POST.get("grupkodu1")
        grupkodu2 = request.POST.get("grupkodu2")
        grupkodu3 = request.POST.get("grupkodu3")
        adres1 = request.POST.get("adres1")
        ilce1 = request.POST.get("ilce1")
        sehir1 = request.POST.get("sehir1")
        telefon1 = request.POST.get("telefon1")
        faks = request.POST.get("faks")
        telefon2 = request.POST.get("telefon2")
        telefon3 = request.POST.get("telefon3")
        gsm1 = request.POST.get("gsm1")
        gsm2 = request.POST.get("gsm2")
        postakodu = request.POST.get("postakodu")
        ulkekodu = request.POST.get("ulkekodu")
        vdkodu = request.POST.get("vdkodu")
        vergitckimlikno = request.POST.get("vergitckimlikno")
        epostaadresi = request.POST.get("epostaadresi")
        webadresi = request.POST.get("webadresi")
        adres2 = request.POST.get("adres2")
        ilce2 = request.POST.get("ilce2")
        sehir2 = request.POST.get("sehir2")
        telefon4 = request.POST.get("telefon4")
        faks2 = request.POST.get("faks2")
        postakodu2 = request.POST.get("postakodu2")
        ulke = request.POST.get("ulke")
        gsm3 = request.POST.get("gsm3")
        telefon5 = request.POST.get("telefon5")
        adi = request.POST.get("adi")
        soyadi = request.POST.get("soyadi")
        babaadi = request.POST.get("babaadi")
        anneadi = request.POST.get("anneadi")
        dogumyeri = request.POST.get("dogumyeri")
        dogumtarihi = request.POST.get("dogumtarihi")
        cinsiyet = request.POST.get("cinsiyet")
        serino = request.POST.get("serino")
        sskbagkurno = request.POST.get("sskbagkurno")
        risklimiti = request.POST.get("risklimiti")
        digerdovizcinsi = request.POST.get("digerdovizcinsi")
        faizvadefarki = request.POST.get("faizvadefarki")
        odemesuresigun = request.POST.get("odemesuresigun")
        iskontoorani = request.POST.get("iskontoorani")
        karorani = request.POST.get("karorani")
        taksitsayisi=  request.POST.get("taksitsayisi")
        taksitodemegunuherayin = request.POST.get("taksitodemegunuherayin")
        satisfiyati  =request.POST.get("satisfiyati")
        alisfiyati = request.POST.get("alisfiyati")
        stokgrupkodu = request.POST.get("stokgrupkodu")
        iskontoorani2= request.POST.get("iskontoorani2")
        indim1= request.POST.get("indim1")
        indim2= request.POST.get("indim2")
        indim3= request.POST.get("indim3")
        indim4= request.POST.get("indim4")
        indim5= request.POST.get("indim5")
        indim6= request.POST.get("indim6")
        uygunkursecenek = request.POST.get("uygunkursecenek")
        otvkullan = request.POST.get("otvkullan")
        bankaadi = request.POST.get("bankaadi")
        subesi = request.POST.get("subesi")
        bankadovizcinsi  =request.POST.get("bankadovizcinsi")
        hesapno = request.POST.get("hesapno")
        iban = request.POST.get("iban")
        subebilgilerisubekodu= request.POST.get("subebilgilerisubekodu")
        subebilgilerisubeadi = request.POST.get("subebilgilerisubeadi")
        subebilgileridovizcinsi = request.POST.get("subebilgileridovizcinsi")
        subebilgileriborctutari = request.POST.get("subebilgileriborctutari")
        subebilgilerialacaktutari= request.POST.get("subebilgilerialacaktutari")
        subebilgileribakiyetutari= request.POST.get("subebilgileribakiyetutari")
        subebilgileriba= request.POST.get("subebilgileriba")
        subebilgilerivadetarihi= request.POST.get("subebilgilerivadetarihi")
        subebilgileriadres= request.POST.get("subebilgileriadres")
        subebilgilerisemt= request.POST.get("subebilgilerisemt")
        subebilgilerisehir= request.POST.get("subebilgilerisehir")
        subebilgileritelefon= request.POST.get("subebilgileritelefon")
        subebilgileriyetkili= request.POST.get("subebilgileriyetkili")
        subebilgileriodemesuresi= request.POST.get("subebilgileriodemesuresi")
        subebilgilerivadehesapyonetimi= request.POST.get("subebilgilerivadehesapyonetimi")
        subebilgilerimuhkodu= request.POST.get("subebilgilerimuhkodu")
        subebilgileripostakodu= request.POST.get("subebilgileripostakodu")
        notlartarihi= request.POST.get("notlartarihi")
        notlarsatici= request.POST.get("notlarsatici")
        notlarnot= request.POST.get("notlarnot")
        firmagoreviadi= request.POST.get("firmagoreviadi")
        firmagorevligorevi= request.POST.get("firmagorevligorevi")
        firmagorevliistelefonu= request.POST.get("firmagorevliistelefonu")
        firmagorevlidahilinumara= request.POST.get("firmagorevlidahilinumara")
        firmagorevligsm= request.POST.get("firmagorevligsm")
        firmaaciklama= request.POST.get("firmaaciklama")
        if float(subebilgilerialacaktutari) > float(subebilgileriborctutari):
            subebilgileriba = "A"
        else:
            subebilgileriba = "B"
        yeni_cari_karti_olusturma = cari_kartlar.objects.create(
            ana_cari_kodu = anacarikodu,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            detay  = caridetay,listede_gorunsun  = listedegorunme,
            cari_kodu = carikodu,mukellefyet_turu = mukellefturu,tip = caritip,
            cari_hesap_kilitli = carihesapkilidi,takip_doviz_cinsi = dovizcinsi,
            cari_adi = cariadi,yetkili_adi = yetkiliadisoyadi,gorevi  =gorevi,
            istihbarat = istihbarat,cari_kart_tipi  =carikarttipi,
            borc_tutari  = 0,alacak_tutari = 0,bakiye_tutari  =0,
            ozel_kod_1 = ozelkod1,ozel_kod_2 = ozelkod2,satici = satici,
            departman  = departman,grup_kod_1 =grupkodu1 ,grup_kod_2 = grupkodu2 ,grup_kod_3=grupkodu3,
            silinme_bilgisi = False,muhkodu = muhkodu,tevkifatkodu  = tevkifatkodu
        )
        cari_kartislemleri_adresleri_kimlik.objects.create(
            cari_bilgisi = get_object_or_404(cari_kartlar,id = yeni_cari_karti_olusturma.id ),
            adres1 = adres1 ,ilce = ilce1 ,il = sehir1 ,telefon = telefon1 ,
            faks = faks ,telefon2 = telefon2 ,Telefon3 = telefon3 ,
            gsm1  = gsm1 ,gsm2 = gsm2 , posta_kodu = postakodu ,
            ulke = get_object_or_404(ulke_ulke_kodlari,ulke_kodu = ulkekodu ),
            vergi_dairesi =  get_object_or_404(vergi_dairesi,vergi_dairesi_kodu = vdkodu ),
            tc_veya_vergi_no = vergitckimlikno ,eposta_adresi = epostaadresi ,
            web_adresi = webadresi  ,adres2  =adres2 ,ilce2 = ilce2 ,
            il2 = sehir2 ,telefon4  =telefon4 ,faks2 = faks2 ,
            gsm3 = gsm3 ,telefon5 = telefon5 ,
            ulke2 = ulke ,posta_kodu2 = postakodu2 ,
            adi=adi,soyadi=soyadi,babaadi=babaadi,anneadi=anneadi,
            dogum_yeri=dogumyeri,dogum_tarihi=dogumtarihi,cinsiyet= cinsiyet,
            seri_no=serino,ssk_bagkur_no=sskbagkurno 
        )
        cari_kartislemleri_diger_bilgiler.objects.create(
            cari_bilgisi = get_object_or_404(cari_kartlar,id = yeni_cari_karti_olusturma.id ),
            risklimiti = risklimiti,digerdovizcinsi = digerdovizcinsi,faizvadefarki = faizvadefarki,
            odemesuresigun = odemesuresigun,iskontoorani = float(iskontoorani),karorani = float(karorani),
            taksitsayisi = int(taksitsayisi),taksitodemegunuherayin = taksitodemegunuherayin,satisfiyati = satisfiyati,
            alisfiyati = alisfiyati, stokgrupkodu = stokgrupkodu,iskontoorani2 = float(iskontoorani2),
            indim1 = indim1,indim2 = indim2,indim3 = indim3,indim4 = indim4,indim5 = indim5,indim6 = indim6,
            uygunkursecenek = uygunkursecenek,bankaadi = bankaadi ,subesi = subesi,bankadovizcinsi = bankadovizcinsi,
            hesapno = hesapno,iban = iban
        )
        cari_kartislemleri_sube_bilgiler.objects.create(
            cari_bilgisi = get_object_or_404(cari_kartlar,id = yeni_cari_karti_olusturma.id ),
            subebilgilerisubekodu = subebilgilerisubekodu,subebilgilerisubeadi=subebilgilerisubeadi,
            subebilgileridovizcinsi = subebilgileridovizcinsi,subebilgileriborctutari = float(subebilgileriborctutari),
            subebilgilerialacaktutari = float(subebilgilerialacaktutari),subebilgileribakiyetutari = float(subebilgileribakiyetutari),
            subebilgileriba = subebilgileriba,subebilgilerivadetarihi = subebilgilerivadetarihi,
            subebilgileriadres = subebilgileriadres,subebilgilerisehir =subebilgilerisehir,subebilgilerisemt =subebilgilerisemt,
            subebilgileritelefon= subebilgileritelefon,subebilgileriyetkili = subebilgileriyetkili,
            subebilgileriodemesuresi = subebilgileriodemesuresi,subebilgilerivadehesapyonetimi = subebilgilerivadehesapyonetimi,
            subebilgilerimuhkodu = subebilgilerimuhkodu,subebilgileripostakodu = subebilgileripostakodu        
            )
        cari_kartislemleri_notlar.objects.create(
            cari_bilgisi = get_object_or_404(cari_kartlar,id = yeni_cari_karti_olusturma.id ),
            notlartarihi = notlartarihi,notlarsatici = notlarsatici,notlarnot =notlarnot
        )
        cari_kartislemleri_firma_gorevilisi.objects.create(
            cari_bilgisi = get_object_or_404(cari_kartlar,id = yeni_cari_karti_olusturma.id ),
            firmagoreviadi = firmagoreviadi, firmagorevligorevi = firmagorevligorevi,
            firmagorevliistelefonu = firmagorevliistelefonu,firmagorevlidahilinumara = firmagorevlidahilinumara,
            firmagorevligsm = firmagorevligsm
        )
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/yenicari.html",content)
def cari_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    kart = get_object_or_404(cari_kartlar,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
  

    cari_kartlar.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/cari/"
    return redirect(link)
#Cari İşlemeler
#Stok İşlemleri
def stok_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"stok/stok.html",content)

def yeni_stok_karti(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["kdv_istisna"] = kdv_istisna_kodu.objects.all()
    content["stoklar"] = stok_kartlar.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        anastokkarti  = request.POST.get("anastokkarti")
        detay = request.POST.get("detay")
        listedegorunme = request.POST.get("listedegorunme")
        stokkilidi = request.POST.get("stokkilidi")
        stokadi = request.POST.get("stokadi")
        stokturu=  request.POST.get("stokturu")
        stokkodu = request.POST.get("stokkodu")
        yeni = stok_kartlar.objects.create(
            ana_stok_kodu = anastokkarti,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            detay  =detay,listede_gorunsun =listedegorunme,stok_kodu  = stokkodu,
            stok_turu = stokturu,stok_hesap_kilitli = stokkilidi,stok_adi =stokadi 
        )
        #stokalisveriş
        birim1 = request.POST.get("birim1")
        birim2 = request.POST.get("birim2")
        birim2adet = request.POST.get("birim2adet")
        carpbol1 = request.POST.get("carpbol1")
        birim3 = request.POST.get("birim3")
        birim3adet = request.POST.get("birim3adet")
        carpbol2 = request.POST.get("carpbol2")
        maxstokbilgisi = request.POST.get("maxstokbilgisi")
        minstokbilgisi = request.POST.get("minstokbilgisi")
        serbeststokbirimi = request.POST.get("serbeststokbirimi")
        gunbilgisi = request.POST.get("gunbilgisi")
        indirim1 = request.POST.get("indirim1")
        indirim2 = request.POST.get("indirim2")
        indirim3 = request.POST.get("indirim3")
        satisbirimi = request.POST.get("satisbirimi")
        alisbirimi = request.POST.get("alisbirimi")
        kdvistisna = request.POST.get("kdvistisna")
        serinokullan = request.POST.get("serinokullan")
        kdvorani = request.POST.get("kdvorani")
        tevkifatorani = request.POST.get("tevkifatorani")
        lotkullanim = request.POST.get("lotkullanim")
        if kdvistisna == "" or kdvistisna == None:
            stok_birim_alis_satis_birimi.objects.create(stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
            birinci_birim = birim1,ikinci_birim  =birim2,ucuncu_birim = birim3,ikinci_birim_deger =birim2adet,
            ucuncu_birim_deger = birim3adet,ikinci_birim_islem = carpbol1,ucuncu_birim_islem = carpbol2,
            max_stok_miktari = maxstokbilgisi,min_stok_miktari =minstokbilgisi,serbest_stok_birimi = serbeststokbirimi,
            indirim1 = indirim1 ,indirim2 = indirim2,indirim3 = indirim3,satis_birimi = satisbirimi,temin_gun =gunbilgisi,
            aliss_birimi = alisbirimi ,
            kdv_orani  = kdvorani,tevkifat_orani = tevkifatorani,lot_kullanimi = lotkullanim,serinokullan = serinokullan
            )
        else:
            stok_birim_alis_satis_birimi.objects.create(stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
            birinci_birim = birim1,ikinci_birim  =birim2,ucuncu_birim = birim3,ikinci_birim_deger =birim2adet,
            ucuncu_birim_deger = birim3adet,ikinci_birim_islem = carpbol1,ucuncu_birim_islem = carpbol2,
            max_stok_miktari = maxstokbilgisi,min_stok_miktari =minstokbilgisi,serbest_stok_birimi = serbeststokbirimi,
            indirim1 = indirim1 ,indirim2 = indirim2,indirim3 = indirim3,satis_birimi = satisbirimi,temin_gun =gunbilgisi,
            aliss_birimi = alisbirimi , kdv_istisna_kodu_sec = get_object_or_404(kdv_istisna_kodu,id = kdvistisna),
            kdv_orani  = kdvorani,tevkifat_orani = tevkifatorani,lot_kullanimi = lotkullanim,serinokullan = serinokullan
            )
        #stok bilgileri
        if True:
            satis1 = request.POST.get("satis1")
            satis2 = request.POST.get("satis2")
            satis3 = request.POST.get("satis3")
            satis4 = request.POST.get("satis4")
            satis5 = request.POST.get("satis5")
            satis6 = request.POST.get("satis6")
            satis7 = request.POST.get("satis7")
            satis8 = request.POST.get("satis8")
            satis9 = request.POST.get("satis9")
            satis10 = request.POST.get("satis10")
            satis1dvz = request.POST.get("satis1dvz")
            satis2dvz = request.POST.get("satis2dvz")
            satis3dvz = request.POST.get("satis3dvz")
            satis4dvz = request.POST.get("satis4dvz")
            satis5dvz = request.POST.get("satis5dvz")
            satis6dvz = request.POST.get("satis6dvz")
            satis7dvz = request.POST.get("satis7dvz")
            satis8dvz = request.POST.get("satis8dvz")
            satis9dvz = request.POST.get("satis9dvz")
            satis10dvz = request.POST.get("satis10dvz")
            kullanilacak_satis_fiyati = request.POST.get("kullanilacak_satis_fiyati")
            satisdovizcinsi = request.POST.get("satisdovizcinsi")
            birim_secenegi = request.POST.get("birim_secenegi")
            alis1 = request.POST.get("alis1")
            alis2 = request.POST.get("alis2")
            alis3 = request.POST.get("alis3")
            alis4 = request.POST.get("alis4")
            alis5 = request.POST.get("alis5")
            alis1dvz = request.POST.get("alis1dvz")
            alis2dvz = request.POST.get("alis2dvz")
            alis3dvz = request.POST.get("alis3dvz")
            alis4dvz = request.POST.get("alis4dvz")
            alis5dvz = request.POST.get("alis5dvz")
            kullanilacak_alis_fiyati = request.POST.get("kullanilacak_alis_fiyati")
            alisdovizcinsi = request.POST.get("alisdovizcinsi")
            alissatisaciklama = request.POST.get("alissatisaciklama")
            alissatimaliyetyontemi = request.POST.get("alissatimaliyetyontemi")
            alissatiskaryontemi = request.POST.get("alissatiskaryontemi")
            karyuzdesi = request.POST.get("karyuzdesi")
            stok_alis_satis.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                satis_fiyati_1_tl = satis1 ,satis_fiyati_2_tl = satis2 ,satis_fiyati_3_tl =satis3 ,satis_fiyati_4_tl =satis4  ,
                satis_fiyati_5_tl = satis5,satis_fiyati_6_tl = satis6 ,satis_fiyati_7_tl = satis7,
                satis_fiyati_8_tl = satis8,satis_fiyati_9_tl =satis9 ,satis_fiyati_10_tl = satis10,
                satis_fiyati_1_dvz = satis1dvz ,satis_fiyati_2_dvz = satis2dvz ,satis_fiyati_3_dvz =satis3dvz  ,
                satis_fiyati_4_dvz = satis4dvz ,satis_fiyati_5_dvz = satis5dvz ,satis_fiyati_6_dvz = satis6dvz ,
                satis_fiyati_7_dvz = satis7dvz ,satis_fiyati_8_dvz =satis8dvz  ,satis_fiyati_9_dvz = satis9dvz ,
                satis_fiyati_10_dvz =satis10dvz  ,aktif_satis_fiyati = kullanilacak_satis_fiyati ,satis_dovizcinsi =satisdovizcinsi
                ,birim_secenegi = birim_secenegi  ,alis_fiyati_1_tl = alis1 ,alis_fiyati_2_tl = alis2,alis_fiyati_3_tl =alis3 ,
                alis_fiyati_4_tl =alis4 ,alis_fiyati_5_tl = alis5,alis_fiyati_1_dvz =alis1dvz  ,
                alis_fiyati_2_dvz =alis2dvz  ,alis_fiyati_3_dvz =alis3dvz  ,alis_fiyati_4_dvz = alis4dvz ,
                alis_fiyati_5_dvz = alis5dvz ,aktif_alis_fiyati = kullanilacak_alis_fiyati ,alis_dovizcinsi = alisdovizcinsi ,
                aciklama = alissatisaciklama ,maliyet_yontemi = alissatimaliyetyontemi ,satis_kar_evrak = alissatiskaryontemi ,
                satis_kar_yuzdesi =karyuzdesi 
            )
            #stok bilgileri
        if True:
            kodlarozelkod1 = request.POST.get("kodlarozelkod1")
            kodlarozelkod2 = request.POST.get("kodlarozelkod2")
            kodlargrupkodu1 = request.POST.get("kodlargrupkodu1")
            kodlargrupkodu2  = request.POST.get("kodlargrupkodu2")
            kodlargrupkodu3 = request.POST.get("kodlargrupkodu3")
            gtipno = request.POST.get("gtipno")
            kalitekodu = request.POST.get("kalitekodu") 
            kodlarbarkodkodu=  request.POST.get("kodlarbarkodkodu")
            kodlarbirimno = request.POST.get("kodlarbirimno") 
            alternatifstokkodu1 = request.POST.get("alternatifstokkodu1")
            alternatifstokadi1 = request.POST.get("alternatifstokadi1")
            alternatifstokkodu2 = request.POST.get("alternatifstokkodu2") 
            alternatifstokadi2 = request.POST.get("alternatifstokadi2")
            alternatifstokkodu3 = request.POST.get("alternatifstokkodu3") 
            alternatifstokadi3 = request.POST.get("alternatifstokadi3")
            yazarkasadepartmani = request.POST.get("yazarkasadepartmani")
            teraziurunkodu = request.POST.get("teraziurunkodu")
            kodlarplukodu = request.POST.get("kodlarplukodu")
            kodlarreyon = request.POST.get("kodlarreyon")
            kodlarraf1 = request.POST.get("kodlarraf1")
            kodlarraf2 = request.POST.get("kodlarraf2")
            kodlarraf3 = request.POST.get("kodlarraf3")
            stok_kodlari.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                ozel_kod_1 = kodlarozelkod1,ozel_kod_2 = kodlarozelkod2,
                grup_kod_1 = kodlargrupkodu1,grup_kod_2 = kodlargrupkodu2,grup_kod_3= kodlargrupkodu3,
                gtipno=gtipno,kalitekodu = kalitekodu,barkod = kodlarbarkodkodu,brimno=kodlarbirimno,
                alternatifstokkodu = alternatifstokkodu1,alternatifstokadi = alternatifstokadi1,
                alternatifstokkodu2 = alternatifstokkodu2,alternatifstokadi2 = alternatifstokadi2,
                alternatifstokkodu3 = alternatifstokkodu3,alternatifstokadi3 = alternatifstokadi3,
                yazarkasadepartman = yazarkasadepartmani,tazeurunkodu = teraziurunkodu,
                plukodu  = kodlarplukodu,reyon = kodlarreyon,raf1 = kodlarraf1,
                raf2 = kodlarraf2,raf3 = kodlarraf3
            )
        if True:
            parametreadi1  = request.POST.get("parametreadi1")
            parametredegeri = request.POST.get("parametredegeri")
            parametreadi2 = request.POST.get("parametreadi2")
            parametredegeri2 = request.POST.get("parametredegeri2")
            detaylarbarkod = request.POST.get("detaylarbarkod")
            detaylarkalite = request.POST.get("detaylarkalite")
            detaylardetayozellikadi = request.POST.get("detaylardetayozellikadi")
            detaylarvaryantsec = request.POST.get("detaylarvaryantsec")
            detaylarvaryantkodu = request.POST.get("detaylarvaryantkodu")
            detaylisecilimi = request.POST.get("detaylisecilimi")
            detaylarvaryantkodutablo = request.POST.get("detaylarvaryantkodutablo")
            ozellik1 = request.POST.get("ozellik1")
            ozellik2 = request.POST.get("ozellik2")
            ozellik3 = request.POST.get("ozellik3")
            ozellik4 = request.POST.get("ozellik4")
            ozellik5 = request.POST.get("ozellik5")
            ozellik6 = request.POST.get("ozellik6")
            ozellik7 = request.POST.get("ozellik7")
            ozellik8 = request.POST.get("ozellik8")
            ozellik9 = request.POST.get("ozellik9")
            ozellik10 = request.POST.get("ozellik10")
            ozellik11 = request.POST.get("ozellik11")
            ozellik12 = request.POST.get("ozellik12")
            ozellik13 = request.POST.get("ozellik13")
            ozellik14 = request.POST.get("ozellik14")
            ozellik15 = request.POST.get("ozellik15")
            ozellik16 = request.POST.get("ozellik16")
            ozellik17 = request.POST.get("ozellik17")
            ozellik18 = request.POST.get("ozellik18")
            ozellik19 = request.POST.get("ozellik19")
            ozellik20 = request.POST.get("ozellik20")
            ozellik21 = request.POST.get("ozellik21")
            ozellik22 = request.POST.get("ozellik22")
            ozellik23 = request.POST.get("ozellik23")
            ozellik24 = request.POST.get("ozellik24")
            ozellik25 = request.POST.get("ozellik25")
            ozellik26 = request.POST.get("ozellik26")
            ozellik27 = request.POST.get("ozellik27")
            ozellik28 = request.POST.get("ozellik28")
            ozellik29 = request.POST.get("ozellik29")
            ozellik30 = request.POST.get("ozellik30")
            stok_detaylari.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                parametreadi1 = parametreadi1,paremetredegeri1= parametredegeri,
                parametreadi2 = parametreadi2,paremetredegeri2 = parametredegeri2,
                barkod = detaylarbarkod,kalite = detaylarkalite,
                detayozellikadi = detaylardetayozellikadi,varyant = detaylarvaryantsec,
                varyantkodu = detaylarvaryantkodu,secili = detaylisecilimi,
                varyantkodu2 = detaylarvaryantkodutablo,
                ozellik1 = ozellik1,ozellik2 = ozellik2,ozellik3 = ozellik3,
                ozellik4 = ozellik4,ozellik5 = ozellik5, ozellik6 = ozellik6,
                ozellik7 = ozellik7,ozellik8 = ozellik8,ozellik9 = ozellik9,
                ozellik10 = ozellik10,ozellik11 = ozellik11,ozellik12 = ozellik12,ozellik13 = ozellik13,
                ozellik14 = ozellik14,ozellik15 = ozellik15,ozellik16 = ozellik16,ozellik17 = ozellik17,
                ozellik18 = ozellik18,ozellik19 = ozellik19,ozellik20 = ozellik20,
                ozellik21 = ozellik21,ozellik22 = ozellik22,ozellik23 = ozellik23,
                ozellik24 = ozellik24,ozellik25 = ozellik25,ozellik26 = ozellik26,
                ozellik27 = ozellik27,ozellik28 = ozellik28,ozellik29 = ozellik29,ozellik30 = ozellik30
            )
        if True:
            stokrecetesien = request.POST.get("stokrecetesien")
            stokrecetesiboy = request.POST.get("stokrecetesiboy")
            stokrecetesikalinlik = request.POST.get("stokrecetesikalinlik")
            stokrecetesicevrilecekbirim = request.POST.get("stokrecetesicevrilecekbirim")
            stokrecetesibolunmekatsayisi = request.POST.get("stokrecetesibolunmekatsayisi")
            stokrecetesiislemsonucu = request.POST.get("stokrecetesiislemsonucu")
            stokrecetesistokbirimi = request.POST.get("stokrecetesistokbirimi")
            stokrecetesiozgulagirlik = request.POST.get("stokrecetesiozgulagirlik")  
            recete_miktari = request.POST.get("recete_miktari")
            fr = request.POST.get("fr")
            if fr == "on":
                fr = True
            else:
                fr = False
            recete_brim_maliyeti = request.POST.get("recete_brim_maliyeti")
            stokrecetesistokid = request.POST.get("stokrecetesistokid")
            stokrecetesibirim = request.POST.get("stokrecetesibirim")
            stokrecetesitur = request.POST.get("stokrecetesitur")
            stokrecetesimiktar = request.POST.get("stokrecetesimiktar")
            stokrecetesidovizcinsi = request.POST.get("stokrecetesidovizcinsi")
            birimfiyatitl = request.POST.get("birimfiyatitl")
            birimfiyatidvz = request.POST.get("birimfiyatidvz")
            fireyuzde = request.POST.get("fireyuzde")
            firemiktari=  request.POST.get("firemiktari")
            stokgideryuzdesi = request.POST.get("stokgideryuzdesi")
            stokrecetesiguncellemetarihi = request.POST.get("stokrecetesiguncellemetarihi")
            satis_aninda_miktar_kadar_uretim_yap= request.POST.get("satis_aninda_miktar_kadar_uretim_yap")
            if satis_aninda_miktar_kadar_uretim_yap == "on":
                satis_aninda_miktar_kadar_uretim_yap = True
            else:
                satis_aninda_miktar_kadar_uretim_yap = False
            uretimden_giriste_sarf_kaydi_yap = request.POST.get("uretimden_giriste_sarf_kaydi_yap")
            if uretimden_giriste_sarf_kaydi_yap == "on":
                uretimden_giriste_sarf_kaydi_yap = True
            else:
                uretimden_giriste_sarf_kaydi_yap = False
            sarf_kaydi_hesaplama_yontemi = request.POST.get("sarf_kaydi_hesaplama_yontemi")
            stok_recetesi.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                brim_en = stokrecetesien,brim_boy = stokrecetesiboy,
                brim_kalinlik =stokrecetesikalinlik ,brim_cevrilecek_brim = stokrecetesicevrilecekbirim,
                brim_bolunme_katsayisi = stokrecetesibolunmekatsayisi,brim_islem_sonucu  =stokrecetesiislemsonucu ,
                stok_brimi = stokrecetesistokbirimi,ozgul_agirlik = stokrecetesiozgulagirlik,
                recete_miktari = recete_miktari,f_r = fr,recete_brim_maliyeti = recete_brim_maliyeti,
                stok_kodu = get_object_or_404(stok_kartlar,id = stokrecetesistokid),
                brim_bilgisi = stokrecetesibirim,tur=stokrecetesitur,miktar =stokrecetesimiktar,
                doviz_cinsi = stokrecetesidovizcinsi,brim_fiyati_tl = birimfiyatitl,
                birim_fiyati_dvz = birimfiyatidvz,fire_yuzdesi = fireyuzde,
                fire_miktari = firemiktari,gider_yuzdesi = stokgideryuzdesi,
                son_guncelleme_tarihi = stokrecetesiguncellemetarihi,
                satis_aninda_miktar_kadar_uretim_yap = satis_aninda_miktar_kadar_uretim_yap,
                uretimden_giriste_sarf_kaydi_yap = uretimden_giriste_sarf_kaydi_yap,
                sarf_kaydi_hesaplama_yontemi = sarf_kaydi_hesaplama_yontemi
            )
        if True:
            kodlarmuhgrupkodu = request.POST.get("kodlarmuhgrupkodu")
            kodlaruretime_sevk_kodu = request.POST.get("kodlaruretime_sevk_kodu")
            kodlaruretime_sarf_h_kodu = request.POST.get("kodlaruretime_sarf_h_kodu")
            kodlaruretime_hesap_kodu = request.POST.get("kodlaruretime_hesap_kodu")
            kodlardepo_s_fazlasi_h_kodu = request.POST.get("kodlardepo_s_fazlasi_h_kodu")
            kodlardepo_s_eksikligi_h_kodu = request.POST.get("kodlardepo_s_eksikligi_h_kodu")
            kodlarsarf_hesap_kodu = request.POST.get("kodlarsarf_hesap_kodu")
            stok_olusturmakodlar = stok_muhasabe_kodlari.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                grup_muh_kodu = kodlarmuhgrupkodu,uretime_sevk_kodu=kodlaruretime_sevk_kodu,
                uretime_sarf_h_kodu = kodlaruretime_sarf_h_kodu,uretime_hesap_kodu = kodlaruretime_hesap_kodu,
                depo_s_fazlasi_h_kodu = kodlardepo_s_fazlasi_h_kodu,
                depo_s_eksikligi_h_kodu = kodlardepo_s_eksikligi_h_kodu,
                sarf_hesap_kodu = kodlarsarf_hesap_kodu,
                fire_hesap_kodu  = request.POST.get("kodlarfire_hesap_kodu")
            )
            kodlarevrak = request.POST.getlist('kodlarevrak')
            kodlarkdvbilgisi = request.POST.getlist("kodlarkdvbilgisi")
            kodlartevkifatorani = request.POST.getlist("kodlartevkifatorani")
            kodlarstokhesapkodu = request.POST.getlist("kodlarstokhesapkodu")
            kodlarkdvhesapkodu = request.POST.getlist("kodlarkdvhesapkodu")
            kodlartevkifathesapkodu1 = request.POST.getlist("kodlartevkifathesapkodu1")
            kodlartevkifathesapkodu2 = request.POST.getlist("kodlartevkifathesapkodu2")
            kodlarotvhesapkodu1 = request.POST.getlist("kodlarotvhesapkodu1")
            kodlarotvtescilhesapkodu1 = request.POST.getlist("kodlarotvtescilhesapkodu1")
            print(kodlarevrak)
            for i , j in enumerate(kodlarevrak):
                stok_muhasebe_kodlari_evraklar.objects.create(
                    evrak_bagli_birim = get_object_or_404(stok_muhasabe_kodlari,id = stok_olusturmakodlar.id),
                    evrak_turu = kodlarevrak[i],kdv_orani = kodlarkdvbilgisi[i],
                    tevkifat_orani = kodlartevkifatorani[i],stok_hesap_kodu = kodlarstokhesapkodu[i],
                    kdv_hesap_kodu = kodlarkdvhesapkodu[i],tevkifat_hesap_kodu1 = kodlartevkifathesapkodu1[i]
                    ,tevkifat_hesap_kodu2 = kodlartevkifathesapkodu2[i],otv_hesap_kodu = kodlarotvhesapkodu1[i],
                    otv_tescilb_hesap_kodu = kodlarotvtescilhesapkodu1[i]
                )
        if True:
            iliskiligiderid = request.POST.get("iliskiligiderid")
            iliskiligiderekle = request.POST.get("iliskiligiderekle")
            gideryuzdesi = request.POST.get("gideryuzdesi")
            iliskiligelirid = request.POST.get("iliskiligelirid")
            iliskiligelirekle = request.POST.get("iliskiligelirekle")
            geliryuzdesi = request.POST.get("geliryuzdesi")
            stok_iliskili_gider_gelir.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                gider = get_object_or_404(Giderler,id = iliskiligiderid),
                o_ekle_gider = iliskiligiderekle,gider_orani = gideryuzdesi,
                gelir = get_object_or_404(Gelirler,id = iliskiligelirid),
                o_ekle_gelir = iliskiligelirekle,gelir_orani = geliryuzdesi
            )
        if True:
            digerkisimotvorani = request.POST.get("digerkisimotvorani")
            otvbirimfiyati = request.POST.get("otvbirimfiyati")
            otvdigerkisimotvbirimno = request.POST.get("otvdigerkisimotvbirimno")
            digerkisimotvtahsilorani = request.POST.get("digerkisimotvtahsilorani")
            digerkisimotvtescilorani = request.POST.get("digerkisimotvtescilorani")
            digerkisimimerafonuorani = request.POST.get("digerkisimimerafonuorani")
            digerkisimifireorani = request.POST.get("digerkisimifireorani")
            stok_diger_kismi_otv.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                otv_orani = digerkisimotvorani,otv_brim_fiyati = otvbirimfiyati,
                otv_tahsil_orani = digerkisimotvtahsilorani,otv_tecil_orani = digerkisimotvtescilorani,
                mera_fonu_orani = digerkisimimerafonuorani,fire_orani = digerkisimifireorani,otv_brim_no =otvdigerkisimotvbirimno
            )
        if True:
            digerkisimlaragirliknet = request.POST.getlist("digerkisimlaragirliknet")
            digerkisimlaragirlikbrut = request.POST.getlist("digerkisimlaragirlikbrut")
            digerkisimlaragirlikdara = request.POST.getlist("digerkisimlaragirlikdara")
            digerkisimlaragirlikpmiktari = request.POST.getlist("digerkisimlaragirlikpmiktari")
            digerkisimlaragirlikaciklama = request.POST.getlist("digerkisimlaragirlikaciklama")
            for i  in  range(len(digerkisimlaragirliknet)):
                stok_diger_kismi_agirliklar.objects.create(
                    stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                    net = digerkisimlaragirliknet[i],brut = digerkisimlaragirlikbrut[i],
                    dara = digerkisimlaragirlikdara[i],p_miktari = digerkisimlaragirlikpmiktari[i],
                    p_aciklamasi = digerkisimlaragirlikaciklama[i]
                )
        if True:
            stokdigerkisimbirimno = request.POST.get("stokdigerkisimbirimno")
            stokdigerkisimen = request.POST.get("stokdigerkisimen")
            stokdigerkisimenbirimi = request.POST.get("stokdigerkisimenbirimi")
            stokdigerkisiboy = request.POST.get("stokdigerkisiboy")
            stokdigerkisiboybirimi = request.POST.get("stokdigerkisiboybirimi")
            stokdigerkisiyukseklik = request.POST.get("stokdigerkisiyukseklik")
            stokdigerkisiyukseklikbirimi = request.POST.get("stokdigerkisiyukseklikbirimi")
            stokdigerkisiebatbirimi = request.POST.get("stokdigerkisiebatbirimi")
            stokdigerkisihacim = request.POST.get("stokdigerkisihacim")
            stok_diger_birim_durumu.objects.create(
                stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=yeni.id),
                birim =stokdigerkisimbirimno ,en = stokdigerkisimen,
                en_birimi = stokdigerkisimenbirimi ,boy = stokdigerkisiboy ,
                boy_birimi= stokdigerkisiboybirimi,yukseklik = stokdigerkisiyukseklik,
                yukseklik_birimi =stokdigerkisiyukseklikbirimi ,ebat_birimi = stokdigerkisiebatbirimi ,
                hacim = stokdigerkisihacim
            )
        #stok stok_kodlari
        #stok stok_kodlari
        link = "/"+slug+"/stok/"
        return redirect(link)
    return render(request,"stok/yeni_stok.html",content)

#stok sil
def stok_sil(request,slug,id):
    stokbilgikarti=stok_kartlar.objects.filter(id = id,silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    stokbilgikarti.update(silinme_bilgisi = True)
    link = "/"+slug+"/stok/"
    return redirect(link)
#stok sil
#Stok İşlemleri

#Fatura İşlemleri
def fatura_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        if True:
            grupturu = request.POST.get("grupturu")
            siparisno = request.POST.get("siparisno")
            caribilgisi = request.POST.get("caribilgisi")
            entkodu = request.POST.get("entkodu")
            kdvdurumu = request.POST.get("kdvdurumu")
            satici = request.POST.get("satici")
            sube_bilgisi = request.POST.get("sube")
            dovizcinsi = request.POST.get("dovizcinsi")
            depobilgisi= request.POST.get("depobilgisi")
            tarih_saat = request.POST.get("teslimtarihi")
            yurticiyurtdisi = request.POST.get("yurticiyurtdisi")
            faturatipi = request.POST.get("faturatipi")
            kasa_bilgisi_ = request.POST.get("kasakodu")
            departman = request.POST.get("departman")
            banka_bilgisi = request.POST.get("bankakodu")
            gunlukkur = request.POST.get("gunlukkur")
            uygunkur = request.POST.get("uygunkur")
            toplamtutartl = request.POST.get("toplamtutartl")
            toplamtutarindirim = request.POST.get("toplamtutarindirim")
            toplamtutarkdv = request.POST.get("toplamtutarkdv")
            toplamtutarotv = request.POST.get("toplamtutarotv")
            toplamtutartevkifat = request.POST.get("toplamtutartevkifat")
            toplamtutargvstopaj = request.POST.get("toplamtutargvstopaj")
            toplamtutarmerafonu = request.POST.get("toplamtutarmerafonu")
            toplamtutargenel = request.POST.get("toplamtutargenel")
            toplamtutartldvz = request.POST.get("toplamtutartldvz")
            toplamtutarindirimdvz = request.POST.get("toplamtutarindirimdvz")
            toplamtutarkdvdvz = request.POST.get("toplamtutarkdvdvz")
            toplamtutarotvdvz = request.POST.get("toplamtutarotvdvz")
            toplamtutartevkifatdvz = request.POST.get("toplamtutartevkifatdvz")
            toplamtutargvstopajdvz = request.POST.get("toplamtutargvstopajdvz")
            toplamtutarmerafonudvz = request.POST.get("toplamtutarmerafonudvz")
            toplamtutargeneldvz = request.POST.get("toplamtutargeneldvz")
            siparisislem = fatura_durumlari.objects.create(
                siparis_tur = grupturu,
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                depo  = depobilgisi,ent_kodu = entkodu,kdv_durumu = kdvdurumu,
                fatura_no = siparisno,tarih = tarih_saat,satici = satici,
                cari_unvan = get_object_or_404(cari_kartlar,id = caribilgisi),
                sube_kodu = get_object_or_404(sube,id = sube_bilgisi),
                islem_doviz_cinsi = dovizcinsi,departman = departman,
                gunluk_kur = gunlukkur,uygun_kur = uygunkur,fatura_yeri = yurticiyurtdisi,
                fatura_tipi = faturatipi,kasa = get_object_or_404(Kasa,id = kasa_bilgisi_),
                banka = get_object_or_404(banka,id = banka_bilgisi),tutar_doviz = toplamtutartldvz,
                tutar_tl = toplamtutartl,kdv_doviz = toplamtutarkdvdvz,kdv_tutari = toplamtutarkdv,
                indirim_tutari = toplamtutarindirim,genel_tutari = toplamtutargenel
            )
        if True:
            siparisturu = request.POST.getlist("siparisturu")
            stok = request.POST.getlist("stok")
            stokmiktari = request.POST.getlist("stokmiktari")
            birimbilgisi = request.POST.getlist("birimbilgisi")
            birimfiyatdovz = request.POST.getlist("birimfiyatdovz")
            stokbirimfiyati = request.POST.getlist("stokbirimfiyati")
            stokindirimyuzdesi = request.POST.getlist("stokindirimyuzdesi")
            stokindirimtl = request.POST.getlist("stokindirimtl")
            stoktutari = request.POST.getlist("stoktutari")
            vergisiztutar = request.POST.getlist("vergisiztutar")
            stokkdvyuzdesi = request.POST.getlist("stokkdvyuzdesi")
            stokkdvtl = request.POST.getlist("stokkdvtl")
            stokkdvistisnayuzdesi = request.POST.getlist("stokkdvistisnayuzdesi")
            stokkdvistisnatl = request.POST.getlist("stokkdvistisnatl")
            stokkdvistisnakodu = request.POST.getlist("stokkdvistisnakodu")
            stokkdvistisnaaciklamasi = request.POST.getlist("stokkdvistisnaaciklamasi")
            stoktevkifatkodu = request.POST.getlist("stoktevkifatkodu")
            stoktevkifatyuzdesi = request.POST.getlist("stoktevkifatyuzdesi")
            stoktevkifattl = request.POST.getlist("stoktevkifattl")
            stokotvmatrahitl = request.POST.getlist("stokotvmatrahitl")
            stokotvyuzdesi = request.POST.getlist("stokotvyuzdesi")
            stokotvbirimtl = request.POST.getlist("stokotvbirimtl")
            stokotvtl = request.POST.getlist("stokotvtl")
            stokotvkodu = request.POST.getlist("stokotvkodu")
            stokotvtahsilyuzdesi = request.POST.getlist("stokotvtahsilyuzdesi")
            stokotvtecillyuzdesi = request.POST.getlist("stokotvtecillyuzdesi")
            stokotvistisnakodu = request.POST.getlist("stokotvistisnakodu")
            stokotvtevkifatyuzdesi = request.POST.getlist("stokotvtevkifatyuzdesi")
            stokgvstopajyuzdesi = request.POST.getlist("stokgvstopajyuzdesi")
            stokmerafonuyuzdesi = request.POST.getlist("stokmerafonuyuzdesi")
            stokmerafonututari = request.POST.getlist("stokmerafonututari")
            stokmuhtasarkodu = request.POST.getlist("stokmuhtasarkodu")
            stokkdvmuhtasarkodu = request.POST.getlist("stokkdvmuhtasarkodu")
            stoksatiraciklamasi = request.POST.getlist("stoksatiraciklamasi")
            stokkampanyakodu = request.POST.getlist("stokkampanyakodu")
            stokmfmiktari = request.POST.getlist("stokmfmiktari")
            stokozelkod1 = request.POST.getlist("stokozelkod1")
            stokozelkod2 = request.POST.getlist("stokozelkod2")
            vadetarihi = request.POST.getlist("vadetarihi")
            stokindirim1 = request.POST.getlist("stokindirim1")
            stokindirim2 = request.POST.getlist("stokindirim2")
            stokindirim3 = request.POST.getlist("stokindirim3")
            stokbirimi = request.POST.getlist("stokbirimi")
            stokmiktaribilgisi = request.POST.getlist("stokmiktaribilgisi")
            stokozellik1 = request.POST.getlist("stokozellik1")
            stokozellik2 = request.POST.getlist("stokozellik2")
            stokozellik3 = request.POST.getlist("stokozellik3")
            stokozellik4 = request.POST.getlist("stokozellik4")
            stokozellik5 = request.POST.getlist("stokozellik5")
            stokozellik6 = request.POST.getlist("stokozellik6")
            stokozellik7 = request.POST.getlist("stokozellik7")
            stokozellik8 = request.POST.getlist("stokozellik8")
            stokozellik9 = request.POST.getlist("stokozellik9")
            stokozellik10 = request.POST.getlist("stokozellik10")
            stokozellik11 = request.POST.getlist("stokozellik11")
            stokozellik12 = request.POST.getlist("stokozellik12")
            stokozellik13 = request.POST.getlist("stokozellik13")
            stokozellik14 = request.POST.getlist("stokozellik14")
            stokozellik15 = request.POST.getlist("stokozellik15")
            stokozellik16 = request.POST.getlist("stokozellik16")
            stokozellik17 = request.POST.getlist("stokozellik17")
            stokozellik18 = request.POST.getlist("stokozellik18")
            stokozellik19 = request.POST.getlist("stokozellik19")
            stokozellik20 = request.POST.getlist("stokozellik20") 
            stokalternatifstokkodu = request.POST.getlist("stokalternatifstokkodu")
            stokalternatifstokadi = request.POST.getlist("stokalternatifstokadi")
            stokserino = request.POST.getlist("stokserino")
            stokteslimdurumu = request.POST.getlist("stokteslimdurumu")
            stokoivkodu = request.POST.getlist("stokoivkodu")
            netagirlik = request.POST.getlist("netagirlik")
            brutagirlik = request.POST.getlist("brutagirlik")
            pkmiktari = request.POST.getlist("pkmiktari")
            pkaciklamasi = request.POST.getlist("pkaciklamasi")
            kalite = request.POST.getlist("kalite")
            stokpartikodu = request.POST.getlist("stokpartikodu")
            sonkullanimtarihi = request.POST.getlist("sonkullanimtarihi")
            aciklama = request.POST.getlist("aciklama")
            irsaliyeno = request.POST.getlist("irsaliyeno")
            irsaliyetarihi = request.POST.getlist("irsaliyetarihi")
            malkabulno = request.POST.getlist("malkabulno")
            for i in range(len(stok)):
                    if  stok[i] == "":
                        pass
                    else:
                        """fatura_olustur.objects.create(
                            grup_kodu = get_object_or_404(siparisislem_durumlari,id = siparisislem.id),
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            tip = siparisturu[i],stok_karti_bilgisi = get_object_or_404(stok_kartlar,id = stok[i].id),
                            miktar = stokmiktari[i],birim = birimbilgisi[i],birim_fiyat_dvz = birimfiyatdovz[i],
                            birim_fiyat_tl  = stokbirimfiyati[i],indirim_yuzdesi  = stokindirimyuzdesi[i],
                            indirim_tutari_tl  = stokindirimtl[i],kdv_yuzdesi = stokkdvyuzdesi[i],
                            kdv_tutari_tl  = stokkdvtl[i],otv_yuzdesi  = stokotvyuzdesi[i],otv_tutari_tl  =stokotvtl[i],
                            stoktutari =  stoktutari[i],indirim1  = stokindirim1[i],indirim2=stokindirim2[i] ,indirim3=stokindirim3[i],
                            satir_aciklamasi = stoksatiraciklamasi[i],serino  = stokserino[i],
                            s_brim  = stokbirimi[i],durumu  =stokteslimdurumu[i],ozellik1 = stokozellik1[i], 
                            ozellik2 = stokozellik2[i], ozellik3 = stokozellik3[i], ozellik4 = stokozellik4[i],
                            ozellik5 = stokozellik5[i], ozellik6 = stokozellik6[i], ozellik7 = stokozellik7[i],
                            ozellik1 = stokozellik1[i], ozellik1 = stokozellik1[i], ozellik1 = stokozellik1[i],   
                        
                        )"""
                        pass
    return render(request,"fatura/fatura.html",content)
#Fatura İşlemleri

#Sipariş Sayfası
def siparis_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = siparisislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    
    if request.POST:
        if True:
            grupturu=  request.POST.get("grupturu")
            siparisno = request.POST.get("siparisno")
            caribilgisi = request.POST.get("caribilgisi")
            entkodu = request.POST.get("entkodu")
            kdvdurumu = request.POST.get("kdvdurumu")
            satici = request.POST.get("satici")
            sube_bilgisi = request.POST.get("sube")
            dovizcinsi = request.POST.get("dovizcinsi")
            depobilgisi = request.POST.get("depobilgisi")
            teslimtarihi = request.POST.get("teslimtarihi")
            teslimsekili = request.POST.get("teslimsekili")
            departman = request.POST.get("departman")
            uygunkur = request.POST.get("uygunkur")
            gunlukkur = request.POST.get("gunlukkur")
            ikdvtutari = request.POST.get("ikdvtutari")
            iindirimtutari = request.POST.get("iindirimtutari")
            igeneltutar = request.POST.get("igeneltutar")
            igeneltoplam = request.POST.get("igeneltoplam")
            iotvtutari = request.POST.get("iotvtutari")
            iindirimtutaridvz = request.POST.get("iindirimtutaridvz")
            igeneltutardvz = request.POST.get("igeneltutardvz")
            igeneltoplamdvz = request.POST.get("igeneltoplamdvz")
            iotvtutaridvz = request.POST.get("iotvtutaridvz")
            siparisislem = siparisislem_durumlari.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                siparis_tur= grupturu ,ent_kodu = entkodu,kdv_durumu = kdvdurumu,
                siparis_no = siparisno,satici = satici,cari_unvan = get_object_or_404(cari_kartlar,id = caribilgisi),
                sube_kodu = get_object_or_404(sube,id = sube_bilgisi),islem_doviz_cinsi  = dovizcinsi,
                depo = depobilgisi,departman = departman,tarih  = teslimtarihi,teslim_sekli = teslimsekili,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
                otv_tutari = iotvtutari,kdv_tutari = ikdvtutari,indirim_tutari =iindirimtutari,
                tutar_tl =  igeneltutar,genel_tutari = igeneltoplam,tutar_doviz = igeneltoplamdvz,irsaliye_durumu="Bekliyor"
            )
            if True:
                stokbilgisi = request.POST.getlist("stok")
                stokbilgisiii = request.POST.get("stok")
                siparisturu = request.POST.getlist("siparisturu")
                stokmiktari = request.POST.getlist("stokmiktari")
                #stokkalanmiktari = request.POST.getlist("stokkalanmiktari")
                birimbilgisi = request.POST.getlist("birimbilgisi")
                stokbirimfiyati = request.POST.getlist("stokbirimfiyati")
                stokindirimyuzdesi = request.POST.getlist("stokindirimyuzdesi")
                stokindirimtl = request.POST.getlist("stokindirimtl")
                stokkdvyuzdesi = request.POST.getlist("stokkdvyuzdesi")
                stokkdvtl = request.POST.getlist("stokkdvtl")
                stokotvyuzdesi = request.POST.getlist("stokotvyuzdesi")
                stokotvtl = request.POST.getlist("stokotvtl")
                stoktutari = request.POST.getlist("stoktutari")
                stokteslimsekli = request.POST.getlist("stokteslimsekli")
                urunteslimtarihi = request.POST.getlist("urunteslimtarihi")
                stokdurumu = request.POST.getlist("stokdurumu")
                stokindirim1 =request.POST.getlist("stokindirim1")
                stokindirim2 =request.POST.getlist("stokindirim2")
                stokindirim3 =request.POST.getlist("stokindirim3")
                stokozelkod1 =request.POST.getlist("stokozelkod1")
                stokozelkod2 =request.POST.getlist("stokozelkod2")
                stokdepartman =request.POST.getlist("stokdepartman")
                stoksatiraciklamasi = request.POST.getlist("stoksatiraciklamasi")
                stokserino = request.POST.getlist("stokserino")
                stokbirimi = request.POST.getlist("stokbirimi")
                stokmiktaribilgisi = request.POST.getlist("stokmiktaribilgisi")
                stokozellik1 = request.POST.getlist("stokozellik1")
                stokozellik2 = request.POST.getlist("stokozellik2")
                stokozellik3 = request.POST.getlist("stokozellik3")
                stokozellik4 = request.POST.getlist("stokozellik4")
                stokozellik5 = request.POST.getlist("stokozellik5")
                stokalternatifstokkodu = request.POST.getlist("stokalternatifstokkodu")
                stokalternatifstokadi = request.POST.getlist("stokalternatifstokadi")
                stokkalitekodu = request.POST.getlist("stokkalitekodu")
                stokanamiktari = request.POST.getlist("stokanamiktari")
                stokanamiktaribirimfiyattl = request.POST.getlist("stokanamiktaribirimfiyattl")
                stokanamiktaribirimfiyatdvz = request.POST.getlist("stokanamiktaribirimfiyatdvz")
                stokpartikodu = request.POST.getlist("stokpartikodu")
                sonkullanimtarihi = request.POST.getlist("sonkullanimtarihi")
                birimfiyatdovz =  request.POST.getlist("birimfiyatdovz")
                
                for i in range(len(stokbilgisi)):
                    if  stokbilgisi[i] == "":
                        pass
                    else:
                        siparis_olustur.objects.create(
                            grup_kodu = get_object_or_404(siparisislem_durumlari,id = siparisislem.id),
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=stokbilgisi[i]),
                            tip = siparisturu[i],birim = birimbilgisi[i],birim_fiyat_tl = stokbirimfiyati[i],
                            miktar = stokmiktari[i],indirim_yuzdesi = stokindirimyuzdesi[i],
                            indirim_tutari_tl = stokindirimtl[i],kdv_yuzdesi = stokkdvyuzdesi[i],
                            kdv_tutari_tl = stokkdvtl[i],otv_yuzdesi = stokotvyuzdesi[i],
                            otv_tutari_tl = stokotvtl[i],indirim1 = stokindirim1[i],indirim2 = stokindirim2[i],
                            indirim3 = stokindirim3[i],durumu  =stokdurumu[i],teslim_tarihi = urunteslimtarihi[i],
                            teslim_sekli=stokteslimsekli[i],ozelkod1 = stokozelkod1[i],ozelkod2 = stokozelkod2[i],
                            departman = stokdepartman[i],satir_aciklamasi  =stoksatiraciklamasi[i],
                            serino = stokserino[i],s_brim = stokbirimi[i],s_miktar = stokmiktaribilgisi[i],
                            alternatifstokkodu =stokalternatifstokkodu[i], alternatifstokadi = stokalternatifstokadi[i],
                            kalite = stokkalitekodu[i],ozellik1  = stokozellik1[i],ozellik2  = stokozellik2[i],
                            ozellik3  =stokozellik3[i],ozellik4  = stokozellik4[i],ozellik5  = stokozellik5[i],
                            ana_miktar = stokanamiktari[i],ana_birim_fiyat_tl = stokanamiktaribirimfiyattl[i],
                            ana_birim_fiyat_dvz = stokanamiktaribirimfiyatdvz[i],parti_kodu  =stokpartikodu[i],
                            son_kullanim_tarihi = sonkullanimtarihi[i],stoktutari = stoktutari[i],birim_fiyat_dvz = birimfiyatdovz[i]

                            )
                    print([i])
        link = "/"+slug+"/siparis/"
        return redirect(link)
    return render(request,"siparis/siparis.html",content)
#siparis düzeltme
def siparis_sayfasi_duzeltme(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = siparisislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    content["duzeltileceksiparis"] =  siparis_olustur.objects.filter(grup_kodu = get_object_or_404(siparisislem_durumlari,id = id),bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    
    if request.POST:
        if True:
            grupturu=  request.POST.get("grupturu")
            siparisno = request.POST.get("siparisno")
            caribilgisi = request.POST.get("caribilgisi")
            entkodu = request.POST.get("entkodu")
            kdvdurumu = request.POST.get("kdvdurumu")
            satici = request.POST.get("satici")
            sube_bilgisi = request.POST.get("sube")
            dovizcinsi = request.POST.get("dovizcinsi")
            depobilgisi = request.POST.get("depobilgisi")
            teslimtarihi = request.POST.get("teslimtarihi")
            teslimsekili = request.POST.get("teslimsekili")
            departman = request.POST.get("departman")
            uygunkur = request.POST.get("uygunkur")
            gunlukkur = request.POST.get("gunlukkur")
            ikdvtutari = request.POST.get("ikdvtutari")
            iindirimtutari = request.POST.get("iindirimtutari")
            igeneltutar = request.POST.get("igeneltutar")
            igeneltoplam = request.POST.get("igeneltoplam")
            iotvtutari = request.POST.get("iotvtutari")
            iindirimtutaridvz = request.POST.get("iindirimtutaridvz")
            igeneltutardvz = request.POST.get("igeneltutardvz")
            igeneltoplamdvz = request.POST.get("igeneltoplamdvz")
            iotvtutaridvz = request.POST.get("iotvtutaridvz")
            siparisislem = siparisislem_durumlari.objects.filter(id=id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False).update(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                siparis_tur= grupturu ,ent_kodu = entkodu,kdv_durumu = kdvdurumu,
                siparis_no = siparisno,satici = satici,cari_unvan = get_object_or_404(cari_kartlar,id = caribilgisi),
                sube_kodu = get_object_or_404(sube,id = sube_bilgisi),islem_doviz_cinsi  = dovizcinsi,
                depo = depobilgisi,departman = departman,tarih  = teslimtarihi,teslim_sekli = teslimsekili,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
                otv_tutari = iotvtutari,kdv_tutari = ikdvtutari,indirim_tutari =iindirimtutari,
                tutar_tl =  igeneltutar,genel_tutari = igeneltoplam,tutar_doviz = igeneltoplamdvz,irsaliye_durumu="Bekliyor"
            )
            if True:
                stokbilgisi = request.POST.getlist("stok")
                siparisturu = request.POST.getlist("siparisturu")
                stokmiktari = request.POST.getlist("stokmiktari")
                #stokkalanmiktari = request.POST.getlist("stokkalanmiktari")
                birimbilgisi = request.POST.getlist("birimbilgisi")
                stokbirimfiyati = request.POST.getlist("stokbirimfiyati")
                stokindirimyuzdesi = request.POST.getlist("stokindirimyuzdesi")
                stokindirimtl = request.POST.getlist("stokindirimtl")
                stokkdvyuzdesi = request.POST.getlist("stokkdvyuzdesi")
                stokkdvtl = request.POST.getlist("stokkdvtl")
                stokotvyuzdesi = request.POST.getlist("stokotvyuzdesi")
                stokotvtl = request.POST.getlist("stokotvtl")
                stoktutari = request.POST.getlist("stoktutari")
                stokteslimsekli = request.POST.getlist("stokteslimsekli")
                urunteslimtarihi = request.POST.getlist("urunteslimtarihi")
                stokdurumu = request.POST.getlist("stokdurumu")
                stokindirim1 =request.POST.getlist("stokindirim1")
                stokindirim2 =request.POST.getlist("stokindirim2")
                stokindirim3 =request.POST.getlist("stokindirim3")
                stokozelkod1 =request.POST.getlist("stokozelkod1")
                stokozelkod2 =request.POST.getlist("stokozelkod2")
                stokdepartman =request.POST.getlist("stokdepartman")
                stoksatiraciklamasi = request.POST.getlist("stoksatiraciklamasi")
                stokserino = request.POST.getlist("stokserino")
                stokbirimi = request.POST.getlist("stokbirimi")
                stokmiktaribilgisi = request.POST.getlist("stokmiktaribilgisi")
                stokozellik1 = request.POST.getlist("stokozellik1")
                stokozellik2 = request.POST.getlist("stokozellik2")
                stokozellik3 = request.POST.getlist("stokozellik3")
                stokozellik4 = request.POST.getlist("stokozellik4")
                stokozellik5 = request.POST.getlist("stokozellik5")
                stokalternatifstokkodu = request.POST.getlist("stokalternatifstokkodu")
                stokalternatifstokadi = request.POST.getlist("stokalternatifstokadi")
                stokkalitekodu = request.POST.getlist("stokkalitekodu")
                stokanamiktari = request.POST.getlist("stokanamiktari")
                stokanamiktaribirimfiyattl = request.POST.getlist("stokanamiktaribirimfiyattl")
                stokanamiktaribirimfiyatdvz = request.POST.getlist("stokanamiktaribirimfiyatdvz")
                stokpartikodu = request.POST.getlist("stokpartikodu")
                sonkullanimtarihi = request.POST.getlist("sonkullanimtarihi")
                birimfiyatdovz =  request.POST.getlist("birimfiyatdovz")
                siparis_olustur.objects.filter(grup_kodu = get_object_or_404(siparisislem_durumlari,id = id),bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).delete()
                for i in range(len(stokbilgisi)):
                    if  stokbilgisi[i] == "":
                        pass
                    else:
                        siparis_olustur.objects.create(
                            grup_kodu = get_object_or_404(siparisislem_durumlari,id = id),
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=stokbilgisi[i]),
                            tip = siparisturu[i],birim = birimbilgisi[i],birim_fiyat_tl = stokbirimfiyati[i],
                            miktar = stokmiktari[i],indirim_yuzdesi = stokindirimyuzdesi[i],
                            indirim_tutari_tl = stokindirimtl[i],kdv_yuzdesi = stokkdvyuzdesi[i],
                            kdv_tutari_tl = stokkdvtl[i],otv_yuzdesi = stokotvyuzdesi[i],
                            otv_tutari_tl = stokotvtl[i],indirim1 = stokindirim1[i],indirim2 = stokindirim2[i],
                            indirim3 = stokindirim3[i],durumu  =stokdurumu[i],teslim_tarihi = urunteslimtarihi[i],
                            teslim_sekli=stokteslimsekli[i],ozelkod1 = stokozelkod1[i],ozelkod2 = stokozelkod2[i],
                            departman = stokdepartman[i],satir_aciklamasi  =stoksatiraciklamasi[i],
                            serino = stokserino[i],s_brim = stokbirimi[i],s_miktar = stokmiktaribilgisi[i],
                            alternatifstokkodu =stokalternatifstokkodu[i], alternatifstokadi = stokalternatifstokadi[i],
                            kalite = stokkalitekodu[i],ozellik1  = stokozellik1[i],ozellik2  = stokozellik2[i],
                            ozellik3  =stokozellik3[i],ozellik4  = stokozellik4[i],ozellik5  = stokozellik5[i],
                            ana_miktar = stokanamiktari[i],ana_birim_fiyat_tl = stokanamiktaribirimfiyattl[i],
                            ana_birim_fiyat_dvz = stokanamiktaribirimfiyatdvz[i],parti_kodu  =stokpartikodu[i],
                            son_kullanim_tarihi = sonkullanimtarihi[i],stoktutari = stoktutari[i],birim_fiyat_dvz = birimfiyatdovz[i]

                            )
        link = "/"+slug+"/siparis/"
        return redirect(link)
    return render(request,"siparis/siparis_duzenleme.html",content)

#siparis düzeltme
#sipariş silme
def siparis_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    siparisislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/siparis/"
    return redirect(link)

def siparis_aktif_pasif_sayfasi(request,slug,id):
    content = site_ayarlari()
    obje = get_object_or_404(siparisislem_durumlari,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    if obje.aktif_pasif:
        siparisislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
                aktif_pasif = False
        )
    else:

        siparisislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
                aktif_pasif = True
        )
    link = "/"+slug+"/siparis/"
    return redirect(link)
def siparis_onaylama_sayfasi(request,slug,id):
    content = site_ayarlari()
    obje = get_object_or_404(siparisislem_durumlari,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    if obje.onay:
        siparisislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
                onay = False
        )
    else:

        siparisislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
                onay = True
        )
    link = "/"+slug+"/siparis/"
    return redirect(link)

#sipariş silme 
#Sipariş Sayfası

#banka
def banka_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["bankalarim"]  = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_yetkilisi"]=banka_yetkilisi.objects.filter(banka_bilgisi__bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_kodlari"]=banka_kodlari.objects.filter(banka_bilgisi__bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_islemleri"] = KasaFisIslemleri.objects.filter(Q(islem_turu="Bankaya Yatırılan") | Q(islem_turu="Bankadan Çekilen") & Q(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)) )
    content["bankada_yapilanfisler"] = bankaFisIslemleri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"banka/banka.html",content)
def yeni_banka_karti(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        bankakodu = request.POST.get("bankakodu")
        entkodu = request.POST.get("entkodu")
        banka_adi = request.POST.get("banka_adi")
        sube_adi = request.POST.get("sube_adi")
        sube_kodu = request.POST.get("sube_kodu")
        hesap_turu = request.POST.get("hesap_turu")
        hesap_adi= request.POST.get("hesap_adi")
        hesap_no = request.POST.get("hesap_no")
        iban_numarasi= request.POST.get("iban_numarasi")
        kullanabilir_kredi_tutari = request.POST.get("kullanabilir_kredi_tutari")
        ozel_kod = request.POST.get("ozel_kod")
        doviz_cinsi = request.POST.get("doviz_cinsi")
        banka_muhasebe_hesap_kodu = request.POST.get("banka_muhasebe_hesap_kodu")
        kredi_kartı_hesap_kodu = request.POST.get("kredi_kartı_hesap_kodu")
        verilen_cekler_hesap_kodu = request.POST.get("verilen_cekler_hesap_kodu")
        tahsil_cekler_hesap_kodu =request.POST.get("tahsil_cekler_hesap_kodu")
        teminat_cekler_hesap_kodu = request.POST.get("teminat_cekler_hesap_kodu")
        tahsil_senetleri_hesap_kodu= request.POST.get("tahsil_senetleri_hesap_kodu")
        teminat_senetleri_hesap_kodu= request.POST.get("teminat_senetleri_hesap_kodu")
        ilgilikisi=  request.POST.get("ilgilikisi")
        telefonbilgisi =request.POST.get("telefonbilgisi")
        adresbilgisi= request.POST.get("adresbilgisi")
        nottarihi = request.POST.get("nottarihi")
        notalma = request.POST.get("not") 
        adi_soyadi = request.POST.get("adi_soyadi")
        gorevi = request.POST.get("gorevi")
        istelefonu = request.POST.get("istelefonu")
        dahili_numara =request.POST.get("dahili_numara")
        gsm = request.POST.get("gsm")
        aciklama =request.POST.get("aciklama")
        tahsilatkodu =request.POST.get("tahsilatkodu")
        tahsilatsekli = request.POST.get("tahsilatsekli")
        taksitadedi= request.POST.get("taksitadedi")
        taksitaralikligun= request.POST.get("taksitaralikligun")
        bankahesabinagecissekli= request.POST.get("bankahesabinagecissekli")
        hesabagecissuresigun= request.POST.get("hesabagecissuresigun")
        carihesapkayitsekli=  request.POST.get("carihesapkayitsekli")
        komisyonorani = request.POST.get("komisyonorani")
        komisyontutari=  request.POST.get("komisyontutari")
        komisyongiderkodu=  request.POST.get("komisyongiderkodu")
        promosyonorani = request.POST.get("promosyonorani")
        promosyontutari = request.POST.get("promosyontutari")
        promosyonkesintisekli= request.POST.get("promosyonkesintisekli")
        promosyongiderkodu  =request.POST.get("promosyongiderkodu")
        hizmetorani =request.POST.get("hizmetorani")
        hizmettutari = request.POST.get("hizmettutari")
        hizmetgiderkodu = request.POST.get("hizmetgiderkodu")
        hizmetkesintisekli = request.POST.get("hizmetkesintisekli")
        kredikartaciklama = request.POST.get("kredikartaciklama")
        taksitgunleri = request.POST.get("taksitgunleri")
        yeni_banka_karti_bilgi = banka.objects.create(
            banka_kodu = bankakodu,entkodu = entkodu,banka_adi= banka_adi,
            sube_adi = sube_adi,sube_kodu = sube_kodu,hesap_turu = hesap_turu,
            hesap_adi = hesap_adi,hesap_no = hesap_no,iban_numarasi = iban_numarasi,
            kullanabilir_kredi_tutari = kullanabilir_kredi_tutari,
            ozel_kod = ozel_kod,doviz_cinsi = doviz_cinsi,
            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            toplam_yatirilan = 0,toplam_cekilen = 0,toplam_bakiye = 0
        )
        banka_kodlari.objects.create(
            banka_bilgisi = get_object_or_404(banka,id = yeni_banka_karti_bilgi.id),
            banka_muhasebe_hesap_kodu = banka_muhasebe_hesap_kodu,kredi_kartı_hesap_kodu = kredi_kartı_hesap_kodu,
            verilen_cekler_hesap_kodu = verilen_cekler_hesap_kodu,tahsil_cekler_hesap_kodu =tahsil_cekler_hesap_kodu,
            tahsil_senetleri_hesap_kodu = tahsil_senetleri_hesap_kodu,teminat_cekler_hesap_kodu = teminat_cekler_hesap_kodu,
            teminat_senetleri_hesap_kodu = teminat_senetleri_hesap_kodu,ilgilikisi = ilgilikisi,telefonbilgisi = telefonbilgisi,
            adresbilgisi = adresbilgisi
        )
        banka_notlari.objects.create(
            banka_bilgisi = get_object_or_404(banka,id = yeni_banka_karti_bilgi.id),
            banka_nottarihi = nottarihi,banka_not = notalma
        )
        banka_yetkilisi.objects.create(
            banka_bilgisi = get_object_or_404(banka,id = yeni_banka_karti_bilgi.id),
            adi_soyadi = adi_soyadi,gorevi = gorevi,istelefonu = istelefonu,
            dahili_numara = dahili_numara,gsm = gsm,aciklama= aciklama

        )
        banka_kredikartibilgileri.objects.create(
            banka_bilgisi = get_object_or_404(banka,id = yeni_banka_karti_bilgi.id),
            tahsilatkodu =tahsilatkodu ,tahsilatsekli = tahsilatsekli, taksitadedi= taksitadedi,
            taksitaralikligun= taksitaralikligun,bankahesabinagecissekli= bankahesabinagecissekli,
            hesabagecissuresigun= hesabagecissuresigun,carihesapkayitsekli=  carihesapkayitsekli,
            komisyonorani = komisyonorani,komisyontutari=  komisyontutari,
            komisyongiderkodu=  komisyongiderkodu,promosyonorani = promosyonorani,promosyontutari = promosyontutari,
            promosyonkesintisekli= promosyonkesintisekli,promosyongiderkodu  =promosyongiderkodu,
            hizmetorani =hizmetorani,hizmettutari = hizmettutari,hizmetgiderkodu = hizmetgiderkodu,
            hizmetkesintisekli = hizmetkesintisekli,kredikartaciklama = kredikartaciklama,
            taksitgunleri = taksitgunleri

        )
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/yenibanka.html",content)

def banka_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    kart = get_object_or_404(banka,id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
  

    banka.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/banka/"
    return redirect(link)
#banka

#kasa Fiş İşlemeleri
#kasa_tahsilat_düzeltildi kasa_odeme_fisi
def kasa_tahsilat_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        print(idbilgisi)
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Tahsilat Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        gelir_bilgisi = get_object_or_404(Gelirler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_kasa = b+float(tutar)
        )
        
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/fisler/tahsilatfisi.html",content)
def kasa_odeme_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_odeme
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Ödeme Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_kasa =  b-float(tutardoviz)
            )
            
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_odeme
            
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Ödeme Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutardoviz ,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_kasa =  b-float(tutar)
            )
            
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/fisler/odemefisi.html",content)
def kasa_virman_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        subebilgisi2 = request.POST.get("subebilgisi2")
        departman2 = request.POST.get("departman2") 
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        kasabilgisi = request.POST.get("kasabilgisi")
        kasabilgisi2 = request.POST.get("kasabilgisi2")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Virman Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        ikinci_kasa_bilgisi =get_object_or_404(Kasa,id=kasabilgisi2),ikinci_departman = departman2,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),ikinci_kasa_muh_kodu = gelirmuhtasarkodu,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz
        )
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(Kasa,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_tahsilat
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            Kasa.objects.filter(id=kasabilgisi2).update(toplam_tahsilat = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(Kasa,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_tahsilat
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
            Kasa.objects.filter(id=kasabilgisi2).update(toplam_tahsilat = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/fisler/virmanfisi.html",content)
def kasa_doviz_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        subebilgisi2 = request.POST.get("subebilgisi2")
        departman2 = request.POST.get("departman2") 
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        kasabilgisi = request.POST.get("kasabilgisi")
        kasabilgisi2 = request.POST.get("kasabilgisi2")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Döviz Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        ikinci_kasa_bilgisi =get_object_or_404(Kasa,id=kasabilgisi2),ikinci_departman = departman2,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),ikinci_kasa_muh_kodu = gelirmuhtasarkodu,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz
        )
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(Kasa,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_tahsilat
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            Kasa.objects.filter(id=kasabilgisi2).update(toplam_tahsilat = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(Kasa,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_tahsilat
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
            Kasa.objects.filter(id=kasabilgisi2).update(toplam_tahsilat = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/fisler/dovizfisi.html",content)
def kasa_acilis_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        borcalacak = request.POST.get("borcalacak")
        tutar_tl= request.POST.get("tutar_tl")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if borcalacak == "B":
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,islem_doviz_cinsi = islemdovizcinsi,tutar_tl= tutar_tl)
        else:
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,alacakbilgisi = borcalacak,islem_doviz_cinsi = islemdovizcinsi,tutar_tl= tutar_tl
            )
        if borcalacak == "B":
            if tutardoviz:
                k = get_object_or_404(Kasa,id=kasabilgisi)
                
                b = k.toplam_bakiye
                k = k.toplam_odeme
                Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            else:
                k = get_object_or_404(Kasa,id=kasabilgisi)
                b = k.toplam_bakiye
                k = k.toplam_odeme
                
                Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
        elif borcalacak == "A":
            if tutardoviz:
                k = get_object_or_404(Kasa,id=kasabilgisi)
                b = k.toplam_bakiye
                k = k.toplam_tahsilat
                
                Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutardoviz),toplam_bakiye = b+float(tutardoviz))
            else:
                k = get_object_or_404(Kasa,id=kasabilgisi)
                b = k.toplam_bakiye
                k = k.toplam_tahsilat
                
                Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/fisler/acilisfisi.html",content)
#kasa_tahsil_düzeltildi kasa_tahsilat_odeme
def kasa_tahsilat_makbuzu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        print(idbilgisi)
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Tahsilat Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        gelir_bilgisi = get_object_or_404(Gelirler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A",tutar_tl = tutar_tl
        )
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/fisler/tahsilatmakbuzu.html",content)
def kasa_tahsilat_odeme(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Ödeme Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl
            )
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_odeme
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
        else:
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Ödeme Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutardoviz ,alacakbilgisi ="B",tutar_tl = tutar_tl
            )
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_odeme
            
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
        link = "/"+slug+"/kasa/"
    return render(request,"kasa/fisler/odememakbuzu.html",content)
def kasa_maas_odeme(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"kasa/fisler/maasodeme.html",content)
#kasa Fiş İşlemeleri
#kasa cari fişleri
def kasa_cari_odeme_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        satici = request.POST.get("satici")
        kampkodu = request.POST.get("kampkodu")
        carisecim = request.POST.get("carisecim")
        carimuhtasarkodu = request.POST.get("carimuhtasarkodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl= request.POST.get("tutar_tl")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Cari Ödeme Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B",tutar_tl = tutar_tl
        )

        k = get_object_or_404(Kasa,id=kasabilgisi)
        b = k.toplam_bakiye
        k = k.toplam_odeme
            
        Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/cari/kasacariodeme.html",content)
def kasa_cari_tahsilat_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        satici = request.POST.get("satici")
        kampkodu = request.POST.get("kampkodu")
        carisecim = request.POST.get("carisecim")
        carimuhtasarkodu = request.POST.get("carimuhtasarkodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl= request.POST.get("tutar_tl")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Cari Tahsilat Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A",tutar_tl = tutar_tl
        )

        k = get_object_or_404(Kasa,id=kasabilgisi)
        b = k.toplam_bakiye
        k = k.toplam_tahsilat
            
        Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/cari/kasacaritahsilat.html",content)
#kasa cari fişleri
#kasa Banka fişleri
def kasa_banka_yatirilan(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")  
        bankabilgisi = request.POST.get("bankabilgisi")
        muhkodukdv = request.POST.get("muhkodukdv")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        gunlukkur = request.POST.get("gunlukkur")    
        uygunkur = request.POST.get("uygunkur")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan = request.POST.get("tahsilatiodemeyiyapan")
        tutardoviz = request.POST.get("tutardoviz")
        tutar = request.POST.get("tutar")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        yatirma = KasaFisIslemleri.objects.create(
            bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Bankaya Yatırılan",tarih = tarih,saat = saat,evrak_no = evrakno,
            ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,banka_bilgisi = get_object_or_404(banka,id = bankabilgisi),
            banka_kasa_muh_kodu = muhkodukdv,birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            tutar_tl = tutar_tl,gunluk_kur = gunlukkur,uygun_kur=uygunkur,alacakbilgisi="B",aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,doviz_tutar = tutardoviz,tutar = tutar,gider_durumu = gider_tutardurumu,
            gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        )  
        if gider_tutardurumu == "Hariç":
            gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = tutardoviz ,doviz_tutar = tutar,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            banka.objects.filter(id=bankabilgisi).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
            banka.objects.filter(id=bankabilgisi).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/banka/kasabankayatirilan.html",content)
def kasa_banka_cekilen(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")  
        bankabilgisi = request.POST.get("bankabilgisi")
        muhkodukdv = request.POST.get("muhkodukdv")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        gunlukkur = request.POST.get("gunlukkur")    
        uygunkur = request.POST.get("uygunkur")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan = request.POST.get("tahsilatiodemeyiyapan")
        tutardoviz = request.POST.get("tutardoviz")
        tutar = request.POST.get("tutar")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        yatirma = KasaFisIslemleri.objects.create(
            bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Bankadan Çekilen",tarih = tarih,saat = saat,evrak_no = evrakno,
            ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,banka_bilgisi = get_object_or_404(banka,id = bankabilgisi),
            banka_kasa_muh_kodu = muhkodukdv,birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            tutar_tl = tutar_tl,gunluk_kur = gunlukkur,uygun_kur=uygunkur,alacakbilgisi="A",aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,doviz_tutar = tutardoviz,tutar = tutar,gider_durumu = gider_tutardurumu,
            gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id= idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        )  
        if gider_tutardurumu == "Hariç":
            gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,gider_kodu = giderkodu,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar =tutar  ,doviz_tutar = tutardoviz ,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl,alacakbilgisi="A"
            )
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_cekilen
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
            banka.objects.filter(id=bankabilgisi).update(toplam_cekilen = tahisi+float(tutardoviz),toplam_bakiye = bak-float(tutardoviz))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_cekilen
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
            banka.objects.filter(id=bankabilgisi).update(toplam_cekilen = tahisi+float(tutar),toplam_bakiye = bak-float(tutar))
        
        link = "/"+slug+"/kasa/"
        return redirect(link)
    return render(request,"kasa/banka/kasabankacekilen.html",content)
#kasa Banka fişleri

#banka fiş işlemleri
def kasadan_bankaya_yatirilan(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")  
        bankabilgisi = request.POST.get("bankabilgisi")
        muhkodukdv = request.POST.get("muhkodukdv")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        gunlukkur = request.POST.get("gunlukkur")    
        uygunkur = request.POST.get("uygunkur")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan = request.POST.get("tahsilatiodemeyiyapan")
        tutardoviz = request.POST.get("tutardoviz")
        tutar = request.POST.get("tutar")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        yatirma = KasaFisIslemleri.objects.create(
            bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Bankaya Yatırılan",tarih = tarih,saat = saat,evrak_no = evrakno,
            ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,banka_bilgisi = get_object_or_404(banka,id = bankabilgisi),
            banka_kasa_muh_kodu = muhkodukdv,birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            tutar_tl = tutar_tl,gunluk_kur = gunlukkur,uygun_kur=uygunkur,alacakbilgisi="B",aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,doviz_tutar = tutardoviz,tutar = tutar,gider_durumu = gider_tutardurumu,
            gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        )  
        if gider_tutardurumu == "Hariç":
            gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = tutardoviz ,doviz_tutar = tutar,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            banka.objects.filter(id=bankabilgisi).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_odeme
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
            banka.objects.filter(id=bankabilgisi).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/kasa/kasabankayatirilan.html",content)
def bankadan_kasaya_yatirilan(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")  
        bankabilgisi = request.POST.get("bankabilgisi")
        muhkodukdv = request.POST.get("muhkodukdv")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        gunlukkur = request.POST.get("gunlukkur")    
        uygunkur = request.POST.get("uygunkur")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan = request.POST.get("tahsilatiodemeyiyapan")
        tutardoviz = request.POST.get("tutardoviz")
        tutar = request.POST.get("tutar")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if tutardoviz:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_cekilen
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
            banka.objects.filter(id=bankabilgisi).update(toplam_cekilen = tahisi+float(tutardoviz),toplam_bakiye = bak-float(tutardoviz))
        else:
            k = get_object_or_404(Kasa,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_tahsilat
            z = get_object_or_404(banka,id=bankabilgisi)
            bak = z.toplam_bakiye
            tahisi = z.toplam_cekilen
            Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
            banka.objects.filter(id=bankabilgisi).update(toplam_cekilen = tahisi+float(tutar),toplam_bakiye = bak-float(tutar))
        
        yatirma = KasaFisIslemleri.objects.create(
            bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Bankadan Çekilen",tarih = tarih,saat = saat,evrak_no = evrakno,
            ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,banka_bilgisi = get_object_or_404(banka,id = bankabilgisi),
            banka_kasa_muh_kodu = muhkodukdv,birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
            tutar_tl = tutar_tl,gunluk_kur = gunlukkur,uygun_kur=uygunkur,alacakbilgisi="A",aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,doviz_tutar = tutardoviz,tutar = tutar,gider_durumu = gider_tutardurumu,
            gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id= idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,islem_sonucu_bakiye_banka  = bak-float(tutar)
        )  
        if gider_tutardurumu == "Hariç":
            gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,gider_kodu = giderkodu,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = KasaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(KasaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar =tutar  ,doviz_tutar = tutardoviz ,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl,alacakbilgisi="A"
            )
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/kasa/kasabankacekilen.html",content)
#banka fiş işlemleri
#banka banka fiş işlemleri
def banka_acilis_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        borcalacak = request.POST.get("borcalacak")
        tutar_tl= request.POST.get("tutar_tl")
        if borcalacak == "B":
            if tutardoviz:
                k = get_object_or_404(banka,id=kasabilgisi)
                
                b = k.toplam_bakiye
                k = k.toplam_cekilen
                banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            else:
                k = get_object_or_404(banka,id=kasabilgisi)
                b = k.toplam_bakiye
                k = k.toplam_cekilen
                
                banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutar),toplam_bakiye = b-float(tutar))
        elif borcalacak == "A":
            if tutardoviz:
                k = get_object_or_404(banka,id=kasabilgisi)
                b = k.toplam_bakiye
                k = k.toplam_yatirilan
                
                banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutardoviz),toplam_bakiye = b+float(tutardoviz))
            else:
                k = get_object_or_404(banka,id=kasabilgisi)
                b = k.toplam_bakiye
                k = k.toplam_yatirilan
                
                banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutar),toplam_bakiye = b+float(tutar))
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if borcalacak == "B":
            bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,islem_doviz_cinsi = islemdovizcinsi,tutar_tl= tutar_tl,islem_sonucu_bakiye_birinci_banka =b-float(tutar))
        else:
            bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,alacakbilgisi = borcalacak,islem_doviz_cinsi = islemdovizcinsi,tutar_tl= tutar_tl,islem_sonucu_bakiye_birinci_banka =b+float(tutar)
            )
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/acilisfisi.html",content)
def banka_virman_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        subebilgisi2 = request.POST.get("subebilgisi2")
        departman2 = request.POST.get("departman2") 
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        kasabilgisi = request.POST.get("kasabilgisi")
        kasabilgisi2 = request.POST.get("kasabilgisi2")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        yatirma =bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Virman Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
        ikinci_banka_bilgisi =get_object_or_404(banka,id=kasabilgisi2),ikinci_departman = departman2,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),ikinci_banka_muh_kodu = gelirmuhtasarkodu,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz
        )
        if gider_tutardurumu == "Hariç":
            gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = tutardoviz ,doviz_tutar = tutar,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        if tutardoviz:
            k = get_object_or_404(banka,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            z = get_object_or_404(banka,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            banka.objects.filter(id=kasabilgisi2).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        else:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            z = get_object_or_404(banka,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutar),toplam_bakiye = b-float(tutar))
            banka.objects.filter(id=kasabilgisi2).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/virmanfisi.html",content)
def banka_doviz_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        subebilgisi2 = request.POST.get("subebilgisi2")
        departman2 = request.POST.get("departman2") 
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        kasabilgisi = request.POST.get("kasabilgisi")
        kasabilgisi2 = request.POST.get("kasabilgisi2")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        yatirma =bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Döviz Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
        ikinci_banka_bilgisi =get_object_or_404(banka,id=kasabilgisi2),ikinci_departman = departman2,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),ikinci_banka_muh_kodu = gelirmuhtasarkodu,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz
        )
        if gider_tutardurumu == "Hariç":
            gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = tutardoviz ,doviz_tutar = tutar,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        if tutardoviz:
            k = get_object_or_404(banka,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            z = get_object_or_404(banka,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            banka.objects.filter(id=kasabilgisi2).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        else:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            z = get_object_or_404(banka,id=kasabilgisi2)
            bak = z.toplam_bakiye
            tahisi = z.toplam_yatirilan
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutar),toplam_bakiye = b-float(tutar))
            banka.objects.filter(id=kasabilgisi2).update(toplam_yatirilan = tahisi+float(tutar),toplam_bakiye = bak+float(tutar))
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/doviz.html",content)
def banka_gelir_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        print(idbilgisi)
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if tutardoviz:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_yatirilan
            
            banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutar),toplam_bakiye = b+float(tutar))
        else:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_yatirilan
            
            banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutar),toplam_bakiye = b+float(tutar))
        bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Gelir Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
        gelir_bilgisi = get_object_or_404(Gelirler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka = b+float(tutar)
        )
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/gelirfisi.html",content)
def banka_gider_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(banka,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Gider Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka =  b-float(tutardoviz)
            )
            
        else:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutar),toplam_bakiye = b-float(tutar))
            bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Gider Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutardoviz ,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka =  b-float(tutar)
            )
            
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/giderfisi.html",content)
def banka_gelir_makbuzu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        print(idbilgisi)
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if tutardoviz:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_yatirilan
            
            banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutar),toplam_bakiye = b+float(tutar))
        else:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_yatirilan
            
            banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutar),toplam_bakiye = b+float(tutar))
        bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Banka Gelir Makbuzu",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
        gelir_bilgisi = get_object_or_404(Gelirler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka = b+float(tutar)
        )
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/gelirmakbuzu.html",content)
def banka_gider_makbuzu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(banka,id=kasabilgisi)
            
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutardoviz),toplam_bakiye = b-float(tutardoviz))
            bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Gider Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka =  b-float(tutardoviz)
            )
            
        else:
            k = get_object_or_404(banka,id=kasabilgisi)
            b = k.toplam_bakiye
            k = k.toplam_cekilen
            
            banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutar),toplam_bakiye = b-float(tutar))
            bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Gider Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutardoviz ,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka =  b-float(tutar)
            )
            
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/fisler/gidermakbuzu.html",content)
#banka fiş işlemleri
#banka cari işlemleri
def banka_cari_gonderilen_havale(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        satici = request.POST.get("satici")
        kampkodu = request.POST.get("kampkodu")
        carisecim = request.POST.get("carisecim")
        carimuhtasarkodu = request.POST.get("carimuhtasarkodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl= request.POST.get("tutar_tl")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        k = get_object_or_404(banka,id=kasabilgisi)
        b = k.toplam_bakiye
        k = k.toplam_cekilen
            
        banka.objects.filter(id=kasabilgisi).update(toplam_cekilen = k+float(tutar),toplam_bakiye = b-float(tutar))
        yatirma = bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Gönderilen Havale",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka =b-float(tutar)
        )
        if gider_tutardurumu == "Hariç":
            gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = tutardoviz ,doviz_tutar = tutar,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/cari/kasacariodeme.html",content)
def banka_cari_gelen_havale(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        satici = request.POST.get("satici")
        kampkodu = request.POST.get("kampkodu")
        carisecim = request.POST.get("carisecim")
        carimuhtasarkodu = request.POST.get("carimuhtasarkodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl= request.POST.get("tutar_tl")
        tutar_tl = request.POST.get("tutar_tl")
        gidertutari = request.POST.get("gidertutari")
        idbilgisi = request.POST.get("idbilgisi")
        gideradi  = request.POST.get("gideradi")
        giderkodu = request.POST.get("giderkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        gideryuzdesi = request.POST.get("gideryuzdesi")
        gider_tutardurumu = request.POST.get("gider_tutardurumu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        k = get_object_or_404(banka,id=kasabilgisi)
        b = k.toplam_bakiye
        k = k.toplam_yatirilan
            
        banka.objects.filter(id=kasabilgisi).update(toplam_yatirilan = k+float(tutar),toplam_bakiye = b+float(tutar))
        yatirma = bankaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Gelen Havale",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_banka =b+float(tutar)
        )
        if gider_tutardurumu == "Hariç":
            gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),tarih = tarih,saat = saat,evrak_no = "00"+str(evrakno),
            ent_kodu = entkodu,
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = gidertutari,doviz_tutar = tutardoviz,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        else:
             gidere_yazma = bankaFisIslemleri.objects.create(
                kendisi_secme = get_object_or_404(bankaFisIslemleri,id = yatirma.id),
                bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                birinci_banka_bilgisi = get_object_or_404(banka,id=kasabilgisi),birinci_banka_muh_kodu =muhtasarkodu,
                gideryuzdesi  = gideryuzdesi,gider_bilgisi = get_object_or_404(Giderler,id  = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,aciklama =gideradi,tutar = tutardoviz ,doviz_tutar = tutar,gider_durumu = gider_tutardurumu,
            tutar_tl = tutar_tl
            )
        
        link = "/"+slug+"/banka/"
        return redirect(link)
    return render(request,"banka/cari/gelenhavale.html",content)
#banka cari işlemleri

#cari fişler 
def cari_borcdekontu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        vadetarih = request.POST.get("vadetarih")
        vadehunu = request.POST.get("vadehunu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.borc_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(borc_tutari = k+float(tutardoviz),bakiye_tutari = b-float(tutardoviz))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Borç Dekontu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b-float(tutardoviz)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu
            )
            
        else:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.borc_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(borc_tutari = k+float(tutar),bakiye_tutari = b-float(tutar))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Borç Dekontu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b-float(tutar)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu)
            
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/borc_dekontu.html",content)

def cari_alacakdekontu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        vadetarih = request.POST.get("vadetarih")
        vadehunu = request.POST.get("vadehunu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.alacak_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutardoviz),bakiye_tutari = b+float(tutardoviz))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Alacak Dekontu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b+float(tutardoviz)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu
            )
            
        else:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.alacak_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutar),bakiye_tutari = b+float(tutar))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Alacak Dekontu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b+float(tutar)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu)
            
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/alacak_dekontu.html",content)

def cari_virman_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        subebilgisi2 = request.POST.get("subebilgisi2")
        departman2 = request.POST.get("departman2") 
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        kasabilgisi = request.POST.get("kasabilgisi")
        kasabilgisi2 = request.POST.get("kasabilgisi2")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if tutardoviz:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            
            b = k.bakiye_tutari
            k = k.alacak_tutari
            z = get_object_or_404(cari_kartlar,id=kasabilgisi2)
            bak = z.bakiye_tutari
            tahisi = z.borc_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutardoviz),bakiye_tutari = b-float(tutardoviz))
            cari_kartlar.objects.filter(id=kasabilgisi2).update(borc_tutari = tahisi+float(tutar),bakiye_tutari = bak+float(tutar))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Virman Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            ikinci_cari_bilgisi =get_object_or_404(cari_kartlar,id=kasabilgisi2),ikinci_departman = departman2,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),ikinci_cari_muh_kodu = gelirmuhtasarkodu,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutardoviz,islem_sonucu_bakiye_birinci_cari = b-float(tutardoviz),islem_sonucu_bakiye_ikinci_cari = bak+float(tutar)
            )
        else:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.alacak_tutari
            z = get_object_or_404(cari_kartlar,id=kasabilgisi2)
            bak = z.bakiye_tutari
            tahisi = z.borc_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutar),bakiye_tutari = b-float(tutar))
            cari_kartlar.objects.filter(id=kasabilgisi2).update(toplam_tahsilat = tahisi+float(tutar),bakiye_tutari = bak+float(tutar))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Virman Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            ikinci_cari_bilgisi =get_object_or_404(cari_kartlar,id=kasabilgisi2),ikinci_departman = departman2,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),ikinci_cari_muh_kodu = gelirmuhtasarkodu,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutardoviz,islem_sonucu_bakiye_birinci_cari = b-float(tutar),islem_sonucu_bakiye_ikinci_cari = bak+float(tutar)
            )
        
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/virman.html",content)
def cari_acilis_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        borcalacak = request.POST.get("borcalacak")
        tutar_tl= request.POST.get("tutar_tl")
        vadetarih = request.POST.get("vadetarih")
        vadehunu = request.POST.get("vadehunu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if borcalacak == "B":
            bakiye = 0
            if tutardoviz:
                k = get_object_or_404(cari_kartlar,id=kasabilgisi)
                
                b = k.bakiye_tutari
                k = k.borc_tutari
                bakiye = b-float(tutardoviz)
                cari_kartlar.objects.filter(id=kasabilgisi).update(borc_tutari = k+float(tutardoviz),bakiye_tutari = b-float(tutardoviz))
            else:
                k = get_object_or_404(cari_kartlar,id=kasabilgisi)
                b = k.bakiye_tutari
                k = k.borc_tutari
                bakiye = b-float(tutar)
                cari_kartlar.objects.filter(id=kasabilgisi).update(borc_tutari = k+float(tutar),bakiye_tutari = b-float(tutar))
        elif borcalacak == "A":
            bakiye = 0
            if tutardoviz:
                k = get_object_or_404(cari_kartlar,id=kasabilgisi)
                b = k.bakiye_tutari
                k = k.alacak_tutari
                bakiye = b+float(tutardoviz)
                cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutardoviz),bakiye_tutari = b+float(tutardoviz))
            else:
                k = get_object_or_404(cari_kartlar,id=kasabilgisi)
                b = k.bakiye_tutari
                k = k.alacak_tutari
                bakiye = b+float(tutar)
                cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutar),bakiye_tutari = b+float(tutar))

        if borcalacak == "B":
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,islem_doviz_cinsi = islemdovizcinsi,tutar_tl= tutar_tl,islem_sonucu_bakiye_birinci_cari = bakiye
            ,vade_tarih = vadetarih,vade_gunu = vadehunu)
        else:
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,alacakbilgisi = borcalacak,islem_doviz_cinsi = islemdovizcinsi,tutar_tl= tutar_tl,islem_sonucu_bakiye_birinci_cari=bakiye
            ,vade_tarih = vadetarih,vade_gunu = vadehunu)
        
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/acilis.html",content)
def cari_borcmakbuzu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        vadetarih = request.POST.get("vadetarih")
        vadehunu = request.POST.get("vadehunu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.borc_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(borc_tutari = k+float(tutardoviz),bakiye_tutari = b-float(tutardoviz))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Borç Makbuzu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b-float(tutardoviz)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu
            )
            
        else:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.borc_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(borc_tutari = k+float(tutar),bakiye_tutari = b-float(tutar))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Borç Makbuzu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="B",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b-float(tutar)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu)
            
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/borcmakbuzu.html",content)

def cari_alacakmakbuzu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        carikodu = request.POST.get("carikodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        gelirkodu = request.POST.get("gelirkodu")
        gelirmuhtasarkodu = request.POST.get("gelirmuhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gideradi = request.POST.get("gideradi")
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl  = request.POST.get("tutar_tl")
        idbilgisi= request.POST.get("idbilgisi")
        vadetarih = request.POST.get("vadetarih")
        vadehunu = request.POST.get("vadehunu")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        
        if tutardoviz:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.alacak_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutardoviz),bakiye_tutari = b+float(tutardoviz))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Alacak Makbuzu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutardoviz),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b+float(tutardoviz)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu
            )
            
        else:
            k = get_object_or_404(cari_kartlar,id=kasabilgisi)
            b = k.bakiye_tutari
            k = k.alacak_tutari
            cari_kartlar.objects.filter(id=kasabilgisi).update(alacak_tutari = k+float(tutar),bakiye_tutari = b+float(tutar))
            cari_fisleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Alacak Makbuzu",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_cari_bilgisi = get_object_or_404(cari_kartlar,id=kasabilgisi),birinci_cari_muh_kodu =muhtasarkodu,
            gider_bilgisi = get_object_or_404(Giderler,id = idbilgisi,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
            ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
            doviz_tutar = tutar,alacakbilgisi ="A",tutar_tl = tutar_tl,islem_sonucu_bakiye_birinci_cari =  b+float(tutar)
            ,vade_tarih = vadetarih,vade_gunu = vadehunu)
            
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/alacak_makbuzu.html",content)
def cari_odeme_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        satici = request.POST.get("satici")
        kampkodu = request.POST.get("kampkodu")
        carisecim = request.POST.get("carisecim")
        carimuhtasarkodu = request.POST.get("carimuhtasarkodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl= request.POST.get("tutar_tl")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Cari Ödeme Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B",tutar_tl = tutar_tl
        )

        k = get_object_or_404(Kasa,id=kasabilgisi)
        b = k.toplam_bakiye
        k = k.toplam_odeme
            
        Kasa.objects.filter(id=kasabilgisi).update(toplam_odeme = k+float(tutar),toplam_bakiye = b-float(tutar))
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/kasacariodeme.html",content)
def cari_tahsilat_fisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    if request.POST:
        tarih = request.POST.get("tarih")
        saat = request.POST.get("saat")
        evrakno = request.POST.get("evrakno")
        entkodu = request.POST.get("entkodu")
        subebilgisi = request.POST.get("subebilgisi")
        ozelkod1 = request.POST.get("ozelkod1")
        ozelkod2 = request.POST.get("ozelkod2")
        departman = request.POST.get("departman")
        satici = request.POST.get("satici")
        kampkodu = request.POST.get("kampkodu")
        carisecim = request.POST.get("carisecim")
        carimuhtasarkodu = request.POST.get("carimuhtasarkodu")
        kasabilgisi = request.POST.get("kasabilgisi")
        muhtasarkodu = request.POST.get("muhtasarkodu")
        islemdovizcinsi = request.POST.get("islemdovizcinsi")
        aciklama = request.POST.get("aciklama")
        tahsilatiodemeyiyapan= request.POST.get("tahsilatiodemeyiyapan")
        tutar = request.POST.get("tutar") 
        gunlukkur = request.POST.get("gunlukkur")
        uygunkur =request.POST.get("uygunkur")
        tutardoviz = request.POST.get("tutardoviz")
        tutar_tl= request.POST.get("tutar_tl")
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Cari Tahsilat Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A",tutar_tl = tutar_tl
        )

        k = get_object_or_404(Kasa,id=kasabilgisi)
        b = k.toplam_bakiye
        k = k.toplam_tahsilat
            
        Kasa.objects.filter(id=kasabilgisi).update(toplam_tahsilat = k+float(tutar),toplam_bakiye = b+float(tutar))
        link = "/"+slug+"/cari/"
        return redirect(link)
    return render(request,"cari/fisler/kasacaritahsilat.html",content)
#
#cari fişler 

#dilekce
def dilekcesayfasi(request,slug):
    content = site_ayarlari()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["dilekcelerimiz"] = dilekceler.objects.filter(bagli_oldugu_firma = None)
    content["dilekceleriniz"] = dilekceler.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"dilekcelersayfasi/dilekce.html",content)
#dilekce
#irsaliye işlemleri
def irsaliye_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    
    if request.POST:
        if True:
            grupturu=  request.POST.get("grupturu")
            siparisno = request.POST.get("siparisno")
            caribilgisi = request.POST.get("caribilgisi")
            entkodu = request.POST.get("entkodu")
            kdvdurumu = request.POST.get("kdvdurumu")
            satici = request.POST.get("satici")
            sube_bilgisi = request.POST.get("sube")
            dovizcinsi = request.POST.get("dovizcinsi")
            depobilgisi = request.POST.get("depobilgisi")
            departman = request.POST.get("departman")
            uygunkur = request.POST.get("uygunkur")
            gunlukkur = request.POST.get("gunlukkur")
            ikdvtutari = request.POST.get("ikdvtutari")
            iindirimtutari = request.POST.get("iindirimtutari")
            igeneltutar = request.POST.get("igeneltutar")
            igeneltoplam = request.POST.get("igeneltoplam")
            igeneltoplamdvz = request.POST.get("igeneltoplamdvz")
            siparisislem = irsaliyeislem_durumlari.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                siparis_tur= grupturu ,ent_kodu = entkodu,kdv_durumu = kdvdurumu,
                siparis_no = siparisno,satici = satici,cari_unvan = get_object_or_404(cari_kartlar,id = caribilgisi),
                sube_kodu = get_object_or_404(sube,id = sube_bilgisi),islem_doviz_cinsi  = dovizcinsi,
                depo = depobilgisi,departman = departman,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
                kdv_tutari = ikdvtutari,indirim_tutari =iindirimtutari,
                tutar_tl =  igeneltutar,genel_tutari = igeneltoplam,tutar_doviz = igeneltoplamdvz
            )
            if True:
                stokbilgisi = request.POST.getlist("stok")
                siparisturu = request.POST.getlist("siparisturu")
                stokmiktari = request.POST.getlist("stokmiktari")
                #stokkalanmiktari = request.POST.getlist("stokkalanmiktari")
                birimbilgisi = request.POST.getlist("birimbilgisi")
                stokbirimfiyati = request.POST.getlist("stokbirimfiyati")
                stokindirimyuzdesi = request.POST.getlist("stokindirimyuzdesi")
                stokindirimtl = request.POST.getlist("stokindirimtl")
                stokkdvyuzdesi = request.POST.getlist("stokkdvyuzdesi")
                stokkdvtl = request.POST.getlist("stokkdvtl")
                stokotvyuzdesi = request.POST.getlist("stokotvyuzdesi")
                stokotvtl = request.POST.getlist("stokotvtl")
                stoktutari = request.POST.getlist("stoktutari")
                stokteslimsekli = request.POST.getlist("stokteslimsekli")
                urunteslimtarihi = request.POST.getlist("urunteslimtarihi")
                stokdurumu = request.POST.getlist("stokdurumu")
                stokindirim1 =request.POST.getlist("stokindirim1")
                stokindirim2 =request.POST.getlist("stokindirim2")
                stokindirim3 =request.POST.getlist("stokindirim3")
                stokozelkod1 =request.POST.getlist("stokozelkod1")
                stokozelkod2 =request.POST.getlist("stokozelkod2")
                stokdepartman =request.POST.getlist("stokdepartman")
                stoksatiraciklamasi = request.POST.getlist("stoksatiraciklamasi")
                stokserino = request.POST.getlist("stokserino")
                stokbirimi = request.POST.getlist("stokbirimi")
                stokmiktaribilgisi = request.POST.getlist("stokmiktaribilgisi")
                stokozellik1 = request.POST.getlist("stokozellik1")
                stokozellik2 = request.POST.getlist("stokozellik2")
                stokozellik3 = request.POST.getlist("stokozellik3")
                stokozellik4 = request.POST.getlist("stokozellik4")
                stokozellik5 = request.POST.getlist("stokozellik5")
                stokalternatifstokkodu = request.POST.getlist("stokalternatifstokkodu")
                stokalternatifstokadi = request.POST.getlist("stokalternatifstokadi")
                stokkalitekodu = request.POST.getlist("stokkalitekodu")
                agirlik = request.POST.getlist("stokanamiktari")
                burutagirlik = request.POST.getlist("stokanamiktaribirimfiyattl")
                pkmiktari = request.POST.getlist("stokanamiktaribirimfiyatdvz")
                stokpartikodu = request.POST.getlist("stokpartikodu")
                sonkullanimtarihi = request.POST.getlist("sonkullanimtarihi")
                birimfiyatdovz =  request.POST.getlist("birimfiyatdovz")
                pkaciklamasi =  request.POST.getlist("pkaciklamasi")
                for i in range(len(stokbilgisi)):
                    if  stokbilgisi[i] == "":
                        pass
                    else:
                        irsaliye_olustur.objects.create(
                            grup_kodu = get_object_or_404(irsaliyeislem_durumlari,id = siparisislem.id),
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=stokbilgisi[i]),
                            tip = siparisturu[i],birim = birimbilgisi[i],birim_fiyat_tl = stokbirimfiyati[i],
                            miktar = stokmiktari[i],indirim_yuzdesi = stokindirimyuzdesi[i],
                            indirim_tutari_tl = stokindirimtl[i],kdv_yuzdesi = stokkdvyuzdesi[i],
                            kdv_tutari_tl = stokkdvtl[i],indirim1 = stokindirim1[i],indirim2 = stokindirim2[i],
                            indirim3 = stokindirim3[i],
                            ozelkod1 = stokozelkod1[i],ozelkod2 = stokozelkod2[i],
                            departman = stokdepartman[i],satir_aciklamasi  =stoksatiraciklamasi[i],
                            serino = stokserino[i],s_brim = stokbirimi[i],s_miktar = stokmiktaribilgisi[i],
                            alternatifstokkodu =stokalternatifstokkodu[i], alternatifstokadi = stokalternatifstokadi[i],
                            kalite = stokkalitekodu[i],ozellik1  = stokozellik1[i],ozellik2  = stokozellik2[i],
                            ozellik3  =stokozellik3[i],ozellik4  = stokozellik4[i],ozellik5  = stokozellik5[i],
                            net_agirlik_kg = agirlik[i],Burut_agirlik_kg = burutagirlik[i],
                            pk_miktari = pkmiktari[i],parti_kodu  =stokpartikodu[i],pk_aciklamasi  =pkaciklamasi[i],
                            son_kullanim_tarihi = sonkullanimtarihi[i],stoktutari = stoktutari[i],birim_fiyat_dvz = birimfiyatdovz[i]

                            )
        link = "/"+slug+"/irsaliye/"
        return redirect(link)
    return render(request,"irsaliye/irsaliye.html",content)

#sipariş silme
def irsaliye_silme_sayfasi(request,slug,id):
    content = site_ayarlari()
    irsaliyeislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/irsaliye/"
    return redirect(link)
#sipariş silme
#siparişi irsaliyeye aktar
def siparisi_irsaliye_aktar(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["siparis_aktarma"] = siparis_olustur.objects.filter(grup_kodu = get_object_or_404(siparisislem_durumlari,id = id),bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["siparis_bilgisi"] = get_object_or_404(siparisislem_durumlari,id = id)
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    
    if request.POST:
        if True:
            grupturu=  request.POST.get("grupturu")
            siparisno = request.POST.get("siparisno")
            caribilgisi = request.POST.get("caribilgisi")
            entkodu = request.POST.get("entkodu")
            kdvdurumu = request.POST.get("kdvdurumu")
            satici = request.POST.get("satici")
            sube_bilgisi = request.POST.get("sube")
            dovizcinsi = request.POST.get("dovizcinsi")
            depobilgisi = request.POST.get("depobilgisi")
            departman = request.POST.get("departman")
            uygunkur = request.POST.get("uygunkur")
            gunlukkur = request.POST.get("gunlukkur")
            ikdvtutari = request.POST.get("ikdvtutari")
            iindirimtutari = request.POST.get("iindirimtutari")
            igeneltutar = request.POST.get("igeneltutar")
            igeneltoplam = request.POST.get("igeneltoplam")
            igeneltoplamdvz = request.POST.get("igeneltoplamdvz")
            siparisislem = irsaliyeislem_durumlari.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                siparis_tur= grupturu ,ent_kodu = entkodu,kdv_durumu = kdvdurumu,
                siparis_no = siparisno,satici = satici,cari_unvan = get_object_or_404(cari_kartlar,id = caribilgisi),
                sube_kodu = get_object_or_404(sube,id = sube_bilgisi),islem_doviz_cinsi  = dovizcinsi,
                depo = depobilgisi,departman = departman,gunluk_kur = gunlukkur,uygun_kur = uygunkur,
                kdv_tutari = ikdvtutari,indirim_tutari =iindirimtutari,
                tutar_tl =  igeneltutar,genel_tutari = igeneltoplam,tutar_doviz = igeneltoplamdvz
            )
            if True:
                stokbilgisi = request.POST.getlist("stok")
                siparisturu = request.POST.getlist("siparisturu")
                stokmiktari = request.POST.getlist("stokmiktari")
                #stokkalanmiktari = request.POST.getlist("stokkalanmiktari")
                birimbilgisi = request.POST.getlist("birimbilgisi")
                stokbirimfiyati = request.POST.getlist("stokbirimfiyati")
                stokindirimyuzdesi = request.POST.getlist("stokindirimyuzdesi")
                stokindirimtl = request.POST.getlist("stokindirimtl")
                stokkdvyuzdesi = request.POST.getlist("stokkdvyuzdesi")
                stokkdvtl = request.POST.getlist("stokkdvtl")
                stokotvyuzdesi = request.POST.getlist("stokotvyuzdesi")
                stokotvtl = request.POST.getlist("stokotvtl")
                stoktutari = request.POST.getlist("stoktutari")
                stokteslimsekli = request.POST.getlist("stokteslimsekli")
                urunteslimtarihi = request.POST.getlist("urunteslimtarihi")
                stokdurumu = request.POST.getlist("stokdurumu")
                stokindirim1 =request.POST.getlist("stokindirim1")
                stokindirim2 =request.POST.getlist("stokindirim2")
                stokindirim3 =request.POST.getlist("stokindirim3")
                stokozelkod1 =request.POST.getlist("stokozelkod1")
                stokozelkod2 =request.POST.getlist("stokozelkod2")
                stokdepartman =request.POST.getlist("stokdepartman")
                stoksatiraciklamasi = request.POST.getlist("stoksatiraciklamasi")
                stokserino = request.POST.getlist("stokserino")
                stokbirimi = request.POST.getlist("stokbirimi")
                stokmiktaribilgisi = request.POST.getlist("stokmiktaribilgisi")
                stokozellik1 = request.POST.getlist("stokozellik1")
                stokozellik2 = request.POST.getlist("stokozellik2")
                stokozellik3 = request.POST.getlist("stokozellik3")
                stokozellik4 = request.POST.getlist("stokozellik4")
                stokozellik5 = request.POST.getlist("stokozellik5")
                stokalternatifstokkodu = request.POST.getlist("stokalternatifstokkodu")
                stokalternatifstokadi = request.POST.getlist("stokalternatifstokadi")
                stokkalitekodu = request.POST.getlist("stokkalitekodu")
                agirlik = request.POST.getlist("stokanamiktari")
                burutagirlik = request.POST.getlist("stokanamiktaribirimfiyattl")
                pkmiktari = request.POST.getlist("stokanamiktaribirimfiyatdvz")
                stokpartikodu = request.POST.getlist("stokpartikodu")
                sonkullanimtarihi = request.POST.getlist("sonkullanimtarihi")
                birimfiyatdovz =  request.POST.getlist("birimfiyatdovz")
                pkaciklamasi =  request.POST.getlist("pkaciklamasi")
                for i in range(len(stokbilgisi)):
                    if  stokbilgisi[i] == "":
                        pass
                    else:
                        irsaliye_olustur.objects.create(
                        grup_kodu = get_object_or_404(irsaliyeislem_durumlari,id = siparisislem.id),
                        bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                        stok_karti_bilgisi = get_object_or_404(stok_kartlar,id=stokbilgisi[i]),
                        tip = siparisturu[i],birim = birimbilgisi[i],birim_fiyat_tl = stokbirimfiyati[i],
                        miktar = stokmiktari[i],indirim_yuzdesi = stokindirimyuzdesi[i],
                        indirim_tutari_tl = stokindirimtl[i],kdv_yuzdesi = stokkdvyuzdesi[i],
                        kdv_tutari_tl = stokkdvtl[i],indirim1 = stokindirim1[i],indirim2 = stokindirim2[i],
                        indirim3 = stokindirim3[i],
                        ozelkod1 = stokozelkod1[i],ozelkod2 = stokozelkod2[i],
                        departman = stokdepartman[i],satir_aciklamasi  =stoksatiraciklamasi[i],
                        serino = stokserino[i],s_brim = stokbirimi[i],s_miktar = stokmiktaribilgisi[i],
                        alternatifstokkodu =stokalternatifstokkodu[i], alternatifstokadi = stokalternatifstokadi[i],
                        kalite = stokkalitekodu[i],ozellik1  = stokozellik1[i],ozellik2  = stokozellik2[i],
                        ozellik3  =stokozellik3[i],ozellik4  = stokozellik4[i],ozellik5  = stokozellik5[i],
                        net_agirlik_kg = agirlik[i],Burut_agirlik_kg = burutagirlik[i],
                        pk_miktari = pkmiktari[i],parti_kodu  =stokpartikodu[i],pk_aciklamasi  =pkaciklamasi[i],
                        son_kullanim_tarihi = sonkullanimtarihi[i],stoktutari = stoktutari[i],birim_fiyat_dvz = birimfiyatdovz[i]

                            )
        link = "/"+slug+"/irsaliye/"
        return redirect(link)
    return render(request,"irsaliye/irsaliyeye_aktar.html",content)

#siparişi irsaliyeye aktar
#irsaliye işlemleri


#irsaliye işlemleri
def genel_muhasebe_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    
    if request.POST:
        if True:
            fistarihi=  request.POST.get("fistarihi")
            grupturu=  request.POST.get("grupturu")
            siparisno = request.POST.get("siparisno")
            yevmiyeno = request.POST.get("yevmiyeno")

            ##
            siparisislem = genel_muhasebe.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                fis_turu =grupturu,fis_tarihi =fistarihi,fis_no = siparisno,
                yevmiye_no = yevmiyeno
            )
            if True:
                hesapkoduid  = request.POST.getlist("hesapkoduid")
                evrakTarihi  = request.POST.getlist("evrakTarihi")
                evrakno  = request.POST.getlist("evrakno")
                bt  = request.POST.getlist("bt")
                vergitc  = request.POST.getlist("vergitc")
                Aciklama  = request.POST.getlist("Aciklama")
                Borclu  = request.POST.getlist("Borclu")
                alacakli  = request.POST.getlist("alacakli")
                belgeturuaciklamsi  = request.POST.getlist("belgeturuaciklamsi")
                ##
                for i in range(len(hesapkoduid)):
                    if  hesapkoduid[i] == "":
                        pass
                    else:
                        print(i)
                        genel_muhasebe_fis.objects.create(
                            bagli_oldugufis = get_object_or_404(genel_muhasebe,id = siparisislem.id),
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesapkoduid[i]),
                            evrak_tarihi = evrakTarihi[i],bt_turu = bt[i],vergi_numarasi = vergitc[i],
                            aciklama = Aciklama[i],aciklama8belgesi = belgeturuaciklamsi[i],
                            borc = Borclu[i],alacak_bilgisi = alacakli[i],evrak_no = evrakno[i]
                            )
        link = "/"+slug+"/genelmuhasebe/"
        return redirect(link)
    return render(request,"genelmuhasebe/genelmuhasebe.html",content)

#sipariş silme
def hesap_planlari_ayarlari(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).order_by("hesap_kodu")
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    return render(request,"hesapplanlari/hesapplanlari.html",content)

def hesap_planlari_ekle(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),detay = "Evet" )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["tevkifa_hesaplari"] = tevkifat_tur_kodu.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    if request.POST:
        hesapkodu = request.POST.get("hesapkodu")
        hesapadi = request.POST.get("hesapadi")
        grupkodu = request.POST.get("grupkodu")
        hesapdetayi = request.POST.get("hesapdetayi")
        hesapadiyabancidil = request.POST.get("hesapadiyabancidil")
        kdvyuzdesi = request.POST.get("kdvyuzdesi")
        kdvhesapkodu = request.POST.get("kdvhesapkodu")
        miktarli = request.POST.get("miktarli")
        stoknumarasi = request.POST.get("stoknumarasi")
        tevkifatorani = request.POST.get("tevkifatorani")
        tevkifathesapkodu = request.POST.get("tevkifathesapkodu")
        tevkifathesapkodutur = request.POST.get("tevkifathesapkodutur")
        stopajyuzdesi = request.POST.get("stopajyuzdesi")
        stopajhesapkodu = request.POST.get("stopajhesapkodu")
        stopajturkodu = request.POST.get("stopajturkodu")
        stopajbelgeturu = request.POST.get("stopajbelgeturu")
        borclualacakli = request.POST.get("borclualacakli")
        babs = request.POST.get("babs")
        kurfarkindakullan = request.POST.get("kurfarkindakullan")
        mutabakatayi = request.POST.get("mutabakatayi")
        kamuozel = request.POST.get("kamuozel")
        yurticisatismi = request.POST.get("yurticisatismi")
        ilaveedilecekkdv = request.POST.get("ilaveedilecekkdv")
        iadekdvmi = request.POST.get("iadekdvmi")
        ozelmatrah = request.POST.get("ozelmatrah")
        kredikartli = request.POST.get("kredikartli")
        iadeyekonu = request.POST.get("iadeyekonu")
        ihrackayitlisatislar = request.POST.get("ihrackayitlisatislar")
        ihrackayitlisatislar87 = request.POST.get("ihrackayitlisatislar87")
        if kdvhesapkodu :
            a = get_object_or_404(HesapPlanlari,id = kdvhesapkodu)
        else:
            a = None
        if stopajhesapkodu :
            b = get_object_or_404(HesapPlanlari,id = stopajhesapkodu)
        else:
            b = None
        if tevkifathesapkodutur :
            c = get_object_or_404(tevkifat_tur_kodu,id = tevkifathesapkodutur)
        else:
            c = None
        if tevkifathesapkodu :
            d = get_object_or_404(HesapPlanlari,id = tevkifathesapkodu)
        else:
            d = None
        
        HesapPlanlari.objects.create(
                bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                hesap_kodu = hesapkodu,hesap_adi = hesapadi,detay = hesapdetayi,
                borclu_alacakli = borclualacakli,miktarli = miktarli,
                stok_kodu = stoknumarasi,kdv_orani = kdvyuzdesi,iliskili_kdv_hesap_kodu2 = a,
                kamumu_ozelmi = kamuozel,hesap_aciklamasi = hesapadiyabancidil,
                grup_kodu = grupkodu,ba_bslerde_kullanilsinmi = babs,kur_farkinida_kullan = kurfarkindakullan,
                stopaj_hesap_kodu2 = b ,stopaj_orani = stopajyuzdesi,
                stopaj_tur_kodu = stopajturkodu,stopaj_belge_turu=stopajbelgeturu,tevkifat_hesap_kodu2 = d,
                kdv_islem_turu = c,tevkifat_orani = tevkifatorani,
                ilave_edilecek_kdv_mi = ilaveedilecekkdv,iade_edilecek_kdv_mi = iadekdvmi,
                ozel_matrah_mi = ozelmatrah,kredi_karti_satis_mi  =kredikartli,ihrac_kayitli_satis_kdv_mi_85 =ihrackayitlisatislar,
                ihrac_kayitli_satis_kdv_mi_87 = ihrackayitlisatislar87,mutabakat_ayi = mutabakatayi,
                yurt_ici_satis_mi = yurticisatismi,yuklenilen_iadeli_konu_olan_kdv_mi = iadeyekonu
                
            )
        link = "/"+slug+"/hesapplanlari/"
        return redirect(link)
    return render(request,"hesapplanlari/hesapplanlariekle.html",content)


def hesap_planlari_silme(request,slug,id):
    HesapPlanlari.objects.filter(id = id,bagli_oldugu_firma =
                                 get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),degistiremez_bilgisi = False).update(silinme_bilgisi = True)
    link = "/"+slug+"/hesapplanlari/"
    return redirect(link)

def hesap_planlari_detay_degistirme(request,slug,id):
    HesapPlanlari.objects.filter(id = id,bagli_oldugu_firma =
                                 get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(detay = "Evet")
    link = "/"+slug+"/hesapplanlari/"
    return redirect(link)


def hesap_planlari_duzenle(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),detay = "Evet" )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["tevkifa_hesaplari"] = tevkifat_tur_kodu.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    content["hes"]=get_object_or_404(HesapPlanlari,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    if request.POST:
        hesapkodu = request.POST.get("hesapkodu")
        hesapadi = request.POST.get("hesapadi")
        grupkodu = request.POST.get("grupkodu")
        hesapdetayi = request.POST.get("hesapdetayi")
        hesapadiyabancidil = request.POST.get("hesapadiyabancidil")
        kdvyuzdesi = request.POST.get("kdvyuzdesi")
        kdvhesapkodu = request.POST.get("kdvhesapkodu")
        miktarli = request.POST.get("miktarli")
        stoknumarasi = request.POST.get("stoknumarasi")
        tevkifatorani = request.POST.get("tevkifatorani")
        tevkifathesapkodu = request.POST.get("tevkifathesapkodu")
        tevkifathesapkodutur = request.POST.get("tevkifathesapkodutur")
        stopajyuzdesi = float(request.POST.get("stopajyuzdesi"))
        stopajhesapkodu = request.POST.get("stopajhesapkodu")
        stopajturkodu = request.POST.get("stopajturkodu")
        stopajbelgeturu = request.POST.get("stopajbelgeturu")
        borclualacakli = request.POST.get("borclualacakli")
        babs = request.POST.get("babs")
        kurfarkindakullan = request.POST.get("kurfarkindakullan")
        mutabakatayi = request.POST.get("mutabakatayi")
        kamuozel = request.POST.get("kamuozel")
        yurticisatismi = request.POST.get("yurticisatismi")
        ilaveedilecekkdv = request.POST.get("ilaveedilecekkdv")
        iadekdvmi = request.POST.get("iadekdvmi")
        ozelmatrah = request.POST.get("ozelmatrah")
        kredikartli = request.POST.get("kredikartli")
        iadeyekonu = request.POST.get("iadeyekonu")
        ihrackayitlisatislar = request.POST.get("ihrackayitlisatislar")
        ihrackayitlisatislar87 = request.POST.get("ihrackayitlisatislar87")
        
            
        HesapPlanlari.objects.filter(bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),id = id).update(
                
                hesap_kodu = hesapkodu,hesap_adi = hesapadi,detay = hesapdetayi,
                borclu_alacakli = borclualacakli,miktarli = miktarli,
                stok_kodu = stoknumarasi,kdv_orani = kdvyuzdesi,iliskili_kdv_hesap_kodu2 = get_object_or_404(HesapPlanlari,id = kdvhesapkodu),
                kamumu_ozelmi = kamuozel,hesap_aciklamasi = hesapadiyabancidil,
                grup_kodu = grupkodu,ba_bslerde_kullanilsinmi = babs,kur_farkinida_kullan = kurfarkindakullan,
                stopaj_hesap_kodu2 = get_object_or_404(HesapPlanlari,id = stopajhesapkodu),stopaj_orani = stopajyuzdesi,
                stopaj_tur_kodu = stopajturkodu,stopaj_belge_turu=stopajbelgeturu,tevkifat_hesap_kodu2 = get_object_or_404(HesapPlanlari,id = tevkifathesapkodu),
                kdv_islem_turu = get_object_or_404(tevkifat_tur_kodu,id = tevkifathesapkodutur),tevkifat_orani = tevkifatorani,
                ilave_edilecek_kdv_mi = ilaveedilecekkdv,iade_edilecek_kdv_mi = iadekdvmi,
                ozel_matrah_mi = ozelmatrah,kredi_karti_satis_mi  =kredikartli,ihrac_kayitli_satis_kdv_mi_85 =ihrackayitlisatislar,
                ihrac_kayitli_satis_kdv_mi_87 = ihrackayitlisatislar87,mutabakat_ayi = mutabakatayi,
                yurt_ici_satis_mi = yurticisatismi,yuklenilen_iadeli_konu_olan_kdv_mi = iadeyekonu
                
            )
        link = "/"+slug+"/hesapplanlari/"
        return redirect(link)
    return render(request,"hesapplanlari/hesapplanlariekle.html",content)


#muavin

def muavin(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),detay = "Evet" )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["tevkifa_hesaplari"] = tevkifat_tur_kodu.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    if request.GET:
        hesa = request.GET.get("hesa")
        ay = request.GET.get("ay")
        borclualacakli = request.GET.get("borclualacakli")
        fisnumarasi = request.GET.get("fisnumarasi")
        evraknumarasi = request.GET.get("evraknumarasi")
        vergitcno = request.GET.get("vergitcno")
        aciklama = request.GET.get("aciklama")
        baslangictarihi = request.GET.get("baslangictarihi")
        bitistarihi = request.GET.get("bitistarihi")
        fis = genel_muhasebe_fis.objects.filter()
        if hesa:
            fis = fis.filter(hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesa))
        if borclualacakli:
            if borclualacakli == "Tümü":
                fis = fis.filter(hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesa))
            if borclualacakli == "Borçlu":
                fis = fis.filter(borc__gte = 0)
            if borclualacakli == "Alacaklı":
                fis = fis.filter(alacak_bilgisi__gte = 0)
        if fisnumarasi:
            fis = fis.filter(bagli_oldugufis__fis_no__icontains = fisnumarasi)
        if evraknumarasi:
            fis = fis.filter(evrak_no__icontains = evraknumarasi)
        if vergitcno:
            fis = fis.filter(vergi_numarasi__icontains = vergitcno)
        if aciklama:
            fis = fis.filter(aciklama__icontains = aciklama)
        content["filtrelenmis_fis_icerigi"] = fis
    return render(request,"hesapplanlari/muavin.html",content)

#genel muhasebe fiş düzenleme
def genel_muhasebe_sayfasi_fis_duzenleme(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    content["fis_duzelt"] = get_object_or_404(genel_muhasebe,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["fisler"] = genel_muhasebe_fis.objects.filter(bagli_oldugufis = get_object_or_404(genel_muhasebe,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)))
    if request.POST:
        if True:
            if True:
                hesapkoduid  = request.POST.getlist("hesapkoduid")
                evrakTarihi  = request.POST.getlist("evrakTarihi")
                evrakno  = request.POST.getlist("evrakno")
                bt  = request.POST.getlist("bt")
                vergitc  = request.POST.getlist("vergitc")
                Aciklama  = request.POST.getlist("Aciklama")
                Borclu  = request.POST.getlist("Borclu")
                alacakli  = request.POST.getlist("alacakli")
                belgeturuaciklamsi  = request.POST.getlist("belgeturuaciklamsi")
                degisecekhesap  =request.POST.getlist("degisecekhesap")
                fisbilgisi = request.POST.get("fisbilgisi")
                ##
                for i in range(len(degisecekhesap)):
                    if  degisecekhesap[i] == "":
                        pass
                    
                    elif degisecekhesap[i] == "yok" and  hesapkoduid[i] != "":
                        print(i)
                        genel_muhasebe_fis.objects.create(
                            bagli_oldugufis = get_object_or_404(genel_muhasebe,id = fisbilgisi),
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesapkoduid[i]),
                            evrak_tarihi = evrakTarihi[i],bt_turu = bt[i],vergi_numarasi = vergitc[i],
                            aciklama = Aciklama[i],aciklama8belgesi = belgeturuaciklamsi[i],
                            borc = Borclu[i],alacak_bilgisi = alacakli[i],evrak_no = evrakno[i]
                            )
                    elif degisecekhesap[i] != "yok":
                        print(i)
                        genel_muhasebe_fis.objects.filter(id = degisecekhesap[i] ).update(
                            hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesapkoduid[i]),
                            evrak_tarihi = evrakTarihi[i],bt_turu = bt[i],vergi_numarasi = vergitc[i],
                            aciklama = Aciklama[i],aciklama8belgesi = belgeturuaciklamsi[i],
                            borc = Borclu[i],alacak_bilgisi = alacakli[i],evrak_no = evrakno[i]
                        )
        link = "/"+slug+"/genelmuhasebe/"
        return redirect(link)
    return render(request,"genelmuhasebe/fis_duzenle.html",content)
#genel muhasebe fiş gösterme
def genel_muhasebe_sayfasi_fis_goster(request,slug,id):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    content["fis_duzelt"] = get_object_or_404(genel_muhasebe,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["fisler"] = genel_muhasebe_fis.objects.filter(bagli_oldugufis = get_object_or_404(genel_muhasebe,id = id,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)))
    return render(request,"genelmuhasebe/fis_goster.html",content)
#sipariş silme


#mizan
def mizan(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    hesaplar = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),detay = "Evet" )
    sistem = HesapPlanlari.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =None)
    kart = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    giderkartti = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    gelirkartti = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    banka_karti = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    subelerim = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    kasa_bilgisi = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerim"]  = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["carilerimsube"] = cari_kartislemleri_sube_bilgiler.objects.filter(cari_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["kart"] = kart
    content["gelirkartti"] = gelirkartti
    content["giderkartti"] = giderkartti
    content["hesapplanlari"] = hesaplar
    content["sistemhesapplanlari"] = sistem
    content["banka_karti"] = banka_karti
    content["subelerim"] = subelerim
    content["kasa_bilgisi"] = kasa_bilgisi
    content["tevkifa_hesaplari"] = tevkifat_tur_kodu.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["siparisler"] = irsaliyeislem_durumlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),silinme_bilgisi = False)
    content["filtrelenmis_fis_icerigi"] = HesapPlanlari.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    if request.GET:
        hesa = request.GET.get("hesa")
        ay = request.GET.get("ay")
        borclualacakli = request.GET.get("borclualacakli")
        fisnumarasi = request.GET.get("fisnumarasi")
        evraknumarasi = request.GET.get("evraknumarasi")
        vergitcno = request.GET.get("vergitcno")
        aciklama = request.GET.get("aciklama")
        baslangictarihi = request.GET.get("baslangictarihi")
        bitistarihi = request.GET.get("bitistarihi")
        fis = genel_muhasebe_fis.objects.filter()
        if hesa:
            fis = fis.filter(hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesa))
        if borclualacakli:
            if borclualacakli == "Tümü":
                fis = fis.filter(hesap_plani_secim = get_object_or_404(HesapPlanlari,id = hesa))
            if borclualacakli == "Borçlu":
                fis = fis.filter(borc__gte = 0)
            if borclualacakli == "Alacaklı":
                fis = fis.filter(alacak_bilgisi__gte = 0)
        if fisnumarasi:
            fis = fis.filter(bagli_oldugufis__fis_no__icontains = fisnumarasi)
        if evraknumarasi:
            fis = fis.filter(evrak_no__icontains = evraknumarasi)
        if vergitcno:
            fis = fis.filter(vergi_numarasi__icontains = vergitcno)
        if aciklama:
            fis = fis.filter(aciklama__icontains = aciklama)
        content["filtrelenmis_fis_icerigi"] = fis
    return render(request,"hesapplanlari/mizan.html",content) 
#mizan

def musavir_cari(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["cari_bilgileri"] = musteri_cari.objects.filter(sininme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    if request.POST:
        cari = request.POST.get("cari")
        tarih = request.POST.getlist("tarih")
        aciklama = request.POST.getlist("aciklama")
        borc = request.POST.getlist("borc")
        alacak = request.POST.getlist("alacak")
        for i in range(0,len(tarih)) :
            if tarih[i]:
                musteri_cari_fis.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_cari = get_object_or_404(musteri_cari,id =cari ),
                    evrak_tarihi = tarih[i],aciklama=aciklama[i],
                    alacak = float(alacak[i]),borc = float(borc[i])
                )
    return render(request,"musavir_cari/musavir_cari.html",content)

def musteri_cari_kart_olustur(request,slug):
    if request.POST:
        slug = request.POST.get("slug")
        isim = request.POST.get("isim")
        musteri_cari.objects.create(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                                    cari_adi = isim)
    z = "/"+slug+"/mustericari/"
    return redirect(z)
def musteri_cari_kart_sil(request,slug,id):
    
    musteri_cari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
                            ).update(sininme_bilgisi = True)
    z = "/"+slug+"/mustericari/"
    return redirect(z)

def musteri_cari_kart_duzelt(request,slug):
    if request.POST:
        id = request.POST.get("slug")
        isim = request.POST.get("isim")
        musteri_cari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
                                    cari_adi = isim)
    z = "/"+slug+"/mustericari/"
    return redirect(z)


def musavir_stok_sayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["cari_bilgileri"] = musavir_stok.objects.filter(sininme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
    if request.POST:
        cari = request.POST.get("cari")
        tarih = request.POST.getlist("tarih")
        aciklama = request.POST.getlist("aciklama")
        borc = request.POST.getlist("borc")
        alacak = request.POST.getlist("alacak")
        for i in range(0,len(tarih)) :
            if tarih[i]:
                musteri_cari_fis.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_cari = get_object_or_404(musteri_cari,id =cari ),
                    evrak_tarihi = tarih[i],aciklama=aciklama[i],
                    alacak = float(alacak[i]),borc = float(borc[i])
                )
    return render(request,"musavir_stok/musavir_stok.html",content)

def musavir_stok_kart_olustur(request,slug):
    if request.POST:
        slug = request.POST.get("slug")
        stokadi = request.POST.get("stokadi")
        stokkodu = request.POST.get("stokkodu")
        birim= request.POST.get("birim")
        ticari = request.POST.get("ticari")
        envanyo = request.POST.get("envanyo")
        ortk = request.POST.get("ortk")
        musavir_stok.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            stok_kodu =  stokkodu,stok_adi = stokadi,
            birim = birim,envanter_yonetimi = envanyo,ort_kar = float(ortk),ticari = ticari)
    z = "/"+slug+"/musavirstok/"
    return redirect(z)

def musavir_stok_kart_sil(request,slug,id):
    
    musavir_stok.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
                            ).update(sininme_bilgisi = True)
    z = "/"+slug+"/musavirstok/"
    return redirect(z)

def musavir_stok_kart_duzenle(request,slug):
    if request.POST:
        slug = request.POST.get("slug")
        stokadi = request.POST.get("stokadi")
        stokkodu = request.POST.get("stokkodu")
        birim= request.POST.get("birim")
        ticari = request.POST.get("ticari")
        envanyo = request.POST.get("envanyo")
        ortk = request.POST.get("ortk")
        musavir_stok.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            stok_kodu =  stokkodu,stok_adi = stokadi,
            birim = birim,envanter_yonetimi = envanyo,ort_kar = float(ortk),ticari = ticari)
    z = "/"+slug+"/musavirstok/"
    return redirect(z)

def musavir_stok_fisi_olusturma(request,slug):
    if request.POST:
        stok = request.POST.get("cari")
        evrakk_tarih =request.POST.getlist("tarih")
        didb =request.POST.getlist("didb")
        iademi =request.POST.getlist("iademi")
        evrakno =request.POST.getlist("evrakno")
        evrakaciklama =request.POST.getlist("evrakaciklama")
        girismiktari =request.POST.getlist("girismiktari")
        girisbirimfiyati =request.POST.getlist("girisbirimfiyati")
        giristutari =request.POST.getlist("giristutari")
        cikismiktari =request.POST.getlist("cikismiktari")
        cikisbirimfiyati =request.POST.getlist("cikisbirimfiyati")
        cikistutari =request.POST.getlist("cikistutari")
        for i in range(len(evrakk_tarih)):
            if evrakk_tarih[i] != "":
                musavir_stok_fisi.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_stok = get_object_or_404(musavir_stok,id = stok),
                    evrak_tarihi = evrakk_tarih[i],donem = didb[i],
                    iademi = iademi[i],evrak_no = evrakno[i],
                    evrak_aciklama = evrakaciklama[i],giris_miktari = girismiktari[i],
                    cikis_miktari = cikismiktari[i],
                    giris_fiyati = giristutari[i],
                    cikis_fiyati = cikistutari[i]
                )
    z = "/"+slug+"/musavirstok/"
    return redirect(z)

#Demirbaşlar
def demirbaslar(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render (request,"demirbas/demirbaslar.html",content)

def demirbas_ekle(request,slug):
    content = site_ayarlari()
    content["sabit_kiymetler"] = amortisman_bilgileri.objects.filter(N1 = None,N2 = None)
    if request.POST:
        demirbaskodu = request.POST.get("demirbaskodu")
        aciklama = request.POST.get("aciklama")
        alistarihi = request.POST.get("alistarihi")
        faturano = request.POST.get("faturano")
        tutar = request.POST.get("tutar")
        yeni_demirbas_degeri = request.POST.get("yeni_demirbas_degeri")
        kdvorani = request.POST.get("kdvorani")
        aliskdvtutari= request.POST.get("aliskdvtutari")
        alinan_firma= request.POST.get("alinan_firma")
        amortisman_orani = request.POST.get("amortisman_orani")
        faydaliomur = request.POST.get("faydaliomur")
        sabit_kiymet_kodu = request.POST.get("sabit_kiymet_kodu")
        sabit_kiymet_adi = request.POST.get("sabit_kiymet_adi")
        kistamortisman = request.POST.get("kistamortisman")
        amortismantipi = request.POST.get("amortismantipi")
        sube = request.POST.get("sube")
        masrafmerkezi =request.POST.get("masrafmerkezi")
        demirbasozelkodu = request.POST.get("demirbasozelkodu")
        demirbashesapkoduid = request.POST.get("demirbashesapkoduid")
        birikmisanmortismandegerid = request.POST.get("birikmisanmortismandegerid")
        donemeaitamortismanhesapid = request.POST.get("donemeaitamortismanhesapid")
        satistarihi = request.POST.get("satistarihi")
        satisfaturano = request.POST.get("satisfaturano")
        satistutar = request.POST.get("satistutar")
        satiskdvorani = request.POST.get("satiskdvorani")
        satiskdvtutari = request.POST.get("satiskdvtutari")
        satilan_firma = request.POST.get("satilan_firma")
        demirbasenfilasyonduzeltmesihesapkodu = request.POST.get("demirbasenfilasyonduzeltmesihesapkodu")
        enfilasyonduzeltmesihesapkodu = request.POST.get("enfilasyonduzeltmesihesapkodu")
        birikmisamortismanenfilasyonduzeltmesihesapkodu = request.POST.get("birikmisamortismanenfilasyonduzeltmesihesapkodu")
        aktifdegerartisikodu = request.POST.get("aktifdegerartisikodu")
        degerartisfonukodu = request.POST.get("degerartisfonukodu")
        kreditutari = request.POST.get("kreditutari")
        kredifaiztutari = request.POST.get("kredifaiztutari")
        tesvikedildimi = request.POST.get("tesvikedildimi")
        Borcunkullanildigiyil = request.POST.get("Borcunkullanildigiyil")
        Borcunkullanildigiay = request.POST.get("Borcunkullanildigiay")
        Borcunkapatidigiyil= request.POST.get("Borcunkapatidigiyil")
        Borcunkapatildigiiay =request.POST.get("Borcunkapatildigiiay")
        sonyenidendegerlenmisdeger= request.POST.get("sonyenidendegerlenmisdeger")
        sonbirikmisamortismandeger= request.POST.get("sonbirikmisamortismandeger")
        duzeltmeyili = request.POST.get("duzeltmeyili")
        duzeltmeayi = request.POST.get("duzeltmeayi")
    return render (request,"demirbas/demirbasl_ekleme.html",content)

#DemirBaşlar
def ayarlar_firma_ayarlari(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    if request.POST:
        damgavergisi5033 = request.POST.get("damgavergisi5033")
        mudamga = request.POST.get("mudamga")
        kdamga = request.POST.get("kdamga")
        kdvdamga = request.POST.get("kdvdamga")
        gecicivergi = request.POST.get("gecicivergi")
        gecicivergikurumlar = request.POST.get("gecicivergikurumlar")
        gecicivergikisi = request.POST.get("gecicivergikisi")
        if firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).count()>0:
            firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
               bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ,
               damga_vergisi_5033sk = damgavergisi5033,muhasabe_odemesi_gelir_vergisi_kesinti_orani =mudamga,
               kira_odemesi_gelir_vergisi_kesinti_orani = kdamga,
               kdv_beyannamesi_damga_vergisi = kdvdamga,gecici_vergi_beyannamesi_damga_vergisi =gecicivergi,
               gecici_vergi_orani_kurumlar =  float(gecicivergikurumlar),
               gecici_vergi_orani_gercek_kisiler = float(gecicivergikisi)
            )
        else:
            firma_ayarlari_ayar_kisimi.objects.create(
               bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ,
               damga_vergisi_5033sk = damgavergisi5033,muhasabe_odemesi_gelir_vergisi_kesinti_orani =mudamga,
               kira_odemesi_gelir_vergisi_kesinti_orani = kdamga,
               kdv_beyannamesi_damga_vergisi = kdvdamga,gecici_vergi_beyannamesi_damga_vergisi =gecicivergi,
               gecici_vergi_orani_kurumlar =  float(gecicivergikurumlar),
               gecici_vergi_orani_gercek_kisiler = float(gecicivergikisi)
            )
        z = "/"+slug+"/ayarlar/"
        return redirect(z)
    return render(request,"ayarlar/firma_ayarlari.html",content)

def ayarlar_smm_ayarlari(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["firma_ayarlari"] = firma_ayarlari_smm_ymm_sm_bilgileri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    if request.POST:
        isim = request.POST.get("isim")
        soyadi = request.POST.get("soyadi")
        tip = request.POST.get("tip")
        kayitlioda = request.POST.get("kayitlioda")
        odasicilno = request.POST.get("odasicilno")
        muhur_numarasi = request.POST.get("muhur_numarasi")
        baslama_tarihi = request.POST.get("baslama_tarihi")
        ortakli_unvan = request.POST.get("ortakli_unvan")
        sirket_unvan = request.POST.get("sirket_unvan")
        vergi_dairesi = request.POST.get("vergi_dairesi")
        vergi_no = request.POST.get("vergi_no")
        ticari_sicil_no = request.POST.get("ticari_sicil_no")
        vergi_kimlik_no = request.POST.get("vergi_kimlik_no")
        tc_kimlik_no = request.POST.get("tc_kimlik_no")
        goreve_baslama_tarihi = request.POST.get("goreve_baslama_tarihi")
        isyeri_adresi = request.POST.get("isyeri_adresi")
        fax = request.POST.get("fax")
        eposta = request.POST.get("eposta")
        arac_plaka_no = request.POST.get("arac_plaka_no")
        cinsiyet = request.POST.get("cinsiyet")
        uyrugu = request.POST.get("uyrugu")
        baba_adi = request.POST.get("baba_adi")
        anne_adi = request.POST.get("anne_adi")
        dogum_yeri = request.POST.get("dogum_yeri")
        dogum_tarihi = request.POST.get("dogum_tarihi")
        nufusa_kayitli_oldugu_yer = request.POST.get("nufusa_kayitli_oldugu_yer")
        ikametgah_adresi = request.POST.get("ikametgah_adresi")
        ikametgah_bulvar = request.POST.get("ikametgah_bulvar")
        ikametgah_cadde = request.POST.get("ikametgah_cadde")
        ikametgah_sokak = request.POST.get("ikametgah_sokak")
        ikametgah_ic_kapi = request.POST.get("ikametgah_ic_kapi")
        ikametgah_dis_kapi = request.POST.get("ikametgah_dis_kapi")
        ikametgah_mahalle_koy = request.POST.get("ikametgah_mahalle_koy")
        ikametgah_ilce = request.POST.get("ikametgah_ilce")
        ikametgah_il = request.POST.get("ikametgah_il")
        ikametgah_posta_kodu = request.POST.get("ikametgah_posta_kodu")
        cep_telefonu = request.POST.get("cep_telefonu")
        if firma_ayarlari_smm_ymm_sm_bilgileri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).count()>0:
            firma_ayarlari_smm_ymm_sm_bilgileri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
               bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ,
               ad = isim,soyad = soyadi,musavir_turu = tip,
               kayitliolduguoda = kayitlioda,odasicilno = odasicilno,
               muhur_numarasi = muhur_numarasi,baslama_tarihi= baslama_tarihi,
               ortakli_unvan= ortakli_unvan,sirket_unvan = sirket_unvan,
               vergi_dairesi = vergi_dairesi,vergi_no = vergi_no,ticari_sicil_no = ticari_sicil_no,
               vergi_kimlik_no = vergi_kimlik_no,tc_kimlik_no = tc_kimlik_no,
               goreve_baslama_tarihi = goreve_baslama_tarihi,
               isyeri_adresi = isyeri_adresi,fax=fax,eposta= eposta,
               arac_plaka_no = arac_plaka_no,cinsiyet = cinsiyet,uyrugu = uyrugu,
               baba_adi = baba_adi,anne_adi = anne_adi,dogum_yeri = dogum_yeri,
               dogum_tarihi = dogum_tarihi,nufusa_kayitli_oldugu_yer=nufusa_kayitli_oldugu_yer,
               ikametgah_adresi = ikametgah_adresi,ikametgah_bulvar= ikametgah_bulvar,
                ikametgah_cadde = ikametgah_cadde,ikametgah_sokak = ikametgah_sokak,
                ikametgah_ic_kapi = ikametgah_ic_kapi,ikametgah_dis_kapi = ikametgah_dis_kapi,
                ikametgah_mahalle_koy = ikametgah_mahalle_koy,ikametgah_ilce = ikametgah_ilce,
                ikametgah_il = ikametgah_il,ikametgah_posta_kodu =ikametgah_posta_kodu,
                cep_telefonu =cep_telefonu
            )
        else:
            firma_ayarlari_smm_ymm_sm_bilgileri.objects.create(
               bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ,
               ad = isim,soyad = soyadi,musavir_turu = tip,
               kayitliolduguoda = kayitlioda,odasicilno = odasicilno,
               muhur_numarasi = muhur_numarasi,baslama_tarihi= baslama_tarihi,
               ortakli_unvan= ortakli_unvan,sirket_unvan = sirket_unvan,
               vergi_dairesi = vergi_dairesi,vergi_no = vergi_no,ticari_sicil_no = ticari_sicil_no,
               vergi_kimlik_no = vergi_kimlik_no,tc_kimlik_no = tc_kimlik_no,
               goreve_baslama_tarihi = goreve_baslama_tarihi,
               isyeri_adresi = isyeri_adresi,fax=fax,eposta= eposta,
               arac_plaka_no = arac_plaka_no,cinsiyet = cinsiyet,uyrugu = uyrugu,
               baba_adi = baba_adi,anne_adi = anne_adi,dogum_yeri = dogum_yeri,
               dogum_tarihi = dogum_tarihi,nufusa_kayitli_oldugu_yer=nufusa_kayitli_oldugu_yer,
               ikametgah_adresi = ikametgah_adresi,ikametgah_bulvar= ikametgah_bulvar,
                ikametgah_cadde = ikametgah_cadde,ikametgah_sokak = ikametgah_sokak,
                ikametgah_ic_kapi = ikametgah_ic_kapi,ikametgah_dis_kapi = ikametgah_dis_kapi,
                ikametgah_mahalle_koy = ikametgah_mahalle_koy,ikametgah_ilce = ikametgah_ilce,
                ikametgah_il = ikametgah_il,ikametgah_posta_kodu =ikametgah_posta_kodu,
                cep_telefonu =cep_telefonu
            )
        z = "/"+slug+"/smmayarlar/"
        return redirect(z)
    return render(request,"ayarlar/firma_smm_ayarlama.html",content)

#kdv1
def kdv1_beyannamesi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    kdv_istisna250 = []
    for i in range(201,251):
        kdv_istisna250.append(str(i))
    content["kdv_istisnalari"] = kdv_istisna_kodu.objects.filter(kod__in = kdv_istisna250)
    kdv_istisna350 = []
    for i in range(301,351):
        kdv_istisna350.append(str(i))
    content["kdv_istisnalari1"] = kdv_istisna_kodu.objects.filter(kod__in = kdv_istisna350)
    tevk_900ler = []
    for i in range(901,926):
        tevk_900ler.append(str(i))
    content["tevkifatlar2"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_900ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    kdv_istisna400 = []
    for i in range(406,451):
        kdv_istisna400.append(str(i))
    content["kdv_istisnalari2"] = kdv_istisna_kodu.objects.filter(kod__in = kdv_istisna400)
    content["ihrac_kayitlari"] =["701 -İHRACATI YAPILACAK NİHAİ ÜRÜNLERİN KANUNUN 11/1-c MADDESİ KAPSAMINDA TESLİMİ",
                                 "702  -DAHİLDE İŞLEME VEYA GEÇİCİ KABUL REJİMLERİ KAPSAMINDA İHRACATIYAPILACAK ÜRÜNÜN İMALİNDE KULLANILACAK MALLARIN DİİB VEYA GKİB SAHİPLERİNE KANUNUN GEÇİCİ 17 NCİ MADDESİ KAPSAMINDA TESLİMİ",
                                 "703  -İHRAÇ KAYITLI ÖTV'Lİ SATIŞ"]
    content["teknolojibolgeleri"] = ""
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["tasinmazililce"] = ""
    content["onceki_beyannameler"]  = kdv1_beyannamesi_bilgileri.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    if request.POST:
        if True:
            an = datetime.now()
            a = an.year
            aylar = {"OCAK": 1, "ŞUBAT": 2, "MART": 3, "NİSAN": 4, "MAYIS": 5, "HAZİRAN": 6, "TEMUZ": 7, "AĞUSTOS": 8, "EYLÜL": 9, "EKİM": 10, "KASIM": 11, "ARALIK": 12}
            aysecimi = request.POST.get("aysecimi")
            ay_numarasi = aylar.get(aysecimi)
            tarih = datetime(a, ay_numarasi, 1)
            beyanname_bilgisi = kdv1_beyannamesi_bilgileri.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
                ,ay = tarih
            )
            #TEVKİFAT UYGULANMAYAN İŞLEMLER
            matrah6 = request.POST.get("matrah6")
            kdv6 = request.POST.get("kdv6")
            vergi7 = request.POST.get("vergi7")
            matrah8 = request.POST.get("matrah8")
            kdv8 = request.POST.get("kdv8")
            vergi9 = request.POST.get("vergi9")
            matrah10 = request.POST.get("matrah10")
            kdv10 = request.POST.get("kdv10")
            vergi11 = request.POST.get("vergi11")
            matrah_bildirimi_tevkifatuygulanmayanislemler.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                matrah = matrah6,kdv = kdv6,vergi = vergi7,matrah1 = matrah8,
                kdv1 = kdv8,vergi1 = vergi9,matrah2 = matrah10,
                kdv2 = kdv10,vergi2 = vergi11
            )
            #TEVKİFAT UYGULANMAYAN İŞLEMLER
            if True:
                #KISMİ TEVKİFAT UYGULANAN İŞLEMLER
                secimtevkifat14 = request.POST.get("secimtevkifat14")
                matrah14 = request.POST.get("matrah14")
                kdv14 = request.POST.get("kdv14")
                tevkifat14 = request.POST.get("tevkifat14")
                vergi15 = request.POST.get("vergi15")
                secimtevkifat16 = request.POST.get("secimtevkifat16")
                matrah16 = request.POST.get("matrah16")
                kdv16 = request.POST.get("kdv16")
                tevkifat16 = request.POST.get("tevkifat16")
                vergi17 = request.POST.get("vergi17")
                secimtevkifat18 = request.POST.get("secimtevkifat18")
                matrah18 = request.POST.get("matrah18")
                kdv18 = request.POST.get("kdv18")
                tevkifat18 = request.POST.get("tevkifat18")
                vergi19 = request.POST.get("vergi19")
                secimtevkifat20 = request.POST.get("secimtevkifat20")
                matrah20 = request.POST.get("matrah20")
                kdv20 = request.POST.get("kdv20")
                tevkifat20 = request.POST.get("tevkifat20")
                vergi21 = request.POST.get("vergi21")
                matrah_bildirimi_kismi_tevkifatuygulanmayanislemler.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    islem_turu = get_object_or_none(tevkifat_tur_kodu, id=secimtevkifat14),
                    matrah = matrah14,kdv = kdv14,vergi = vergi15,tevkifatorani = tevkifat14,
                    islem_turu1 = get_object_or_none(tevkifat_tur_kodu, id=secimtevkifat16),
                    matrah1 = matrah16,kdv1 = kdv16,vergi1 = vergi17,tevkifatorani1 = tevkifat16,
                    islem_turu2 = get_object_or_none(tevkifat_tur_kodu, id=secimtevkifat18),
                    matrah2 = matrah18,kdv2 = kdv18,vergi2 = vergi19,tevkifatorani2 = tevkifat18,
                    islem_turu3 = get_object_or_none(tevkifat_tur_kodu, id=secimtevkifat20),
                    matrah3 = matrah20,kdv3 = kdv20,vergi3 = vergi21,tevkifatorani3 = tevkifat20
                )
                #KISMİ TEVKİFAT UYGULANAN İŞLEMLER
            if True:
                # DİĞER İŞLEMLER
                bigi1 = request.POST.get("bigi1")
                matrah22 = request.POST.get("matrah22")
                vergi23 = request.POST.get("vergi23")
                bigi2 = request.POST.get("bigi2")
                matrah24 = request.POST.get("matrah24")
                vergi25 = request.POST.get("vergi25")
                bigi3 = request.POST.get("bigi3")
                matrahbenzer1 = request.POST.get("matrahbenzer1")
                vergibenzer1 = request.POST.get("vergibenzer1")
                bigi4 = request.POST.get("bigi4")
                matrahbenzer2 = request.POST.get("matrahbenzer2")
                vergibenzer2 = request.POST.get("vergibenzer2")
                bigi5 = request.POST.get("bigi5")
                matrah94 = request.POST.get("matrah94")
                vergi95 = request.POST.get("vergi95")
                bigi6 = request.POST.get("bigi6")
                matrahnumarasiz = request.POST.get("matrahnumarasiz")
                verginumarasiz = request.POST.get("verginumarasiz")
                bigi7 = request.POST.get("bigi7")
                matrah26 = request.POST.get("matrah26")
                vergi27 = request.POST.get("vergi27")
                matrah_bildirimi_digerislemleri.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    bilgi = bigi1,matrah1 = matrah22,vergi1 = vergi23,bilgi2 = bigi2,matrah2 =matrah24,vergi2 = vergi25,
                    bilgi3 = bigi3,matrah3 = matrahbenzer1,vergi3 = vergibenzer1,bilgi4 = bigi4,matrah4 = matrahbenzer2,
                    vergi4 = vergibenzer2,bilgi5 = bigi5,matrah5 = matrah94,vergi5 = vergi95,
                    bilgi6 = bigi6,matrah6 = matrahnumarasiz,vergi6 = verginumarasiz,
                    bilgi7 = bigi7,matrah7 = matrah26,vergi7 = vergi27
                )
            # DİĞER İŞLEMLER
            if True:
                #İSTEĞE BAĞLI TAM TEVKİFAT UYGULANAN İŞLEMLER
                istege_baglitevkat = request.POST.getlist("istege_baglitevkat")
                istegebaglimatrah = request.POST.getlist("istegebaglimatrah")
                istebaglikdv = request.POST.getlist("istebaglikdv")
                istebaglivergi = request.POST.getlist("istebaglivergi")
                #toplam 
                for i in range(0,len(istege_baglitevkat)):
                    if get_object_or_none(tevkifat_tur_kodu,id = istege_baglitevkat[i] ):
                        matrah_bildirimi_istegebaglitamtevkifat.objects.create(
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                            bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                            islem_turu = get_object_or_none(tevkifat_tur_kodu,id = istege_baglitevkat[i] ),
                            matrah = istegebaglimatrah[i],kdv = istebaglikdv[i],vergi = istebaglivergi[i]
                        )
                indirimkdvsi = request.POST.get("indirimkdvsi")
                #İSTEĞE BAĞLI TAM TEVKİFAT UYGULANAN İŞLEMLER
            if True:
                # İNDİRİMLER
                indirimler1 = request.POST.get("indirimler1")
                indirimlerdeger1 = request.POST.get("indirimlerdeger1")
                indirimler2 = request.POST.get("indirimler2")
                indirimlerdeger2 = request.POST.get("indirimlerdeger2")
                indirimler3 = request.POST.get("indirimler3")
                indirimlerdeger3 = request.POST.get("indirimlerdeger3")
                indirimler4 = request.POST.get("indirimler4")
                indirimlerdeger4 = request.POST.get("indirimlerdeger4")
                indirimler5 = request.POST.get("indirimler5")
                indirimlerdeger5 = request.POST.get("indirimlerdeger5")
                indirimler6 = request.POST.get("indirimler6")
                indirimlerdeger6 = request.POST.get("indirimlerdeger6")
                indirimler7 = request.POST.get("indirimler7")
                indirimlerdeger7 = request.POST.get("indirimlerdeger7")
                indirimler8 = request.POST.get("indirimler8")
                indirimlerdeger8 = request.POST.get("indirimlerdeger8")
                indirimler9 = request.POST.get("indirimler9")
                indirimlerdeger9 = request.POST.get("indirimlerdeger9")
                indirimler10 = request.POST.get("indirimler10")
                indirimlerdeger10 = request.POST.get("indirimlerdeger10")
                indirimler11 = request.POST.get("indirimler11")
                indirimlerdeger11 = request.POST.get("indirimlerdeger11")
                # İNDİRİMLER
                indirimler.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    tutar  =indirimlerdeger1,bilgi = indirimler1,bilgi1 = indirimler3,tutar1  =indirimlerdeger3,
                    bilgi2 = indirimler4,tutar2  =indirimlerdeger4,bilgi3 = indirimler5,tutar3  =indirimlerdeger5,
                    bilgi4 = indirimler6,tutar4  =indirimlerdeger6,bilgi5 = indirimler7,tutar5  =indirimlerdeger7,
                    bilgi7 = indirimler9,tutar7  =indirimlerdeger9,bilgi8 = indirimler10,tutar8  =indirimlerdeger10
                )
            if True:
                #BU DÖNEME AİT İNDİRİLECEK KDV TUTARININ ORANLARA GÖRE DAĞILIMI
                indiirmdagiliskdv1 = request.POST.get("indiirmdagiliskdv1")
                indiirmdagiliskdvtutari1 = request.POST.get("indiirmdagiliskdvtutari1")
                indiirmdagiliskdv2 = request.POST.get("indiirmdagiliskdv2")
                indiirmdagiliskdvtutari2 = request.POST.get("indiirmdagiliskdvtutari2")
                indiirmdagiliskdv3 = request.POST.get("indiirmdagiliskdv3")
                indiirmdagiliskdvtutari3 = request.POST.get("indiirmdagiliskdvtutari3")
                #BU DÖNEME AİT İNDİRİLECEK KDV TUTARININ ORANLARA GÖRE DAĞILIMI
                indirim_bildirimi.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    kdvorani1 = indiirmdagiliskdv1,kdvtutari1 = indiirmdagiliskdvtutari1,kdvorani2 = indiirmdagiliskdv2,
                    kdvtutari2 = indiirmdagiliskdvtutari2,kdvorani3 = indiirmdagiliskdv3,kdvtutari3 =indiirmdagiliskdvtutari3 
                )
            if True:
                #ÖNCEKİ DÖNEME AİT MİKTARDA DEĞİŞİKLİK VARSA BU TABLO DOLDURULACAKTIR
                indirimoncekidonem1 = request.POST.get("indirimoncekidonem1")
                aciklama1 = request.POST.get("aciklama1")
                miktar1 = request.POST.get("miktar1")
                indirimoncekidonem2 = request.POST.get("indirimoncekidonem2")
                aciklama2 = request.POST.get("aciklama2")
                miktar2 = request.POST.get("miktar2")
                indirimoncekidonem3 = request.POST.get("indirimoncekidonem3")
                aciklama3 = request.POST.get("aciklama3")
                miktar3 = request.POST.get("miktar3")
                indirimoncekidonem4 = request.POST.get("indirimoncekidonem4")
                aciklama4 = request.POST.get("aciklama4")
                miktar4 = request.POST.get("miktar4")
                indirimoncekidonem5 = request.POST.get("indirimoncekidonem5")
                aciklama5 = request.POST.get("aciklama5")
                miktar5 = request.POST.get("miktar5")
                indirimoncekidonem6 = request.POST.get("indirimoncekidonem6")
                aciklama6 = request.POST.get("aciklama6")
                miktar6 = request.POST.get("miktar6")
                indirimoncekidonem7 = request.POST.get("indirimoncekidonem7")
                aciklama7 = request.POST.get("aciklama7")
                miktar7 = request.POST.get("miktar7")
                indirimoncekidonem8 = request.POST.get("indirimoncekidonem8")
                aciklama8 = request.POST.get("aciklama8")
                miktar8 = request.POST.get("miktar8")
                #ÖNCEKİ DÖNEME AİT MİKTARDA DEĞİŞİKLİK VARSA BU TABLO DOLDURULACAKTIR
                indirim_oncekidonem.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    indirimoncekidonem1 = indirimoncekidonem1,aciklama1 = aciklama1,miktar1 = miktar1,
                    indirimoncekidonem2 = indirimoncekidonem2, aciklama2 = aciklama2,miktar2 = miktar2,indirimoncekidonem3 = indirimoncekidonem3,
                    aciklama3 = aciklama3,miktar3 = miktar3,indirimoncekidonem4 = indirimoncekidonem4,
                    aciklama4 =aciklama4,miktar4 = miktar4,indirimoncekidonem5 = indirimoncekidonem5,
                    aciklama5 = aciklama5,miktar5 = miktar5,
                    indirimoncekidonem6 = indirimoncekidonem6,aciklama6 = aciklama6,miktar6 = miktar6,
                    indirimoncekidonem7 = indirimoncekidonem7,aciklama7 = aciklama7,miktar7 = miktar7,
                    indirimoncekidonem8 =indirimoncekidonem8,aciklama8 = aciklama8,miktar8 = miktar8
                )
            if True:
                #SONUÇ HESAPLARI
                sonucyazisi1 = request.POST.get("sonucyazisi1")
                sonuc1 = request.POST.get("sonuc1")
                sonuc2 = request.POST.get("sonuc2")
                sonucyazisi2 = request.POST.get("sonucyazisi2")
                sonuc3 = request.POST.get("sonuc3")
                sonucyazisi3 = request.POST.get("sonucyazisi3")
                sonuc4 = request.POST.get("sonuc4")
                sonucyazisi4 = request.POST.get("sonucyazisi4")
                #SONUÇ HESAPLARI
                sonuc_hesaplari.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    sonucyazisi1 = sonucyazisi1,sonuc1 = sonuc1,sonuc2 = sonuc2,sonucyazisi2 =sonucyazisi2,
                    sonuc3 = sonuc3,sonucyazisi3 = sonucyazisi3,sonuc4 = sonuc4,sonucyazisi4 = sonucyazisi4
                )
            if True:
                #DİĞER BİLGİLER
                sonucyazisidiger1 = request.POST.get("sonucyazisidiger1")
                sonucdiger1 = request.POST.get("sonucdiger1")
                sonucdiger2 = request.POST.get("sonucdiger2")
                sonucyazisidiger2 = request.POST.get("sonucyazisidiger2")
                sonucdiger3 = request.POST.get("sonucdiger3")
                sonucyazisidiger3 = request.POST.get("sonucyazisidiger3")
                sonucdiger4 = request.POST.get("sonucdiger4")
                sonucyazisidiger4 = request.POST.get("sonucyazisidiger4")
                #DİĞER BİLGİLER
                sonuc_hesaplari_digerbilgiler.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    sonucyazisidiger1 = sonucyazisidiger1,sonucdiger1 = sonucdiger1,sonucdiger2 = sonucdiger2,
                    sonucyazisidiger2 = sonucyazisidiger2,sonucdiger3 = sonucdiger3,sonucyazisidiger3 = sonucyazisidiger3,
                    sonucdiger4 = sonucdiger4,sonucyazisidiger4 = sonucyazisidiger4
                )
            if True:
                # KISMİ İSTİSNA KAPSAMINA GİREN İŞLEMLER
                istisnakismikdvistisnasecimi1 = request.POST.get("istisnakismikdvistisnasecimi1")
                istisnakismikdvistisnasecimihizmetveteslimtutari1 = request.POST.get("istisnakismikdvistisnasecimihizmetveteslimtutari1")
                istisnakismikdvistisnasecimiyuklenilenkdv1 = request.POST.get("istisnakismikdvistisnasecimiyuklenilenkdv1")
                istisnakismikdvistisnasecimi2 = request.POST.get("istisnakismikdvistisnasecimi2")
                istisnakismikdvistisnasecimihizmetveteslimtutari2 = request.POST.get("istisnakismikdvistisnasecimihizmetveteslimtutari2")
                istisnakismikdvistisnasecimiyuklenilenkdv2 = request.POST.get("istisnakismikdvistisnasecimiyuklenilenkdv2")
                istisnakismikdvistisnasecimi3 = request.POST.get("istisnakismikdvistisnasecimi3")
                istisnakismikdvistisnasecimihizmetveteslimtutari3 = request.POST.get("istisnakismikdvistisnasecimihizmetveteslimtutari3")
                istisnakismikdvistisnasecimiyuklenilenkdv3 = request.POST.get("istisnakismikdvistisnasecimiyuklenilenkdv3")
                istisnakismikdvistisnasecimi4 = request.POST.get("istisnakismikdvistisnasecimi4")
                istisnakismikdvistisnasecimihizmetveteslimtutari4 = request.POST.get("istisnakismikdvistisnasecimihizmetveteslimtutari4")
                istisnakismikdvistisnasecimiyuklenilenkdv4 = request.POST.get("istisnakismikdvistisnasecimiyuklenilenkdv4")
                istisnakismikdvistisnasecimi5 = request.POST.get("istisnakismikdvistisnasecimi5")
                istisnakismikdvistisnasecimihizmetveteslimtutari5 = request.POST.get("istisnakismikdvistisnasecimihizmetveteslimtutari5")
                istisnakismikdvistisnasecimiyuklenilenkdv5 = request.POST.get("istisnakismikdvistisnasecimiyuklenilenkdv5")
                # KISMİ İSTİSNA KAPSAMINA GİREN İŞLEMLER
                kismi_istisna_durumu.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    istisna1 = get_object_or_none(kdv_istisna_kodu,istisnakismikdvistisnasecimi1),istisnakismikdvistisnasecimihizmetveteslimtutari1 =istisnakismikdvistisnasecimihizmetveteslimtutari1,
                    istisnakismikdvistisnasecimiyuklenilenkdv1 =istisnakismikdvistisnasecimiyuklenilenkdv1 ,istisna2 = get_object_or_none(kdv_istisna_kodu,istisnakismikdvistisnasecimi2),
                    istisnakismikdvistisnasecimihizmetveteslimtutari2 = istisnakismikdvistisnasecimihizmetveteslimtutari2,
                    istisnakismikdvistisnasecimiyuklenilenkdv2 = istisnakismikdvistisnasecimiyuklenilenkdv2,
                    istisna3 = get_object_or_none(kdv_istisna_kodu,istisnakismikdvistisnasecimi3),
                    istisnakismikdvistisnasecimihizmetveteslimtutari3 = istisnakismikdvistisnasecimihizmetveteslimtutari3,
                    istisnakismikdvistisnasecimiyuklenilenkdv3 = istisnakismikdvistisnasecimiyuklenilenkdv3,
                    istisna4= get_object_or_none(kdv_istisna_kodu,istisnakismikdvistisnasecimi4),
                    istisnakismikdvistisnasecimihizmetveteslimtutari4 = istisnakismikdvistisnasecimihizmetveteslimtutari4,
                    istisnakismikdvistisnasecimiyuklenilenkdv4 = istisnakismikdvistisnasecimiyuklenilenkdv4,
                    istisna5 = get_object_or_none(kdv_istisna_kodu,istisnakismikdvistisnasecimi5),
                    istisnakismikdvistisnasecimihizmetveteslimtutari5 = istisnakismikdvistisnasecimihizmetveteslimtutari5,
                    istisnakismikdvistisnasecimiyuklenilenkdv5 = istisnakismikdvistisnasecimiyuklenilenkdv5
                )
            if True:
                # TAM İSTİSNA KAPSAMINA GİREN İŞLEMLER
                tamistisnakodsecimi1 = request.POST.get("tamistisnakodsecimi1")
                tamistisnamalhizmeti1 = request.POST.get("tamistisnamalhizmeti1")
                tamistisnamalbedeli1 = request.POST.get("tamistisnamalbedeli1")
                tamistisnayuklenilenkdv1 = request.POST.get("tamistisnayuklenilenkdv1")
                tamistisnakodsecimi2 = request.POST.get("tamistisnakodsecimi2")
                tamistisnamalhizmeti2 = request.POST.get("tamistisnamalhizmeti2")
                tamistisnamalbedeli2 = request.POST.get("tamistisnamalbedeli2")
                tamistisnayuklenilenkdv2 = request.POST.get("tamistisnayuklenilenkdv2")
                tamistisnakodsecimi3 = request.POST.get("tamistisnakodsecimi3")
                tamistisnamalhizmeti3 = request.POST.get("tamistisnamalhizmeti3")
                tamistisnamalbedeli3 = request.POST.get("tamistisnamalbedeli3")
                tamistisnayuklenilenkdv3 = request.POST.get("tamistisnayuklenilenkdv3")
                tamistisnakodsecimi4 = request.POST.get("tamistisnakodsecimi4")
                tamistisnamalhizmeti4 = request.POST.get("tamistisnamalhizmeti4")
                tamistisnamalbedeli4 = request.POST.get("tamistisnamalbedeli4")
                tamistisnayuklenilenkdv4 = request.POST.get("tamistisnayuklenilenkdv4")
                tamistisnakodsecimi5 = request.POST.get("tamistisnakodsecimi5")
                tamistisnamalhizmeti5 = request.POST.get("tamistisnamalhizmeti5")
                tamistisnamalbedeli5= request.POST.get("tamistisnamalbedeli5")
                tamistisnayuklenilenkdv5 = request.POST.get("tamistisnayuklenilenkdv5")
                # TAM İSTİSNA KAPSAMINA GİREN İŞLEMLER
                tam_istisnaa_durumu.objects.create(
                bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                istisnaa1 = get_object_or_none(kdv_istisna_kodu,tamistisnakodsecimi1),tamistisnamalhizmeti1 =tamistisnamalhizmeti1,
                tamistisnamalbedeli1 =tamistisnamalbedeli1 ,istisnaa2 = get_object_or_none(kdv_istisna_kodu,tamistisnakodsecimi2),tamistisnamalhizmeti2 = tamistisnamalhizmeti2,
                tamistisnamalbedeli2 = tamistisnamalbedeli2,istisnaa3 = get_object_or_none(kdv_istisna_kodu,tamistisnakodsecimi3),
                tamistisnamalhizmeti3 = tamistisnamalhizmeti3,tamistisnamalbedeli3 = tamistisnamalbedeli3,
                istisnaa4= get_object_or_none(kdv_istisna_kodu,tamistisnakodsecimi4),tamistisnamalhizmeti4 = tamistisnamalhizmeti4,tamistisnamalbedeli4 = tamistisnamalbedeli4,istisnaa5 = get_object_or_none(kdv_istisna_kodu,tamistisnakodsecimi5),
                tamistisnamalhizmeti5 = tamistisnamalhizmeti5,tamistisnamalbedeli5 = tamistisnamalbedeli5,
                tamistisnayuklenilenkdv1 = tamistisnayuklenilenkdv1,tamistisnayuklenilenkdv2 = tamistisnayuklenilenkdv2,tamistisnayuklenilenkdv3 = tamistisnayuklenilenkdv3,
                tamistisnayuklenilenkdv4 = tamistisnayuklenilenkdv4,tamistisnayuklenilenkdv5 = tamistisnayuklenilenkdv5,

            )
            if True:
                #İSTEĞE BAĞLI TAM TEVKİFAT KAPSAMINA GİREN İŞLEMLER
                istege_baglitevkatgirenislemler = request.POST.getlist("istege_baglitevkatgirenislemler")
                teslimvehizmettutari = request.POST.getlist("teslimvehizmettutari")
                iadeyekonuolankdv = request.POST.getlist("iadeyekonuolankdv")
                #İSTEĞE BAĞLI TAM TEVKİFAT KAPSAMINA GİREN İŞLEMLER
                for i in range(0,len(istege_baglitevkatgirenislemler)):
                    if istege_baglitevkatgirenislemler[i] != "":
                        istegebaglitamtevkifat_giren_islemler.objects.create(
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                        bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                        islem_turu = get_object_or_none(tevkifat_tur_kodu,id = istege_baglitevkatgirenislemler[i]),
                        teslim_ve_hizmet = teslimvehizmettutari[i],iadeye_konu_olan_kdv =iadeyekonuolankdv[i] 
                        )
            if True:
                # DİĞER İADE HAKKI DOĞURAN İŞLEMLER
                digeriadersecim1 = request.POST.get("digeriadersecim1")
                digeriadetamistisnamalhizmeti1 = request.POST.get("digeriadetamistisnamalhizmeti1")
                digeriadekonuolankdv1 = request.POST.get("digeriadekonuolankdv1")
                digeriadersecim2 = request.POST.get("digeriadersecim2")
                digeriadetamistisnamalhizmeti2 = request.POST.get("digeriadetamistisnamalhizmeti2")
                digeriadekonuolankdv2 = request.POST.get("digeriadekonuolankdv2")
                digeriadersecim3 = request.POST.get("digeriadersecim3")
                digeriadetamistisnamalhizmeti3 = request.POST.get("digeriadetamistisnamalhizmeti3")
                digeriadekonuolankdv3 = request.POST.get("digeriadekonuolankdv3")
                digeriadersecim4 = request.POST.get("digeriadersecim4")
                digeriadetamistisnamalhizmeti4 = request.POST.get("digeriadetamistisnamalhizmeti4")
                digeriadekonuolankdv4 = request.POST.get("digeriadekonuolankdv4")
                digeriadersecim5 = request.POST.get("digeriadersecim5")
                digeriadetamistisnamalhizmeti5 = request.POST.get("digeriadetamistisnamalhizmeti5")
                digeriadekonuolankdv5 = request.POST.get("digeriadekonuolankdv5")
                # DİĞER İADE HAKKI DOĞURAN İŞLEMLER
                iade_hakki_digerislemleri.objects.create(
                    bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    bilgi = digeriadersecim1,digeriadetamistisnamalhizmeti1 = digeriadetamistisnamalhizmeti1,digeriadekonuolankdv1 = digeriadekonuolankdv1,
                    bilgi2 = digeriadersecim2,digeriadetamistisnamalhizmeti2 = digeriadetamistisnamalhizmeti2,
                    digeriadekonuolankdv2 = digeriadekonuolankdv2,bilgi3 = digeriadersecim3,
                    digeriadetamistisnamalhizmeti3 = digeriadetamistisnamalhizmeti3,digeriadekonuolankdv3 = digeriadekonuolankdv3,
                    bilgi4 = digeriadersecim4,digeriadetamistisnamalhizmeti4 = digeriadetamistisnamalhizmeti4,
                    digeriadekonuolankdv4 = digeriadekonuolankdv4,bilgi5 = digeriadersecim5,
                    digeriadetamistisnamalhizmeti5 = digeriadetamistisnamalhizmeti5,digeriadekonuolankdv5 = digeriadekonuolankdv5
                )
            if True:
                #İHRAÇ KAYDIYLA TESLİMLER
                ihrackayditurusecimi = request.POST.getlist("ihrackayditurusecimi")
                ihrackayditutar = request.POST.getlist("ihrackayditutar")
                ihrackaydikdvorani = request.POST.getlist("ihrackaydikdvorani")
                hesaplanantutar = request.POST.getlist("hesaplanantutar")
                #İHRAÇ KAYDIYLA TESLİMLER
                for i in range(0,len(ihrackayditurusecimi)):
                    if ihrackayditurusecimi[i]  != "":
                        ihrac_kaydiyla_teslimler.objects.create(
                            bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
                    bagli_oldugu_beyanname = get_object_or_404(kdv1_beyannamesi_bilgileri,id = beyanname_bilgisi.id),
                    islem_turu = ihrackayditurusecimi[i],ihrac_kaydiyla_teslimler_tutar = ihrackayditutar[i],
                    ihrackaydikdvorani = float(ihrackaydikdvorani[i]),hesaplanantutar = hesaplanantutar[i]
                        )
        #
        ihrackayditeslimbedeltoplami = request.POST.get("ihrackayditeslimbedeltoplami")
        teciledilebilirkdv = request.POST.get("teciledilebilirkdv")
        ihracatingerceklestigiiadeedilecekteciledilmeyenkdv = request.POST.get("ihracatingerceklestigiiadeedilecekteciledilmeyenkdv")
        yurticivedisikdvodemeksizinteminedilenmalbedeli = request.POST.get("yurticivedisikdvodemeksizinteminedilenmalbedeli")
        ihracatingerceklestigidonemiadekdv = request.POST.get("ihracatingerceklestigidonemiadekdv")
        yuklenilenkdv = request.POST.get("yuklenilenkdv")
        indirimlioranatabimallarinihrackaydi = request.POST.get("indirimlioranatabimallarinihrackaydi")

        #KDV Kanunun 13/F Maddesi Kapsamında Yüklenici Firmalara Yapılan Teslim Ve Hizmetlere Ait Liste
        istisnabelgesiniduzenleeynkurulus = request.POST.getlist("istisnabelgesiniduzenleeynkurulus")
        istisnabelgesinintarihi = request.POST.getlist("istisnabelgesinintarihi")
        istisnabelgesisayisi = request.POST.getlist("istisnabelgesisayisi")
        istisnabelgesinintarihionaylanan = request.POST.getlist("istisnabelgesinintarihionaylanan")
        istisnabelgesisayisionaylanan = request.POST.getlist("istisnabelgesisayisionaylanan")
        alicifirmaadisoyadibilgdsi = request.POST.getlist("alicifirmaadisoyadibilgdsi")
        tcvergikimlikno = request.POST.getlist("tcvergikimlikno")
        malinhizmetnumarasisirasi = request.POST.getlist("malinhizmetnumarasisirasi")
        malinolcubirimi = request.POST.get("malinolcubirimi")
        malinhizmetintutari = request.POST.getlist("malinhizmetintutari")
        faturatarihi = request.POST.getlist("faturatarihi")
        faturano = request.POST.getlist("faturano")
        faturabedeli = request.POST.getlist("faturabedeli")
        #KDV Kanunun 13/F Maddesi Kapsamında Yüklenici Firmalara Yapılan Teslim Ve Hizmetlere Ait Liste
        #Türk Hava Kuvetlerinin Güçlenmesine Katılım Payı
        satilanbiletadeti = request.POST.getlist("satilanbiletadeti")
        satilanbiletpaytutari = request.POST.getlist("satilanbiletpaytutari")
        satilanbilettopamtutar = request.POST.getlist("satilanbilettopamtutar")
        #Türk Hava Kuvetlerinin Güçlenmesine Katılım Payı
        #KISMİ TEVKİFAT UYGULAMASI KAPSAMINDAKİ İŞLEMLERE AİT BİLDİRİM
        kismitevkifatalicitcvergikimlikl = request.POST.getlist("kismitevkifatalicitcvergikimlikl")
        kismitevkifatalicivergikimlikl = request.POST.getlist("kismitevkifatalicivergikimlikl")
        kismitevkifataliciadisoyadi = request.POST.getlist("kismitevkifataliciadisoyadi")
        kismitevkifatbelgetarihi = request.POST.getlist("kismitevkifatbelgetarihi")
        kismitevkifatbelgeserisi = request.POST.getlist("kismitevkifatbelgeserisi")
        kismitevkifatbelgesiranosu = request.POST.getlist("kismitevkifatbelgesiranosu")
        kismitevkifatislemcinsi = request.POST.getlist("kismitevkifatislemcinsi")
        kismitevkifatistutari = request.POST.getlist("kismitevkifatistutari")
        kismitevkifatkdvorani = request.POST.getlist("kismitevkifatkdvorani")
        kismitevkifatorani = request.POST.getlist("kismitevkifatorani")
        tevkifathhesapkdvtutari = request.POST.getlist("tevkifathhesapkdvtutari")
        alicitarafinabeyanedilecekkdvtutari = request.POST.getlist("alicitarafinabeyanedilecekkdvtutari")
        #KISMİ TEVKİFAT UYGULAMASI KAPSAMINDAKİ İŞLEMLERE AİT BİLDİRİM
        #İSTEĞE BAĞLI TAM TEVKİFAT UYGULAMASI KAPSAMINDAKİ İŞLEMLERE AİT BİLDİRİM
        alicinintcsi = request.POST.getlist("alicinintcsi")
        alicininvergisi = request.POST.getlist("alicininvergisi")
        aliciadisoyadiunvan = request.POST.getlist("aliciadisoyadiunvan")
        faturabenzeritarih = request.POST.getlist("faturabenzeritarih")
        faturabenzerisira = request.POST.getlist("faturabenzerisira")
        alicikismiislemturu = request.POST.getlist("alicikismiislemturu")
        islemtutarikdvszi = request.POST.getlist("islemtutarikdvszi")
        kdvoranialicinin = request.POST.getlist("kdvoranialicinin")
        vergisiialicinin = request.POST.getlist("vergisiialicinin")
        #İSTEĞE BAĞLI TAM TEVKİFAT UYGULAMASI KAPSAMINDAKİ İŞLEMLERE AİT BİLDİRİM
        #Teknoloji Geliştirme Bölgeleri
        teknolojigelistirme = request.POST.getlist("teknolojigelistirme")
        projeninbaslangictarihi = request.POST.getlist("projeninbaslangictarihi")
        projebelgesininnumarasi = request.POST.getlist("projebelgesininnumarasi")
        projeninihizmetbedeli = request.POST.getlist("projeninihizmetbedeli")
        projeninyuklenilenkdv = request.POST.getlist("projeninyuklenilenkdv")
        #Teknoloji Geliştirme Bölgeleri
        #Yatırım Teşvik Belgesi Kapsamında Makina Techizat Alımlarına İlişkin Bildirim
        saticininverginosu = request.POST.getlist("saticininverginosu")
        saticininvergidairesikodu = request.POST.getlist("saticininvergidairesikodu")
        saticininadisoyadi = request.POST.getlist("saticininadisoyadi")
        alinanmalintutari = request.POST.getlist("alinanmalintutari")
        tesvikbelgesinintarihi = request.POST.getlist("tesvikbelgesinintarihi")
        tesvikbelgesininnosu = request.POST.getlist("tesvikbelgesininnosu")
        alinanmalincinsi = request.POST.getlist("alinanmalincinsi")
        alinanmalinmiktari = request.POST.getlist("alinanmalinmiktari")
        alisfaturasintarihi = request.POST.getlist("alisfaturasintarihi")
        alisfaturasisayisi = request.POST.getlist("alisfaturasisayisi")
        #Yatırım Teşvik Belgesi Kapsamında Makina Techizat Alımlarına İlişkin Bildirim
        #3065 Sayılı Kanun 13/i Maddesindeki İstisna Kapsamında Yapılan Teslimlere İlişkin Bildirim
        aliciadisoyadiunvantasinmaz = request.POST.getlist("aliciadisoyadiunvantasinmaz")
        alicivergikimliknosutasinmaz = request.POST.getlist("alicivergikimliknosutasinmaz")
        alicininuyrugu = request.POST.getlist("alicininuyrugu")
        alicinincalismaveoturmaizni = request.POST.getlist("alicinincalismaveoturmaizni")
        tasinmazinilveilce = request.POST.getlist("tasinmazinilveilce")
        tasinmazinniteligi = request.POST.getlist("tasinmazinniteligi")
        tasinmazinada = request.POST.getlist("tasinmazinada")
        tasinmazinparsel = request.POST.getlist("tasinmazinparsel")
        tasinmazinulusaladresnumarasi = request.POST.getlist("tasinmazinulusaladresnumarasi")
        alicininismerkezininbulunduguulke = request.POST.getlist("alicininismerkezininbulunduguulke")
        tasinmazinusistemnumarasi = request.POST.getlist("tasinmazinusistemnumarasi")
        satisfaturasinintarihi = request.POST.getlist("satisfaturasinintarihi")
        satisfaturasisayisi = request.POST.getlist("satisfaturasisayisi")
        satisfaturasitarihi = request.POST.getlist("satisfaturasitarihi")
        #3065 Sayılı Kanun 13/i Maddesindeki İstisna Kapsamında Yapılan Teslimlere İlişkin Bildirim
        #DEĞERSİZ HALE GELEN ALACAKLARA İLİŞKİN BİLDİRİM
        borclununverginosu = request.POST.getlist("borclununverginosu")
        borclununadisoyadi = request.POST.getlist("borclununadisoyadi")
        borclununfaturabenzeritarihi = request.POST.getlist("borclununfaturabenzeritarihi")
        borclununfaturabenzeribelgeninserisi = request.POST.getlist("borclununfaturabenzeribelgeninserisi")
        borclununfaturabenzeribelgeninsiranosu = request.POST.getlist("borclununfaturabenzeribelgeninsiranosu")
        degersizhalegelenalacaktutari = request.POST.getlist("degersizhalegelenalacaktutari")
        degersizhalegelenalacakkdvsi = request.POST.getlist("degersizhalegelenalacakkdvsi")
        degersizhalegelenalacaktutartarih = request.POST.getlist("degersizhalegelenalacaktutartarih")
        #DEĞERSİZ HALE GELEN ALACAKLARA İLİŞKİN BİLDİRİM
        #107 KOD NUMARALI SATIR ARACILIĞIYLA İNDİRİM KONUSU YAPILAN KDV ALACAĞININ DÖNEMİ
        faturaaysecimi = request.POST.getlist("faturaaysecimi")
        faturayili = request.POST.getlist("faturayili")
        faturatoplamkdvtutari = request.POST.getlist("faturatoplamkdvtutari")
        indirimkonusuyapilankdvtutari = request.POST.getlist("indirimkonusuyapilankdvtutari")
        #107 KOD NUMARALI SATIR ARACILIĞIYLA İNDİRİM KONUSU YAPILAN KDV ALACAĞININ DÖNEMİ
        # TAM VE KISMİ İSTİSNALARA İLİŞKİN BİLDİRİM
        istisnabelgeturu = request.POST.getlist("istisnabelgeturu")
        bolge = request.POST.getlist("bolge")
        belgeno = request.POST.getlist("belgeno")
        teslimbedeli = request.POST.getlist("teslimbedeli")
        tabiolduguoran = request.POST.getlist("tabiolduguoran")
        belgesahibivergikimlik = request.POST.getlist("belgesahibivergikimlik")
        # TAM VE KISMİ İSTİSNALARA İLİŞKİN BİLDİRİM
        #YENİLENMİŞ CEP TELEFONU SATIŞLARINA İLİŞKİN BİLDİRİM
        telefonalisbelgesituru = request.POST.getlist("telefonalisbelgesituru")
        telefonalistarihi = request.POST.getlist("telefonalistarihi")
        telefonalisbelgeno = request.POST.getlist("telefonalisbelgeno")
        telefonsqaticikimlikturu = request.POST.getlist("telefonsqaticikimlikturu")
        telefonsaticininkimlikno = request.POST.getlist("telefonsaticininkimlikno")
        telefonsaticininadisoyadi = request.POST.getlist("telefonsaticininadisoyadi")
        telefonalisbedeli = request.POST.getlist("telefonalisbedeli")
        telefonvarsaodenenkdv = request.POST.getlist("telefonvarsaodenenkdv")
        telefonmarka = request.POST.getlist("telefonmarka")
        telefonmodel = request.POST.getlist("telefonmodel")
        telefonimei = request.POST.getlist("telefonimei")
        telefonsatisbelgesituru = request.POST.getlist("telefonsatisbelgesituru")
        telefonsatistarihi = request.POST.getlist("telefonsatistarihi")
        telefonsatisbelgeno = request.POST.getlist("telefonsatisbelgeno")
        telefonalicininkimlikturu = request.POST.getlist("telefonalicininkimlikturu")
        telefonalicininninkimlikno = request.POST.getlist("telefonalicininninkimlikno")
        telefonalicininninadisoyadi = request.POST.getlist("telefonalicininninadisoyadi")
        telefonsatisbedeli = request.POST.getlist("telefonsatisbedeli")
        telefonsatisvarsaodenenkdv = request.POST.getlist("telefonsatisvarsaodenenkdv")
        #YENİLENMİŞ CEP TELEFONU SATIŞLARINA İLİŞKİN BİLDİRİM
    return render(request,"beyannameler/kdv1_beyanname.html",content)

#kdv1
def kdv2_beyannamesi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(301,326):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_300ler = []
    for i in range(301,326):
        tevk_300ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_300ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    content["kdv_tamtefikat"]=["101 - İKAMETGÂHI, İŞYERİ, KANUNİ MERKEZİ VE İŞ MERKEZİ TÜRKİYEDE BULUNMAYANLAR TARAFINDAN YAPILAN İŞLEMLER [GT 117-Bölüm (2.1)]",
                               "102 - SERBEST MESLEK FAALİYETİ ÇERÇEVESİNDE YAPILAN TESLİM VE HİZMETLER [GT 117-Bölüm (2.2)]",
                               "103 - KİRALAMA İŞLEMLERİ [GT 117-Bölüm (2.3)]",
                               "104 - REKLÂM VERME İŞLEMLERİ [GT 117-Bölüm (2.4)]",
                               "105 - 5300 SAYILI KANUN KAPSAMINDA DÜZENLENEN ÜRÜN SENETLERİNİN TEMSİL ETTİĞİ ÜRÜNÜ DEPODAN ÇEKECEK OLANLARA YAPILACAK TESLİMLER [KDV GUT -(II/F-4.18.4)]",
                               "106 - İTHAL EDİLEN MALIN BEDELİNDE SONRADAN ORTAYA ÇIKAN ÖDEMELER",
                               "150 - DİĞERLERİ"]
    if request.POST:
        aysecimi = request.POST.get("aysecimi")
        donem = request.POST.get("donem")
        #TAM TEVKİFAT UYGULANAN İŞLEMLERE AİT BİLDİRİM
        islemturu6 = request.POST.get("islemturu6")
        matrah6 = request.POST.get("matrah6")
        kdv6 = request.POST.get("kdv6")
        vergi7 = request.POST.get("vergi7")
        islemturu8 = request.POST.get("islemturu8")
        matrah8 = request.POST.get("matrah8")
        kdv8 = request.POST.get("kdv8")
        vergi9 = request.POST.get("vergi9")
        islemturu10 = request.POST.get("islemturu10")
        matrah10 = request.POST.get("matrah10")
        kdv10 = request.POST.get("kdv10")
        vergi11 = request.POST.get("vergi11")
        islemturu12 = request.POST.get("islemturu12")
        matrah12 = request.POST.get("matrah12")
        kdv12 = request.POST.get("kdv12")
        vergi13 = request.POST.get("vergi13")
        vergitoplami = request.POST.get("vergitoplami")
        matrahtoplami = request.POST.get("matrahtoplami")
        #TAM TEVKİFAT UYGULANAN İŞLEMLERE AİT BİLDİRİM
        #İSTEĞE BAĞLI TAM TEVKİFAT UYGULANAN İŞLEMLERE AİT BİLDİRİM
        istege_baglitevkat = request.POST.getlist("istege_baglitevkat")
        istegebaglimatrah = request.POST.getlist("istegebaglimatrah")
        istebaglikdv = request.POST.getlist("istebaglikdv")
        istebaglivergi = request.POST.getlist("istebaglivergi")
        #İSTEĞE BAĞLI TAM TEVKİFAT UYGULANAN İŞLEMLERE AİT BİLDİRİM
        #KISMİ TEVKİFAT UYGULANAN İŞLEMLERE AİT BİLDİRİM
        secimtevkifat16 = request.POST.get("secimtevkifat16")
        matrah16 = request.POST.get("matrah16")
        kdv16 = request.POST.get("kdv16")
        tevkifat16 = request.POST.get("tevkifat16")
        vergi17 = request.POST.get("vergi17")
        secimtevkifat18 = request.POST.get("secimtevkifat18")
        matrah18 = request.POST.get("matrah18")
        kdv18 = request.POST.get("kdv18")
        tevkifat18 = request.POST.get("tevkifat18")
        vergi19 = request.POST.get("vergi19")
        secimtevkifat20 = request.POST.get("secimtevkifat20")
        matrah20 = request.POST.get("matrah20")
        kdv20 = request.POST.get("kdv20")
        tevkifat20 = request.POST.get("tevkifat20")
        vergi21 = request.POST.get("vergi21")
        secimtevkifat22 = request.POST.get("secimtevkifat22")
        matrah22 = request.POST.get("matrah22")
        kdv22 = request.POST.get("kdv22")
        tevkifat22 = request.POST.get("tevkifat22")
        vergi23 = request.POST.get("vergi23")
        secimtevkifat24 = request.POST.get("secimtevkifat24")
        matrah24 = request.POST.get("matrah24")
        kdv24 = request.POST.get("kdv24")
        tevkifat24 = request.POST.get("tevkifat24")
        vergi25 = request.POST.get("vergi25")
        secimtevkifat26 = request.POST.get("secimtevkifat26")
        matrah26 = request.POST.get("matrah26")
        kdv26 = request.POST.get("kdv26")
        tevkifat26 = request.POST.get("tevkifat26")
        vergi27 = request.POST.get("vergi27")
        matrahtoplamikismi = request.POST.get("matrahtoplamikismi")
        vergitoplamikimi = request.POST.get("vergitoplamikimi")
        toplamkdvmatrahi = request.POST.get("toplamkdvmatrahi")
        tevkiedilenkdvtoplami = request.POST.get("tevkiedilenkdvtoplami")
        İlaveedilecekkdv = request.POST.get("İlaveedilecekkdv")
        odemesigerekenkdv = request.POST.get("odemesigerekenkdv")
        #KISMİ TEVKİFAT UYGULANAN İŞLEMLERE AİT BİLDİRİM
        #KATMA DEĞER VERGİSİ KESİNTİSİ YAPILAN MÜKELLEFLERE AİT BİLDİRİM
        soyadiunvan = request.POST.getlist("soyadiunvan")
        adiunvan = request.POST.getlist("adiunvan")
        vergikimlikno = request.POST.getlist("vergikimlikno")
        tckimlikno = request.POST.getlist("tckimlikno")
        vergiyetabimatrah = request.POST.getlist("vergiyetabimatrah")
        tevkifedilenmatrah = request.POST.getlist("tevkifedilenmatrah")
        odemeturu = request.POST.getlist("odemeturu")
        #KATMA DEĞER VERGİSİ KESİNTİSİ YAPILAN MÜKELLEFLERE AİT BİLDİRİM 
        #TAM TEVKİFAT KAPSAMINDA İTHALAT İŞLEMLERİNE İLİŞKİN BİLGİLER
        islemturutamtevkifat = request.POST.getlist("islemturutamtevkifat")
        tamtevkifattarihi = request.POST.getlist("tamtevkifattarihi")
        dolasimagirenbeyannamesayisi = request.POST.getlsit("dolasimagirenbeyannamesayisi")
        odememememuhafiyeti = request.POST.getlist("odememememuhafiyeti")
        #TAM TEVKİFAT KAPSAMINDA İTHALAT İŞLEMLERİNE İLİŞKİN BİLGİLER
        #İSTEĞE BAĞLI TAM TEVKİFAT UYGULAMASI KAPSAMINDAKİ İŞLEMLERE AİT BİLDİRİM
        alicinintcsi = request.POST.getlist("alicinintcsi")
        alicininvergisi = request.POST.getlist("alicininvergisi")
        aliciadisoyadiunvan = request.POST.getlist("aliciadisoyadiunvan")
        faturabenzeritarih = request.POST.getlist("faturabenzeritarih")
        faturabenzerisira = request.POST.getlist("faturabenzerisira")
        alicikismiislemturu = request.POST.getlist("alicikismiislemturu")
        islemtutarikdvszi = request.POST.getlist("islemtutarikdvszi")
        kdvoranialicinin = request.POST.getlist("kdvoranialicinin")
        vergisiialicinin = request.POST.getlist("vergisiialicinin")
        #İSTEĞE BAĞLI TAM TEVKİFAT UYGULAMASI KAPSAMINDAKİ İŞLEMLERE AİT BİLDİRİM
    return render(request,"beyannameler/kdv2_beyanname.html",content)
def kdv4_beyannamesi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    if request.POST:
        #hasılat Bilgdirimi
        matrah1 = request.POST.get("matrah1")
        kdvorani1 = request.POST.get("kdvorani1")
        hesaplanankdv1 = request.POST.get("hesaplanankdv1")
        hasilat1 = request.POST.get("hasilat1")
        matrah2 = request.POST.get("matrah2")
        kdvorani2 = request.POST.get("kdvorani2")
        hesaplanankdv2 = request.POST.get("hesaplanankdv2")
        hasilat2 = request.POST.get("hasilat2")
        matrah3 = request.POST.get("matrah3")
        kdvorani3 = request.POST.get("kdvorani3")
        hesaplanankdv3 = request.POST.get("hesaplanankdv3")
        hasilat3 = request.POST.get("hasilat3")
        toplam = request.POST.get("toplam")
        nethasilat = request.POST.get("nethasilat")
        gerceklesmeyenislsem = request.POST.get("gerceklesmeyenislsem")
        #hasılat Bilgdirimi
        #Vergi Bildirimi
        nethasilat2 = request.POST.get("nethasilat2")
        nethasilatuygulanacakvergiorani = request.POST.get("nethasilatuygulanacakvergiorani")
        hasitatkapasamindaodemesigerekenvergi =request.POST.get("hasitatkapasamindaodemesigerekenvergi")
        toplamhasilatkumeletif =request.POST.get("toplamhasilatkumeletif")

        #Vergi Bildirimi
    return render(request,"beyannameler/kdv4_beyanname.html",content)

def gecici_beyanname(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    content["indiirimler"] = gecicivergi_beyannamesi_inidimi.objects.all()
    content["iller_ilkodu"] = iller_ilkodu.objects.all()
    content["saglikhizmetindenfaydalananisletmeturu"] = saglikhizmetindenfaydalananisletmeturu.objects.all()
    content["saglikhizmetindenfaydalananisletmeadi"] = saglikhizmetindenfaydalananisletmeadi.objects.all()
    if request.POST:
        aysecimi = request.POST.get("aysecimi")
        ticarikazanczarar = request.POST.get("ticarikazanczarar")
        ticarikazanckar = request.POST.get("ticarikazanckar")
        yatiriminsindirimizarar = request.POST.get("yatirimindiirmizarar")
        istisnalarzarar = request.POST.get("istisnalarzarar")
        kalanticarikazanckar = request.POST.get("kalanticarikazanckar")
        serbestmeslekkazancizarar = request.POST.get("serbestmeslekkazancizarar")
        serbestmeslekkazancikar = request.POST.get("serbestmeslekkazancikar")
        indirim1 = request.POST.get("indirim1")
        tutari1 = request.POST.get("tutari1")
        indirim2 = request.POST.get("indirim2")
        tutari2 = request.POST.get("tutari2")
        indirim3 = request.POST.get("indirim3")
        tutari3 = request.POST.get("tutari3")
        indirim4 = request.POST.get("indirim4")
        tutari4 = request.POST.get("tutari4")
        indirim5 = request.POST.get("indirim5")
        tutari5 = request.POST.get("tutari5")
        toplambilgisi = request.POST.get("toplambilgisi")
        donemzarari = request.POST.get("donemzarari")
        gecicivergimatrahi = request.POST.get("gecicivergimatrahi")
        gecicvergiyetabimatrah = request.POST.get("gecicvergiyetabimatrah")
        gecicvergiorani = request.POST.get("gecicvergiorani")
        geneloranatabivergimatrahi = request.POST("geneloranatabivergimatrahi")
        #
        gecicivergimatrahi = request.POST.get("gecicivergimatrahi")
        hesaplanangecicivergi = request.POST.get("hesaplanangecicivergi")
        oncekideonemlerdehesaplanangecicivergi = request.POST.get("oncekideonemlerdehesaplanangecicivergi")
        odenmesigerekenvergi = request.POST.get("odenmesigerekenvergi")
        mahsupedilecektevkifat = request.POST.get("mahsupedilecektevkifat")
        mahsupedilecekgecicivergivetevkifattoplami = request.POST.get("mahsupedilecekgecicivergivetevkifattoplami")
        odenecekgecicivergi = request.POST.get("odenecekgecicivergi")
        sonrakidonemdedevredentevkifattutari = request.POST.get("sonrakidonemdedevredentevkifattutari")
        sonrakidonemedevredengecicivergi = request.POST.get("sonrakidonemedevredengecicivergi")
        damgavergisi = request.POST.get("damgavergisi")
        #
        faliyetkodu1 = request.POST.get("faliyetkodu1")
        burtutsatistutari1 = request.POST.get("burtutsatistutari1")
        faliyetkodu2 = request.POST.get("faliyetkodu2")
        burtutsatistutari2 = request.POST.get("burtutsatistutari2")
        faliyetkodu3 = request.POST.get("faliyetkodu3")
        burtutsatistutari3 = request.POST.get("burtutsatistutari3")
        #
        istisna1 = request.POST.get("istisna1")
        kar1 = request.POST.get("kar1")
        zarar1 = request.POST.get("zarar1")
        istisna2 = request.POST.get("istisna2")
        kar2 = request.POST.get("kar2")
        zarar2 = request.POST.get("zarar2")
        istisna3 = request.POST.get("istisna3")
        kar3 = request.POST.get("kar3")
        zarar3 = request.POST.get("zarar3")
        istisna4 = request.POST.get("istisna4")
        kar4 = request.POST.get("kar4")
        zarar4 = request.POST.get("zarar4")
        istisna5 = request.POST.get("istisna5")
        kar5 = request.POST.get("kar5")
        zarar5 = request.POST.get("zarar5")
        istisna6 = request.POST.get("istisna6")
        kar6 = request.POST.get("kar6")
        zarar6 = request.POST.get("zarar6")
        istisna7 = request.POST.get("istisna7")
        kar7 = request.POST.get("kar7")
        zarar7 = request.POST.get("zarar7")
        istisna8 = request.POST.get("istisna8")
        kar8 = request.POST.get("kar8")
        zarar8 = request.POST.get("zarar8")
        #
        istisnaturu = request.POST.get("istisnaturu")
        vergivetc = request.POST.get("vergivetc")
        #
        patentfaydalibelge = request.POST.getlist("patentfaydalibelge")
        numarasi = request.POST.getlist("numarasi")
        korumasonaeristarihi = request.POST.getlist("korumasonaeristarihi")
        istisnayakonukacanctutari = request.POST.getlist("istisnayakonukacanctutari")
        kazancturur = request.POST.getlist("kazancturur")
        #Yurtdışı Mukimi Kişi ve/veya Kurumbra Verien Sağlık Hizmetlerine ilişkin Fonm
        saglikhizmetindenfaydalanankisiadisoyadi = request.POST.getlist("saglikhizmetindenfaydalanankisiadisoyadi")
        saglikhizmetindenfaydalanankisidogumtarihi = request.POST.getlist("saglikhizmetindenfaydalanankisidogumtarihi")
        saglikhizmetindenfaydalanankisiuyrugu = request.POST.getlist("saglikhizmetindenfaydalanankisiuyrugu")
        saglikhizmetindenfaydalanankisipasaportnosu = request.POST.getlist("saglikhizmetindenfaydalanankisipasaportnosu")
        saglikhizmetindenfaydalananyerilkodu = request.POST.getlist("saglikhizmetindenfaydalananyerilkodu")
        saglikhizmetindenfaydalananisletmeturu1 = request.POST.getlist("saglikhizmetindenfaydalananisletmeturu")
        saglikhizmetindenfaydalananisletmeadi1 = request.POST.getlist("saglikhizmetindenfaydalananisletmeadi")
        faturayiduzenleyenkurumkisi = request.POST.getlist("faturayiduzenleyenkurumkisi")
        faturaduzenlemetarihi = request.POST.getlist("faturaduzenlemetarihi")
        faturakdvstutari = request.POST.getlist("faturakdvstutari")
        faturaduzenlemesayisi = request.POST.getlist("faturaduzenlemesayisi")
        #Yurtdışı Mukimi Kişi ve/veya Kurumbra Verien Egitim Hizmetlerine ilişkin Fonm
        egitimhizmetindenfaydalanankisiadisoyadi =request.POST.getlist("egitimhizmetindenfaydalanankisiadisoyadi")
        egitimhizmetindenfaydalanankisidogumtarihi = request.POST.getlist("egitimhizmetindenfaydalanankisidogumtarihi")
        egitimhizmetindenfaydalanankisiuyrugu = request.POST.getlist("egitimhizmetindenfaydalanankisiuyrugu")
        egitimhizmetindenfaydalanankisipasaportnosu = request.POST.getlist("egitimhizmetindenfaydalanankisipasaportnosu")
        egitimhizmetindenfaydalananyerilkodu = request.POST.getlist("egitimhizmetindenfaydalananyerilkodu")
        egitimhizmetindenfaydalananisletmeturu = request.POST.getlist("egitimhizmetindenfaydalananisletmeturu")
        egitimfaturayiduzenleyenkurumkisi = request.POST.getlist("egitimfaturayiduzenleyenkurumkisi")
        egitimfaturaduzenlemetarihi = request.POST.getlist("egitimfaturaduzenlemetarihi")
        egitimfaturaduzenlemesayisi = request.POST.getlist("egitimfaturaduzenlemesayisi")
        egitimfaturakdvstutari = request.POST.getlist("egitimfaturakdvstutari")

        #
        alinanhizmetturu = request.POST.getlist("alinanhizmetturu")
        hizmettesebusvergiveyatc = request.POST.getlist("hizmettesebusvergiveyatc")
        hizmettesebusadisoyadiunvan = request.POST.getlist("hizmettesebusadisoyadiunvan")
        hizmetinbelgeturu = request.POST.getlist("hizmetinbelgeturu")
        hizmetlerinbelgetarihi = request.POST.getlist("hizmetlerinbelgetarihi")
        hizmetbelgeserino = request.POST.getlist("hizmetbelgeserino")
        hizmettutarbilgisi = request.POST.getlist("hizmettutarbilgisi")

    return render(request,"beyannameler/gecici_beyanname.html",content)
def kurumlar_vergisi_beyanname(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["dar_mukellef"] = kurumlar_dar_mukkelef_kimlik_ve_adres_bilgisi.objects.filter(sube_bilgisi =sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first() ).last()
    content["bilgi1"] = zarar_olsa_dahi_indilicekistisnaveindirim.objects.all()
    content["bilgi2"] = kazancin_bulunmasi_halinde_indirilecek_istisna_veindirimler.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        subeli = request.POST.get("sube")
        cikisyeri = request.POST.get("cikisyeri")
        ajanlik = request.POST.get("ajanlik")
        imalatyeri = request.POST.get("imalatyeri")
        satisyeri = request.POST.get("satisyeri")
        sair = request.POST.get("sair")
        #
        istisnazarari2016 = request.POST.get("istisnazarari2016")
        digerzararlar2016 = request.POST.get("digerzararlar2016")
        istisnazarari2017 = request.POST.get("istisnazarari2017")
        digerzararlar2017 = request.POST.get("digerzararlar2017")
        istisnazarari2018 = request.POST.get("istisnazarari2018")
        digerzararlar2018 = request.POST.get("digerzararlar2018")
        istisnazarari2019 = request.POST.get("istisnazarari2019")
        digerzararlar2019 = request.POST.get("digerzararlar2019")
        istisnazarari2020 = request.POST.get("istisnazarari2020")
        digerzararlar2020 = request.POST.get("digerzararlar2020")
        zararlartoplam = request.POST.get("zararlartoplam")
        #
        ticaribilanco = request.POST.get("ticaribilanco")
        ticaribilancozarar = request.POST.get("ticaribilancozarar")
        ticaribilancokar = request.POST.get("ticaribilancokar")
        addolananagelirkar = request.POST.get("addolananagelirkar")
        addolananagelir = request.POST.get("addolananagelir")
        #
        ilaveler1 = request.POST.get("ilaveler1")
        ilavelertutar1 = request.POST.get("ilavelertutar1")
        ilaveler2 = request.POST.get("ilaveler2")
        ilavelertutar2 = request.POST.get("ilavelertutar2")
        ilavelertoplambilgisi = request.POST.get("ilavelertoplambilgisi")
        ilavelertoplam = request.POST.get("ilavelertoplam")
        #
        istisnaindirim1 = request.POST.getlist("istisnaindirim1")
        istisnaindirimtutar1 = request.POST.getlist("istisnaindirimtutar1")
        istisnaindirimtutartoplambilgisi = request.POST.get("istisnaindirimtutartoplambilgisi")
        istisnaindirimtutartoplam = request.POST.get("istisnaindirimtutartoplam")
        #
        karilavetoplami = request.POST.get("karilavetoplami")
        karilavetoplamitutri = request.POST.get("karilavetoplamitutri")
        cariyilaiatistisnaindirim = request.POST.get("cariyilaiatistisnaindirim")
        cariyilaiatistisnaindirimtutari = request.POST.get("cariyilaiatistisnaindirimtutari")
        zararbilgisi = request.POST.get("zararbilgisi")
        zararbilgisitutari = request.POST.get("zararbilgisitutari")
        karbilgisi = request.POST.get("karbilgisi")
        karbilgisitutari =request.POST.get("karbilgisitutari")
        digeryilzararlari = request.POST.get("digeryilzararlari")
        digeryilzararlaritutari = request.POST.get("digeryilzararlaritutari")
        istisnadanyilzararlaritutari = request.POST.get("istisnadanyilzararlaritutari")
        mahsupedilecekgrcmisyilzararlari = request.POST.get("mahsupedilecekgrcmisyilzararlari")
        mahsupedilecekgrcmisyilzararlaritutari = request.POST.get("mahsupedilecekgrcmisyilzararlaritutari")
        indirimesas = request.POST.get("indirimesas")
        indirimesastutari = request.POST.get("indirimesastutari")
        #
        kazancindirimleri = request.POST.getlist("kazancindirimleri")
        kazancindirimleritutar = request.POST.getlist("kazancindirimleritutar")
        kazancindirimleritopamtutar = request.POST.get("kazancindirimleritopamtutar")
        kazancindirimleritopam = request.POST.get("kazancindirimleritopam")
        #
        vergibildiirmibilgi1 = request.POST.get("vergibildiirmibilgi1")
        vergibildiirmitutar1 = request.POST.get("vergibildiirmitutar1")
        vergibildiirmibilgi2 = request.POST.get("vergibildiirmibilgi2")
        fav_language  = request.POST.get("fav_language")
        vergibildiirmibilgi3 = request.POST.get("vergibildiirmibilgi3")
        vergibildiirmitutar3 = request.POST.get("vergibildiirmitutar3")
        vergibildiirmibilgi4 = request.POST.get("vergibildiirmibilgi4")
        vergibildiirmitutar4 = request.POST.get("vergibildiirmitutar4")
        vergibildiirmibilgi5 = request.POST.get("vergibildiirmibilgi5")
        vergibildiirmitutar5 = request.POST.get("vergibildiirmitutar5")
        vergibildiirmibilgi6 = request.POST.get("vergibildiirmibilgi6")
        vergibildiirmitutar6 = request.POST.get("vergibildiirmitutar6")
        vergibildiirmibilgi7 = request.POST.get("vergibildiirmibilgi7")
        vergibildiirmitutar7 = request.POST.get("vergibildiirmitutar7")
        vergibildiirmibilgi8 = request.POST.get("vergibildiirmibilgi8")
        vergibildiirmitutar8 = request.POST.get("vergibildiirmitutar8")
        #VERGİ BİLDİRİMİ
        vergibildirimi1 = request.POST.get("vergibildirimi1")
        vergibildirimitutar1 = request.POST.get("vergibildirimitutar1")
        vergibildirimi2 = request.POST.get("vergibildirimi2")
        vergibildirimitutar2 = request.POST.get("vergibildirimitutar2")
        vergibildirimi3 = request.POST.get("vergibildirimi3")
        vergibildirimitutar3 = request.POST.get("vergibildirimitutar3")
        #VERGİ BİLDİRİMİ
        #MAHSUP EDİLECEK VERGİLER
        mahsupedilecekbilgi1 = request.POST.get("mahsupedilecekbilgi1")
        mahsupedilecektutar1 = request.POST.get("mahsupedilecektutar1")
        mahsupedilecekbilgi2 = request.POST.get("mahsupedilecekbilgi2")
        mahsupedilecektutar2 = request.POST.get("mahsupedilecektutar2")
        mahsupedilecekbilgi3 = request.POST.get("mahsupedilecekbilgi3")
        mahsupedilecektutar3 = request.POST.get("mahsupedilecektutar3")
        mahsupedilecekbilgi4 = request.POST.get("mahsupedilecekbilgi4")
        mahsupedilecektutar4 = request.POST.get("mahsupedilecektutar4")
        #MAHSUP EDİLECEK VERGİLER

        #
        mahsupedilecekergitoplamibilgi = request.POST.get("mahsupedilecekergitoplamibilgi")
        mahsupedilecekergitoplamitutar = request.POST.get("mahsupedilecekergitoplamitutar")
        mahsupedilmeyecekyabancibilgi = request.POST.get("mahsupedilmeyecekyabancibilgi")
        mahsupedilmeyecekyabancitutar = request.POST.get("mahsupedilmeyecekyabancitutar")
        odenemesigerekenkurumlarvergisi = request.POST.get("odenemesigerekenkurumlarvergisi")
        odenemesigerekenkurumlarvergisitutar = request.POST.get("odenemesigerekenkurumlarvergisitutar")
        tesciledilmeyenkurumlarvergisi = request.POST.get("tesciledilmeyenkurumlarvergisi")
        tesciledilmeyenkurumlarvergisitutar = request.POST.get("tesciledilmeyenkurumlarvergisitutar")
        islemlerdensonraodemesigerekenvergi = request.POST.get("islemlerdensonraodemesigerekenvergi")
        islemlerdensonraodemesigerekenvergitutar = request.POST.get("islemlerdensonraodemesigerekenvergitutar")
        iadesigerekengecivergi = request.POST.get("iadesigerekengecivergi")
        iadesigerekengecivergitutar = request.POST.get("iadesigerekengecivergitutar")
        iadesigerekenkruumlarvergisi = request.POST.get("iadesigerekenkruumlarvergisi")
        iadesigerekenkruumlarvergisitutar = request.POST.get("iadesigerekenkruumlarvergisitutar")
        iadesigerekengecicivergi = request.POST.get("iadesigerekengecicivergi")
        iadesigerekengecicivergitutat = request.POST.get("iadesigerekengecicivergitutat")
        kalanvergiindirimi = request.POST.get("kalanvergiindirimi")
        kalanvergiindirimitutar = request.POST.get("kalanvergiindirimitutar")
        damgavergisi = request.POST.get("damgavergisi")
        damgavergisitutar = request.POST.get("damgavergisitutar")
        kazancintespityontemi = request.POST.get("kazancintespityontemi")
        kazancintespityontemisecimi = request.POST.get("kazancintespityontemisecimi")
        #
        kesintiyapanadisoyadibilgdsi = request.POST.getlist("kesintiyapanadisoyadibilgdsi")
        kesintiyaapantcvergikimlikno = request.POST.getlist("kesintiyaapantcvergikimlikno")
        kesintiyaapantcvergino = request.POST.getlist("kesintiyaapantcvergino")
        kesintiyaapanfonem = request.POST.getlist("kesintiyaapanfonem")
        kesintiburuttutar = request.POST.getlist("kesintiburuttutar")
        kesintitutar = request.POST.getlist("kesintitutar")
        #
        kardagitimbilgi2 = request.POST.get("kardagitimbilgi2")
        kardagitimoncekidonem2 = request.POST.get("kardagitimoncekidonem2")
        kardagitimcari2 = request.POST.get("kardagitimcari2")
        kardagitimbilgi3 = request.POST.get("kardagitimbilgi3")
        kardagitimoncekidonem3 = request.POST.get("kardagitimoncekidonem3")
        kardagitimcari3 = request.POST.get("kardagitimcari3")
        kardagitimbilgi4 = request.POST.get("kardagitimbilgi4")
        kardagitimoncekidonem4 = request.POST.get("kardagitimoncekidonem4")
        kardagitimcari4 = request.POST.get("kardagitimcari4")
        kardagitimbilgi5 = request.POST.get("kardagitimbilgi5")
        kardagitimoncekidonem5 = request.POST.get("kardagitimoncekidonem5")
        kardagitimcari5 = request.POST.get("kardagitimcari5")
        kardagitimbilgi6 = request.POST.get("kardagitimbilgi6")
        kardagitimoncekidonem6 = request.POST.get("kardagitimoncekidonem6")
        kardagitimcari6 = request.POST.get("kardagitimcari6")
        kardagitimbilgi7 = request.POST.get("kardagitimbilgi7")
        kardagitimoncekidonem7 = request.POST.get("kardagitimoncekidonem7")
        kardagitimcari7 = request.POST.get("kardagitimcari7")   
        kardagitimbilgi8 = request.POST.get("kardagitimbilgi8")
        kardagitimoncekidonem8 = request.POST.get("kardagitimoncekidonem8")
        kardagitimcari8 = request.POST.get("kardagitimcari8")
        kardagitimbilgi9 = request.POST.get("kardagitimbilgi9")
        kardagitimoncekidonem9 = request.POST.get("kardagitimoncekidonem9")
        kardagitimcari9 = request.POST.get("kardagitimcari9")  
        kardagitimbilgi10 = request.POST.get("kardagitimbilgi10")
        kardagitimoncekidonem10 = request.POST.get("kardagitimoncekidonem10")
        kardagitimcari10 = request.POST.get("kardagitimcari10")
        kardagitimbilgi11 = request.POST.get("kardagitimbilgi11")
        kardagitimoncekidonem11 = request.POST.get("kardagitimoncekidonem11")
        kardagitimcari11 = request.POST.get("kardagitimcari11")
        kardagitimbilgi12 = request.POST.get("kardagitimbilgi12")
        kardagitimoncekidonem12 = request.POST.get("kardagitimoncekidonem12")
        kardagitimcari12 = request.POST.get("kardagitimcari12")
        kardagitimbilgi13 = request.POST.get("kardagitimbilgi13")
        kardagitimoncekidonem13 = request.POST.get("kardagitimoncekidonem13")
        kardagitimcari13 = request.POST.get("kardagitimcari13")
        kardagitimbilgi14 = request.POST.get("kardagitimbilgi14")
        kardagitimoncekidonem14 = request.POST.get("kardagitimoncekidonem14")
        kardagitimcari14 = request.POST.get("kardagitimcari14")
        kardagitimbilgi15 = request.POST.get("kardagitimbilgi15")
        kardagitimoncekidonem15 = request.POST.get("kardagitimoncekidonem15")
        kardagitimcari15 = request.POST.get("kardagitimcari15")
        kardagitimbilgi16 = request.POST.get("kardagitimbilgi16")
        kardagitimoncekidonem16 = request.POST.get("kardagitimoncekidonem16")
        kardagitimcari16 = request.POST.get("kardagitimcari16")
        kardagitimbilgi17 = request.POST.get("kardagitimbilgi17")
        kardagitimoncekidonem17 = request.POST.get("kardagitimoncekidonem17")
        kardagitimcari17 = request.POST.get("kardagitimcari17")   
        kardagitimbilgi18 = request.POST.get("kardagitimbilgi18")
        kardagitimoncekidonem18 = request.POST.get("kardagitimoncekidonem18")
        kardagitimcari18 = request.POST.get("kardagitimcari18")
        kardagitimbilgi19 = request.POST.get("kardagitimbilgi19")
        kardagitimoncekidonem19 = request.POST.get("kardagitimoncekidonem19")
        kardagitimcari19 = request.POST.get("kardagitimcari19")
        kardagitimbilgi20 = request.POST.get("kardagitimbilgi20")
        kardagitimoncekidonem20 = request.POST.get("kardagitimoncekidonem20")
        kardagitimcari20 = request.POST.get("kardagitimcari20")
        kardagitimbilgi21 = request.POST.get("kardagitimbilgi21")
        kardagitimoncekidonem21 = request.POST.get("kardagitimoncekidonem21")
        kardagitimcari21 = request.POST.get("kardagitimcari21")
        kardagitimbilgi22 = request.POST.get("kardagitimbilgi22")
        kardagitimoncekidonem22 = request.POST.get("kardagitimoncekidonem22")
        kardagitimcari22 = request.POST.get("kardagitimcari22")
        kardagitimbilgi23 = request.POST.get("kardagitimbilgi23")
        kardagitimoncekidonem23 = request.POST.get("kardagitimoncekidonem23")
        kardagitimcari23 = request.POST.get("kardagitimcari23")
        kardagitimbilgi24 = request.POST.get("kardagitimbilgi24")
        kardagitimoncekidonem24 = request.POST.get("kardagitimoncekidonem24")
        kardagitimcari24 = request.POST.get("kardagitimcari24")
        kardagitimbilgi25 = request.POST.get("kardagitimbilgi25")
        kardagitimoncekidonem25 = request.POST.get("kardagitimoncekidonem25")
        kardagitimcari25 = request.POST.get("kardagitimcari25")
        kardagitimbilgi26 = request.POST.get("kardagitimbilgi26")
        kardagitimoncekidonem26 = request.POST.get("kardagitimoncekidonem26")
        kardagitimcari26 = request.POST.get("kardagitimcari26")
        kardagitimbilgi27 = request.POST.get("kardagitimbilgi27")
        kardagitimoncekidonem27 = request.POST.get("kardagitimoncekidonem27")
        kardagitimcari27 = request.POST.get("kardagitimcari27")   
        kardagitimbilgi28 = request.POST.get("kardagitimbilgi28")
        kardagitimoncekidonem28 = request.POST.get("kardagitimoncekidonem28")
        kardagitimcari28 = request.POST.get("kardagitimcari28")
        kardagitimbilgi29 = request.POST.get("kardagitimbilgi29")
        kardagitimoncekidonem29 = request.POST.get("kardagitimoncekidonem29")
        kardagitimcari29 = request.POST.get("kardagitimcari29")
        kardagitimbilgi30 = request.POST.get("kardagitimbilgi30")
        kardagitimoncekidonem30 = request.POST.get("kardagitimoncekidonem30")
        kardagitimcari30 = request.POST.get("kardagitimcari30")
        kardagitimbilgi31 = request.POST.get("kardagitimbilgi31")
        kardagitimoncekidonem31 = request.POST.get("kardagitimoncekidonem31")
        kardagitimcari31 = request.POST.get("kardagitimcari31")
        kardagitimbilgi32 = request.POST.get("kardagitimbilgi32")
        kardagitimoncekidonem32 = request.POST.get("kardagitimoncekidonem32")
        kardagitimcari32 = request.POST.get("kardagitimcari32")
        kardagitimbilgi33 = request.POST.get("kardagitimbilgi33")
        kardagitimoncekidonem33 = request.POST.get("kardagitimoncekidonem33")
        kardagitimcari33 = request.POST.get("kardagitimcari33")
        kardagitimbilgi34 = request.POST.get("kardagitimbilgi34")
        kardagitimoncekidonem34 = request.POST.get("kardagitimoncekidonem34")
        kardagitimcari34 = request.POST.get("kardagitimcari34")
        kardagitimbilgi35 = request.POST.get("kardagitimbilgi35")
        kardagitimoncekidonem35 = request.POST.get("kardagitimoncekidonem35")
        kardagitimcari35 = request.POST.get("kardagitimcari35")
        kardagitimbilgi36 = request.POST.get("kardagitimbilgi36")
        kardagitimoncekidonem36 = request.POST.get("kardagitimoncekidonem36")
        kardagitimcari36 = request.POST.get("kardagitimcari36")
        kardagitimbilgi37 = request.POST.get("kardagitimbilgi37")
        kardagitimoncekidonem37 = request.POST.get("kardagitimoncekidonem37")
        kardagitimcari37 = request.POST.get("kardagitimcari37")   
        kardagitimbilgi38 = request.POST.get("kardagitimbilgi38")
        kardagitimoncekidonem38 = request.POST.get("kardagitimoncekidonem38")
        kardagitimcari38 = request.POST.get("kardagitimcari38")
        kardagitimbilgi39 = request.POST.get("kardagitimbilgi39")
        kardagitimoncekidonem39 = request.POST.get("kardagitimoncekidonem39")
        kardagitimcari39 = request.POST.get("kardagitimcari39")
        kardagitimbilgi40 = request.POST.get("kardagitimbilgi40")
        kardagitimoncekidonem40 = request.POST.get("kardagitimoncekidonem40")
        kardagitimcari40 = request.POST.get("kardagitimcari40")
        kardagitimbilgi41 = request.POST.get("kardagitimbilgi41")
        kardagitimoncekidonem41 = request.POST.get("kardagitimoncekidonem41")
        kardagitimcari41 = request.POST.get("kardagitimcari41")
        kardagitimbilgi42 = request.POST.get("kardagitimbilgi42")
        kardagitimoncekidonem42 = request.POST.get("kardagitimoncekidonem42")
        kardagitimcari42 = request.POST.get("kardagitimcari42")
        kardagitimbilgi43 = request.POST.get("kardagitimbilgi43")
        kardagitimoncekidonem43 = request.POST.get("kardagitimoncekidonem43")
        kardagitimcari43 = request.POST.get("kardagitimcari43")
        kardagitimbilgi44 = request.POST.get("kardagitimbilgi44")
        kardagitimoncekidonem44 = request.POST.get("kardagitimoncekidonem44")
        kardagitimcari44 = request.POST.get("kardagitimcari44")
        kardagitimbilgi45 = request.POST.get("kardagitimbilgi45")
        kardagitimoncekidonem45 = request.POST.get("kardagitimoncekidonem45")
        kardagitimcari45 = request.POST.get("kardagitimcari45")
        kardagitimbilgi46 = request.POST.get("kardagitimbilgi46")
        kardagitimoncekidonem46 = request.POST.get("kardagitimoncekidonem46")
        kardagitimcari46 = request.POST.get("kardagitimcari46")
        kardagitimbilgi47 = request.POST.get("kardagitimbilgi47")
        kardagitimoncekidonem47 = request.POST.get("kardagitimoncekidonem47")
        kardagitimcari47 = request.POST.get("kardagitimcari47")   
        kardagitimbilgi48 = request.POST.get("kardagitimbilgi48")
        kardagitimoncekidonem48 = request.POST.get("kardagitimoncekidonem48")
        kardagitimcari48 = request.POST.get("kardagitimcari48")
        kardagitimbilgi49 = request.POST.get("kardagitimbilgi49")
        kardagitimoncekidonem49 = request.POST.get("kardagitimoncekidonem49")
        kardagitimcari49 = request.POST.get("kardagitimcari49")
        kardagitimbilgi50 = request.POST.get("kardagitimbilgi50")
        kardagitimoncekidonem50 = request.POST.get("kardagitimoncekidonem50")
        kardagitimcari50 = request.POST.get("kardagitimcari50")
        kardagitimbilgi51 = request.POST.get("kardagitimbilgi51")
        kardagitimoncekidonem51 = request.POST.get("kardagitimoncekidonem51")
        kardagitimcari51 = request.POST.get("kardagitimcari51")
        kardagitimbilgi52 = request.POST.get("kardagitimbilgi52")
        kardagitimoncekidonem52 = request.POST.get("kardagitimoncekidonem52")
        kardagitimcari52 = request.POST.get("kardagitimcari52")
        #
        mudurgenelmudur = request.POST.getlist("mudurgenelmudur")
        yonetimkuruluuyesi = request.POST.getlist("yonetimkuruluuyesi")
        ortakbilgisi = request.POST.getlist("ortakbilgisi")
        kanunitemsilcimi = request.POST.getlist("kanunitemsilcimi")
        yurticiyurtdisi = request.POST.getlist("yurticiyurtdisi")
        ortakvergikimliknosu = request.POST.getlist("ortakvergikimliknosu")
        ortakadisoyadiunvani = request.POST.getlist("ortakadisoyadiunvani")
        ortakikametgahadresi = request.POST.getlist("ortakikametgahadresi")
        ortaktckimliknosu = request.POST.getlist("ortaktckimliknosu")
        ortaktelefonnumarasi = request.POST.getlist("ortaktelefonnumarasi")
        ortakhisseorani = request.POST.getlist("ortakhisseorani")
        #
    return render(request,"beyannameler/kurumlar_vergisi_beyanname.html",content)
#
#ba bs formları

def baformu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        verginumarasitc = request.POST.get("verginumarasitc")
        verginumarasi = request.POST.get("verginumarasi")
        soyadiunvan = request.POST.get("soyadiunvan")
        adiunvan = request.POST.get("adiunvan")
        vergidairesi = request.POST.get("vergidairesi")
        ticaretsicilno = request.POST.get("ticaretsicilno")
        eposta = request.POST.get("eposta")
        telefon = request.POST.get("telefon")
        #DÖNEM İÇİNDE KENDİSİNDEN MAL VE HİZMET ALINAN MÜKELLİFLER İLİŞKİN BİLDİRİMLER
        siranumarasi = request.POST.getlist("siranumarasi")
        adisoyadiunvanbilgsi = request.POST.getlist("adisoyadiunvanbilgsi")
        ulkekodu = request.POST.getlist("ulkekodu")
        vergikimliknumarali = request.POST.getlist("vergikimliknumarali")
        belgesayisi = request.POST.getlist("belgesayisi")
        malvehizmetbedeli = request.POST.getlist("malvehizmetbedeli")

        #DÖNEM İÇİNDE KENDİSİNDEN MAL VE HİZMET ALINAN MÜKELLİFLER İLİŞKİN BİLDİRİMLER
        muhasebeci = request.POST.get("muhasebeci")
        muhasebecininvergikimliknosu = request.POST.get("muhasebecininvergikimliknosu")
        muhasebecinintckimliknosu = request.POST.get("muhasebecinintckimliknosu")
        muhasebecininsoyadiunvan = request.POST.get("muhasebecininsoyadiunvan")
        muhasebecininadi =request.POST.get("muhasebecininadi")

    return render(request,"beyannameler/baformu.html",content)

def bsformu(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        verginumarasitc = request.POST.get("verginumarasitc")
        verginumarasi = request.POST.get("verginumarasi")
        soyadiunvan = request.POST.get("soyadiunvan")
        adiunvan = request.POST.get("adiunvan")
        vergidairesi = request.POST.get("vergidairesi")
        ticaretsicilno = request.POST.get("ticaretsicilno")
        eposta = request.POST.get("eposta")
        telefon = request.POST.get("telefon")
        #DÖNEM İÇİNDE KENDİSİNDEN MAL VE HİZMET ALINAN MÜKELLİFLER İLİŞKİN BİLDİRİMLER
        siranumarasi = request.POST.getlist("siranumarasi")
        adisoyadiunvanbilgsi = request.POST.getlist("adisoyadiunvanbilgsi")
        ulkekodu = request.POST.getlist("ulkekodu")
        vergikimliknumarali = request.POST.getlist("vergikimliknumarali")
        belgesayisi = request.POST.getlist("belgesayisi")
        malvehizmetbedeli = request.POST.getlist("malvehizmetbedeli")

        #DÖNEM İÇİNDE KENDİSİNDEN MAL VE HİZMET ALINAN MÜKELLİFLER İLİŞKİN BİLDİRİMLER
        muhasebeci = request.POST.get("muhasebeci")
        muhasebecininvergikimliknosu = request.POST.get("muhasebecininvergikimliknosu")
        muhasebecinintckimliknosu = request.POST.get("muhasebecinintckimliknosu")
        muhasebecininsoyadiunvan = request.POST.get("muhasebecininsoyadiunvan")
        muhasebecininadi =request.POST.get("muhasebecininadi")

    return render(request,"beyannameler/bsformu.html",content)

#damga vergisi
def damgavergisi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    if request.POST:
        aysecimi = request.POST.get("aysecimi")
        siranosu = request.POST.getlist("siranosu")
        duzenlemetarihi = request.POST.getlist("duzenlemetarihi")
        no = request.POST.getlist("no")
        turu = request.POST.getlist("turu")
        aciklama = request.POST.getlist("aciklama")
        iecerdigibedel = request.POST.getlist("iecerdigibedel")
        damgavergisi = request.POST.getlist("damgavergisi")
        toplam = request.POST.get("toplam")
        toplam2 = request.POST.get("toplam2")
    return render(request,"beyannameler/damgavergisi.html",content)

#Kurumlar Geri KAzanım PAyı vergisi
def kurumlargerikazanimpayi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    turkey_cities = ["000 - Yurtdışı",
    "001 - Adana", "002 - Adıyaman", "003 - Afyonkarahisar", "004 - Ağrı", "005 - Amasya", "006 - Ankara", "007 - Antalya", "008 - Artvin", "009 - Aydın", "010 - Balıkesir",
    "011 - Bilecik", "012 - Bingöl", "013 - Bitlis", "014 - Bolu", "015 - Burdur", "016 - Bursa", "017 - Çanakkale", "018 - Çankırı", "019 - Çorum", "020 - Denizli", "021 - Diyarbakır",
    "022 - Edirne", "023 - Elazığ", "024 - Erzincan", "025 - Erzurum", "026 - Eskişehir", "027 - Gaziantep", "028 - Giresun", "029 - Gümüşhane", "030 - Hakkari", "031 - Hatay",
    "032 - Isparta", "033 - Mersin", "034 - İstanbul", "035 - İzmir", "036 - Kars", "037 - Kastamonu", "038 - Kayseri", "039 - Kırklareli", "040 - Kırşehir", "041 - Kocaeli",
    "042 - Konya", "043 - Kütahya", "044 - Malatya", "045 - Manisa", "046 - Kahramanmaraş", "047 - Mardin", "048 - Muğla", "049 - Muş", "050 - Nevşehir", "051 - Niğde", "052 - Ordu",
    "053 - Rize", "054 - Sakarya", "055 - Samsun", "056 - Siirt", "057 - Sinop", "058 - Sivas", "059 - Tekirdağ", "060 - Tokat", "061 - Trabzon", "062 - Tunceli", "063 - Şanlıurfa",
    "064 - Uşak", "065 - Van", "066 - Yozgat", "067 - Zonguldak", "068 - Aksaray", "069 - Bayburt", "070 - Karaman", "071 - Kırıkkale", "072 - Batman", "073 - Şırnak", "074 - Bartın",
    "075 - Ardahan", "076 - Iğdır", "077 - Yalova", "078 - Karabük", "079 - Kilis", "080 - Osmaniye", "081 - Düzce"
    ]
    content["sehirler"]  = turkey_cities
    content["urunler"] = urunler.objects.all()
    content["dayanak"] = dayanak.objects.all()
    if request.POST:
        aysecimi = request.POST.get("aysecimi")
        yurticidisi = request.POST.getlist("yurticidisi")
        ilbilgisi = request.POST.getlist("ilbilgisi")
        tcveyavergikimlikno = request.POST.getlist("tcveyavergikimlikno")
        adsoyadunvan = request.POST.getlist("adsoyadunvan")
        aybilgisi = request.POST.getlist("aybilgisi")
        sattigiadet = request.POST.getlist("sattigiadet")
        gerikazandigitutar = request.POST.getlist("gerikazandigitutar")
        #YURT İÇİNDE ÜRETİLEREK PİYASAYA ARZ EDİLEN ÜRÜNLERE İLİŞKİN GEKAP BİLDİRİM SATIRLARI
        urunlerlistesi = request.POST.getlist("urunlerlistesi")
        depozitoonaykodu = request.POST.getlist("depozitoonaykodu")
        birimtutari = request.POST.getlist("birimtutari")
        miktar = request.POST.getlist("miktar")
        tutarislemi = request.POST.getlist("tutarislemi")
        #YURT İÇİNDE ÜRETİLEREK PİYASAYA ARZ EDİLEN ÜRÜNLERE İLİŞKİN GEKAP BİLDİRİM SATIRLARI
        #İTHAL EDİLEREK YURT İÇİNDE PİYASAYA ARZ EDİLEN ÜRÜNLERE İLİŞKİN GEKAP BİLDİRİM SATIRLARI
        urunlerlistesi1 = request.POST.getlist("urunlerlistesi1")
        depozitoonaykodu1 = request.POST.getlist("depozitoonaykodu1")
        birimtutari1 = request.POST.getlist("birimtutari1")
        miktar1 = request.POST.getlist("miktar1")
        tutarislemi1 = request.POST.getlist("tutarislemi1")
        #İTHAL EDİLEREK YURT İÇİNDE PİYASAYA ARZ EDİLEN ÜRÜNLERE İLİŞKİN GEKAP BİLDİRİM SATIRLARI
        #ÖNCEKİ DÖNEM DEPOZİTO KAYNAKLI OLUŞAN GEKAP BİLDİRİM SATIRLARI
        urunlerlistesi2 = request.POST.getlist("urunlerlistesi2")
        depozitoonaykodu2 = request.POST.getlist("depozitoonaykodu2")
        birimtutari2 = request.POST.getlist("birimtutari2")
        miktar2 = request.POST.getlist("miktar2")
        tutarislemi2 = request.POST.getlist("tutarislemi2")
        #ÖNCEKİ DÖNEM DEPOZİTO KAYNAKLI OLUŞAN GEKAP BİLDİRİM SATIRLARI
        #MAHSUP EDİLECEK GEKAP (PLASTİK POŞET HARİÇ)
        oncekidonemmahsupdevreden = request.POST.get("oncekidonemmahsupdevreden")
        budoenemaitmahsup = request.POST.get("budoenemaitmahsup")
        #MAHSUP EDİLECEK GEKAP (PLASTİK POŞET HARİÇ)
        #GEKAP TAHSİL EDİLMEYECEK ÜRÜNLER
        dayanak1 =  request.POST.getlist("dayanak")
        urunlerlistesi3 = request.POST.getlist("urunlerlistesi3")
        birimtutari3 = request.POST.getlist("birimtutari3")
        miktar3 = request.POST.getlist("miktar3")
        tutarislemi3 = request.POST.getlist("tutarislemi3")
        #GEKAP TAHSİL EDİLMEYECEK ÜRÜNLER
    return render(request,"beyannameler/kurumlargerikazanimpayi.html",content)

#turizim Beyannamesi
def turizm(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        #Turizm Payına Tabi Faliyetler
        istege_baglitevkat = request.POST.getlist("istege_baglitevkat")
        istegebaglimatrah = request.POST.getlist("istegebaglimatrah")
        istebaglikdv = request.POST.getlist("istebaglikdv")
        istebaglivergihesaplanan = request.POST.getlist("istebaglivergihesaplanan")
        #Turizm Payına Tabi Faliyetler
        #İndirimli Turizm Payına Tabi Faliyetler
        istege_baglitevkat = request.POST.getlist("istege_baglitevkat")
        istegebaglimatrah = request.POST.getlist("istegebaglimatrah")
        istebaglikdv = request.POST.getlist("istebaglikdv")
        istebaglivergihesaplanan = request.POST.getlist("istebaglivergihesaplanan")
        #İndirimli Turizm Payına Tabi Faliyetler
        #İndirimli İşletme Bilgisi
        islemturutamtevkifat =request.POST.getlist("islemturutamtevkifat")
        dolasimagirenbeyannamesayisi = request.POST.getlist("dolasimagirenbeyannamesayisi")
        tesisadi = request.POST.getlist("tesisadi")
        tamtevkifattarihi = request.POST.getlist("tamtevkifattarihi")
        belgesayisi = request.POST.getlist("belgesayisi")
        #İndirimli İşletme Bilgisi
    return render(request,"beyannameler/turizm.html",content)

#ebeyanname
def e_beyanname(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        #
        kdv1aylik = request.POST.get("kdv1aylik")
        kdv1ucaylik = request.POST.get("kdv1ucaylik")
        kdv2aylik = request.POST.get("kdv2aylik")
        kdv2ucaylik = request.POST.get("kdv2ucaylik")
        kdv4aylik = request.POST.get("kdv4aylik")
        muhtasaraylik = request.POST.get("muhtasaraylik")
        muhtasarucaylik = request.POST.get("muhtasarucaylik")
        gecicivergibeyannamesi = request.POST.get("gecicivergibeyannamesi")
        babsformu = request.POST.get("babsformu")
        damgavergisi = request.POST.get("damgavergisi")
        posetbeyannamesiaylik = request.POST.get("posetbeyannamesiaylik")
        posetbeyannamesiucaylik = request.POST.get("posetbeyannamesiucaylik")
        posetbeyannamesialtiaylik = request.POST.get("posetbeyannamesialtiaylik")
        turzimaylik = request.POST.get("turzimaylik")
        turzimucaylik = request.POST.get("turzimucaylik")
        vergidonemitarihi = request.POST.get("vergidonemitarihi")
        kdv1 = request.POST.getlist("kdv1")
        kdv2 = request.POST.getlist("kdv2")
        muhtasarsgk = request.POST.getlist("muhtasarsgk")
        gecici = request.POST.getlist("gecici")
        ba = request.POST.getlist("ba")
        bs = request.POST.getlist("bs")
        gelir = request.POST.getlist("gelir")
        kurumlar = request.POST.getlist("kurumlar")
        kdv4 = request.POST.getlist("kdv4")
        poset = request.POST.getlist("poset")
        damga = request.POST.getlist("damga")
        turizm = request.POST.getlist("turizm")
        muhsgk2 = request.POST.getlist("muhsgk2")
    return render(request,"beyannameler/ebeyanname.html",content)

#turizim Beyannamesi
def muhsgksayfasi(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["vergidairesi"] = vergi_dairesi.objects.all()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        #MATRAH VE VERGİ BİLDİRİMİ
        odemeturu2 = request.POST.get("odemeturu2")
        odemetutari2 = request.POST.get("odemetutari2")
        odemetutarikesinti2 = request.POST.get("odemetutarikesinti2")
        odemeturu3 = request.POST.get("odemeturu3")
        odemetutari3 = request.POST.get("odemetutari3")
        odemetutarikesinti3 = request.POST.get("odemetutarikesinti3")
        odemeturu4 = request.POST.get("odemeturu4")
        odemetutari4 = request.POST.get("odemetutari4")
        odemetutarikesinti4 = request.POST.get("odemetutarikesinti4")
        odemeturu5 = request.POST.get("odemeturu5")
        odemetutari5 = request.POST.get("odemetutari5")
        odemetutarikesinti5 = request.POST.get("odemetutarikesinti5")
        odemeturu6 = request.POST.get("odemeturu6")
        odemetutari6 = request.POST.get("odemetutari6")
        odemetutarikesinti6 = request.POST.get("odemetutarikesinti6")
        odemeturu7 = request.POST.get("odemeturu7")
        odemetutari7 = request.POST.get("odemetutari7")
        odemetutarikesinti7 = request.POST.get("odemetutarikesinti7")
        odemeturu8 = request.POST.get("odemeturu8")
        odemetutari8 = request.POST.get("odemetutari8")
        odemetutarikesinti8 = request.POST.get("odemetutarikesinti8")
        odemeturu9 = request.POST.get("odemeturu9")
        odemetutari9 = request.POST.get("odemetutari9")
        odemetutarikesinti9 = request.POST.get("odemetutarikesinti9")
        odemeturu10 = request.POST.get("odemeturu10")
        odemetutari10 = request.POST.get("odemetutari10")
        odemetutarikesinti10 = request.POST.get("odemetutarikesinti10")
        odemeturu11 = request.POST.get("odemeturu11")
        odemetutari11 = request.POST.get("odemetutari11")
        odemetutarikesinti11 = request.POST.get("odemetutarikesinti11")
        odemeturu12 = request.POST.get("odemeturu12")
        odemetutari12 = request.POST.get("odemetutari12")
        odemetutarikesinti12 = request.POST.get("odemetutarikesinti12")
        odemeturu13 = request.POST.get("odemeturu13")
        odemetutari13 = request.POST.get("odemetutari13")
        odemetutarikesinti13 = request.POST.get("odemetutarikesinti13")
        odemeturu14 = request.POST.get("odemeturu14")
        odemetutari14 = request.POST.get("odemetutari14")
        odemetutarikesinti14 = request.POST.get("odemetutarikesinti14")
        odemeturu15 = request.POST.get("odemeturu15")
        odemetutari15 = request.POST.get("odemetutari15")
        odemetutarikesinti15 = request.POST.get("odemetutarikesinti15")
        odemeturu16 = request.POST.get("odemeturu16")
        odemetutari16 = request.POST.get("odemetutari16")
        odemetutarikesinti16 = request.POST.get("odemetutarikesinti16")
        odemetutaritoplam = request.POST.get("odemetutaritoplam")
        odemetutarikesintitoplami = request.POST.get("odemetutarikesintitoplami")
        odemetutarikesinti5225kanunu = request.POST.get("odemetutarikesinti5225kanunu")
        odemetutarikesinti5746kanunu = request.POST.get("odemetutarikesinti5746kanunu")
        odemetutarikesinti4691kanunu = request.POST.get("odemetutarikesinti4691kanunu")
        odemetutarikesinti17b18kanunu = request.POST.get("odemetutarikesinti17b18kanunu")
        #MATRAH VE VERGİ BİLDİRİMİ
        #MAHSUP EDİLEN VERGİLER
        mahsupedilenvergi2  =request.POST.get("mahsupedilenvergi2")
        mahsupedilenvergi3  =request.POST.get("mahsupedilenvergi3")
        mahsupedilenvergi4  =request.POST.get("mahsupedilenvergi4")
        mahsupedilenvergi5  =request.POST.get("mahsupedilenvergi5")
        mahsupedilenvergi6  =request.POST.get("mahsupedilenvergi6")
        mahsupedilenvergi7  =request.POST.get("mahsupedilenvergi7")
        mahsupedilenvergi8  =request.POST.get("mahsupedilenvergi8")
        #MAHSUP EDİLEN VERGİLER
        #ÇALIŞAN BİLGİLERİ
        bilgiver1 = request.POST.get("bilgiver1")
        digerucretilicalisansayisi = request.POST.get("digerucretilicalisansayisi")
        digerucretiligelivmuaf = request.POST.get("digerucretiligelivmuaf")
        digerucretilisgkvmuaf = request.POST.get("digerucretilisgkvmuaf")
        digerucretilismatrahtoplami = request.POST.get("digerucretilismatrahtoplami")
        digerucretilisasgaritoplami = request.POST.get("digerucretilisasgaritoplami")
        digerucretilisgelirvergisikesintitoplami = request.POST.get("digerucretilisgelirvergisikesintitoplami")
        digerucretilisasgariistisnatoplami = request.POST.get("digerucretilisasgariistisnatoplami")
        digerucretilisdamgavergisitoplami = request.POST.get("digerucretilisdamgavergisitoplami")
        bilgiver2 = request.POST.get("bilgiver2")
        asgariucretilicalisansayisi = request.POST.get("asgariucretilicalisansayisi")
        asgariucretiligelivmuaf = request.POST.get("asgariucretiligelivmuaf")
        asgariucretilisgkvmuaf = request.POST.get("asgariucretilisgkvmuaf")
        asgariucretilismatrahtoplami = request.POST.get("asgariucretilismatrahtoplami")
        asgariucretilisasgaritoplami = request.POST.get("asgariucretilisasgaritoplami")
        asgariucretilisgelirvergisikesintitoplami = request.POST.get("asgariucretilisgelirvergisikesintitoplami")
        asgariucretilisasgariistisnatoplami = request.POST.get("asgariucretilisasgariistisnatoplami")
        asgariucretilisdamgavergisitoplami = request.POST.get("asgariucretilisdamgavergisitoplami")
        #ÇALIŞAN BİLGİLERİ
        #TAHAKKUKA ESAS İCMAL CETVELİ
        icmalcetveli2 = request.POST.get("icmalcetveli2")
        icmalcetveli3 = request.POST.get("icmalcetveli3")
        icmalcetveli4 = request.POST.get("icmalcetveli4")
        icmalcetveli5 = request.POST.get("icmalcetveli5")
        icmalcetveli6 = request.POST.get("icmalcetveli6")
        icmalcetveli7 = request.POST.get("icmalcetveli7")
        icmalcetveli8 = request.POST.get("icmalcetveli8")
        #TAHAKKUKA ESAS İCMAL CETVELİ
        #İŞYERİ BİLGİLERİ
        isyerituru  = request.POST.get("isyerituru")
        isyerikodu = request.POST.get("isyerikodu")
        isyeriticaretsicilno = request.POST.get("isyeriticaretsicilno")
        ticaretsicilmudurlugu = request.POST.get("ticaretsicilmudurlugu")
        faliyetnacekodu = request.POST.get("faliyetnacekodu")
        isyeriadi = request.POST.get("isyeriadi")
        isyeriadresno = request.POST.get("isyeriadresno")
        isyerimulkiyetdurumu = request.POST.get("isyerimulkiyetdurumu")
        #İŞYERİ BİLGİLERİ
        #Yeraltı ve Yerüstü Maden İşletmeleri Bildirimi
        Madenbigisi = request.POST.get("Madenbigisi")
        sehirlerilceler = request.POST.get("sehirlerilceler")
        madencinsi = request.POST.get("madencinsi")
        madeniscisaysi = request.POST.getU("madeniscisaysi")
        madensgkisyerisicilnumarasi = request.POST.get("madensgkisyerisicilnumarasi")
        madenruhsatbaslamatarihi = request.POST.get("madenruhsatbaslamatarihi")
        madenruhsatbitistarihi = request.POST.get("madenruhsatbitistarihi")
        madenisyeriadresi = request.POST.get("madenisyeriadresi")
        #Yeraltı ve Yerüstü Maden İşletmeleri Bildirimi
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (4691)
        maddekapsamindabildirimilsecimi = request.POST.get("maddekapsamindabildirimilsecimi")
        maddekapsamindavergidairesi = request.POST.get("maddekapsamindavergidairesi")
        maddekapsamindacalisansayisi = request.POST.get("maddekapsamindacalisansayisi")
        maddekapsamindaunitekodu = request.POST.get("maddekapsamindaunitekodu")
        maddekapsamindaeskiunitekodu = request.POST.get("maddekapsamindaeskiunitekodu")
        maddekapsamindailkodu = request.POST.get("maddekapsamindailkodu")
        maddekapsamindaisyerisiranosu = request.POST.get("maddekapsamindaisyerisiranosu")
        maddekapsamindaaltisnumarasi = request.POST.get("maddekapsamindaaltisnumarasi")
        maddekapsamindaisyerininadresi=request.POST.get("maddekapsamindaisyerininadresi")
        maddekapsamindaprojekodu = request.POST.get("maddekapsamindaprojekodu")
        maddekapsamindaisyeribulundugubolge = request.POST.get("maddekapsamindaisyeribulundugubolge")
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (4691)
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (4691)
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (4691)

        #Bildirim Kapsamında  Bulunan İşyerlerine İlişkin Bilgiler (5746)
        argeilkodu = request.POST.get("argeilkodu")
        argevergidairesikodu = request.POST.get("argevergidairesikodu")
        argeiscisaysi = request.POST.get("argeiscisaysi")
        argeisyerissksicilno = request.POST.get("argeisyerissksicilno")
        argeadresbilgisi = request.POST.get("argeadresbilgisi")
        #Bildirim Kapsamında  Bulunan İşyerlerine İlişkin Bilgiler (5746)
        #Terkin Edilecek Tutara İlişkin Bilgiler (5746)
        terkinturu = request.POST.get("terkinturu")
        terkinadisoyadi = request.POST.get("terkinadisoyadi")
        terkintckimlikno = request.POST.get("terkintckimlikno")
        terkintarihi = request.POST.get("terkintarihi")
        terkinburtucrettoplami = request.POST.get("terkinburtucrettoplami")
        terkinmatrahtutari = request.POST.get("terkinmatrahtutari")
        terkinvergitutari = request.POST.get("terkinvergitutari")
        terkinorani = request.POST.get("terkinorani")
        #Terkin Edilecek Tutara İlişkin Bilgiler (5746)
        #G.V.K. GEÇİCİ 72. MADDE KAPSAMINDA YAPILAN GELİR VERGİSİ TEVKİFAT TUTARLARINA İLİŞKİN BİLDİRİM
        gvtckimlikno = request.POST.get("gvtckimlikno")
        gvadisoyadi = request.POST.get("gvadisoyadi")
        gvspordali = request.POST.get("gvspordali")
        gvamatorprofesyonel = request.POST.get("gvamatorprofesyonel")
        gvmatrahi = request.POST.get("gvmatrahi")
        gvtevkifatorani = request.POST.get("gvtevkifatorani")
        gvkesilengelirvergisi = request.POST.get("gvkesilengelirvergisi")
        gviadeyekonuolanvergisi = request.POST.get("gviadeyekonuolanvergisi")
        #G.V.K. GEÇİCİ 72. MADDE KAPSAMINDA YAPILAN GELİR VERGİSİ TEVKİFAT TUTARLARINA İLİŞKİN BİLDİRİM
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (6550)
        merkezadi = request.POST.get("merkezadi")
        projekodu = request.POST.get("projekodu")
        projebaslangictarihi = request.POST.get("projebaslangictarihi")
        projebitistarihi = request.POST.get("projebitistarihi")
        sgkisyerino = request.POST.get("sgkisyerino")
        isyerininadi = request.POST.get("isyerininadi")
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (6550)

        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (6550)
        projekodubilgisi = request.POST.get("projekodubilgisi")
        projekapsamitckimlikno = request.POST.get("projekapsamitckimlikno")
        projekapsamicalisanpersonelsuresi = request.POST.get("projekapsamicalisanpersonelsuresi")
        toplamucret = request.POST.get("toplamucret")
        eldeedilenucret = request.POST.get("eldeedilenucret")
        yasakapsamindakesilmeyengelirvergisi = request.POST.get("yasakapsamindakesilmeyengelirvergisi")
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (6550)
    return render(request,"beyannameler/muhsgk.html",content)

#turizim Beyannamesi
def muhsgksayfasi2(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["ulkeler"] = ulke_ulke_kodlari.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["vergidairesi"] = vergi_dairesi.objects.all()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        #MATRAH VE VERGİ BİLDİRİMİ
        odemeturu2 = request.POST.get("odemeturu2")
        odemetutari2 = request.POST.get("odemetutari2")
        odemetutarikesinti2 = request.POST.get("odemetutarikesinti2")
        odemeturu3 = request.POST.get("odemeturu3")
        odemetutari3 = request.POST.get("odemetutari3")
        odemetutarikesinti3 = request.POST.get("odemetutarikesinti3")
        odemeturu4 = request.POST.get("odemeturu4")
        odemetutari4 = request.POST.get("odemetutari4")
        odemetutarikesinti4 = request.POST.get("odemetutarikesinti4")
        odemeturu5 = request.POST.get("odemeturu5")
        odemetutari5 = request.POST.get("odemetutari5")
        odemetutarikesinti5 = request.POST.get("odemetutarikesinti5")
        odemeturu6 = request.POST.get("odemeturu6")
        odemetutari6 = request.POST.get("odemetutari6")
        odemetutarikesinti6 = request.POST.get("odemetutarikesinti6")
        odemeturu7 = request.POST.get("odemeturu7")
        odemetutari7 = request.POST.get("odemetutari7")
        odemetutarikesinti7 = request.POST.get("odemetutarikesinti7")
        odemeturu8 = request.POST.get("odemeturu8")
        odemetutari8 = request.POST.get("odemetutari8")
        odemetutarikesinti8 = request.POST.get("odemetutarikesinti8")
        odemeturu9 = request.POST.get("odemeturu9")
        odemetutari9 = request.POST.get("odemetutari9")
        odemetutarikesinti9 = request.POST.get("odemetutarikesinti9")
        odemeturu10 = request.POST.get("odemeturu10")
        odemetutari10 = request.POST.get("odemetutari10")
        odemetutarikesinti10 = request.POST.get("odemetutarikesinti10")
        odemeturu11 = request.POST.get("odemeturu11")
        odemetutari11 = request.POST.get("odemetutari11")
        odemetutarikesinti11 = request.POST.get("odemetutarikesinti11")
        odemeturu12 = request.POST.get("odemeturu12")
        odemetutari12 = request.POST.get("odemetutari12")
        odemetutarikesinti12 = request.POST.get("odemetutarikesinti12")
        odemeturu13 = request.POST.get("odemeturu13")
        odemetutari13 = request.POST.get("odemetutari13")
        odemetutarikesinti13 = request.POST.get("odemetutarikesinti13")
        odemeturu14 = request.POST.get("odemeturu14")
        odemetutari14 = request.POST.get("odemetutari14")
        odemetutarikesinti14 = request.POST.get("odemetutarikesinti14")
        odemeturu15 = request.POST.get("odemeturu15")
        odemetutari15 = request.POST.get("odemetutari15")
        odemetutarikesinti15 = request.POST.get("odemetutarikesinti15")
        odemeturu16 = request.POST.get("odemeturu16")
        odemetutari16 = request.POST.get("odemetutari16")
        odemetutarikesinti16 = request.POST.get("odemetutarikesinti16")
        odemetutaritoplam = request.POST.get("odemetutaritoplam")
        odemetutarikesintitoplami = request.POST.get("odemetutarikesintitoplami")
        odemetutarikesinti5225kanunu = request.POST.get("odemetutarikesinti5225kanunu")
        odemetutarikesinti5746kanunu = request.POST.get("odemetutarikesinti5746kanunu")
        odemetutarikesinti4691kanunu = request.POST.get("odemetutarikesinti4691kanunu")
        odemetutarikesinti17b18kanunu = request.POST.get("odemetutarikesinti17b18kanunu")
        #MATRAH VE VERGİ BİLDİRİMİ
        #MAHSUP EDİLEN VERGİLER
        mahsupedilenvergi2  =request.POST.get("mahsupedilenvergi2")
        mahsupedilenvergi3  =request.POST.get("mahsupedilenvergi3")
        mahsupedilenvergi4  =request.POST.get("mahsupedilenvergi4")
        mahsupedilenvergi5  =request.POST.get("mahsupedilenvergi5")
        mahsupedilenvergi6  =request.POST.get("mahsupedilenvergi6")
        mahsupedilenvergi7  =request.POST.get("mahsupedilenvergi7")
        mahsupedilenvergi8  =request.POST.get("mahsupedilenvergi8")
        #MAHSUP EDİLEN VERGİLER
        #ÇALIŞAN BİLGİLERİ
        bilgiver1 = request.POST.get("bilgiver1")
        digerucretilicalisansayisi = request.POST.get("digerucretilicalisansayisi")
        digerucretiligelivmuaf = request.POST.get("digerucretiligelivmuaf")
        digerucretilisgkvmuaf = request.POST.get("digerucretilisgkvmuaf")
        digerucretilismatrahtoplami = request.POST.get("digerucretilismatrahtoplami")
        digerucretilisasgaritoplami = request.POST.get("digerucretilisasgaritoplami")
        digerucretilisgelirvergisikesintitoplami = request.POST.get("digerucretilisgelirvergisikesintitoplami")
        digerucretilisasgariistisnatoplami = request.POST.get("digerucretilisasgariistisnatoplami")
        digerucretilisdamgavergisitoplami = request.POST.get("digerucretilisdamgavergisitoplami")
        bilgiver2 = request.POST.get("bilgiver2")
        asgariucretilicalisansayisi = request.POST.get("asgariucretilicalisansayisi")
        asgariucretiligelivmuaf = request.POST.get("asgariucretiligelivmuaf")
        asgariucretilisgkvmuaf = request.POST.get("asgariucretilisgkvmuaf")
        asgariucretilismatrahtoplami = request.POST.get("asgariucretilismatrahtoplami")
        asgariucretilisasgaritoplami = request.POST.get("asgariucretilisasgaritoplami")
        asgariucretilisgelirvergisikesintitoplami = request.POST.get("asgariucretilisgelirvergisikesintitoplami")
        asgariucretilisasgariistisnatoplami = request.POST.get("asgariucretilisasgariistisnatoplami")
        asgariucretilisdamgavergisitoplami = request.POST.get("asgariucretilisdamgavergisitoplami")
        #ÇALIŞAN BİLGİLERİ
        #TAHAKKUKA ESAS İCMAL CETVELİ
        icmalcetveli2 = request.POST.get("icmalcetveli2")
        icmalcetveli3 = request.POST.get("icmalcetveli3")
        icmalcetveli4 = request.POST.get("icmalcetveli4")
        icmalcetveli5 = request.POST.get("icmalcetveli5")
        icmalcetveli6 = request.POST.get("icmalcetveli6")
        icmalcetveli7 = request.POST.get("icmalcetveli7")
        icmalcetveli8 = request.POST.get("icmalcetveli8")
        #TAHAKKUKA ESAS İCMAL CETVELİ
        #İŞYERİ BİLGİLERİ
        isyerituru  = request.POST.get("isyerituru")
        isyerikodu = request.POST.get("isyerikodu")
        isyeriticaretsicilno = request.POST.get("isyeriticaretsicilno")
        ticaretsicilmudurlugu = request.POST.get("ticaretsicilmudurlugu")
        faliyetnacekodu = request.POST.get("faliyetnacekodu")
        isyeriadi = request.POST.get("isyeriadi")
        isyeriadresno = request.POST.get("isyeriadresno")
        isyerimulkiyetdurumu = request.POST.get("isyerimulkiyetdurumu")
        #İŞYERİ BİLGİLERİ
        #Yeraltı ve Yerüstü Maden İşletmeleri Bildirimi
        Madenbigisi = request.POST.get("Madenbigisi")
        sehirlerilceler = request.POST.get("sehirlerilceler")
        madencinsi = request.POST.get("madencinsi")
        madeniscisaysi = request.POST.getU("madeniscisaysi")
        madensgkisyerisicilnumarasi = request.POST.get("madensgkisyerisicilnumarasi")
        madenruhsatbaslamatarihi = request.POST.get("madenruhsatbaslamatarihi")
        madenruhsatbitistarihi = request.POST.get("madenruhsatbitistarihi")
        madenisyeriadresi = request.POST.get("madenisyeriadresi")
        #Yeraltı ve Yerüstü Maden İşletmeleri Bildirimi
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (4691)
        maddekapsamindabildirimilsecimi = request.POST.get("maddekapsamindabildirimilsecimi")
        maddekapsamindavergidairesi = request.POST.get("maddekapsamindavergidairesi")
        maddekapsamindacalisansayisi = request.POST.get("maddekapsamindacalisansayisi")
        maddekapsamindaunitekodu = request.POST.get("maddekapsamindaunitekodu")
        maddekapsamindaeskiunitekodu = request.POST.get("maddekapsamindaeskiunitekodu")
        maddekapsamindailkodu = request.POST.get("maddekapsamindailkodu")
        maddekapsamindaisyerisiranosu = request.POST.get("maddekapsamindaisyerisiranosu")
        maddekapsamindaaltisnumarasi = request.POST.get("maddekapsamindaaltisnumarasi")
        maddekapsamindaisyerininadresi=request.POST.get("maddekapsamindaisyerininadresi")
        maddekapsamindaprojekodu = request.POST.get("maddekapsamindaprojekodu")
        maddekapsamindaisyeribulundugubolge = request.POST.get("maddekapsamindaisyeribulundugubolge")
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (4691)
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (4691)
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (4691)

        #Bildirim Kapsamında  Bulunan İşyerlerine İlişkin Bilgiler (5746)
        argeilkodu = request.POST.get("argeilkodu")
        argevergidairesikodu = request.POST.get("argevergidairesikodu")
        argeiscisaysi = request.POST.get("argeiscisaysi")
        argeisyerissksicilno = request.POST.get("argeisyerissksicilno")
        argeadresbilgisi = request.POST.get("argeadresbilgisi")
        #Bildirim Kapsamında  Bulunan İşyerlerine İlişkin Bilgiler (5746)
        #Terkin Edilecek Tutara İlişkin Bilgiler (5746)
        terkinturu = request.POST.get("terkinturu")
        terkinadisoyadi = request.POST.get("terkinadisoyadi")
        terkintckimlikno = request.POST.get("terkintckimlikno")
        terkintarihi = request.POST.get("terkintarihi")
        terkinburtucrettoplami = request.POST.get("terkinburtucrettoplami")
        terkinmatrahtutari = request.POST.get("terkinmatrahtutari")
        terkinvergitutari = request.POST.get("terkinvergitutari")
        terkinorani = request.POST.get("terkinorani")
        #Terkin Edilecek Tutara İlişkin Bilgiler (5746)
        #G.V.K. GEÇİCİ 72. MADDE KAPSAMINDA YAPILAN GELİR VERGİSİ TEVKİFAT TUTARLARINA İLİŞKİN BİLDİRİM
        gvtckimlikno = request.POST.get("gvtckimlikno")
        gvadisoyadi = request.POST.get("gvadisoyadi")
        gvspordali = request.POST.get("gvspordali")
        gvamatorprofesyonel = request.POST.get("gvamatorprofesyonel")
        gvmatrahi = request.POST.get("gvmatrahi")
        gvtevkifatorani = request.POST.get("gvtevkifatorani")
        gvkesilengelirvergisi = request.POST.get("gvkesilengelirvergisi")
        gviadeyekonuolanvergisi = request.POST.get("gviadeyekonuolanvergisi")
        #G.V.K. GEÇİCİ 72. MADDE KAPSAMINDA YAPILAN GELİR VERGİSİ TEVKİFAT TUTARLARINA İLİŞKİN BİLDİRİM
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (6550)
        merkezadi = request.POST.get("merkezadi")
        projekodu = request.POST.get("projekodu")
        projebaslangictarihi = request.POST.get("projebaslangictarihi")
        projebitistarihi = request.POST.get("projebitistarihi")
        sgkisyerino = request.POST.get("sgkisyerino")
        isyerininadi = request.POST.get("isyerininadi")
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNE İLİŞKİN BİLDİRİM (6550)

        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (6550)
        projekodubilgisi = request.POST.get("projekodubilgisi")
        projekapsamitckimlikno = request.POST.get("projekapsamitckimlikno")
        projekapsamicalisanpersonelsuresi = request.POST.get("projekapsamicalisanpersonelsuresi")
        toplamucret = request.POST.get("toplamucret")
        eldeedilenucret = request.POST.get("eldeedilenucret")
        yasakapsamindakesilmeyengelirvergisi = request.POST.get("yasakapsamindakesilmeyengelirvergisi")
        #BİLDİRİM KAPSAMINDA BULUNAN İŞYERLERİNİN ÇALIŞANLARINA İLİŞKİN BİLGİLER (6550)
    return render(request,"beyannameler/muhsgk.html",content)

def kurum_gecici_beyanname(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    content["indiirimler"] = gecicivergi_beyannamesi_inidimi.objects.all()
    content["iller_ilkodu"] = iller_ilkodu.objects.all()
    content["saglikhizmetindenfaydalananisletmeturu"] = saglikhizmetindenfaydalananisletmeturu.objects.all()
    content["saglikhizmetindenfaydalananisletmeadi"] = saglikhizmetindenfaydalananisletmeadi.objects.all()
    if request.POST:
        aysecimi = request.POST.get("aysecimi")
        ticarikazanczarar = request.POST.get("ticarikazanczarar")
        ticarikazanckar = request.POST.get("ticarikazanckar")
        yatiriminsindirimizarar = request.POST.get("yatirimindiirmizarar")
        istisnalarzarar = request.POST.get("istisnalarzarar")
        kalanticarikazanckar = request.POST.get("kalanticarikazanckar")
        serbestmeslekkazancizarar = request.POST.get("serbestmeslekkazancizarar")
        serbestmeslekkazancikar = request.POST.get("serbestmeslekkazancikar")
        indirim1 = request.POST.get("indirim1")
        tutari1 = request.POST.get("tutari1")
        indirim2 = request.POST.get("indirim2")
        tutari2 = request.POST.get("tutari2")
        indirim3 = request.POST.get("indirim3")
        tutari3 = request.POST.get("tutari3")
        indirim4 = request.POST.get("indirim4")
        tutari4 = request.POST.get("tutari4")
        indirim5 = request.POST.get("indirim5")
        tutari5 = request.POST.get("tutari5")
        toplambilgisi = request.POST.get("toplambilgisi")
        donemzarari = request.POST.get("donemzarari")
        gecicivergimatrahi = request.POST.get("gecicivergimatrahi")
        gecicvergiyetabimatrah = request.POST.get("gecicvergiyetabimatrah")
        gecicvergiorani = request.POST.get("gecicvergiorani")
        geneloranatabivergimatrahi = request.POST("geneloranatabivergimatrahi")
        #
        gecicivergimatrahi = request.POST.get("gecicivergimatrahi")
        hesaplanangecicivergi = request.POST.get("hesaplanangecicivergi")
        oncekideonemlerdehesaplanangecicivergi = request.POST.get("oncekideonemlerdehesaplanangecicivergi")
        odenmesigerekenvergi = request.POST.get("odenmesigerekenvergi")
        mahsupedilecektevkifat = request.POST.get("mahsupedilecektevkifat")
        mahsupedilecekgecicivergivetevkifattoplami = request.POST.get("mahsupedilecekgecicivergivetevkifattoplami")
        odenecekgecicivergi = request.POST.get("odenecekgecicivergi")
        sonrakidonemdedevredentevkifattutari = request.POST.get("sonrakidonemdedevredentevkifattutari")
        sonrakidonemedevredengecicivergi = request.POST.get("sonrakidonemedevredengecicivergi")
        damgavergisi = request.POST.get("damgavergisi")
        #
        faliyetkodu1 = request.POST.get("faliyetkodu1")
        burtutsatistutari1 = request.POST.get("burtutsatistutari1")
        faliyetkodu2 = request.POST.get("faliyetkodu2")
        burtutsatistutari2 = request.POST.get("burtutsatistutari2")
        faliyetkodu3 = request.POST.get("faliyetkodu3")
        burtutsatistutari3 = request.POST.get("burtutsatistutari3")
        #
        istisna1 = request.POST.get("istisna1")
        kar1 = request.POST.get("kar1")
        zarar1 = request.POST.get("zarar1")
        istisna2 = request.POST.get("istisna2")
        kar2 = request.POST.get("kar2")
        zarar2 = request.POST.get("zarar2")
        istisna3 = request.POST.get("istisna3")
        kar3 = request.POST.get("kar3")
        zarar3 = request.POST.get("zarar3")
        istisna4 = request.POST.get("istisna4")
        kar4 = request.POST.get("kar4")
        zarar4 = request.POST.get("zarar4")
        istisna5 = request.POST.get("istisna5")
        kar5 = request.POST.get("kar5")
        zarar5 = request.POST.get("zarar5")
        istisna6 = request.POST.get("istisna6")
        kar6 = request.POST.get("kar6")
        zarar6 = request.POST.get("zarar6")
        istisna7 = request.POST.get("istisna7")
        kar7 = request.POST.get("kar7")
        zarar7 = request.POST.get("zarar7")
        istisna8 = request.POST.get("istisna8")
        kar8 = request.POST.get("kar8")
        zarar8 = request.POST.get("zarar8")
        #
        istisnaturu = request.POST.get("istisnaturu")
        vergivetc = request.POST.get("vergivetc")
        #
        patentfaydalibelge = request.POST.getlist("patentfaydalibelge")
        numarasi = request.POST.getlist("numarasi")
        korumasonaeristarihi = request.POST.getlist("korumasonaeristarihi")
        istisnayakonukacanctutari = request.POST.getlist("istisnayakonukacanctutari")
        kazancturur = request.POST.getlist("kazancturur")
        #Yurtdışı Mukimi Kişi ve/veya Kurumbra Verien Sağlık Hizmetlerine ilişkin Fonm
        saglikhizmetindenfaydalanankisiadisoyadi = request.POST.getlist("saglikhizmetindenfaydalanankisiadisoyadi")
        saglikhizmetindenfaydalanankisidogumtarihi = request.POST.getlist("saglikhizmetindenfaydalanankisidogumtarihi")
        saglikhizmetindenfaydalanankisiuyrugu = request.POST.getlist("saglikhizmetindenfaydalanankisiuyrugu")
        saglikhizmetindenfaydalanankisipasaportnosu = request.POST.getlist("saglikhizmetindenfaydalanankisipasaportnosu")
        saglikhizmetindenfaydalananyerilkodu = request.POST.getlist("saglikhizmetindenfaydalananyerilkodu")
        saglikhizmetindenfaydalananisletmeturu1 = request.POST.getlist("saglikhizmetindenfaydalananisletmeturu")
        saglikhizmetindenfaydalananisletmeadi1 = request.POST.getlist("saglikhizmetindenfaydalananisletmeadi")
        faturayiduzenleyenkurumkisi = request.POST.getlist("faturayiduzenleyenkurumkisi")
        faturaduzenlemetarihi = request.POST.getlist("faturaduzenlemetarihi")
        faturakdvstutari = request.POST.getlist("faturakdvstutari")
        faturaduzenlemesayisi = request.POST.getlist("faturaduzenlemesayisi")
        #Yurtdışı Mukimi Kişi ve/veya Kurumbra Verien Egitim Hizmetlerine ilişkin Fonm
        egitimhizmetindenfaydalanankisiadisoyadi =request.POST.getlist("egitimhizmetindenfaydalanankisiadisoyadi")
        egitimhizmetindenfaydalanankisidogumtarihi = request.POST.getlist("egitimhizmetindenfaydalanankisidogumtarihi")
        egitimhizmetindenfaydalanankisiuyrugu = request.POST.getlist("egitimhizmetindenfaydalanankisiuyrugu")
        egitimhizmetindenfaydalanankisipasaportnosu = request.POST.getlist("egitimhizmetindenfaydalanankisipasaportnosu")
        egitimhizmetindenfaydalananyerilkodu = request.POST.getlist("egitimhizmetindenfaydalananyerilkodu")
        egitimhizmetindenfaydalananisletmeturu = request.POST.getlist("egitimhizmetindenfaydalananisletmeturu")
        egitimfaturayiduzenleyenkurumkisi = request.POST.getlist("egitimfaturayiduzenleyenkurumkisi")
        egitimfaturaduzenlemetarihi = request.POST.getlist("egitimfaturaduzenlemetarihi")
        egitimfaturaduzenlemesayisi = request.POST.getlist("egitimfaturaduzenlemesayisi")
        egitimfaturakdvstutari = request.POST.getlist("egitimfaturakdvstutari")

        #
        alinanhizmetturu = request.POST.getlist("alinanhizmetturu")
        hizmettesebusvergiveyatc = request.POST.getlist("hizmettesebusvergiveyatc")
        hizmettesebusadisoyadiunvan = request.POST.getlist("hizmettesebusadisoyadiunvan")
        hizmetinbelgeturu = request.POST.getlist("hizmetinbelgeturu")
        hizmetlerinbelgetarihi = request.POST.getlist("hizmetlerinbelgetarihi")
        hizmetbelgeserino = request.POST.getlist("hizmetbelgeserino")
        hizmettutarbilgisi = request.POST.getlist("hizmettutarbilgisi")

    return render(request,"beyannameler/kurum_gecici_beyanname.html",content)
def gelir_vergisi_beyanname(request,slug):
    content = site_ayarlari()
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()
    content["firma_ayarlari"] = firma_ayarlari_ayar_kisimi.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) ).last()
    content["faliyet"] = sube_faliyet_bilgileri.objects.filter(sube_bilgisi=sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).first()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["dar_mukellef"] = kurumlar_dar_mukkelef_kimlik_ve_adres_bilgisi.objects.filter(sube_bilgisi =sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first() ).last()
    content["bilgi1"] = zarar_olsa_dahi_indilicekistisnaveindirim.objects.all()
    content["bilgi2"] = kazancin_bulunmasi_halinde_indirilecek_istisna_veindirimler.objects.all()
    content["beyannameduzenleyen"]=beyanname_duzenleyene_ait_bilgiler.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["mirasci"] =beyanname_bilgileri.objects.filter(sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["kanuni_temsilci"] = beyanname_kanuni_temsilcisi.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["beyannamegonderen"] = Beyannameyi_gonderen_bilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    content["ymmbilgileri"]  =ymmbilgileri.objects.filter(beyanname_bilgisi__sube_bilgisi = sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).first()).last()
    tevk_600ler = []
    for i in range(601,628):
        tevk_600ler.append(str(i))
    content["tevkifatlar"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_600ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    tevk_800ler = []
    for i in range(801,826):
        tevk_800ler.append(str(i))
    content["tevkifatlar1"] =tevkifat_tur_kodu.objects.filter(hesap_kodu__in = tevk_800ler,silinme_bilgisi = False,bagli_oldugu_firma = None)
    if request.POST:
        subeli = request.POST.get("sube")
        cikisyeri = request.POST.get("cikisyeri")
        ajanlik = request.POST.get("ajanlik")
        imalatyeri = request.POST.get("imalatyeri")
        satisyeri = request.POST.get("satisyeri")
        sair = request.POST.get("sair")
        #
        istisnazarari2016 = request.POST.get("istisnazarari2016")
        digerzararlar2016 = request.POST.get("digerzararlar2016")
        istisnazarari2017 = request.POST.get("istisnazarari2017")
        digerzararlar2017 = request.POST.get("digerzararlar2017")
        istisnazarari2018 = request.POST.get("istisnazarari2018")
        digerzararlar2018 = request.POST.get("digerzararlar2018")
        istisnazarari2019 = request.POST.get("istisnazarari2019")
        digerzararlar2019 = request.POST.get("digerzararlar2019")
        istisnazarari2020 = request.POST.get("istisnazarari2020")
        digerzararlar2020 = request.POST.get("digerzararlar2020")
        zararlartoplam = request.POST.get("zararlartoplam")
        #
        ticaribilanco = request.POST.get("ticaribilanco")
        ticaribilancozarar = request.POST.get("ticaribilancozarar")
        ticaribilancokar = request.POST.get("ticaribilancokar")
        addolananagelirkar = request.POST.get("addolananagelirkar")
        addolananagelir = request.POST.get("addolananagelir")
        #
        ilaveler1 = request.POST.get("ilaveler1")
        ilavelertutar1 = request.POST.get("ilavelertutar1")
        ilaveler2 = request.POST.get("ilaveler2")
        ilavelertutar2 = request.POST.get("ilavelertutar2")
        ilavelertoplambilgisi = request.POST.get("ilavelertoplambilgisi")
        ilavelertoplam = request.POST.get("ilavelertoplam")
        #
        istisnaindirim1 = request.POST.getlist("istisnaindirim1")
        istisnaindirimtutar1 = request.POST.getlist("istisnaindirimtutar1")
        istisnaindirimtutartoplambilgisi = request.POST.get("istisnaindirimtutartoplambilgisi")
        istisnaindirimtutartoplam = request.POST.get("istisnaindirimtutartoplam")
        #
        karilavetoplami = request.POST.get("karilavetoplami")
        karilavetoplamitutri = request.POST.get("karilavetoplamitutri")
        cariyilaiatistisnaindirim = request.POST.get("cariyilaiatistisnaindirim")
        cariyilaiatistisnaindirimtutari = request.POST.get("cariyilaiatistisnaindirimtutari")
        zararbilgisi = request.POST.get("zararbilgisi")
        zararbilgisitutari = request.POST.get("zararbilgisitutari")
        karbilgisi = request.POST.get("karbilgisi")
        karbilgisitutari =request.POST.get("karbilgisitutari")
        digeryilzararlari = request.POST.get("digeryilzararlari")
        digeryilzararlaritutari = request.POST.get("digeryilzararlaritutari")
        istisnadanyilzararlaritutari = request.POST.get("istisnadanyilzararlaritutari")
        mahsupedilecekgrcmisyilzararlari = request.POST.get("mahsupedilecekgrcmisyilzararlari")
        mahsupedilecekgrcmisyilzararlaritutari = request.POST.get("mahsupedilecekgrcmisyilzararlaritutari")
        indirimesas = request.POST.get("indirimesas")
        indirimesastutari = request.POST.get("indirimesastutari")
        #
        kazancindirimleri = request.POST.getlist("kazancindirimleri")
        kazancindirimleritutar = request.POST.getlist("kazancindirimleritutar")
        kazancindirimleritopamtutar = request.POST.get("kazancindirimleritopamtutar")
        kazancindirimleritopam = request.POST.get("kazancindirimleritopam")
        #
        vergibildiirmibilgi1 = request.POST.get("vergibildiirmibilgi1")
        vergibildiirmitutar1 = request.POST.get("vergibildiirmitutar1")
        vergibildiirmibilgi2 = request.POST.get("vergibildiirmibilgi2")
        fav_language  = request.POST.get("fav_language")
        vergibildiirmibilgi3 = request.POST.get("vergibildiirmibilgi3")
        vergibildiirmitutar3 = request.POST.get("vergibildiirmitutar3")
        vergibildiirmibilgi4 = request.POST.get("vergibildiirmibilgi4")
        vergibildiirmitutar4 = request.POST.get("vergibildiirmitutar4")
        vergibildiirmibilgi5 = request.POST.get("vergibildiirmibilgi5")
        vergibildiirmitutar5 = request.POST.get("vergibildiirmitutar5")
        vergibildiirmibilgi6 = request.POST.get("vergibildiirmibilgi6")
        vergibildiirmitutar6 = request.POST.get("vergibildiirmitutar6")
        vergibildiirmibilgi7 = request.POST.get("vergibildiirmibilgi7")
        vergibildiirmitutar7 = request.POST.get("vergibildiirmitutar7")
        vergibildiirmibilgi8 = request.POST.get("vergibildiirmibilgi8")
        vergibildiirmitutar8 = request.POST.get("vergibildiirmitutar8")
        #VERGİ BİLDİRİMİ
        vergibildirimi1 = request.POST.get("vergibildirimi1")
        vergibildirimitutar1 = request.POST.get("vergibildirimitutar1")
        vergibildirimi2 = request.POST.get("vergibildirimi2")
        vergibildirimitutar2 = request.POST.get("vergibildirimitutar2")
        vergibildirimi3 = request.POST.get("vergibildirimi3")
        vergibildirimitutar3 = request.POST.get("vergibildirimitutar3")
        #VERGİ BİLDİRİMİ
        #MAHSUP EDİLECEK VERGİLER
        mahsupedilecekbilgi1 = request.POST.get("mahsupedilecekbilgi1")
        mahsupedilecektutar1 = request.POST.get("mahsupedilecektutar1")
        mahsupedilecekbilgi2 = request.POST.get("mahsupedilecekbilgi2")
        mahsupedilecektutar2 = request.POST.get("mahsupedilecektutar2")
        mahsupedilecekbilgi3 = request.POST.get("mahsupedilecekbilgi3")
        mahsupedilecektutar3 = request.POST.get("mahsupedilecektutar3")
        mahsupedilecekbilgi4 = request.POST.get("mahsupedilecekbilgi4")
        mahsupedilecektutar4 = request.POST.get("mahsupedilecektutar4")
        #MAHSUP EDİLECEK VERGİLER

        #
        mahsupedilecekergitoplamibilgi = request.POST.get("mahsupedilecekergitoplamibilgi")
        mahsupedilecekergitoplamitutar = request.POST.get("mahsupedilecekergitoplamitutar")
        mahsupedilmeyecekyabancibilgi = request.POST.get("mahsupedilmeyecekyabancibilgi")
        mahsupedilmeyecekyabancitutar = request.POST.get("mahsupedilmeyecekyabancitutar")
        odenemesigerekenkurumlarvergisi = request.POST.get("odenemesigerekenkurumlarvergisi")
        odenemesigerekenkurumlarvergisitutar = request.POST.get("odenemesigerekenkurumlarvergisitutar")
        tesciledilmeyenkurumlarvergisi = request.POST.get("tesciledilmeyenkurumlarvergisi")
        tesciledilmeyenkurumlarvergisitutar = request.POST.get("tesciledilmeyenkurumlarvergisitutar")
        islemlerdensonraodemesigerekenvergi = request.POST.get("islemlerdensonraodemesigerekenvergi")
        islemlerdensonraodemesigerekenvergitutar = request.POST.get("islemlerdensonraodemesigerekenvergitutar")
        iadesigerekengecivergi = request.POST.get("iadesigerekengecivergi")
        iadesigerekengecivergitutar = request.POST.get("iadesigerekengecivergitutar")
        iadesigerekenkruumlarvergisi = request.POST.get("iadesigerekenkruumlarvergisi")
        iadesigerekenkruumlarvergisitutar = request.POST.get("iadesigerekenkruumlarvergisitutar")
        iadesigerekengecicivergi = request.POST.get("iadesigerekengecicivergi")
        iadesigerekengecicivergitutat = request.POST.get("iadesigerekengecicivergitutat")
        kalanvergiindirimi = request.POST.get("kalanvergiindirimi")
        kalanvergiindirimitutar = request.POST.get("kalanvergiindirimitutar")
        damgavergisi = request.POST.get("damgavergisi")
        damgavergisitutar = request.POST.get("damgavergisitutar")
        kazancintespityontemi = request.POST.get("kazancintespityontemi")
        kazancintespityontemisecimi = request.POST.get("kazancintespityontemisecimi")
        #
        kesintiyapanadisoyadibilgdsi = request.POST.getlist("kesintiyapanadisoyadibilgdsi")
        kesintiyaapantcvergikimlikno = request.POST.getlist("kesintiyaapantcvergikimlikno")
        kesintiyaapantcvergino = request.POST.getlist("kesintiyaapantcvergino")
        kesintiyaapanfonem = request.POST.getlist("kesintiyaapanfonem")
        kesintiburuttutar = request.POST.getlist("kesintiburuttutar")
        kesintitutar = request.POST.getlist("kesintitutar")
        #
        kardagitimbilgi2 = request.POST.get("kardagitimbilgi2")
        kardagitimoncekidonem2 = request.POST.get("kardagitimoncekidonem2")
        kardagitimcari2 = request.POST.get("kardagitimcari2")
        kardagitimbilgi3 = request.POST.get("kardagitimbilgi3")
        kardagitimoncekidonem3 = request.POST.get("kardagitimoncekidonem3")
        kardagitimcari3 = request.POST.get("kardagitimcari3")
        kardagitimbilgi4 = request.POST.get("kardagitimbilgi4")
        kardagitimoncekidonem4 = request.POST.get("kardagitimoncekidonem4")
        kardagitimcari4 = request.POST.get("kardagitimcari4")
        kardagitimbilgi5 = request.POST.get("kardagitimbilgi5")
        kardagitimoncekidonem5 = request.POST.get("kardagitimoncekidonem5")
        kardagitimcari5 = request.POST.get("kardagitimcari5")
        kardagitimbilgi6 = request.POST.get("kardagitimbilgi6")
        kardagitimoncekidonem6 = request.POST.get("kardagitimoncekidonem6")
        kardagitimcari6 = request.POST.get("kardagitimcari6")
        kardagitimbilgi7 = request.POST.get("kardagitimbilgi7")
        kardagitimoncekidonem7 = request.POST.get("kardagitimoncekidonem7")
        kardagitimcari7 = request.POST.get("kardagitimcari7")   
        kardagitimbilgi8 = request.POST.get("kardagitimbilgi8")
        kardagitimoncekidonem8 = request.POST.get("kardagitimoncekidonem8")
        kardagitimcari8 = request.POST.get("kardagitimcari8")
        kardagitimbilgi9 = request.POST.get("kardagitimbilgi9")
        kardagitimoncekidonem9 = request.POST.get("kardagitimoncekidonem9")
        kardagitimcari9 = request.POST.get("kardagitimcari9")  
        kardagitimbilgi10 = request.POST.get("kardagitimbilgi10")
        kardagitimoncekidonem10 = request.POST.get("kardagitimoncekidonem10")
        kardagitimcari10 = request.POST.get("kardagitimcari10")
        kardagitimbilgi11 = request.POST.get("kardagitimbilgi11")
        kardagitimoncekidonem11 = request.POST.get("kardagitimoncekidonem11")
        kardagitimcari11 = request.POST.get("kardagitimcari11")
        kardagitimbilgi12 = request.POST.get("kardagitimbilgi12")
        kardagitimoncekidonem12 = request.POST.get("kardagitimoncekidonem12")
        kardagitimcari12 = request.POST.get("kardagitimcari12")
        kardagitimbilgi13 = request.POST.get("kardagitimbilgi13")
        kardagitimoncekidonem13 = request.POST.get("kardagitimoncekidonem13")
        kardagitimcari13 = request.POST.get("kardagitimcari13")
        kardagitimbilgi14 = request.POST.get("kardagitimbilgi14")
        kardagitimoncekidonem14 = request.POST.get("kardagitimoncekidonem14")
        kardagitimcari14 = request.POST.get("kardagitimcari14")
        kardagitimbilgi15 = request.POST.get("kardagitimbilgi15")
        kardagitimoncekidonem15 = request.POST.get("kardagitimoncekidonem15")
        kardagitimcari15 = request.POST.get("kardagitimcari15")
        kardagitimbilgi16 = request.POST.get("kardagitimbilgi16")
        kardagitimoncekidonem16 = request.POST.get("kardagitimoncekidonem16")
        kardagitimcari16 = request.POST.get("kardagitimcari16")
        kardagitimbilgi17 = request.POST.get("kardagitimbilgi17")
        kardagitimoncekidonem17 = request.POST.get("kardagitimoncekidonem17")
        kardagitimcari17 = request.POST.get("kardagitimcari17")   
        kardagitimbilgi18 = request.POST.get("kardagitimbilgi18")
        kardagitimoncekidonem18 = request.POST.get("kardagitimoncekidonem18")
        kardagitimcari18 = request.POST.get("kardagitimcari18")
        kardagitimbilgi19 = request.POST.get("kardagitimbilgi19")
        kardagitimoncekidonem19 = request.POST.get("kardagitimoncekidonem19")
        kardagitimcari19 = request.POST.get("kardagitimcari19")
        kardagitimbilgi20 = request.POST.get("kardagitimbilgi20")
        kardagitimoncekidonem20 = request.POST.get("kardagitimoncekidonem20")
        kardagitimcari20 = request.POST.get("kardagitimcari20")
        kardagitimbilgi21 = request.POST.get("kardagitimbilgi21")
        kardagitimoncekidonem21 = request.POST.get("kardagitimoncekidonem21")
        kardagitimcari21 = request.POST.get("kardagitimcari21")
        kardagitimbilgi22 = request.POST.get("kardagitimbilgi22")
        kardagitimoncekidonem22 = request.POST.get("kardagitimoncekidonem22")
        kardagitimcari22 = request.POST.get("kardagitimcari22")
        kardagitimbilgi23 = request.POST.get("kardagitimbilgi23")
        kardagitimoncekidonem23 = request.POST.get("kardagitimoncekidonem23")
        kardagitimcari23 = request.POST.get("kardagitimcari23")
        kardagitimbilgi24 = request.POST.get("kardagitimbilgi24")
        kardagitimoncekidonem24 = request.POST.get("kardagitimoncekidonem24")
        kardagitimcari24 = request.POST.get("kardagitimcari24")
        kardagitimbilgi25 = request.POST.get("kardagitimbilgi25")
        kardagitimoncekidonem25 = request.POST.get("kardagitimoncekidonem25")
        kardagitimcari25 = request.POST.get("kardagitimcari25")
        kardagitimbilgi26 = request.POST.get("kardagitimbilgi26")
        kardagitimoncekidonem26 = request.POST.get("kardagitimoncekidonem26")
        kardagitimcari26 = request.POST.get("kardagitimcari26")
        kardagitimbilgi27 = request.POST.get("kardagitimbilgi27")
        kardagitimoncekidonem27 = request.POST.get("kardagitimoncekidonem27")
        kardagitimcari27 = request.POST.get("kardagitimcari27")   
        kardagitimbilgi28 = request.POST.get("kardagitimbilgi28")
        kardagitimoncekidonem28 = request.POST.get("kardagitimoncekidonem28")
        kardagitimcari28 = request.POST.get("kardagitimcari28")
        kardagitimbilgi29 = request.POST.get("kardagitimbilgi29")
        kardagitimoncekidonem29 = request.POST.get("kardagitimoncekidonem29")
        kardagitimcari29 = request.POST.get("kardagitimcari29")
        kardagitimbilgi30 = request.POST.get("kardagitimbilgi30")
        kardagitimoncekidonem30 = request.POST.get("kardagitimoncekidonem30")
        kardagitimcari30 = request.POST.get("kardagitimcari30")
        kardagitimbilgi31 = request.POST.get("kardagitimbilgi31")
        kardagitimoncekidonem31 = request.POST.get("kardagitimoncekidonem31")
        kardagitimcari31 = request.POST.get("kardagitimcari31")
        kardagitimbilgi32 = request.POST.get("kardagitimbilgi32")
        kardagitimoncekidonem32 = request.POST.get("kardagitimoncekidonem32")
        kardagitimcari32 = request.POST.get("kardagitimcari32")
        kardagitimbilgi33 = request.POST.get("kardagitimbilgi33")
        kardagitimoncekidonem33 = request.POST.get("kardagitimoncekidonem33")
        kardagitimcari33 = request.POST.get("kardagitimcari33")
        kardagitimbilgi34 = request.POST.get("kardagitimbilgi34")
        kardagitimoncekidonem34 = request.POST.get("kardagitimoncekidonem34")
        kardagitimcari34 = request.POST.get("kardagitimcari34")
        kardagitimbilgi35 = request.POST.get("kardagitimbilgi35")
        kardagitimoncekidonem35 = request.POST.get("kardagitimoncekidonem35")
        kardagitimcari35 = request.POST.get("kardagitimcari35")
        kardagitimbilgi36 = request.POST.get("kardagitimbilgi36")
        kardagitimoncekidonem36 = request.POST.get("kardagitimoncekidonem36")
        kardagitimcari36 = request.POST.get("kardagitimcari36")
        kardagitimbilgi37 = request.POST.get("kardagitimbilgi37")
        kardagitimoncekidonem37 = request.POST.get("kardagitimoncekidonem37")
        kardagitimcari37 = request.POST.get("kardagitimcari37")   
        kardagitimbilgi38 = request.POST.get("kardagitimbilgi38")
        kardagitimoncekidonem38 = request.POST.get("kardagitimoncekidonem38")
        kardagitimcari38 = request.POST.get("kardagitimcari38")
        kardagitimbilgi39 = request.POST.get("kardagitimbilgi39")
        kardagitimoncekidonem39 = request.POST.get("kardagitimoncekidonem39")
        kardagitimcari39 = request.POST.get("kardagitimcari39")
        kardagitimbilgi40 = request.POST.get("kardagitimbilgi40")
        kardagitimoncekidonem40 = request.POST.get("kardagitimoncekidonem40")
        kardagitimcari40 = request.POST.get("kardagitimcari40")
        kardagitimbilgi41 = request.POST.get("kardagitimbilgi41")
        kardagitimoncekidonem41 = request.POST.get("kardagitimoncekidonem41")
        kardagitimcari41 = request.POST.get("kardagitimcari41")
        kardagitimbilgi42 = request.POST.get("kardagitimbilgi42")
        kardagitimoncekidonem42 = request.POST.get("kardagitimoncekidonem42")
        kardagitimcari42 = request.POST.get("kardagitimcari42")
        kardagitimbilgi43 = request.POST.get("kardagitimbilgi43")
        kardagitimoncekidonem43 = request.POST.get("kardagitimoncekidonem43")
        kardagitimcari43 = request.POST.get("kardagitimcari43")
        kardagitimbilgi44 = request.POST.get("kardagitimbilgi44")
        kardagitimoncekidonem44 = request.POST.get("kardagitimoncekidonem44")
        kardagitimcari44 = request.POST.get("kardagitimcari44")
        kardagitimbilgi45 = request.POST.get("kardagitimbilgi45")
        kardagitimoncekidonem45 = request.POST.get("kardagitimoncekidonem45")
        kardagitimcari45 = request.POST.get("kardagitimcari45")
        kardagitimbilgi46 = request.POST.get("kardagitimbilgi46")
        kardagitimoncekidonem46 = request.POST.get("kardagitimoncekidonem46")
        kardagitimcari46 = request.POST.get("kardagitimcari46")
        kardagitimbilgi47 = request.POST.get("kardagitimbilgi47")
        kardagitimoncekidonem47 = request.POST.get("kardagitimoncekidonem47")
        kardagitimcari47 = request.POST.get("kardagitimcari47")   
        kardagitimbilgi48 = request.POST.get("kardagitimbilgi48")
        kardagitimoncekidonem48 = request.POST.get("kardagitimoncekidonem48")
        kardagitimcari48 = request.POST.get("kardagitimcari48")
        kardagitimbilgi49 = request.POST.get("kardagitimbilgi49")
        kardagitimoncekidonem49 = request.POST.get("kardagitimoncekidonem49")
        kardagitimcari49 = request.POST.get("kardagitimcari49")
        kardagitimbilgi50 = request.POST.get("kardagitimbilgi50")
        kardagitimoncekidonem50 = request.POST.get("kardagitimoncekidonem50")
        kardagitimcari50 = request.POST.get("kardagitimcari50")
        kardagitimbilgi51 = request.POST.get("kardagitimbilgi51")
        kardagitimoncekidonem51 = request.POST.get("kardagitimoncekidonem51")
        kardagitimcari51 = request.POST.get("kardagitimcari51")
        kardagitimbilgi52 = request.POST.get("kardagitimbilgi52")
        kardagitimoncekidonem52 = request.POST.get("kardagitimoncekidonem52")
        kardagitimcari52 = request.POST.get("kardagitimcari52")
        #
        mudurgenelmudur = request.POST.getlist("mudurgenelmudur")
        yonetimkuruluuyesi = request.POST.getlist("yonetimkuruluuyesi")
        ortakbilgisi = request.POST.getlist("ortakbilgisi")
        kanunitemsilcimi = request.POST.getlist("kanunitemsilcimi")
        yurticiyurtdisi = request.POST.getlist("yurticiyurtdisi")
        ortakvergikimliknosu = request.POST.getlist("ortakvergikimliknosu")
        ortakadisoyadiunvani = request.POST.getlist("ortakadisoyadiunvani")
        ortakikametgahadresi = request.POST.getlist("ortakikametgahadresi")
        ortaktckimliknosu = request.POST.getlist("ortaktckimliknosu")
        ortaktelefonnumarasi = request.POST.getlist("ortaktelefonnumarasi")
        ortakhisseorani = request.POST.getlist("ortakhisseorani")
        #
    return render(request,"beyannameler/gelir_vergisi_beyanname.html",content)
#
def firmayi_geri_getir(request,slug):
    firma.objects.filter(firma_ozel_anahtar = slug).update(silinme_bilgisi = False)
    a = "/company/companysettings/"
    return redirect(a)


def subeyi_geri_getir(request,slug):
    sube.objects.filter(id = slug).update(silinme_bilgisi = False)
    a = "/company/companysettings/"
    return redirect(a)



def ticari_raporlar(request,slug):
    content = site_ayarlari()
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"ticari_raporlar/raporlar.html",content)