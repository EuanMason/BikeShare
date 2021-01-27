from django.db import models


class User(models.Model):
    userid = models.EmailField(unique=True, primary_key=True, blank=False)
    nickname = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=10, default='user')

    class Meta:
        managed = False
        db_table = 'bikeshareapp_user'

# Create your models here.
