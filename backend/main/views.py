from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.http import HttpResponse
from users.models import *
from bilgideposu.models import *
# Create your views here.
def homepage(request):
    content = {}
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    return render(request,"index.html",content)

def firma_sayfasi(request,slug):
    content = {}
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"firma_index.html",content)
#Kasa İşlemeleri 
def kasa_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["kasakartlarim"] = Kasa.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"kasa/kasa.html",content)

def yeni_kasa_karti_sayfasi(request,slug):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["giderler"] = Giderler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"gider_gelir/gider.html",content)


def yeni_gider_sayfasi(request,slug):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["gelirler"] = Gelirler.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"gider_gelir/gelir.html",content)


def yeni_gelir_sayfasi(request,slug):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["carikartlari"] = cari_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"cari/cari.html",content)
def yeni_cari_karti(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    if request.POST:
        anacarikodu = request.POST.get("anacarikodu")
        caridetay = request.POST.get("caridetay")
        print(anacarikodu,caridetay)
    return render(request,"cari/yenicari.html",content)
#Cari İşlemeler
#Stok İşlemleri
def stok_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"stok/stok.html",content)

def yeni_stok_karti(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"stok/yeni_stok.html",content)
#Stok İşlemleri

#Fatura İşlemleri
def fatura_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"fatura/fatura.html",content)
#Fatura İşlemleri

#Sipariş Sayfası
def siparis_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"siparis/siparis.html",content)
#Sipariş Sayfası