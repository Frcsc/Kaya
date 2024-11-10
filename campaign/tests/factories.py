import factory
from factory import fuzzy

from campaign.models import Campaign
from kaya.factories import BaseModelFactory, FuzzyText


class CampaignFactory(BaseModelFactory, factory.django.DjangoModelFactory):
    class Meta:
        model = Campaign

    campaign_id = FuzzyText
    campaign_name = FuzzyText
    campaign_type = fuzzy.FuzzyChoice(['SEARCH_STANDARD', 'VIDEO_RESPONSIVE'])
