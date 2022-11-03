from rest_framework import serializers
from .models import user_location

class user_loacation_serializer(serializers.ModelSerializer):
    class Meta:
        model = user_location
        fields = ('locationId', 'userId','user_first_name', 'user_last_name', 'image', 'latitude', 'longitude')
        