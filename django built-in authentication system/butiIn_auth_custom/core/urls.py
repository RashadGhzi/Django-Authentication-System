from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user_register/', views.UserRegister.as_view(), name='user_register'),
    path('login/', views.Login.as_view(), name='login'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', views.PasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]
