from django.conf.urls import patterns, url
from views import EngagementList, EngagementDetail

urlpatterns = patterns('',
    url(r'^rest/engagements$', EngagementList.as_view()),
    url(r'^rest/engagement/(?P<pk>\d*)$', EngagementDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/engagement$', EngagementDetail.as_view(
        actions={'post': 'create'})),
)
