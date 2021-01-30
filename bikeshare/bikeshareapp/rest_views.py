from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status


from rest_framework.decorators import action
from rest_framework.response import Response

from bikeshareapp.serializers import UserSerializer, GroupSerializer
from .models import Wallet, Address, Bike, Trip
from .rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer

# Some people say the logic shouldn't be on the views
# Some other say the opposite.
# For practicality, I think it would be better to leave the logic here
# 
# NOTE I: We are using the class viewsets.ModelViewSet to get quick access
#       to basic operations for reading and writing
# NOTE II: I created a dummy function to add money to the wallet
#           it only has the basic stuff, if we need something else we can
#           look for it together :)  


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer 
    permission_classes = [permissions.IsAuthenticated]

    # Add any other methods needed here for Wallet objects
    # The decorator action allows us to create custom actions
    # All the methods that doesn't necessary imply a post/get/update/delete 
    #   can be created based on this decorator
    # detail=True allows us to retrieve one single object, 
    #   otherwise, like a list, should be False
    # NOTE: We are using *args and **kwargs to get access to any
    #       of the values passed on the url or post request.
    #       Although, we can use data=request.data too :)
    @action(methods=['post'], detail=True, url_path='add_money/')
    def addMoneyToWallet(self, request, *args, **kwargs):        
        self.object = self.get_object()
        print(request.data)
        return Response({"Status":"OK"}, status=status.HTTP_200_OK)    

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer 
    permission_classes = [permissions.IsAuthenticated]

    # Add any other method needed here for Address objects

class BikeViewSet(viewsets.ModelViewSet):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer 
    permission_classes = [permissions.IsAuthenticated]

    # Add any other method needed here for Bike objects

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer 
    permission_classes = [permissions.IsAuthenticated]

    # Add any other method needed here for Trip objects