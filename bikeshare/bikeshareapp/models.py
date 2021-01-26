from django.db import models


class User(models.Model):
    id = models.EmailField(unique=True, primary_key=True, blank=False)
    password = models.CharField(max_length=50,blank=False)
    role = models.CharField(max_length=10)
# Create your models here.
