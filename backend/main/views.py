from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.http import HttpResponse
from users.models import *
from bilgideposu.models import *
from django.db.models import Q
# Create your views here.
def homepage(request):
    content = {}
    if request.user.is_authenticated:
        content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    else:
        return redirect("/users/loginandregister/")
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
    content["kasafisleri"] = KasaFisIslemleri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
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
    content["carifisleri"] = cari_fisleri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"cari/cari.html",content)
def yeni_cari_karti(request,slug):
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["stokkartlarim"] =  stok_kartlar.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["stokkartozelligi1"] = stok_birim_alis_satis_birimi.objects.filter(stok_karti_bilgisi__bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"stok/stok.html",content)

def yeni_stok_karti(request,slug):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
    siparisislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/siparis/"
    return redirect(link)

def siparis_aktif_pasif_sayfasi(request,slug,id):
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["bankalarim"]  = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_yetkilisi"]=banka_yetkilisi.objects.filter(banka_bilgisi__bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_kodlari"]=banka_kodlari.objects.filter(banka_bilgisi__bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_islemleri"] = KasaFisIslemleri.objects.filter(Q(islem_turu="Bankaya Yatırılan") | Q(islem_turu="Bankadan Çekilen") & Q(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)) )
    content["bankada_yapilanfisler"] = bankaFisIslemleri.objects.filter(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"banka/banka.html",content)
def yeni_banka_karti(request,slug):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"kasa/fisler/maasodeme.html",content)
#kasa Fiş İşlemeleri
#kasa cari fişleri
def kasa_cari_odeme_fisi(request,slug):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content = {}
    content["firmalarim"] = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["dilekcelerimiz"] = dilekceler.objects.filter(bagli_oldugu_firma = None)
    content["dilekceleriniz"] = dilekceler.objects.filter(bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render(request,"dilekcelersayfasi/dilekce.html",content)
#dilekce
#irsaliye işlemleri
def irsaliye_sayfasi(request,slug):
    content ={}
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
    content ={}
    irsaliyeislem_durumlari.objects.filter(id = id,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)).update(
            silinme_bilgisi = True
    )
    link = "/"+slug+"/irsaliye/"
    return redirect(link)
#sipariş silme
#siparişi irsaliyeye aktar
def siparisi_irsaliye_aktar(request,slug,id):
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
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
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["subeleri"] =  sube.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    return render (request,"demirbas/demirbaslar.html",content)

def demirbas_ekle(request,slug):
    content ={}
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








