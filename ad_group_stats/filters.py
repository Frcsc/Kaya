from django_filters import rest_framework as filters

from ad_group_stats.models import AdGroupStat


class CampaignPerformanceFilter(filters.FilterSet):
    campaigns = filters.CharFilter(
        method='filter_campaigns',
        help_text="Comma-separated list of campaign IDs to filter by.",
    )
    start_date = filters.DateFilter(
        field_name='date', lookup_expr='gte', required=False
    )
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte', required=False)

    class Meta:
        model = AdGroupStat
        fields = ['campaigns', 'start_date', 'end_date']

    def filter_campaigns(self, queryset, name, value):
        campaign_ids = value.split(',')
        return queryset.filter(ad_group__campaign__campaign_id__in=campaign_ids)


class CompareCampaignPerformanceFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte', required=True)
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte', required=True)

    class Meta:
        model = AdGroupStat
        fields = ['start_date', 'end_date']
