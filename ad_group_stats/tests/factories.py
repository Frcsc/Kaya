import factory
from django.utils import timezone
from factory import fuzzy

from ad_group_stats.models import AdGroupStat
from kaya.factories import BaseModelFactory, FuzzyDecimal, FuzzyIntger


class AdGroupStatFactory(BaseModelFactory, factory.django.DjangoModelFactory):
    class Meta:
        model = AdGroupStat

    date = fuzzy.FuzzyAttribute(lambda: timezone.localtime().date())
    ad_group = factory.SubFactory('ad_group.tests.factories.AdGroupFactory')
    device = fuzzy.FuzzyChoice(['MOBILE', 'TABLET', 'DESKTOP'])
    impressions = FuzzyIntger
    clicks = FuzzyIntger
    conversions = FuzzyDecimal
    cost = FuzzyDecimal
