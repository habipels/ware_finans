from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import HttpResponse
from users.models import *
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

def kasa_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"kasa/kasa.html",content)

def yeni_kasa_karti_sayfasi(request,slug):
    content ={}
    content["firma"] = get_object_or_404(firma,silinme_bilgisi = False,firma_muhasabecisi = request.user,firma_ozel_anahtar = slug)
    return render(request,"kasa/yenikasa.html",content)