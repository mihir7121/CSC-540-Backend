from rest_framework import serializers #type: ignore
from . models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'password']