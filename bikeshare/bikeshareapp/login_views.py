from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login

from util.decorators import auth_required
from util.sql_query import *
from django.http import HttpResponse, HttpResponseRedirect


def user_login(request):
    if request.POST:
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        user = login_check(userid, password)

        if user == 1 or user == 2:
            # State code :1) wrong password. 2) User does not exist
            return render(request, 'bikeshareapp/login.html', {'info': str(user)})
        else:
            role = user.role
            nickname = user.nickname
            response = HttpResponseRedirect('/home/')
            response.set_cookie('userid', userid)
            response.set_cookie('role', role)
            response.set_cookie('nickname', nickname)
            return response
    else:
        return render(request, 'bikeshareapp/login.html')


# function for
def check_if_login(request):
    try:
        userid = request.COOKIES['userid']
        nickname = request.COOKIES['nickname']
        role = request.COOKIES['role']
        return render(request, 'bikeshareapp/user_page.html', {'userid': userid, 'role': role, 'nickname': nickname})
    except KeyError:
        return render(request, 'user_page.html', {'userid': 'not logged in'})


@auth_required
def logout(request):
    response = HttpResponseRedirect('/login/')
    if request.COOKIES['userid'] is not None:
        response.delete_cookie('userid')
        response.delete_cookie('role')
        response.delete_cookie('nickname')
    return response
# Create your views here.
