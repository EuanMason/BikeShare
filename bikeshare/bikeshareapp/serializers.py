from django.contrib.auth.models import User, Group
from rest_framework import serializers

# Taken from https://www.django-rest-framework.org/tutorial/quickstart/ as tests
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']