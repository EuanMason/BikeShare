# Import Rest modules to manage responses and requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import of models and serializers
from bikeshareapp.models import Wallet, Address, Bike, Trip, User, Repairs, Movement
from bikeshareapp.rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, UserSerializer, UserLimitedSerializer, RepairsSerializer, MovementSerializer

# Import Django modules that are used in the code
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.models import Avg
from django.db.models.functions import datetime
from django.utils import timezone

# Import other modules used inside this code
from util.decorators import auth_required, role_check
import json
import requests
import dateutil.parser

# The main popurse of this script is to add most of the functionality of the system

#/* -------------------------------------------------------------------------- */
#/*                             General Actions                                */
#/* -------------------------------------------------------------------------- */
@api_view(['GET'])
@role_check(['operator', 'manager', 'user'])
def getAllBikes(request):
    """ Get all the bikes possibles depending on the role of each user

    Args:
        request (Request): The request that comes with the call of this method

    Returns:
        response (Response): The response containing the bikes' information in form of a list
    """
    # Get the role of the user
    role = request.COOKIES['role']

    # Depending on the role it will be a different query
    # Always call the serializer to retrieve the data in JSON format
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
        # Manager gets all the bikes
        queryset = Bike.objects.all()
        serialized = BikeSerializer(queryset, many=True)
        data_to_return = serialized.data
    
    response = {
        'data': data_to_return
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['operator', 'manager'])
def trackBikes(request):
    """ Retrieves the information of all the bikes inisde the DB

    Args:
        request (Request): The request that comes with the call of this method

    Returns:
        response (Response): The response containing the list of bikes with all their information
    """

    # Create the query using all to select without filters
    queryset = Bike.objects.all()
    serialized = BikeSerializer(queryset, many=True)
    # Serialized the data to be retrieved
    data_to_return = serialized.data
    response = {
        'data': data_to_return
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['operator', 'manager', 'user'])
def getAllBikesBasedOnLocation(request, location):
    """ Retrieves the information of all the bikes in a specific location

    Args:
        request (Request): The request that comes with the call of this method
        location (string): The address or location to look for

    Returns:
        response (Response): The response containing the list of bikes with all their information
    """

    role = request.COOKIES['role']
    # Change plus signs with spaces in case needed
    location = location.replace('+',' ').upper()
    try:
        # Try to get the location using the line 1
        locations = Address.objects.filter(Line1=location) 
        if len(locations) == 0:
            # If line 1 does not work use postcode
            locations = Address.objects.filter(Postcode=location)
        if len(locations) == 0:
            # If postcode does not work retrieve an error
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Since filter method was used, which means a list is returned, select only the first element (it should be of length 1)
        locationObj = locations[0]

        # Depending on the role it will be a different query
        # Always call the serializer to retrieve the data in JSON format
        if role == 'user':
            # For customer we only need the available bikes and not defective
            queryset = Bike.objects.filter(IsAvailable = 1, IsDefective = 0, AddressLocationID=locationObj.LocationID)
            serialized = BikeSerializer(queryset, many=True)
            data_to_return = serialized.data
            serialized_loc = AddressSerializer(locationObj, many=False)
            data_loc = serialized_loc.data
        elif role == 'operator':
            # For operator we need to show the bikes that are available and 
            #   it does not matter if it is defective
            queryset = Bike.objects.filter(IsAvailable = 1, AddressLocationID=locationObj.LocationID)
            serialized = BikeSerializer(queryset, many=True)
            data_to_return = serialized.data
            # Add the repair report for each bike that is not available
            for d in data_to_return:
                repairFiltered = Repairs.objects.filter(BikeID=d['bike_id'], InProgress__in=[0,1])
                serialized_repairs = RepairsSerializer(repairFiltered, many=True)
                data_repairs = serialized_repairs.data
                d['reports'] = data_repairs
            serialized_loc = AddressSerializer(locationObj, many=False)
            data_loc = serialized_loc.data
        elif role == 'manager':
            # For manager retrieve all the bikes in the location
            queryset = Bike.objects.filter(AddressLocationID=locationObj.LocationID)
            serialized = BikeSerializer(queryset, many=True)
            data_to_return = serialized.data
            serialized_loc = AddressSerializer(locationObj, many=False)
            data_loc = serialized_loc.data
    
        response = {
            'data': {'bikes':data_to_return, 'loc': data_loc}
        }
        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        # print("----------------------********************")
        # print(e)
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@role_check(['operator', 'manager', 'user'])
def getAvailableLocationsOfBikes(request):
    """ Retrieves the information of all the location with a bike

    Args:
        request (Request): The request that comes with the call of this method

    Returns:
        response (Response): The response containing the list of locations with all their information
    """

    locations_to_return = {}

    # get the bikes to know their location
    bike_address = Bike.objects.filter(IsAvailable=1).values('AddressLocationID_id')
    list_bike_address = list(bike_address)
    # Iterates over the result to create a list of IDs and then remove duplicates if needed 
    list_id_address = []
    for ba in bike_address:
        list_id_address += list(ba.values())
    # Use a set to remove duplicates
    list_id_address = list(set(list_id_address))

    # return addresses based on the locations id
    queryset = Address.objects.filter(LocationID__in=list_id_address)
    serialized = AddressSerializer(queryset, many=True)
    # Seriale the result to be in JSON format
    locations_to_return = serialized.data

    response = {
        'location': locations_to_return
    }
    return Response(response, status=status.HTTP_200_OK)

