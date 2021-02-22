import requests
from django.db.models.functions import datetime
from django.utils import timezone
import dateutil.parser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from bikeshareapp.models import Wallet, Address, Bike, Trip, User, Repairs, Movement
from bikeshareapp.rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, UserSerializer, UserLimitedSerializer, RepairsSerializer, MovementSerializer

from util.decorators import auth_required, role_check
import json
from django.http import HttpResponse, JsonResponse

from django.db.models import Count
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from django.db.models.functions import TruncDate
from django.db.models import Avg


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
@role_check(['operator', 'manager'])
def trackBikes(request):
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
    try:
        locations = Address.objects.filter(Line1=location) 
        if len(locations) == 0:
            locations = Address.objects.filter(Postcode=location)
        if len(locations) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        locationObj = locations[0]
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
            for d in data_to_return:
                repairFiltered = Repairs.objects.filter(BikeID=d['bike_id'], InProgress__in=[0,1])
                serialized_repairs = RepairsSerializer(repairFiltered, many=True)
                data_repairs = serialized_repairs.data
                d['reports'] = data_repairs
            serialized_loc = AddressSerializer(locationObj, many=False)
            data_loc = serialized_loc.data

            

        elif role == 'manager':
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
@role_check(['user'])
def getWallet(request):

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
        "wallet already connected"

    serialized = UserSerializer(queryset, many=False)

    response = {
        'data': serialized.data["wallet_id"]
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
        if request.data:
            request_json = request.data
            amountToCharge = request_json['amount']
            userid = request.COOKIES['userid']

            currentUser = User.objects.get(userid=userid)
            currentWallet = Wallet.objects.get(WalletID=currentUser.WalletID.WalletID)
            if not currentWallet:
                return  Response(status=status.HTTP_404_NOT_FOUND)
    
            currenCredit = 0
            #if currentWallet.Credit < 0 or currentWallet.Credit == None:
            #    return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
            #else:
            currenCredit = currentWallet.Credit

            #if currenCredit + amountToCharge < 0:
            #    return Response(status=status.HTTP_409_CONFLICT)
            
            currentWallet.Credit = round(float(currenCredit) + float(amountToCharge),2)
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



@api_view(['POST'])
def returnBike(request):
    if request.method == 'POST':
        bike_id = request.data['bike_id']
        location = request.data['location'].replace(" ","")
        trip_id = request.data['trip_id']
        user_id = request.COOKIES['userid']
        try:
            trip = Trip.objects.filter(TripID=trip_id, BikeID=bike_id, Cost=0.0)
            serialized_trip = TripSerializer(Trip.objects.get(TripID=trip_id,BikeID=bike_id, Cost=0.0))
        except ObjectDoesNotExist as e:
            #print("----------------------********************")
            #print(e) 
            return Response(status=status.HTTP_404_NOT_FOUND)

        town = ""
        postcode = ""

        queryset = Address.objects.filter(Line1=location) | Address.objects.filter(Postcode=location)
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

        try:
            queryset = Address.objects.get(Line1=location) 
        except:
            queryset = Address.objects.get(Postcode=location)

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
        serialized_trip = TripSerializer(Trip.objects.get(BikeID=bike_id, Cost=cost))


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
    # print(request)
    try:
        if request.COOKIES :
            data = request.data
            if data:
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']

                bikes = Bike.objects.filter(BikeID=bike_id)
                # user = User.objects.get(userid=operatorID)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                bikes=bikes[0]
                #if bikes.IsDefective:
                bikes.IsAvailable = 3
                bikes.IsDefective = 1
                bikes.save()

                currentUser = User.objects.get(userid=user_id)

                # Update or create reports
                Repairs.objects.filter(BikeID=bikes.BikeID).update_or_create(BikeID=bikes,InProgress=1,AssignedOperator=currentUser)
                # Create the object if not exists
                #repair, created = Repairs.objects.get_or_create(
                #    BikeID = bikes.BikeID,
                #    ReportedUser = reportUser,
                #    Issue = report['issue'],
                #    AssignedOperator = operatorUser,
                #    InProgress = 0
                #)
            
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
    # print(request)
    try:
        if request.COOKIES :
            data = request.data
            if data:
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']

                bikes = Bike.objects.filter(BikeID=bike_id)
                # user = User.objects.get(userid=operatorID)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                bikes=bikes[0]
                #if bikes.IsDefective:
                bikes.IsAvailable = 1
                bikes.IsDefective = 0
                    # bikes.OperatorID = None
                bikes.save()

                # Update reports --> -1 means is done
                Repairs.objects.filter(BikeID=bikes.BikeID).update(InProgress=-1)
            
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
def moveBikeStart(request):
    try:
        if request.COOKIES :
            data = request.data
            if data:
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']
                intented = data['place']
                locations = Address.objects.filter(Line1=intented)
                if len(locations) == 0:
                    locations = Address.objects.filter(Postcode=intented)
                if len(locations) == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                intented_location = locations[0]
                bikes = Bike.objects.filter(BikeID=bike_id)
                user = User.objects.get(userid=user_id)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                bikes=bikes[0]
                bikes.IsAvailable = 2
                bikes.AddressLocationID = intented_location
                #Repairs.objects.filter(IsAvailable=bikes.BikeID).update(InProgress=-1)
                bikes.save()

                # Save new move
                move = Movement(
                    ProposedLocation=intented_location, 
                    BikeID=bikes,
                    MoveOperator=user,
                    InProgress = 1
                )
                move.save()
            
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
def moveBikeEnd(request):
    # print(request)
    try:
        if request.COOKIES :
            data = request.data
            if data:
                user_id = request.COOKIES['userid']
                bike_id = data['bike_id']
                intented = data['place']
                locations = Address.objects.filter(Line1=intented)
                if len(locations) == 0:
                    locations = Address.objects.filter(Postcode=intented)
                if len(locations) == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                intented_location = locations[0]
                bikes = Bike.objects.filter(BikeID=bike_id)
                # user = User.objects.get(userid=operatorID)
                if len(bikes)!=1:
                    return  Response(status=status.HTTP_400_BAD_REQUEST)

                bikes=bikes[0]
                #if bikes.IsDefective:
                bikes.IsAvailable = 1
                bikes.AddressLocationID = intented_location
                bikes.save()

                # Update move
                Movement.objects.filter(MoveOperator=user_id, BikeID=bike_id, InProgress=1).update(InProgress=-1)
            
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
    try:
        user_id = request.COOKIES['userid']
        role = request.COOKIES['role']
        
        # Get the Pending repairments
        repairFiltered = Repairs.objects.filter(AssignedOperator=user_id, InProgress=1)
        serialized_repairs = RepairsSerializer(repairFiltered, many=True)
        data_repairs = serialized_repairs.data

        # Get the pending movements
        movesFiltered = Movement.objects.filter(MoveOperator=user_id,InProgress=1)
        serialized_movs = MovementSerializer(movesFiltered, many=True)
        data_movs = serialized_movs.data

        # Filter to return only the bikes from the repairs
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
# Assign a defective bike to operator
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

@api_view(['GET'])
@role_check(['manager'])
def trips_in_daterange(request):
    # print(request.GET['start_date'])
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        queryset = Trip.objects.filter(Date__range=(start_date, end_date))
    except KeyError:
        queryset = Trip.objects.all()

    # print(queryset)
    serialized = TripSerializer(queryset, many=True)
    data_to_return = serialized.data
    response = {
        'data': data_to_return

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def total_income(request):
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        queryset = Trip.objects.filter(Date__range=(start_date, end_date)).aggregate(Sum('Cost'))
    except KeyError:
        queryset = Trip.objects.all()

    response = {
        'data': [queryset['Cost__sum']]

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def trip_count(request):

    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        queryset = Trip.objects.filter(Date__range=(start_date, end_date)).count()
    except KeyError:
        queryset = Trip.objects.all().count()
    response = {
        'data': [queryset]

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def most_common_locations(request):
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        queryset = Trip.objects.filter(Date__range=(start_date, end_date))
    except KeyError:
        queryset = Trip.objects.all()
    endcount = {}
    startcount = {}

    for trips in queryset:
        try:
            endcount[trips.EndAddress_id] += 1
            startcount[trips.StartAddress_id] += 1
        except KeyError:
            endcount.update({trips.EndAddress_id: 1})
            startcount.update({trips.StartAddress_id: 1})

    max_start = max(startcount, key=startcount.get)
    max_end = max(endcount, key=endcount.get)
    
    common_start_query = Address.objects.get(LocationID=max_start)
    common_start = AddressSerializer(common_start_query, many=False).data

    common_end_query = Address.objects.get(LocationID=max_end)
    common_end = AddressSerializer(common_end_query, many=False).data

    data = {'most_common_start': common_start,
            'most_common_end': common_end}
    response = {
        'data': data

    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_check(['manager'])
def report_data(request):
    try:
        start_date = dateutil.parser.parse(request.GET["start_date"])
        end_date = dateutil.parser.parse(request.GET["end_date"])

        # Transaction.objects.all().values('actor').annotate(total=Count('actor')).order_by('total')
        # User.objects.all()
        #     .filter(course='Course 1')
        #     .annotate(registered_date=TruncDate('registered_at'))
        #     .order_by('registered_date')
        #     .values('registered_date')
        #     .annotate(**{'total': Count('registered_at')})

        # Trip count per day
        queryset_trip_count = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(date_start=TruncDate('StartTime'))
            .order_by('date_start')
            .values('date_start')
            .annotate(total=Count('StartTime')))

        # Trip count per bike
        queryset_trip_count_bike = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(bike=F('BikeID__BikeID'))
            .values('bike')
            .annotate(total=Count('BikeID'))
            .order_by('-total')
        )

        # Income per day
        queryset_income_day = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(date_start=TruncDate('StartTime'))
            .order_by('date_start')
            .values('date_start')
            .annotate(total=Sum('Cost')))

        # Income per bike avg
        queryset_income_day_avg = (Trip.objects.all()
            .filter(Date__range=(start_date, end_date))
            .annotate(bike=F('BikeID__BikeID'))
            .values('bike')
            .annotate(total=Avg('Cost'))
            .order_by('-total')
        )

        # Count reports per bike
        queryset_cnt_rep = (
            Repairs.objects.all()
                .annotate(bike=F('BikeID__BikeID'))
                .values('bike')
                .order_by('bike')
                .annotate(Count('bike'))
        )

        # Count movements of bike
        queryset_cnt_mov = (
            Movement.objects.all()
                .annotate(bike=F('BikeID__BikeID'))
                .values('bike')
                .order_by('bike')
                .annotate(Count('bike'))
        )

        # Count rep per op
        queryset_cnt_repairs_op = (
            Repairs.objects.all()
                .annotate(opera=F('AssignedOperator__userid'))
                .values('opera')
                .annotate(counts=Count('opera'))
                .order_by('-counts')
        )

        # Count mov per op
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

        bikes_moving_ser = BikeSerializer(queryset_bikes_moving, many=True).data
        bikes_repair_ser = BikeSerializer(queryset_bikes_repair, many=True).data

        popular_bike = queryset_trip_count_bike[0] if len(queryset_trip_count_bike) > 0 else None
        profit_bike = queryset_income_day_avg[0] if len(queryset_income_day_avg) > 0 else None
        opera_most_repa = queryset_cnt_repairs_op[0] if len(queryset_cnt_repairs_op) > 0 else None
        opera_most_movs = queryset_cnt_mov_op[0] if len(queryset_cnt_mov_op) > 0 else None

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

    