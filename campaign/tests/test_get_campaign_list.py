from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ad_group.tests.factories import AdGroupFactory
from ad_group_stats.tests.factories import AdGroupStatFactory
from campaign.models import Campaign
from campaign.tests.factories import CampaignFactory


class CampaignListTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('all:campaign:campaign')
        self.fields = {
            'campaign_id',
            'campaign_name',
            'campaign_type',
            'number_of_ad_groups',
            'average_monthly_cost',
            'cost_per_conversion',
            'ad_groups',
        }

    def tearDown(self):
        super().tearDown()
        cache.clear()

    def test_get_list_of_campaigns_when_databse_is_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data)

    def test_get_campaign_with_no_ad_groups(self):
        CampaignFactory.create_batch(3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        queryset = Campaign.objects.all()

        self.assertEqual(len(data), 3)
        for datum in data:
            self.assertEqual(self.fields, set(datum.keys()))
            campaign = queryset.get(campaign_id=datum.get('campaign_id'))
            self.assertEqual(datum.get('ad_groups'), [])
            self.assertEqual(datum.get('number_of_ad_groups'), 0)
            self.assertEqual(
                campaign.average_monthly_cost, datum.get('average_monthly_cost')
            )
            self.assertEqual(
                campaign.cost_per_conversion, datum.get('cost_per_conversion')
            )

    def test_get_campaign_with_ad_group_but_not_stats(self):
        AdGroupFactory()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        queryset = Campaign.objects.all()

        self.assertEqual(1, len(data))

        for datum in data:
            self.assertEqual(self.fields, set(datum.keys()))
            campaign = queryset.get(campaign_id=datum.get('campaign_id'))
            self.assertEqual(
                campaign.average_monthly_cost, datum.get('average_monthly_cost')
            )
            self.assertEqual(
                campaign.cost_per_conversion, datum.get('cost_per_conversion')
            )

            ad_groups = campaign.adgroup_set.all()

            for group in datum.get('ad_groups'):
                ad_group = ad_groups.get(ad_group_id=group.get('ad_group_id'))

                self.assertEqual(
                    group.get('average_monthly_cost'), ad_group.average_monthly_cost
                )
                self.assertEqual(
                    group.get('cost_per_conversion'), ad_group.cost_per_conversion
                )

    def test_get_multiple_campaign_with_ad_group_and_stats(self):
        AdGroupStatFactory.create_batch(5)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        queryset = Campaign.objects.all()
        data = response.data

        self.assertEqual(5, len(data))

        for datum in data:
            self.assertEqual(self.fields, set(datum.keys()))
            campaign = queryset.get(campaign_id=datum.get('campaign_id'))
            self.assertEqual(
                campaign.average_monthly_cost, datum.get('average_monthly_cost')
            )
            self.assertEqual(
                campaign.cost_per_conversion, datum.get('cost_per_conversion')
            )

            ad_groups = campaign.adgroup_set.all()

            for group in datum.get('ad_groups'):
                ad_group = ad_groups.get(ad_group_id=group.get('ad_group_id'))

                self.assertEqual(
                    group.get('average_monthly_cost'), ad_group.average_monthly_cost
                )
                self.assertEqual(
                    group.get('cost_per_conversion'), ad_group.cost_per_conversion
                )
