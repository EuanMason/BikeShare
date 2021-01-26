from django.db import models


class User(models.Model):
    id = models.EmailField(unique=True, primary_key=True, blank=False)
    nickname = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=10, default='user')


# Create your models here.