""" @api_view(['GET'])
def getUser(request):
    
    user_id = request.query_params.get('user_id')
    queryset = User.objects.filter(userid=user_id)
    serialized = UserSerializer(queryset, many=True)#, context={'request': request})
    response = {
        'data': serialized.data
    }
    return Response(response, status=status.HTTP_200_OK) """

@api_view(['GET'])
@role_check(['user'])
def getWallet(request):
    """ Retrieves the information of a user's wallet

    Args:
        request (Request): The request that comes with the call of this method

    Returns:
        response (Response): The response containing the wallet information
    """

    # Ge the User object from models
    user_id = request.COOKIES['userid']
    queryset = User.objects.get(userid=user_id)
    serialized = UserSerializer(queryset, many=False)

    try:
        # If wallet ID hasn't been assigned
        if serialized.data["wallet_id"] == 0 or serialized.data["wallet_id"] is None:
            #Create new wallet
            wallet = Wallet.objects.create(Credit=0.0)
            #Connect user to wallet
            User.objects.filter(userid=user_id).update(WalletID=wallet.WalletID)
            queryset = User.objects.get(userid=user_id)
    except ValueError:
        return  Response(status=status.HTTP_404_NOT_FOUND)

    serialized = UserSerializer(queryset, many=False)

    response = {
        'data': serialized.data["wallet_id"]
    }
    return Response(response, status=status.HTTP_200_OK)

""" @api_view(['GET'])
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
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) """

