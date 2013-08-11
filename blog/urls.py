from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'blog$', 'blog.views.blog_list'),
    url(r'blog/(?P<post_id>\d+)$', 'blog.views.blog_details'),
)
