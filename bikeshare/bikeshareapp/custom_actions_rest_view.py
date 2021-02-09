import requests
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

    # Changed to use the cookies instead of a parameter
    # userid = request.COOKIES['userid']
    # nickname = request.COOKIES['nickname']
    role = request.COOKIES['role']

    print(request.COOKIES)

    if role == 'user':
        # For customer we only need the available bikes and not defective
        queryset = Bike.objects.filter(IsAvailable = 1, IsDefective = 0)
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    elif role == 'operator':
        # For operator we need to show the bikes that are available and 
        #   it does not matter if it is defective
        queryset = Bike.objects.filter(IsAvailable = 1)
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    elif role == 'manager':
        queryset = Bike.objects.all()
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    
    response = {
        'data': data_to_return
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAvailableLocationsOfBikes(request):
    locations_to_return = {}

    queryset = Address.objects.all()
    serialized = AddressSerializer(queryset, many=True)
    locations_to_return = serialized.data

    response = {
        'location': locations_to_return
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

@api_view(['GET'])
def getLocation(request):
    if 'address' in request.GET:
        address = request.GET['address']
        api_key = "AIzaSyD0SRiJJupEmCVUyh-WnilaPP00dcgBb_c"
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)

        result = requests.get(url).json()
        response = {
            'data': result['results'][0]["geometry"]["location"]
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

# TODO ID of bike and location bike left at
# TODO  Delete old location if no linked bikes?

@api_view(['POST'])
def returnBike(request):
    if request.method == 'POST':
        bike_id = request.query_params.get('bike_id')
        location = request.query_params.get('location')

        trip = Trip.objects.first.filter(BikeID=bike_id, EndTime="")

        queryset = Address.objects.filter(Line1=location)
        if not queryset:
            address = location.replace(" ", "+")
            api_key = "AIzaSyD0SRiJJupEmCVUyh-WnilaPP00dcgBb_c"
            url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
            result = requests.get(url).json()
            town = result['results'][0]["address_components"][0]["long_name"]
            postcode = result['results'][0]["address_components"][4]["long_name"]
            lat = result['results'][0]["geometry"]["location"]["lat"]
            long = result['results'][0]["geometry"]["location"]["lng"]

            Address.objects.update_or_create(Line1=location, City=town, Postcode= postcode,Longitude=lat, Latitude=long)

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