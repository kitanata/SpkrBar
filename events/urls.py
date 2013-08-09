from django.conf.urls import patterns, url
from views import EventList, EventDetail

urlpatterns = patterns('',
    url(r'rest_events$', EventList.as_view()),
    url(r'rest_event/(?P<pk>\d+)$', EventDetail.as_view()),

    url(r'events$', 'events.views.event_list'),
    url(r'event/new$', 'events.views.event_new'),
    url(r'event/(?P<event_id>\d+)/edit$', 'events.views.event_edit'),
    url(r'event/(?P<event_id>\d+)/delete$', 'events.views.event_delete'),
    url(r'event/(?P<event_id>\d+)/attend$', 'events.views.event_attendee_new'),
    url(r'event/(?P<event_id>\d+)/open$', 'events.views.event_open'),
    url(r'event/(?P<event_id>\d+)/close$', 'events.views.event_close'),
    url(r'event/(?P<event_id>\d+)/endorse$', 'events.views.event_endorsement_new'),
    url(r'event/(?P<event_id>\d+)$', 'events.views.event_detail'),
)
