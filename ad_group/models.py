from django.db import models

from kaya.models import BaseModel


class AdGroup(BaseModel):
    ad_group_id = models.CharField(primary_key=True, editable=False, max_length=128)
    ad_group_name = models.CharField(max_length=128)
    campaign = models.ForeignKey('campaign.Campaign', on_delete=models.PROTECT)

    def __str__(self):
        return self.ad_group_name
