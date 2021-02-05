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
            raise HttpResponse(json.dumps({'state': NOPERMISSION}), status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            return HttpResponse(json.dumps({'state': NOPERMISSION}), status=status.HTTP_403_FORBIDDEN)
        return HttpResponse(json.dumps({'state': NOPERMISSION}), status=status.HTTP_403_FORBIDDEN)

    return decorator
