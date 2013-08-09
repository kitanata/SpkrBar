from django.conf.urls import patterns, url
from views import EngagementList, EngagementDetail

urlpatterns = patterns('',
    url(r'engagements$', EngagementList.as_view()),
    url(r'engagement/(?P<pk>\d*)$', EngagementDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'engagement$', EngagementDetail.as_view(
        actions={'post': 'create'})),
)
