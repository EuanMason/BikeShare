from django.http import HttpResponse, JsonResponse, Http404

from util.decorators import auth_required, role_check
from .models import *
from rest_framework.decorators import api_view


@role_check(['operator', 'manager'])
def select_locations(request):
    try:
        bike_list = Bike.objects.all()
        address_list = []
        for bike in bike_list:
            location_id = bike.AddressLocationID
            location = location_id.Line1
            address_list.append(location)
        address_list = list(set(address_list))
        return JsonResponse({'locations': address_list})
    except:
        return Http404()


@role_check(['operator', 'manager'])
def move_bike(request):
    if request.POST and request.POST['location']:
        line1 = request.POST['location']
        location_id = Address.objects.get(Line1=line1).LocationID
        bikes = Bike.objects.filter(AddressLocationID=location_id, IsAvailable=1)
        id_list = []
        for bike in bikes:
            bike_id = bike.BikeID
            id_list.append(bike_id)
        return JsonResponse({'bikes_can_be_move': id_list})
