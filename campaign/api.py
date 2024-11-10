from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from campaign.models import Campaign
from campaign.serializers import CampaignSerializer, PatchCampaignSerializer
from user.permissions import AllowAnyPermission


class CampaignListAPIView(AllowAnyPermission, ListAPIView):
    queryset = Campaign.objects.all().order_by('-campaign_id')
    serializer_class = CampaignSerializer


class CampaignPatchAPIView(AllowAnyPermission, APIView):
    serializer_class = PatchCampaignSerializer

    def patch(self, request, *args, **kwargs):
        campaign_id = kwargs['campaign_id']
        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response(
                {"message": "Campaign not found", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PatchCampaignSerializer(campaign, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successful", "data": serializer.data},
            status=status.HTTP_404_NOT_FOUND,
        )
