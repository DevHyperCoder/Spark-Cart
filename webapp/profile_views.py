from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile


@login_required(login_url='/signin')
def profile(request):
    return render(request, "profile.html", {'user': request.user})
