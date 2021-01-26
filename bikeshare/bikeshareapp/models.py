from django.db import models


class User(models.Model):
    id = models.EmailField(unique=True, primary_key=True, blank=False)
    password = models.CharField(max_length=50,blank=False)
    role = models.CharField(max_length=10)
# Create your models here.


class BikeUser(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=40, primary_key=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'bike_user'