from django.http import HttpResponse, JsonResponse, Http404

from util.decorators import auth_required, role_check
from .models import *
from rest_framework.decorators import api_view


# from bikeshareapp.rest_serializers import RepairsSerializer


@api_view(['POST'])
@auth_required
def report_defective(request):
    """ Create a report object on the DB when necessary

    Args:
        request (Request): The request that comes with the call of this method
        This should include the bike id and the comment to be added on the report of the bike

    Returns:
        response (Response): The response containing a state. 
    """
    request.encoding = 'utf-8'
    # Get the id from the request
    if 'bikeid' in request.POST and request.POST['bikeid']:
        try:
            # Get the bike and set it as defective
            bikeid = request.POST['bikeid']
            comment = request.POST['comment']
            bike = Bike.objects.get(BikeID=bikeid)
            bike.IsDefective = 1
            bike.save()

            # Get the user that is reporting the bike
            reportUser = User.objects.get(userid=request.COOKIES['userid'])

            # Create a report if not exists
            report, created = Repairs.objects.get_or_create(
                BikeID=bike,
                ReportedUser=reportUser,
                Issue=comment,
                InProgress=0
            )
            report.save()

            # Return the state of success
            return JsonResponse({'state': 'Report success!'})
        except Exception as e:
            # In case the bike already exists
            return JsonResponse({'state': 'Bike ID wrong.'})
    elif 'bikeid' not in request.GET:
        # In case the request is incorrect
        return JsonResponse({'state': 'Error, Bike ID not been sent.'})
    elif not request.GET['bikeid']:
        # In case the request is incorrect
        return JsonResponse({'state': 'Error, Bike ID has no value'})
    else:
        # In case something goes wrong on the server
        return JsonResponse({'state': 'Unknown Error.'})
