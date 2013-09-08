from django.conf.urls import patterns, url
from views import EngagementList, EngagementDetail

urlpatterns = patterns('',
    url(r'^engagements$', EngagementList.as_view()),
    url(r'^engagement/(?P<pk>\d*)$', EngagementDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^engagement$', EngagementDetail.as_view(
        actions={'post': 'create'})),

    url(r'^talk_event/(?P<talk_event_id>\d+)/attend$', 'talkevents.views.talk_event_attendee_new'),
)
