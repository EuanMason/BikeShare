from django.contrib import admin
from bikeshareapp import models

admin.site.register(models.User)
# Register models to be accessed on the admin view
admin.site.register(models.Wallet)
admin.site.register(models.Address)
admin.site.register(models.Bike)
admin.site.register(models.Trip)
admin.site.register(models.Repairs)
admin.site.register(models.Movement)