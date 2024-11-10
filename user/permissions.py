from rest_framework import permissions

from user.mixins import IsLevelOne, IsLevelThree, IsLevelTwo


class AllowAnyPermission:
    permission_classes = [permissions.AllowAny]


class LevelOnePermission:
    permission_classes = [IsLevelOne]


class LevelTwoPermission:
    permission_classes = [IsLevelTwo]


class LevelThreePermission:
    permission_classes = [IsLevelThree]


class LevelTwoOnePermission:
    permission_classes = [IsLevelTwo | IsLevelOne]


class LevelThreeTwoPermission:
    permission_classes = [IsLevelThree | IsLevelTwo]


class AllLevelPermission:
    permission_classes = [IsLevelThree | IsLevelTwo | IsLevelOne]
