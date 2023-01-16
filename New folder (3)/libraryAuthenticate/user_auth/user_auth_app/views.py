from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'sign.html')
def signForm(request):
    if request.method ==  'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        retype_password = request.POST.get('retype_password')

        if len(first_name) < 5 or len(last_name) < 5 or len(username) < 5:
            messages.error(request,'Your first name, last name and username must be greater then 3 characters.')
            return redirect('home')

        elif '@' not in email:
            messages.error(request,'enter an valid email address')
            return redirect('home')

        elif password != retype_password:
            messages.error(request, 'your password is not matched')
            return redirect('home')

        user = User.objects.create_user(username=username, email=email, password=retype_password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('log')

def log(request):
    return render(request, 'log.html')

def logForm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('main')

        elif user != username:
            messages.error(request, 'invalid password and username')
            return redirect('log')
        else:
            messages.error(request, 'invalid password and username')
            return redirect('log')

def main(request):
    return render(request, 'main.html')
