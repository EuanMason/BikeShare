from django.http import HttpResponse, JsonResponse, Http404

from util.decorators import auth_required, role_check
from .models import *
from rest_framework.decorators import api_view


@api_view(['POST'])
@auth_required
def report_defective(request):
    request.encoding = 'utf-8'
    if 'bikeid' in request.POST and request.POST['bikeid']:
        try:
            bikeid = request.POST['bikeid']
            bike = Bike.objects.get(BikeID=bikeid)
            bike.IsDefective = 1
            bike.save()
            return JsonResponse({'state': 'Report success!'})
        except:
            return JsonResponse({'state': 'Bike ID wrong.'})
    elif 'bikeid' not in request.GET:
        return JsonResponse({'state': 'Error, Bike ID not been sent.'})
    elif not request.GET['bikeid']:
        return JsonResponse({'state': 'Error, Bike ID has no value'})
    else:
        return JsonResponse({'state': 'Unknown Error.'})


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
    pass
