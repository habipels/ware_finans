
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *
app_name = "users"
urlpatterns = [
    path("loginandregister/",login_and_register,name="LoginAndRegister"),
    path("login/",custom_login,name="custom_login"),
    path("logout/",logoutUser,name="logoutUser"),
    path("registers/",registers,name="registers"),
]
#