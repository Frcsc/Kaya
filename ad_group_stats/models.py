from django.db import models

from kaya.models import BaseModel


class AdGroupStat(BaseModel):
    class DEVICE(models.TextChoices):
        MOBILE = "MOBILE"
        TABLET = "TABLET"
        DESKTOP = "DESKTOP"

    date = models.DateField()
    ad_group = models.ForeignKey('ad_group.AdGroup', on_delete=models.PROTECT)
    device = models.CharField(max_length=128, choices=DEVICE.choices)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    conversions = models.DecimalField(max_digits=22, decimal_places=10)
    cost = models.DecimalField(max_digits=22, decimal_places=10)
