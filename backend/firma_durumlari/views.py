from django.shortcuts import render ,redirect
from .forms import *
from users.models import *
# Create your views here.
def firma_ekleme(request):
    form = firma_ekle(request.POST)
    content = {"form":form}
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
        firma.objects.create(firma_muhasabecisi = request.user,
                             tanitici_isim = tanitici_isim ,
                             firma_unvani = firma_adi,
                             Firma_unvani2 = firma_soyadi,
                             silinme_bilgisi = False)
        adresler.objects.create(
            adres = adres_aciklama,mahhalle_koy=mahallekoy,
            bulvar = bulvar,cadde = cadde, sokak = sokak,
            adaparselno = adaparselno,diskapino = diskapino,
            ickapino = ickapino,posta_kodu = postakodu,semt=semt,
            ilce = ilce,il = il,silinme_bilgisi = False
        )
        return redirect ("/")
    else:  
        return render (request,"firma_durumlari/firma_index.html",content)