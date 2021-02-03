from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bikeshareapp.models import Wallet, Address, Bike, Trip
from bikeshareapp.rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer

# The file rest_views.py is only to have the basic stuff
# Here we can add any other functionality that we need.
# NOTE:
#       * Always add the decorator @api_view and give a list of the allowed methods
#       * Remeber to add your url to url.py bikeshare/urls.py (it's not in this same folder)

#/* -------------------------------------------------------------------------- */
#/*                             General Actions                                */
#/* -------------------------------------------------------------------------- */
@api_view(['GET'])
def getAllBikes(request, type):
    data_to_return = {}
    if type == 1:
        # For customer we only need the available bikes and not defective
        queryset = Bike.objects.filter(IsAvailable = 1, IsDefective = 0)
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    elif type == 2:
        # For operator we need to show the bikes that are available and 
        #   it does not matter if it is defective
        queryset = Bike.objects.filter(IsAvailable = 1)
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    elif type == 3:
        queryset = Bike.objects.all()
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    
    response = {
        'data': data_to_return
    }
    return Response(response, status=status.HTTP_200_OK)

#/* -------------------------------------------------------------------------- */
#/*                            Customer Actions                                */
#/* -------------------------------------------------------------------------- */
@api_view(['POST'])
def addMoney(request):
    if request.method == 'POST':
        response = {
            "Status":"OK!!!!!!!",
            "request": request.data
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


#/* -------------------------------------------------------------------------- */
#/*                            Operator Actions                                */
#/* -------------------------------------------------------------------------- */


#/* -------------------------------------------------------------------------- */
#/*                             Manager Actions                                */
#/* -------------------------------------------------------------------------- */