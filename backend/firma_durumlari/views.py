from django.shortcuts import render ,redirect,get_object_or_404
from .forms import *
from users.models import *
# Create your views here.
def firma_ekleme(request):
    form = firma_ekle(request.POST)
    v = vergi_dairesi.objects.all()
    faliyet_kace_kodu_modal = faliyet_bilgisi.objects.all()
    content = {"form":form,"vergidaireleri":v,
               "faliyet_nace":faliyet_kace_kodu_modal}
    if request.method == "POST":
        tanitici_isim = request.POST.get("firmataniticiadi")
        firma_adi = request.POST.get("firmaunvanadi")
        firma_soyadi = request.POST.get("firmaunvansoyadi")
        sube_adi = request.POST.get("subeadi")
        sube_soyadi = request.POST.get("subeunvani")
        adres_aciklama = request.POST.get("adresaciklama")
        mahallekoy = request.POST.get("mahallekoy")
        bulvar = request.POST.get("bulvar")
        cadde = request.POST.get("cadde")
        sokak = request.POST.get("sokak")
        adaparselno = request.POST.get("adaparselno")
        diskapino = request.POST.get("diskapino")
        ickapino = request.POST.get("ickapino")
        postakodu = request.POST.get("postakodu")
        semt = request.POST.get("semt")
        ilce = request.POST.get("ilce")
        il = request.POST.get("il")
        firmaverginumarasi = request.POST.get("firmaverginumarasi")
        firmavergidairesi = request.POST.get("firmavergidairesi")
        firmavergidairesikodu = request.POST.get("firmavergidairesikodu")
        sahisisetc = request.POST.get("sahisisetc")
        firmaeposta = request.POST.get("firmaeposta")
        firmawebadresi = request.POST.get("firmawebadresi")
        firmatelefon = request.POST.get("firmatelefon")
        defterturu = request.POST.get("defterturu")
        kdv1 =request.POST.get("kdv1")
        turizim = request.POST.get("turizim")
        muhsgk = request.POST.get("muhsgk")
        poset = request.POST.get("poset")
        firmadefterturu = request.POST.get("firmadefterturu")
        kdv2 = request.POST.get("kdv2")
        kdvorani = request.POST.get("kdvorani")
        firmamt = request.POST.get("firmamt")
        firmastokenvanter = request.POST.get("firmastokenvanter")
        faliyet_kurulus_tarihi = request.POST.get("faliyet_kurulus_tarihi")
        faliyet_terk_tarihi =request.POST.get("faliyet_terk_tarihi")
        if defterturu == "genelmuhasabe":
            defterturu = "Genel Muhasebe"
        elif defterturu == "isletmedefteri":
            defterturu = "İşletme Defteri"
        if kdv1 == "kdv1aylik":
            kdv1 = "Aylık"
        elif kdv1 == "kdv1ucaylik":
            kdv1 = "Üç Aylık"
        if turizim == "turizimaylik":
            turizim = "Aylık"
        elif turizim == "turizimucaylik":
            turizim = "Üç Aylık"
        if muhsgk == "sgkaylik":
            muhsgk = "Aylık"
        elif muhsgk == "sgkucaylik":
            muhsgk = "Üç Aylık"
        if poset == "posetaylik":
            poset = "Aylık"
        elif poset == "posetucaylik":
            poset = "Üç Aylık"
        elif poset == "posetaltiaylik":
            poset = "Altı Aylık"
        if firmadefterturu == "isletme":
            firmadefterturu = "İşletme"
        elif firmadefterturu == "serbestmeslekdefteri":
            firmadefterturu = "Serbest Meslek Defteri"
        if kdv2 == "kdv2aylik":
            kdv2 = "Aylık"
        elif kdv2 == "kdv2ucaylik":
            kdv2 = "Üç Aylık"
        firma_olustur = firma.objects.create(firma_muhasabecisi = request.user,
                             tanitici_isim = tanitici_isim ,
                             firma_unvani = firma_adi,
                             Firma_unvani2 = firma_soyadi,
                             silinme_bilgisi = False)
        yeni_adres  = adresler.objects.create(
            adres = adres_aciklama,mahhalle_koy=mahallekoy,
            bulvar = bulvar,cadde = cadde, sokak = sokak,
            adaparselno = adaparselno,diskapino = diskapino,
            ickapino = ickapino,posta_kodu = postakodu,semt=semt,
            ilce = ilce,il = il,silinme_bilgisi = False
        )
        sube.objects.create(
            bagli_oldugu_firma = get_object_or_404(firma,id = firma_olustur.id ),
            sube_adi = sube_adi,sube_unvani = sube_soyadi,adres_bilgisi = get_object_or_404(adresler,id = yeni_adres.id),
            vergi_dairesi_adi =get_object_or_404(vergi_dairesi,vergi_dairesi_adi = firmavergidairesi) ,vergi_dairesi_kodu = firmavergidairesikodu,
            vergi_numarasi = firmaverginumarasi,sahis_ise_tc = sahisisetc,
            email_adresi = firmaeposta,web_adresi = firmawebadresi,
            telefon_numarasi = firmatelefon,
            sube_defter_turu =defterturu,
            kdv1 = kdv1,kdv2 = kdv2,turizm = turizim,
            muhsgk = muhsgk,poset = poset,firma_defter_turu =firmadefterturu,
            mukellefiyet_turu= firmamt,stok_bilgisi =firmastokenvanter,
            gecici_vergi_orani = kdvorani
        )
        return redirect ("/")
    else:  
        return render (request,"firma_durumlari/firma_index.html",content)