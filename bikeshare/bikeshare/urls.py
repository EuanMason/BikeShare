"""bikeshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from bikeshareapp import login_views
from bikeshareapp import register_views
from bikeshareapp.frontend_views import *

from django.urls import include, path
from rest_framework import routers
from bikeshareapp import views  # progsd-bike-share\bikeshare\bikeshareapp\views.py
from bikeshareapp import rest_views  # progsd-bike-share\bikeshare\bikeshareapp\rest_views.py
from bikeshareapp.report_view import *
from bikeshareapp.custom_actions_rest_view import *

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# Register the Rest Views
router.register(r'wallet', rest_views.WalletViewSet, basename='wallet')
router.register(r'address', rest_views.AddressViewSet)
router.register(r'bike', rest_views.BikeViewSet)
router.register(r'trip', rest_views.TripViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', login_views.user_login),
    url(r'^$', RedirectView.as_view(url='/login/')),
    url(r'^home/$', login_views.check_if_login),
    url(r'^logout/$', login_views.logout),
    path(r'login/to_register/', register_views.to_register_view),
    path('register/', register_views.register_view),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('add-money-to-wallet/', addMoney),
    path('all-bikes/', getAllBikes),
    path('avail-bikes/', getAvailableBikes),
    path('get_user/', getUser),
    path('return_bike/', returnBike),
    path('locations-of-availabe-bikes/', getAvailableLocationsOfBikes),
    url(r'^home/report_defective', report_defective),
    url(r'^operator/', include('bikeshareapp.operator_urls'))
]
