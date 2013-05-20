from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'events.views.event_list'),
    url(r'^event/(?P<event_id>\d+)/$', 'events.views.event_detail'),
    url(r'^event/(?P<event_id>\d+)/edit/$', 'events.views.event_edit'),
    url(r'^event/(?P<event_id>\d+)/delete/$', 'events.views.event_delete'),
    url(r'^event/(?P<event_id>\d+)/attend/$', 'events.views.event_attendee_new'),
    url(r'^talk/(?P<talk_id>\d+)/event/new/$', 'events.views.event_new'),

    url(r'^talk/new/$', 'talks.views.talk_new'),
    url(r'^talk/(?P<talk_id>\d+)/$', 'talks.views.talk_detail'),
    url(r'^talk/(?P<talk_id>\d+)/edit/$', 'talks.views.talk_edit'),
    url(r'^talk/(?P<talk_id>\d+)/delete/$', 'talks.views.talk_delete'),

    url(r'^talk/(?P<talk_id>\d+)/tag/new/$', 'talks.views.talk_tag_new'),
    url(r'^talk/(?P<talk_id>\d+)/comment/new/$', 'talks.views.talk_comment_new'),
    url(r'^talk/(?P<talk_id>\d+)/endorse/$', 'talks.views.talk_endorsement_new'),
    url(r'^talk/(?P<talk_id>\d+)/publish/$', 'talks.views.talk_publish'),
    url(r'^talk/(?P<talk_id>\d+)/archive/$', 'talks.views.talk_archive'),

    url(r'^speakers/$', 'core.views.speakers'),
    url(r'^speaker/(?P<username>\w+)/$', 'core.views.speaker_detail'),
    url(r'^speaker/(?P<username>\w+)/follow/$', 'core.views.speaker_follow'),

    url(r'^profile/edit/$', 'core.views.profile_edit'),
    url(r'^profile/edit/photo/$', 'core.views.profile_edit_photo'),
    url(r'^profile/edit/link/new/$', 'core.views.profile_link_new'),
    url(r'^profile/edit/tag/new/$', 'core.views.profile_tag_new'),
    url(r'^profile/publish/$', 'core.views.profile_publish'),
    url(r'^profile/archive/$', 'core.views.profile_archive'),

    url(r'^locations/$', 'locations.views.locations'),
    url(r'^location/new/$', 'locations.views.location_new'),
    url(r'^location/(?P<location_id>\d+)/$', 'locations.views.location'),

    url(r'^load_fixtures/$', 'core.views.load_fixtures'),

    url(r'^login/$', 'core.views.login_user'),
    url(r'^logout/$', 'core.views.logout_user'),
    url(r'^register/$', 'core.views.register_user'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
