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
    url(r'^', include('talks.urls')),

    url(r'^talks$', 'talks.views.talk_list'),
    url(r'^speakers$', 'core.views.speaker_list'),

    url(r'^', include('engagements.urls')),
    url(r'^', include('core.urls')),

    url(r'^location/new$', 'locations.views.location_new'),

    url(r'^', include('blog.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
