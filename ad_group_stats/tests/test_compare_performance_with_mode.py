from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ad_group.tests.factories import AdGroupFactory
from ad_group_stats.models import AdGroupStat
from ad_group_stats.tests.factories import AdGroupStatFactory
from kaya.factories import FuzzyText


class CompareCampaignPerformanceListTestCase(APITestCase):
    def setUp(self):
        self.ad_group = AdGroupFactory()
        self.today = date.today()
        self.current_ad_group_stat = AdGroupStatFactory(
            date=self.today,
            ad_group=self.ad_group,
        )

        self.previous_ad_group_stat = AdGroupStatFactory(
            date=self.today - timedelta(days=7),
            ad_group=self.ad_group,
        )
        self.url = reverse('all:ad-group-stats:compare-performance')

    def test_compare_campaign_performance_bad_mode(self):
        response = self.client.get(
            self.url,
            {
                'compare_mode': FuzzyText.fuzz(),
                'start_date': self.today - timedelta(days=7),
                'end_date': self.today,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('message'), 'Invalid comparison mode provided.'
        )
        self.assertEqual(response.data.get('data'), [])

    def test_compare_campaign_performance_no_current_preceding(self):
        AdGroupStat.objects.filter(id=self.current_ad_group_stat.id).delete()

        response = self.client.get(
            self.url,
            {
                'compare_mode': 'preceding',
                'start_date': self.today,
                'end_date': self.today,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('message'),
            'Please select a different date combination for current metrics',
        )
        self.assertEqual(response.data.get('data'), [])

    def test_compare_campaign_performance_no_previous_preceding(self):
        AdGroupStat.objects.filter(id=self.previous_ad_group_stat.id).delete()

        response = self.client.get(
            self.url,
            {
                'compare_mode': 'preceding',
                'start_date': self.today,
                'end_date': self.today,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('message'),
            'No previous data exists for comparison',
        )
        self.assertEqual(response.data.get('data'), [])

    def test_compare_campaign_performance_no_current_previous_month(self):
        AdGroupStat.objects.filter(id=self.current_ad_group_stat.id).delete()

        response = self.client.get(
            self.url,
            {
                'compare_mode': 'previous_month',
                'start_date': self.today,
                'end_date': self.today,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('message'),
            'Please select a different date combination for current metrics',
        )
        self.assertEqual(response.data.get('data'), [])

    def test_compare_campaign_performance_previous_preceding(self):
        dates_to_create = [
            self.today,
            self.today - timedelta(days=1),
            self.today - timedelta(days=2),
            self.today - timedelta(days=3),
            self.today - timedelta(days=3),
            self.today - timedelta(days=4),
        ]
        for date_value in dates_to_create:
            AdGroupStatFactory(date=date_value, ad_group=self.ad_group)
        response = self.client.get(
            self.url,
            {
                'compare_mode': 'preceding',
                'start_date': self.today - timedelta(days=2),
                'end_date': self.today,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_compare_campaign_performance_previous_month(self):
        previous_month_date = self.today - relativedelta(months=1)
        first_day_previous_month = previous_month_date.replace(day=1)

        dates_to_create = [
            first_day_previous_month,
            first_day_previous_month + timedelta(days=8),
            first_day_previous_month + timedelta(days=9),
            first_day_previous_month + timedelta(days=10),
            first_day_previous_month + timedelta(days=11),
            first_day_previous_month + timedelta(days=12),
        ]

        for date_value in dates_to_create:
            AdGroupStatFactory(date=date_value, ad_group=self.ad_group)

        response = self.client.get(
            self.url,
            {
                'compare_mode': 'previous_month',
                'start_date': self.today - timedelta(days=2),
                'end_date': self.today,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
