from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
