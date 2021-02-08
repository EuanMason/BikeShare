from django.conf.urls import url
from bikeshareapp.operator_views import *

urlpatterns = [

    url(r'locations/', select_locations),
    url(r'move/', select_move_bike),
    url(r'^move_start', move_start)

]
