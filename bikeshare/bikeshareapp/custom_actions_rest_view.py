from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bikeshareapp.models import Wallet, Address, Bike, Trip, User
from bikeshareapp.rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, UserSerializer

# The file rest_views.py is only to have the basic stuff
# Here we can add any other functionality that we need.
# NOTE:
#       * Always add the decorator @api_view and give a list of the allowed methods
#       * Remeber to add your url to url.py bikeshare/urls.py (it's not in this same folder)

#/* -------------------------------------------------------------------------- */
#/*                             General Actions                                */
#/* -------------------------------------------------------------------------- */
@api_view(['GET'])
def getAllBikes(request):
    queryset = Bike.objects.all()
    serialized = BikeSerializer(queryset, many=True)#, context={'request': request})
    response = {
        'data': serialized.data
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def getAvailableBikes(request):
    queryset = Bike.objects.filter(IsAvailable=1)
    serialized = BikeSerializer(queryset, many=True)#, context={'request': request})
    response = {
        'data': serialized.data
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
def getUser(request):
    user_id = request.query_params.get('user_id')
    queryset = User.objects.filter(userid=user_id)
    serialized = UserSerializer(queryset, many=True)#, context={'request': request})
    response = {
        'data': serialized.data
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

# ID of bike and location bike left at
# Delete old location if no linked bikes
@api_view(['POST'])
def returnBike(request):
    if request.method == 'POST':
        bike_id = request.query_params.get('bike_id')
        location = request.query_params.get('location')
        data=request.data
        bike = BikeSerializer(Bike.objects.filter(BikeID=bike_id))


        queryset = Address.objects.filter(Line1=location)
        if not queryset:
            Address.objects.update_or_create(Line1=location)

        queryset = Address.objects.get(Line1=location)
        serialized = AddressSerializer(queryset, many=False)
        Bike.objects.filter(BikeID=bike_id).update(AddressLocationID=serialized.data["location_id"])


        response = {
            "Status":"OK!!!!!!!",
            "request": serialized.data["location_id"]
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