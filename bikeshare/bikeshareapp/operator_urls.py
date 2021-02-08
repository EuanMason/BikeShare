from django.conf.urls import url
from bikeshareapp.operator_views import *

urlpatterns = [

    url(r'^locations', select_locations),
    url(r'^move_select_bike', select_move_bike),
    url(r'^move_start', move_start)

]
