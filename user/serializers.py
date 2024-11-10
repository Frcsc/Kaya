from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from user.models import UserProfile

User = get_user_model()


class RegisterUserSerializer(serializers.Serializer):
    '''
    Note: The is_verified attribute should be updated once a verification method is established.
    For now all registered users will be marked as verified.
    '''

    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("This email belongs to an existing user")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_verified = True
        user.save()
        userprofile = UserProfile(user=user)
        userprofile.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['email']
        password = data['password']

        if authenticate(email=email, password=password) is None:
            raise serializers.ValidationError('Invalid credentials')
        return authenticate(email=email, password=password)
