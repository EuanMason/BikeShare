
from django.http import HttpResponse, Http404
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
            raise Http404()
        except KeyError:
            return HttpResponse(json.dumps({'code': NOPERMISSION}))
        return HttpResponse(json.dumps({'code': NOPERMISSION}))

    return decorator
