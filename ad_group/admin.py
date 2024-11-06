from django.contrib import admin

from ad_group.models import AdGroup


class AdGroupAdmin(admin.ModelAdmin):
    list_display = (
        'ad_group_id',
        'ad_group_name',
        'campaign_name',
        'created_at',
    )

    def campaign_name(self, obj):
        return obj.campaign.campaign_name


admin.site.register(AdGroup, AdGroupAdmin)
