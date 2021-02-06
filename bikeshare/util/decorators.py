from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.utils import json


def auth_required(func):
    """
    Authentication decorator
    """

    NOPERMISSION = "Login Required"

    def decorator(request, *args, **kwargs):
        try:
            if request.COOKIES['userid']:
                return func(request, *args, **kwargs)
        except ValueError:
            raise HttpResponse(status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    return decorator


def role_check(roles: list, func=None):
    """
    Role checker
    """

    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            try:
                for role in roles:
                    if request.COOKIES['role'] and request.COOKIES['role'] == role:
                        return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return returned_wrapper

    if not func:
        def foo(func):
            return decorator(func)

        return foo

    else:
        return decorator(func)
