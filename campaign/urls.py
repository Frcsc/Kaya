from django.urls import path

from campaign.api import CampaignListAPIView, CampaignPatchAPIView

app_name = 'campaign'

urlpatterns = [
    path('campaigns', CampaignListAPIView.as_view(), name="campaign"),
    path(
        'campaign/<str:campaign_id>',
        CampaignPatchAPIView.as_view(),
        name="campaign-patch",
    ),
]
