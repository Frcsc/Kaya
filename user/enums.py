from django.db import models


class UserType(models.TextChoices):
    LEVEL_ONE = 'L1'
    LEVEL_TWO = 'L2'
    LEVEL_THREE = 'L3'
