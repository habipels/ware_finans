from django.shortcuts import render ,redirect
from .forms import *

# Create your views here.
def firma_ekleme(request):
    form = firma_ekle(request.POST)
    content = {"form":form}
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.firma_muhasabecisi = request.user
            user.save()
            return redirect('/')
    else:  
        return render (request,"firma_durumlari/firma_index.html",content)