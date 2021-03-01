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

from django.urls import include, path
from rest_framework import routers
from bikeshareapp import rest_views  # progsd-bike-share\bikeshare\bikeshareapp\rest_views.py
from bikeshareapp import rent_views  # progsd-bike-share\bikeshare\bikeshareapp\rent_views.py
from bikeshareapp.report_view import *
from bikeshareapp.custom_actions_rest_view import *

router = routers.DefaultRouter()
# Register the Rest Views
router.register(r'wallet', rest_views.WalletViewSet, basename='wallet')
router.register(r'address', rest_views.AddressViewSet)
router.register(r'bike', rest_views.BikeViewSet)
router.register(r'trip', rest_views.TripViewSet)
router.register(r'repairs', rest_views.RepairsViewSet)

# All the URLs that is being used on the application
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', login_views.user_login),
    url(r'^$', RedirectView.as_view(url='/login/')),
    url(r'^home/$', login_views.check_if_login),
    url(r'^logout/$', login_views.logout),
    path(r'login/to_register/', register_views.to_register_view),
    path('register/', register_views.register_view),
    path('register-a-administrative-role-86eb3212a32d5fde5d53c77d4f872fd2/', register_views.to_register_view_other),
    path('create-a-administrative-role-86eb3212a32d5fde5d53c77d4f872fd2/', register_views.register_other_view),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('recalculate-wallet/', recalculateMoney),
    path('all-bikes/', getAllBikes),
    path('get_wallet/', getWallet),
    path('return_bike/', returnBike),
    path('locations-of-availabe-bikes/', getAvailableLocationsOfBikes),
    path('report_defective/', report_defective),
    path('all-bikes-location/<str:location>/', getAllBikesBasedOnLocation),
    path('rent_bike/', rent_views.rent_view),
    path(
        'start_rent_bike/<int:trip_id>/',
        rent_views.start_rent_view
    ),
    path('bike-repaired-by-operator-start/',startRepairABike),
    path('bike-repaired-by-operator-end/',endRepairABike),
    path('bike-move-start/', moveBikeStart),
    path('bike-move-end/', moveBikeEnd),
    path('get-pendings-op/',getPendingAcctions),
    path('track-bikes/',trackBikes),
    path('trips_in_daterange/', trips_in_daterange),
    path('total_income/', total_income),
    path('trip_count/', trip_count),
    path('most_common_locations/', most_common_locations),
    path('report-data/', report_data)

    # path('get_user/', getUser),
    # path('get_Location/', getLocation),
    # url('get-operators/', getAllOperators),
    # url('assign-defective-to-operator/', assignBikeToOperator),
    # url('get-operators-defectives/', getAssignedBikes),
]
