from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import ListItemModel


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListItemModel
        fields = "__all__"
