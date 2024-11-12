from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path(
        'ad-group-stats/v1/', include('ad_group_stats.urls', namespace='ad-group-stats')
    ),
    path('campaign/v1/', include('campaign.urls', namespace='campaign')),
    path('user/v1/', include('user.urls', namespace='user')),
]
