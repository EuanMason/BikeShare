from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login

from util.decorators import auth_required
from util.sql_query import *
from django.http import HttpResponse, HttpResponseRedirect

from bikeshareapp.models import User, Trip
from bikeshareapp.rest_serializers import UserSerializer, UserLimitedSerializer, TripSerializer



def user_login(request):
    if request.POST:
        userid = request.POST.get('userid').replace(' ','')
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
        if role=='operator':
            return render(request, 'bikeshareapp/operator_page.html', {'userid': userid, 'role': role, 'nickname': nickname})
        elif role=='manager':
            return render(request, 'bikeshareapp/manager_page.html', {'userid': userid, 'role': role, 'nickname': nickname})
        else: 
            currentTrip = User.objects.get(userid=userid)
            serialized_trip = UserSerializer(currentTrip)
            wallet_credit = dict(serialized_trip.data['wallet_id'])['credit']
            # Check if there is a trip on going
            trip = None
            queryset_trip = Trip.objects.filter(UserID=userid)
            for qt in queryset_trip:
                qts = TripSerializer(qt)
                if (qts.data['end_time'] == qts.data['start_time'] ):
                    trip = qts.data['trip_id']
                    break
            
            return render(request, 'bikeshareapp/user_page.html', {'userid': userid, 'role': role, 'nickname': nickname, 'wallet': wallet_credit, 'trip': trip})
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
