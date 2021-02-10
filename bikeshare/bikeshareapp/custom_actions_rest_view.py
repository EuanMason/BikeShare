import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bikeshareapp.models import Wallet, Address, Bike, Trip, User
from bikeshareapp.rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, UserSerializer, UserLimitedSerializer

from util.decorators import auth_required, role_check
import json
from django.http import HttpResponse, JsonResponse

from django.db.models import Count


# The file rest_views.py is only to have the basic stuff
# Here we can add any other functionality that we need.
# NOTE:
#       * Always add the decorator @api_view and give a list of the allowed methods
#       * Remeber to add your url to url.py bikeshare/urls.py (it's not in this same folder)

#/* -------------------------------------------------------------------------- */
#/*                             General Actions                                */
#/* -------------------------------------------------------------------------- */
@api_view(['GET'])
@role_check(['operator', 'manager', 'user'])
def getAllBikes(request):

    # Changed to use the cookies instead of a parameter
    # userid = request.COOKIES['userid']
    # nickname = request.COOKIES['nickname']
    role = request.COOKIES['role']

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
@role_check(['operator', 'manager', 'user'])
def getAllBikesBasedOnLocation(request, location):

    # Changed to use the cookies instead of a parameter
    # userid = request.COOKIES['userid']
    # nickname = request.COOKIES['nickname']
    role = request.COOKIES['role']
    location = location.replace('+',' ')
    print(location)
    try:
        locations = Address.objects.filter(Line1=location)
        if len(locations) == 0:
            locations = Address.objects.filter(Postcode=location)
        if len(locations) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        locationObj = locations[0]
        print(locationObj.LocationID)
        if role == 'user':
            # For customer we only need the available bikes and not defective
            queryset = Bike.objects.filter(IsAvailable = 1, IsDefective = 0, AddressLocationID=locationObj.LocationID)
            serialized = BikeSerializer(queryset, many=True)
            data_to_return = serialized.data
        elif role == 'operator':
            # For operator we need to show the bikes that are available and 
            #   it does not matter if it is defective
            queryset = Bike.objects.filter(IsAvailable = 1, AddressLocationID=locationObj.LocationID)
            serialized = BikeSerializer(queryset, many=True)
            data_to_return = serialized.data
        elif role == 'manager':
            queryset = Bike.objects.filter(AddressLocationID=locationObj.LocationID)
            serialized = BikeSerializer(queryset, many=True)
            data_to_return = serialized.data
    
        response = {
            'data': data_to_return
        }
        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@role_check(['operator', 'manager', 'user'])
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
@role_check(['user'])
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
@role_check(['user'])
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
# Get all the defective bikes to an operator
@api_view(['GET'])
@role_check(['operator'])
def getAssignedBikes(request):

    userid = request.COOKIES['userid']
    # role = request.COOKIES['role']

    try:
        bikesFiltered = Bike.objects.filter(OperatorID=userid)
        serialized = BikeSerializer(bikesFiltered, many=True)
        data_to_return = serialized.data

        response = {
            'data': data_to_return
        }
        return Response(response, status=status.HTTP_200_OK)
    except:
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@role_check(['operator'])
def startRepairABike(request):
    print(request)
    try:
        if request.COOKIES :
            data = request.data
            if data:
                user_id = request.COOKIES['userid']
                bike_id = request_json['bike_id']

                bikes = Bike.objects.filter(BikeID=bikeID)
                user = User.objects.get(userid=operatorID)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                bikes=bikes[0]
                if bikes.IsDefective:
                    bikes.IsAvailable = 0
                    bikes.IsDefective = 0
                bikes.save()
            
                serialized = BikeSerializer(bikes,many=False)
                data_to_return = serialized.data
                response = {
                    'Data':  data_to_return
                }
    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@role_check(['operator'])
def getAssignedBikes(request):

    userid = request.COOKIES['userid']
    # role = request.COOKIES['role']

    try:
        bikesFiltered = Bike.objects.filter(OperatorID=userid)
        serialized = BikeSerializer(bikesFiltered, many=True)
        data_to_return = serialized.data

        response = {
            'data': data_to_return
        }
        return Response(response, status=status.HTTP_200_OK)
    except:
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@role_check(['operator'])
def endRepairABike(request):
    print(request)
    try:
        if request.COOKIES :
            data = request.data
            if data:
                user_id = request.COOKIES['userid']
                bike_id = request_json['bike_id']

                bikes = Bike.objects.filter(BikeID=bikeID)
                user = User.objects.get(userid=operatorID)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                bikes=bikes[0]
                if bikes.IsDefective:
                    bikes.IsAvailable = 1
                    bikes.IsDefective = 1
                    bikes.OperatorID = None
                bikes.save()
            
                serialized = BikeSerializer(bikes,many=False)
                data_to_return = serialized.data
                response = {
                    'Data':  data_to_return
                }
    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

            
#/* -------------------------------------------------------------------------- */
#/*                             Manager Actions                                */
#/* -------------------------------------------------------------------------- */
# Assign a defective bike to operator
@api_view(['POST'])
@role_check(['manager'])
def assignBikeToOperator(request):
    print(request)
    try:
        if request.data :
            request_json = request.data
            operatorID = request_json['operator_id']
            bikeID = request_json['bike_id']

            bikeFiltered = Bike.objects.filter(BikeID=bikeID)
            operatorUser = User.objects.get(userid=operatorID)
            if len(bikeFiltered) != 1:
                return  Response(status=status.HTTP_400_BAD_REQUEST)
    
            bikeFiltered = bikeFiltered[0]
            bikeFiltered.OperatorID = operatorUser
            bikeFiltered.IsDefective = 1
            bikeFiltered.save()

            serialized = BikeSerializer(bikeFiltered, many=False)
            #serialized.is_valid(raise_exception=True)
            #self.perform_update(serializer)
            data_to_return = serialized.data
    
            response = {
                'data': data_to_return
            }

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@role_check(['manager'])
def getAllOperators(request):

    try:
        # SELECT 
        #   USERID,
        #   NICKNAME
        # FROM USERS
        # LEFT JOIN BIKES
        # ON USERID = OPERATORID
        # WHERE ROLE='OPERATOR'
        # GROUP BY USERID
        result = User.objects.filter(role='operator').values('userid','nickname').annotate(bikes=Count('OperatorID'))    
        response = {
            'data': result
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        # print("----------------------********************")
        # print(e)
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


