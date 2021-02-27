from django.db import models
from django.utils import timezone

class Wallet(models.Model):
    """ Model to represent the table Wallet - Which is to manage the user's money

    Attributes:
        WalletID (int): Id of the wallet
        Credit (int): Available money
        PaymentMethods (int) : Possible ways to pay - Not used
    """

    WalletID = models.AutoField(primary_key=True)
    Credit = models.FloatField()
    PaymentMethods = models.BinaryField(default=None)

    # String to be retrieved on admin view
    def __str__(self):
        return str(self.WalletID)

    # Assing the table name
    class Meta:
        db_table = 'wallet'

class User(models.Model):
    """ Model to represent the table User - Which is to manage the users on the system

    Attributes:
        userid (int): Id of the user
        password (int): User's password
        role (str): Role of the user
        nickname (str): Nickname of the user
        WalletID (int): Foreing key to the user's wallet
    """
    userid = models.EmailField(unique=True, primary_key=True, blank=False)
    password = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=10, default='user')
    nickname = models.CharField(max_length=50, blank=False)
    WalletID = models.ForeignKey(Wallet, blank=True, null=True, on_delete=models.CASCADE)

     # Assing the table name
    class Meta:
        managed = False
        db_table = 'bikeshareapp_user'

class Address(models.Model):
    """ Model to represent the table Address - Which is to manage the locations

    Attributes:
        LocationID (int): Id of the Address
        Line1 (str): Line 1 of the address
        City (str): City of the address
        Postcode (str): Postcode of the address
        Longitude (float): Longitude of the coordinate of the address
        Latitude (float): Latitude of the coordinate of the address
    """
    LocationID = models.AutoField(primary_key=True)
    Line1 = models.CharField(max_length=200, blank=False)
    City = models.CharField(max_length=100)
    Postcode = models.CharField(max_length=50, blank=False)
    Longitude = models.FloatField(max_length=200)
    Latitude = models.FloatField(max_length=200)

    # String to be retrieved on admin view
    def __str__(self):
        return self.Postcode

    # Assing the table name
    class Meta:
        db_table = 'address'    

class Bike(models.Model):
    """ Model to represent the table Bike - Which is to manage the bikes in the system

    Attributes:
        BikeID (int): Id of the Bike
        Rent (float): How much is the rent of the bike
        IsAvailable (int): Bike's state (0-3)
        IsDefective (int): Flag to check if the bike is defective
        AddressLocationID (int): Foreing key to the location of the bike
    """
    BikeID = models.AutoField(primary_key=True)
    Rent = models.FloatField(null=False)
    # Extended use of isAvailable
    # 1 = bike is available for user to ride
    # 0 = bike is not available 
    # 2 = bike is not available due movement
    # 3 = bike is not available due repair
    IsAvailable = models.IntegerField(null=False)
    IsDefective = models.IntegerField(null=False)
    AddressLocationID = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='AddressLocationID')
    # OperatorID = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='OperatorID')

    # String to be retrieved on admin view
    def __str__(self):
        return str(self.BikeID)

    # Assing the table name
    class Meta:
        db_table = 'bike'

class Trip(models.Model):
    """ Model to represent the table Trip - Which is to manage the trips in the system

    Attributes:
        TripID (int): Id of the Trip
        BikeID (int): Foreing key to the Bike of the trip
        Date (float): Date of the trip
        StartTime (datetime): Date and time of the start of the trip
        EndTime (datetime): Date and time of the end of the trip
        StartAddress (int): Foreing key to the location of the start of the trip 
        EndAddress (int): Foreing key to the location of the end of the trip
        Cost (float): Cost of the trip
        PaymentStatus (int): To represent the status payment - not used
        UserID (int): Foreing key to user who is in the trip
    """
    TripID = models.AutoField(primary_key=True)
    BikeID = models.ForeignKey(Bike, on_delete=models.CASCADE)
    Date = models.DateTimeField(default=timezone.now)
    StartTime = models.DateTimeField(default=timezone.now)
    EndTime = models.DateTimeField(default=timezone.now)
    StartAddress = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='StartAddress')
    EndAddress = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='EndAddress')
    Cost = models.FloatField()
    PaymentStatus = models.IntegerField()
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    # String to be retrieved on admin view
    def __str__(self):
        return str(self.TripID)

    # Assing the table name
    class Meta:
        db_table = 'trip'

class Repairs(models.Model):
    """ Model to represent the table Repairs - Which is to manage the repairs reports

    Attributes:
        RepairsID (int): Id of the Repair
        BikeID (int): Foreing key to the Bike of the repair
        ReportedUser (int): Foreing key to the user who is reporting a problem
        Issue (str): Description of the problem
        AssignedOperator (int): Foreing key to the operator who took the repairment
        InProgress (int): Flag to check if the repairment is on going
    """
    RepairsID = models.AutoField(primary_key=True)
    BikeID = models.ForeignKey(Bike, on_delete=models.CASCADE)
    ReportedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    Issue = models.CharField(max_length=400)
    AssignedOperator = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE, related_name='assigned_operator')
    # -1 is done
    # 0 not started
    # 1 in progress
    InProgress = models.IntegerField(null=False, default=0)

    # String to be retrieved on admin view
    def __str__(self):
        # If the operator has not been assigned use TBD 
        operator = ""
        if (self.AssignedOperator is None):
            operator = "TBD"
        else:
            operator = str(self.AssignedOperator.userid)
        return str(self.RepairsID) + ' - ' + operator

    # Assing the table name
    class Meta:
        db_table = 'repairs'

class Movement(models.Model):
    """ Model to represent the table Movements - Which is to manage the movements reports

    Attributes:
        MovementID (int): Id of the movement
        ProposedLocation (int): Foreing key to the location to where the bike is being moved
        BikeID (int): Foreing key to the Bike that is being moved
        MoveOperator (str): Foreing key to the operator that is doing the movement
        InProgress (int): Flag to check if the movement is on going
    """
    MovementID = models.AutoField(primary_key=True)
    ProposedLocation = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='proposed_location')
    BikeID = models.ForeignKey(Bike, on_delete=models.CASCADE)
    MoveOperator = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE, related_name='move_operator')
    # -1 is done
    # 0 not started
    # 1 in progress
    InProgress = models.IntegerField(null=False, default=0)

    # String to be retrieved on admin view
    def __str__(self):
        # If the operator has not been assigned use TBD
        operator = ""
        if (self.MoveOperator is None):
            operator = "TBD"
        else:
            operator = str(self.MoveOperator.userid)
        return str(self.MovementID) + ' - ' + operator

    # Assing the table name
    class Meta:
        db_table = 'movement'