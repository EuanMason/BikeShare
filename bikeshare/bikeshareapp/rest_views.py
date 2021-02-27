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

from .models import Wallet, Address, Bike, Trip, Repairs
from .rest_serializers import WalletSerializer, AddressSerializer, BikeSerializer, TripSerializer, RepairsSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """ ViewSet to get access to the set of basic operations (Create, update, delete, etc) for the 
    wallet model. This is mainly used on admin view
    
    Attributes:
        queryset (object): Basic queryset to get all the objects of type Wallet from DB
        serializer_class (object): Serializer to return the data as JSON format
        permission_classes (list): List of permission to access this operations
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class AddressViewSet(viewsets.ModelViewSet):
    """ ViewSet to get access to the set of basic operations (Create, update, delete, etc) for the 
    address (location) model. This is mainly used on admin view
    
    Attributes:
        queryset (object): Basic queryset to get all the objects of type Address from DB
        serializer_class (object): Serializer to return the data as JSON format
        permission_classes (list): List of permission to access this operations
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class BikeViewSet(viewsets.ModelViewSet):
    """ ViewSet to get access to the set of basic operations (Create, update, delete, etc) for the 
    bike model. This is mainly used on admin view
    
    Attributes:
        queryset (object): Basic queryset to get all the objects of type Bike from DB
        serializer_class (object): Serializer to return the data as JSON format
        permission_classes (list): List of permission to access this operations
    """
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class TripViewSet(viewsets.ModelViewSet):
    """ ViewSet to get access to the set of basic operations (Create, update, delete, etc) for the 
    Trip model. This is mainly used on admin view
    
    Attributes:
        queryset (object): Basic queryset to get all the objects of type Trip from DB
        serializer_class (object): Serializer to return the data as JSON format
        permission_classes (list): List of permission to access this operations
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer 
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class RepairsViewSet(viewsets.ModelViewSet):
    """ ViewSet to get access to the set of basic operations (Create, update, delete, etc) for the 
    repairs model. This is mainly used on admin view
    
    Attributes:
        queryset (object): Basic queryset to get all the objects of type Repairs from DB
        serializer_class (object): Serializer to return the data as JSON format
        permission_classes (list): List of permission to access this operations
    """
    queryset = Repairs.objects.all()
    serializer_class = RepairsSerializer
    permission_classes = [permissions.AllowAny]