from django.db import models

from kaya.models import BaseModel


class Campaign(BaseModel):
    class Type(models.TextChoices):
        SEARCH_STANDARD = 'SEARCH_STANDARD'
        VIDEO_RESPONSIVE = 'VIDEO_RESPONSIVE'

    campaign_id = models.CharField(primary_key=True, editable=False, max_length=128)
    campaign_name = models.CharField(max_length=128)
    campaign_type = models.CharField(max_length=128, choices=Type.choices)

    def __str__(self):
        return self.campaign_name
