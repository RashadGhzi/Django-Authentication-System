from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("signForm", signForm, name="signForm"),
    path("log", log, name="log"),
    path("sign", sign, name="sign"),
    path("logForm", logForm, name="logForm"),
    path("LogOut",LogOut,name="LogOut")
]
