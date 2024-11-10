from django.urls import path

from campaign.api import CampaignListAPIView, CampaignPatchAPIView

app_name = 'campaign'

urlpatterns = [
    path('', CampaignListAPIView.as_view(), name="campaign-list"),
    path('<int:campaign_id>', CampaignPatchAPIView.as_view(), name="campaign-patch"),
]
