from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login

from util.sql_query import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
import time

from util.decorators import auth_required, role_check
from .models import *
from rest_framework.decorators import api_view

@api_view(['POST'])
@auth_required
def rent_view(request):
    if request.POST:
        bike_id = str(request.POST.get("bikeid"))
        try:
            bike = Bike.objects.get(BikeID=bike_id)
        except Bike.DoesNotExist:
            return JsonResponse({'state': 0})
        if bike.IsAvailable == 0 or bike.IsDefective == 1:
            return JsonResponse({'state': 1})
        bike.IsAvailable = 0
        time_now = time.localtime()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time_now)
        start_date = start_time[:10]
        start_location = bike.AddressLocationID_id
        # TripID = user_id + date
        user_id = request.COOKIES.get('userid')
        trip_id = bike_id + time.strftime("%Y%m%d%H%M%S", time_now)
        # print(trip_id)
        Trip.objects.create(TripID=trip_id,
                            Date=start_date,
                            StartTime=start_time,
                            EndTime=start_time,
                            Cost=0,
                            PaymentStatus=0,
                            BikeID_id=bike_id,
                            EndAddress_id=start_location,
                            StartAddress_id=start_location,
                            UserID_id=user_id
                            )
        # response = JsonResponse({'state': 2, 'trip_id': trip_id})
        # response.set_cookie('trip_id', trip_id)
        return JsonResponse({'state': 2, 'trip_id': str(trip_id)})

@api_view(['GET'])
@auth_required
def start_rent_view(request, trip_id):
    return render(request, 'bikeshareapp/rent_bike.html', {'trip_id': trip_id})