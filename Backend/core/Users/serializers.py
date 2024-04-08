from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializers(serializers.Serializer):
    """
    Serializers for the registration endpoint
    """
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'Error': 'This username already exists'})
        return data
    
    def create(self, data):
        user = User.objects.create_user(
            username=data['username'], # .lower()
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password']) # For Hashing Password 
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializers for the login endpoint
    """ 
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'Error': 'This username does not exist'})
        
        return data
    
    # authentication logic in the serializer is appropriate, such as when you want to centralize authentication logic across multiple views or when you're implementing a custom authentication mechanism within the serializer itself.