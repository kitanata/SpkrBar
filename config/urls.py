from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.views import SpeakerList
from talks.views import TalkList

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TalkList.as_view()),
    url(r'^talk/new/$', 'talks.views.talk_new'),
    url(r'^talk/(?P<talk_id>\d+)/$', 'talks.views.talk_detail'),

    url(r'^speakers/$', SpeakerList.as_view()),
    url(r'^speaker/(?P<speaker_id>\d+)/$', 'core.views.speaker_detail'),

    url(r'^profile/$', 'core.views.profile'),
    url(r'^profile/edit/$', 'core.views.profile_edit'),
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
