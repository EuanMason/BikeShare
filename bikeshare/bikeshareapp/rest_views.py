from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view, schema



from bikeshareapp.serializers import UserSerializer, GroupSerializer
from .models import Wallet, Address, Bike, Trip, Repairs
from .rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, RepairsSerializer

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
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class BikeViewSet(viewsets.ModelViewSet):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class RepairsViewSet(viewsets.ModelViewSet):
    queryset = Repairs.objects.all()
    serializer_class = RepairsSerializer
    permission_classes = [permissions.AllowAny]