from django.contrib import admin
from bikeshareapp import models

admin.site.register(models.User)
# Register your models here.
admin.site.register(models.Wallet)
admin.site.register(models.Address)
admin.site.register(models.Bike)
admin.site.register(models.Trip)
admin.site.register(models.Repairs)
admin.site.register(models.Movement)