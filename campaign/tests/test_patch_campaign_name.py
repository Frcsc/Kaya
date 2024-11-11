from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ad_group.tests.factories import AdGroupFactory
from ad_group_stats.tests.factories import AdGroupStatFactory
from campaign.models import Campaign
from campaign.tests.factories import CampaignFactory
from kaya.factories import FuzzyIntger, FuzzyText


class CampaignPatchTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.data = {"campaign_name": FuzzyText.fuzz()}

    def tearDown(self):
        super().tearDown()
        cache.clear()

    def test_patch_campaign_name_without_data(self):
        campaign = CampaignFactory()
        url = reverse(
            'all:campaign:campaign-patch', kwargs={'campaign_id': campaign.campaign_id}
        )
        response = self.client.patch(url)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('campaign_name', response.data)
        self.assertEqual(
            response.data.get('campaign_name')[0], 'This field is required.'
        )

    def test_patch_campaign_name_bad_data(self):
        campaign = CampaignFactory()
        url = reverse(
            'all:campaign:campaign-patch', kwargs={'campaign_id': campaign.campaign_id}
        )
        response = self.client.patch(url, data={"campaign_name": ""})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('campaign_name', response.data)
        self.assertEqual(
            response.data.get('campaign_name')[0], 'This field may not be blank.'
        )

    def test_patch_campaign_name_with_non_existent_id(self):
        url = reverse(
            'all:campaign:campaign-patch', kwargs={'campaign_id': FuzzyText.fuzz()}
        )
        response = self.client.patch(url, data=self.data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get('message'), "Campaign not found")
        self.assertEqual(response.data.get('data'), [])

    def test_patch_campaign_name_success(self):
        campaign = CampaignFactory()
        url = reverse(
            'all:campaign:campaign-patch', kwargs={'campaign_id': campaign.campaign_id}
        )
        response = self.client.patch(url, data=self.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get('message'), "Successful")
        self.assertEqual(
            self.data.get('campaign_name'),
            response.data.get('data').get('campaign_name'),
        )

        campaign.refresh_from_db()
        self.assertEqual(self.data.get('campaign_name'), campaign.campaign_name)
