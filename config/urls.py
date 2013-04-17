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

    url(r'^speakers/$', SpeakerList.as_view()),
    url(r'^speaker/(?P<username>\w+)/$', 'core.views.speaker_detail'),
    url(r'^speaker/(?P<username>\w+)/talks/$', 'core.views.speaker_talks'),

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
