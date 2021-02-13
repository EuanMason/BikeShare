import sqlite3
from bikeshareapp.models import *


# Check if the user exist,
# param: userid (login name -- Email, unique Identifier)
# return: bool
def check_user(userid: str) -> bool:
    try:
        user = User.objects.get(userid=userid)
        return True
    except models.ObjectDoesNotExist:
        return False


# Check the user login info
# params: str userid (login name -- Email, unique Identifier)
#         str password
# return: user instance or int state code
def login_check(userid: str, password: str):
    exist = check_user(userid)
    if not exist:
        return 2  # state code 2: username not exist
    elif exist and User.objects.get(userid=userid).password != password:
        return 1  # state code 1: wrong password
    else:
        return User.objects.get(userid=userid)


def get_all_locations():
    try:
        locations = Address.objects.all()
        address_list = []
        for location in locations:
            line1 = location.Line1
            address_list.append(line1)
        address_list = list(set(address_list))
        print(address_list)
        return address_list
    except:
        return None


def get_all_bikes_locations():
    try:
        bike_list = Bike.objects.all()
        address_list = []
        for bike in bike_list:
            location_id = bike.AddressLocationID
            location = location_id.Line1
            address_list.append(location)
        address_list = list(set(address_list))
        return address_list
    except:
        return None


def get_all_unavailable_bikes():
    try:
        bikes = Bike.objects.filter(IsAvailable=0)
        bike_list = []
        for bike in bikes:
            bike_list.append(bike.BikeID)
        bike_list = list(set(bike_list))
        print(bike_list)
        return bike_list
    except:
        return None
