from django.conf.urls import patterns, url
from views import UserTagList
from views import UserDetail, UserTagDetail, UserLinkDetail
from views import NotificationDetail, NotificationList

urlpatterns = patterns('',
    url(r'^profile/invite/thanks$', 'core.views.profile_invite_thanks'),
    url(r'^profile/invite$', 'core.views.profile_invite'),
    url(r'^profile/photo$', 'core.views.profile_photo'),

    url(r'^profile/(?P<id>\d+)$','core.views.profile_detail'),

    url(r'^rest/user_tags$', UserTagList.as_view()),
    url(r'^rest/user_tag/(?P<pk>\d+)$', UserTagDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/user_tag$', UserTagDetail.as_view(
        actions={'post': 'create'})),

    url(r'^rest/user_link/(?P<pk>\d+)$', UserLinkDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/user_link$', UserLinkDetail.as_view(
        actions={'post': 'create'})),

    url(r'^user/(?P<username>\w+)/follow$', 'core.views.user_follow'),
    url(r'^user/(?P<user_id>\d+)/note/(?P<pk>\d+)$', NotificationDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^user/(?P<user_id>\d+)/note$', NotificationDetail.as_view(
        actions={'post': 'create'})),
    url(r'^user/(?P<user_id>\d+)/notes$', NotificationList.as_view()),

    url(r'^rest/user/(?P<pk>\d+)$', UserDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),

    url(r'^events$', 'core.views.event_list'),
    url(r'^event/(?P<slug>[\w+-]*)$', 'core.views.event_detail'),

    url(r'^login$', 'core.views.login_user'),
    url(r'^logout$', 'core.views.logout_user'),
    url(r'^register$', 'core.views.register_user'),
    url(r'^forgot$', 'django.contrib.auth.views.password_reset', {
        'template_name': "auth/password_reset.haml",
        'email_template_name': "mail/password_reset.html",
        'subject_template_name': "mail/password_reset_subject.txt",
        'post_reset_redirect': '/' }),
    url(r'^forgot-confirm/(?P<uidb36>\w+)/(?P<token>[\d\w-]+)$', 
            'django.contrib.auth.views.password_reset_confirm', {
                'template_name': "auth/password_reset_confirm.haml",
                'post_reset_redirect': '/login'
                }),
)
