from django.conf.urls import patterns, url

from views import TalkDetail, TalkTagList, TalkTagDetail

urlpatterns = patterns('',

    url(r'^rest_talk_tag/(?P<pk>\d*)', TalkTagDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),

    url(r'^rest_talk/(?P<pk>\d+)/tags', TalkTagList.as_view()),
    url(r'^rest_talk/(?P<pk>\d*)', TalkDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),

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
)
