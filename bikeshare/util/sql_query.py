import sqlite3
from bikeshareapp.models import *


def check_user(username):
    try:
        user = User.objects.get(id=username)
        return True
    except models.ObjectDoesNotExist:
        return False


def login_check(username, password):
    exist = check_user(username)
    if exist and User.objects.get(id=username).password == password:
        return User.objects.get(id=username)
    elif exist and User.objects.get(id=username).password != password:
        return 1  # state code 1: wrong password
    else:
        return 2  # state code 2: username not exist


