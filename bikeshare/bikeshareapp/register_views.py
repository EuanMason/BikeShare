from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login
from util.sql_query import *
from django.http import HttpResponse
from .models import *


def to_register_view(request):
    return render(request, 'bikeshareapp/index.html')

def to_register_view_other(request):
    return render(request, 'bikeshareapp/register_other.html')

def register_view(request):
    nickname = request.POST.get("nickname", '')
    email = request.POST.get("email", '')
    # phone_number = request.POST.get("phone_number", '')
    password = request.POST.get("password", '')

    if nickname and email and password:
        # Check if user exists
        userTry = User.objects.filter(userid=email)
        if( len(userTry) == 0): # User does not exits
             # Create wallet
            new_wallet = Wallet(Credit=0)
            new_wallet.save()
            # Create user
            user = User(nickname=nickname, userid=email, password=password, WalletID=new_wallet)
            user.save()
            return render(request, 'bikeshareapp/index.html', {'status': 'COMPLETE'})
        else:
            return render(request, 'bikeshareapp/index.html', {'status': 'EXISTED'})
    else:
        return render(request, 'bikeshareapp/index.html', {'status': 'INCOMPLETE'})

def register_other_view(request):
    nickname = request.POST.get("nickname", '')
    email = request.POST.get("email", '')
    # phone_number = request.POST.get("phone_number", '')
    password = request.POST.get("password", '')
    role = request.POST.get("role", '')

    if nickname and email and password:
        # Check if user exists
        userTry = User.objects.filter(userid=email)
        if( len(userTry) == 0): # User does not exits
            # Create user
            user = User(nickname=nickname, userid=email, password=password, role=role)
            user.save()
            return render(request, 'bikeshareapp/register_other.html', {'status': 'COMPLETE'})
        else:
            return render(request, 'bikeshareapp/register_other.html', {'status': 'EXISTED'})
    else:
        return render(request, 'bikeshareapp/register_other.html', {'status': 'INCOMPLETE'})