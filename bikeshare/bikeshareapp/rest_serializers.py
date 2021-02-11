from django.contrib.auth.models import User, Group
from rest_framework import serializers
from bikeshareapp.models import Wallet, Address, Bike, Trip, User, Repairs

class UserLimitedSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.CharField(source='userid')
    user_nickname = serializers.CharField(source='nickname')

    class Meta:
        model = User
        fields = [
            'user_id',
            'user_nickname'
        ]

class WalletSerializer(serializers.HyperlinkedModelSerializer):

    # This should not be done, but the DB doesn't follow the 
    #   acording nomeclature for json response
    wallet_id = serializers.IntegerField(source='WalletID')
    credit = serializers.FloatField(source='Credit')
    payment = serializers.FloatField(source='PaymentMethods')

    class Meta:
        model = Wallet
        fields = ['wallet_id',
                  'credit',
                  'payment'
                  ]

class UserSerializer(serializers.HyperlinkedModelSerializer):

    user_id = serializers.CharField(source='userid')
    user_pass = serializers.CharField(source='password')
    user_role = serializers.CharField(source='role')
    user_nickname = serializers.CharField(source='nickname')
    wallet_id = WalletSerializer(source='WalletID')


    class Meta:
        model = User
        fields = [
            'user_id',
            'user_pass',
            'user_role',
            'user_nickname',
            'wallet_id'
        ]

class AddressSerializer(serializers.HyperlinkedModelSerializer):

    location_id = serializers.IntegerField(source='LocationID')
    line_1 = serializers.CharField(source='Line1')
    city = serializers.CharField(source='City')
    postcode = serializers.CharField(source='Postcode')
    longitude = serializers.FloatField(source='Longitude')
    latitude = serializers.FloatField(source='Latitude')

    class Meta:
        model = Address
        fields = ['location_id',
                  'line_1',
                  'city',
                  'postcode',
                  'longitude',
                  'latitude'
                  ]

class BikeSerializer(serializers.HyperlinkedModelSerializer):

    bike_id = serializers.IntegerField(source='BikeID')
    rent = serializers.FloatField(source='Rent')
    is_available = serializers.IntegerField(source='IsAvailable')
    is_defective = serializers.IntegerField(source='IsDefective')
    # This is the case if you only need to retrieve one field from the relationship
    # Can check here: https://www.django-rest-framework.org/api-guide/relations/
    #address_location_id = serializers.StringRelatedField(many=False, source='AddressLocationID')
    # This is the case if you need to retrieve the object
    location = AddressSerializer(source='AddressLocationID')
    #address_location_id = serializers.IntegerField(source='AddressLocationID')
    #operator = UserLimitedSerializer(source = 'OperatorID')

    class Meta:
        model = Bike
        fields = ['bike_id',
                  'rent',
                  'is_available',
                  'is_defective',
                  'location',
                  #'operator'
                  ]

class TripSerializer(serializers.HyperlinkedModelSerializer):

    trip_id = serializers.IntegerField(source='TripID')
    bike = BikeSerializer(source='BikeID')
    date = serializers.DateTimeField(source='Date', format="%Y-%m-%d %H:%M:%S")
    start_time = serializers.DateTimeField(source='StartTime', format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(source='EndTime', format="%Y-%m-%d %H:%M:%S")
    start_address = AddressSerializer(source='StartAddress')
    end_address = AddressSerializer(source='EndAddress')
    cost = serializers.FloatField(source='Cost')
    payment_status = serializers.IntegerField(source='PaymentStatus')
    user = UserSerializer(source='UserID')

    class Meta:
        model = Trip
        fields = [
            'trip_id', 
            'bike',
            'date', 
            'start_time', 
            'end_time',
            'start_address', 
            'end_address',
            'cost',
            'payment_status',
            'user'
        ]

class RepairsSerializer(serializers.HyperlinkedModelSerializer):

    repairs_id = serializers.IntegerField(source='RepairsID')
    bike_id = BikeSerializer(source='BikeID')
    reported_user = UserLimitedSerializer(source='ReportedUser')
    issue = serializers.CharField(source='Issue')
    assigned_operator = UserLimitedSerializer(source='AssignedOperator')
    in_progress = serializers.IntegerField(source="InProgress")

    class Meta:
        model = Repairs
        fields = ['repairs_id',
                  'bike_id',
                  'reported_user',
                  'issue',
                  'assigned_operator',
                  'in_progress'
                  ]

