from django.db import models
from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth

from kaya.models import BaseModel


class AdGroup(BaseModel):
    ad_group_id = models.CharField(primary_key=True, editable=False, max_length=128)
    ad_group_name = models.CharField(max_length=128)
    campaign = models.ForeignKey('campaign.Campaign', on_delete=models.PROTECT)

    def __str__(self):
        return self.ad_group_name

    @property
    def average_monthly_cost(self):
        output = (
            self.adgroupstat_set.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(monthly_total_cost=Sum('cost'))
            .aggregate(average_total_cost=Avg('monthly_total_cost'))
        )
        return output['average_total_cost']

    @property
    def average_monthly_conversions(self):
        output = (
            self.adgroupstat_set.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(monthly_conversions=Sum('conversions'))
            .aggregate(average_monthly_conversions=Avg('monthly_conversions'))
        )
        return output['average_monthly_conversions']
