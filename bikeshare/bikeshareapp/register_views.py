from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login
from util.sql_query import *
from django.http import HttpResponse
from .models import *


def to_register_view(request):
    return render(request, 'bikeshareapp/index.html')

def register_view(request):
    nickname = request.POST.get("nickname", '')
    email = request.POST.get("email", '')
    # phone_number = request.POST.get("phone_number", '')
    password = request.POST.get("password", '')

    if nickname and email and password:
        user = User(nickname=nickname, userid=email, password=password)
        user.save()
        return HttpResponse("Register Successful!")
    else:
        return HttpResponse("Please input complete account number or password!")