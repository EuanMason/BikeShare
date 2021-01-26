from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login
from bikeshare.util.sql_query import *
from django.http import HttpResponse
from .models import *


def to_register_view(request):
    return render(request, 'register.html')

def register_view(request):
    username = request.POST.get("username", '')
    email = request.POST.get("email", '')
    phone_number = request.POST.get("phone_number", '')
    password = request.POST.get("password", '')

    if username and email and phone_number and password:
        user = BikeUser(username=username,email=email,phone_number=phone_number,password=password)
        user.save()
        return HttpResponse("Register Successful!")
    else:
        return HttpResponse("Please input complete account number or password!")