from django.db.models import Case, DecimalField, F, Sum, Value, When
from django.db.models.functions import Cast

from ad_group_stats.utils import quantize_two_decimal_places


class CampaignPerformanceMixin:
    def get_aggregated_queryset(self, queryset, aggregate_period):
        return (
            queryset.annotate(period=aggregate_period)
            .values('period')
            .annotate(
                total_cost=Sum('cost'),
                total_clicks=Sum('clicks'),
                total_conversions=Sum('conversions'),
                total_impressions=Sum('impressions'),
            )
            .annotate(
                average_cost_per_click=Case(
                    When(total_clicks=0, then=Value(None)),
                    default=F('total_cost') / F('total_clicks'),
                    output_field=DecimalField(decimal_places=2),
                ),
                average_cost_per_conversion=Case(
                    When(total_conversions=0, then=Value(None)),
                    default=F('total_cost') / F('total_conversions'),
                    output_field=DecimalField(decimal_places=2),
                ),
                average_click_through_rate=Case(
                    When(total_impressions=0, then=Value(None)),
                    default=F('total_clicks')
                    / Cast(
                        F('total_impressions'),
                        DecimalField(max_digits=10, decimal_places=2),
                    ),
                    output_field=DecimalField(decimal_places=2),
                ),
                average_conversion_rate=Case(
                    When(total_clicks=0, then=Value(None)),
                    default=F('total_conversions') / F('total_clicks'),
                    output_field=DecimalField(decimal_places=2),
                ),
            )
        )

    def get_performance_data(self, queryset, aggregate_period):
        aggregated_queryset = self.get_aggregated_queryset(queryset, aggregate_period)

        return [
            {
                "total_cost": quantize_two_decimal_places(item['total_cost']),
                "total_clicks": item['total_clicks'],
                "total_conversions": quantize_two_decimal_places(
                    item['total_conversions']
                )
                if item['total_conversions'] is not None
                else None,
                "average_cost_per_click": quantize_two_decimal_places(
                    item['average_cost_per_click']
                )
                if item['average_cost_per_click'] is not None
                else None,
                "average_cost_per_conversion": quantize_two_decimal_places(
                    item['average_cost_per_conversion']
                )
                if item['average_cost_per_conversion'] is not None
                else None,
                "average_click_through_rate": quantize_two_decimal_places(
                    item['average_click_through_rate']
                )
                if item['average_click_through_rate'] is not None
                else None,
                "average_conversion_rate": quantize_two_decimal_places(
                    item['average_conversion_rate']
                )
                if item['average_conversion_rate'] is not None
                else None,
            }
            for item in aggregated_queryset
        ]


class CompareCampaignPerformanceMixin:
    def get_total_cost_clicks_conversions_impressions(self, queryset):
        data = queryset.aggregate(
            total_cost=Sum('cost'),
            total_clicks=Sum('clicks'),
            total_conversions=Sum('conversions'),
            total_impressions=Sum('impressions'),
        )
        data['total_cost'] = quantize_two_decimal_places(data['total_cost'])
        data['total_conversions'] = quantize_two_decimal_places(
            data['total_conversions']
        )
        return data

    def get_averages_and_rates_for_a_period(self, queryset):
        data = self.get_total_cost_clicks_conversions_impressions(queryset)

        total_cost = data.get('total_cost')
        total_clicks = data.get('total_clicks')
        total_conversions = data.get('total_conversions')
        total_impressions = data.get('total_impressions')

        data.update(
            {
                'cost_per_click': quantize_two_decimal_places(
                    (total_cost / total_clicks)
                )
                if total_clicks
                else None,
                'cost_per_conversion': quantize_two_decimal_places(
                    (total_cost / total_conversions)
                )
                if total_conversions
                else None,
                'cost_per_mille_impression': quantize_two_decimal_places(
                    ((total_cost / total_impressions) * 1000)
                )
                if total_impressions
                else None,
                'click_through_rate': quantize_two_decimal_places(
                    (total_clicks / total_impressions)
                )
                if total_impressions
                else None,
                'conversion_rate': quantize_two_decimal_places(
                    (total_conversions / total_clicks)
                )
                if total_clicks
                else None,
            }
        )

        return data
