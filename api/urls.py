from django.urls import include, path

app_name = 'api'

urlpatterns = [
    # path('v1/ad-group', include('ad_group.urls', namespace='ad-group')),
    path(
        'v1/ad-group-stats/', include('ad_group_stats.urls', namespace='ad-group-stats')
    ),
    path('v1/campaign', include('campaign.urls', namespace='campaign')),
    path('v1/user/', include('user.urls', namespace='user')),
]
