from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mobile.views.index'),
    url(r'^login/$', 'mobile.views.login_user'),
    url(r'^logout/$', 'mobile.views.logout_user'),
    url(r'^register/$', 'mobile.views.register_user'),

    url(r'^search/$', 'mobile.views.search'),
    url(r'^speakers/$', 'mobile.views.speakers'),
    url(r'^profile/$', 'mobile.views.profile'),

    url(r'^event/(?P<event_id>\d+)/$', 'mobile.views.event_detail'),
)