#/* -------------------------------------------------------------------------- */
#/*                            Customer Actions                                */
#/* -------------------------------------------------------------------------- */
@api_view(['POST'])
@role_check(['user'])
def recalculateMoney(request):
    """ Recalculates user's balance on wallet

    Args:
        request (Request): The request that comes with the call of this method

    Returns:
        response (Response): The response containing the wallet information
    """

    try:
        if request.data:
            request_json = request.data
            # Get the amount to be charged and the user id from the request
            amountToCharge = request_json['amount']
            userid = request.COOKIES['userid']

            # Get the user object
            currentUser = User.objects.get(userid=userid)
            # Get the wallet of the user
            currentWallet = Wallet.objects.get(WalletID=currentUser.WalletID.WalletID)
            # In case the wallet is not found
            if not currentWallet:
                return  Response(status=status.HTTP_404_NOT_FOUND)
    
            # Set credit from the wallet
            currenCredit = 0
            currenCredit = currentWallet.Credit
            
            # Change the value of the wallet based on the amount 
            currentWallet.Credit = round(float(currenCredit) + float(amountToCharge),2)
            currentWallet.save()

            # Serialize the result to be returned in a JSON format
            serialized = WalletSerializer(currentWallet, many=False)
            data_to_return = serialized.data

            response = {
                'data': data_to_return
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def returnBike(request):
    """ Recalculates user's balance on wallet. 
        This method is capable of create new location in case needed.

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the id of the bike (bike_id)
            * the location that should be the postcode (location)
            * the id of the trip that is finishing (trio_id)
    Returns:
        response (Response): The response containing the wallet information
    """

    if request.method == 'POST':
        # Get the values from the request (bikeid, location, trip and userid)
        bike_id = request.data['bike_id']
        location = request.data['location'].replace(" ","").upper()
        trip_id = request.data['trip_id']
        user_id = request.COOKIES['userid']

        # Get the trip
        try:
            trip = Trip.objects.filter(TripID=trip_id, BikeID=bike_id, Cost=0.0)
            serialized_trip = TripSerializer(Trip.objects.get(TripID=trip_id,BikeID=bike_id, Cost=0.0))
        except ObjectDoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Set variables town and postcode as empty at first
        town = ""
        postcode = ""

        # Try to get the location based on the location using line 1 or postcode
        queryset = Address.objects.filter(Line1=location) | Address.objects.filter(Postcode=location)
        if not queryset:
            # If the result is empty the create a new location using google maps api
            address = location.replace(" ", "+")
            api_key = ""
            url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
            result = requests.get(url).json()
            # Check if the result is not empty
            if(len(result['results']) > 0):
                # Get the components of the location to create an Address object on DB
                # Get the town
                for i in result['results'][0]["address_components"]:
                    if "postal_town" in i["types"]:
                        town = i["long_name"]

                # Get the postcode
                for i in result['results'][0]["address_components"]:
                    if "postal_code" in i["types"]:
                        postcode = i["long_name"]
                        postcode = postcode.replace(" ","")
                line1 = location

                # Get the longitude and latitude
                for i in result['results'][0]["address_components"]:
                    if "route" in i["types"]:
                        if line1 == location:
                            line1 = ""
                        line1 += i["long_name"] + " "
                    if "sublocality" in i["types"]:
                        if line1 == location:
                            line1 = ""
                        line1 += i["long_name"]

                # Set it in a format we can use
                lat = result['results'][0]["geometry"]["location"]["lat"]
                long = result['results'][0]["geometry"]["location"]["lng"]
                # Save the Address object on DB
                Address.objects.update_or_create(Line1=line1, City=town, Postcode=postcode, Longitude=long, Latitude=lat)
            else:
                # If not result found
                return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the location 
        try:
            queryset = Address.objects.get(Line1=location) 
        except:
            queryset = Address.objects.get(Postcode=location)
        serialized = AddressSerializer(queryset, many=False)

        # Update bike and retrieve the cost
        rent = Bike.objects.get(BikeID=bike_id).Rent
        end_time = timezone.now().replace(tzinfo=None)
        cost = end_time - dateutil.parser.parse(serialized_trip.data["start_time"])
        # Calculate the cost
        cost = cost.total_seconds()/3600
        cost = cost * rent
        # If the cost is less than 1 sixth of the then set the cost as it 
        if cost < (rent/6):
            cost = rent/6
        Bike.objects.filter(BikeID=bike_id).update(AddressLocationID=serialized.data["location_id"], IsAvailable=1)
        # Update the trip
        trip.update(EndTime=end_time, EndAddress=serialized.data["location_id"], Cost=cost)
        # Serialze the trip and return it 
        serialized_trip = TripSerializer(Trip.objects.get(TripID=trip_id, BikeID=bike_id, Cost=cost))

        response = {
            "status" : "OK",
            "data": serialized_trip.data
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#/* -------------------------------------------------------------------------- */
#/*                            Operator Actions                                */
#/* -------------------------------------------------------------------------- */
""" # Get all the defective bikes to an operator
@api_view(['GET'])
@role_check(['operator'])
def getAssignedBikes(request):

    userid = request.COOKIES['userid']

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
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR) """

@api_view(['POST'])
@role_check(['operator'])
def startRepairABike(request):
    """ Set the status of the bike as being repaired and create or change the corresponding reports

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the id of the bike (bike_id)
    Returns:
        response (Response): The response containing the bike information
    """
    try:
        if request.COOKIES :
            data = request.data
            if data:
                # Get the userd id and bike id from the request
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']

                # Get the bikes with the bike id (it should be just one)
                bikes = Bike.objects.filter(BikeID=bike_id)
                # user = User.objects.get(userid=operatorID)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                # Since filter method retrieves a list just get the first one (it should be just one result)
                bikes=bikes[0]
                # Set the status of the bike and save it on DB
                bikes.IsAvailable = 3
                bikes.IsDefective = 1
                bikes.save()

                currentUser = User.objects.get(userid=user_id)

                # Update or create reports
                Repairs.objects.filter(BikeID=bikes.BikeID).update_or_create(BikeID=bikes,InProgress=1,AssignedOperator=currentUser)

                # Serialize the data and return it 
                serialized = BikeSerializer(bikes,many=False)
                data_to_return = serialized.data
                response = {
                    'data':  data_to_return
                }

                return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@role_check(['operator'])
def endRepairABike(request):
    """ Set the status of the bike as available and change the corresponding reports

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the id of the bike (bike_id)
    Returns:
        response (Response): The response containing the bike information
    """
    try:
        if request.COOKIES :
            data = request.data
            if data:
                # Get the bike and user ID from request
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']

                # Get the bikes, it should be just one
                bikes = Bike.objects.filter(BikeID=bike_id)
                # In case there are multiple bike, which should not be the case
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                # Get just the first bike, it should be just one
                bikes=bikes[0]
                # Update the status of the bike and save it on DB
                bikes.IsAvailable = 1
                bikes.IsDefective = 0
                bikes.save()

                # Update reports --> -1 means is done
                Repairs.objects.filter(BikeID=bikes.BikeID).update(InProgress=-1)
            
                # Serialize the data and return it
                serialized = BikeSerializer(bikes,many=False)
                data_to_return = serialized.data
                response = {
                    'data':  data_to_return
                }
                return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@role_check(['operator'])
def moveBikeStart(request):
    """ Set the status of the bike as being moved and create or change the corresponding reports

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the id of the bike (bike_id)
            * the place where the bike will be probably left (place)
    Returns:
        response (Response): The response containing the bike information
    """
    try:
        if request.COOKIES :
            data = request.data
            if data:
                # Get the user id, bike id and place from the request
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']
                intented = data['place'].replace(' ','').upper()

                # Try to get the location based on the location using line 1 or postcode
                queryset = Address.objects.filter(Line1=intented) | Address.objects.filter(Postcode=intented)

                if not queryset:
                    # If the result is empty the create a new location using google maps api
                    address = intented.replace(" ", "+")
                    api_key = "AIzaSyD0SRiJJupEmCVUyh-WnilaPP00dcgBb_c"
                    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
                    result = requests.get(url).json()
                    # Check if the result is not empty
                    if(len(result['results']) > 0):
                        # Get the components of the location to create an Address object on DB
                        # Get the town
                        for i in result['results'][0]["address_components"]:
                            if "postal_town" in i["types"]:
                                town = i["long_name"]

                        # Get the postcode
                        for i in result['results'][0]["address_components"]:
                            if "postal_code" in i["types"]:
                                postcode = i["long_name"]
                                postcode = postcode.replace(" ","")
                        line1 = intented

                        # Get the longitude and latitude
                        for i in result['results'][0]["address_components"]:
                            if "route" in i["types"]:
                                if line1 == intented:
                                    line1 = ""
                                line1 += i["long_name"] + " "
                            if "sublocality" in i["types"]:
                                if line1 == intented:
                                    line1 = ""
                                line1 += i["long_name"]

                        # Set it in a format we can use
                        lat = result['results'][0]["geometry"]["location"]["lat"]
                        long = result['results'][0]["geometry"]["location"]["lng"]
                        # Save the Address object on DB
                        Address.objects.update_or_create(Line1=line1, City=town, Postcode=postcode, Longitude=long, Latitude=lat)
                    else:
                        # If not result found
                        return Response(status=status.HTTP_404_NOT_FOUND)

                # Get the location and check with line 1 and postcode
                locations = Address.objects.filter(Line1=intented)
                if len(locations) == 0:
                    # If line 1 does not work, use postcode
                    locations = Address.objects.filter(Postcode=intented)
                if len(locations) == 0:
                    # If that location is not found then 404
                    return Response(status=status.HTTP_404_NOT_FOUND)

                # Get the inteded location from the list
                intented_location = locations[0]
                # Get the bike as well
                bikes = Bike.objects.filter(BikeID=bike_id)
                # And also get the user
                user = User.objects.get(userid=user_id)
                if len(bikes)!=1:
                    # In case there is more than 1 bike, which should not be the case
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                # Get the bike from the list
                bikes=bikes[0]
                # Update the statud of the bike and save it on the db
                bikes.IsAvailable = 2
                bikes.AddressLocationID = intented_location
                bikes.save()

                # Save new move on DB
                move = Movement(
                    ProposedLocation=intented_location, 
                    BikeID=bikes,
                    MoveOperator=user,
                    InProgress = 1
                )
                move.save()

                # Serialize the data to be returned in a JSON format
                serialized = BikeSerializer(bikes,many=False)
                data_to_return = serialized.data
                response = {
                    'data':  data_to_return
                }
                return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@role_check(['operator'])
def moveBikeEnd(request):
    """ Set the status of the bike as being available and create or change the corresponding reports

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the id of the bike (bike_id)
            * the place where the bike will be left (place)
    Returns:
        response (Response): The response containing the bike information
    """
    try:
        if request.COOKIES :
            data = request.data
            if data:
                # Get the user id, bike id and place from the request
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']
                intented = data['place'].replace(' ','').upper()

                # Try to get the location based on the location using line 1 or postcode
                queryset = Address.objects.filter(Line1=intented) | Address.objects.filter(Postcode=intented)

                if not queryset:
                    # If the result is empty the create a new location using google maps api
                    address = intented.replace(" ", "+")
                    api_key = "AIzaSyD0SRiJJupEmCVUyh-WnilaPP00dcgBb_c"
                    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, api_key)
                    result = requests.get(url).json()
                    # Check if the result is not empty
                    if(len(result['results']) > 0):
                        # Get the components of the location to create an Address object on DB
                        # Get the town
                        for i in result['results'][0]["address_components"]:
                            if "postal_town" in i["types"]:
                                town = i["long_name"]

                        # Get the postcode
                        for i in result['results'][0]["address_components"]:
                            if "postal_code" in i["types"]:
                                postcode = i["long_name"]
                                postcode = postcode.replace(" ","")
                        line1 = intented

                        # Get the longitude and latitude
                        for i in result['results'][0]["address_components"]:
                            if "route" in i["types"]:
                                if line1 == intented:
                                    line1 = ""
                                line1 += i["long_name"] + " "
                            if "sublocality" in i["types"]:
                                if line1 == intented:
                                    line1 = ""
                                line1 += i["long_name"]

                        # Set it in a format we can use
                        lat = result['results'][0]["geometry"]["location"]["lat"]
                        long = result['results'][0]["geometry"]["location"]["lng"]
                        # Save the Address object on DB
                        Address.objects.update_or_create(Line1=line1, City=town, Postcode=postcode, Longitude=long, Latitude=lat)
                    else:
                        # If not result found
                        return Response(status=status.HTTP_404_NOT_FOUND)

                # Get the location and check with line 1 and postcode
                locations = Address.objects.filter(Line1=intented)
                if len(locations) == 0:
                    # If line 1 does not work, use postcode
                    locations = Address.objects.filter(Postcode=intented)
                if len(locations) == 0:
                    # If that location is not found then 404
                    return Response(status=status.HTTP_404_NOT_FOUND)

                # Get the inteded location from the list
                intented_location = locations[0]
                # Get the bike as too
                bikes = Bike.objects.filter(BikeID=bike_id)
                if len(bikes)!=1:
                    # In case there is more than 1 bike, which should not be the case
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                # Get the bike from the list
                bikes=bikes[0]
                # Update the statud of the bike and save it on the db
                bikes.IsAvailable = 1
                bikes.AddressLocationID = intented_location
                bikes.save()

                # Update move report on DB
                Movement.objects.filter(MoveOperator=user_id, BikeID=bike_id, InProgress=1).update(InProgress=-1)
            
                # Serialize the data to be returned in a JSON format
                serialized = BikeSerializer(bikes,many=False)
                data_to_return = serialized.data
                response = {
                    'data':  data_to_return
                }
                return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@role_check(['operator'])
def getPendingAcctions(request):
    """ Retrives all the pending (on going) actions of an operator

    Args:
        request (Request): The request that comes with the call of this method. 

    Returns:
        response (Response): The response containing the the information of the repairs and movenment that are on going.
    """
    try:
        # Get the user id and the role from the requests cookies
        user_id = request.COOKIES['userid']
        role = request.COOKIES['role']
        
        # Get the Pending repairments
        repairFiltered = Repairs.objects.filter(AssignedOperator=user_id, InProgress=1)
        serialized_repairs = RepairsSerializer(repairFiltered, many=True)
        data_repairs = serialized_repairs.data

        # Get the pending movements
        movesFiltered = Movement.objects.filter(MoveOperator=user_id,InProgress=1)
        serialized_movs = MovementSerializer(movesFiltered, many=True)
        # Serialze the data to be returned in a JSON format
        data_movs = serialized_movs.data

        # Filter to return only the bikes from the repairs IDs since the DB returns a nested dictionary
        bikes_dic = {}
        for b in data_repairs:
            bikes_dic[b['bike_id']['bike_id']] = b['bike_id']

        d_rep_bikes = bikes_dic.values()

        response = {
            'repairs':  d_rep_bikes,
            'movs': data_movs
        }

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        print("----------------------********************")
        print(e)
        return  Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#/* -------------------------------------------------------------------------- */
#/*                             Manager Actions                                */
#/* -------------------------------------------------------------------------- */
""" # Assign a defective bike to operator
@api_view(['POST'])
@role_check(['manager'])
def assignBikeToOperator(request):
    # print(request)
    try:
        if request.data:
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
                InProgress = 0
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
        return  Response(status=status.HTTP_400_BAD_REQUEST) """

""" @api_view(['GET'])
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
 """
@api_view(['GET'])
@role_check(['manager'])
def trips_in_daterange(request):
    """ Retrieves the trips information for the manager report between two dates. 

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the start date of the report (start_date)
            * the end date of the report (end_date)

    Returns:
        response (Response): The response containing the information for the report. This includes:
        * A list with all the information of the trips
    """
    # Get the start and end date from request and parse them to dateutil python object
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])
        
        # Get the trips based on the dates range
        queryset = Trip.objects.filter(Date__range=(start_date, end_date))
    except KeyError:
        queryset = Trip.objects.all()

    # Serialize and retrive the trips
    serialized = TripSerializer(queryset, many=True)
    data_to_return = serialized.data
    response = {
        'data': data_to_return

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def total_income(request):
    """ Retrieves the total income for the manager report between two dates. 

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the start date of the report (start_date)
            * the end date of the report (end_date)

    Returns:
        response (Response): The response containing the information for the report. This includes:
        * The total income
    """

    # Get the start and end date from request and parse them to dateutil python object
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        # Get the trips based on the dates range and group them to sum to cost
        queryset = Trip.objects.filter(Date__range=(start_date, end_date)).aggregate(Sum('Cost'))
    except KeyError:
        queryset = Trip.objects.all()

    # Serialize and retrive the trips
    response = {
        'data': [queryset['Cost__sum']]

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def trip_count(request):
    """ Retrieves the amount of trips for the manager report between two dates. 

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the start date of the report (start_date)
            * the end date of the report (end_date)

    Returns:
        response (Response): The response containing the information for the report. This includes:
        * The amount of trips
    """
    try:
        # Get the start and end date from request and parse them to dateutil python object
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        # Get the trips based on the dates range and group them count them
        queryset = Trip.objects.filter(Date__range=(start_date, end_date)).count()
    except KeyError:
        queryset = Trip.objects.all().count()

    # Serialize and retrive the trips
    response = {
        'data': [queryset]
    }

    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def most_common_locations(request):
    """ Retrieves the most common location for start and end trips for the manager report  between two dates. 

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the start date of the report (start_date)
            * the end date of the report (end_date)

    Returns:
        response (Response): The response containing the information for the report. This includes:
        * Common start
        * Common end
    """

    # Get the start and end date from request and parse them to dateutil python object
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        # Get the trips based on the dates range 
        queryset = Trip.objects.filter(Date__range=(start_date, end_date))
    except KeyError:
        queryset = Trip.objects.all()

    # Initialize the dictionaries for end and start location. Location will be the key and count will be the values
    endcount = {}
    startcount = {}

    # Iterate over the queryset result to count the times a location repeats
    for trips in queryset:
        try:
            # Try to sum directly on the dictionary, if exists it will sum up, if not it will raise and KeyError exception
            endcount[trips.EndAddress_id] += 1
            startcount[trips.StartAddress_id] += 1
        except KeyError:
            # If raise the error add a new value to the dictionary
            endcount.update({trips.EndAddress_id: 1})
            startcount.update({trips.StartAddress_id: 1})

    # Get the max from the dictionaries to get the most popular start and end
    max_start = max(startcount, key=startcount.get)
    max_end = max(endcount, key=endcount.get)
    
    # Get the location start based on the result from the max operation
    common_start_query = Address.objects.get(LocationID=max_start)
    common_start = AddressSerializer(common_start_query, many=False).data

    # Get the location end based on the result from the max operation
    common_end_query = Address.objects.get(LocationID=max_end)
    common_end = AddressSerializer(common_end_query, many=False).data

    # Format the result and retrieve it
    data = {'most_common_start': common_start,
            'most_common_end': common_end}
    response = {
        'data': data

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def report_data(request):
    """ Retrieves all the extra needed data to create the report for the manager  between two dates. 

    Args:
        request (Request): The request that comes with the call of this method. This will contains the followning
            * the start date of the report (start_date)
            * the end date of the report (end_date)
    Returns:
        response (Response): The response containing the information for the report. This includes:
        * Trips per day
        * Income per day
        * Movements per day
        * Which bikes are being moved
        * Count of movements of bikes
        * Which bikes are being repaired
        * Trips per bike
        * Average income per bike
        * Amount of repairs per operator
        * Amount of movements per operator
        * Most popular bike
        * Most profitable bike
        * Operator with most repairs
        * Operator with most movements 
    """
    try:
        # Get the start and end date from request and parse them to dateutil python object
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        # Query to get the trips count per day
        queryset_trip_count = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(date_start=TruncDate('StartTime'))
            .order_by('date_start')
            .values('date_start')
            .annotate(total=Count('StartTime')))

        # Query to get the trips count per bike
        queryset_trip_count_bike = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(bike=F('BikeID__BikeID'))
            .values('bike')
            .annotate(total=Count('BikeID'))
            .order_by('-total')
        )

        # Query to get the income per day
        queryset_income_day = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(date_start=TruncDate('StartTime'))
            .order_by('date_start')
            .values('date_start')
            .annotate(total=Sum('Cost')))

        # Query to get the average income per bike
        queryset_income_day_avg = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(bike=F('BikeID__BikeID'))
            .values('bike')
            .annotate(total=Avg('Cost'))
            .order_by('-total')
        )

        # Query to get the count of reports per bike
        queryset_cnt_rep = (
            Repairs.objects.all()
                .annotate(bike=F('BikeID__BikeID'))
                .values('bike')
                .order_by('bike')
                .annotate(Count('bike'))
        )

        # Query to get the count movements of bikes
        queryset_cnt_mov = (
            Movement.objects.all()
                .annotate(bike=F('BikeID__BikeID'))
                .values('bike')
                .order_by('bike')
                .annotate(Count('bike'))
        )

        # Query to get the count reports per operator
        queryset_cnt_repairs_op = (
            Repairs.objects
                .filter(AssignedOperator__isnull=False)
                .annotate(opera=F('AssignedOperator__userid'))
                .values('opera')
                .annotate(counts=Count('opera'))
                .order_by('-counts')
        )

        # Query to get the count the movements per operator
        queryset_cnt_mov_op = (
            Movement.objects.all()
                .annotate(opera=F('MoveOperator__userid'))
                .values('opera')
                .annotate(counts=Count('opera'))
                .order_by('-counts')
        )

        # How many bikes are moving?
        queryset_bikes_moving = Bike.objects.filter(IsAvailable=2)

        # How many bikes are repairing
        queryset_bikes_repair = Bike.objects.filter(IsAvailable=3)

        # How many bikes were repaired?
        queryset_bikes_moved = Repairs.objects.filter(InProgress=-1)

        # How many bikes were moved?
        queryset_bikes_repaired = Movement.objects.filter(InProgress=-1)

        # Serialize the results
        bikes_moving_ser = BikeSerializer(queryset_bikes_moving, many=True).data
        bikes_repair_ser = BikeSerializer(queryset_bikes_repair, many=True).data

        # If the length of some queries is zero then return none else get the first element to get different metrics
        # Most popular bike
        popular_bike = queryset_trip_count_bike[0] if len(queryset_trip_count_bike) > 0 else None
        # Most profitable bike
        profit_bike = queryset_income_day_avg[0] if len(queryset_income_day_avg) > 0 else None
        # Operator with most repairs done
        opera_most_repa = queryset_cnt_repairs_op[0] if len(queryset_cnt_repairs_op) > 0 else None
        # Operator with most movements done
        opera_most_movs = queryset_cnt_mov_op[0] if len(queryset_cnt_mov_op) > 0 else None

        # Retrieve the information in JSON format
        response = {
            "trip_count_per_day": list(queryset_trip_count),
            "income_per_day": list(queryset_income_day),
            "reports_per_bike": list(queryset_cnt_rep),
            "movs_per_bike": list(queryset_cnt_mov),
            "moving_bikes": bikes_moving_ser,
            "cnt_moving_bikes": len(queryset_bikes_moved),
            "repairing_bikes": bikes_repair_ser,
            "cnt_repair_bikes": len(queryset_bikes_repaired),
            "trip_per_bikes": list(queryset_trip_count_bike),
            "average_income_per_bike": list(queryset_income_day_avg),
            "repairs_per_operator": list(queryset_cnt_repairs_op),
            "movs_per_operator": list(queryset_cnt_mov_op),
            "popular_bike": popular_bike,
            "profit_bike": profit_bike,
            "opera_most_repa": opera_most_repa,
            "opera_most_movs": opera_most_movs
        }

        return Response( response, status=status.HTTP_200_OK)

        
    except KeyError:
        queryset = Trip.objects.all()

    
