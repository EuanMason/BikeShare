from django.http import HttpResponse, JsonResponse

from .models import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def report_defective(request):
    request.encoding = 'utf-8'
    if 'bikeid' in request.GET and request.GET['bikeid']:
        try:
            bikeid = request.GET['bikeid']
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
