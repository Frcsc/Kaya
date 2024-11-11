from django.urls import path

from ad_group_stats.api import (
    CampaignPerformanceListView,
    CompareCampaignPerformanceListView,
)

app_name = 'ad_group_stats'

urlpatterns = [
    path(
        'performance-time-series',
        CampaignPerformanceListView.as_view(),
        name="performance",
    ),
    path(
        'compare-performance',
        CompareCampaignPerformanceListView.as_view(),
        name="compare-performance",
    ),
]
