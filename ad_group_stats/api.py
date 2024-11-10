from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from ad_group_stats.filters import (
    CampaignPerformanceFilter,
    CompareCampaignPerformanceFilter,
)
from ad_group_stats.mixins import (
    CampaignPerformanceMixin,
    CompareCampaignPerformanceMixin,
)
from ad_group_stats.models import AdGroupStat
from ad_group_stats.pagination import CampaignPerformancePagination
from ad_group_stats.serializers import (
    CompareCampaignPerformanceSerializer,
    PerformanceTimeSeriesSerializer,
)
from ad_group_stats.utils import (
    AGGREGATE_BY,
    COMPARE_MODE,
    aggregate_map,
    get_previouse_dates,
)
from user.permissions import AllowAnyPermission


class CampaignPerformanceListView(
    AllowAnyPermission, CampaignPerformanceMixin, ListAPIView
):
    pagination_class = CampaignPerformancePagination
    filterset_class = CampaignPerformanceFilter

    def get_queryset(self):
        return self.filter_queryset(AdGroupStat.objects.all())

    def list(self, request, *args, **kwargs):
        aggregate_by = request.query_params.get('aggregate_by')

        if not aggregate_by or aggregate_by not in AGGREGATE_BY:
            return Response(
                {"message": "Invalid aggregation param.", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset()
        performance_data = self.get_performance_data(
            queryset, aggregate_map(aggregate_by)
        )

        return self.pagination_class().paginate_and_respond(
            performance_data, PerformanceTimeSeriesSerializer, request
        )


class CompareCampaignPerformanceListView(
    AllowAnyPermission, CompareCampaignPerformanceMixin, ListAPIView
):
    filterset_class = CompareCampaignPerformanceFilter
    serializer_class = CompareCampaignPerformanceSerializer
    pagination_class = CampaignPerformancePagination

    def get_queryset(self):
        return self.filter_queryset(AdGroupStat.objects.all())

    def get_previous_queryset(self, start_date, end_date, compare_mode):
        previous_start_date, previous_end_date = get_previouse_dates(
            parse_date(start_date), parse_date(end_date), compare_mode
        )
        return (
            previous_start_date,
            previous_end_date,
            AdGroupStat.objects.filter(
                date__range=(previous_start_date, previous_end_date)
            ),
        )

    def list(self, request, *args, **kwargs):
        compare_mode = request.query_params.get('compare_mode')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not compare_mode or compare_mode not in COMPARE_MODE:
            return Response(
                {"message": "Invalid comparison mode provided.", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset()
        (
            previous_start_date,
            previous_end_date,
            previous_queryset,
        ) = self.get_previous_queryset(start_date, end_date, compare_mode)

        if not queryset:
            return Response(
                {
                    "message": "Please select a different date combination for current metrics",
                    "data": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not previous_queryset:
            return Response(
                {"message": "No previous data exists for comparison", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current = self.get_averages_and_rates_for_a_period(queryset)
        before = self.get_averages_and_rates_for_a_period(previous_queryset)

        data = {
            key: {"current": current[key], "previous": before[key]}
            for key in current.keys()
        }

        return Response(
            {
                "message": "successful",
                "previous_period": f'{previous_start_date} - {previous_end_date}',
                "data": self.get_serializer(data).data,
            }
        )
