from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mobile.views.index'),
    url(r'^login/$', 'mobile.views.login'),
    url(r'^register/$', 'mobile.views.register'),

    url(r'^search/$', 'mobile.views.search'),
    url(r'^speakers/$', 'mobile.views.speakers'),
    url(r'^profile/$', 'mobile.views.profile'),

    url(r'^event/(?P<event_id>\d+)/$', 'mobile.views.event_detail'),
)
