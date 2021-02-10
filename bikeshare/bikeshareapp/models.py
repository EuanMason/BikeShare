from django.db import models
from django.utils import timezone

class Wallet(models.Model):
    WalletID = models.AutoField(primary_key=True)
    Credit = models.FloatField()
    PaymentMethods = models.BinaryField()

    def __str__(self):
        return str(self.WalletID)

    # If we need to override the basisc acitions
    # def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)

    class Meta:
        db_table = 'wallet'

class User(models.Model):
    userid = models.EmailField(unique=True, primary_key=True, blank=False)
    password = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=10, default='user')
    nickname = models.CharField(max_length=50, blank=False)
    WalletID = models.ForeignKey(Wallet, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'bikeshareapp_user'


# Create your models here.



class Address(models.Model):
    LocationID = models.AutoField(primary_key=True)
    Line1 = models.CharField(max_length=200, blank=False)
    City = models.CharField(max_length=100)
    Postcode = models.CharField(max_length=50, blank=False)
    Longitude = models.FloatField(max_length=200)
    Latitude = models.FloatField(max_length=200)

    def __str__(self):
        return self.Postcode

    class Meta:
        db_table = 'address'    


class Bike(models.Model):
    BikeID = models.AutoField(primary_key=True)
    Rent = models.FloatField(null=False)
    IsAvailable = models.IntegerField(null=False)
    IsDefective = models.IntegerField(null=False)
    AddressLocationID = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='AddressLocationID')
    OperatorID = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='OperatorID')

    def __str__(self):
        return str(self.BikeID)

    class Meta:
        db_table = 'bike'

class Trip(models.Model):
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

    # Test = models.IntegerField(default=-1)
    # userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.TripID)

    class Meta:
        db_table = 'trip'

class Repairs(models.Model):
    RepairsID = models.AutoField(primary_key=True)
    BikeID = models.ForeignKey(Bike, on_delete=models.CASCADE)
    ReportedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    Issue = models.CharField(max_length=400)
    AssignedOperator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_operator')
    InProgress = models.IntegerField(null=False, default=0)

    def __str__(self):
        return str(self.RepairsID) + ' - ' + str(self.AssignedOperator.userid)

    class Meta:
        db_table = 'repairs'