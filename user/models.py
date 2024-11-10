from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models

from kaya.models import BaseModel
from user.enums import UserType

password_reset_token = PasswordResetTokenGenerator()


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=128, choices=UserType.choices, default=UserType.LEVEL_ONE
    )
