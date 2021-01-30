from django.contrib.auth.models import User, Group
from rest_framework import serializers
from bikeshareapp   .models import Wallet, Address, Bike, Trip

class WalletSerializer(serializers.HyperlinkedModelSerializer):

    # This should not be done, but the DB doesn't follow the 
    #   acording nomeclature for json response
    wallet_id = serializers.IntegerField(source='WalletID')
    credit = serializers.FloatField(source='Credit')
    payment = serializers.FloatField(source='Credit')

    class Meta:
        model = Wallet
        fields = ['wallet_id', 'credit', 'payment']

class AddressSerializer(serializers.HyperlinkedModelSerializer):

    location_id = serializers.IntegerField(source='LocationID')
    line_1 = serializers.CharField(source='Line1')
    city = serializers.CharField(source='City')
    postcode = serializers.CharField(source='Postcode')

    class Meta:
        model = Address
        fields = ['location_id', 'line_1', 'city', 'postcode']

class BikeSerializer(serializers.HyperlinkedModelSerializer):

    bike_id = serializers.IntegerField(source='BikeID')
    rent = serializers.FloatField(source='Rent')
    is_available = serializers.IntegerField(source='IsAvailable')
    is_defective = serializers.IntegerField(source='IsDefective')
    location_id = serializers.IntegerField(source='LocationID')

    class Meta:
        model = Bike
        fields = ['bike_id', 'rent', 'is_available', 'is_defective', 'location_id']

class TripSerializer(serializers.HyperlinkedModelSerializer):

    trip_id = serializers.IntegerField(source='TripID')
    bike_id = serializers.IntegerField(source='BikeID')
    date  = serializers.DateField(source='Date')
    start_time = serializers.DateField(source='StartTime')
    end_time = serializers.DateField(source='EndTime')
    start_address = serializers.IntegerField(source='StartAddress')
    end_address = serializers.IntegerField(source='EndAddress')
    cost = serializers.FloatField(source='Cost')
    payment_status = serializers.IntegerField(source='PaymentStatus')

    class Meta:
        model = Trip
        fields = [
            'trip_id', 
            'bike_id', 
            'date', 
            'start_time', 
            'end_time',
            'start_address', 
            'end_address',
            'cost',
            'payment_status'
        ]