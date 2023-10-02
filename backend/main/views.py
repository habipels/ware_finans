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
        #diger bilgiler bunların modelsi yok
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
        #diger bilgiler bunların modelsi yok
        #Şubebilgileri modelsi yok
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
        #Şubebilgileri modelsi yok
        #notlar modelsi yok
        notlartarihi= request.POST.get("notlartarihi")
        notlarsatici= request.POST.get("notlarsatici")
        notlarnot= request.POST.get("notlarnot")
        #notlar modelsi yok
        #firma gorevlisi modelsi yok
        firmagoreviadi= request.POST.get("firmagoreviadi")
        firmagorevligorevi= request.POST.get("firmagorevligorevi")
        firmagorevliistelefonu= request.POST.get("firmagorevliistelefonu")
        firmagorevlidahilinumara= request.POST.get("firmagorevlidahilinumara")
        firmagorevligsm= request.POST.get("firmagorevligsm")
        firmaaciklama= request.POST.get("firmaaciklama")
        #firma gorevlisi modelsi yok
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