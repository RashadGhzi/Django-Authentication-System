from django.shortcuts import render, redirect
from django.contrib.auth import views,urls
from django.views.generic.base import TemplateView
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.decorators import login_required  # This is for function view
from django.contrib.auth.mixins import LoginRequiredMixin  # User login required This is for class based view
# Create your views here.

# @login_required  # This is for function view
class Home(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    login_url = 'login/'  # If user is not authenticate this url will redirect the user to login page

class UserRegister(FormView):
    template_name = 'core/user_register.html'
    form_class = forms.UserRegisterForm

    def form_valid(self, form):
        login(self.request.user)
        messages.success(self.request, 'registered successfully')
        return redirect("home")

class Login(SuccessMessageMixin, views.LoginView):
    template_name = 'core/login.html'
    success_url = reverse_lazy('home')
    success_message = "You have been logged in."
    redirect_authenticated_user = True

    # if form data is not valid then this view will hit 
    def form_invalid(self, form):
        messages.error(self.request, "your username and password did't mached!")
        return super().form_invalid(form)

class PasswordReset(views.PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    template_name = 'core/password_reset.html'

class PasswordResetDone(views.PasswordResetDoneView):
    template_name = 'core/password_reset_done.html'

class PasswordResetConfirm(views.PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'

class PasswordResetComplete(views.PasswordResetCompleteView):
    template_name = 'core/password_reset_complete.html'
