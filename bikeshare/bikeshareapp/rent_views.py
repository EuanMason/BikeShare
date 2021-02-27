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
import datetime

from django.utils import timezone
import dateutil.parser

from bikeshareapp.rest_serializers import TripSerializer


@api_view(['POST'])
@auth_required
@role_check(['user'])
def rent_view(request):
    """ Create the objects when a bike is rented

    Args:
        request (Request): The request that comes with the call of this method
        This should include the bike id

    Returns:
        response (Response): The response containing a state 2 if the renting was done correctly
    """
    if request.POST:
        # Get the bike object from DB
        bike_id = str(request.POST.get("bikeid"))
        try:
            bike = Bike.objects.get(BikeID=bike_id)
        except Bike.DoesNotExist:
            # If the bike doesn't exist then return a state 0
            return JsonResponse({'state': 0})
        if bike.IsAvailable == 0 or bike.IsDefective == 1:
            # If the bike is not available return a 1
            return JsonResponse({'state': 1})

        # Change the bike to be 0 means is not available
        bike.IsAvailable = 0
        bike.save()
        # Get the start of the trip
        time_now = time.localtime()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time_now)
        start_date = start_time[:10]
        start_location = bike.AddressLocationID_id
        # Create a trip on tbe DB
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
        return JsonResponse({'state': 2, 'trip_id': str(trip_id)})

@api_view(['GET'])
@role_check(['user'])
def start_rent_view(request, trip_id):
    """ Render the view of the rendering the renting view

    Args:
        request (Request): The request that comes with the call of this method
        trip_id (int): The id of the trip to be rendered

    Returns:
        response (Response): The response containing a state 2 if the renting was done correctly
    """
    # Get the trip from DB
    currentTrip = Trip.objects.get(TripID=trip_id)
    serialized_trip = TripSerializer(currentTrip)
    
    # Get the actual time elapsed since bike was rented
    end_time = timezone.now().replace(tzinfo=None)
    current = end_time - dateutil.parser.parse(serialized_trip.data["start_time"])
    current = round(current.total_seconds())

    # Get the bike of the trip
    current_bike = dict(serialized_trip.data["bike"])['bike_id']

    # Check if the the end time and the start time are equals. If they are the trip is still going
    if (serialized_trip.data['end_time'] != serialized_trip.data['start_time'] ):
        return render(request, 'bikeshareapp/rent_bike.html', {'ended': 1})

    return render(request, 'bikeshareapp/rent_bike.html', {'trip_id': trip_id, 'current_time': current, 'current_bike': current_bike})
