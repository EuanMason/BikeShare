from django.db import models
from django.utils import timezone


class User(models.Model):
    userid = models.EmailField(unique=True, primary_key=True, blank=False)
    nickname = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=10, default='user')

    class Meta:
        managed = False
        db_table = 'bikeshareapp_user'

# Create your models here.
class Wallet(models.Model):
    credit = models.FloatField()
    dueCharge = models.FloatField()

    def __str__(self):
        return self.name

class Address(models.Model):
    town = models.CharField(max_length=100)
    city  = models.CharField(max_length=100)
    postcode  = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Bike(models.Model):
    rent = models.FloatField()
    isAvailable = models.BooleanField()
    isDefective = models.BooleanField()
    locationID = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Trip(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    bikeId = models.ForeignKey(Bike, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    startTime  = models.DateTimeField(default=timezone.now)
    endTime  = models.DateTimeField(default=timezone.now)
    startAddressId = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_start')
    endAddressId = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_end')
    bikeRent = models.FloatField()
    paymentStatus  = models.CharField(max_length=50)

    def __str__(self):
        return self.name
