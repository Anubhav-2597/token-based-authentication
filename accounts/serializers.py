from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import ListUserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListUserModel
        fields = "__all__"
