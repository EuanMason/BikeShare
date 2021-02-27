from django.contrib.auth.models import User, Group
from rest_framework import serializers
from bikeshareapp.models import Wallet, Address, Bike, Trip, User, Repairs

class UserLimitedSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer to render the User data in a JSON format. This one is limited
        Since only returns the user id and nickname

    Attributes:
        user_id (str): Id of the user
        user_nickname (str): User's nickname
    """
    user_id = serializers.CharField(source='userid')
    user_nickname = serializers.CharField(source='nickname')

    # Specify the model and the fields to be returned
    class Meta:
        model = User
        fields = [
            'user_id',
            'user_nickname'
        ]

class WalletSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer to render the Wallet data in a JSON format. 

    Attributes:
        wallet_id (str): Id of the wallet
        credit (str): Money available on the wallet
        payment (float): Methods of payment - Not used
    """

    # This should not be done, but the DB doesn't follow the 
    #   acording nomeclature for json response
    wallet_id = serializers.IntegerField(source='WalletID')
    credit = serializers.FloatField(source='Credit')
    payment = serializers.FloatField(source='PaymentMethods')

    # Specify the model and the fields to be returned
    class Meta:
        model = Wallet
        fields = ['wallet_id',
                  'credit',
                  'payment'
                  ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer to render the User data in a JSON format. 

    Attributes:
        user_id (str): Id of the user
        user_pass (str): User's password
        user_role (str): User's role
        user_nickname (str): User's nickname
        wallet_id (object): User's wallet object
    """

    user_id = serializers.CharField(source='userid')
    user_pass = serializers.CharField(source='password')
    user_role = serializers.CharField(source='role')
    user_nickname = serializers.CharField(source='nickname')
    wallet_id = WalletSerializer(source='WalletID')

    # Specify the model and the fields to be returned
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
    """ Serializer to render the Address data in a JSON format. 

    Attributes:
        location_id (int): Id of the Address
        line_1 (str): Line 1 of the address
        city (str): City of the address
        postcode (str): Postcode of the address
        longitude (float): Longitude of the coordinate of the address
        latitude (float): Latitude of the coordinate of the address
    """
    location_id = serializers.IntegerField(source='LocationID')
    line_1 = serializers.CharField(source='Line1')
    city = serializers.CharField(source='City')
    postcode = serializers.CharField(source='Postcode')
    longitude = serializers.FloatField(source='Longitude')
    latitude = serializers.FloatField(source='Latitude')

    # Specify the model and the fields to be returned
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
    """ Serializer to render the Bike data in a JSON format. 

    Attributes:
        bike_id (int): Id of the Bike
        rent (float): How much is the rent of the bike
        is_available (int): Bike's state (0-3)
        is_defective (int): Flag to check if the bike is defective
        location (object): Bike's current location object
    """

    bike_id = serializers.IntegerField(source='BikeID')
    rent = serializers.FloatField(source='Rent')
    is_available = serializers.IntegerField(source='IsAvailable')
    is_defective = serializers.IntegerField(source='IsDefective')
    location = AddressSerializer(source='AddressLocationID')

    # Specify the model and the fields to be returned
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
    """ Serializer to render the Trip data in a JSON format. 

    Attributes:
        trip_id (int): Id of the Trip
        bike (object): Bike object that is being used on the trip
        date (float): Date of the trip
        start_time (datetime): Date and time of the start of the trip
        end_time (datetime): Date and time of the end of the trip
        start_address (object): Address object of the location where the trip started
        end_address (object): Address object of the location where the trip ended
        cost (float): Cost of the trip
        payment_status (int): To represent the status payment - not used
        user (object): User object who is on the trip
    """

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

    # Specify the model and the fields to be returned
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
    """ Serializer to render the Repairs data in a JSON format. 

    Attributes:
        repairs_id (int): Id of the Repair
        bike_id (object): Bike object that is being repaired
        reported_user (object): User object that reported the bike
        issue (str): Description of the problem
        assigned_operator (object): Operator object that is working on the repair
        in_progress (int): Flag to check if the repairment is on going
    """

    repairs_id = serializers.IntegerField(source='RepairsID')
    bike_id = BikeSerializer(source='BikeID')
    reported_user = UserLimitedSerializer(source='ReportedUser')
    issue = serializers.CharField(source='Issue')
    assigned_operator = UserLimitedSerializer(source='AssignedOperator')
    in_progress = serializers.IntegerField(source="InProgress")

    # Specify the model and the fields to be returned
    class Meta:
        model = Repairs
        fields = ['repairs_id',
                  'bike_id',
                  'reported_user',
                  'issue',
                  'assigned_operator',
                  'in_progress'
                  ]

class MovementSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer to render the Repairs data in a JSON format. 

    Attributes:
        move_id (int): Id of the movement
        location (object): Location object to where the bike will be moved
        bike_id (object): Bike object that is the bike that is being moved
        operator (object): Operator object that is executing the movement
        in_progress (int): Flag to check if the movement is on going
    """

    move_id = serializers.IntegerField(source='MovementID')
    location = AddressSerializer(source='ProposedLocation')
    bike_id = BikeSerializer(source='BikeID')
    operator = UserLimitedSerializer(source='MoveOperator')
    in_progress = serializers.IntegerField(source="InProgress")

    # Specify the model and the fields to be returned
    class Meta:
        model = Repairs
        fields = ['move_id',
                  'location',
                  'bike_id',
                  'operator',
                  'in_progress'
                  ]