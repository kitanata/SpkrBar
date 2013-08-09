import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.index'),
    url(r'^search$', 'core.views.search'),
    url(r'^mobile', include('mobile.urls')),

    url(r'^', include('events.urls')),

    url(r'^talk/new$', 'talks.views.talk_new'),
    url(r'^talk/(?P<talk_id>\d+)$', 'talks.views.talk_detail'),
    url(r'^talk/(?P<talk_id>\d+)/edit$', 'talks.views.talk_edit'),
    url(r'^talk/(?P<talk_id>\d+)/delete$', 'talks.views.talk_delete'),

    url(r'^talk/(?P<talk_id>\d+)/tag/new/$', 'talks.views.talk_tag_new'),
    url(r'^talk/(?P<talk_id>\d+)/tag/(?P<tag_id>\d+)/delete$', 'talks.views.talk_tag_delete'),
    url(r'^talk/(?P<talk_id>\d+)/comment/new$', 'talks.views.talk_comment_new'),
    url(r'^talk/(?P<talk_id>\d+)/rate$', 'talks.views.talk_rate_new'),
    url(r'^talk/(?P<talk_id>\d+)/endorse$', 'talks.views.talk_endorsement_new'),
    url(r'^talk/(?P<talk_id>\d+)/publish$', 'talks.views.talk_publish'),
    url(r'^talk/(?P<talk_id>\d+)/archive$', 'talks.views.talk_archive'),

    url(r'^talk/(?P<talk_id>\d+)/recruit$', 'talks.views.talk_recruit'),
    url(r'^talk/(?P<talk_id>\d+)/submit$', 'talks.views.talk_submit'),

    url(r'^talk/(?P<talk_id>\d+)/slides/new$', 'talks.views.talk_slides_new'),
    url(r'^talk/(?P<talk_id>\d+)/video/new$', 'talks.views.talk_video_new'),
    url(r'^talk/(?P<talk_id>\d+)/photo/new$', 'talks.views.talk_photo_new'),
    url(r'^talk/(?P<talk_id>\d+)/link/new$', 'talks.views.talk_link_new'),
    url(r'^talk/(?P<talk_id>\d+)/link/(?P<link_id>\d+)/delete$', 'talks.views.talk_link_delete'),

    url(r'^talks$', 'talkevents.views.talk_event_list'),
    url(r'^talk_event/(?P<talk_event_id>\d+)/attend$', 'talkevents.views.talk_event_attendee_new'),

    url(r'^speakers/$', 'core.views.speaker_list'),

    url(r'^', include('talkevents.urls')),
    url(r'^', include('core.urls')),

    url(r'^location/new$', 'locations.views.location_new'),

    url(r'^blog$', 'blog.views.blog_list'),
    url(r'^blog/(?P<post_id>\d+)$', 'blog.views.blog_details'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
