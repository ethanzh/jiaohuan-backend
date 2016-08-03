from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # Removed password
        fields = ['id', 'username', 'phone_number', 'company', 'location', 'email', 'first_name', 'last_name',
                  'is_staff', 'date_joined', 'website', 'title', 'info']

