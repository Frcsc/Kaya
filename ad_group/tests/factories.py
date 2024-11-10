import factory

from ad_group.models import AdGroup
from kaya.factories import BaseModelFactory, FuzzyText


class AdGroupFactory(BaseModelFactory, factory.django.DjangoModelFactory):
    class Meta:
        model = AdGroup

    ad_group_id = FuzzyText
    ad_group_name = FuzzyText
    campaign = factory.SubFactory('campaign.tests.factories.CampaignFactory')
