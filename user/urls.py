from django.urls import path

from user.api import RegisterUserAPIView, UserLogin

app_name = 'user'

urlpatterns = [
    path('register', RegisterUserAPIView.as_view(), name="register"),
    path('login', UserLogin.as_view(), name="login"),
]
