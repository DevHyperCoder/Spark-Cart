from django.shortcuts import render,redirect

# About page
def about_page(request):
    return render(request,"about.html")