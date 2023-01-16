from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signForm', signForm, name='signForm'),
    path('log', log, name='log'),
    path('logForm', logForm, name='logForm'),
    path('main', main, name='main')
]