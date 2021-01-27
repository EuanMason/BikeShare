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
