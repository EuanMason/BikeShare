from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def test(request):
    return render(request, 'bikeshareapp/login.html') 