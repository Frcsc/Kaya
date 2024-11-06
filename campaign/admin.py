from django.contrib import admin

from campaign.models import Campaign


class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        'campaign_id',
        'campaign_name',
        'campaign_type',
        'created_at',
    )


admin.site.register(Campaign, CampaignAdmin)
