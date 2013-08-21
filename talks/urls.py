from django.conf.urls import patterns, url

from views import TalkDetail, TalkTagList, TalkTagDetail
from views import TalkLinkList, TalkLinkDetail
from views import TalkCommentList, TalkCommentDetail

urlpatterns = patterns('',
    url(r'^rest_talk/(?P<talk_id>\d+)/comment/(?P<pk>\d+)$', TalkCommentDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest_talk/(?P<talk_id>\d+)/comment$', TalkCommentDetail.as_view(
        actions={'post': 'create'})),
    url(r'^rest_talk/(?P<talk_id>\d+)/comments$', TalkCommentList.as_view()),

    url(r'^rest_talk/(?P<talk_id>\d+)/tag/(?P<pk>\d+)$', TalkTagDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest_talk/(?P<talk_id>\d+)/tag$', TalkTagDetail.as_view(
        actions={'post': 'create'})),
    url(r'^rest_talk/(?P<talk_id>\d+)/tags$', TalkTagList.as_view()),

    url(r'^rest_talk/(?P<talk_id>\d+)/link/(?P<pk>\d+)$', TalkLinkDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest_talk/(?P<talk_id>\d+)/link$', TalkLinkDetail.as_view(
        actions={'post': 'create'})),
    url(r'^rest_talk/(?P<talk_id>\d+)/links$', TalkLinkList.as_view()),

    url(r'^rest_talk/(?P<pk>\d*)$', TalkDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),

    url(r'^talk/new$', 'talks.views.talk_new'),
    url(r'^talk/(?P<talk_id>\d+)$', 'talks.views.talk_detail'),
    url(r'^talk/(?P<talk_id>\d+)/edit$', 'talks.views.talk_edit'),
    url(r'^talk/(?P<talk_id>\d+)/delete$', 'talks.views.talk_delete'),

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
)
