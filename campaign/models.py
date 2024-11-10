from django.db import models

from ad_group_stats.utils import quantize_two_decimal_places
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

    @property
    def number_of_ad_groups(self):
        return self.adgroup_set.count()

    @property
    def average_monthly_cost(self):
        total_cost = sum(
            adgroup.average_monthly_cost for adgroup in self.adgroup_set.all()
        )
        return quantize_two_decimal_places(total_cost)

    @property
    def cost_per_conversion(self):

        total_cost = sum(
            adgroup.cost_per_conversion for adgroup in self.adgroup_set.all()
        )

        return quantize_two_decimal_places(total_cost)
