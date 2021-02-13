import json

from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status

from util.decorators import auth_required, role_check
from util.sql_query import *
from .models import *
from rest_framework.decorators import api_view


@role_check(['operator', 'manager'])
def select_locations(request):
    address_list = get_all_bikes_locations()
    if address_list is not None:
        return JsonResponse({'locations': address_list})
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@role_check(['operator', 'manager'])
def select_move_bike(request):
    try:
        if request.POST['location']:
            line1 = request.POST['location']
            location_id = Address.objects.get(Line1=line1).LocationID
            bikes = Bike.objects.filter(AddressLocationID=location_id, IsAvailable=1)
            id_list = []
            for bike in bikes:
                bike_id = bike.BikeID
                id_list.append(bike_id)
            return JsonResponse({'bikes': id_list})
        else:
            return JsonResponse({'bikes': "\'location\' missing"})

    except models.ObjectDoesNotExist:
        return JsonResponse({"state": "data no found"})

    except KeyError:
        return JsonResponse({"state": "key error"})


@api_view(['POST'])
@role_check(['operator', 'manager'])
def move_start(request):
    try:
        if request.body:
            bikes_json = json.loads(request.body)
            for bike_id in bikes_json['bike_id']:
                bike = Bike.objects.get(BikeID=str(bike_id))
                bike.IsAvailable = 0
                bike.save()

            return JsonResponse({"state": 1})
        return JsonResponse({"state": 2})

    except models.ObjectDoesNotExist:
        return JsonResponse({"state": 3})

    except KeyError:
        return JsonResponse({"state": 4})


@api_view(['POST'])
@role_check(['operator', 'manager'])
def move_get_loc_bikes(request):
    address_list = get_all_locations()
    bike_list = get_all_unavailable_bikes()
    if address_list is not None and bike_list is not None:
        print(address_list)
        return JsonResponse({'locations': address_list, 'unavailable_bikes': bike_list})
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@role_check(['operator', 'manager'])
def move_end(request):
    try:
        if request.body:
            json_obj = json.loads(request.body)
            line1 = json_obj["location"]
            address = Address.objects.get(Line1=line1)
            bikes = json_obj["bike_id"]
            for bike_id in bikes:
                bike = Bike.objects.get(BikeID=bike_id)
                bike.IsAvailable = 1
                bike.AddressLocationID = address
                bike.save()
            return JsonResponse({"state": 1})
        return JsonResponse({"state": 2})

    except models.ObjectDoesNotExist:
        return JsonResponse({"state": 3})

    except KeyError:
        return JsonResponse({"state": 4})
