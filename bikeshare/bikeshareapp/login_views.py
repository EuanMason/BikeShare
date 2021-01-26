from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login
from util.sql_query import *
from django.http import HttpResponse


def login_index(request):
    return render(request, 'login_beta.html')


def user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = login_check(username, password)

        if user == 1 or user == 2:
            # State code :1) wrong password. 2) User does not exist
            return render(request, 'login_beta.html', {'info': str(user)})
        else:
            role = user.role
            nickname = user.nickname
            response = render(request, 'login_beta.html', {'info': "Login Successful!"})
            response.set_cookie('username', username)
            response.set_cookie('role', role)
            response.set_cookie('nickname', nickname)
            return response
    else:
        print("Not Post")
        return render(request, 'login_beta.html', {'info': "This is a GET request"})


def check_if_login(request):
    nickname = request.COOKIES['nickname']
    userid = request.COOKIES['username']
    role = request.COOKIES['role']
    return render(request, 'user_page.html', {'userid': userid, 'role': role, 'nickname': nickname})
# Create your views here.
