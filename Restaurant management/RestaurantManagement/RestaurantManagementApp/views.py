from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def signForm(request): 
    return render(request, 'auth/sign.html')

def log(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, 'auth/log.html')

def sign(request):
    if request.method == "POST":
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        retype_password = request.POST['retype_password']
        

        if len(fname) < 5 or len(lname) < 5 or len(username) < 5:
            messages.error(request, "First name, Lastname or Username can't be less then 5 character.")
            return redirect('signForm')
        elif '@' not in email:
            messages.error(request, "Enter an valid email address.")
            return redirect('signForm')
        elif password != retype_password:
            messages.error(request, "Your password is not mached.")
            return redirect('signForm')
        else:
            user = User.objects.create_user(username=username,email=email, password=retype_password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your account has been successfully created.")
            return redirect('/log')

    return HttpResponse('sign')

def logForm(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, "You have successfully LogIn.")
            return redirect("/")
        else:
            messages.error(request, "Please enter a valid username and password.")
            return redirect('log')

def LogOut(request):
    logout(request)
    messages.success(request, "You have successfully logout.")
    return redirect("log")
