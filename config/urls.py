from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.views import TalkList

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TalkList.as_view()),
    url(r'^talk/new/$', 'core.views.talk_new'),

    url(r'^profile/$', 'core.views.profile'),
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
