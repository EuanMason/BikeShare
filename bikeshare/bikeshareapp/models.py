from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.IntegerField(max_length=20)
    charges = models.DecimalField(decimal_places=2, default=0.00)
    user_role_id = models.IntegerField(max_length=10)


class Bikes(models.Model):
    id = models.AutoField(primary_key=True)
    is_available = models.BooleanField(default=True)
    is_defective = models.BooleanField(default=False)
    location_id = models.IntegerField(max_length=10)
    rent = models.DecimalField(max_length=10, decimal_places=2)


class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    Address = models.CharField(max_length=100)
    bike_count = models.IntegerField(default=0)


class Trips(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.DO_NOTHING)
    bike_id = models.ForeignKey('Bikes', on_delete=models.DO_NOTHING)
    start_location = models.IntegerField()
    end_location = models.IntegerField()
    duration = models.TimeField()
    cost = models.DecimalField(decimal_places=2, default=0.00)
# Create your models here.
