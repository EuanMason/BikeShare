import requests
from django.db.models.functions import datetime
from django.utils import timezone
import dateutil.parser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bikeshareapp.models import Wallet, Address, Bike, Trip, User, Repairs
from bikeshareapp.rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, UserSerializer, UserLimitedSerializer, RepairsSerializer

from util.decorators import auth_required, role_check
import json
from django.http import HttpResponse, JsonResponse

from django.db.models import Count
from django.db.models import F



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
def recalculateMoney(request):
    try:
        if request.data :
            request_json = request.data
            amountToCharge = request_json['amount']
            userid = request.COOKIES['userid']

            currentUser = User.objects.get(userid=userid)
            currentWallet = Wallet.objects.get(WalletID=currentUser.WalletID.WalletID)
            if not currentWallet:
                return  Response(status=status.HTTP_404_NOT_FOUND)
    
            currenCredit = 0
            if currentWallet.Credit < 0 or currentWallet.Credit == None:
                currenCredit = 0
            else:
                currenCredit = currentWallet.Credit

            if currenCredit + amountToCharge < 0:
                return Response(status=status.HTTP_409_CONFLICT)
            
            currentWallet.Credit = currenCredit + amountToCharge
            currentWallet.save()

            serialized = WalletSerializer(currentWallet, many=False)
            data_to_return = serialized.data

            response = {
                'data': data_to_return
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

# TODO ID of bike and location bike left at
# TODO  Delete old location if no linked bikes?

@api_view(['POST'])
@role_check(['user'])
def returnBike(request):
    if request.method == 'POST':
        bike_id = request.query_params.get('bike_id')
        location = request.query_params.get('location')
        user_id = request.COOKIES['userid']

        trip = Trip.objects.filter(BikeID=bike_id, Cost=0.0)
        serialized_trip = TripSerializer(Trip.objects.get(BikeID=bike_id, Cost=0.0))
        town = ""
        postcode = ""

        queryset = Address.objects.filter(Line1=location)
        if not queryset:
            address = location.replace(" ", "+")
            api_key = "AIzaSyD0SRiJJupEmCVUyh-WnilaPP00dcgBb_c"
            url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
            result = requests.get(url).json()
            for i in result['results'][0]["address_components"]:
                if "postal_town" in i["types"]:
                    town = i["long_name"]

            for i in result['results'][0]["address_components"]:
                if "postal_code" in i["types"]:
                    postcode = i["long_name"]

            lat = result['results'][0]["geometry"]["location"]["lat"]
            long = result['results'][0]["geometry"]["location"]["lng"]

            Address.objects.update_or_create(Line1=location, City=town, Postcode=postcode, Longitude=long, Latitude=lat)

        queryset = Address.objects.get(Line1=location)

        serialized = AddressSerializer(queryset, many=False)

        rent = Bike.objects.get(BikeID=bike_id).Rent
        end_time = timezone.now().replace(tzinfo=None)
        cost = end_time - dateutil.parser.parse(serialized_trip.data["start_time"])
        cost = cost.total_seconds()/3600
        cost = cost * rent
        if cost < (rent/6):
            cost = rent/6
        Bike.objects.filter(BikeID=bike_id).update(AddressLocationID=serialized.data["location_id"], IsAvailable=1)
        trip.update(EndTime=end_time, EndAddress=serialized.data["location_id"], Cost=cost)

        response = {
            "Status" : "OK!!!!!!!",
            "request": serialized_trip.data
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
        #bikesFiltered = Bike.objects.filter(OperatorID=userid)
        repairFiltered = Repairs.objects.filter(AssignedOperator=userid)
        serialized = RepairsSerializer(repairFiltered, many=True)
        data_to_return = serialized.data

        response = {
            'data': data_to_return
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        #print("----------------------********************")
        #print(e)
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
    # print(request)
    try:
        if request.data :
            request_json = request.data
            bikeID = request_json['bike_id']
            operatorID = request_json['operator_id']
            report = request_json['report']

            bikeFiltered = Bike.objects.filter(BikeID=bikeID)
            operatorUser = User.objects.get(userid=operatorID)
            reportUser = User.objects.get(userid=report['report_user'])
            if len(bikeFiltered) != 1:
                return  Response(status=status.HTTP_400_BAD_REQUEST)

            bikeFiltered = bikeFiltered[0]
            
            # Create the object if not exists
            repair, created = Repairs.objects.get_or_create(
                BikeID = bikeFiltered.BikeID,
                ReportedUser = reportUser,
                Issue = report['issue'],
                AssignedOperator = operatorUser,
                InProgress = 1
            )

            bikeFiltered.IsDefective = 1
            bikeFiltered.save()

            serialized = RepairsSerializer(repair, many=False)
            data_to_return = serialized.data

            response = {
                'data': data_to_return
            }

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        #print("----------------------********************")
        #print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@role_check(['manager'])
def getAllOperators(request):

    try:
        #result = User.objects.filter(role='operator').values('userid','nickname').annotate(bikes=Count('OperatorID'))    
        result = (Repairs.objects.filter(InProgress=0).values('AssignedOperator','AssignedOperator__nickname')
            .annotate(
                op_id=F('AssignedOperator'),
                op_name=F('AssignedOperator__nickname'),
                bikes=Count('BikeID'))
            .values('op_id', 'op_name', 'bikes')) 
        #print(result)
        response = {
            'data': result
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        # print("----------------------********************")
        # print(e)
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)