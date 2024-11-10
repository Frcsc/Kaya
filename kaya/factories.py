import factory
from django.utils import timezone
from factory import fuzzy

from kaya.models import BaseModel


class BaseModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseModel
        abstract = True

    created_at = fuzzy.FuzzyDateTime(start_dt=timezone.now())
    updated_at = fuzzy.FuzzyDateTime(start_dt=timezone.now())


FuzzyText = fuzzy.FuzzyText(length=50)
FuzzyIntger = fuzzy.FuzzyInteger(low=0, high=1000)
FuzzyDecimal = fuzzy.FuzzyDecimal(0.00, 3000.00, 6)
