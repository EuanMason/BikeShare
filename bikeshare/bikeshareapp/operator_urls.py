from django.conf.urls import url
from bikeshareapp.report_view import *

urlpatterns = [

    url(r'locations/', select_locations),
    url(r'move/', move_bike)

]
