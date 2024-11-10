from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from user.permissions import AllowAnyPermission
from user.serializers import LoginSerializer, RegisterUserSerializer


class RegisterUserAPIView(AllowAnyPermission, CreateAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successful", "data": serializer.validated_data['email']},
            status=status.HTTP_201_CREATED,
        )


class UserLogin(AllowAnyPermission, KnoxLoginView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user.is_verified is False:
            return Response(
                {"message": "Please verify your account", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance, token = AuthToken.objects.create(user)

        return Response(
            {'message': 'Successful', 'token': token, 'expiry': instance.expiry},
            status=status.HTTP_200_OK,
        )
