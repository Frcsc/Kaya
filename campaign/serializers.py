from rest_framework import serializers

from ad_group.models import AdGroup
from campaign.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            'campaign_id',
            'campaign_name',
            'campaign_type',
            'number_of_ad_groups',
            'average_monthly_cost',
            'cost_per_conversion',
            'ad_groups',
        )

    class AdGroupSerializer(serializers.ModelSerializer):
        class Meta:
            model = AdGroup
            fields = (
                'ad_group_id',
                'ad_group_name',
                'average_monthly_cost',
                'cost_per_conversion',
            )

    ad_groups = AdGroupSerializer(source='adgroup_set', many=True)


class PatchCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('campaign_name',)

    def update(self, instance, validated_data):
        instance.campaign_name = validated_data['campaign_name']
        instance.save()
        return instance
