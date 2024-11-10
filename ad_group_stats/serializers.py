import logging
from decimal import InvalidOperation

from rest_framework import serializers

from ad_group_stats.utils import quantize_two_decimal_places

logger = logging.getLogger(__name__)


class PerformanceTimeSeriesSerializer(serializers.Serializer):
    total_cost = serializers.DecimalField(max_digits=22, decimal_places=4)
    total_clicks = serializers.IntegerField()
    total_conversions = serializers.DecimalField(max_digits=22, decimal_places=4)
    average_cost_per_click = serializers.DecimalField(
        max_digits=22, decimal_places=2, required=False, allow_null=True
    )
    average_cost_per_conversion = serializers.DecimalField(
        max_digits=22, decimal_places=2, required=False, allow_null=True
    )
    average_click_through_rate = serializers.DecimalField(
        max_digits=22, decimal_places=4, required=False, allow_null=True
    )
    average_conversion_rate = serializers.DecimalField(
        max_digits=22, decimal_places=4, required=False, allow_null=True
    )


class CompareBaseSerializer(serializers.Serializer):
    change_percentage = serializers.SerializerMethodField()

    def get_change_percentage(self, obj):
        current = obj.get("current")
        previous = obj.get("previous")

        if current is not None and previous is not None:
            try:
                change = (current - previous) / previous
                return quantize_two_decimal_places(change)
            except (InvalidOperation, ZeroDivisionError) as e:
                logger.error(
                    f"Error calculating change: {e}, current: {current}, previous: {previous}"
                )
                return None
        return None


class CompareDecimalBaseSerializer(CompareBaseSerializer):
    current = serializers.DecimalField(
        max_digits=22, decimal_places=4, required=False, allow_null=True
    )
    previous = serializers.DecimalField(
        max_digits=22, decimal_places=4, required=False, allow_null=True
    )


class CompareIntegerBaseSerializer(CompareBaseSerializer):
    current = serializers.IntegerField()
    previous = serializers.IntegerField()


class CompareCampaignPerformanceSerializer(serializers.Serializer):
    cost_per_conversion = CompareDecimalBaseSerializer()
    cost_per_click = CompareDecimalBaseSerializer()
    cost_per_mille_impression = CompareDecimalBaseSerializer()
    conversion_rate = CompareDecimalBaseSerializer()
    click_through_rate = CompareDecimalBaseSerializer()
    total_conversions = CompareDecimalBaseSerializer()
    total_cost = CompareDecimalBaseSerializer()
    total_clicks = CompareIntegerBaseSerializer()
