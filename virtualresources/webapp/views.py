from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm

# Sign in route (LOGIN)
def sign_in(request):
    data =request.POST or None 
    form = AuthenticationForm(data = data)

    nextA = ""
    if request.GET:
        nextA = request.GET.get('next')

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username,password = password)
        login(user = user,request = request)
        if nextA != "":
            print(nextA)
            return redirect(nextA)

        return redirect('home')
    
    return render(request,"signin.html",{'form':form,'next':nextA})

# Sign up route (REGISTER)
def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('sign_in')
        
    return render(request,"register.html",{'form':form})

# Logout page
def logout(request):
    django_logout(request)
    return redirect('home')

    

            
