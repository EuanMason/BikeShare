from django.http import HttpResponse, JsonResponse, Http404

from util.decorators import auth_required, role_check
from .models import *
from rest_framework.decorators import api_view


# from bikeshareapp.rest_serializers import RepairsSerializer


@api_view(['POST'])
@auth_required
def report_defective(request):
    request.encoding = 'utf-8'
    if 'bikeid' in request.POST and request.POST['bikeid']:
        try:
            bikeid = request.POST['bikeid']
            comment = request.POST['comment']
            bike = Bike.objects.get(BikeID=bikeid)
            bike.IsDefective = 1
            bike.save()

            reportUser = User.objects.get(userid=request.COOKIES['userid'])

            report, created = Repairs.objects.get_or_create(
                BikeID=bike,
                ReportedUser=reportUser,
                Issue=comment,
                InProgress=0
            )
            report.save()

            return JsonResponse({'state': 'Report success!'})
        except Exception as e:
            print("----------------------")
            print(e)
            return JsonResponse({'state': 'Bike ID wrong.'})
    elif 'bikeid' not in request.GET:
        return JsonResponse({'state': 'Error, Bike ID not been sent.'})
    elif not request.GET['bikeid']:
        return JsonResponse({'state': 'Error, Bike ID has no value'})
    else:
        return JsonResponse({'state': 'Unknown Error.'})
