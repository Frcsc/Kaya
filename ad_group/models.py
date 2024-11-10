from django.db import models
from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth

from ad_group_stats.utils import quantize_two_decimal_places
from kaya.models import BaseModel


class AdGroup(BaseModel):
    ad_group_id = models.CharField(primary_key=True, editable=False, max_length=128)
    ad_group_name = models.CharField(max_length=128)
    campaign = models.ForeignKey('campaign.Campaign', on_delete=models.PROTECT)

    def __str__(self):
        return self.ad_group_name

    @property
    def average_monthly_cost(self):
        if not self.adgroupstat_set.exists():
            return quantize_two_decimal_places('0.00')
        output = (
            self.adgroupstat_set.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(monthly_total_cost=Sum('cost'))
            .aggregate(average_total_cost=Avg('monthly_total_cost'))
        )
        return quantize_two_decimal_places(output['average_total_cost'])

    @property
    def cost_per_conversion(self):
        if not self.adgroupstat_set.exists():
            return quantize_two_decimal_places('0.00')

        output = self.adgroupstat_set.aggregate(
            total_cost=Sum('cost'), total_conversions=Sum('conversions')
        )

        if output.get('total_conversions') == 0:
            return quantize_two_decimal_places('0.00')

        average_cost = output['total_cost'] / output['total_conversions']

        return quantize_two_decimal_places(average_cost)
