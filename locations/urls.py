from django.conf.urls import patterns, url

from views import LocationList, LocationDetail

urlpatterns = patterns('',
    url(r'^rest/location/(?P<pk>\d+)$', LocationDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/location$', LocationDetail.as_view(
        actions={'post': 'create'})),
    url(r'^rest/locations$', LocationList.as_view()),
)