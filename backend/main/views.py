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
        link = "/"+slug+"/stok/"
        return redirect(link)
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

#banka
def banka_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    content["bankalarim"]  = banka.objects.filter(silinme_bilgisi = False,bagli_oldugu_firma = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_yetkilisi"]=banka_yetkilisi.objects.filter(banka_bilgisi__bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
    content["banka_kodlari"]=banka_kodlari.objects.filter(banka_bilgisi__bagli_oldugu_firma =  get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug))
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Tahsilat Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        gelir_bilgisi = get_object_or_404(Gelirler,gelir_kodu = gelirkodu,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A"
        )
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Ödeme Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        gider_bilgisi = get_object_or_404(Giderler,gider_kodu = gelirkodu,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B"
        )
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        if borcalacak == "B":
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            )
        else:
            KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
            islem_turu = "Açılış Fişi",tarih =tarih,saat= saat,
            evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
            ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
            birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,aciklama = aciklama,
            islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur
            ,alacakbilgisi = borcalacak
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Kasa Tahsilat Makbuzu",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        gelir_bilgisi = get_object_or_404(Gelirler,gelir_kodu = gelirkodu,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A"
        )
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Kasa Ödeme Makbuzu",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        gider_bilgisi = get_object_or_404(Giderler,gider_kodu = gelirkodu,bagli_oldugu_firma=get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug) )
        ,gelir_muh_kodu = gelirmuhtasarkodu,islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B"
        )
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
        link = "/"+slug+"/kasa/"
        return redirect(link)
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Cari Ödeme Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="B"
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
        if tutardoviz =="" or tutardoviz == None:
            tutardoviz = 0
        KasaFisIslemleri.objects.create(bagli_oldugu_firma =get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug),
        islem_turu = "Cari Tahsilat Fişi",tarih =tarih,saat= saat,
        evrak_no = evrakno,ent_kodu = entkodu,birinciislem_sube_bilgisi = get_object_or_404(sube,id=subebilgisi),
        ozelkod1 = ozelkod1,ozelkod2 = ozelkod2,birinci_departman = departman,
        birinci_kasa_bilgisi = get_object_or_404(Kasa,id=kasabilgisi),birinci_kasa_muh_kodu =muhtasarkodu,
        islem_doviz_cinsi = islemdovizcinsi,aciklama = aciklama,
        islemi_yapan = tahsilatiodemeyiyapan,tutar= float(tutar),gunluk_kur = gunlukkur,uygun_kur = uygunkur,
        doviz_tutar = tutardoviz,alacakbilgisi ="A"
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
    return render(request,"kasa/banka/kasabankayatirilan.html",content)
#kasa Banka fişleri
