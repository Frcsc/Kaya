from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ad_group_stats.models import AdGroupStat
from ad_group_stats.tests.factories import AdGroupStatFactory
from ad_group_stats.utils import quantize_two_decimal_places
from kaya.factories import FuzzyText


class CampaignPerformanceListTestCase(APITestCase):
    def setUp(self):

        self.url = reverse('all:ad-group-stats:performance')
        self.fields = {
            'total_cost',
            'total_clicks',
            'total_conversions',
            'average_cost_per_click',
            'average_cost_per_conversion',
            'average_click_through_rate',
            'average_conversion_rate',
        }
        self.today = date.today()
        self.start_date = self.today - timedelta(days=7)
        self.end_date = self.today - timedelta(days=5)

    def test_no_aggregate_by_param_provided(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Invalid aggregation param.")
        self.assertEqual(response.data['data'], [])

    def test_invalid_aggregate_by_param_provided(self):
        response = self.client.get(self.url, {"aggregate_by": FuzzyText.fuzz()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Invalid aggregation param.")
        self.assertEqual(response.data['data'], [])

    def test_aggregate_by_day(self):
        AdGroupStatFactory.create_batch(5)
        AdGroupStatFactory.create_batch(3)
        response = self.client.get(self.url, {'aggregate_by': 'day'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data.get('message'), 'Successful')
        self.assertTrue(len(data.get("data")) > 0)

        for datum in data.get('data'):

            self.assertEqual(self.fields, set(datum.keys()))

    def test_aggregate_by_week(self):
        AdGroupStatFactory.create_batch(5)
        AdGroupStatFactory.create_batch(3)
        response = self.client.get(self.url, {'aggregate_by': 'week'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data.get('message'), 'Successful')
        self.assertTrue(len(data.get("data")) > 0)

        for datum in data.get('data'):

            self.assertEqual(self.fields, set(datum.keys()))

    def test_aggregate_by_month(self):
        AdGroupStatFactory.create_batch(5)
        AdGroupStatFactory.create_batch(3)
        response = self.client.get(self.url, {'aggregate_by': 'week'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data.get('message'), 'Successful')
        self.assertTrue(len(data.get("data")) > 0)

        for datum in data.get('data'):

            self.assertEqual(self.fields, set(datum.keys()))

    def test_filter_by_date_range(self):
        stats_1 = AdGroupStatFactory(date=self.start_date)
        stats_2 = AdGroupStatFactory(date=self.end_date)

        total_cost_1 = quantize_two_decimal_places(stats_1.cost)
        total_cost_2 = quantize_two_decimal_places(stats_2.cost)
        total_conversion_1 = quantize_two_decimal_places(stats_1.conversions)
        total_conversion_2 = quantize_two_decimal_places(stats_2.conversions)
        total_clicks_1 = quantize_two_decimal_places(stats_1.clicks)
        total_clicks_2 = quantize_two_decimal_places(stats_2.clicks)
        total_impressions_1 = quantize_two_decimal_places(stats_1.impressions)
        total_impressions_2 = quantize_two_decimal_places(stats_2.impressions)

        # Filtered out instance
        AdGroupStatFactory(
            date=self.today - timedelta(days=2),
        )

        response = self.client.get(
            self.url,
            {
                'aggregate_by': 'day',
                'start_date': (self.start_date).isoformat(),
                'end_date': (self.end_date).isoformat(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AdGroupStat.objects.count(), 3)
        data = response.data.get('data')

        self.assertEqual(
            {stats_1.clicks, stats_2.clicks}, {s.get('total_clicks') for s in data}
        )
        self.assertEqual(
            {total_cost_1, total_cost_2},
            {s.get('total_cost') for s in data},
        )
        self.assertEqual(
            {total_conversion_1, total_conversion_2},
            {s.get('total_conversions') for s in data},
        )
        self.assertEqual(
            {
                quantize_two_decimal_places(total_cost_1 / total_clicks_1),
                quantize_two_decimal_places(total_cost_2 / total_clicks_2),
            },
            {s.get('average_cost_per_click') for s in data},
        )
        self.assertEqual(
            {
                quantize_two_decimal_places(total_cost_1 / total_conversion_1),
                quantize_two_decimal_places(total_cost_2 / total_conversion_2),
            },
            {s.get('average_cost_per_conversion') for s in data},
        )
        self.assertEqual(
            {
                quantize_two_decimal_places(total_clicks_1 / total_impressions_1),
                quantize_two_decimal_places(total_clicks_2 / total_impressions_2),
            },
            {s.get('average_click_through_rate') for s in data},
        )
        self.assertEqual(
            {
                quantize_two_decimal_places(total_conversion_1 / total_clicks_1),
                quantize_two_decimal_places(total_conversion_2 / total_clicks_2),
            },
            {s.get('average_conversion_rate') for s in data},
        )

    def test_filter_by_campaigns(self):
        ad_group_stat_1 = AdGroupStatFactory(date=self.today + timedelta(2))
        ad_group_stat_2 = AdGroupStatFactory()
        response = self.client.get(
            self.url,
            {
                'aggregate_by': 'day',
                'campaigns': f"{ad_group_stat_1.ad_group.campaign.campaign_id},{ad_group_stat_2.ad_group.campaign.campaign_id}",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('data')), 2)
