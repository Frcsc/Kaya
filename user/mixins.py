from rest_framework import permissions

from user.enums import UserType


class BaseAuthentication(permissions.IsAuthenticated):
    user_type = None

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.userprofile.user_type == self.user_type
        )


class IsLevelOne(BaseAuthentication):
    user_type = UserType.LEVEL_ONE


class IsLevelTwo(BaseAuthentication):
    user_type = UserType.LEVEL_TWO


class IsLevelThree(BaseAuthentication):
    user_type = UserType.LEVEL_THREE
