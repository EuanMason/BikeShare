import sqlite3
from bikeshareapp.models import *


def check_user(userid: str) -> bool:
    """ Check if the user exist,

    Args:
        userid (string): Email, unique Identifier

    Returns:
        bool (Response): Boolean indicating the validation
    """

    try:
        # Try to get the user
        user = User.objects.get(userid=userid)
        return True
    except models.ObjectDoesNotExist:
        return False

 
def login_check(userid: str, password: str):
    """ Check the user login info

    Args:
        userid (string): Email, unique Identifier
        password (string): Password
    Returns:
        user (Object): user instance or int state code
    """

    # Check if user exists
    exist = check_user(userid)
    if not exist:
        return 2  # state code 2: username not exist
    elif exist and User.objects.get(userid=userid).password != password:
        return 1  # state code 1: wrong password
    else:
        return User.objects.get(userid=userid)


def get_all_locations():
    """ Get locations

    Args:
        None
    Returns:
        address_list (list): list of locations
    """

    try:
        # Get all locations
        locations = Address.objects.all()
        address_list = []
        # Iterate over locations to form list
        for location in locations:
            line1 = location.Line1
            address_list.append(line1)
        # Format list
        address_list = list(set(address_list))
        # print(address_list)
        return address_list
    except:
        return None


def get_all_bikes_locations():
    """ Get bikes locations

    Args:
        None
    Returns:
        address_list (list): list of locations
    """

    try:
        # Get all bikes
        bike_list = Bike.objects.all()
        address_list = {}
        # Iterate over list of bikes to get all the locations
        for bike in bike_list:
            location_id = bike.AddressLocationID
            location = location_id.Line1
            if location in address_list.keys():
                # Count the ocurrences of the address
                address_list[location] += 1
            else:
                # If address does not extist, add a new one
                address_list[location] = 1
        # Retunr the formed list
        return address_list
    except:
        return None


def get_all_unavailable_bikes():
    """ Get not available bikes

    Args:
        None
    Returns:
        bike_list (list): list of bikes
    """

    try:
        # Get all the not available bikes
        bikes = Bike.objects.filter(IsAvailable=0)
        bike_list = []
        # Iterate to create id list
        for bike in bikes:
            bike_list.append(bike.BikeID)
        bike_list = list(set(bike_list))
        # print(bike_list)
        # Return the bikes ids
        return bike_list
    except:
        return None
