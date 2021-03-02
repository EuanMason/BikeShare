from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.utils import json


def auth_required(func):
    """ Authentication decorator

    Args:
        func (Function): the function to be executed

    Returns:
        response (Response): The response containing the status
    """

    NOPERMISSION = "Login Required"

    # Inner function of decorator
    def decorator(request, *args, **kwargs):
        try:
            # Try execute function
            if request.COOKIES['userid']:
                return func(request, *args, **kwargs)
        # Catch the exceptions
        except ValueError:
            raise HttpResponse(status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    # Return decorator 
    return decorator


def role_check(roles: list, func=None):
    """ Role checker

    Args:
        func (Function): the function to be executed

    Returns:
        response (Response): The response containing the status
    """

    def decorator(func):
        # Inner function to validate the role
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            try:
                for role in roles:
                    # Check the roles
                    if request.COOKIES['role'] and request.COOKIES['role'] == role:
                        return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return returned_wrapper
    # Return function based on existence of func param
    if not func:
        # If not exists then create a dummy function to retunr the previous decorator
        def foo(func):
            return decorator(func)

        return foo

    else:
        return decorator(func)
