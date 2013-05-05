from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.views import SpeakerList

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'talks.views.talk_list'),
    url(r'^talk/new/$', 'talks.views.talk_new'),
    url(r'^talk/(?P<talk_id>\d+)/$', 'talks.views.talk_detail'),
    url(r'^talk/(?P<talk_id>\d+)/edit/$', 'talks.views.talk_edit'),
    url(r'^talk/(?P<talk_id>\d+)/delete/$', 'talks.views.talk_delete'),

    url(r'^talk/(?P<talk_id>\d+)/tag/new/$', 'talks.views.talk_tag_new'),
    url(r'^talk/(?P<talk_id>\d+)/comment/new/$', 'talks.views.talk_comment_new'),
    url(r'^talk/(?P<talk_id>\d+)/attend/$', 'talks.views.talk_attendee_new'),
    url(r'^talk/(?P<talk_id>\d+)/endorse/$', 'talks.views.talk_endorsement_new'),
    url(r'^talk/(?P<talk_id>\d+)/publish/$', 'talks.views.talk_publish'),
    url(r'^talk/(?P<talk_id>\d+)/archive/$', 'talks.views.talk_archive'),

    url(r'^location/new/$', 'talks.views.location_new'),

    url(r'^speakers/$', SpeakerList.as_view()),
    url(r'^speaker/(?P<username>\w+)/$', 'core.views.speaker_detail'),
    url(r'^speaker/(?P<username>\w+)/follow/$', 'core.views.speaker_follow'),

    url(r'^profile/edit/$', 'core.views.profile_edit'),
    url(r'^profile/edit/photo/$', 'core.views.profile_edit_photo'),
    url(r'^profile/edit/link/new/$', 'core.views.profile_link_new'),
    url(r'^profile/edit/tag/new/$', 'core.views.profile_tag_new'),

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
