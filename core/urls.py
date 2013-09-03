from django.conf.urls import patterns, url
from views import UserDetail, NotificationDetail, NotificationList, CommentDetail

urlpatterns = patterns('',
    url(r'^profile/invite/thanks$', 'core.views.profile_invite_thanks'),
    url(r'^profile/invite$', 'core.views.profile_invite'),
    url(r'^profile/edit/photo$', 'core.views.profile_edit_photo'),
    url(r'^profile/edit/link/new$', 'core.views.profile_link_new'),
    url(r'^profile/edit/link/(?P<link_id>\d+)/delete$', 'core.views.profile_link_delete'),
    url(r'^profile/edit/tag/new$', 'core.views.profile_tag_new'),
    url(r'^profile/edit/tag/(?P<tag_id>\d+)/delete$', 'core.views.profile_tag_delete'),

    url(r'^profile/edit$', 'core.views.profile_edit'),
    url(r'^profile/(?P<username>\w+)$', 'core.views.profile_detail'),

    url(r'^user/(?P<username>\w+)/follow$', 'core.views.user_follow'),
    url(r'^user/(?P<user_id>\d+)/note/(?P<pk>\d+)$', NotificationDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^user/(?P<user_id>\d+)/note$', NotificationDetail.as_view(
        actions={'post': 'create'})),
    url(r'^user/(?P<user_id>\d+)/notes$', NotificationList.as_view()),

    url(r'^comment/(?P<pk>\d+)$', CommentDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^comment$', CommentDetail.as_view(
        actions={'post': 'create'})),

    url(r'^user/(?P<pk>\d+)$', UserDetail.as_view()),

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
    
    url(r'^register/speaker$', 'core.views.register_speaker'),
    url(r'^register/attendee$', 'core.views.register_attendee'),
    url(r'^register/event$', 'core.views.register_event'),
)
