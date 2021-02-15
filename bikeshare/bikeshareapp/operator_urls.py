from django.conf.urls import url
from django.urls import path

from bikeshareapp.operator_views import *

urlpatterns = [

    path(r'locations/', select_locations),
    path(r'move/select_bike/', select_move_bike),
    path(r'move/start/', move_start),
    path(r'move/loc_n_bikes/', move_get_loc_bikes),
    path(r'move/end/', move_end)

]
