from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .decorators import user_not_authenticated
from .forms import *

def login_and_register(request):
    form = UserRegistrationForm(request.POST)
    content = {"form":form}
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect("/")
            
            return redirect('/')
    else:  
        return render (request,"loginandregister.html",content)

@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        
        user = authenticate(
            username=request.POST.get("logemail"),
            password=request.POST.get("logpass"),
        )
        if user is not None:
            login(request, user)
            return redirect("/")
        return redirect("/")
    else:
        return redirect("/users/loginandregister/")

@user_not_authenticated
def registers(request):
    

    if request.POST:
        emailkullaniciadi = request.POST.get("emailkullaniciadi")
        sifresi = request.POST.get("sifresi")
        
        newUser = CustomUser(username =emailkullaniciadi,email = emailkullaniciadi)
        newUser.set_password(sifresi)

        newUser.save()
        login(request,newUser)
        return redirect('/')

    else:
        return render("/users/loginandregister/")
    
def sifre_degistir(request):
    if request.POST:
        logpass0 = request.POST.get("logpass0")
        logpass = request.POST.get("logpass")
        logpass2 = request.POST.get("logpass2")
        if logpass == logpass2:
            if request.user.check_password(logpass0):
                u = CustomUser.objects.get(id = request.user.id)
                u.set_password(logpass)
                u.save()
                return redirect("users:logout")
    return render(request,"changepassword.html")

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("/")
