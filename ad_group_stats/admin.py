from django.contrib import admin

from ad_group_stats.models import AdGroupStat


class AdGroupStatAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'ad_group_name',
        'device',
        'impressions',
        'clicks',
        'conversions',
        'cost',
        'created_at',
    )

    def ad_group_name(self, obj):
        return obj.ad_group.ad_group_name


admin.site.register(AdGroupStat, AdGroupStatAdmin)
