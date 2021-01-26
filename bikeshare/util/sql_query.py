import sqlite3
from bikeshareapp.models import *


def check_user(userid):
    try:
        user = User.objects.get(userid=userid)
        return True
    except models.ObjectDoesNotExist:
        return False


def login_check(userid, password):
    exist = check_user(userid)
    if exist and User.objects.get(userid=userid).password == password:
        return User.objects.get(userid=userid)
    elif exist and User.objects.get(userid=userid).password != password:
        return 1  # state code 1: wrong password
    else:
        return 2  # state code 2: username not exist


